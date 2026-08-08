# tools/pagespeed

Ferramenta local, reproduzível e extraível para baseline de performance de
uma página pública via **PageSpeed Insights API v5** (`runPagespeed`) e,
opcionalmente, **Chrome UX Report (CrUX) API v1** (`records:queryRecord`).

Nunca é servida pelo site (GitHub Pages é estático) — roda só na sua
máquina. Segue a mesma convenção de `tools/instagram/`: config local via
`.env` nunca commitado, core sem dependência de HTML/CSS/regras de
campanha do Trevo.

## Finalidade

Medir performance/acessibilidade/best-practices/SEO de uma pre-sell antes
de investir em tráfego pago, com múltiplos runs (para lidar com a
variabilidade natural do Lighthouse), estatística (mediana/pior run) e
achados classificados por impacto (P0/P1/P2/INFO) — sem usar `100/100`
como gate artificial.

## Requisitos

- Python >= 3.11
- Windows 11 (testado), sem dependência de Linux/Docker/WSL
- Uma API key do Google com **PageSpeed Insights API** habilitada
  (Chrome UX Report API é opcional — ver seção "CrUX" abaixo)

Instalação (dentro de `tools/pagespeed/`):

```bash
python -m pip install -e ".[dev]"
```

## `.env`

Copie `.env.example` para `.env` (nunca commitado — já coberto por
`tools/pagespeed/.gitignore`) e preencha:

```
GOOGLE_PAGESPEED_API_KEY=sua_chave_aqui
```

Como obter a chave: [console.cloud.google.com](https://console.cloud.google.com)
→ *APIs & Services* → habilitar **PageSpeed Insights API** → *Credentials*
→ criar uma API key. Restrinja a chave a essa API (e a Chrome UX Report
API, se for usar CrUX).

A ferramenta nunca imprime a chave — `Config.__repr__`/`__str__` só mostram
`PRESENTE`/`AUSENTE`, e qualquer mensagem de erro passa por
`sanitize.redact_text`/`redact_url` antes de chegar ao stdout/arquivo.

### CrUX (opcional)

A mesma chave pode ser usada para a Chrome UX Report API se ela também
estiver habilitada no mesmo projeto do Google Cloud. A ferramenta nunca
cria uma segunda chave automaticamente. Se a API não estiver habilitada
para a chave, a consulta CrUX simplesmente registra o gap
(`NOT_ENABLED`) no relatório — não é tratado como erro fatal, e o resto
da análise (PageSpeed) continua normalmente. Use `--no-crux` para pular
essa etapa de propósito.

## Comandos

```bash
python -m trevo_pagespeed.cli analyze --url "https://trevodigitalconversoes.github.io/produtos/<slug>/" --runs 3
```

Opções:

| Flag | Default | Descrição |
|---|---|---|
| `--url` | obrigatório | URL pública a analisar |
| `--runs` | `3` | Runs por strategy (mobile + desktop = `2 * runs` chamadas) |
| `--delay-seconds` | `2.0` | Intervalo entre chamadas consecutivas (evita rajada) |
| `--output-dir` | `evidencias/pagespeed/` na raiz do repo | Onde salvar a evidência |
| `--no-crux` | desabilitado | Pula as duas consultas CrUX (page + origin) |

Se `GOOGLE_PAGESPEED_API_KEY` estiver ausente, o comando para **antes** de
qualquer chamada de rede e imprime `{"status": "GOOGLE_PAGESPEED_API_KEY_AUSENTE"}`
(exit code 1) — nunca pede para colar a chave em nenhum lugar.

## Outputs

Cada execução cria `evidencias/pagespeed/<timestamp>/`:

```
raw/
  mobile_run1.json .. mobile_run3.json   # resposta bruta de cada runPagespeed
  desktop_run1.json .. desktop_run3.json
crux_page.json                            # se --no-crux nao foi usado
crux_origin.json
resumo.json                               # tudo estruturado (scores, metricas, achados, veredito)
relatorio.md                              # relatorio humano completo
metricas.csv                              # uma linha por run, para planilha/BI
dashboard.html                            # visual autocontido, abre local, sem segredo/JS pesado
```

### Por que `evidencias/` não é versionada

Os 6 JSONs brutos de uma execução somam alguns MB (cada resposta
`runPagespeed` completa, com todos os audits, passa de 600 KB). Isso é
grande demais para versionar a cada execução sem necessidade real — a
evidência é 100% reproduzível rodando `analyze` de novo. `tools/pagespeed/.gitignore`
já ignora `evidencias/`. Se uma execução específica precisar virar
evidência permanente (ex.: anexada a um PR), copie manualmente os arquivos
processados (`resumo.json`, `relatorio.md`, `metricas.csv`) para fora
desse diretório antes de versionar — evite versionar os `raw/*.json`
salvo necessidade explícita.

## Interpretação

- **Scores** são normalizados de 0–1 (retorno nativo da API) para 0–100
  só para apresentação.
- A conclusão prioriza a **mediana** dos runs e sempre mostra o **pior
  run** — resultados de Lighthouse oscilam, uma medição isolada não é
  confiável.
- **Lab data** (Lighthouse, sintético) e **field data** (CrUX, usuários
  reais) aparecem separados — nunca misturados. TBT (lab) é um proxy útil
  de responsividade, mas não é semanticamente o mesmo que INP real.
- **Achados** são classificados por impacto, não por score:
  - `P0` — bloqueia o microteste (score de performance mediano < 50, ou
    LCP mediano mobile > 4s, ou falha de medição).
  - `P1` — corrigir antes do lançamento (economia estimada pela própria
    API >= 300ms ou >= 500 KB; score de categoria < 90; LCP mediano
    entre 2.5s–4s).
  - `P2` — otimizar depois (economia menor, ou score entre 90–99).
  - `INFO` — sem ação necessária.
- Nenhuma economia é inventada: só usamos `overallSavingsMs`/`overallSavingsBytes`
  quando a própria API os retorna, ou a soma dos valores por-item
  (`wastedMs`/`wastedBytes`) quando o audit não traz um agregado — isso é
  agregação de dado real da API, não estimativa nossa.

## Gap conhecido: taxonomia de audits do Lighthouse

O Lighthouse >= 12 substituiu vários audits clássicos (`modern-image-formats`,
`uses-long-cache-ttl`, `render-blocking-resources`,
`largest-contentful-paint-element`, `dom-size`, etc.) por uma taxonomia de
"Insights" com IDs terminados em `-insight` (`image-delivery-insight`,
`cache-insight`, `render-blocking-insight`, `lcp-discovery-insight`,
`dom-size-insight`...). Confirmado na resposta real da API em 2026-08-08
(versão retornada: `13.4.1`). A ferramenta reconhece **ambas** as
taxonomias (`extract.py`), então continua funcionando se uma versão futura
da API voltar a usar os IDs clássicos em algum strategy. Se um audit
esperado não existir em nenhuma das duas taxonomias, o campo correspondente
fica `None` e o relatório mostra `NAO DISPONIVEL NA VERSAO LIGHTHOUSE ATUAL`
em vez de tratar isso como erro.

## Limitações

- `ruff`/`mypy` não estão configurados neste pacote (gap conhecido, mesmo
  padrão de `tools/instagram`).
- CrUX depende de volume de tráfego real suficiente — uma pre-sell nova
  frequentemente não tem dados ainda (`NO_DATA`), o que é esperado e não
  é falha da ferramenta.
- GitHub Pages não permite configurar cache-control customizado por
  arquivo — um achado de "cache lifetime" curto em assets estáticos é uma
  característica da hospedagem, não algo corrigível só no HTML/CSS do
  repo.

## Como repetir a análise

```bash
python -m trevo_pagespeed.cli analyze --url "<URL>" --runs 3
```

Rode de novo sempre que quiser um novo baseline (ex.: depois de otimizar
imagens, ou depois de adicionar tracking).

## Comparar baseline antes/depois de tracking

Cada `resumo.json` tem `meta.baseline_label`. Rode uma vez **antes** de
adicionar PostHog/analytics (`PRE_TRACKING_BASELINE`) e guarde o
`resumo.json`/`relatorio.md` dessa execução. Depois de adicionar o
tracking, rode de novo e compare os scores/métricas medianas dos dois
`resumo.json` lado a lado — a diferença é o custo de performance que o
tracking adicionou.

## Testes

```bash
python -m pytest -q
```

Nenhum teste chama a API real — tudo usa `httpx.MockTransport` ou
fixtures locais. Cobrem: leitura de `.env` (sem sobrescrever variável já
definida), sanitização da chave em URL/erro/repr, parsing de resposta
(incluindo as duas taxonomias de audits), score/audit ausente, CrUX sem
dados/API desabilitada, erro HTTP permanente vs. transitório (retry),
timeout, JSON inválido, cálculo de mediana, classificação de achados
(P0/P1/P2), e geração de relatório/CSV/dashboard sem vazar segredo.

## Segurança

- Zero segredo em HTML/CSS/JS público — esta ferramenta nunca é servida
  pelo site.
- Config só via `.env` local, nunca commitado.
- Toda chamada de rede é **leitura** (GET/POST de consulta, nunca muta
  nada na conta Google) — não há equivalente a `publish` aqui.
