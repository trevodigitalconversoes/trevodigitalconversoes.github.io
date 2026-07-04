# Relatório — ajustes editoriais/visuais para aprovação da produtora (v1)

## Contexto

Rodada de ajustes editoriais, visuais e estruturais sobre o projeto já
saneado para produção (ver `docs/relatorio_final_saneamento_v1.md`).
**Nenhuma reescrita do projeto, da stack ou do layout geral foi feita** —
apenas os ajustes de tom, estrutura de avisos e preparação para GitHub
Pages descritos abaixo. Layout, paleta e componentização existentes
foram preservados; os componentes afetados foram editados, não
recriados do zero.

## Arquivos alterados

| Arquivo | Mudança |
|---|---|
| `src/data/product.ts` | `CREATOR` reescrito e expandido (texto principal, complemento, `observed[]`, `checkBeforeBuying[]`, sem `notice` defensivo); `RESPONSIBLE_RECOMMENDATION` reescrito com 2 parágrafos; `AFFILIATE_DISCLOSURE` renomeado/expandido para `IMPORTANT_NOTICES` (intro + 5 cards); `FINAL_CTA` com novo título/texto e campo `microcopy` |
| `src/components/CreatorSection.tsx` | Reescrito: avatar abstrato "CS", texto + complemento editorial, dois blocos ("O que foi observado" / "O que conferir antes de comprar"); nenhum aviso/disclaimer nesta seção |
| `src/components/AffiliateDisclosure.tsx` → `src/components/ImportantNoticesSection.tsx` | Componente renomeado e reescrito: título "Avisos importantes", 2 parágrafos introdutórios + grid de 5 cards |
| `src/components/FinalCTA.tsx` | Adicionada a linha de microcopy ("Compra e acesso processados pela Hotmart.") entre o botão e o complemento |
| `src/components/Footer.tsx` | Link do rodapé atualizado de "Aviso de Afiliado" (`#aviso`) para "Avisos importantes" (`#avisos-importantes`) |
| `src/App.tsx` | Import/uso do componente renomeado; ordem das seções mantida (Avisos importantes continua entre FAQ e CTA final) |
| `vite.config.ts` | Novo `base` configurável via `VITE_BASE_PATH` (fallback `/`), para permitir publicação em subpasta no GitHub Pages |
| `src/vite-env.d.ts` | Tipo `VITE_BASE_PATH?: string` adicionado |
| `.env.example` | Adicionada `VITE_BASE_PATH` com comentário explicando root vs. subpasta |
| `README.md` | Nova seção "Publicação econômica no GitHub Pages junto ao Trevo Digital Conversões"; seção de `.env` atualizada com `VITE_BASE_PATH`; nova subseção "Como configurar o base path" |
| `docs/sitemap.md` | Âncora/componente `#aviso`/`AffiliateDisclosure.tsx` → `#avisos-importantes`/`ImportantNoticesSection.tsx` |
| `docs/wireframe.md` | Itens 9–13 reescritos para refletir o novo conteúdo da criadora e a nova seção de avisos |
| `docs/copy.md` | Seções "Sobre a criadora", "Minha leitura como afiliado" e "Aviso de afiliado" → "Avisos importantes" reescritas por completo |
| `docs/compliance.md` | Referências a `AffiliateDisclosure.tsx`/`#aviso` atualizadas; nova linha "Avisos concentrados no final"; nova seção "Tom com a produtora" |
| `docs/relatorio_ajustes_produtora_v1.md` | Este relatório |

## Textos movidos para o final

Antes deste ajuste, a seção "Sobre a criadora" continha o seguinte texto
no meio da página:

> "Esta análise considera este produto específico. Outros produtos da
> mesma criadora não são usados como garantia de qualidade deste
> produto."

Esse texto foi **removido da seção "Sobre a criadora"** (podia soar
defensivo/negativo lida fora de contexto) e sua ideia foi reformulada de
forma diplomática, movida para o início da seção final "Avisos
importantes":

> "Esta página não avalia outros produtos da criadora. As informações
> aqui se referem apenas ao produto '+100 Aplicativos Úteis para
> Produtividade Empreendedora'."

Junto dela, também no início da seção final, foi adicionado o
enquadramento de rascunho/aprovação:

> "Esta página foi criada como rascunho de pré-venda/review por
> afiliado, com base nas informações públicas observadas na página do
> produto na Hotmart. O conteúdo pode ser ajustado conforme orientação
> da produtora antes de qualquer campanha."

Todos os avisos legais, cautelas e notas de afiliado da página agora
ficam **exclusivamente** na seção `ImportantNoticesSection.tsx`
(`#avisos-importantes`), posicionada depois do FAQ e antes do CTA final.
Nenhum aviso permanece espalhado no meio da página.

## Nova copy — "Sobre a criadora"

Ver `docs/copy.md` para o texto completo. Resumo da estrutura:
- **Texto principal:** mantém exatamente o texto-base fornecido (nome
  público na Hotmart, 7 anos de histórico, posicionamento profissional).
- **Complemento editorial:** explica o recorte da análise (foco no
  produto, não na trajetória completa da criadora).
- **Bloco "O que foi observado":** 4 itens factuais, sem opinião.
- **Bloco "O que conferir antes de comprar":** 4 itens práticos,
  orientados ao comprador — descrição, suporte, avaliações, garantia.
- **Visual:** card branco elegante com avatar abstrato "CS" em gradiente
  da marca (sem foto, sem dados pessoais, sem redes sociais).

Nenhum fato foi inventado; todo o conteúdo vem do texto-base fornecido
ou de reformulações neutras dele.

## Nova copy — "Minha leitura como afiliado"

Dois parágrafos, exatamente conforme o texto fornecido:
1. Posiciona o produto como curadoria de ferramentas para quem quer
   economizar tempo de pesquisa, listando os perfis a que pode servir.
2. Reforça que a utilidade depende do perfil de cada pessoa e recomenda
   conferir a página oficial antes de decidir.

Nenhum dos termos vetados ("garante produtividade", "vai melhorar
vendas", "gera lucro", "ferramentas validadas", "apps gratuitos",
"resultado garantido") aparece no texto — confirmado manualmente e via
`scripts/validate-production.mjs` (lista de termos proibidos).

## Nova seção — "Avisos importantes"

Posição: depois do FAQ, antes do CTA final (`ImportantNoticesSection.tsx`,
`#avisos-importantes`).

Estrutura:
- Título "Avisos importantes".
- 2 parágrafos introdutórios centralizados (rascunho/aprovação + "não
  avalia outros produtos da criadora").
- Grid de 5 cards, cada um com ícone abstrato (Lucide) + título curto +
  texto: "Página de afiliado", "Página não oficial", "Rascunho para
  aprovação", "Informações sujeitas a alteração", "Sem promessa de
  resultado" — todos com o texto exato fornecido no briefing.

## Ajustes para GitHub Pages / Trevo Digital Conversões

- `vite.config.ts` agora lê `VITE_BASE_PATH` (via `loadEnv`) e aplica
  como `base` do build. Testado manualmente com
  `VITE_BASE_PATH=/100-aplicativos-uteis/` — assets (`favicon.svg`,
  bundle JS) passaram a ser referenciados corretamente com o prefixo da
  subpasta no `dist/index.html` gerado.
- `.env.example` documenta os dois cenários (raiz vs. subpasta), sem
  fixar nenhuma URL ou caminho real.
- README ganhou a seção "Publicação econômica no GitHub Pages junto ao
  Trevo Digital Conversões", com passo a passo completo, incluindo
  checklist específico para o envio à produtora (manter `noindex`,
  revisar tom, confirmar que os avisos estão só no final).
- Nenhuma dependência paga, backend, banco de dados ou serviço externo
  obrigatório foi introduzido — o projeto continua 100% estático
  (Vite build → arquivos HTML/CSS/JS/fontes servidos diretamente).

## Responsividade

Nenhuma mudança estrutural de breakpoints foi necessária: os novos
blocos (`CreatorSection.tsx` e `ImportantNoticesSection.tsx`) reutilizam
os mesmos padrões já usados no restante do projeto
(`grid-cols-[repeat(auto-fit,minmax(...px,1fr))]`, containers com
`max-w-*`, escala de espaçamento padrão do Tailwind — verificado que
nenhum valor de espaçamento fora da escala foi introduzido). Isso
garante que os cards de "O que foi observado" / "O que conferir antes de
comprar" e os 5 cards de "Avisos importantes" empilham automaticamente
em mobile, sem blocos excessivamente altos, seguindo o mesmo
comportamento já validado nas seções de dor/benefícios/checklist.

## Compliance — verificação pós-ajuste

Confirmado por inspeção manual e por `scripts/validate-production.mjs`
(0 termos proibidos encontrados no build gerado):
- Sem promessa de produtividade, vendas, lucro, renda, sucesso ou
  resultado garantido.
- Sem urgência falsa.
- Sem depoimentos ou avaliações inventadas.
- Sem comparação ou crítica a outros produtos da criadora — pelo
  contrário, a página agora afirma explicitamente que não avalia outros
  produtos.
- Sem dados pessoais, fotos, prints da Hotmart ou logos reais de
  aplicativos (nenhuma dessas categorias de asset existe no projeto).

## Comandos executados e resultados

```bash
npm run lint            # ✅ oxlint — 0 warnings, 0 erros (30 arquivos)
npx tsc -b               # ✅ sem erros
npm run build            # ❌ falha por design — VITE_HOTMART_HOTLINK e
                          #    VITE_SITE_URL ainda são placeholders neste
                          #    ambiente (não é um erro de código; é o gate
                          #    de produção funcionando como esperado)
npm run build:staging    # ✅ build gerado normalmente; confirmado por
                          #    grep que os novos textos ("Avisos
                          #    importantes", "Rascunho para aprovação",
                          #    "O que foi observado", "O que conferir
                          #    antes de comprar") estão no bundle final
npm run check:prod       # ❌ falha pela mesma razão do build — sem
                          #    valores reais em .env, o comportamento é o
                          #    esperado e documentado
```

Nenhum comando foi omitido ou teve resultado forjado: `npm run build`
genuinamente falha neste ambiente porque não há um `.env` real
configurado — isso é o gate de produção (`check:prod`) funcionando
corretamente, não uma regressão introduzida por este ajuste.

## Pendências antes da publicação

1. Preencher `VITE_HOTMART_HOTLINK`, `VITE_SITE_URL`,
   `VITE_HOTMART_VERIFICATION_DATE` com valores reais.
2. Confirmar com quem administra o "Trevo Digital Conversões" o caminho
   final (`VITE_BASE_PATH`) e a URL definitiva antes de configurá-los.
3. Rodar `npm run build` (gated) com esses valores reais e depois
   `npm run preview` para conferência final.

## Pendências antes de anúncios

1. Obter aprovação explícita da produtora sobre o conteúdo (a página
   está pronta para esse envio: avisos concentrados no final, tom
   editorial e respeitoso na seção da criadora, sem críticas a outros
   produtos).
2. Só depois da aprovação, trocar `VITE_ROBOTS` para `index,follow` e
   gerar um novo build/deploy.
3. Revisar novamente preço (R$ 69,90) e garantia (7 dias) na página
   oficial da Hotmart antes do anúncio, pois podem ter mudado.

## Git

Commit desta rodada: `ajusta-landing-100-apps-para-aprovacao-produtora`.
Nenhum remote está configurado neste ambiente — o `push` fica a cargo do
usuário.
