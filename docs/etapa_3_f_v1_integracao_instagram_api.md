# Etapa 3F — Adaptador Instagram/Meta (primeira fatia segura e extraível)

- **Status:** `INSTAGRAM_API_ADAPTER_READY_READ_BLOCKED`. Implementação
  completa, testada e validada até o limite seguro desta fatia; a
  única validação real contra a API (`inspect`) está bloqueada por
  ausência de credenciais no ambiente — o que é esperado nesta etapa
  (nenhuma credencial foi solicitada ao usuário no chat).
- **Objetivo:** primeira fatia extraível de uma futura ferramenta
  independente de publicação social, começando pelo Instagram e pelo
  Post 2 institucional já preparado na etapa 3E.

## Pesquisa oficial (Meta Developers)

Consultado em **2026-08-08**, priorizando documentação oficial sobre
blogs de terceiros:

| Item | Fonte | Resultado |
|---|---|---|
| API recomendada | [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login) | Requer conta profissional (Business/Creator); scopes atuais `instagram_business_basic` + `instagram_business_content_publish` (escopos antigos depreciados em 27/01/2025) |
| Fluxo de publicação | [Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing) | `POST /{ig-user-id}/media` (container) → `GET /{container-id}?fields=status_code` → `POST /{ig-user-id}/media_publish`. Limite: 100 posts publicados via API por período móvel de 24h |
| Host | idem | `graph.instagram.com` (Instagram Login) — confirmado, não hardcoded em mais de um lugar (`config.py`) |
| Restrições de imagem | [IG User /media reference](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media) | Só **JPEG**; aspect ratio 4:5 a 1.91:1; largura 320-1440px (reescalada automaticamente fora da faixa); máx. 8 MB; sRGB |
| Versão da API | [Graph API changelog](https://developers.facebook.com/docs/graph-api/changelog) | Mais recente publicada: **v26.0**. Configurável via `INSTAGRAM_API_VERSION`, default documentado e datado — não hardcoded sem registro |
| Token de longa duração | busca dirigida a developers.facebook.com | `GET graph.instagram.com/access_token` com `grant_type=ig_exchange_token`; token de 60 dias; troca exige app secret e deve ser feita server-side, nunca no navegador |

## Decisão de API

**`Instagram API with Instagram Login`** foi escolhida, conforme a
preferência já indicada na tarefa: reduz dependência de Página do
Facebook, é mais adequada a uma ferramenta futura multi-conta, e
separa a publicação da infraestrutura de Ads. Nenhum bloqueador
específico da conta Trevo foi encontrado que justificasse
`Facebook Login` — não houve necessidade de trocar de abordagem.

## Scopes solicitados (mínimo necessário)

`instagram_business_basic` (identidade) + `instagram_business_content_publish`
(publicação). Nenhum escopo de mensagens, comentários, insights ou
anúncios foi solicitado — não são necessários para esta fatia
(identidade básica + publicação de imagem única).

## Arquitetura

```
tools/instagram/
├── README.md, pyproject.toml, .env.example, .gitignore
├── src/trevo_instagram/
│   ├── config.py, sanitize.py, models.py, client.py,
│   │   auth.py, media.py, state.py, publishing.py, cli.py
├── manifests/
│   ├── post-02-institucional.toml
│   └── post-02-institucional.caption.txt
└── tests/  (13 arquivos, 59 casos)
```

Detalhes completos, incluindo a fronteira exata entre "core
reutilizável" e "configuração do Trevo", estão em
`tools/instagram/README.md` — não duplicados aqui.

**Por que fora do site público:** o Trevo é HTML/CSS estático no
GitHub Pages. Um token de acesso Meta em qualquer arquivo servido
publicamente (HTML, CSS, JS, assets, query string) seria uma exposição
de segredo grave e irreversível assim que indexado/cacheado. Por isso
`tools/instagram/` é uma ferramenta **operacional local**, nunca
importada pelo `index.html`/`produtos/*` nem por nenhum JavaScript
servido ao visitante.

## Segurança

- Zero segredos em HTML/CSS/JS público (nenhum arquivo em
  `tools/instagram/` é referenciado por nenhuma página do site).
- Configuração via `.env` local, nunca commitado (`.gitignore` na raiz
  do repo **e** dentro de `tools/instagram/`, redundante de propósito
  já que a pasta é candidata a extração futura).
- `Config.__repr__`/`__str__` nunca expõe o token bruto (mostra
  `PRESENTE`/`AUSENTE`) — testado.
- Erros de API e URLs passam por `sanitize.py` (`redact_text`,
  `redact_url`) antes de qualquer log/print — testado com um caso que
  contém um "token" fake dentro da mensagem de erro simulada.
- `token_fingerprint()` (SHA-256 truncado, não reversível) é o único
  jeito de "ver" o token nos comandos — nunca o valor bruto.
- Manifestos TOML rejeitam explicitamente chaves de segredo
  (`access_token`, `app_secret`, `client_secret`, `token`) — testado.

## CLI

| Comando | Rede | Descrição |
|---|---|---|
| `inspect` | GET (só leitura) | Confirma token/conta, nunca publica |
| `validate-media --file <f>` | Nenhuma | Valida JPEG/aspect ratio/tamanho/sRGB localmente |
| `prepare --manifest <m>` | Nenhuma | Monta e grava um plano (`.instagram-output/`), calcula hash de idempotência |
| `publish --manifest <m>` | GET+POST, só com dupla confirmação | `--confirm-publish` (CLI) **e** `INSTAGRAM_ALLOW_PUBLISH=1` (ambiente) — faltando qualquer um, aborta antes de qualquer chamada mutável |

### Salvaguardas de `publish` (testadas)

- Zero confirmação → `PublishNotConfirmedError`, nenhuma chamada de rede.
- Só `--confirm-publish` → bloqueado.
- Só `INSTAGRAM_ALLOW_PUBLISH=1` → bloqueado.
- As duas juntas → chega ao cliente HTTP (testado com transporte
  mockado, nunca contra a API real).
- Plano com `blockers` (ex.: `media_url` ausente/local, mídia inválida)
  → `PublishBlockedError`, nunca chega ao cliente, mesmo com as duas
  confirmações presentes.
- Mesmo manifesto já `PUBLISHED` → bloqueado por padrão
  (`--allow-duplicate` força).
- Credenciais ausentes → bloqueado antes do cliente.

## Idempotência

`StateStore` (`.instagram-state/<hash>.json`, ignorado pelo Git) guarda
`publication_hash` (SHA-256 de asset+legenda+conta), `container_id`,
`media_id`, `status`, timestamp. `is_already_published()` é consultado
antes de qualquer publicação real.

## Post 2 institucional — manifesto

`tools/instagram/manifests/post-02-institucional.toml` aponta para
`assets/social/post-02-institucional.jpg` (novo — conversão mecânica
do PNG já existente, ver "Gap encontrado" abaixo), legenda em
`post-02-institucional.caption.txt` (texto idêntico ao já documentado
na etapa 3E, sem copy nova), `alt_text` também reaproveitado. `media_url`
fica **vazio de propósito** — a branch ainda não foi mesclada/deploy,
então a URL pública
`https://trevodigitalconversoes.github.io/assets/social/post-02-institucional.jpg`
**não existe** ainda. `prepare` roda e reporta `BLOCKED` por essa
razão — comportamento correto, não um bug.

### Gap encontrado: formato do asset

O `post-02-institucional.png` gerado na etapa 3E é **PNG**. A
Content Publishing API só aceita **JPEG** para o container de imagem
(confirmado na documentação oficial). `validate-media` já reporta essa
rejeição corretamente. Gerado `post-02-institucional.jpg` (conversão
mecânica com Pillow, `quality=92`, mesmo conteúdo visual, sem nenhuma
alteração de design/copy) — `validate-media` confirma: `1080x1350`,
aspect ratio `0.8` (dentro de `4:5`–`1.91:1`), formato `JPEG`, sem
erros. O manifesto do Post 2 referencia o `.jpg`.

## Post 3 (Lightroom)

Não criado. Sem manifesto hardcoded para "post 2" no core — `cli.py`
recebe `--manifest <caminho>` genérico; qualquer manifesto futuro
(inclusive o do Post 3, quando o bloco de criativos da campanha
existir) usa o mesmo código sem alteração.

## Testes

```
59 passed
```

Arquivos: `test_sanitize.py`, `test_config.py`, `test_media.py`,
`test_models.py`, `test_client.py`, `test_auth.py`,
`test_publishing.py`, `test_state.py`. Cobertura conforme lista de
critérios da tarefa: config sem/com token, segredo nunca em repr/log,
`inspect`/`prepare` nunca fazem POST, `validate-media` (arquivo
ausente, JPEG válido, PNG rejeitado, aspect ratio inválido, hash
determinístico), manifesto válido/ausente/TOML inválido/schema
errado/tipo não suportado/segredo proibido, `media_url` ausente/
`file://`/`localhost` rejeitados, criação de container e publish
mockados (sucesso e falha), zero/uma/duas confirmações de publish,
duplicação detectada, timeout sanitizado, Unicode/hashtag na legenda,
legenda vazia permitida.

Gates executados: `pytest` (59/59), `python -m compileall` (limpo),
scan manual de segredos no diff staged (nenhuma ocorrência real —
apenas valores fake em fixtures de teste, ex. `"fake-token"`,
`"super-secret"`). `ruff`/`mypy` não estavam disponíveis neste
ambiente Python local — gate pulado, registrado aqui como gap
conhecido (código segue tipagem e convenções PEP 8 manualmente).

## Validação real (read-only)

```
INSTAGRAM_READ_BLOCKED_MISSING_CREDENTIALS
```

Nenhuma credencial Meta foi solicitada ou fornecida nesta sessão (o
chat nunca é um canal aceitável para compartilhar token — ver
"AÇÃO SUA" em `tools/instagram/README.md`). `instagram-tool inspect`
executado no ambiente real confirma corretamente esse bloqueio, sem
fazer nenhuma chamada de rede (comportamento verificado: retorna antes
de instanciar o cliente HTTP).

## Publicação — confirmação explícita

- Zero `POST /{ig-user-id}/media` real.
- Zero `POST /{ig-user-id}/media_publish` real.
- Zero post publicado.
- Zero conteúdo apagado.
- Zero interação social automatizada (curtir, seguir, comentar, DM).
- Todos os testes de `publish` usam `httpx.MockTransport` — nenhum
  passou perto de `graph.instagram.com`.

## AÇÃO SUA

Se/quando a publicação real for autorizada:

1. Seguir "Setup Meta" em `tools/instagram/README.md` (conta
   profissional → App Meta → Business Login → scopes → token de longa
   duração → `.env` local).
2. Rodar `instagram-tool inspect` e confirmar `INSTAGRAM_READ_READY`.
3. Depois do merge/deploy deste PR, confirmar
   `https://trevodigitalconversoes.github.io/assets/social/post-02-institucional.jpg`
   retorna HTTP 200 com `content-type: image/jpeg`.
4. Preencher `media_url` no manifesto (ou via suporte futuro a
   `--media-url` na CLI) com essa URL confirmada.
5. Rodar `prepare` novamente e confirmar `status: READY`.
6. Só então, humanamente, decidir publicar: `INSTAGRAM_ALLOW_PUBLISH=1`
   + `publish --confirm-publish`.

## Futuro — extração e evolução

Registrado em `tools/instagram/README.md` ("Fronteira de extração").
Fora de escopo desta fatia (não implementado): scheduler/cron, filas,
publicação recorrente, múltiplas contas/projetos, comentários, DMs,
webhooks, insights, Reels, Stories, carrossel, adapters para Facebook/
LinkedIn/TikTok, dashboard/GUI. Extração para um repositório/pacote
próprio (nome ainda não decidido) é o próximo passo natural quando um
segundo projeto/conta precisar da mesma capacidade.

## Documentação

- `tools/instagram/README.md` — manual completo da ferramenta.
- Este arquivo.
- `CLAUDE.md`/`AGENTS.md` — regra durável adicionada (nunca tokens
  Meta no site; publicação social é operação local; publicação real
  exige dupla confirmação).

## Segurança/comercial

- Nenhuma copy comercial nova (legenda/alt text do Post 2 são texto já
  publicado; Post 3 não foi criado).
- Nenhuma chamada mutável real à API do Instagram.
- Nenhum login, publicação, agendamento, DM, "seguir" ou "curtir".
- Nenhum gasto, nenhuma API paga.
- PR permanece **draft — não mesclado**.

## Veredito

**`INSTAGRAM_API_ADAPTER_READY_READ_BLOCKED`**

Não mesclar. Não publicar no Instagram.
