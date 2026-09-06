# -*- coding: utf-8 -*-
"""FINAL pre-publishing SEO audit for bpaau.org. Read-only (no fixes here)."""
import os, re, json, sys, urllib.parse
from html.parser import HTMLParser
from collections import defaultdict, Counter

ROOT = r"C:\Users\User\Documents\GitHub\Australia igaming website"
PUB = os.path.join(ROOT, "public")

OPERATORS = {
    "1XAUD": "https://1xaud.com/register",
    "GD8": "https://gd8au.com/register",
    "MR BLUEY": "https://mrblueyau.com/register",
    "1XACE": "https://1xaceau.com/register",
    "GARCAT8": "https://garcat8.com/register",
    "TOY STORY 9": "https://toystory9au.com/register",
}
OP_SET = set(OPERATORS.values())

def list_html():
    out = []
    for dp, dn, fn in os.walk(PUB):
        for f in fn:
            if f.lower().endswith(".html"):
                out.append(os.path.join(dp, f))
    return sorted(out)

def relpath(p):
    return os.path.relpath(p, PUB).replace("\\", "/")

def read(p):
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read()

# ---------- Parsers ----------
class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.meta = {}          # (name, property) -> content
        self.title = None
        self.h1s = []
        self.skip = False
        self.h1_text = []
        self.links = []         # (href, attrs dict)
        self.imgs = []          # attrs dict
        self.ld_blocks = []     # raw strings
        self.in_script = False
        self.in_style = False
        self.script_buf = []
        self.script_type = None
        self.style_blocks = 0
        self.other_scripts = 0
        self.in_nav = False
        self.in_footer = False
        self.in_header = False
        self.in_main = False
        self.depth_main = 0
        self.body_tokens = []
        self.tag_stack = []
        self.rg_banner = False
        self.product_grid = False
        self.game_grid = False
        self.game_cards = 0
        self.game_card_ctas = []
        self.inline_figures = 0
        self.details_count = 0
        self.faq_details = 0
        self.canonical = None
        self.og_tags = set()
        self.twitter_tags = set()
        self.has_viewport = False
        self.has_charset = False
        self.fetchpriority_high_imgs = 0
        self.detail_is_faq = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        self.tag_stack.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            if name == "viewport":
                self.has_viewport = True
            if a.get("charset"):
                self.has_charset = True
            if name:
                self.meta[name] = a.get("content", "")
            if prop.startswith("og:"):
                self.og_tags.add(prop)
            if prop == "og:url" or name == "twitter:card":
                pass
            if name.startswith("twitter:"):
                self.twitter_tags.add(name)
            if name == "robots":
                self.meta["_robots"] = a.get("content", "")
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
        if tag == "title":
            self.skip = True
        if tag == "h1":
            self.h1s.append(a.get("class", ""))
            self.h1_text = []
        if tag == "a":
            self.links.append((a.get("href", ""), a))
            if "skip" in cls:
                self.skip_link = True
            if "rg-banner" in cls:
                self.rg_banner = True
        if tag == "aside" and "rg-banner" in cls:
            self.rg_banner = True
        if tag == "img":
            self.imgs.append(a)
            if a.get("fetchpriority") == "high":
                self.fetchpriority_high_imgs += 1
        if tag == "script":
            self.in_script = True
            self.script_type = a.get("type", "")
            self.script_buf = []
            if self.script_type != "application/ld+json":
                self.other_scripts += 1
        if tag == "style":
            self.in_style = True
            self.style_blocks += 1
        if tag == "nav":
            self.in_nav = True
        if tag == "footer":
            self.in_footer = True
        if tag == "header":
            self.in_header = True
        if tag == "main":
            self.in_main = True
        if tag == "div" and "product-grid" in cls:
            self.product_grid = True
        if tag == "div" and "game-grid" in cls:
            self.game_grid = True
        if tag == "article" and "game-card" in cls:
            self.game_cards += 1
        if tag == "figure" and "inline-figure" in cls:
            self.inline_figures += 1
        if tag == "details":
            self.details_count += 1
            if "faq" in cls:
                self.faq_details += 1
        # capture CTA links
        if tag == "a" and "game-card__cta" in cls:
            self.game_card_ctas.append(a.get("href", ""))

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == "title":
            self.skip = False
        if tag == "h1":
            self.skip = False
        if tag == "script":
            self.in_script = False
            if self.script_type == "application/ld+json":
                self.ld_blocks.append("".join(self.script_buf))
            self.script_buf = []
            self.script_type = None
        if tag == "style":
            self.in_style = False
        if tag == "nav":
            self.in_nav = False
        if tag == "footer":
            self.in_footer = False
        if tag == "header":
            self.in_header = False
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.skip:
            if self.h1_text is not None:
                self.h1_text.append(data)
            self.title = (self.title or "") + data
            return
        if self.in_script or self.in_style:
            if self.in_script:
                self.script_buf.append(data)
            return
        if self.in_nav or self.in_footer or self.in_header:
            return
        if self.in_main:
            self.body_tokens.append(data)

def parse_page(path):
    raw = read(path)
    p = MetaParser()
    p.feed(raw)
    body_text = " ".join(p.body_tokens)
    words = len(re.findall(r"\S+", body_text))
    title = (p.title or "").strip()
    h1 = " ".join("".join(p.h1_text).split()) if p.h1_text else ""
    return p, raw, words, title, h1

# ---------- Resolve internal link ----------
def resolve_internal(href, page_path):
    """Return (exists, resolved_rel_path_or_None, kind). kind: internal/anchor/mailto/tel/external."""
    if href is None:
        return None
    h = href.strip()
    if h.startswith("mailto:") or h.startswith("tel:"):
        return ("contact", None)
    if h.startswith("#"):
        return ("anchor", None)
    if h.startswith("http://") or h.startswith("https://"):
        if "bpaau.org" in h or "bpaau.com" in h:
            return ("internal_http", h)
        return ("external", h)
    if h.startswith("//"):
        return ("external", h)
    if h.startswith("/"):
        return ("internal_abs", h)
    # relative
    return ("internal_rel", h)

def target_exists(href, page_path):
    """Resolve an internal href against public/ and check the file exists."""
    h = href.split("#")[0].split("?")[0]
    if not h:
        return True  # anchor only
    if h.startswith("/"):
        local = h[1:]
    else:
        base = os.path.dirname(page_path)
        local = os.path.normpath(os.path.join(os.path.relpath(base, PUB), h)).replace("\\", "/")
    local = urllib.parse.unquote(local)
    # clean URL resolution
    candidates = []
    if local == "":
        candidates.append("index.html")
    else:
        # /foo -> /foo.html
        candidates.append(local + ".html")
        # /foo/ -> /foo/index.html
        candidates.append(local.rstrip("/") + "/index.html")
        # /foo/index.html (already)
        if local.endswith(".html"):
            candidates.append(local)
        # /blog -> /blog/index.html
        candidates.append(os.path.join(local, "index.html"))
    for c in candidates:
        if os.path.isfile(os.path.join(PUB, c)):
            return True, c
    return False, local

def main():
    pages = list_html()
    report = {
        "total_pages": len(pages),
        "pages": [],
        "broken_links": [],
        "broken_images": [],
        "missing_alt": [],
        "missing_dims": [],
        "missing_lazy": [],
        "missing_lang": [],
        "missing_viewport": [],
        "missing_title": [],
        "missing_desc": [],
        "missing_canonical": [],
        "missing_og": [],
        "missing_twitter": [],
        "bad_h1": [],
        "missing_skip": [],
        "missing_rg": [],
        "https_internal": [],
        "html_ext_in_href": [],
        "affiliate_counts": Counter(),
        "affiliate_bad_attrs": [],
        "jsonld_total": 0,
        "jsonld_invalid": [],
        "jsonld_types": defaultdict(set),
        "faq_mismatch": [],
        "mojibake_files": [],
        "short_pages": [],
        "total_words": 0,
        "game_pages": [],
        "home_game_cards": 0,
        "inline_pages": {},
        "product_grid_pages": 0,
        "external_fonts": 0,
        "other_scripts": 0,
        "inline_styles": 0,
        "all_internal_links": 0,
        "external_links": 0,
        "anchor_links": 0,
        "contact_links": 0,
    }

    MOJI = ["â€", "Â·", "Â»", "Ã©", "Ã¨", "â€™", "â€œ", "â€"]
    # We only flag the canonical mojibake sequences requested, but also catch common ones.
    MOJI_CHECK = ["â€", "Â·", "Â»", "Ã©", "Ã¨"]

    PILLAR_INLINE = [
        "best-high-rtp", "legality", "no-deposit", "payid-cashouts",
        "mobile", "curacao-licence", "free-chips", "fastest-withdrawal"
    ]
    inline_found = {k: 0 for k in PILLAR_INLINE}

    for pp in pages:
        rel = relpath(pp)
        p, raw, words, title, h1 = parse_page(pp)
        entry = {"file": rel, "words": words, "title": title}
        report["total_words"] += words

        # ---- meta checks ----
        if p.lang != "en-AU":
            report["missing_lang"].append((rel, p.lang))
        if not p.has_viewport:
            report["missing_viewport"].append(rel)
        if not title:
            report["missing_title"].append(rel)
        desc = p.meta.get("description", "")
        if not desc:
            report["missing_desc"].append(rel)
        if not p.canonical:
            report["missing_canonical"].append(rel)
        need_og = {"og:title", "og:description", "og:type", "og:url", "og:image"}
        if not need_og.issubset(p.og_tags):
            report["missing_og"].append((rel, sorted(need_og - p.og_tags)))
        need_tw = {"twitter:card", "twitter:title", "twitter:description", "twitter:image"}
        if not need_tw.issubset(p.twitter_tags):
            report["missing_twitter"].append((rel, sorted(need_tw - p.twitter_tags)))
        if len(p.h1s) != 1:
            report["bad_h1"].append((rel, len(p.h1s)))
        if not getattr(p, "skip_link", False):
            report["missing_skip"].append(rel)
        if not p.rg_banner:
            report["missing_rg"].append(rel)

        # ---- links ----
        for href, attrs in p.links:
            if href is None:
                continue
            if href.startswith("mailto:") or href.startswith("tel:"):
                report["contact_links"] += 1
                continue
            if href.startswith("#"):
                report["anchor_links"] += 1
                continue
            if href.startswith("http://") or href.startswith("https://"):
                report["external_links"] += 1
                # affiliate checks
                if href in OP_SET:
                    report["affiliate_counts"][href] += 1
                    rel_attr = attrs.get("rel", "")
                    tgt = attrs.get("target", "")
                    if "sponsored" not in rel_attr or "nofollow" not in rel_attr or "noopener" not in rel_attr:
                        report["affiliate_bad_attrs"].append((rel, href, "rel=" + rel_attr))
                    if tgt != "_blank":
                        report["affiliate_bad_attrs"].append((rel, href, "target=" + tgt))
                continue
            # internal
            report["all_internal_links"] += 1
            if href.startswith("http://"):
                report["https_internal"].append((rel, href))
            if ".html" in href:
                report["html_ext_in_href"].append((rel, href))
            ok, target = target_exists(href, pp)
            if not ok:
                report["broken_links"].append((rel, href, target))

        # ---- images ----
        for im in p.imgs:
            src = im.get("src", "")
            if not src:
                continue
            # resolve
            if src.startswith("http"):
                exists = True
            else:
                if src.startswith("/"):
                    local = src[1:]
                else:
                    local = os.path.normpath(os.path.join(os.path.dirname(pp), src)).replace("\\","/")
                local = urllib.parse.unquote(local)
                exists = os.path.isfile(os.path.join(PUB, local))
            if not exists:
                report["broken_images"].append((rel, src))
            alt = im.get("alt", None)
            if alt is None or alt.strip() == "":
                report["missing_alt"].append((rel, src))
            if "width" not in im or "height" not in im:
                report["missing_dims"].append((rel, src))
            # lazy check: non-hero images
            is_hero = (im.get("fetchpriority") == "high") or ("/hero/" in src)
            if not is_hero and im.get("loading") != "lazy":
                report["missing_lazy"].append((rel, src, im.get("loading")))

        # ---- JSON-LD ----
        for block in p.ld_blocks:
            report["jsonld_total"] += 1
            try:
                data = json.loads(block)
                types = data.get("@type")
                if isinstance(types, str):
                    types = [types]
                for t in types:
                    report["jsonld_types"][rel].add(t)
            except Exception as e:
                report["jsonld_invalid"].append((rel, str(e)[:120], block[:120]))

        # FAQ mismatch
        if "FAQPage" in report["jsonld_types"][rel]:
            # count questions
            qcount = 0
            for block in p.ld_blocks:
                try:
                    data = json.loads(block)
                    if data.get("@type") == "FAQPage":
                        qcount = len(data.get("mainEntity", []))
                except Exception:
                    pass
            if qcount != p.faq_details and p.faq_details > 0:
                report["faq_mismatch"].append((rel, qcount, p.faq_details))

        # ---- mojibake (only html files here) ----
        for m in MOJI_CHECK:
            if m in raw:
                report["mojibake_files"].append((rel, m))
                break

        # ---- games ----
        if p.game_grid:
            report["game_pages"].append((rel, p.game_cards))
        if rel == "index.html":
            report["home_game_cards"] = p.game_cards

        # ---- inline figures on pillars ----
        if p.inline_figures > 0:
            for k in PILLAR_INLINE:
                if k in rel:
                    inline_found[k] += p.inline_figures
        if p.product_grid:
            report["product_grid_pages"] += 1

        # ---- perf ----
        report["other_scripts"] += p.other_scripts
        report["inline_styles"] += p.style_blocks
        # external fonts
        for href, attrs in p.links:
            pass
        # count font preconnect/stylesheets
        if re.search(r'<link[^>]+href=["\']https?://[^"\']*fonts', raw, re.I):
            report["external_fonts"] += 1

        entry["h1_count"] = len(p.h1s)
        entry["has_product_grid"] = p.product_grid
        entry["has_game_grid"] = p.game_grid
        entry["game_cards"] = p.game_cards
        entry["inline_figures"] = p.inline_figures
        report["pages"].append(entry)

    report["inline_found"] = inline_found
    # short pages
    sp = sorted(report["pages"], key=lambda x: x["words"])
    report["shortest5"] = [(x["file"], x["words"]) for x in sp[:5]]
    report["under600"] = [(x["file"], x["words"]) for x in report["pages"] if x["words"] < 600]

    # ---- mojibake across ALL files in public ----
    all_moji = []
    for dp, dn, fn in os.walk(PUB):
        for f in fn:
            full = os.path.join(dp, f)
            try:
                with open(full, "r", encoding="utf-8") as fh:
                    txt = fh.read()
            except Exception:
                continue
            for m in MOJI_CHECK:
                if m in txt:
                    all_moji.append((relpath(full), m))
                    break
    report["mojibake_all_files"] = all_moji

    print(json.dumps(report, indent=2, default=str, ensure_ascii=False))

if __name__ == "__main__":
    main()
