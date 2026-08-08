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
   (produto, Hotmart, plataforma de anúncios, contrato ou lei). Nunca
   foi (e não é) um portão de aprovação obrigatório por padrão.
7. **Nunca commite segredos.** Este repositório é público — sem
   `.env` real, tokens, senhas, chaves de API ou credenciais.
8. Este repositório é **estático (HTML + CSS, JS mínimo só quando
   justificado)**. Não introduza um framework/build (Next.js, Vite,
   React etc.) no repositório inteiro só para reaproveitar um
   protótipo de outro lugar.
9. **Páginas nascem como produção.** Toda pre-sell/landing vai direto
   para `/produtos/<slug>/`, com `index,follow` e canonical final
   desde o primeiro commit. **`/aprovacao/` foi removido em 2026-08-07
   e não existe mais neste repositório — nunca recrie essa pasta ou
   esse padrão.** Revisão técnica acontece em
   branch → PR → ambiente local → QA → revisão humana → merge, nunca
   numa área pública separada. Nunca deixe rascunho, placeholder, nota
   de QA, TODO/FIXME, referência a `docs/` internos ou estado de
   aprovação visível no HTML público (nem em comentários HTML). O
   estado de desenvolvimento fica em git/branch/PR, não na página.
10. **`/produtos/` é o catálogo público**, com seu próprio
    `produtos/index.html` (nunca listagem de diretório). Todo produto
    de produção deve aparecer lá e na home, com card factual e link
    interno para a página do produto — nunca o hotlink diretamente no
    card. Presença no catálogo **não** significa campanha paga ativa;
    não confunda as duas coisas em código ou documentação. O thumbnail
    de cada card deve ser legível em tamanho pequeno (pouco texto,
    bom contraste) — banners de OG/social geralmente têm texto demais para
    funcionar como thumbnail; use `assets/produtos/` para imagens
    criadas só para essa finalidade.
11. **QA de responsividade inclui 320px** como piso mínimo, além de
    375/390/425/768/1440. Textos sem espaço (e-mails, URLs) usam
    `overflow-wrap: anywhere` (regra global em `styles.css`) para não
    causar overflow horizontal.
12. **Integrações com redes sociais (Instagram/Meta e futuras) são
    ferramentas locais/operacionais** (`tools/<rede>/`), nunca código
    servido pelo site público. Nenhum token, secret ou credencial de
    API social entra em HTML/CSS/JS público, commit, log ou saída de
    comando — configuração sempre via `.env` local (nunca commitado).
    Publicação real exige confirmação dupla e explícita (flag de CLI +
    variável de ambiente); nenhum agente publica, apaga, comenta ou
    interage automaticamente em rede social sem essa confirmação
    humana. Use sempre a API oficial da plataforma. Código de
    integração deve permanecer extraível (core sem dependência do
    HTML/regras de campanha do Trevo) — ver
    `tools/instagram/README.md` como referência.
