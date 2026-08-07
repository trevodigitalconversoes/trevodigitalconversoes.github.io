# Instruções para agentes de código neste repositório

Fonte completa: [`docs/ADR_PRESELL_OWNERSHIP.md`](docs/ADR_PRESELL_OWNERSHIP.md).
Este arquivo é só um resumo — em caso de dúvida ou conflito, o ADR
prevalece.

1. **Este repositório (`trevodigitalconversoes/trevodigitalconversoes.github.io`)
   é o proprietário das pre-sells/landing pages públicas.** Nenhuma
   página pública de afiliado deve ser implementada em outro lugar.
2. **`afiliados-mega-lab` (AML) não hospeda páginas públicas.** É um
   repositório operacional/experimental (pesquisa, tracking,
   evidências). Implementações de pre-sell feitas lá são protótipos a
   migrar para cá, nunca o destino final.
3. **Antes de implementar qualquer pre-sell/landing, confirme
   `git remote -v` e `git rev-parse --show-toplevel`.** Se o remote
   não for este repositório, pare e migre antes de escrever código
   público.
4. **GitHub Pages é o destino de hospedagem atual** (branch `main`,
   pasta raiz, sem build). Não migrar para Vercel ou outra hospedagem
   sem uma ADR nova.
5. **Não reescreva copy comercial aprovada.** Copy vem do Figma
   aprovado e/ou de fonte comercial documentada — preserve
   literalmente, não "melhore" por iniciativa própria.
6. **Não exija contato com a produtora sem uma regra explícita**
   (produto, Hotmart, plataforma de anúncios, contrato ou lei). A
   pasta `/aprovacao/` é uma área opcional de revisão controlada, não
   um portão de aprovação obrigatório por padrão.
7. **Nunca commite segredos.** Este repositório é público — sem
   `.env` real, tokens, senhas, chaves de API ou credenciais.
8. Este repositório é **estático (HTML + CSS, JS mínimo só quando
   justificado)**. Não introduza um framework/build (Next.js, Vite,
   React etc.) no repositório inteiro só para reaproveitar um
   protótipo de outro lugar.
