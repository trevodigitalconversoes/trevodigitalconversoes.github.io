# Decisão — substituição da SPA React por HTML+CSS estático

## Motivo

A versão anterior desta página (pasta `aprovacao/100-aplicativos-uteis-cs-rascunho/`,
agora removida) era o build publicado de um projeto Vite + React +
TypeScript + Tailwind (`codigo-fonte/`). O `index.html` gerado continha
apenas `<div id="root"></div>` e tags `<script type="module">` —
**nenhum conteúdo aparecia sem JavaScript**. Isso viola um requisito
obrigatório do projeto: a página publicada não pode depender
criticamente de JavaScript para exibir o conteúdo principal (afeta
crawlers que não executam JS, navegadores com JS desabilitado, e
robustez geral).

## O que foi preservado

Todo o **texto/copy** já escrito no projeto React (`src/data/product.ts`,
`faq.ts`, `legal.ts`) foi reaproveitado integralmente no novo
`index.html` estático — nenhuma mensagem, disclaimer, pergunta de FAQ ou
texto da seção "Sobre a criadora" foi reescrito ou enfraquecido. A
paleta de cores e tipografia (Sora + Instrument Sans, tokens de cor
violeta/magenta) também foi preservada em `../styles.css`, a partir de
`codigo-fonte/src/index.css`.

Documentação preservada nesta pasta (`docs/`):
- `copy.md` — cópia de leitura de todo o texto-fonte.
- `compliance.md` — checklist de compliance, adaptado para a versão
  estática (sem menções a React/Vite/variáveis de ambiente).
- `relatorio_auditoria_conversao_v1.md`, `relatorio_ajustes_produtora_v1.md`,
  `relatorio_ajustes_produtora_v2.md`, `relatorio_final_saneamento_v1.md`
  — relatórios históricos do projeto React, mantidos sem alteração como
  registro do processo anterior.

## O que foi removido

- `codigo-fonte/` inteira (projeto Vite+React+TypeScript, `node_modules`,
  scripts de build/validação, `.env.example`) — deixou de ser necessária,
  já que não há mais build. Nada disso estava commitado no repositório
  (pasta `aprovacao/` inteira era `??` no `git status` antes desta
  rodada), então nenhum histórico de commit foi perdido.
- A pasta `100-aplicativos-uteis-cs-rascunho/` foi renomeada/substituída
  por `100-aplicativos-uteis/` (URL final sem o sufixo `-cs-rascunho`,
  conforme decisão do usuário).

## O que mudou na arquitetura

| Antes (React/Vite) | Agora (HTML estático) |
|---|---|
| `<div id="root"></div>` + JS crítico | Todo o conteúdo em HTML puro |
| FAQ com `aria-expanded`/JS | `<details>`/`<summary>` nativo |
| Modal (`LegalModal.tsx`, JS + focus-trap) para Política/Termos/Contato | `<details>`/`<summary>` no rodapé |
| CTA com lógica condicional (`hotlinkBlockedInProduction`) | `<a>` real, sempre navegável, apontando para a URL pública oficial da Hotmart enquanto não há hotlink de afiliado |
| Variáveis `VITE_*` resolvidas em build time | Valores escritos diretamente no HTML (sem build) |
| Ano do rodapé calculado via `<script>` | Ano fixo escrito no HTML (`© 2026`) |
| Fontes via `@fontsource` (pacote npm) | Arquivos `.woff2` copiados para `../fonts/`, servidos localmente, sem CDN |

## Pendências que não mudaram

Independente da arquitetura, continuam pendentes (dependem de informação
externa, não de código):
1. Hotlink de afiliado real da Hotmart (`VITE_HOTMART_HOTLINK` não existe
   mais como conceito — agora é só substituir a URL diretamente nos dois
   `<a>` de CTA em `../index.html`).
2. Data de verificação de preço/garantia na Hotmart.
3. Canal de contato definitivo do Trevo Digital Conversões (hoje aponta
   para `https://trevodigitalconversoes.github.io/#contato`).
4. Aprovação explícita da produtora sobre o conteúdo.
5. Troca de `noindex,nofollow` para `index,follow` — só depois de 1–4.
