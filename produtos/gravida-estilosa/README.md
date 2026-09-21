# Pre-sell independente: Grávida Estilosa

**ESTADO (rodada 3): pronta para revisão humana. Sem merge/deploy autorizados.**

## Finalidade
Página de análise/pré-venda independente de afiliado do curso "Grávida Estilosa" (Hotmart), destino futuro de anúncios Google Ads. URL prevista: `https://trevodigitalconversoes.com.br/produtos/gravida-estilosa/`.

## HotLink / atribuição (rodada 3)
- CTA (dois botões, `a.cta-button[data-hotlink]`): Google Ads URL oficial de **PRODUCT_PAGE** gerado pela Hotmart:
  `https://go.hotmart.com/H106516913T?dp=1&redirectionUrl=https%3A%2F%2Fhotmart.com%2Fpt-br%2Fmarketplace%2Fprodutos%2Fgravida-estilosa%2FQ94220392S`
- `H106516913T` = código de afiliado deste produto (afiliação 106516913). `xkc2j92m` = oferta (não é afiliado). `V106592210H` pertence a outro produto: **nunca usar aqui**.
- **NÃO usar** o HotLink SALES_PAGE (`go.hotmart.com/H106516913T` sem `dp=1`/`redirectionUrl`) nem o googleAdsUrl de SALES_PAGE: a Hotmart aponta `usesExternalPage = true` e eles levam ao site externo da produtora, hoje inacessível.
- `dp=1`, `redirectionUrl` e o código H106516913T ficam fixos no href. `cta-params.js` só acrescenta `utm_*` (contrato do Trevo) e ignora qualquer `ref`, `src`, `dp`, `redirectionUrl`, `gclid` etc. vindos da URL da página.
- Para trocar o CTA: editar o `href` dos dois botões em `index.html`.

## Fontes
Ver `docs/gravida-estilosa/etapa_1_a_v1_pesquisa_fontes.md` e `etapa_1_b_v1_matriz_evidencias.md`. Base de fatos: página pública da Hotmart e checkout (21/09/2026). Recuperação histórica do site da produtora: sem resultados. Vídeo de divulgação: só a transcrição fornecida foi usada como pista, nunca como fato.

## Ativos
- Origem do original: `Postdoinstagramdiadoobstetrahomenagemminimalistamarromebege.png` (675×675), imagem oficial do produto fornecida pelo proprietário (a mesma usada pela Hotmart). SHA-256 `98d42830…bcbab2`. **O original foi preservado sem alteração**, fora do repositório (`Projetos\trevodigitalconversoes-assets-originais\`).
- Derivada: `assets/capa-produto-{360,675}.webp` (WebP q88, ~12 KB e ~30 KB). Remove **exclusivamente** as referências de contato hoje indisponíveis (perfil do Instagram e endereço do site da produtora), com preenchimento do fundo em degradê apenas nessa área. Pessoa, título "Grávida Estilosa", "por Nathália Costa" e composição permanecem intactos.
- Finalidade: exibir a capa do produto na pre-sell sem oferecer chamada para destinos indisponíveis. Favicon reutiliza `assets/logo-social.png` do Trevo.
- Vídeo bruto (~260 MB) não versionado; incorporação futura só após confirmar proveniência ("Materiais de divulgação").

## Tracking
Reaproveita o contrato existente: whitelist de `assets/js/tracking-config.generated.js`; somente `utm_*` repassados. **`src` está desativado**: exige um `experimentId` próprio a ser definido pelo proprietário (`mt01` pertence a outro microteste). `cta-params.js` **não carrega PostHog** (sem analytics/replay/cookies) porque o tema é gestação (categoria sensível) e o script existente está acoplado ao HotLink de outro produto. Decisão sobre analytics fica para revisão. DECISÃO PENDENTE: definir `experimentId` deste produto.

## Executar / validar localmente
```
py -3.13 -m http.server 8765
# abrir http://localhost:8765/produtos/gravida-estilosa/?utm_source=google&utm_content=teste&gclid=x
```
Esperado no CTA: `ref=H106516913T` + UTMs; `gclid`, `src`, `ref` da URL e desconhecidos não são repassados.

## Atualizar preço/garantia
Editar a seção "Informações comerciais" e o FAQ em `index.html`; só publicar dados conferidos no checkout atual (e datados). Garantia de 7 dias confirmada na Hotmart em 21/09/2026.

## Regras de conteúdo
Nenhum claim sem linha "CONFIRMADA" na matriz. Sem depoimentos, avaliações, escassez, contadores, comissão ou menção ao prazo da afiliação. Sem Product/Offer/Review em structured data (apenas WebPage).

## Segurança
Sem formulários, sem dados pessoais, sem segredos. `rel="noopener noreferrer sponsored"` nos CTAs.

## Rollback
`git revert` do merge ou remoção da pasta `produtos/gravida-estilosa/`. Nada mais é alterado.

## Limitações
Conteúdo das aulas não verificado; página não listada em `/produtos/`; canônico do repositório novo precisará reconciliar depois (`apps/public-site`).
