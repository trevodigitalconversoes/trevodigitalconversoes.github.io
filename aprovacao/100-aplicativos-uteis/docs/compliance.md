# Compliance — "+100 Aplicativos Úteis" (afiliado Hotmart)

Checklist de regras obrigatórias e como cada uma é garantida no HTML
estático publicado (`../index.html`, `../styles.css`). Revise este
documento antes de aceitar qualquer alteração de copy.

> Este checklist foi adaptado para a versão atual da página, em HTML+CSS
> estático, sem build e sem JavaScript — ver `decisao_migracao_html_estatico.md`.

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
`index,follow` manualmente, depois de: aprovação explícita da produtora
e revisão final de conteúdo. O hotlink de afiliado já está configurado
(ver seção abaixo) — isso não é mais uma pendência para a troca de
`robots`.

## CTA da Hotmart — hotlink de afiliado configurado
O botão "Ver produto na Hotmart" (hero e CTA final) usa o link otimizado
para Google Ads, derivado do hotlink de afiliado confirmado na área de
Hotlinks da Hotmart:

```
https://go.hotmart.com/Q106592213V?redirectionUrl=https%3A%2F%2Fhotmart.com%2Fpt-br%2Fmarketplace%2Fprodutos%2F100-aplicativos-uteis-para-produtividade-empreendedora%2FN87977370D
```

Hotlink base (sem o parâmetro de redirecionamento para Google Ads):
`https://go.hotmart.com/Q106592213V`. O link usado nos CTAs preserva o
rastreamento de afiliado (gera comissão em compras via esse link) —
`target="_blank"`, `rel="noopener noreferrer sponsored"` em ambos.

**Antes de iniciar campanha paga**, ainda é necessário:
1. Testar manualmente o clique no CTA e confirmar que redireciona
   corretamente para a página do produto na Hotmart.
2. Confirmar na Hotmart e no Google Ads se esse é o formato de link
   recomendado para a campanha (o parâmetro `redirectionUrl` foi gerado
   como link otimizado para Ads).
3. Preencher a data real de verificação de preço/garantia
   (`[INSERIR_DATA_DE_VERIFICACAO]` na seção "Informações observadas na
   Hotmart").
4. Obter aprovação explícita da produtora sobre o conteúdo.

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
