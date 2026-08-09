/*
 * Tracking do Microteste Comercial 01 (PostHog + HotLink Hotmart).
 * Gerado/mantido a partir de trevodigitalconversoes/trevo-ops (privado)
 * -- contrato completo e gerador em trevo-ops/tools/tracking/. Este
 * arquivo e o unico artefato de tracking que vive neste repo publico
 * (roda no navegador).
 *
 * A partir de 2026-08-08 este arquivo tambem habilita, via
 * config.posthogInitOptions (gerado em Python, em trevo-ops):
 * autocapture, heatmaps, Web Vitals e Session Replay -- decisao
 * explicita do usuario de usar progressivamente mais capacidades do
 * PostHog nesta pre-sell.
 * Esse objeto e repassado a posthog.init() sem transformacao (ver
 * initPostHog abaixo), entao qualquer mudanca de config fica so no
 * Python.
 *
 * O que NAO muda com isso: `outbound_hotmart` continua a metrica de
 * conversao explicita e canonica (autocapture nao a substitui, so
 * adiciona contexto complementar); nenhuma chamada a identify()/
 * alias()/group()/setPersonProperties() existe neste arquivo; nenhuma
 * captura de payload de rede (request/response body) e habilitada.
 *
 * Regra inegociavel: falha de tracking NUNCA pode impedir o CTA. Cada
 * bloco que fala com o PostHog ou constroi URL esta em try/catch, e o
 * href do CTA sempre comeca com o HotLink base valido no HTML -- se este
 * script nunca rodar (bloqueado, erro, JS desabilitado), o clique ainda
 * leva ao HotLink correto, so sem enriquecimento de SRC/UTM.
 */
(function () {
  "use strict";

  var config = window.__TREVO_TRACKING_CONFIG__;
  if (!config || !config.posthogProjectToken) {
    return;
  }

  var ALLOWED_PARAMS = config.allowedCampaignParams || [];
  var HOTMART_FORWARDED_PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];
  var OUTBOUND_EVENT_PARAMS = HOTMART_FORWARDED_PARAMS.concat([
    "campaign_id", "ad_group_id", "ad_id", "device", "network", "matchtype", "gclid"
  ]);
  var SRC_MAX_LENGTH = 30;
  var SRC_FALLBACK_CREATIVE = "none";

  function readCampaignParams() {
    var out = {};
    try {
      var usp = new URLSearchParams(window.location.search);
      for (var i = 0; i < ALLOWED_PARAMS.length; i++) {
        var key = ALLOWED_PARAMS[i];
        var value = usp.get(key);
        if (value) out[key] = value;
      }
    } catch (err) {
      /* URLSearchParams indisponivel/erro: segue sem parametros de campanha */
    }
    return out;
  }

  function sanitizeSrcSegment(value) {
    return String(value || "")
      .trim()
      .toLowerCase()
      .replace(/_/g, "-")
      .replace(/\s+/g, "-")
      .replace(/[^a-z0-9-]/g, "")
      .replace(/-{2,}/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function buildHotmartSrc(experimentId, creativeCode) {
    var network = "g";
    var experiment = sanitizeSrcSegment(experimentId) || "mt01";
    var creative = sanitizeSrcSegment(creativeCode) || SRC_FALLBACK_CREATIVE;
    var src = network + "|" + experiment + "|" + creative;
    if (src.indexOf("_") !== -1 || src.length > SRC_MAX_LENGTH) {
      src = network + "|" + experiment + "|" + SRC_FALLBACK_CREATIVE;
    }
    return src;
  }

  function buildHotlink(baseUrl, src, campaignParams) {
    try {
      var url = new URL(baseUrl);
      url.searchParams.set("src", src);
      for (var i = 0; i < HOTMART_FORWARDED_PARAMS.length; i++) {
        var key = HOTMART_FORWARDED_PARAMS[i];
        if (campaignParams[key]) url.searchParams.set(key, campaignParams[key]);
      }
      return url.toString();
    } catch (err) {
      return baseUrl;
    }
  }

  // Fail-closed por design: se a sanitizacao falhar por qualquer motivo,
  // retorna null (nunca a URL bruta). Quem chama (beforeSend) trata null
  // removendo a propriedade em vez de transmiti-la sem sanitizar.
  function sanitizeCurrentUrl(rawUrl) {
    try {
      var url = new URL(rawUrl);
      var cleanParams = new URLSearchParams();
      var original = new URLSearchParams(url.search);
      original.forEach(function (value, key) {
        if (ALLOWED_PARAMS.indexOf(key) !== -1) cleanParams.set(key, value);
      });
      var query = cleanParams.toString();
      return url.origin + url.pathname + (query ? "?" + query : "");
    } catch (err) {
      return null;
    }
  }

  // Fail-closed: uma excecao aqui (ou uma falha de sanitizeCurrentUrl)
  // NUNCA deixa a URL bruta (com query string completa) ser transmitida.
  // Se nao for possivel produzir uma versao segura, a propriedade e
  // removida do evento em vez de enviada sem sanitizar -- o evento ainda
  // e enviado, so sem $current_url.
  function beforeSend(event) {
    try {
      if (event && event.properties && typeof event.properties.$current_url === "string") {
        var sanitized = sanitizeCurrentUrl(event.properties.$current_url);
        if (sanitized === null) {
          delete event.properties.$current_url;
        } else {
          event.properties.$current_url = sanitized;
        }
      }
    } catch (err) {
      if (event && event.properties) {
        delete event.properties.$current_url;
      }
    }
    return event;
  }

  var campaignParams = readCampaignParams();

  function initPostHog() {
    if (!window.posthog || typeof window.posthog.init !== "function") return null;
    try {
      var initOptions = {};
      for (var key in config.posthogInitOptions) {
        if (Object.prototype.hasOwnProperty.call(config.posthogInitOptions, key)) {
          initOptions[key] = config.posthogInitOptions[key];
        }
      }
      initOptions.api_host = config.posthogHost;
      initOptions.before_send = beforeSend;
      window.posthog.init(config.posthogProjectToken, initOptions);
      return window.posthog;
    } catch (err) {
      return null;
    }
  }

  function loadPostHogScript(onReady) {
    try {
      var script = document.createElement("script");
      script.src = config.posthogHost.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js";
      script.async = true;
      script.onload = function () {
        onReady(initPostHog());
      };
      script.onerror = function () {
        onReady(null);
      };
      document.head.appendChild(script);
    } catch (err) {
      onReady(null);
    }
  }

  var posthogInstance = null;
  loadPostHogScript(function (instance) {
    posthogInstance = instance;
  });

  function instrumentCta(anchor) {
    var location = anchor.getAttribute("data-cta-position") || "unknown";
    var creativeCode = campaignParams.utm_content || null;
    var src = buildHotmartSrc(config.experimentId, creativeCode);
    var finalHref = buildHotlink(config.hotlinkBase, src, campaignParams);

    // Progressive enhancement: o href original do HTML (HotLink base) ja
    // funciona sozinho; so o substituimos se conseguirmos montar um novo
    // com sucesso.
    anchor.setAttribute("href", finalHref);

    anchor.addEventListener("click", function () {
      if (!posthogInstance) return;
      try {
        var properties = {
          product_slug: config.productSlug,
          experiment_id: config.experimentId,
          cta_location: location
        };
        if (creativeCode) properties.creative_code = creativeCode;
        for (var i = 0; i < OUTBOUND_EVENT_PARAMS.length; i++) {
          var key = OUTBOUND_EVENT_PARAMS[i];
          if (campaignParams[key]) properties[key] = campaignParams[key];
        }
        posthogInstance.capture("outbound_hotmart", properties);
      } catch (err) {
        /* tracking nunca pode impedir a navegacao do CTA */
      }
    });
  }

  function instrumentAllCtas() {
    try {
      var anchors = document.querySelectorAll(
        'a.cta-button[href^="' + config.hotlinkBase + '"]'
      );
      for (var i = 0; i < anchors.length; i++) {
        instrumentCta(anchors[i]);
      }
    } catch (err) {
      /* CTAs seguem com o href estatico do HTML */
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", instrumentAllCtas);
  } else {
    instrumentAllCtas();
  }

  // Exposto de proposito para teste de regressao automatizado (trevo-ops,
  // tools/tracking/tests/) -- funcoes puras de transformacao de string/URL,
  // nunca incluem token/config real. Nao apagar: e a unica forma de testar
  // este arquivo sem duplicar a logica em outra linguagem.
  window.__trevoTrackingInternals__ = {
    sanitizeCurrentUrl: sanitizeCurrentUrl,
    beforeSend: beforeSend,
    buildHotmartSrc: buildHotmartSrc,
    buildHotlink: buildHotlink
  };
})();
