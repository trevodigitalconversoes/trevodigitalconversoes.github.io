# Auditoria de pré-publicação — "+100 Aplicativos Úteis para Produtividade Empreendedora"

Página avaliada: `aprovacao/100-aplicativos-uteis/index.html`
URL final: `https://trevodigitalconversoes.github.io/aprovacao/100-aplicativos-uteis/`
Data da auditoria: 2026-07-04

## 1. Clareza da proposta
- O H1 ("Descubra uma curadoria com +100 aplicativos para organizar
  melhor sua rotina empreendedora") comunica o produto em uma leitura.
- O subtítulo explica o escopo (produtividade, organização, criação,
  marketing, gestão) sem prometer resultado.
- O eyebrow "Review independente de afiliado" já avisa a natureza da
  página antes mesmo do H1.
- CTA principal ("Ver produto na Hotmart") é único e repetido (hero +
  CTA final), sem CTAs concorrentes.
- **Avaliação: claro.**

## 2. Conversão
- A página cria interesse por curadoria/organização, sem prometer
  produtividade/renda/resultado — condizente com a proposta de review,
  não de hype.
- CTA primário no hero e no final da página; CTA secundário ("Entender a
  curadoria") só rola a própria página, sem fricção.
- Não há formulário, checkout, ou qualquer etapa extra antes do clique —
  fricção mínima.
- Preço e garantia aparecem de forma transparente antes do FAQ, o que
  ajuda a decisão em vez de escondê-la.
- **Avaliação: sem promessas exageradas, caminho ao CTA é direto.**

## 3. Confiança
- Barra superior fixa já declara "página independente de afiliado" antes
  de qualquer scroll.
- FAQ tem duas perguntas dedicadas só a esclarecer que não é a página
  oficial e que o pagamento não é feito ali.
- Seção "Sobre a criadora" é respeitosa, cita apenas dado público (nome
  no marketplace, tempo de plataforma), sem tom defensivo ou crítico a
  outros produtos dela.
- CTA usa o hotlink de afiliado (link otimizado para Google Ads),
  preservando o rastreamento de comissão de forma transparente para o
  visitante.
- **Avaliação: transparente, sem assustar o visitante.**

## 4. Compliance
- Nenhuma promessa de resultado, produtividade, renda, vendas ou lucro
  garantido em nenhum bloco de texto (verificado bloco a bloco contra
  `docs/compliance.md`).
- Nenhuma logo real de aplicativo, print da Hotmart, foto ou dado pessoal
  da produtora.
- Não parece página oficial (FAQ + avisos + barra superior reforçam isso
  três vezes, sem repetição cansativa).
- Não confunde o consumidor sobre onde a compra acontece (Hotmart, nunca
  nesta página).
- **Avaliação: em conformidade.**

## 5. SEO técnico de rascunho
- `<title>` e meta description específicos do produto.
- `canonical` aponta para a URL final de aprovação
  (`.../aprovacao/100-aplicativos-uteis/`), coerente com o local real de
  publicação.
- `<meta name="robots" content="noindex,nofollow">` fixo no HTML.
- H1 único; H2 abre cada seção; H3 usado para subtópicos dentro de seção
  (ex.: "O que você encontra", "Confira antes de comprar") — hierarquia
  sem saltos.
- Open Graph/Twitter Card preenchidos, sem exagero de copy (mesmo texto
  do `<title>`/description, sem clickbait).
- `favicon.svg` presente.
- Nenhum `sitemap.xml` no repositório — página em aprovação não é
  referenciada em nenhum sitemap público.
- **Avaliação: correto para fase de rascunho.**

## 6. Acessibilidade
- Link "Pular para o conteúdo" como primeiro elemento focável.
- `:focus-visible` global com contorno visível (contraste roxo sobre
  fundo claro).
- FAQ e conteúdo legal usam `<details>`/`<summary>` nativos — acessíveis
  por teclado (Enter/Espaço) e leitores de tela, sem necessidade de ARIA
  manual.
- Hierarquia de headings sem pular níveis.
- Links com texto descritivo (nenhum "clique aqui").
- Áreas clicáveis dos botões usam padding generoso (14px/28px).
- Nenhuma informação depende só de cor (avisos usam texto, não cor
  isolada).
- `lang="pt-BR"` no `<html>`.
- **Avaliação: boa cobertura para uma página estática sem componente de
  terceiros.** Recomenda-se rodar um scanner automatizado (axe/Lighthouse)
  após a publicação real, como checagem complementar.

## 7. Performance
- HTML único, sem framework, sem bundle JS.
- CSS único e pequeno (sem Tailwind compilado, sem CSS não utilizado).
- Fontes: apenas 7 arquivos `.woff2` (subset latin, sem duplicar
  latin-ext nem `.woff` legado) — mais leve que o build React anterior,
  que também incluía `.woff` e subset `-ext` para todos os pesos.
- Nenhum script, nenhuma dependência de CDN externa, nenhuma imagem
  pesada (apenas SVGs para favicon/OG).
- **Avaliação: leve, sem JS crítico, sem dependências pesadas.**

## 8. Compatibilidade
- `<details>`/`<summary>` e `<dialog>`-like accordion via `<details>` são
  suportados nativamente em Chrome, Edge, Firefox e Safari/WebKit atuais
  (desktop e mobile), sem necessidade de polyfill.
- Layout em CSS Grid/Flexbox com `clamp()` — suportado nos navegadores
  listados; testado visualmente em desktop (1280px) e mobile (375px) via
  preview local.
- Com JavaScript desabilitado: página **inteira** funciona, já que não
  existe nenhum `<script>` — confirmado por inspeção (`document.querySelectorAll('script').length === 0`
  no HTML servido).
- Com cookies bloqueados: página não usa nenhum cookie, `localStorage`
  ou `sessionStorage` — nenhum impacto.
- **Avaliação: compatível com o conjunto de navegadores e cenários
  exigidos.**

## 9. Publicação no GitHub Pages
- Caminhos de `styles.css`, `fonts/*.woff2`, `favicon.svg`, `og-image.svg`
  são relativos à própria pasta (`fonts/arquivo.woff2`, não
  `/fonts/arquivo.woff2`) — funcionam tanto em preview local quanto
  publicados em `/aprovacao/100-aplicativos-uteis/`, sem depender de
  configuração de base path.
- Nenhuma rota client-side (não há roteador) — não há risco de "refresh
  direto na URL" quebrar, típico de SPAs.
- `404.html` na raiz do repositório já existe, é simples e não lista
  páginas em aprovação.
- **Avaliação: pronto para publicação estática padrão do GitHub Pages
  (Deploy from a branch, `main`, `/root`).**

## 10. Risco de aprovação pela produtora
- Nenhum trecho fala mal do produto, da criadora ou de outros produtos
  dela.
- Nenhuma promessa exagerada que a produtora precisaria desmentir depois.
- O CTA já usa o hotlink de afiliado (link otimizado para Google Ads),
  então não há pendência técnica que precise ser explicada à produtora
  nesse ponto.
- Nada precisa ser removido antes do envio; os avisos/ressalvas já estão
  concentrados no final, não atrapalhando a leitura do produto.

## Conclusão

**Aprovado com ressalvas.**

A página corrige o problema crítico da versão anterior (dependência de
JavaScript para conteúdo principal), preserva integralmente o copy já
validado em compliance, já usa o hotlink de afiliado (link otimizado
para Google Ads, hotlink base confirmado:
`https://go.hotmart.com/Q106592213V`) e está tecnicamente pronta para
envio à produtora. As ressalvas abaixo **não bloqueiam o envio para
revisão da produtora**, mas bloqueiam a troca para `index,follow`/início
de campanha paga:

1. Teste manual do clique no CTA, confirmando redirecionamento correto
   para a página do produto na Hotmart.
2. Data de verificação de preço/garantia ainda não preenchida.
3. Aprovação explícita da produtora ainda não obtida.
4. Decisão futura sobre indexação: `robots` deve permanecer
   `noindex,nofollow` até os itens 1–3 serem resolvidos.
