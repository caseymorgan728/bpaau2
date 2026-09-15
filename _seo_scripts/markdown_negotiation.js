// markdown_negotiation.js — HTML -> Markdown converter for AI crawlers.
// Tested locally with node against the real public/ pages.

function decodeEntities(s) {
  return s
    .replace(/&nbsp;/g, " ")
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

// --- CLI test: node markdown_negotiation.js <file> [baseUrl] ---
if (typeof require !== "undefined" && require.main === module) {
  const fs = require("fs");
  const file = process.argv[2];
  const base = process.argv[3] || "https://bpaau.org/";
  if (!file) { console.error("usage: node markdown_negotiation.js <html> [baseUrl]"); process.exit(1); }
  const html = fs.readFileSync(file, "utf-8");
  const md = htmlToMarkdown(html, base);
  console.log(md.slice(0, 3000));
  console.log("\n---\nLENGTH:", md.length);
}

module.exports = { htmlToMarkdown };
