"""Sanitizacao de segredos em logs, erros e URLs. Usada em todo lugar que
possa acabar em stdout, arquivo de saida ou excecao.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_SECRET_PARAM_NAMES = {
    "access_token",
    "app_secret",
    "client_secret",
    "authorization",
}

_BEARER_RE = re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]+=*", re.IGNORECASE)


def redact_url(url: str) -> str:
    """Remove valores de parametros de query sensiveis de uma URL, mantendo
    a URL legivel para diagnostico (host, path, demais parametros)."""
    parts = urlsplit(url)
    query_pairs = parse_qsl(parts.query, keep_blank_values=True)
    redacted_pairs = [
        (k, "***" if k.lower() in _SECRET_PARAM_NAMES else v) for k, v in query_pairs
    ]
    new_query = urlencode(redacted_pairs)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))


def redact_text(text: str) -> str:
    """Remove tokens Bearer e sequencias que parecam token/segredo de um
    texto livre (mensagens de erro, corpo de resposta, etc.)."""
    text = _BEARER_RE.sub("Bearer ***", text)
    return text


def redact_mapping(data: dict[str, Any]) -> dict[str, Any]:
    """Retorna uma copia rasa de um dict com valores de chaves sensiveis
    substituidos por '***'. Usado antes de logar payloads/params."""
    redacted: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in _SECRET_PARAM_NAMES:
            redacted[key] = "***"
        else:
            redacted[key] = value
    return redacted


def token_fingerprint(token: str | None) -> str:
    """Fingerprint curta e nao reversivel de um token, so para conferir
    que dois valores sao o mesmo token sem exibi-lo. Nunca usar para
    reconstruir o token."""
    if not token:
        return "AUSENTE"
    import hashlib

    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:8]}"
