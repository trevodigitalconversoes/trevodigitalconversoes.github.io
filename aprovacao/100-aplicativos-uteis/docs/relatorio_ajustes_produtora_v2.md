# Relatório — correção do fluxo de build e ajustes de tom/contato (v2)

## Contexto

Rodada curta e cirúrgica de correções sobre o projeto já ajustado em
`docs/relatorio_ajustes_produtora_v1.md`. **Nenhuma reescrita do
projeto, da stack ou do layout geral foi feita** — apenas os itens
listados abaixo. Layout, paleta e componentização existentes foram
preservados.

## Arquivos alterados

| Arquivo | Mudança |
|---|---|
| `scripts/clean.mjs` | Novo. Remove `dist/` via `fs.rmSync` (Node), funciona igual no Windows e no Linux/macOS. |
| `scripts/validate-production.mjs` | Refatorado para aceitar um modo (`source` \| `dist`, via `process.argv[2]`). Modo `source` roda as checagens de `.env`/hotlink/URL/copy proibida/forms/links mortos e **nunca** olha `dist/`. Modo `dist` só varre `dist/index.html` em busca de placeholders não resolvidos, e agora falha (não apenas avisa) se `dist/index.html` não existir, pois só deve ser chamado depois de um build. |
| `scripts/package-release.mjs` | `npm run package` agora usa `Compress-Archive` (PowerShell) no Windows em vez de depender do binário `zip`, que não vem instalado por padrão nesse sistema operacional. Em Linux/macOS continua usando `zip`. |
| `package.json` | Novos scripts `clean`, `check:prod:source`, `check:prod:dist`. `build` agora aponta para `build:prod`. `build:prod` passou a ser `clean && check:prod:source && tsc -b && vite build && check:prod:dist`. `check:prod` virou um atalho manual (`check:prod:source && check:prod:dist`), não é mais chamado automaticamente antes do `vite build`. |
| `src/{components,data,lib,hooks}/` | Removido. Diretório vazio com nome literal de brace-expansion não expandida (erro de criação de pastas em um shell sem suporte a `{a,b,c}`), sem relação com as pastas reais `src/components`, `src/data`, `src/lib` (que continuam existindo normalmente). |
| `src/data/product.ts` | `IMPORTANT_NOTICES.intro[1]` reescrito para uma versão mais diplomática, sem mencionar "outros produtos da criadora". `RESPONSIBLE_RECOMMENDATION.title` renomeado de "Minha leitura como afiliado" para "Análise responsável da curadoria". |
| `src/components/CreatorSection.tsx` | Comentário atualizado para refletir o novo título (nenhuma mudança de estrutura/layout). |
| `src/data/legal.ts` | Parágrafo de cookies da Política de Privacidade reescrito para não sugerir rastreamento inexistente (o projeto não usa analytics/pixels). Parágrafo de Contato reescrito para: (1) sempre direcionar dúvidas de produto/compra/pagamento/acesso/garantia à Hotmart; (2) usar o canal do Trevo Digital Conversões (`VITE_CONTACT_URL`) quando configurado, com fallback genérico seguro caso contrário. |
| `src/lib/links.ts` | Novo `CONTACT_URL` (lido de `VITE_CONTACT_URL`, sem fallback inventado) e `hasContactUrl`. |
| `src/vite-env.d.ts` | Tipo `VITE_CONTACT_URL?: string` adicionado. |
| `.env.example` | Nova variável `VITE_CONTACT_URL`, documentada como opcional e sem valor padrão inventado. |
| `README.md` | Seções de scripts/build/validação reescritas para o novo fluxo (`clean`, `check:prod:source`, `check:prod:dist`); nova subseção "Como configurar o contato"; passo a passo de GitHub Pages atualizado com a convenção de pastas `paginas-de-vendas/aguardando-aprovacao/`; checklists atualizados. |
| `docs/copy.md` | Título da seção atualizado; texto do aviso de escopo atualizado; nota sobre Contato/Privacidade adicionada. |
| `docs/wireframe.md` | Referências ao título antigo e ao texto do aviso de escopo atualizadas. |
| `docs/compliance.md` | Seção "Tom com a produtora" corrigida (nome certo da constante `IMPORTANT_NOTICES.intro`) e expandida; nova seção "Política de Privacidade e Contato". |
| `docs/relatorio_ajustes_produtora_v2.md` | Este relatório. |

## Por que o build de produção falhava (causa raiz)

Antes: `"build": "npm run check:prod && tsc -b && vite build"`. O script
`check:prod` (antigo, único) sempre varria `dist/index.html` **se ele já
existisse** — inclusive antes do `vite build` da própria chamada atual.
Se alguém tivesse rodado `npm run build:staging` anteriormente (sem
`.env` real, portanto com placeholders `[INSERIR_...]`/`%VITE_...%` no
HTML gerado), esse `dist/` antigo permanecia em disco. Na próxima vez
que `npm run build` fosse chamado — mesmo com um `.env` de produção
100% correto — `check:prod` rodava **antes** do `vite build` da vez
atual, encontrava os placeholders no `dist/` **antigo**, e abortava o
comando inteiro com `process.exit(1)`. O `vite build` novo nunca chegava
a rodar, então o `dist/` nunca era corrigido — um impasse.

**Correção:** a validação de fonte (`check:prod:source`) nunca depende
de `dist/`. A validação de `dist/` (`check:prod:dist`) só roda depois do
`vite build`, dentro de `build:prod`, que sempre começa com
`npm run clean` (remove `dist/` via Node, sem depender de `rm -rf` do
Unix). Resultado: cada validação sempre vê o estado correto — a fonte
atual, ou o build recém-gerado — nunca um artefato desatualizado.

## Compatibilidade Windows

- `npm run clean` usa `fs.rmSync` do Node (não `rm -rf`), funciona
  identicamente no Windows.
- `npm run package` (`scripts/package-release.mjs`) detecta
  `process.platform === 'win32'` e usa `Compress-Archive` do PowerShell
  (nativo no Windows 10+) em vez do binário `zip`, que não está
  disponível por padrão neste sistema.

## Comandos executados e resultados

Ver seção "Validação" mais abaixo neste repositório (mensagem de
entrega da tarefa) para a saída completa de `npm run lint`,
`npx tsc -b`, `npm run build:staging`, `npm run check:prod:source`,
`npm run build:prod` e `npm run check:prod:dist` (estes dois últimos
rodados com um `.env` fictício e seguro, nunca commitado).

## Pendências antes da publicação

Inalteradas em relação ao relatório anterior — seguem reais e não foram
preenchidas com valores inventados:

1. `VITE_HOTMART_HOTLINK` real.
2. `VITE_SITE_URL` final.
3. `VITE_BASE_PATH` final (depende de onde a página for efetivamente
   publicada dentro do repositório do "Trevo Digital Conversões").
4. `VITE_HOTMART_VERIFICATION_DATE` real.
5. `VITE_CONTACT_URL` real do Trevo Digital Conversões (opcional, mas
   recomendado antes de qualquer divulgação).
6. Decisão sobre manter `VITE_ROBOTS=noindex,nofollow` até a aprovação
   explícita da produtora.

## Git

Este projeto foi copiado para dentro do repositório do "Trevo Digital
Conversões", em `paginas-de-vendas/aguardando-aprovacao/100-aplicativos-uteis/`,
por já não estar aprovado para publicação pública. Ver o commit
correspondente no histórico do repositório principal.
