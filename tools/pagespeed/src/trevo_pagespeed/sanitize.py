"""Sanitizacao da API key em logs, erros e URLs. Usada em todo lugar que
possa acabar em stdout, arquivo de saida ou excecao. Espelha
tools/instagram/src/trevo_instagram/sanitize.py, adaptado ao parametro
`key` que a Google usa nas APIs PageSpeed/CrUX (em vez de access_token).
"""

from __future__ import annotations

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_SECRET_PARAM_NAMES = {"key", "api_key", "apikey"}

# Chaves de API do Google (AIza...) tem um prefixo estavel e reconhecivel;
# cobre o caso de a chave aparecer solta dentro de uma mensagem de erro em
# vez de como parametro de query estruturado.
_GOOGLE_KEY_RE = re.compile(r"AIza[0-9A-Za-z_-]{10,}")


def redact_url(url: str) -> str:
    """Remove o valor do parametro `key` (e equivalentes) de uma URL,
    mantendo o resto legivel para diagnostico (host, path, demais
    parametros)."""
    parts = urlsplit(url)
    query_pairs = parse_qsl(parts.query, keep_blank_values=True)
    redacted_pairs = [
        (k, "***" if k.lower() in _SECRET_PARAM_NAMES else v) for k, v in query_pairs
    ]
    new_query = urlencode(redacted_pairs)
    redacted = urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))
    return _GOOGLE_KEY_RE.sub("AIza***", redacted)


def redact_text(text: str) -> str:
    """Remove chaves de API do Google que aparecam soltas num texto livre
    (mensagens de erro, corpo de resposta, etc.)."""
    return _GOOGLE_KEY_RE.sub("AIza***", text)


def key_fingerprint(key: str | None) -> str:
    """Fingerprint curta e nao reversivel da chave, so para conferir que
    dois valores sao a mesma chave sem exibi-la. Nunca usar para
    reconstruir a chave."""
    if not key:
        return "AUSENTE"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:8]}"
