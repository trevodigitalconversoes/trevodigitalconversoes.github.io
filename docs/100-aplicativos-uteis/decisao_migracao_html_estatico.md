# Decisão — HTML+CSS estático, zero JavaScript

## Motivo

Uma versão anterior desta página dependia de um framework JavaScript
para renderizar o conteúdo (nada aparecia sem executar o script). Isso
viola um requisito do projeto: a página publicada não pode depender de
JavaScript para exibir o conteúdo principal — afeta crawlers que não
executam JS, navegadores com JS desabilitado, e robustez geral.

## O que mudou

A página foi reconstruída como um único `index.html` + `styles.css`,
sem build e **sem nenhuma tag `<script>`**:

- Todo o conteúdo (texto, disclaimers, FAQ, avisos) está no HTML puro.
- FAQ e conteúdo institucional (Política de Privacidade/Termos/Contato)
  usam `<details>`/`<summary>` nativos do HTML, sem JS.
- CTA é sempre um `<a>` real e navegável. Já usa o hotlink de afiliado
  (link otimizado para Google Ads) — ver `docs/compliance.md` para o
  link completo e o hotlink base.
- Fontes self-hosted em `../fonts/` (`.woff2`), sem CDN.
- Ano do rodapé é texto fixo no HTML, não calculado.

Nenhum texto/disclaimer/pergunta de FAQ foi enfraquecido nessa troca —
o conteúdo textual foi preservado integralmente, só a forma de entrega
mudou.

## Pendências (não relacionadas à arquitetura)

A pendência de hotlink de afiliado real já foi resolvida — os dois CTAs
usam o link de afiliado otimizado para Google Ads. Em 2026-08-07, a
página foi promovida a `/produtos/100-aplicativos-uteis/` com
`robots: index,follow`, data de verificação preenchida (07/08/2026,
fatos revalidados na Hotmart) e sem exigência de aprovação de
produtora (ver `docs/ADR_PRESELL_OWNERSHIP.md`). Nenhuma pendência de
arquitetura permanece.
