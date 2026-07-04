# Relatório de auditoria — conversão `.dc.html` → Vite/React/TS/Tailwind (v1)

## Contexto

Havia um protótipo exportado do Claude Design (`Landing +100 Apps.dc.html`
+ `support.js`), útil como referência de copy e direção visual, mas
dependente de um runtime proprietário, sem build, sem componentização e
sem stack adequada para publicação profissional/tráfego pago.

Este projeto (`100-aplicativos-uteis-landing`) é a reconstrução completa
da mesma landing page como um projeto front-end real, publicável,
usando Vite + React + TypeScript + Tailwind CSS v4. **Nenhum arquivo do
protótipo (`.dc.html`, `support.js`) foi incluído neste projeto.**

## O que foi feito

1. **Scaffold** com `npm create vite@latest -- --template react-ts`.
2. **Tailwind CSS v4** instalado via `@tailwindcss/vite` (sem PostCSS
   manual — abordagem recomendada pela própria Tailwind v4). Tokens de
   marca (cores, fontes, animação) definidos em `@theme` dentro de
   `src/index.css`, replicando exatamente a paleta já validada no
   protótipo anterior (`docs/design-system.md`).
3. **Fontes self-hosted** via `@fontsource/sora` e
   `@fontsource/instrument-sans` — elimina a dependência de
   `fonts.googleapis.com` em runtime (melhora performance/privacidade e
   atende à recomendação de "evitar fontes externas se possível").
4. **Componentização completa** — 17 componentes em `src/components/`
   (um por seção + utilitários `Container`, `CtaButton`,
   `SectionHeading`, `LegalModal`, `SkipLink`), consumindo dados
   tipados de `src/data/product.ts`, `src/data/faq.ts` e
   `src/data/legal.ts`.
5. **Hotlink centralizado** — `src/lib/links.ts` exporta
   `HOTMART_HOTLINK`, lido de `import.meta.env.VITE_HOTMART_HOTLINK`,
   com fallback visível para o placeholder documentado. Todos os CTAs
   (`CtaButton.tsx`) consomem essa única fonte.
6. **`.env.example`** criado com `VITE_HOTMART_HOTLINK` e
   `VITE_SITE_URL` como placeholders — nenhum `.env` real foi criado ou
   commitado.
7. **Ícones abstratos** via `lucide-react` (traço simples,
   monocromático) substituindo qualquer sugestão de logo real de app.
8. **SEO técnico** em `index.html`: `<html lang="pt-BR">`, title, meta
   description, `robots`, `canonical` (placeholder), Open Graph
   completo, Twitter Card, favicon SVG próprio e imagem OG SVG própria
   (`public/favicon.svg`, `public/og-image.svg`) — nenhuma dependência
   de imagem externa.
9. **Acessibilidade**: link "Pular para o conteúdo" (`SkipLink.tsx`),
   foco visível global, FAQ com `aria-expanded` / `aria-controls` /
   `aria-labelledby` / `role="region"` e pergunta em `<h3>`, modal
   institucional com focus-trap e `role="dialog"`, `prefers-reduced-motion`
   respeitado globalmente, HTML semântico (`header`/`nav`/`main`/`section`/`footer`).
10. **Links institucionais sem `#` morto** — como a página deve
    permanecer única (sem rotas), Política de Privacidade, Termos de Uso
    e Contato são exibidos em modal acessível (`LegalModal.tsx`) com
    texto institucional genérico (sem dados pessoais da produtora,
    sem inventar canais de atendimento).
11. **Documentação completa** em `docs/`: `sitemap.md`, `wireframe.md`,
    `copy.md` (cópia de leitura de todo o texto), `design-system.md`,
    `compliance.md` (checklist de regras obrigatórias e onde cada uma é
    garantida no código) e este relatório.

## Comandos executados

```bash
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss @tailwindcss/vite
npm install lucide-react @fontsource/sora @fontsource/instrument-sans
npx tsc -b            # ✅ sem erros
npm run build          # ✅ build limpo (tsc -b && vite build)
npm run lint            # ✅ oxlint — 0 warnings, 0 erros
npm run preview         # ✅ servido localmente para conferência, depois encerrado
```

### Resultado do build

```
dist/index.html                2.00 kB │ gzip:  0.73 kB
dist/assets/index-*.css       44.16 kB │ gzip:  7.70 kB
dist/assets/index-*.js       234.73 kB │ gzip: 73.12 kB
+ fontes self-hosted (woff2/woff, Sora + Instrument Sans)
```

Build sem erros de TypeScript, sem warnings de lint, sem dependências
não utilizadas.

## Verificações de compliance

- ✅ Nenhum `<form>`/`<input>` de captura em todo o projeto.
- ✅ Nenhuma imagem (print, foto, logo real) — apenas SVG/CSS próprios.
- ✅ Nenhum dado sensível ou segredo no código (`grep` de termos como
  `api_key`, `secret`, `token`, `password` não retornou nada além dos
  nomes de variável `VITE_*`, que são placeholders documentados).
- ✅ Nenhum `.env` commitado (apenas `.env.example`, com placeholders).
- ✅ Nenhum link `#` sem destino (âncoras reais ou modal).
- ✅ CTAs centralizados em `lib/links.ts` — texto fixo "Ver produto na
  Hotmart" em todos os pontos de conversão.
- ✅ Nenhuma promessa de resultado garantido — ver `docs/compliance.md`.

## Pendências (mesmas do protótipo anterior, ainda aplicáveis)

1. Substituir `VITE_HOTMART_HOTLINK` pelo link real de afiliado.
2. Substituir `VITE_SITE_URL` e os placeholders de URL em `index.html`
   (`canonical`, `og:url`, `og:image`, `twitter:image`).
3. Preencher `HOTMART_VERIFICATION_DATE`
   (`src/data/product.ts`) com a data real da verificação de preço e
   garantia na Hotmart — **não preenchido automaticamente**, conforme
   instrução explícita de não inventar datas.
4. Revisar preço (R$ 69,90) e garantia (7 dias) diretamente na página
   oficial antes de publicar, pois podem ter mudado.
5. Opcional: gerar uma versão rasterizada (PNG) da `og-image.svg` caso
   alguma rede social específica não renderize SVG em preview de link
   (a maioria hoje aceita SVG, mas isso varia).

## Próximos passos recomendados

- Rodar uma auditoria automatizada (Lighthouse/axe) após publicar em
  ambiente real, para validar contraste e performance com dados de rede
  reais.
- Configurar as variáveis de ambiente na hospedagem escolhida antes do
  primeiro deploy.
- Depois de publicar, testar o link final em um "link preview" de
  WhatsApp/Instagram/Twitter para confirmar que a `og-image.svg`
  renderiza como esperado na plataforma de destino do tráfego pago.

## Git

Este relatório foi gerado antes do commit `converte-landing-100-apps-para-vite-react`.
Repositório inicializado localmente nesta conversão; nenhum remote foi
configurado neste ambiente, então nenhum `push` foi realizado — isso deve
ser feito pelo usuário para o repositório de destino desejado.
