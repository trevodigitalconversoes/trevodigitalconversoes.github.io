# Compliance — "+100 Aplicativos Úteis" (afiliado Hotmart)

Checklist de regras obrigatórias e como cada uma é garantida no HTML
estático publicado (`../index.html`, `../styles.css`). Revise este
documento antes de aceitar qualquer alteração de copy.

> Este checklist foi originalmente escrito para a versão em Vite+React do
> projeto (ver `relatorio_auditoria_conversao_v1.md` e
> `relatorio_final_saneamento_v1.md`, preservados nesta pasta como
> histórico). Ele foi adaptado para a versão atual, em HTML+CSS estático
> sem build e sem nenhum `<script>` — ver `decisao_migracao_html_estatico.md`.

## Estrutura da página
| Regra | Status | Onde é garantido |
|---|---|---|
| Página única, sem rotas extras | ✅ | Um único `index.html`, sem roteador de nenhum tipo |
| Sem checkout próprio | ✅ | Os dois CTAs são `<a>` externos apontando para a página do produto na Hotmart, nunca um formulário de pagamento |
| Sem formulário | ✅ | Nenhum `<form>`/`<input>` em toda a página |
| Sem newsletter / captura de email | ✅ | Nenhum campo de email |
| Sem blog / área de membros | ✅ | Não há listagem de posts, rotas de conteúdo ou autenticação |
| Links institucionais sem `#` morto | ✅ | Política de Privacidade / Termos / Contato são `<details>`/`<summary>` no rodapé (sem JS); "Avisos importantes" usa âncora real (`#avisos-importantes`) |
| Avisos concentrados no final | ✅ | Seção "Avisos importantes" fica depois do FAQ e antes do CTA final — nada de aviso defensivo espalhado no meio da página |
| **Zero JavaScript** | ✅ | Nenhuma tag `<script>` em `index.html`. Ano do rodapé é texto fixo, não calculado. FAQ e conteúdo legal usam `<details>`/`<summary>` nativos do HTML |

## Proibições de conteúdo
| Regra | Status |
|---|---|
| Sem prints da Hotmart | ✅ nenhuma imagem/screenshot |
| Sem foto da produtora | ✅ nenhuma imagem de pessoa |
| Sem email/dados pessoais da produtora | ✅ apenas nome público exibido na Hotmart e "7 anos na plataforma" |
| Sem imagens de outros produtos da produtora | ✅ |
| Sem logos reais de aplicativos | ✅ nenhuma logo, apenas texto/tags de categoria |
| Sem depoimentos/avaliações inventadas | ✅ |
| Sem estatísticas/porcentagens falsas | ✅ o único número absoluto ("100+") descreve a quantidade de itens da curadoria, não performance |
| Sem gráficos de performance | ✅ |
| Sem urgência/escassez falsa | ✅ nenhum contador, nenhum "restam X vagas" |

## Promessas proibidas
Nenhum texto da página (ver `copy.md`) afirma produtividade, vendas,
lucro, renda, sucesso ou resultado automático garantido. Toda seção que
fala em benefício usa linguagem condicional ("pode ajudar", "tende a
fazer sentido"), e a seção de Valor + o FAQ reforçam explicitamente que
**não há garantia de resultado**:

> "Os resultados dependem de como cada pessoa escolhe e usa as
> ferramentas. O produto não garante produtividade, vendas ou resultados
> automáticos." — seção "O valor não está só na lista"

> "Não. Nenhum aplicativo ou curadoria garante resultado automático."
> — primeira pergunta do FAQ

## Divulgação de afiliado
- Barra superior e seção dedicada "Avisos importantes" deixam claro que é
  uma página independente de afiliado.
- FAQ reforça que "Essa é a página oficial?" → não.
- Rodapé repete a mesma informação em nota final.
- Os dois CTAs usam `rel="noopener noreferrer sponsored"`.

## Dados observados na Hotmart
Preço, garantia e demais dados (seção "Informações observadas na
Hotmart") são apresentados como "informações observadas", com nota final
pedindo para conferir a página oficial antes de comprar. **Não há data de
verificação preenchida** nesta versão — pendência documentada no README
da página e no relatório final.

## Robots / indexação
`<meta name="robots" content="noindex,nofollow">` fixo no HTML, sem
depender de nenhuma variável de build (não há mais build). Só deve virar
`index,follow` manualmente, depois de: hotlink de afiliado real
configurado, aprovação explícita da produtora, e revisão final de
conteúdo.

## CTA da Hotmart — link temporário, não afiliado
O botão "Ver produto na Hotmart" aponta, temporariamente, para a **URL
pública oficial do produto na Hotmart** (sem parâmetro de afiliado):
`https://hotmart.com/pt-br/marketplace/produtos/100-aplicativos-uteis-para-produtividade-empreendedora/N87977370D`.
Isso **não é** o hotlink de afiliado definitivo — é um link real e
funcional (não `href="#"`, não desabilitado), usado apenas até que o
hotlink de afiliado seja aprovado/configurado. A seção "Avisos
importantes" tem um card específico avisando isso explicitamente ao
visitante. Quando o hotlink de afiliado real for definido, ele deve
substituir essa URL nos dois CTAs (`index.html`).

## Acessibilidade (resumo)
- Link "Pular para o conteúdo" (`.skip-link`).
- Foco visível global (`:focus-visible` em `styles.css`).
- FAQ e conteúdo legal com `<details>`/`<summary>` nativos — acessíveis
  por teclado e leitor de tela sem nenhum JS ou ARIA extra.
- `prefers-reduced-motion` respeitado.
- `lang="pt-BR"` no documento.

## Tom com a produtora
- A seção "Sobre a criadora" usa apenas informações públicas observadas
  na Hotmart, sem dados pessoais, sem foto, sem crítica a outros produtos
  da criadora e sem tom defensivo.
- Nenhum texto da página compara ou insinua problemas com outros produtos
  da mesma criadora — o texto de recorte da análise ("Esta análise se
  limita ao produto... e às informações públicas observadas na Hotmart")
  aparece apenas uma vez, no final da página, de forma diplomática.
- A seção "Análise responsável da curadoria" mantém o conteúdo
  transparente, sem promessas.

## Política de Privacidade e Contato
- A Política de Privacidade não menciona nenhuma ferramenta de medição de
  audiência: a página não usa analytics/pixels/cookies no momento. O
  texto deixa explícito que, se alguma ferramenta de rastreamento for
  adicionada no futuro, esta política deve ser atualizada antes da
  publicação.
- O bloco de Contato deixa claro que dúvidas sobre produto, compra,
  pagamento, acesso ou garantia são sempre com a Hotmart. Para dúvidas
  sobre esta página, aponta para o canal público do Trevo Digital
  Conversões (`https://trevodigitalconversoes.github.io/#contato`).

## O que NÃO alterar sem nova revisão de compliance
- Textos de disclaimer/disclosure na seção "Avisos importantes" e no FAQ.
- A barra superior.
- O texto do rodapé.
- O `rel="noopener noreferrer sponsored"` dos CTAs.
- A regra de zero JavaScript na página.
