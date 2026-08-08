# Etapa 3C — Remoção de `/aprovacao/` e promoção de "+100 Aplicativos Úteis"

- **Status:** `TREVO_ALL_PAGES_READY_FOR_VISUAL_QA`. QA técnico
  completo; aprovação visual/humana ainda pendente.
- **Objetivo:** eliminar completamente o namespace `/aprovacao/` do
  repositório (decisão canônica nova — não existe mais fluxo público
  de aprovação/revisão/rascunho/staging) e promover a única página que
  ainda vivia lá, "+100 Aplicativos Úteis para Produtividade
  Empreendedora", para `/produtos/100-aplicativos-uteis/`, como página
  de produção.

## Inventário original de `/aprovacao/`

```
aprovacao/index.html
aprovacao/README.md
aprovacao/100-aplicativos-uteis/index.html
aprovacao/100-aplicativos-uteis/styles.css
aprovacao/100-aplicativos-uteis/favicon.svg
aprovacao/100-aplicativos-uteis/og-image.svg
aprovacao/100-aplicativos-uteis/fonts/*.woff2 (7 arquivos)
aprovacao/100-aplicativos-uteis/README.md
aprovacao/100-aplicativos-uteis/docs/compliance.md
aprovacao/100-aplicativos-uteis/docs/decisao_migracao_html_estatico.md
```

Classificação:

| Item | Classe | Destino |
|---|---|---|
| `index.html`, `styles.css`, `favicon.svg`, `og-image.svg`, `fonts/*` | A — página/asset de produção | `produtos/100-aplicativos-uteis/` |
| `README.md`, `docs/compliance.md`, `docs/decisao_migracao_html_estatico.md` | B — documentação histórica/técnica | `docs/100-aplicativos-uteis/` |
| `aprovacao/index.html`, `aprovacao/README.md` | C — obsoleto (mensagem genérica e convenção de uma área que não existe mais) | Removido |

Nenhum item foi classificado como redundante sem migração — tudo em A
e B foi preservado (movido, não copiado e duplicado).

## Arquivos migrados (produção)

`git mv` preservando histórico:

- `aprovacao/100-aplicativos-uteis/index.html` → `produtos/100-aplicativos-uteis/index.html`
- `aprovacao/100-aplicativos-uteis/styles.css` → `produtos/100-aplicativos-uteis/styles.css`
- `aprovacao/100-aplicativos-uteis/favicon.svg` → `produtos/100-aplicativos-uteis/favicon.svg`
- `aprovacao/100-aplicativos-uteis/og-image.svg` → `produtos/100-aplicativos-uteis/og-image.svg`
- `aprovacao/100-aplicativos-uteis/fonts/` → `produtos/100-aplicativos-uteis/fonts/` (7 arquivos `.woff2`)

## Documentação preservada (fora da pasta pública do produto)

- `aprovacao/100-aplicativos-uteis/README.md` → `docs/100-aplicativos-uteis/README.md`
- `aprovacao/100-aplicativos-uteis/docs/compliance.md` → `docs/100-aplicativos-uteis/compliance.md`
- `aprovacao/100-aplicativos-uteis/docs/decisao_migracao_html_estatico.md` → `docs/100-aplicativos-uteis/decisao_migracao_html_estatico.md`

Os três arquivos foram atualizados para: apontar para o novo caminho
(`produtos/100-aplicativos-uteis/`), remover pendências já resolvidas
(data de verificação, `robots`, aprovação de produtora) e registrar a
data/fonte da revalidação comercial (ver abaixo).

## Arquivos removidos

- `aprovacao/index.html` (mensagem genérica da extinta área de
  revisão — sem função sem `/aprovacao/`).
- `aprovacao/README.md` (convenção operacional de uma pasta que não
  existe mais).
- Toda a árvore `aprovacao/` foi removida do filesystem após a
  migração (`rm -rf aprovacao` local, seguido de `git rm` para os
  itens ainda rastreados).

## Correção de metadata (produção)

Em `produtos/100-aplicativos-uteis/index.html`:

| Campo | Antes | Depois |
|---|---|---|
| Comentário HTML | `<!-- Rascunho aguardando aprovação da produtora... -->` | Removido |
| `robots` | `noindex,nofollow` | `index,follow` |
| `canonical` | `.../aprovacao/100-aplicativos-uteis/` | `.../produtos/100-aplicativos-uteis/` |
| `og:url` | `.../aprovacao/...` | `.../produtos/...` |
| `og:image` | `.../aprovacao/.../og-image.svg` | `.../produtos/.../og-image.svg` |
| `twitter:image` | `.../aprovacao/.../og-image.svg` | `.../produtos/.../og-image.svg` |
| Seção "Avisos importantes" | "Esta página é um rascunho... Pode ser ajustada conforme orientação da produtora antes de qualquer campanha." | "Esta é uma página independente de pré-venda/review por afiliado, com base nas informações públicas observadas na página do produto na Hotmart." |
| Política de Privacidade (rodapé) | "...Se alguma ferramenta de medição for adicionada no futuro, esta política deverá ser atualizada antes da publicação." | Frase removida (nota operacional interna, não conteúdo para o visitante — mesma correção já aplicada à pre-sell de fotografia na etapa 3A-v2) |
| "Dados observados em" | `[INSERIR_DATA_DE_VERIFICACAO]` | `07/08/2026` (verificação real, ver abaixo) |

Busca automatizada por `rascunho`, `INSERIR_DATA`, `aprovacao`,
`noindex` no HTML final: nenhuma ocorrência.

## Fatos comerciais revalidados

**Fonte:** página oficial do produto no marketplace da Hotmart —
`https://hotmart.com/pt-br/marketplace/produtos/100-aplicativos-uteis-para-produtividade-empreendedora/N87977370D`
(URL pública, extraída do próprio `redirectionUrl` já documentado no
hotlink de afiliado; **não é** o hotlink de afiliado em si, nenhum
clique foi dado nele, nenhuma atribuição de afiliado foi gerada por
essa visita).

**Data da verificação:** 07/08/2026.

| Fato | Valor observado na página oficial (07/08/2026) | Valor já publicado na página do Trevo | Bate? |
|---|---|---|---|
| Preço | R$ 69,90 | R$ 69,90 | Sim |
| Garantia | 7 dias | 7 dias | Sim |
| Criadora | Camila Silveira | Camila Silveira | Sim |
| Tempo na Hotmart | "7 Ano Hotmarter" (~7 anos) | "7 anos de atuação na plataforma" | Sim |
| Formato | eBooks ou Documentos | "Produto digital (computador, celular, tablet)" | Consistente (não é uma contradição, mas o detalhe "computador, celular, tablet" não foi re-confirmado explicitamente nesta visita) |

Os dois campos da tabela "Informações observadas na Hotmart" que não
foram re-confirmados explicitamente nesta visita ("Acesso: Enviado por
email", "Página oficial: Botão 'Ir para o carrinho' na Hotmart" — este
último **foi** confirmado, o botão existe) foram mantidos como estavam
por não contradizerem nada observado e por não serem dados específicos
e verificáveis de forma isolada na página pública do marketplace (são
mecânica padrão da Hotmart). Nenhum dado foi inventado ou alterado sem
base — a única mudança de conteúdo factual foi preencher a data de
verificação, já que os valores existentes se confirmaram.

Nenhum contato com a produtora foi feito. Nenhuma compra, checkout ou
clique no hotlink de afiliado foi realizado.

## Home e catálogo — 2 produtos

- `index.html` (home), seção "Produtos anunciados": agora lista dois
  cards — "10 Dicas de Fotografia + 18 Presets de Lightroom" (já
  existente) e "+100 Aplicativos Úteis para Produtividade
  Empreendedora" (novo). Mesmo padrão visual (`.product-card`),
  imagem oficial (`og-image.svg` do produto), descrição factual
  reaproveitada literalmente do `index.html` da própria página
  (parágrafo `lead` do hero), CTA neutro "Conhecer o produto"
  apontando para a página interna — nunca o hotlink direto no card.
- `produtos/index.html` (catálogo): mesmo card replicado, grid
  `repeat(auto-fill, minmax(280px, 1fr))` já preparado para crescer
  além de 2 produtos sem alteração estrutural.

## `/aprovacao/` — confirmação de remoção total

```
git ls-files aprovacao
```

retorna vazio. `Test-Path aprovacao` (PowerShell) retorna `False`. A
pasta não existe mais no filesystem nem no índice do git.

## Auditoria de referências

Busca repositório inteiro por `/aprovacao/`, `aprovacao/`, `aprovação`,
`aguardando aprovação`, `link de revisão`, `produtora`. Resultado:

- **HTML público:** nenhuma ocorrência de `/aprovacao/` ou de
  instrução para usá-lo. Ocorrências de "produtora"/"aprovação" nas
  páginas públicas (`index.html` raiz, `termos-de-uso.html`,
  `produtos/fotografia-presets-lightroom/`,
  `produtos/100-aplicativos-uteis/`) são sobre a relação de afiliação
  com o produtor de cada produto específico (disclosure, "não sou a
  produtora do conteúdo", "sem promessa de aprovação/resultado") —
  não sobre o fluxo removido.
- **`CLAUDE.md`, `AGENTS.md`, `docs/ADR_PRESELL_OWNERSHIP.md`,
  `README.md`:** reescritos nesta etapa. Nenhum desses arquivos
  normativos instrui recriar `/aprovacao/`; todos declaram
  explicitamente que a pasta foi removida em 2026-08-07 e que
  `/produtos/` é o único namespace público.
- **Documentos históricos** (`docs/etapa_3_a_v1_migracao_presell_trevo.md`,
  `docs/auditoria_100_aplicativos_uteis.md`,
  `docs/100-aplicativos-uteis/README.md`): mantêm menções a
  `/aprovacao/` ao narrar o que aconteceu naquela etapa/data —
  claramente marcadas como passado (a auditoria recebeu uma nota
  explícita no topo apontando para o caminho atual).

## Inventário final de páginas (7)

| # | Página | URL local (QA) |
|---|---|---|
| 1 | Home | `http://127.0.0.1:8080/` |
| 2 | Catálogo | `http://127.0.0.1:8080/produtos/` |
| 3 | Pre-sell Fotografia | `http://127.0.0.1:8080/produtos/fotografia-presets-lightroom/` |
| 4 | Pre-sell 100 Apps | `http://127.0.0.1:8080/produtos/100-aplicativos-uteis/` |
| 5 | Política de Privacidade | `http://127.0.0.1:8080/politica-de-privacidade.html` |
| 6 | Termos de Uso | `http://127.0.0.1:8080/termos-de-uso.html` |
| 7 | Experiência 404 | `http://127.0.0.1:8080/404.html` (rota inexistente testada: `/__visual_qa_404_inexistente__/`) |

## QA técnico (todas as 7 páginas)

| Página | Desktop 1440 | Tablet 768 | Mobile 375 | Console | Overflow | Assets/Links |
|---|---|---|---|---|---|---|
| Home | OK (1425px real) | OK (753px real) | OK | 0 erros | Nenhum | 2 cards, links 200 |
| Catálogo | OK | OK | OK | 0 erros | Nenhum | 2 cards, links 200, sem directory listing |
| Pre-sell Fotografia | OK | — (sem alteração nesta etapa) | — (sem alteração nesta etapa) | 0 erros | Nenhum | Sem regressão |
| Pre-sell 100 Apps | OK | OK | OK | 0 erros | Nenhum | Favicon/og-image/CSS/fonts 200; CTAs corretos |
| Política de Privacidade | OK | — | — | 0 erros | Nenhum | Link de volta OK |
| Termos de Uso | OK | — | — | 0 erros | Nenhum | — |
| 404 | OK (arquivo válido) | — | — | erro de rede esperado só na rota inexistente testada | — | `404.html` carrega 200 quando acessado diretamente |

**Nota sobre o teste de 404:** o servidor local (`python -m
http.server`) não replica o roteamento de 404 do GitHub Pages (que
serve `404.html` automaticamente para qualquer rota inexistente) — no
simulador local, uma rota inexistente retorna a página de erro padrão
do próprio servidor Python, não `404.html`. O arquivo `404.html` em si
foi verificado diretamente (`GET /404.html` → 200, sem erros de
console, link de volta para a home funcional) e seu conteúdo/config já
existia antes desta etapa, sem alteração.

Busca por termos de rascunho/QA/placeholder/TODO/docs internos/
directory listing nas 7 páginas: nenhuma ocorrência real (falsos
positivos de "TODO" dentro de "Todos" revisados manualmente, como nas
etapas anteriores).

## Visual QA (preparação para `visual-qa-capture`)

Ferramenta em desenvolvimento em outra sessão — não modificada aqui.
Manifesto das 7 URLs canônicas (mesma tabela do inventário final
acima). Quando a ferramenta estiver disponível, cobertura esperada:

- 7 páginas × 3 viewports (desktop/tablet/mobile) × 2 formatos
  (viewport + full page) = **42 screenshots principais**, mais
  segmentos quando necessário (ex.: rodapé, seções `<details>`
  expandidas).

Nenhum QA técnico substitui aprovação visual humana — o estado desta
etapa é `TREVO_ALL_PAGES_READY_FOR_VISUAL_QA`, não "design aprovado".

## Limitações e pendências

- Aprovação visual humana ainda não ocorreu (será feita via upload dos
  screenshots ao ChatGPT pelo usuário, fora desta sessão).
- `visual-qa-capture` ainda não estava pronta nesta execução — apenas
  o manifesto de URLs foi preparado.
- Campos "Acesso" e "Formato" da tabela de dados observados na Hotmart
  não foram individualmente re-confirmados byte a byte contra a página
  oficial nesta revalidação (ver seção "Fatos comerciais
  revalidados").
- Teste de 404 limitado pelo comportamento do servidor local (ver nota
  acima) — o arquivo em si foi validado diretamente.

## Segurança/comercial

- Nenhuma compra, checkout, campanha ou gasto.
- Nenhum clique real em nenhum hotlink de afiliado (Hotmart) em nenhum
  momento desta etapa.
- Nenhum contato com produtora.
- A revalidação de fatos comerciais usou a URL pública do marketplace
  da Hotmart (não o hotlink de afiliado), sem gerar atribuição de
  afiliado.
- PR permanece **draft, não mesclado**.
