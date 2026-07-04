# Relatório final — saneamento técnico e preparação para publicação (v1)

## Contexto

Rodada final de saneamento sobre o projeto já convertido para Vite +
React + TypeScript + Tailwind (ver `docs/relatorio_auditoria_conversao_v1.md`).
**Nenhuma reescrita de layout, copy ou stack foi feita** — apenas
correção de pendências de configuração de produção, compliance e
empacotamento, conforme escopo solicitado.

## Arquivos alterados

| Arquivo | Mudança |
|---|---|
| `.env.example` | Adicionadas `VITE_HOTMART_VERIFICATION_DATE` e `VITE_ROBOTS`, com comentários explicando o comportamento de cada uma |
| `index.html` | `og:url`/`canonical`/`og:image`/`twitter:image` passaram a usar interpolação nativa do Vite (`%VITE_SITE_URL%`); `robots` passou a usar `%VITE_ROBOTS%`, resolvido por plugin próprio com fallback seguro |
| `vite.config.ts` | Novo plugin `robotsMetaPlugin` — resolve `<meta name="robots">` em build time com fallback `noindex,nofollow` (nunca fica um placeholder não resolvido nessa tag, que seria perigoso para SEO) |
| `src/lib/links.ts` | Reescrito: `readEnv()` genérico, `hotlinkBlockedInProduction`, `HOTMART_VERIFICATION_DATE` / `isVerificationDatePlaceholder`, `isSiteUrlPlaceholder` |
| `src/vite-env.d.ts` | Tipos para `VITE_HOTMART_VERIFICATION_DATE` e `VITE_ROBOTS` |
| `src/components/CtaButton.tsx` | `rel="noopener sponsored"` → `rel="noopener noreferrer sponsored"`; novo estado desabilitado/acessível quando o build é de produção e o hotlink ainda é placeholder |
| `src/data/product.ts` | Removido o placeholder estático de data de verificação (`HOTMART_VERIFICATION_DATE`/`HOTMART_INFO.subtitle`); reescrito o comentário de compliance no topo do arquivo para não conter literalmente o termo proibido "produtividade garantida" (era um falso positivo do próprio comentário interno, não da copy da página) |
| `src/components/HotmartInfoSection.tsx` | Subtítulo agora calculado a partir de `VITE_HOTMART_VERIFICATION_DATE`, com fallback genérico sem data |
| `docs/compliance.md` | Atualizado `rel`, adicionadas seções "Robots / indexação" e "Hotlink em runtime" |
| `docs/copy.md` | Nota de verificação atualizada para refletir o comportamento dinâmico (antes descrevia um placeholder estático que não existe mais) |
| `README.md` | Reescrito com todas as seções pedidas: dev, `.env`, hotlink, URL final, data de verificação, staging vs. produção, robots, build, `check:prod`, publicação, `package`, checklist |
| `.gitignore` | Passa a ignorar o ZIP de release gerado (`*.zip`) além de `.env*` |
| `scripts/validate-production.mjs` | **Novo** — validador de produção (ver abaixo) |
| `scripts/package-release.mjs` | **Novo** — empacotador do ZIP final sem `.git`/`node_modules`/`.env`/`dist` |
| `package.json` | Novos scripts `check:prod`, `build:staging`, `build:prod`, `package`; `build` passou a rodar `check:prod` antes |
| `docs/relatorio_final_saneamento_v1.md` | Este relatório |

Nenhum arquivo de layout de componente (estrutura JSX/Tailwind) foi
alterado além do necessário para os itens acima. Nenhuma copy visível foi
reescrita — apenas o texto dinâmico da data de verificação, que antes era
um placeholder sempre visível e agora nunca aparece sem valor real.

## Problemas corrigidos

1. **Placeholders estáticos em `index.html`** — `[INSERIR_URL_FINAL_DA_PAGINA_AQUI]`
   ficava hardcoded em `canonical`/`og:url`/`og:image`/`twitter:image`.
   Agora usa `%VITE_SITE_URL%`, resolvido pelo próprio Vite em build time
   (testado manualmente com e sem a variável definida — ver seção de
   testes).
2. **Robots fixo em `index, follow`** — a página seria indexada mesmo em
   estado de rascunho. Agora o padrão é `noindex,nofollow`, só muda com
   `VITE_ROBOTS=index,follow` explícito, e o validador bloqueia essa
   combinação enquanto hotlink/URL ainda forem placeholders.
3. **Data de verificação sempre visível como placeholder** — a página
   antes sempre mostrava `[INSERIR_DATA_DA_VERIFICACAO]` literalmente
   (não havia lógica condicional). Agora, sem a variável configurada, um
   texto genérico sem data é exibido; nenhuma data é inventada.
4. **`rel` incompleto nos links externos** — `noopener sponsored` não
   incluía `noreferrer`. Corrigido em `CtaButton.tsx` (fonte única de
   todos os CTAs).
5. **Hotlink podia, em teoria, "vazar" como link quebrado** — antes, um
   build de produção sem `VITE_HOTMART_HOTLINK` configurado ainda geraria
   um `<a href="[INSERIR_HOTLINK_HOTMART_AQUI]">` clicável. Agora, em
   qualquer `vite build` (não só `dev`), esse cenário faz o CTA renderizar
   desabilitado — e `check:prod` impede que esse build chegue a produção
   de qualquer forma.
6. **Falso positivo do próprio validador** — a primeira versão do
   scanner de termos proibidos encontrava a frase "produtividade
   garantida" dentro de um comentário interno do próprio código-fonte
   (o comentário que *proíbe* usar essa frase). Corrigido reescrevendo o
   comentário; documentado aqui para transparência.
7. **Falso positivo do scanner de `dist/`** — a primeira versão da
   varredura de placeholders no build final também buscava dentro dos
   bundles JS, onde a string do placeholder aparece legitimamente como
   parte da lógica de fallback em runtime (`src/lib/links.ts`). Ajustado
   para varrer apenas `dist/index.html` (onde placeholders realmente
   vazando importariam para SEO/crawlers).

## Validador de produção (`scripts/validate-production.mjs`)

Sem dependências externas. Verifica:
- Nenhum `.env`/`.env.local`/etc. rastreado pelo Git (`git ls-files`).
- `VITE_HOTMART_HOTLINK` e `VITE_SITE_URL` configurados e não-placeholder
  (**bloqueia** o build se ausentes).
- `VITE_HOTMART_VERIFICATION_DATE` configurado (**avisa**, não bloqueia —
  há fallback seguro documentado).
- `VITE_ROBOTS`: avisa se ausente (fallback seguro já cobre); **bloqueia**
  se for `index,follow` enquanto hotlink/URL ainda são placeholders.
- Ausência de `<form>` e `<input type="email">` em `src/` e `index.html`.
- Ausência de uma lista de termos de promessa proibidos (produtividade/
  vendas/lucro/renda/sucesso/resultado "garantido", "100% seguro",
  "ferramentas validadas", "apps gratuitos e premium" etc.), comparando
  com e sem acentuação.
- Ausência de links institucionais mortos (`href="#"` literal).
- Se `dist/index.html` já existir: ausência de placeholders estáticos
  (`[INSERIR_...]`, `%VITE_...%`) não resolvidos no HTML final.

## Comandos executados e resultados

```bash
npm run lint            # ✅ oxlint — 0 warnings, 0 erros (30 arquivos)
npx tsc -b               # ✅ sem erros
npm run build:staging    # ✅ build gerado normalmente (sem gate, CTA fica
                          #    desabilitado por não haver hotlink real)
npm run check:prod       # ❌ falha (esperado) — sem .env real:
                          #    VITE_HOTMART_HOTLINK não configurado
                          #    VITE_SITE_URL não configurado
                          #    placeholder %VITE_SITE_URL% no dist/index.html
```

Testes adicionais feitos manualmente durante o saneamento (não fazem
parte do fluxo padrão, usados só para validar a implementação):
- Build com `VITE_SITE_URL`/`VITE_ROBOTS` fictícios via variável de
  ambiente do shell → `canonical`/`og:url`/`robots` resolvidos
  corretamente no `dist/index.html` gerado.
- Build com `VITE_HOTMART_HOTLINK` fictício + `check:prod` rodado logo em
  seguida, no mesmo processo → passou sem erros bloqueantes.
- Build **sem** `VITE_SITE_URL` → `%VITE_SITE_URL%` permanece literal no
  HTML e `check:prod` bloqueia corretamente, apontando o arquivo exato.
- `npm run package` → ZIP gerado (58 arquivos, ~75 KB) sem `.git`,
  `node_modules`, `.env` ou `dist`; script inclui checagem final que
  falha o próprio empacotamento se algo proibido sobrar no pacote.

Nenhum valor fictício usado nos testes foi salvo em `.env` nem commitado.

## Confirmações pedidas explicitamente

- ✅ **`.git` não entra no ZIP final** — `scripts/package-release.mjs`
  exclui o diretório `.git` na cópia filtrada (nunca é sequer copiado) e
  faz uma checagem de segurança final antes de gerar o ZIP.
- ✅ **`.env` não foi criado/versionado** — nenhum `.env` existe no
  projeto neste momento; todos os testes com valores fictícios foram
  feitos via variáveis de ambiente de shell, nunca escritos em disco.
- ✅ **Sem formulário/newsletter** — confirmado por inspeção manual e
  pelo próprio `check:prod` (checagem automatizada de `<form>`/
  `<input type="email">`).
- ✅ **Sem promessas indevidas** — confirmado por inspeção manual e pela
  lista de termos proibidos do validador; nenhuma copy foi alterada
  nesta rodada além do texto dinâmico de data de verificação.

## Pendências restantes (dependem de informação externa)

1. Preencher `VITE_HOTMART_HOTLINK` com o link real de afiliado.
2. Preencher `VITE_SITE_URL` com a URL final publicada.
3. Preencher `VITE_HOTMART_VERIFICATION_DATE` com a data real da
   verificação de preço/garantia na Hotmart.
4. Só depois de 1–3 e de uma revisão final de conteúdo, definir
   `VITE_ROBOTS=index,follow`.
5. Revisar preço (R$ 69,90) e garantia (7 dias) diretamente na página
   oficial antes de publicar — podem ter mudado desde a última análise.

## Próximos passos recomendados

- Configurar as 4 variáveis de ambiente na hospedagem escolhida.
- Rodar `npm run build` (já gated) diretamente no pipeline de deploy —
  ele falha ruidosamente se qualquer pendência acima não foi resolvida,
  em vez de publicar uma página incompleta silenciosamente.
- Depois do primeiro deploy real, rodar uma auditoria Lighthouse/axe.
- Gerar o ZIP de entrega com `npm run package` sempre que for necessário
  compartilhar o projeto fora do controle de versão.

## Git

Commit desta rodada: `saneia-landing-100-apps-para-publicacao`.
Nenhum remote está configurado neste ambiente — o `push` fica a cargo do
usuário, para o repositório de destino desejado.
