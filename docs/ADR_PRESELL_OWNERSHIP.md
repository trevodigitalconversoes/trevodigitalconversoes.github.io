# ADR — Propriedade das pre-sells públicas e papel do AML

- **Status:** aceito (atualizado)
- **Data:** 2026-08-07
- **Contexto da criação:** correção de um erro arquitetural do
  [PR #51](https://github.com/correa0inaiara/afiliados-mega-lab/pull/51)
  do repositório `afiliados-mega-lab`, que implementou uma pre-sell
  pública dentro do repositório operacional/experimental em vez do
  repositório proprietário das páginas públicas.
- **Contexto da atualização (mesmo dia):** a primeira migração da
  pre-sell "Fotografia + Presets" foi colocada em `/aprovacao/`, com
  `noindex,nofollow` e mensagens de estado de revisão/QA visíveis no
  HTML público. Essa não é mais a regra: ver "Regra de publicação —
  páginas nascem como produção" abaixo.
- **Contexto da atualização (catálogo, mesmo dia):** a home ainda
  afirmava "nenhum produto está sendo anunciado publicamente" e
  mencionava um fluxo de "link de revisão" enviado por e-mail, e
  `/produtos/` não tinha `index.html` próprio (o servidor expunha
  listagem de diretório). Corrigido: ver "`/produtos/` é o catálogo
  público" abaixo.
- **Contexto da atualização (remoção de `/aprovacao/`, mesmo dia):** a
  pasta `/aprovacao/` foi **removida completamente** do repositório em
  2026-08-07. A única página que ainda vivia lá
  (`100-aplicativos-uteis/`) foi promovida a
  `/produtos/100-aplicativos-uteis/`, com metadata de produção e
  fatos comerciais revalidados. `/produtos/` passa a ser o **único**
  namespace público de pre-sells/produtos deste repositório. Ver
  "`/aprovacao/` foi removido" abaixo (substitui a seção anterior, que
  tratava a pasta como "exceção histórica ainda existente").

## Decisão

A separação de responsabilidades entre os dois repositórios é:

### `trevodigitalconversoes/trevodigitalconversoes.github.io` (este repo)

- Site público institucional.
- Páginas editoriais, reviews, landing pages e pre-sells de afiliado.
- Hospedagem via GitHub Pages.
- **É o único repositório que publica conteúdo público de afiliado.**

### `correa0inaiara/afiliados-mega-lab` (AML)

- Pesquisa, triagem e ranking de produtos.
- Decisões e experimentos operacionais.
- Evidências, tracking/atribuição, métricas, análise operacional.
- **Não hospeda páginas públicas.** Qualquer implementação de
  pre-sell/landing feita ali é experimental e deve ser migrada para o
  Trevo antes de qualquer publicação real, mesmo em ambiente de
  revisão/QA.

### Fluxo canônico

```
copy comercial aprovada
  → Figma aprovado
  → Claude Code / Codex
  → Trevo Digital Conversões (este repo)
  → GitHub Pages
  → Hotmart
```

O **Vercel não faz parte do caminho crítico atual**. Migrar a
hospedagem para Vercel (ou qualquer plataforma além do GitHub Pages)
exige uma nova ADR explícita — não é uma decisão que um agente de
código deve tomar sozinho ao implementar uma página.

## Regra de publicação — páginas nascem como produção

### Regra

Novas pre-sells são implementadas **diretamente como páginas
destinadas a produção**, em `/produtos/<slug>/`, com metadata real
(`index,follow`, canonical apontando para a URL final) desde o
primeiro commit que as adiciona ao repositório.

O estado de desenvolvimento de uma página pertence a **git, branches e
PRs** — não ao HTML servido ao visitante. Uma branch pode estar em
desenvolvimento e passar por revisão; a página em si, quando existe no
repositório, é um artefato de produção. QA continua obrigatório, mas
acontece no fluxo `branch → PR → ambiente local → testes → revisão`,
nunca como texto exposto dentro do conteúdo público.

### Proibição

Agentes de código não devem inserir, em nenhuma página pública deste
repositório:

- indicação de rascunho;
- placeholder;
- nota de QA interno;
- `TODO`/`FIXME`;
- referência a documentos internos (`docs/...`);
- indicação de estado de aprovação ("aguardando aprovação", "sem
  aprovação para tráfego pago");
- instruções voltadas a desenvolvedores/mantenedores.

Isso vale tanto para texto visível quanto para comentários HTML
(`<!-- ... -->`) — comentários em uma página pública ainda são
publicados e legíveis por qualquer visitante que veja o código-fonte.

### `/aprovacao/` foi removido

`/aprovacao/` **foi removido completamente deste repositório em
2026-08-07** — não existe mais como pasta, rota ou fluxo. Não há
"exceção histórica ativa": a única página que ainda vivia lá
(`100-aplicativos-uteis/`) foi promovida para
`/produtos/100-aplicativos-uteis/` na mesma etapa (registro completo em
`trevo-ops`, privado).

**`/produtos/` é o único namespace público de pre-sells/produtos**
deste repositório. Não existe mais um fluxo público de aprovação,
revisão, rascunho, staging, ou "link privado por obscuridade". Revisão
técnica acontece inteiramente em
`branch → PR → ambiente local → QA → revisão humana → merge`.

Agentes de código **nunca devem recriar `/aprovacao/`** (nem essa
pasta específica, nem um padrão equivalente de "área de revisão
pública separada da produção"). Se um caso realmente excepcional exigir
algo assim no futuro, isso exige uma ADR nova e explícita — não uma
decisão silenciosa durante a implementação.

Documentos históricos operacionais (em `trevo-ops`, privado) podem
mencionar `/aprovacao/` ao narrar o que aconteceu naquela etapa — isso é
registro de passado, não instrução de uso atual.

### Contato com produtor

Mantém-se a regra já decidida na versão original deste ADR: **não
solicitar aprovação nem contato com a produtora por padrão.** Contato
só ocorre quando regra oficial do produto, da Hotmart, da plataforma
de anúncios, contrato ou legislação aplicável exigir — ver regra 5 em
"Regras derivadas" abaixo. Essa regra nunca dependeu da existência de
`/aprovacao/` — publicar direto em `/produtos/` não é, por si só, uma
exigência de aprovação nova.

## `/produtos/` é o catálogo público

Uma página em `/produtos/<slug>/` destinada a produção deve ser
**descoberível pelo site**, não apenas acessível por URL direta:

- `/produtos/` é o **catálogo público** de produtos anunciados —
  tem seu próprio `produtos/index.html` (identidade visual do site,
  header/nav/footer consistentes), nunca listagem de diretório do
  servidor.
- A home (seção "Produtos anunciados") apresenta um card institucional
  de cada produto de produção existente e um link para o catálogo
  completo.
- Um card de produto (na home ou no catálogo) contém apenas dados
  factuais/aprovados (imagem oficial, título oficial, descrição
  reaproveitada ou reduzida de forma neutra a partir da copy já
  aprovada) e um link **interno** para a página do produto — nunca o
  hotlink de afiliado diretamente no card. O fluxo é sempre
  `home/catálogo → página do produto → Hotmart`.
- **Presença no catálogo não significa que uma campanha paga está
  ativa.** Uma página em `/produtos/<slug>/` pode estar publicada e
  descobrível (production-ready) antes da primeira campanha de tráfego
  pago começar — são decisões independentes. Não confundir "produto
  publicado/divulgável" com "campanha paga ativa" em nenhuma
  documentação ou comunicação.
- A home não deve reafirmar "nenhum produto anunciado" nem mencionar
  fluxo de link de revisão por e-mail quando já existir ao menos um
  produto de produção publicado — isso contradiz a regra de
  publicação acima (a página já é um artefato de produção assim que
  existe em `/produtos/`).

## Regras derivadas

1. **Verificação obrigatória antes de implementar.** Antes de
   escrever código de uma pre-sell/landing pública, confirme
   `git remote -v` e o `git rev-parse --show-toplevel` do diretório de
   trabalho. Se o remote não for
   `trevodigitalconversoes/trevodigitalconversoes.github.io`, pare e
   migre/clone o repositório correto antes de continuar.
2. **GitHub Pages é o destino de hospedagem atual.** Deploy é feito a
   partir da branch `main`, pasta raiz (`/`), sem etapa de build — ver
   `README.md`.
3. **Não migrar para Vercel (ou outra hospedagem) sem uma ADR nova**
   que documente a justificativa.
4. **Não reescrever copy comercial aprovada.** Quando uma
   implementação reaproveitável existir em outro repositório (ex.:
   PR #51), a copy do Figma aprovado e/ou da fonte comercial aprovada
   deve ser preservada literalmente na migração — não "melhorada" por
   iniciativa própria do agente.
5. **Contato com a produtora não é uma exigência automática.** Nenhuma
   página pública deste repositório cria uma obrigação geral de
   contatar, autorizar ou aguardar aprovação da produtora antes de
   qualquer publicação. Contato com a produtora só é necessário quando
   uma das fontes abaixo exigir explicitamente:
   - regra explícita do próprio produto/produtora;
   - regra da Hotmart (ou outra plataforma de distribuição);
   - política da plataforma de anúncios usada na campanha;
   - contrato;
   - legislação aplicável (ex.: LGPD, Código de Defesa do Consumidor);
   - outra obrigação oficial equivalente.

   A ausência de uma dessas exigências **não significa ausência de
   compliance** — ela apenas significa que o envio à produtora não é
   um passo obrigatório do fluxo padrão. Revisão técnica (QA, testes,
   validação) acontece em branch/PR/ambiente local — nunca precisou de
   uma área pública de revisão para isso, e não precisa agora.
6. **Agentes de código não assumem autoria comercial.** Um agente que
   implementa uma página não é a produtora do conteúdo, não decide
   preço/garantia/comissão, e não deve inventar claims (depoimentos,
   escassez, urgência, garantia, autoridade) que não estejam na fonte
   aprovada (Figma e/ou copy comercial documentada).
7. **Implementação iniciada no repositório errado deve ser
   interrompida e migrada**, não descartada. O trabalho reaproveitável
   (copy, estrutura, assets, decisões de acessibilidade/responsivo,
   testes, evidências) deve ser preservado na migração sempre que
   houver fonte verificável.
8. **Exceções a qualquer regra acima exigem uma decisão arquitetural
   explícita** (nova ADR ou atualização desta), não uma escolha
   silenciosa de um agente durante a implementação.

## Consequências

- Toda pre-sell/landing pública do portfólio de afiliados vive neste
  repositório, exclusivamente em `/produtos/<slug>/` — nunca em
  `afiliados-mega-lab`, e nunca em `/aprovacao/` (removido).
- O AML permanece livre para experimentar arquiteturas
  (Next.js, route groups, etc.) para fins de prototipagem, mas esse
  código não é o artefato de publicação — ele é fonte de referência a
  ser adaptada para a arquitetura estática deste repositório (HTML +
  CSS, JavaScript mínimo só quando tecnicamente justificado).
- Cada migração de um protótipo do AML para este repositório deve
  documentar: origem, o que foi reaproveitado literalmente, o que foi
  adaptado, hashes de assets, e limitações/gaps encontrados (ex.:
  tokens de design não preservados, validações não realizadas).

## Fronteira público/privado (atualização 2026-08-08)

Adicionada em complemento a esta ADR, não substitui nenhuma regra
acima: separação entre este repositório (camada mínima de publicação) e
`trevodigitalconversoes/trevo-ops` (privado — tooling, testes, QA,
automações, evidências, documentação operacional). Regra completa em
`CLAUDE.md`/`AGENTS.md`, seção "Fronteira público/privado". Em resumo:
este repositório nunca deve conter `/tools`, testes internos,
automações, CLIs, integrações externas (ex.: Instagram/Meta) ou
documentação operacional extensa — isso vive em `trevo-ops`.

## Referências

- Migração de referência, plano de tracking, remoção de `/aprovacao/` e
  demais relatórios operacionais: `trevo-ops/docs/` (privado).
- `README.md` — estrutura geral do repositório e deploy.
