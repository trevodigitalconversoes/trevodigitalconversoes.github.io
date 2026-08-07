# Etapa 3B — Plano de tracking Nível 0 (investigação, sem implementação)

- **Status:** planejamento. **Nenhum código de tracking foi adicionado
  nesta etapa** — nem no HTML de `produtos/fotografia-presets-lightroom/`
  nem em nenhuma outra página. Este documento só registra a
  investigação e a recomendação.
- **Escopo:** o mínimo necessário para medir a pre-sell "10 Dicas de
  Fotografia + 18 Presets de Lightroom" (e, por extensão, qualquer
  outra pre-sell futura em `/produtos/`) — visita, cliques nos dois
  CTAs, e atribuição de origem/campanha.

## O que precisamos medir (Nível 0)

1. Visita à pre-sell.
2. Clique no CTA principal (hero).
3. Clique no CTA final (outbound para Hotmart).
4. Origem/campanha (`utm_source`, `utm_medium`, `utm_campaign`,
   `utm_content`, identificador de criativo).

## Respostas

### 1. PostHog é adequado à página estática atual?

Sim, com ressalva. PostHog JS (`posthog-js`) é um script client-side
que não exige backend nem build — funciona embutido via `<script>` em
HTML estático, o que é compatível com a arquitetura atual (zero
JavaScript hoje, mas a adição seria só deste script, não um
framework). A única mudança estrutural necessária é permitir uma tag
`<script>` na página — hoje `produtos/fotografia-presets-lightroom/`
não tem nenhuma (ver `docs/etapa_3_a_v1_migracao_presell_trevo.md`).

### 2. Qual configuração minimiza coleta de dados?

`cookieless_mode: "always"` (documentação oficial:
`https://posthog.com/docs/tutorials/cookieless-tracking`,
`https://posthog.com/docs/privacy/data-collection`). Nesse modo:

- Nenhum cookie e nenhum `localStorage`/`sessionStorage` são usados
  para identificar o visitante.
- `identify()` **não é suportado** neste modo (não precisamos dele —
  não há login/conta nesta pre-sell).
- A contagem de usuários usa hashes preservando privacidade
  calculados no servidor da PostHog, não um ID persistente no
  navegador.

```javascript
posthog.init("<ph_project_token>", {
  cookieless_mode: "always",
  api_host: "https://us.i.posthog.com", // ou instância self-hosted/EU, a definir
  defaults: "2026-05-30",
});
```

Alternativa mais simples, mas menos "oficialmente cookieless": setar
apenas `persistence: 'memory'` no `init()`, que evita cookies mas ainda
é um modo de configuração geral, não a feature dedicada de privacidade
da PostHog. **Recomendação: usar `cookieless_mode: "always"`**, por
ser a opção com garantia documentada de "sem cookie, sem storage".

### 3. Cookies/localStorage são usados nessa configuração?

Não, com `cookieless_mode: "always"`. Isso é o ponto central da
recomendação — elimina a necessidade de mapear esta ferramenta como
"cookie" na Política de Privacidade.

### 4. Podemos usar modo cookieless ou equivalente oficialmente suportado?

Sim — `cookieless_mode: "always"` é uma feature de primeira classe da
PostHog, documentada oficialmente (não é workaround). Existe também
`cookieless_mode: "on_reject"`, que **assume um banner de
consentimento** (só grava dado após rejeição/consentimento
explícito) — não é necessário para o Nível 0 se optarmos direto por
`"always"`.

### 5. Quais eventos/propriedades exatamente serão enviados?

Proposta mínima (a implementar só na próxima etapa, não nesta):

| Evento | Quando dispara | Propriedades |
|---|---|---|
| `presell_page_view` | Carregamento da página | `product_slug` (`fotografia-presets-lightroom`), `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `creative_id` (custom, via `custom_campaign_params`) |
| `presell_cta_click` | Clique em qualquer CTA para a Hotmart | `product_slug`, `cta_position` (`hero`/`final`), mesmas UTMs acima (herdadas do contexto da sessão/memória, já que não há cookie persistente) |

Nenhuma outra propriedade (sem PII, sem e-mail, sem nome, sem
identificador de dispositivo persistente).

### 6. O que precisamos alterar na Política de Privacidade?

Mesmo em modo cookieless, a página passaria a carregar um script de
terceiro (PostHog) que processa dados (IP truncado/hash, user agent,
página vista, evento de clique) — isso precisa ser descrito
explicitamente antes de ativar:

- Nome da ferramenta (PostHog) e finalidade (medir visitas e cliques
  nos CTAs, sem identificar a pessoa individualmente).
- Confirmação de que não são usados cookies nem armazenamento local
  (`cookieless_mode: "always"`).
- Dados efetivamente processados (IP, user agent, página, evento,
  UTMs) e que não incluem nome/e-mail/documento.
- Base legal (LGPD): provavelmente legítimo interesse para
  estatística agregada, a confirmar com quem decide a política do
  Trevo — **fora do escopo desta investigação técnica**.
- Local de processamento dos dados (região do host PostHog escolhido
  — Cloud US, Cloud EU, ou self-hosted).

### 7. Precisaremos de banner/consentimento antes do carregamento?

Com `cookieless_mode: "always"`, a documentação da PostHog não exige
um banner de consentimento para essa configuração específica (ao
contrário do modo `on_reject`, que é desenhado justamente para
banners). Ainda assim, a exigência real de banner depende da política
de privacidade/cookies que for adotada pelo Trevo e de orientação
jurídica sobre LGPD para o caso concreto — **essa decisão não foi
tomada nesta investigação técnica** e não deve ser assumida
automaticamente como dispensada.

### 8. Como validar eventos antes de liberar orçamento?

Antes de qualquer campanha paga:

1. Ativar em ambiente local/staging (branch separada), nunca direto
   em produção.
2. Confirmar no dashboard da PostHog (aba "Activity"/"Live events")
   que `presell_page_view` e `presell_cta_click` chegam com as
   propriedades esperadas, testando com URLs de exemplo contendo
   `utm_source`/`utm_medium`/`utm_campaign`/`utm_content` fictícios.
3. Confirmar que nenhum cookie nem entrada de `localStorage` é criada
   (inspecionar Application/Storage no DevTools).
4. Só então habilitar em produção, sem UTMs de campanha real ainda,
   navegando manualmente (sem clicar no CTA de verdade) para validar
   o evento de `page_view` em produção.
5. Nenhum clique real no hotlink deve ser necessário para validar
   `presell_cta_click` — o evento pode ser dispsarado no `onClick`
   antes da navegação, e testado com `preventDefault` temporário em
   ambiente de teste, não em produção.

### 9. Como correlacionar UTMs/creative ID com cliques no CTA?

Usando `custom_campaign_params: ["creative_id"]` (ou nome equivalente)
no `init()` da PostHog para capturar automaticamente um parâmetro
customizado de URL (`?creative_id=...`) junto com as UTMs padrão, e
incluindo essas mesmas propriedades no evento `presell_cta_click` (não
só no `page_view`) — assim cada clique carrega consigo a mesma origem
da visita que o gerou, mesmo sem cookie persistente (a doc oficial de
UTM segmentation aceita `$set`/propriedades customizadas por evento
quando não há cookie, ver seção 5 acima).

### 10. Como reconciliar posteriormente com dados da Hotmart?

Não há integração nativa comprovada entre PostHog e Hotmart nesta
investigação. A reconciliação prática seria manual/indireta:

- Usar `utm_content`/`creative_id` únicos por criativo/campanha nos
  links de anúncio que apontam para a pre-sell (não no hotlink da
  Hotmart em si, que já não recebe parâmetros — ver
  `docs/etapa_3_a_v1_migracao_presell_trevo.md`).
- Comparar, por janela de tempo e campanha, o volume de
  `presell_cta_click` (PostHog) com o volume de vendas/cliques
  reportado pelo painel da Hotmart para o mesmo produto/hotlink no
  mesmo período — reconciliação agregada por período, não por
  clique individual (a Hotmart não recebe nenhum identificador do
  lado da PostHog nesta configuração).
- Qualquer reconciliação 1:1 por usuário exigiria anexar parâmetros à
  URL do hotlink da Hotmart — o que a etapa 3A explicitamente evitou
  fazer por falta de evidência de que a Hotmart repassa/preserva
  query strings arbitrários. Confirmar esse comportamento com a
  documentação da Hotmart antes de mudar essa decisão.

## Fontes consultadas

- `https://posthog.com/docs/tutorials/cookieless-tracking`
- `https://posthog.com/docs/privacy/data-collection`
- `https://posthog.com/docs/data/utm-segmentation`
- `https://posthog.com/docs/getting-started/install`

## Recomendação

1. Adotar **PostHog JS** com `cookieless_mode: "always"` como Nível 0
   de tracking para as pre-sells de `/produtos/`.
2. Antes de ativar em qualquer página de produção: atualizar a
   Política de Privacidade (pergunta 6), decidir a região de
   hospedagem dos dados, e confirmar internamente se algum
   consentimento é necessário apesar do modo cookieless (pergunta 7).
3. Implementar e validar em uma branch separada, seguindo o checklist
   da pergunta 8, antes de qualquer liberação de orçamento de
   campanha.
4. Usar `custom_campaign_params` para um `creative_id` próprio, para
   viabilizar a correlação criativo → clique (pergunta 9).
5. Tratar a reconciliação com a Hotmart como agregada/por período, não
   por usuário individual, salvo decisão futura explícita de anexar
   parâmetros ao hotlink (pergunta 10).

**Nesta etapa (3B), nenhuma dessas ações foi executada** — é
puramente um plano para uma etapa futura (3C ou equivalente), a ser
aberta como uma nova branch/PR quando for decidido ativar tracking de
verdade.
