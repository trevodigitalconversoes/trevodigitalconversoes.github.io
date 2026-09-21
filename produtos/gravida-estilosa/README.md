# Pre-sell independente: Grávida Estilosa

**ESTADO (rodada 2): pronta para revisão humana. Sem merge/deploy autorizados.**

## Finalidade
Página de análise/pré-venda independente de afiliado do curso "Grávida Estilosa" (Hotmart), destino futuro de anúncios Google Ads. URL prevista: `https://trevodigitalconversoes.com.br/produtos/gravida-estilosa/`.

## HotLink / atribuição (rodada 2)
- CTA: `https://hotmart.com/pt-br/marketplace/produtos/gravida-estilosa/Q94220392S?ref=H106516913T`.
- `H106516913T` = código de afiliado deste produto. `xkc2j92m` = código da oferta (não é afiliado). `V106592210H` pertence a outro produto (10 Dicas de Fotografia): **nunca usar aqui**.
- O antigo `go.hotmart.com/H106516913T` redireciona ao site quebrado da produtora e a variante `redirectionUrl` retorna 400; ambos descartados.
- `ref=` é fixo no href e `cta-params.js` nunca o altera (nem por `?ref=` na URL da página).
- Para trocar o CTA: editar o `href` dos dois `a.cta-button[data-hotlink]` em `index.html`.

## Fontes
Ver `docs/gravida-estilosa/etapa_1_a_v1_pesquisa_fontes.md` e `etapa_1_b_v1_matriz_evidencias.md`. Base de fatos: página pública da Hotmart e checkout (21/09/2026). Recuperação histórica do site da produtora: sem resultados. Vídeo de divulgação: só a transcrição fornecida foi usada como pista, nunca como fato.

## Ativos
`assets/capa-produto-{360,675}.webp`: imagem de divulgação oficial fornecida pelo proprietário (`Postdoinstagramdiadoobstetrahomenagemminimalistamarromebege.png`, 675×675, a mesma usada pela Hotmart), convertida para WebP q85 (11 KB/28 KB); original não modificado e fora do repositório. Favicon reutiliza `assets/logo-social.png` do Trevo. Vídeo bruto (~260 MB) não versionado; incorporação futura só após confirmar proveniência ("Materiais de divulgação").

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
Conteúdo das aulas não verificado; a imagem contém o domínio antigo da produtora dentro dela; página não listada em `/produtos/`; canônico do repositório novo precisará reconciliar depois (`apps/public-site`).
