# trevo-instagram — adaptador local para a Instagram API

Ferramenta operacional **local** (não roda no navegador do visitante,
não faz parte do JavaScript do site público) para publicar conteúdo no
Instagram usando a API oficial da Meta. Construída para ser a primeira
fatia de uma futura ferramenta independente, reutilizável por vários
projetos e várias contas sociais — ver "Fronteira de extração" abaixo.

## Finalidade

- Verificar credenciais/conta de forma somente-leitura (`inspect`).
- Validar um arquivo de imagem localmente antes de publicar
  (`validate-media`).
- Montar e revisar um plano de publicação sem tocar a rede
  (`prepare`).
- Publicar de verdade (`publish`) — **desabilitado por padrão**, exige
  dupla confirmação mecânica.

**Nesta primeira fatia, `publish` nunca foi executado contra a conta
real do Trevo.** Ver `docs/etapa_3_f_v1_integracao_instagram_api.md`
no repositório principal para o relatório completo dessa etapa.

## Arquitetura

```
tools/instagram/
├── README.md              (este arquivo)
├── pyproject.toml
├── .env.example
├── .gitignore              (.env, .instagram-state/, .instagram-output/)
├── src/trevo_instagram/
│   ├── config.py            configuração via ambiente, nunca hardcoda segredo
│   ├── sanitize.py          redação de segredos em logs/erros/URLs
│   ├── models.py            manifesto declarativo (TOML) + estados
│   ├── client.py            cliente HTTP isolado (host/versão centralizados)
│   ├── auth.py              inspect() — só GET
│   ├── media.py             validação 100% local de imagem
│   ├── state.py             idempotência local (evita publicar 2x)
│   ├── publishing.py        prepare() (sem rede) e publish() (com salvaguardas)
│   └── cli.py                comandos: inspect / validate-media / prepare / publish
├── manifests/
│   ├── post-02-institucional.toml
│   └── post-02-institucional.caption.txt
└── tests/                   75 testes, sem nenhuma chamada de rede real
```

### Fronteira de extração

**Core reutilizável** (não conhece nada do Trevo além do que recebe
como dado): `config.py`, `sanitize.py`, `models.py`, `client.py`,
`auth.py`, `media.py`, `state.py`, `publishing.py`, `cli.py`.

**Configuração específica do Trevo**: os arquivos em `manifests/`
(caminho do asset, legenda, alt text, nome da conta) e o `.env` local
(nunca commitado). Nenhum desses arquivos é importado pelo core — o
core só recebe um `Manifest` já carregado.

Critério de extração: mover `src/trevo_instagram/` para um repositório
próprio deve ser possível copiando a pasta inteira, sem tocar em HTML/
CSS/regras de campanha do Trevo. Quando isso acontecer, `manifests/`
fica no repositório do Trevo (ou de cada projeto cliente) e passa a
apontar para o pacote publicado (`pip install trevo-instagram` ou
equivalente) em vez de um caminho relativo.

## Requisitos

- Python 3.11+
- Conta Instagram **profissional** (Business ou Creator) — contas
  pessoais não funcionam com a Content Publishing API.
- App Meta configurado (ver "Setup Meta" abaixo).

## Instalação local

```powershell
cd tools/instagram
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Setup Meta — passo a passo

> **AÇÃO SUA.** Estes passos exigem acesso ao painel Meta for
> Developers e à conta Instagram do Trevo — não podem ser feitos por
> um agente de código.

1. Confirme que a conta Instagram do Trevo é **Business** ou
   **Creator** (Configurações do app → Conta → tipo de conta). Se for
   pessoal, converta manualmente antes de continuar — esta ferramenta
   **não** converte contas automaticamente.
2. Acesse [developers.facebook.com](https://developers.facebook.com/)
   e crie (ou reutilize) um App.
3. No painel do App, adicione o produto **Instagram** → **API setup
   with Instagram login** ("Business Login for Instagram").
4. Configure o **Redirect URI** de autorização conforme exigido pelo
   fluxo de Business Login (ver documentação oficial linkada abaixo —
   muda conforme a ferramenta usada para gerar o token; o Graph API
   Explorer da Meta é a forma mais simples para uma conta única).
5. Solicite (ou confirme concedidos) os scopes mínimos:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
   Não peça escopos de mensagens, comentários, insights ou anúncios
   nesta fatia — não são necessários.
6. Gere um **access token de curta duração** (via Graph API Explorer
   ou o fluxo de autorização do App).
7. Troque por um **token de longa duração** (60 dias) — endpoint
   oficial `GET https://graph.instagram.com/access_token` com
   `grant_type=ig_exchange_token`. Este passo exige o app secret e
   **deve ser feito server-side/local, nunca no navegador**.
8. Obtenha o **IG User ID**: `GET https://graph.instagram.com/v26.0/me?fields=id,username&access_token=...`
   (ou use `instagram-tool inspect` depois de colocar o token no `.env`
   — o próprio comando já busca isso).
9. Copie `.env.example` para `.env` dentro de `tools/instagram/` e
   preencha `INSTAGRAM_ACCESS_TOKEN` e `INSTAGRAM_USER_ID`. **Nunca
   cole o token no chat, em um PR, issue ou qualquer lugar público.**
   `.env` já está no `.gitignore` (raiz e local).

Documentação oficial consultada (2026-08-08):
- [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login)
- [Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [IG User /media reference](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media)
- [Graph API changelog](https://developers.facebook.com/docs/graph-api/changelog) (versão vigente)

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `INSTAGRAM_ACCESS_TOKEN` | Sim (para `inspect`/`publish` reais) | Token de usuário de longa duração |
| `INSTAGRAM_USER_ID` | Sim (idem) | IG User ID da conta profissional |
| `INSTAGRAM_API_HOST` | Não | Default `graph.instagram.com` |
| `INSTAGRAM_API_VERSION` | Não | Default `v26.0` (verificado 2026-08-08) |
| `INSTAGRAM_TIMEOUT_SECONDS` | Não | Default `20` |
| `INSTAGRAM_ALLOW_PUBLISH` | Sim, só para publicar de verdade | Precisa ser `1` **e** `publish` precisa receber `--confirm-publish` — as duas coisas juntas |

## Comandos

### `inspect` — somente leitura

```powershell
python -m trevo_instagram.cli inspect
```

Confirma token presente/utilizável, conta encontrada, `username`,
`account_type`. **Nunca imprime o token** — só uma fingerprint SHA-256
truncada e não reversível. Faz apenas `GET /me`.

Resultados possíveis: `INSTAGRAM_READ_READY`,
`INSTAGRAM_READ_BLOCKED_MISSING_CREDENTIALS`,
`INSTAGRAM_READ_BLOCKED_API_ERROR`,
`INSTAGRAM_PROFESSIONAL_ACCOUNT_REQUIRED`.

### `validate-media` — 100% local

```powershell
python -m trevo_instagram.cli validate-media --file ../../assets/social/post-02-institucional.jpg
```

Verifica, sem nenhuma chamada de rede: existência, hash SHA-256,
tamanho de arquivo (máx. 8 MB), formato (**só JPEG** é aceito pela
API — PNG é rejeitado aqui de propósito), dimensões, aspect ratio
(faixa aceita: 4:5 a 1.91:1), espaço de cor.

### `prepare` — dry-run

```powershell
python -m trevo_instagram.cli prepare --manifest manifests/post-02-institucional.toml
```

Resolve o manifesto, valida a mídia, calcula o hash de publicação
(usado para idempotência), monta um plano e grava
`.instagram-output/<timestamp>/plan.json` + `resumo.md` (sem
segredos). **Nunca faz POST.** Se `media_url` não for uma URL
`http(s)` pública (rejeita `file://`, `localhost`, `127.0.0.1`, etc.),
o plano fica `BLOCKED` — isso é esperado antes do deploy do site.

### Configurando `media_url` — antes do deploy

Enquanto a página/branch ainda não foi mesclada e publicada em
`https://trevodigitalconversoes.github.io/...`, é possível testar o
fluxo inteiro (exceto a publicação em si) apontando `media_url` para o
conteúdo já commitado na branch via **raw.githubusercontent.com** —
funciona para qualquer branch de um repositório público, não só
`main`:

```
https://raw.githubusercontent.com/<org>/<repo>/<branch>/<caminho-do-arquivo>
```

Exemplo real usado nesta etapa:

```
https://raw.githubusercontent.com/trevodigitalconversoes/trevodigitalconversoes.github.io/feature/claude/migrar-presell-fotografia-trevo/assets/social/post-02-institucional.jpg
```

Essa URL é **temporária** (fica obsoleta quando a branch for mesclada/
removida) — não é a URL final de produção. Depois do merge/deploy,
troque para
`https://trevodigitalconversoes.github.io/assets/social/post-02-institucional.jpg`.

Se você mantiver um manifesto pessoal com essa URL de teste em vez do
manifesto canônico do post, nomeie-o com o sufixo `.local.toml` (ex.:
`manifests/post-02-institucional.local.toml`) — esse padrão já está no
`.gitignore` da ferramenta, então não é commitado.

`prepare` valida a `media_url` de forma rigorosa e rejeita, com
mensagem de erro explicando o motivo:

- string vazia, `None`, ou só espaço em branco;
- espaço em branco no início/fim (indício de copiar/colar errado);
- qualquer um dos caracteres `[` `]` `(` `)` `\` — cobre o erro comum
  de colar um **link Markdown inteiro** (`[texto](url)`) em vez da URL
  pura, e o erro de escapar o ponto como se fosse regex
  (`raw\.githubusercontent.com`, que não é uma URL válida — o hostname
  correto não tem barra invertida: `raw.githubusercontent.com`);
- texto que pareça um objeto do PowerShell serializado por engano
  (ex.: contém `System.Management.Automation` ou `InternalHost`);
- esquema diferente de `http`/`https`;
- hostname local (`localhost`, `127.0.0.1`, `*.local`) ou sem ponto.

#### Erro comum no PowerShell: `$host` é reservado

Se você tentar montar a URL manualmente com um comando como:

```powershell
$host = "raw.githubusercontent.com"   # ERRADO
```

o PowerShell recusa com
`VariableNotWritable: Não é possível substituir a variável Host porque
ela é somente leitura ou constante`. Isso acontece porque `$Host`
(nomes de variável no PowerShell **não diferenciam maiúsculas de
minúsculas**, então `$host` e `$Host` são a mesma coisa) é uma
variável automática do próprio PowerShell — representa o host do
console (`ConsoleHost`), não é um nome livre para usar. Use qualquer
outro nome:

```powershell
$rawHost = "raw.githubusercontent.com"    # correto -- $Host e reservado
$assetPath = "trevodigitalconversoes/trevodigitalconversoes.github.io/feature/claude/migrar-presell-fotografia-trevo/assets/social/post-02-institucional.jpg"
$rawUrl = "https://$rawHost/$assetPath"
```

Prefira, porém, editar a `media_url` diretamente no arquivo `.toml`
(um editor de texto comum) em vez de reconstruí-la via PowerShell toda
vez — é mais confiável e menos sujeito a esse tipo de erro.

### `publish` — publica de verdade

```powershell
$env:INSTAGRAM_ALLOW_PUBLISH = "1"
python -m trevo_instagram.cli publish --manifest manifests/post-02-institucional.toml --confirm-publish
```

Só chega a fazer qualquer chamada de rede mutável
(`POST /media`, `POST /media_publish`) se **as duas** proteções
estiverem presentes ao mesmo tempo: `--confirm-publish` na linha de
comando **e** `INSTAGRAM_ALLOW_PUBLISH=1` no ambiente. Faltando
qualquer uma delas, aborta antes de tocar a rede
(`PublishNotConfirmedError`).

Fluxo real (uma vez confirmado): `POST /{ig_user_id}/media` →
consulta `status_code` do container até `FINISHED` → `POST
/{ig_user_id}/media_publish`. Se o mesmo manifesto (mesmo hash de
asset+legenda+conta) já tiver sido publicado antes,
`publish` aborta por padrão (`--allow-duplicate` força republicação).

## Segurança

- Nenhum segredo entra em HTML/CSS/JS do site público — esta pasta
  roda apenas localmente.
- Configuração só via variáveis de ambiente (`.env`, nunca
  commitado — ver `.gitignore`).
- `Config.__repr__`/`__str__` nunca imprime o token bruto (mostra
  `PRESENTE`/`AUSENTE`).
- Erros de API passam por `sanitize.redact_text`/`redact_url` antes de
  propagar — nunca incluem `Authorization: Bearer ...` nem
  `access_token=...` em texto legível.
- `access_token` vai sempre como parâmetro de query da própria API (é
  assim que a Instagram API espera), nunca em header `Authorization`
  custom nem em log.
- Manifestos (`.toml`) rejeitam explicitamente chaves como
  `access_token`/`app_secret`/`token` — segredo nunca deve ir em um
  arquivo versionado.

## Troubleshooting

| Sintoma | Causa provável |
|---|---|
| `INSTAGRAM_READ_BLOCKED_MISSING_CREDENTIALS` | `.env` não criado/preenchido, ou variáveis não exportadas na sessão atual |
| `INSTAGRAM_PROFESSIONAL_ACCOUNT_REQUIRED` | Conta Instagram ainda é pessoal — converta manualmente no app |
| `prepare` fica `BLOCKED` por `media_url` | Normal antes do deploy: a URL pública do asset só existe depois do merge/deploy do site |
| `validate-media` rejeita um PNG | Esperado — a API só aceita JPEG; gere uma versão `.jpg` (ex.: `Pillow`, `img.convert("RGB").save(..., "JPEG")`) |
| `publish` retorna `PUBLISH_NOT_CONFIRMED` | Falta `--confirm-publish` e/ou `INSTAGRAM_ALLOW_PUBLISH=1` — as duas são obrigatórias |
| `VariableNotWritable` no PowerShell | Você tentou usar `$host`/`$Host` como nome de variável — é reservado pelo próprio PowerShell (case-insensitive). Use outro nome, ex. `$rawHost` |
| `prepare` rejeita a `media_url` mesmo parecendo "certa" | Confira se não colou um link Markdown inteiro (`[texto](url)`) em vez da URL pura, e se não há barra invertida (`raw\.githubusercontent.com` é inválido — o correto é `raw.githubusercontent.com`, sem `\`) |

## Testes

```powershell
pytest
```

75 testes, nenhum faz chamada de rede real (usam
`httpx.MockTransport`). Cobrem: sanitização de segredos, config sem/
com token, `inspect` read-only, `validate-media` (JPEG válido, PNG
rejeitado, aspect ratio inválido), manifesto válido/inválido/com
segredo proibido, cliente HTTP (GET/POST corretos, erros
sanitizados, timeout), salvaguardas de `publish` (zero confirmação,
uma confirmação, duas confirmações, plano bloqueado, duplicação),
idempotência local, e validação de `media_url` (`test_media_url_validation.py`
+ casos de `prepare` em `test_publishing.py`): aceita URL real de
`raw.githubusercontent.com`, rejeita link Markdown colado por engano,
barra invertida (escape de regex indevido), objeto do PowerShell
serializado, string vazia/espaço, host local.

## Fora de escopo nesta fatia

Scheduler/cron, filas, publicação recorrente, múltiplas contas,
comentários, DMs, webhooks, insights, Reels, Stories, carrossel,
Facebook/LinkedIn/TikTok, dashboard/GUI. Ver
`docs/etapa_3_f_v1_integracao_instagram_api.md` (repositório
principal) para o registro de evolução futura.
