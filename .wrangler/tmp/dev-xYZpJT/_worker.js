var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// redirects.json
var redirects_default = {
  _comment: "301 redirect map for bpaau.org. Consumed at runtime by _worker.js, which imports this file and issues a permanent redirect on any exact path match. Keys and values are root-relative, no trailing slash (the worker normalises trailing slashes before lookup). Never delete an entry once it ships - old URLs stay indexed for a long time and removing a row turns a working 301 into a 404.",
  _generated: "2026-08-31",
  redirects: {
    "/ausmegaways44": "/ausmegaways-review",
    "/bestrtp44-aus": "/bestrtp-review",
    "/freecredit777-aus": "/freecredit777-review",
    "/lockrespin88": "/lockrespin-review",
    "/megawin33-au": "/megawin33-review",
    "/nodepspin22": "/nodepspin-review",
    "/payid-withdraw44": "/payid-withdraw-review",
    "/blog-bonus-guides": "/blog/bonus-guides",
    "/blog-fast-cashouts": "/blog/fast-cashouts",
    "/blog-promo-guides": "/blog/promo-guides",
    "/blog-top-pokies": "/blog/top-pokies",
    "/blog-winning-tips": "/blog/winning-tips",
    "/top-10-easiest-profit-pokies-2026": "/best-high-rtp-pokies-australia-2026"
  }
};

// _worker.js
var REDIRECT_MAP = redirects_default && redirects_default.redirects || {};
var VERIFICATION_FILES = /* @__PURE__ */ new Set([
  "/google6c4a857337176f53.html"
]);
var worker_default = {
  async fetch(request, env) {
    const url = new URL(request.url);
    const isLocalhost = url.hostname === "localhost" || url.hostname === "127.0.0.1" || url.hostname === "0.0.0.0" || url.hostname.endsWith(".local") || url.hostname.endsWith(".internal");
    if (url.protocol === "http:" && !isLocalhost) {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    if (url.hostname === "www.bpaau.org") {
      url.hostname = "bpaau.org";
      return Response.redirect(url.toString(), 301);
    }
    let path = url.pathname;
    if (VERIFICATION_FILES.has(path)) {
      return env.ASSETS.fetch(request);
    }
    if (path.endsWith(".html")) {
      let clean = path.slice(0, -5);
      if (clean === "/index") clean = "/";
      url.pathname = clean;
      return Response.redirect(url.toString(), 301);
    }
    if (path.length > 1 && path.endsWith("/")) {
      url.pathname = path.slice(0, -1);
      return Response.redirect(url.toString(), 301);
    }
    const redirectTarget = REDIRECT_MAP[url.pathname];
    if (redirectTarget) {
      url.pathname = redirectTarget;
      return Response.redirect(url.toString(), 301);
    }
    let response = await env.ASSETS.fetch(request);
    if (response.status === 404 && !path.includes(".") && path !== "/") {
      const htmlUrl = new URL(request.url);
      htmlUrl.pathname = path + ".html";
      const htmlRequest = new Request(htmlUrl.toString(), request);
      const htmlResponse = await env.ASSETS.fetch(htmlRequest);
      if (htmlResponse.status !== 404) {
        response = htmlResponse;
      }
    }
    return addResponseHeaders(response, path);
  }
};
function addResponseHeaders(response, path) {
  const h = new Headers(response.headers);
  const ct = h.get("content-type") || "";
  if (!h.has("strict-transport-security"))
    h.set("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload");
  if (!h.has("x-content-type-options"))
    h.set("X-Content-Type-Options", "nosniff");
  if (!h.has("referrer-policy"))
    h.set("Referrer-Policy", "strict-origin-when-cross-origin");
  if (!h.has("permissions-policy"))
    h.set("Permissions-Policy", "interest-cohort=(), browsing-topics=()");
  if (!h.has("x-frame-options"))
    h.set("X-Frame-Options", "SAMEORIGIN");
  if (!h.has("content-security-policy") && ct.includes("text/html")) {
    h.set(
      "Content-Security-Policy",
      "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests"
    );
  }
  if (ct.startsWith("text/html") && !ct.toLowerCase().includes("charset")) {
    h.set("Content-Type", "text/html; charset=utf-8");
  }
  if (ct.includes("text/html") && response.status === 200) {
    h.set("Cache-Control", "public, max-age=600, stale-while-revalidate=86400");
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: h
  });
}
__name(addResponseHeaders, "addResponseHeaders");

// ../../../AppData/Local/Doubao/User Data/sandbox_runtime/.cache/node/npm-cache/_npx/32026684e21afda6/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../../../AppData/Local/Doubao/User Data/sandbox_runtime/.cache/node/npm-cache/_npx/32026684e21afda6/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    const body = JSON.stringify(error);
    const headers = {
      "Content-Type": "application/json",
      "MF-Experimental-Error-Stack": "true"
    };
    const encoded = encodeURIComponent(body);
    if (encoded.length <= 8192) {
      headers["MF-Experimental-Error-Stack-Payload"] = encoded;
    }
    return new Response(body, { status: 500, headers });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-lXHqSa/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = worker_default;

// ../../../AppData/Local/Doubao/User Data/sandbox_runtime/.cache/node/npm-cache/_npx/32026684e21afda6/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-lXHqSa/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  scheduledTime;
  cron;
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=_worker.js.map
