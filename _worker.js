// bpaau.org Worker entrypoint.
// - Enforces HTTPS
// - Redirects www -> apex
// - Redirects .html URLs to clean URLs (301, SEO-friendly)
// - Normalises trailing slashes
// - Applies the 301 redirect map from redirects.json (legacy URL migrations)
// - Serves static assets from ./public via the ASSETS binding
//   (ASSETS natively serves clean URLs: /about -> about.html)

import redirectConfig from "./redirects.json";

// Legacy path -> current path. Bundled at build time by wrangler.
// Edit redirects.json (not this file) to add a migration.
const REDIRECT_MAP = (redirectConfig && redirectConfig.redirects) || {};

// Files that must remain accessible at their .html URL (e.g. search-engine verification).
const VERIFICATION_FILES = new Set([
  "/google6c4a857337176f53.html",
]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. Enforce HTTPS on production hosts only (skip localhost/dev).
    const isLocalhost =
      url.hostname === "localhost" ||
      url.hostname === "127.0.0.1" ||
      url.hostname === "0.0.0.0" ||
      url.hostname.endsWith(".local") ||
      url.hostname.endsWith(".internal");
    if (url.protocol === "http:" && !isLocalhost) {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    // 2. Redirect www -> apex (preserve path + query).
    if (url.hostname === "www.bpaau.org") {
      url.hostname = "bpaau.org";
      return Response.redirect(url.toString(), 301);
    }

    let path = url.pathname;

    // 3. Allow verification files to pass through untouched.
    if (VERIFICATION_FILES.has(path)) {
      return env.ASSETS.fetch(request);
    }

    // 4. Redirect .html URLs to their clean equivalent (301 for SEO).
    if (path.endsWith(".html")) {
      let clean = path.slice(0, -5); // strip ".html"
      if (clean === "/index") clean = "/";
      url.pathname = clean;
      return Response.redirect(url.toString(), 301);
    }

    // 5. Normalise trailing slashes: /about/ -> /about (root stays "/").
    if (path.length > 1 && path.endsWith("/")) {
      url.pathname = path.slice(0, -1);
      return Response.redirect(url.toString(), 301);
    }

    // 6. Apply the legacy 301 redirect map. Runs after .html stripping and
    //    trailing-slash normalisation so every lookup sees a canonical clean
    //    path. Preserves query strings and hashes are client-side anyway.
    const redirectTarget = REDIRECT_MAP[url.pathname];
    if (redirectTarget) {
      url.pathname = redirectTarget;
      return Response.redirect(url.toString(), 301);
    }

    // 7. Serve from ASSETS. Clean URLs (/about) are natively resolved to
    //    about.html by the ASSETS binding â€” no manual rewrite needed.
    //    If a clean URL 404s, fall back to trying the .html file directly.
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

    // 8. Markdown Negotiation: when an AI agent asks for text/markdown,
    //    serve a clean Markdown rendering of the HTML page.
    const accept = request.headers.get("Accept") || "";
    if (
      accept.includes("text/markdown") &&
      response.status === 200 &&
      (response.headers.get("content-type") || "").includes("text/html")
    ) {
      const html = await response.text();
      const md = htmlToMarkdown(html, url.origin);
      return new Response(md, {
        status: 200,
        headers: {
          "Content-Type": "text/markdown; charset=utf-8",
          "Cache-Control": "public, max-age=600, stale-while-revalidate=86400",
        },
      });
    }

    // 9. Post-process response: add SEO/security headers that ASSETS doesn't set.
    return addResponseHeaders(response, path);
  },
};

// Add security + SEO headers. Cloudflare Workers' ASSETS binding doesn't
// consistently apply _headers, so we set them here on every response.
function addResponseHeaders(response, path) {
  const h = new Headers(response.headers);
  const ct = h.get("content-type") || "";

  // Always-on security headers
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

  // Content Security Policy: safe defaults for a static content site.
  // Inline styles/scripts are used in this codebase (theme + tiny inline JS),
  // and Google Fonts is the only external asset host, so allow those.
  if (!h.has("content-security-policy") && ct.includes("text/html")) {
    h.set(
      "Content-Security-Policy",
      "default-src 'self'; " +
      "script-src 'self' 'unsafe-inline'; " +
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
      "font-src 'self' https://fonts.gstatic.com data:; " +
      "img-src 'self' data: https:; " +
      "connect-src 'self'; " +
      "frame-ancestors 'self'; " +
      "base-uri 'self'; " +
      "form-action 'self'; " +
      "upgrade-insecure-requests"
    );
  }

  // Add charset to HTML Content-Type if missing
  if (ct.startsWith("text/html") && !ct.toLowerCase().includes("charset")) {
    h.set("Content-Type", "text/html; charset=utf-8");
  }

  // Cache-Control for HTML: short cache with stale-while-revalidate.
  // ASSETS' default is often max-age=0 for HTML; override so repeat visits are fast.
  if (ct.includes("text/html") && response.status === 200) {
    h.set("Cache-Control", "public, max-age=600, stale-while-revalidate=86400");
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: h,
  });
}




function decodeEntities(s) {
  return s
    .replace(/&nbsp;/g, " ")
    .replace(/&raquo;/g, "»")
    .replace(/&middot;/g, "·")
    .replace(/&bull;/g, "•")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&copy;/g, "(c)")
    .replace(/&reg;/g, "(r)")
    .replace(/&trade;/g, "(tm)")
    .replace(/&ndash;/g, "-")
    .replace(/&mdash;/g, "-");
}

function absoluteUrl(href, baseUrl) {
  if (!href) return "";
  href = href.trim();
  if (href.startsWith("http://") || href.startsWith("https://")) return href;
  if (href.startsWith("//")) return "https:" + href;
  if (href.startsWith("#")) return baseUrl + href;
  if (href.startsWith("mailto:") || href.startsWith("tel:")) return href;
  if (href.startsWith("/")) return "https://bpaau.org" + href;
  return baseUrl + "/" + href.replace(/^\.\//, "");
}

function htmlToMarkdown(html, baseUrl) {
  if (!html) return "";

  // 1. Cut out non-content blocks first.
  let doc = html.replace(/<(script|style|noscript|iframe|svg|canvas|form)[\s\S]*?<\/\1>/gi, " ");
  doc = doc.replace(/<nav[\s\S]*?<\/nav>/gi, " ");
  doc = doc.replace(/<header[\s\S]*?<\/header>/gi, " ");
  doc = doc.replace(/<footer[\s\S]*?<\/footer>/gi, " ");
  doc = doc.replace(/<aside[\s\S]*?<\/aside>/gi, " ");

  // 2. Isolate main content: <main>, else <article>, else body.
  let main = doc;
  const mMain = doc.match(/<main[\s\S]*?<\/main>/i);
  const mArt = doc.match(/<article[\s\S]*?<\/article>/i);
  if (mMain) main = mMain[0];
  else if (mArt) main = mArt[0];
  else {
    const mBody = doc.match(/<body[\s\S]*?<\/body>/i);
    if (mBody) main = mBody[0];
  }

  // 3. Drop the breadcrumb/CTA chunks that hurt readability.
  main = main.replace(/<div[^>]*class="[^"]*breadcrumb[^"]*"[\s\S]*?<\/div>/gi, " ");
  main = main.replace(/<div[^>]*class="[^"]*related[^"]*"[\s\S]*?<\/div>/gi, " ");
  main = main.replace(/<div[^>]*class="[^"]*product-card[^"]*"[\s\S]*?<\/div>/gi, " ");
  main = main.replace(/<div[^>]*class="[^"]*pxt-card[^"]*"[\s\S]*?<\/div>/gi, " ");
  main = main.replace(/<section[^>]*class="[^"]*(products|operators|grid-products)[^"]*"[\s\S]*?<\/section>/gi, " ");

  // 4. FAQ details/summary -> Q/A lines.
  main = main.replace(/<details[\s\S]*?<summary[^>]*>([\s\S]*?)<\/summary>([\s\S]*?)<\/details>/gi,
    function (m, q, a) {
      const qq = q.replace(/<[^>]+>/g, "").trim();
      const aa = a.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
      return "\n\n**Q: " + qq + "**\n\n" + aa + "\n";
    });

  // 5. Structural tags -> blank lines (headings handled next).
  main = main.replace(/<\/(p|div|section|article|li|tr|h1|h2|h3|h4|h5|h6|blockquote|table)>/gi, "\n\n");
  main = main.replace(/<(br|hr)\s*\/?>/gi, "\n");

  // 6. Headings.
  main = main.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, "\n\n# " + "$1".trim() + "\n");
  main = main.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, "\n\n## " + "$1".trim() + "\n");
  main = main.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, "\n\n### " + "$1".trim() + "\n");
  main = main.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, "\n\n#### " + "$1".trim() + "\n");
  main = main.replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, "\n\n##### " + "$1".trim() + "\n");
  main = main.replace(/<h6[^>]*>([\s\S]*?)<\/h6>/gi, "\n\n###### " + "$1".trim() + "\n");

  // 7. Lists.
  main = main.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, "- $1\n");
  main = main.replace(/<ul[\s\S]*?<\/ul>/gi, function (m) { return "\n" + m + "\n"; });
  main = main.replace(/<ol[\s\S]*?<\/ol>/gi, function (m) { return "\n" + m + "\n"; });

  // 8. Tables -> markdown tables.
  main = main.replace(/<table[\s\S]*?<\/table>/gi, function (tbl) {
    const rows = [];
    const trs = tbl.match(/<tr[\s\S]*?<\/tr>/gi) || [];
    for (const tr of trs) {
      const cells = [];
      const tds = tr.match(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi) || [];
      for (const td of tds) {
        cells.push(td.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
      }
      rows.push(cells);
    }
    if (!rows.length) return "";
    let out = "\n";
    const header = rows[0] || [];
    out += "| " + header.join(" | ") + " |\n";
    out += "| " + header.map(function () { return "---"; }).join(" | ") + " |\n";
    for (let i = 1; i < rows.length; i++) {
      out += "| " + rows[i].join(" | ") + " |\n";
    }
    return out + "\n";
  });

  // 9. Links & images.
  main = main.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi,
    function (m, href, text) {
      const t = text.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
      const h = absoluteUrl(href, baseUrl);
      if (!t || t === h) return h;
      return "[" + t + "](" + h + ")";
    });
  main = main.replace(/<a[^>]*href='([^']*)'[^>]*>([\s\S]*?)<\/a>/gi,
    function (m, href, text) {
      const t = text.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
      const h = absoluteUrl(href, baseUrl);
      if (!t || t === h) return h;
      return "[" + t + "](" + h + ")";
    });
  main = main.replace(/<img[^>]*src="([^"]*)"[^>]*>/gi, function (m, src) {
    const altM = m.match(/alt="([^"]*)"/);
    const alt = altM ? altM[1] : "";
    return "![ " + alt + " ](" + absoluteUrl(src, baseUrl) + ")";
  });

  // 10. Inline emphasis.
  main = main.replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, "**$1**");
  main = main.replace(/<b[^>]*>([\s\S]*?)<\/b>/gi, "**$1**");
  main = main.replace(/<em[^>]*>([\s\S]*?)<\/em>/gi, "*$1*");
  main = main.replace(/<i[^>]*>([\s\S]*?)<\/i>/gi, "*$1*");
  main = main.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, "`$1`");

  // 11. Strip any remaining tags.
  main = main.replace(/<[^>]+>/g, " ");

  // 12. Decode entities, normalise whitespace.
  main = decodeEntities(main);
  main = main.replace(/[ \t]+\n/g, "\n");
  main = main.replace(/\n{3,}/g, "\n\n");
  main = main.replace(/^\n+/, "").replace(/\s+$/, "");

  return main;
}
