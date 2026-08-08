"""Constroi o HotLink final que o CTA usa (etapa 11/13 do runbook).

Nunca substitui o link publico do produto pelo HotLink de afiliado (a base
ja E o HotLink -- ela e o link de atribuicao de comissao). So adiciona
`src` e o subconjunto de UTMs documentado, preservando qualquer parametro
legitimo ja existente na URL base. Usa urllib.parse -- nunca concatenacao
manual de query string."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .params import HOTMART_FORWARDED_PARAMS


def build_hotlink(base_url: str, *, src: str, campaign_params: dict[str, str]) -> str:
    parts = urlsplit(base_url)
    existing_pairs = parse_qsl(parts.query, keep_blank_values=True)

    overrides: dict[str, str] = {"src": src}
    for key in HOTMART_FORWARDED_PARAMS:
        value = campaign_params.get(key)
        if value:
            overrides[key] = value

    merged: list[tuple[str, str]] = [
        (k, v) for k, v in existing_pairs if k not in overrides
    ]
    merged.extend(overrides.items())

    new_query = urlencode(merged)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))
