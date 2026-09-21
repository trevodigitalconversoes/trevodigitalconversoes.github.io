# Etapa 1A v1 — Pesquisa de fontes (Grávida Estilosa)

Data das consultas: 21/09/2026. Somente leitura, fontes públicas.

| # | Fonte | URL / consulta | Resultado | Informação encontrada | Confiabilidade | Sustenta afirmação pública? |
|---|---|---|---|---|---|---|
| 1 | Wayback CDX, URL exata (http/https, com/sem www, com/sem barra) | `nathconsultoria.com.br/pages/gravida-estilosa` | 0 capturas | nada | n/a | não |
| 2 | Wayback availability | mesmas variantes | `archived_snapshots: {}` | nada | n/a | não |
| 3 | Wayback, domínio | `nathconsultoria.com.br` (matchType=domain) | 1 captura da home: 2024-09-10 21:46:00 (Shopify) | home anterior ao curso; nenhuma menção a "Grávida" | alta (para a data) | não (não trata do produto) |
| 4 | Common Crawl | 30 índices CC-MAIN-2024-18 a 2026-39, `nathconsultoria.com.br/*` | 0 capturas nos índices que responderam; 6 índices deram 502/504 (2025-51, 2025-33, 2024-42, 2024-33, 2024-22, 2024-18) | nada | n/a | não |
| 5 | Site da produtora ao vivo | `https://nathconsultoria.com.br/pages/gravida-estilosa` | falha TLS (`SEC_E_ILLEGAL_MESSAGE`); DNS 23.227.38.65; HTTP retorna 409 | offline | n/a | não |
| 6 | Hotmart página pública (renderizada) | `hotmart.com/pt-br/marketplace/produtos/gravida-estilosa/Q94220392S` | OK | Descrição; formato "Cursos Online e Serviços de Assinatura"; **5 módulos: Boas Vindas, Descubra o seu Estilo, O Corpo da Gestante, Tecidos, Closet**; bio da produtora | alta (fonte oficial atual) | SIM |
| 7 | Hotmart perfil da produtora (mesma página) | idem | OK | "formada pela Escola de Moda Denise Aguiar, graduanda em Moda pela Faculdade Estácio" — **conflita** com "graduada em moda" na descrição do produto | alta, mas conflitante | parcial (evitar afirmar graduação) |
| 8 | Hotmart checkout | `pay.hotmart.com/Q94220392S?off=xkc2j92m` (não finalizado) | OK | Autor "Nath Consultoria de Imagem e Estilo"; R$ 197,00 à vista; 12x R$ 20,37 (com acréscimo); nenhuma menção a garantia | alta em 21/09/2026 | SIM, datado |
| 9 | Busca web | título + criadora | 1 snippet | reafirma descrição da Hotmart; snippet do site da produtora sem conteúdo acessível | média | só o que repete a fonte 6 |
| 10 | Vídeo/transcrição de divulgação fornecido pelo usuário | 8 partes ZIP em Downloads (existem localmente); transcrição fornecida | usada a transcrição; vídeo não recomposto/analisado | menciona closet cápsula, guia de looks, dois provadores, puerpério e amamentação (conteúdo futuro) | média (promessa da época da gravação) | NÃO como entrega atual; só citado como "citado no vídeo, não confirmado" |
| 11 | Histórico local/GitHub | repos `trevodigitalconversoes.github.io`, `trevo-ops`, `trevo-digital-conversoes` | 0 ocorrências de "gravida"/"nathconsultoria"/"Q94220392S" | nada | n/a | não |
| 12 | HotLink base | `go.hotmart.com/H106516913T` | 302 → `nathconsultoria.com.br/pages/gravida-estilosa?ref=H106516913T` (destino quebrado); seta cookies Hotmart | ver bloqueio | alta | n/a |
| 13 | HotLink com `redirectionUrl` | para hotmart.com marketplace, para pay.hotmart.com | **HTTP 400** nos dois | Hotmart rejeita destino que não seja o domínio da produtora | alta | n/a |

## Conclusão
- Recuperação histórica da página da produtora: **falhou** (sem snapshots; sem WARC). Não bloqueia.
- Fonte oficial atual utilizável: Hotmart (página pública + checkout).
- Google Search/Bing "cache" não foram usados (indisponível/descontinuado).
