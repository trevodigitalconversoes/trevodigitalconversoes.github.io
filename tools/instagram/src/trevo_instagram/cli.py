"""CLI local. Todos os comandos sao read-only por padrao, exceto
`publish`, que exige dupla confirmacao mecanica (ver publishing.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import auth, publishing
from .config import Config
from .media import validate_media
from .models import Manifest, ManifestError
from .publishing import PublishBlockedError, PublishNotConfirmedError
from .state import StateStore

TOOL_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE_DIR = TOOL_ROOT / ".instagram-state"
DEFAULT_OUTPUT_DIR = TOOL_ROOT / ".instagram-output"


def _print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def cmd_inspect(args: argparse.Namespace) -> int:
    config = Config.from_env()
    result = auth.inspect(config)
    _print_json(
        {
            "status": result.status,
            "token_fingerprint": result.token_fingerprint,
            "ig_user_id": result.ig_user_id,
            "username": result.username,
            "account_type": result.account_type,
            "error": result.error,
        }
    )
    return 0 if result.is_ready else 1


def cmd_validate_media(args: argparse.Namespace) -> int:
    result = validate_media(Path(args.file))
    _print_json(
        {
            "path": str(result.path),
            "exists": result.exists,
            "sha256": result.sha256,
            "file_size_bytes": result.file_size_bytes,
            "format": result.format,
            "width": result.width,
            "height": result.height,
            "aspect_ratio": result.aspect_ratio,
            "errors": result.errors,
            "warnings": result.warnings,
            "is_valid_for_publish": result.is_valid_for_publish,
        }
    )
    return 0 if result.is_valid_for_publish else 1


def cmd_prepare(args: argparse.Namespace) -> int:
    try:
        manifest = Manifest.load(Path(args.manifest))
    except ManifestError as exc:
        _print_json({"status": "MANIFEST_INVALID", "error": str(exc)})
        return 1

    state_dir = Path(args.state_dir) if args.state_dir else DEFAULT_STATE_DIR
    state_store = StateStore(state_dir)
    plan = publishing.prepare(manifest, state_store)

    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR
    run_dir = output_dir / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)

    plan_dict = plan.to_dict()
    (run_dir / "plan.json").write_text(
        json.dumps(plan_dict, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    resumo_lines = [
        f"# Plano de publicacao — {manifest.account.name}",
        "",
        f"- Manifesto: `{plan.manifest_path}`",
        f"- Asset: `{plan.asset_path}` (sha256 `{plan.media.sha256}`)",
        f"- Formato/dimensoes: {plan.media.format} {plan.media.width}x{plan.media.height} "
        f"(aspect ratio {plan.media.aspect_ratio})",
        f"- Legenda ({len(plan.caption)} caracteres): {plan.caption[:200]!r}",
        f"- Alt text: {plan.alt_text!r}",
        f"- URL publica planejada: {plan.media_url or '(nao definida)'}",
        f"- Hash de publicacao: `{plan.publication_hash}`",
        f"- Status: **{plan.status.value}**",
    ]
    if plan.media.warnings:
        resumo_lines.append("\n## Avisos")
        resumo_lines += [f"- {w}" for w in plan.media.warnings]
    if plan.blockers:
        resumo_lines.append("\n## Bloqueios")
        resumo_lines += [f"- {b}" for b in plan.blockers]
    (run_dir / "resumo.md").write_text("\n".join(resumo_lines), encoding="utf-8")

    _print_json({**plan_dict, "output_dir": str(run_dir)})
    return 0 if plan.status.value != "BLOCKED" else 1


def cmd_publish(args: argparse.Namespace) -> int:
    try:
        manifest = Manifest.load(Path(args.manifest))
    except ManifestError as exc:
        _print_json({"status": "MANIFEST_INVALID", "error": str(exc)})
        return 1

    config = Config.from_env()
    state_dir = Path(args.state_dir) if args.state_dir else DEFAULT_STATE_DIR
    state_store = StateStore(state_dir)

    try:
        record = publishing.publish(
            manifest,
            config,
            state_store,
            confirm_publish_flag=args.confirm_publish,
            allow_duplicate=args.allow_duplicate,
        )
    except PublishNotConfirmedError as exc:
        _print_json({"status": "PUBLISH_NOT_CONFIRMED", "error": str(exc)})
        return 2
    except PublishBlockedError as exc:
        _print_json({"status": "PUBLISH_BLOCKED", "error": str(exc)})
        return 3

    _print_json(record.to_dict())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="instagram-tool", description="Adaptador local para a Instagram API."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_inspect = sub.add_parser("inspect", help="Verifica credenciais e conta (read-only).")
    p_inspect.set_defaults(func=cmd_inspect)

    p_validate = sub.add_parser("validate-media", help="Valida um arquivo de imagem localmente.")
    p_validate.add_argument("--file", required=True)
    p_validate.set_defaults(func=cmd_validate_media)

    p_prepare = sub.add_parser("prepare", help="Monta o plano de publicacao (dry-run, sem rede).")
    p_prepare.add_argument("--manifest", required=True)
    p_prepare.add_argument("--state-dir", default=None)
    p_prepare.add_argument("--output-dir", default=None)
    p_prepare.set_defaults(func=cmd_prepare)

    p_publish = sub.add_parser(
        "publish", help="Publica de verdade. Exige --confirm-publish e INSTAGRAM_ALLOW_PUBLISH=1."
    )
    p_publish.add_argument("--manifest", required=True)
    p_publish.add_argument("--confirm-publish", action="store_true", default=False)
    p_publish.add_argument("--allow-duplicate", action="store_true", default=False)
    p_publish.add_argument("--state-dir", default=None)
    p_publish.set_defaults(func=cmd_publish)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
