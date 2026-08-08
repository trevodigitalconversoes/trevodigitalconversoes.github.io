"""CLI local. `analyze` e a unica operacao que fala com a rede (PageSpeed
Insights API + CrUX API), sempre leitura (nenhuma API aqui muta estado
remoto)."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .analyze import run_analysis
from .client import PageSpeedApiError, PageSpeedClient
from .config import Config
from .report import build_summary_dict, render_csv_rows, render_dashboard_html, render_markdown_report

TOOL_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = TOOL_ROOT.parent.parent / "evidencias" / "pagespeed"


def _print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _git_commit_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=TOOL_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "desconhecido"


def cmd_analyze(args: argparse.Namespace) -> int:
    config = Config.from_env()
    if not config.has_credentials:
        _print_json({"status": "GOOGLE_PAGESPEED_API_KEY_AUSENTE"})
        return 1

    now = datetime.now(timezone.utc)
    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR
    run_dir = output_dir / now.strftime("%Y%m%d_%H%M%S")
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    saved_raw_files: list[str] = []

    def now_fn() -> datetime:
        return datetime.now(timezone.utc)

    try:
        with PageSpeedClient(config) as client:
            original_run_pagespeed = client.run_pagespeed

            def run_and_save(url: str, strategy: str, categories: list[str]) -> dict:
                raw = original_run_pagespeed(url, strategy, categories)
                idx = sum(1 for f in saved_raw_files if strategy in f) + 1
                path = raw_dir / f"{strategy}_run{idx}.json"
                path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
                saved_raw_files.append(str(path))
                return raw

            client.run_pagespeed = run_and_save  # type: ignore[method-assign]

            analysis = run_analysis(
                client,
                args.url,
                runs_per_strategy=args.runs,
                now_fn=now_fn,
                sleep_fn=time.sleep,
                inter_call_delay_seconds=args.delay_seconds,
                include_crux=not args.no_crux,
            )
    except PageSpeedApiError as exc:
        _print_json({"status": "PAGESPEED_API_ERROR", "error": str(exc)})
        return 2

    if analysis.crux_page:
        (run_dir / "crux_page.json").write_text(
            json.dumps(analysis.crux_page.__dict__, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
    if analysis.crux_origin:
        (run_dir / "crux_origin.json").write_text(
            json.dumps(analysis.crux_origin.__dict__, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    meta = {
        "url": args.url,
        "commit_sha": _git_commit_sha(),
        "generated_at_utc": now.isoformat(),
        "baseline_label": "PRE_TRACKING_BASELINE",
    }
    summary = build_summary_dict(analysis, meta)
    (run_dir / "resumo.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )

    markdown = render_markdown_report(analysis, meta)
    (run_dir / "relatorio.md").write_text(markdown, encoding="utf-8")

    csv_rows = render_csv_rows(analysis)
    with (run_dir / "metricas.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    dashboard = render_dashboard_html(summary)
    (run_dir / "dashboard.html").write_text(dashboard, encoding="utf-8")

    _print_json(
        {
            "status": "OK",
            "verdict": summary["verdict"],
            "output_dir": str(run_dir),
            "raw_files": saved_raw_files,
        }
    )
    return 0 if summary["measurement_ok"] else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pagespeed-tool", description="Baseline de performance via PageSpeed Insights API + CrUX."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Executa a analise completa (mobile+desktop, N runs).")
    p_analyze.add_argument("--url", required=True)
    p_analyze.add_argument("--runs", type=int, default=3)
    p_analyze.add_argument("--delay-seconds", type=float, default=2.0)
    p_analyze.add_argument("--output-dir", default=None)
    p_analyze.add_argument("--no-crux", action="store_true", default=False)
    p_analyze.set_defaults(func=cmd_analyze)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
