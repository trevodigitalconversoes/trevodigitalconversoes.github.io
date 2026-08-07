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

### `/aprovacao/`

**Não é mais o fluxo padrão para novas pre-sells.** A pasta continua
existindo apenas para o caso histórico já publicado antes desta regra
(`100-aplicativos-uteis/`) e para eventuais casos excepcionais
futuros, que devem ser documentados explicitamente como exceção (ex.:
um comentário nesta seção ou uma nova entrada na tabela de páginas do
`README.md`) — não é mais assumida como o destino padrão de uma nova
implementação.

### Contato com produtor

Mantém-se a regra já decidida na versão original deste ADR: **não
solicitar aprovação nem contato com a produtora por padrão.** Contato
só ocorre quando regra oficial do produto, da Hotmart, da plataforma
de anúncios, contrato ou legislação aplicável exigir — ver regra 5 em
"Regras derivadas" abaixo. Essa regra não muda com a adoção do fluxo
production-first: publicar direto em `/produtos/` sem passar por
`/aprovacao/` **não é**, por si só, uma exigência de aprovação nova —
é a mesma ausência de exigência de sempre, aplicada de forma
consistente.

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
5. **Contato com a produtora não é uma exigência automática.** A
   existência da pasta `/aprovacao/` **não cria** uma obrigação geral
   de contatar, autorizar ou aguardar aprovação da produtora antes de
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
   um passo obrigatório do fluxo padrão. `/aprovacao/` é uma área
   **opcional** de revisão controlada (inclusive para QA interno),
   não um portão de aprovação de terceiros por padrão. Ver
   `aprovacao/README.md` para a convenção operacional dessa pasta.
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
  repositório, em `/produtos/<slug>/` (fluxo padrão, produção) ou,
  excepcionalmente, em `/aprovacao/<slug>/` (caso histórico/exceção
  documentada) — nunca em `afiliados-mega-lab`.
- O AML permanece livre para experimentar arquiteturas
  (Next.js, route groups, etc.) para fins de prototipagem, mas esse
  código não é o artefato de publicação — ele é fonte de referência a
  ser adaptada para a arquitetura estática deste repositório (HTML +
  CSS, JavaScript mínimo só quando tecnicamente justificado).
- Cada migração de um protótipo do AML para este repositório deve
  documentar: origem, o que foi reaproveitado literalmente, o que foi
  adaptado, hashes de assets, e limitações/gaps encontrados (ex.:
  tokens de design não preservados, validações não realizadas).

## Referências

- Migração de referência: `docs/etapa_3_a_v1_migracao_presell_trevo.md`
  (pre-sell "10 Dicas de Fotografia + 18 Presets de Lightroom",
  migrada de `afiliados-mega-lab` PR #51 para
  `/produtos/fotografia-presets-lightroom/`).
- Plano de tracking (investigação, sem implementação):
  `docs/etapa_3_b_v1_plano_tracking_nivel_0.md`.
- `aprovacao/README.md` — convenção da área de revisão.
- `README.md` — estrutura geral do repositório e deploy.
