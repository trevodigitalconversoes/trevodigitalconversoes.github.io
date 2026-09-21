/*
 * Propagacao de parametros de campanha para o HotLink desta pre-sell.
 *
 * Reaproveita o contrato de tracking existente (assets/js/etapa_5_d_v1_tracking.js):
 *  - whitelist: window.__TREVO_TRACKING_CONFIG__.allowedCampaignParams;
 *  - src (g|<experimentId>|<utm_content>) fica DESATIVADO ate o proprietario definir o experimentId;
 *  - somente utm_source/medium/campaign/content/term seguem para a Hotmart.
 *
 * Diferenca proposital: NAO carrega PostHog, nao faz requests, nao grava
 * cookie/localStorage. Pagina sobre gestacao = categoria sensivel; a decisao
 * sobre analytics/replay fica para a revisao humana (ver README.md).
 * Falha aqui nunca impede o CTA: o href do HTML ja e o HotLink base.
 */
(function () {
  "use strict";
  var config = window.__TREVO_TRACKING_CONFIG__ || {};
  var allowed = config.allowedCampaignParams || [];
  var forwarded = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];
  function run() {
    try {
      var usp = new URLSearchParams(window.location.search);
      var params = {};
      allowed.forEach(function (k) { var v = usp.get(k); if (v) params[k] = v; });
      var anchors = document.querySelectorAll("a.cta-button[data-hotlink]");
      for (var i = 0; i < anchors.length; i++) {
        try {
          var url = new URL(anchors[i].getAttribute("href"));
          // src NAO e enviado: exigiria um experimentId proprio, ainda nao
          // definido pelo proprietario (mt01 pertence a outro microteste).
          // O parametro fixo ref (afiliado) ja esta no href e nunca e alterado.
          forwarded.forEach(function (k) { if (params[k]) url.searchParams.set(k, params[k]); });
          anchors[i].setAttribute("href", url.toString());
        } catch (e) { /* mantem o href estatico */ }
      }
    } catch (e) { /* sem parametros: segue com o href estatico */ }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
