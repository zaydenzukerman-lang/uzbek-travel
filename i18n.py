#!/usr/bin/env python3
"""Translation layer for the generated English site.
  python3 i18n.py extract   -> i18n/en_segments.json  (every translatable text unit, keyed by hash)
  python3 i18n.py build     -> writes /ru/... and /es/... from i18n/ru.json + i18n/es.json,
                               and wires the EN | RU | ES switcher + hreflang on every page.
Run AFTER build.py (build.py regenerates the English pages)."""
import os, re, sys, json, glob, hashlib, html as _html
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://uzgbektravel.com"
LANGS = ["ru", "es"]
BLOCK = {"p","li","h1","h2","h3","h4","dt","dd","summary","label","option","button","title","div","td","th"}
INLINE_UNIT = {"a","span","b","strong","em"}
ATTRS = ["alt", "placeholder", "title", "aria-label"]
LETTERS = re.compile(r"[A-Za-z]")
key = lambda s: hashlib.sha1(s.strip().encode()).hexdigest()[:12]

def en_pages():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(f), ROOT)
        rel = "" if rel == "." else rel + "/"
        if rel.split("/")[0] in LANGS or rel.startswith("_"): continue
        out.append((rel, f))
    return out

def skip(el):
    return any(p.name in ("script", "style", "svg") or {"lang", "fbrand", "brand"} & set(p.get("class") or []) for p in [el, *el.parents] if p.name)

def units(soup):
    """Deterministic list of elements whose inner HTML is one translatable segment."""
    leaves = [el for el in soup.find_all(BLOCK) if not el.find(BLOCK) and not skip(el) and LETTERS.search(el.get_text())]
    inside = set()
    for el in leaves:
        inside.add(id(el)); inside.update(id(d) for d in el.descendants)
    extra = []
    for t in soup.find_all(string=True):
        if id(t) in inside or isinstance(t, (Comment, Doctype)) or not LETTERS.search(t): continue
        par = t.parent
        if par is None or skip(par) or id(par) in inside: continue
        if par.name in INLINE_UNIT:
            extra.append(par); inside.add(id(par)); inside.update(id(d) for d in par.descendants)
    return leaves + extra

def attr_targets(soup):
    out = []
    for el in soup.find_all(True):
        if skip(el): continue
        for a in ATTRS:
            v = el.get(a)
            if v and LETTERS.search(v) and "@" not in v: out.append((el, a))
    for m in soup.find_all("meta"):
        if m.get("name") == "description" or m.get("property") in ("og:title", "og:description", "og:image:alt"):
            out.append((m, "content"))
    return out

def extract():
    segs = {}
    for rel, f in en_pages():
        soup = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        for el in units(soup):
            h = el.decode_contents().strip(); segs.setdefault(key(h), h)
        for el, a in attr_targets(soup):
            v = el[a].strip(); segs.setdefault(key(v), v)
    os.makedirs(os.path.join(ROOT, "i18n"), exist_ok=True)
    json.dump(segs, open(os.path.join(ROOT, "i18n/en_segments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(segs)} unique segments, {sum(len(v) for v in segs.values()):,} chars -> i18n/en_segments.json")

def switcher(soup, rel, lang):
    """Rebuild the header + footer language switchers as real links to the same page in each language."""
    depth = rel.count("/") + (0 if lang == "en" else 1)
    up = "../" * depth
    href = {"en": up + rel, "ru": up + "ru/" + rel, "es": up + "es/" + rel}
    for box in soup.select("div.lang"):
        box.clear()
        for L in ["en", "ru", "es"]:
            a = soup.new_tag("a", href=href[L]); a.string = L.upper()
            if L == lang: a["class"] = "on"; a["aria-current"] = "true"
            a["hreflang"] = L; box.append(a)
    for p in soup.select("footer .foot-grid > div:first-child p"):
        if "EN" in p.get_text() and "RU" in p.get_text():
            p.clear()
            for i, L in enumerate(["en", "ru", "es"]):
                if i: p.append(NavigableString(" | "))
                a = soup.new_tag("a", href=href[L]); a.string = L.upper()
                if L == lang: a["style"] = "color:#fff;font-weight:700"
                p.append(a)
    head = soup.head
    LOC = {"en": "en_US", "ru": "ru_RU", "es": "es_ES"}
    for m in head.find_all("meta", property=["og:locale", "og:locale:alternate"]): m.decompose()
    ogt = head.find("meta", property="og:site_name") or head.find("meta", property="og:url")
    tags = [soup.new_tag("meta", property="og:locale", content=LOC[lang])] + \
           [soup.new_tag("meta", property="og:locale:alternate", content=LOC[x]) for x in LOC if x != lang]
    for t in reversed(tags): ogt.insert_after(t)
    for old in head.select('link[rel="alternate"]'): old.decompose()
    for L in ["en", "ru", "es"]:
        head.append(soup.new_tag("link", rel="alternate", hreflang=L, href=f"{SITE}/{'' if L=='en' else L+'/'}{rel}"))
    head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=f"{SITE}/{rel}"))

AGENCY_ID = SITE + "/#agency"
def localize_ld(node, L, tr, missing):
    """Translate schema.org strings via the same segment dictionary, and point page URLs at the /ru/ or /es/ version."""
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in ("@context", "@type", "@id", "email", "sameAs", "logo", "image", "priceCurrency", "knowsLanguage", "addressCountry"):
                out[k] = v
            elif k == "inLanguage": out[k] = L
            else: out[k] = localize_ld(v, L, tr, missing)
        return out
    if isinstance(node, list): return [localize_ld(x, L, tr, missing) for x in node]
    if isinstance(node, str):
        if node.startswith(SITE + "/") and "/assets/" not in node and node != AGENCY_ID:
            return SITE + "/" + L + node[len(SITE):]
        if not LETTERS.search(node) or node.startswith("http"): return node
        for cand in (node, _html.escape(node, quote=False)):
            k = key(cand)
            if k in tr: return _html.unescape(re.sub(r"<[^>]+>", "", tr[k])).strip()
        missing.add("ld:" + node[:40]); return node
    return node

def build():
    tr = {L: json.load(open(os.path.join(ROOT, f"i18n/{L}.json"), encoding="utf-8")) for L in LANGS}
    missing = {L: set() for L in LANGS}
    for rel, f in en_pages():
        src = open(f, encoding="utf-8").read()
        soup = BeautifulSoup(src, "html.parser"); switcher(soup, rel, "en")
        open(f, "w", encoding="utf-8").write(str(soup))            # EN gets real switcher + hreflang
        for L in LANGS:
            s = BeautifulSoup(src, "html.parser")
            for el in units(s):
                k = key(el.decode_contents())
                if k in tr[L]:
                    el.clear()
                    for node in list(BeautifulSoup(tr[L][k], "html.parser").contents): el.append(node)
                else: missing[L].add(k)
            for el, a in attr_targets(s):
                hit = next((tr[L][key(c)] for c in (el[a], _html.escape(el[a], quote=False)) if key(c) in tr[L]), None)
                if hit is not None: el[a] = _html.unescape(re.sub(r"<[^>]+>", "", hit)).strip()
                else: missing[L].add(key(el[a]))
            s.html["lang"] = L
            for el in s.find_all(True):                               # assets live one level up from /ru/ and /es/
                for a in ("src", "href"):
                    v = el.get(a)
                    if v and "assets/" in v and not v.startswith(("http", "/", "mailto")): el[a] = "../" + v
                if el.get("style") and "assets/" in el["style"]:
                    el["style"] = re.sub(r"url\('(?!http|/)", "url('../", el["style"])
            can = s.find("link", rel="canonical")
            if can: can["href"] = f"{SITE}/{L}/{rel}"
            for m in s.find_all("meta", property="og:url"): m["content"] = f"{SITE}/{L}/{rel}"
            for sc in s.find_all("script", type="application/ld+json"):
                data = json.loads(sc.string)
                sc.string = json.dumps(localize_ld(data, L, tr[L], missing[L]), ensure_ascii=False).replace("</", "<\\/")
            switcher(s, rel, L)
            out = os.path.join(ROOT, L, rel, "index.html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(str(s))
    sitemap()
    for L in LANGS: print(f"{L}: built, {len(missing[L])} untranslated segments" + (f" e.g. {sorted(missing[L])[:5]}" if missing[L] else ""))

def sitemap():
    rels=[r for r,_ in en_pages()]
    alts=lambda r: "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{"" if l=="en" else l+"/"}{r}"/>' for l in ["en","ru","es"]) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{r}"/>'
    urls="".join(f"  <url><loc>{SITE}/{p}{r}</loc>{alts(r)}</url>\n" for p in ["","ru/","es/"] for r in rels)
    open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+urls+"</urlset>\n")
    print(f"sitemap: {len(rels)*3} urls")

if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()
