# Pre-sell independente: Grávida Estilosa

**ESTADO: NÃO PUBLICAR ANTES DE RESOLVER O BLOQUEIO DO HOTLINK (ver abaixo).**

## Finalidade
Página de análise/pré-venda independente de afiliado do curso "Grávida Estilosa" (Hotmart), destino futuro de anúncios Google Ads. URL prevista: `https://trevodigitalconversoes.com.br/produtos/gravida-estilosa/`.

## Bloqueio do HotLink (verificado em 21/09/2026)
- CTA configurado: `https://go.hotmart.com/H106516913T` (o link aprovado).
- Esse HotLink redireciona (302) para `nathconsultoria.com.br/pages/gravida-estilosa`, **que está com falha TLS**: o visitante vê erro.
- A variante `?redirectionUrl=` para a página pública da Hotmart ou para o checkout retorna **HTTP 400** (a Hotmart só aceita o domínio da produtora). Portanto não foi usada.
- Não foi trocado por link não afiliado. Saídas possíveis: a produtora restaurar o site; alterar a "página de vendas" configurada no produto; ou perguntar ao suporte Hotmart como enviar afiliado ao checkout com atribuição (o parâmetro `ref` não foi validado).
- Para trocar o CTA: editar `href` dos dois `a.cta-button` (`data-hotlink`) em `index.html`.

## Fontes
Ver `docs/gravida-estilosa/etapa_1_a_v1_pesquisa_fontes.md` e `etapa_1_b_v1_matriz_evidencias.md`. Base de fatos: página pública da Hotmart e checkout (21/09/2026). Recuperação histórica do site da produtora: sem resultados. Vídeo de divulgação: só a transcrição fornecida foi usada como pista, nunca como fato.

## Ativos
Nenhuma imagem/vídeo de terceiros. Design em CSS puro. Favicon e og:image reutilizam `assets/logo-social.png` do Trevo. Vídeo bruto (~260 MB) não versionado; incorporação futura só após confirmar proveniência ("Materiais de divulgação").

## Tracking
Reaproveita o contrato existente: whitelist de `assets/js/tracking-config.generated.js`; `src=g|<experimentId>|<utm_content>` (≤30 chars); somente `utm_*` repassados à Hotmart. `cta-params.js` **não carrega PostHog** (sem analytics/replay/cookies) porque o tema é gestação (categoria sensível) e o script existente está acoplado ao HotLink de outro produto. Decisão sobre analytics fica para revisão. `experimentId` usa `mt01` (valor existente na config); confirmar se este produto deve ter outro.

## Executar / validar localmente
```
py -3.13 -m http.server 8765
# abrir http://localhost:8765/produtos/gravida-estilosa/?utm_source=google&utm_content=teste&gclid=x
```
Esperado no CTA: `src=g|mt01|teste` + UTMs; `gclid` e desconhecidos não são repassados.

## Atualizar preço/garantia
Editar a seção "Informações comerciais" e o FAQ em `index.html`; só publicar dados conferidos no checkout atual (e datados). Garantia não confirmada.

## Regras de conteúdo
Nenhum claim sem linha "CONFIRMADA" na matriz. Sem depoimentos, avaliações, escassez, contadores, comissão ou menção ao prazo da afiliação. Sem Product/Offer/Review em structured data (apenas WebPage).

## Segurança
Sem formulários, sem dados pessoais, sem segredos. `rel="noopener noreferrer sponsored"` nos CTAs.

## Rollback
`git revert` do merge ou remoção da pasta `produtos/gravida-estilosa/`. Nada mais é alterado.

## Limitações
Conteúdo das aulas não verificado; sem garantia/bônus confirmados; página não listada em `/produtos/`; canônico do repositório novo precisará reconciliar depois (`apps/public-site`).
