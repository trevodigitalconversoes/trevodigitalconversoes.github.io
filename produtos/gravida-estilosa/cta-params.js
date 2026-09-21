/*
 * Propagacao de parametros de campanha para o HotLink desta pre-sell.
 *
 * Reaproveita o contrato de tracking existente (assets/js/etapa_5_d_v1_tracking.js):
 *  - whitelist: window.__TREVO_TRACKING_CONFIG__.allowedCampaignParams;
 *  - src no formato "g|<experimentId>|<utm_content>" (max 30 caracteres);
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
  var experiment = config.experimentId || "mt01";

  function seg(v) {
    return String(v || "").trim().toLowerCase().replace(/_/g, "-").replace(/\s+/g, "-")
      .replace(/[^a-z0-9-]/g, "").replace(/-{2,}/g, "-").replace(/^-+|-+$/g, "");
  }

  function buildSrc(creative) {
    var src = "g|" + (seg(experiment) || "mt01") + "|" + (seg(creative) || "none");
    return src.length > 30 ? "g|" + (seg(experiment) || "mt01") + "|none" : src;
  }

  function run() {
    try {
      var usp = new URLSearchParams(window.location.search);
      var params = {};
      allowed.forEach(function (k) { var v = usp.get(k); if (v) params[k] = v; });
      var anchors = document.querySelectorAll("a.cta-button[data-hotlink]");
      for (var i = 0; i < anchors.length; i++) {
        try {
          var url = new URL(anchors[i].getAttribute("href"));
          url.searchParams.set("src", buildSrc(params.utm_content));
          forwarded.forEach(function (k) { if (params[k]) url.searchParams.set(k, params[k]); });
          anchors[i].setAttribute("href", url.toString());
        } catch (e) { /* mantem o href estatico */ }
      }
    } catch (e) { /* sem parametros: segue com o href estatico */ }
  }

  window.__gravidaCtaInternals__ = { buildSrc: buildSrc };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
