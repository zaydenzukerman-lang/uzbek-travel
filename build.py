#!/usr/bin/env python3
"""Uzbek Travel static site generator. Run: python3 build.py  -> writes all pages into this folder.
Content comes from the client's Website Design & Content Blueprint (Sep 2026)."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://uzgbektravel.com"
EMAIL = "info.uzbektravelguide@gmail.com"
VK = "https://vk.ru/id822026476"
TG = "https://t.me/AhunjanovMahmut"
TRIP_TOURS = "https://clubok.travel/tours/4482"
TRIP_GUIDE = "https://clubok.travel/guides/2870"
e = html.escape

# ---- footer contact icons (brand marks from Simple Icons; Instagram has no link yet by request) ----
import re as _re
def _brand(name):
    svg = open(os.path.join(ROOT, "assets/img/icons", name + ".svg")).read()
    return _re.sub(r"<title>.*?</title>", "", svg).replace('<svg ', '<svg width="21" height="21" fill="currentColor" aria-hidden="true" ')
_MAIL = '<svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>'
_STAR = '<svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-.9z"/></svg>'
SOCIAL = ('<div class="social">'
  f'<a href="mailto:{EMAIL}" aria-label="Email us" title="Email: {EMAIL}">{_MAIL}</a>'
  f'<a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram" title="Telegram: @AhunjanovMahmut">{_brand("telegram")}</a>'
  f'<a href="{VK}" target="_blank" rel="noopener" aria-label="VK" title="VK">{_brand("vk")}</a>'
  f'<span class="soon" role="img" aria-label="Instagram (coming soon)" title="Instagram — coming soon">{_brand("instagram")}</span>'
  f'<a href="{TRIP_TOURS}" target="_blank" rel="noopener" aria-label="Reviews on Tripster" title="Our reviews on Tripster">{_STAR}</a>'
  '</div>')

LOGO = """<svg viewBox="0 0 64 48" aria-hidden="true"><ellipse cx="32" cy="24" rx="30" ry="22" fill="#1a5f6e"/>
<ellipse cx="32" cy="24" rx="25" ry="18" fill="none" stroke="#2ecfb8" stroke-width="2"/>
<g fill="#f5a623">%s</g><circle cx="32" cy="24" r="7" fill="#e8503a"/><circle cx="32" cy="24" r="3.2" fill="#fafaf5"/></svg>""" % "".join(
    f'<ellipse cx="32" cy="12" rx="3" ry="7" transform="rotate({a} 32 24)"/>' for a in range(0, 360, 45))

ICON = {
 "compass": '<svg width="58" height="58" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M16.2 7.8l-2.1 6.3-6.3 2.1 2.1-6.3z"/></svg>',
 "people": '<svg width="58" height="58" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5"/><circle cx="17" cy="9" r="2.8"/><path d="M16 13.6c3 .3 5.5 2.8 5.5 6"/></svg>',
 "star": '<svg width="58" height="58" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-.9z"/></svg>',
}

NAV = [("Home", ""), ("Tours", "tours/"), ("Destinations", "destinations/"), ("Our Guides", "guides/"),
       ("About Us", "about/"), ("Contact & Book", "contact/")]

import hashlib as _h
VER = _h.md5((open(os.path.join(ROOT,"assets/css/style.css"),"rb").read()+open(os.path.join(ROOT,"assets/js/main.js"),"rb").read())).hexdigest()[:8]  # cache-buster: changes whenever CSS/JS change

def page(path, title, desc, body, active=""):
    depth = path.count("/")               # "" -> 0, "tours/" -> 1, "tours/parkent/" -> 2
    r = "../" * depth
    navhtml = "".join(f'<a href="{r}{h}"{" class=\"active\"" if n == active else ""}>{n}</a>' for n, h in NAV)
    head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/{path}"><meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/assets/img/pool/px-samarkand1.jpg"><meta property="og:url" content="{SITE}/{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/img/favicon.png" type="image/png"><link rel="apple-touch-icon" href="{r}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css?v={VER}"></head><body>
<header class="site-head"><div class="lang-bar"><div class="wrap"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg><div class="lang" aria-label="Language"><a class="on" href="{r}">EN</a><span>RU</span><span>ES</span></div></div></div><div class="wrap nav">
 <a class="brand" href="{r}"><img src="{r}assets/img/logo.png" alt="Uzbek Travel logo" width="38" height="46"><span>Uzbek Travel</span></a>
 <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke-width="2.2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
 <nav class="nav-links">{navhtml}</nav>
 <div class="nav-right"><div class="lang"><a class="on" href="{r}">EN</a><span title="Russian version coming soon">RU</span><span title="Spanish version coming soon">ES</span></div>
 <a class="btn btn-orange" href="{r}contact/" style="padding:10px 20px">Book Now</a></div>
</div></header>"""
    foot = f"""<footer class="foot"><div class="wrap foot-grid">
 <div><div class="fbrand"><img src="{r}assets/img/logo.png" alt="" width="36" height="44">Uzbek Travel</div><p>uzgbektravel.com<br>Tashkent, Uzbekistan</p>
 <p style="margin-top:14px"><b style="color:#fff">EN</b> &nbsp;|&nbsp; RU &nbsp;|&nbsp; ES</p></div>
 <div><h4>Quick Links</h4><ul>{"".join(f'<li><a href="{r}{h}">{n}</a></li>' for n, h in NAV)}</ul></div>
 <div><h4>Our Tours</h4><ul>
  <li><a href="{r}tours/parkent/">Parkent: Golden Sun &amp; Wine Stories</a></li>
  <li><a href="{r}tours/bostanlyk/">Bostanlyk: Mountains &amp; Ancient Legends</a></li>
  <li><a href="{r}tours/tashkent-bukhara/">Tashkent to Bukhara</a></li>
  <li><a href="{r}tours/custom/">Custom &amp; Private Tours</a></li></ul></div>
 <div><h4>Contact</h4>{SOCIAL}</div>
</div><div class="foot-bottom">&copy; 2026 Uzbek Travel. All rights reserved.</div></footer>
<script src="{r}assets/js/main.js?v={VER}"></script></body></html>"""
    out = os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(head + body.replace("{R}", r) + foot)
    print("wrote", "/" + path)

def img(n):  # ints = client's own photos (zero-padded), strings = Pexels landmark shots ("registan3" -> px-registan3.jpg)
    return "{R}assets/img/pool/%s.jpg" % (("%02d" % n) if isinstance(n, int) else "px-" + n)

def hero(title, sub, pic, pos="center"):
    return f'<section class="page-hero" style="background-image:url(\'{img(pic)}\');background-position:{pos}"><div class="wrap"><h1>{title}</h1><p>{sub}</p></div></section>'

def tour_card(slug, title, meta, desc, pic, cat=""):
    return f"""<a class="card" href="{{R}}tours/{slug}/" data-cat="{cat}"><div class="card-img" style="background-image:url('{img(pic)}')"></div>
<div class="card-body"><div class="meta">{meta}</div><h3>{title}</h3><p>{desc}</p><span class="card-link">See Full Tour &rarr;</span></div></a>"""

def tile(slug, name, line, pic, big=False):
    return f"""<a class="tile{' big' if big else ''}" href="{{R}}destinations/{slug}/"><div class="tbg" style="background-image:url('{img(pic)}')"></div>
<div class="tin"><h3>{name}</h3><span>{line}</span></div></a>"""

def facts(rows):
    return '<div class="factbox"><dl>' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl></div>"

def gallery(pics, alt):
    return '<div class="gallery">' + "".join(f'<img src="{img(p)}" alt="{e(alt)}" loading="lazy">' for p in pics) + "</div>"

def stops(items):
    return '<ol class="stops">' + "".join(f"<li><h4>{t}</h4><p>{d}</p></li>" for t, d in items) + "</ol>"

def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def cta_band(title="Ready to Plan Your Trip?", text="Tell us when you are coming, what you are interested in, and how many people are in your group. We will get back to you within 24 hours.", btn="Plan My Trip", q=""):
    return f"""<section class="section band"><div class="wrap"><h2>{title}</h2><p>{text}</p>
<a class="btn btn-orange" href="{{R}}contact/{q}">{btn}</a></div></section>"""

GUIDES = [
 ("mahmud", "Mahmud", "Founder &amp; Guide", "Born and raised in Tashkent. Food, culture and the great Silk Road cities.", "img", "#1a5f6e"),
 ("sarvinoz", "Sarvinoz", "Guide", "Samarkand, Bukhara, Kokand — every stone has a story.", "S", "#e8503a"),
 ("konstantin", "Konstantin", "Guide", "Historic corridors, artisan workshops and hidden backstreets.", "K", "#f5a623"),
 ("elena", "Elena", "Mountain Guide", "Ski instructor and guide to the Western Tian Shan.", "E", "#2ecfb8"),
]
def avatar(g, size_cls="avatar"):
    slug, name, _, _, kind, color = g
    if kind == "img":
        return f'<img class="{size_cls}" src="{{R}}assets/img/guides/mahmut.jpg" alt="{name}, guide at Uzbek Travel">'
    return f'<img class="{size_cls}" src="{{R}}assets/img/guides/{slug}.svg" alt="{name}, guide at Uzbek Travel">'

# v2: real portraits for all four guides (from client's "Guides profiles" doc, Sep 2026)
GUIDES = [
 ("mahmud", "Mahmud", "Founder &amp; Guide", "21 years guiding. Born and raised in Tashkent — food, culture and the Silk Road cities.", "mahmut", ""),
 ("sarvinoz", "Sarvinoz", "Guide", "From Tashkent to Samarkand, Bukhara, Kokand and the Tian Shan.", "sarvinoz", ""),
 ("konstantin", "Konstantin", "Guide", "Classic Silk Road routes — and the hidden corners off the beaten path.", "konstantin", ""),
 ("elena", "Elena", "Mountain Guide &amp; Ski Instructor", "Snowy passes, forested slopes and canyons of the Western Tian Shan.", "elena", ""),
]
def avatar(g, size_cls="avatar"):
    return f'<img class="{size_cls}" src="{{R}}assets/img/guides/{g[4]}.jpg" alt="{g[1]}, {g[2].replace("&amp;","&")} at Uzbek Travel" loading="lazy">'

TOUR_OPTIONS = [("parkent", "Parkent: Golden Sun &amp; Wine Stories (7 hours, from €104 / $119)"),
                ("bostanlyk", "Bostanlyk: Mountains &amp; Ancient Legends (9 hours, from $66 / €58 per person)"),
                ("tashkent-bukhara", "Tashkent to Bukhara: Multi-Day Tour (price on request)"),
                ("custom", "Custom / Private Tour (price on request)")]

# ---------------------------------------------------------------- AMERICAN-AUDIENCE LAYER
# Most U.S. travelers have never considered Uzbekistan -> sell the country (why / safe / easy / cost) before the tours.
CHK = '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10"/></svg>'
TRUST = '<div class="trust"><div class="wrap">' + "".join(f"<span>{CHK}{t}</span>" for t in [
    "Visa-free for U.S. citizens (up to 30 days)", "Safe &amp; famously welcoming", "English-speaking local guides", "Rated 5★ on Tripster (12 reviews)", "We reply within 24 hours"]) + "</div></div>"
WHY = [
 ("2,500+","Years of Silk Road history","Samarkand is roughly as old as Rome. For centuries, caravans carried silk, spices and ideas between China and Europe through these very cities."),
 ("4","UNESCO World Heritage cities","Samarkand, Bukhara, Khiva and Shakhrisabz are living cities you walk through — not ruins behind a rope."),
 ("30","Days visa-free for Americans","No visa application for U.S. citizens on stays up to 30 days. Just book your flight and go."),
 ("<$10","For a great local meal","Your dollar goes a long way here. Private guided days often cost less than a group bus tour in Western Europe."),
 ("Few","Tour-bus crowds (for now)","This is what Italy felt like before mass tourism. Tiled courtyards and mountain viewpoints, almost to yourself."),
 ("2","Worlds in one trip","Blue-domed Silk Road cities one day, snowy Tian Shan peaks, waterfalls and vineyards the next — all near Tashkent."),
]
FAQ = [
 ("Is Uzbekistan safe for American travelers?","Yes. Travelers are consistently surprised by how safe and relaxed it feels — street crime is low and hospitality is a point of national pride. As with any trip, check the current U.S. State Department travel advisory before you go, and your guide is with you throughout."),
 ("Do I need a visa?","U.S. citizens can visit Uzbekistan visa-free for up to 30 days. You just need a passport valid for your stay. Rules can change, so confirm the current requirements before you fly — we are happy to help."),
 ("Where exactly is Uzbekistan, and how do I get there?","Uzbekistan is in Central Asia, on the ancient Silk Road between China and Europe, bordered by Kazakhstan, Kyrgyzstan, Tajikistan, Afghanistan and Turkmenistan. From the U.S. you typically fly with one stop — via Istanbul, Dubai or a European hub — into Tashkent. We pick you up at the airport."),
 ("Is it a Muslim country? What should I wear?","Uzbekistan is Muslim-majority but secular and very open to visitors. Everyday casual clothing is fine. When visiting mosques and holy sites, cover shoulders and knees (women may want a light scarf). Your guide will tell you before each stop."),
 ("Will people speak English?","In hotels and main tourist areas, often yes — elsewhere, less so. That is exactly why a local guide makes such a difference. All of our guides speak English, and several also speak Russian and Spanish."),
 ("What about money — can I use my card?","The local currency is the som. Cards work in most hotels and many restaurants in the big cities, and ATMs are easy to find, but bazaars and small villages are cash only. U.S. dollars are easy to exchange."),
 ("When is the best time to visit?","Spring (April to June) and autumn (September to October) are ideal — warm days, cool evenings, and everything in bloom or harvest. Summer is hot in the cities but perfect in the mountains. Winter brings skiing in the Tian Shan."),
 ("Can you customize a tour for my group or family?","Absolutely. Every tour can be private, and we build custom itineraries around your interests, dates and pace. Tell us what you want and we will send a plan and a price within 24 hours."),
]
def faq_block(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"

# ---------------------------------------------------------------- HOME
home = f"""
<section class="hero"><div class="hero-bg" style="background-image:url('{img("samarkand1")}')"></div>
<div class="wrap hero-in"><div class="eyebrow" style="color:#f5a623">Uzbek Travel · Tashkent</div>
<h1>Discover the Real Uzbekistan</h1><p>Private and group tours led by local guides who love what they do.</p>
<div class="hero-ctas"><a class="btn btn-orange" href="{{R}}tours/">Explore Our Tours</a><a class="btn btn-ghost" href="{{R}}guides/">Meet Our Guides</a></div></div></section>
{TRUST}

<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">The best trip you haven't heard of</div><h2>Why Uzbekistan?</h2>
<p class="lead">It is the heart of the ancient Silk Road — and still one of the world's great undiscovered destinations. Here is why travelers who go can't stop talking about it.</p></div>
<div class="why">{"".join(f'<div class="why-item"><div class="num">{n}</div><h3>{h}</h3><p>{p}</p></div>' for n,h,p in WHY)}</div></div></section>

<section class="section tint"><div class="wrap feature-row">
 <div class="feature"><div class="ic">{ICON['compass']}</div><h3>Local Expertise</h3><p>Born and raised here. We know every corner.</p></div>
 <div class="feature"><div class="ic">{ICON['people']}</div><h3>Personal Guides</h3><p>Small groups, real connections, no rushing.</p></div>
 <div class="feature"><div class="ic">{ICON['star']}</div><h3>Authentic Experiences</h3><p>Beyond the monuments. Into the culture.</p></div>
</div></section>

<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">Handpicked routes</div><h2>Our Tours</h2></div>
<div class="cards" style="margin-top:34px">
{tour_card("parkent","Parkent — Golden Sun &amp; Wine Stories","7 hours · Private · From €104 / $119","A day in the mountains: a solar research complex, a sacred mosque at 1,500m, wine tasting, and a proper mountain lunch.",26)}
{tour_card("bostanlyk","Bostanlyk — Mountains &amp; Ancient Legends","9 hours · Group · From $66 / €58 pp","Ancient petroglyphs, a cable car, waterfalls, Zoroastrian burial sites, and lunch at a traditional teahouse by the reservoir.",24)}
{tour_card("tashkent-bukhara","Tashkent to Bukhara — The Full Uzbekistan","Multi-day · Private · Price on request","Tashkent, Samarkand, and Bukhara with a professional guide, comfortable transport, and curated restaurants and stays.","registan3")}
</div><div class="center" style="margin-top:34px"><a class="btn btn-outline" href="{{R}}tours/">View All Tours Including Custom &amp; Private</a></div></div></section>

<section class="section tint"><div class="wrap"><div class="center"><div class="eyebrow">Destinations</div><h2>Where We Take You</h2>
<p class="lead">From the ancient Silk Road cities to the wild peaks of the Tian Shan — Uzbekistan has more than you expect.</p></div>
<div class="tiles" style="margin-top:34px">
{tile("samarkand","Samarkand","The crown jewel of the Silk Road","registan3",True)}
{tile("tashkent","Tashkent","The capital where history meets modern life","tashkent2")}
{tile("bukhara","Bukhara","A living medieval city","bukhara3")}
{tile("kokand","Kokand &amp; Fergana Valley","Silk, ceramics, and craftsmanship","ceramics0")}
{tile("tian-shan","Tian Shan","Wild mountains, waterfalls, and open sky",22)}
</div></div></section>

<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">Our team</div><h2>The People Behind Your Journey</h2>
<p class="lead">We are a small team of experienced local guides based in Tashkent. We speak English, Russian, and Spanish, and we care deeply about giving every visitor a genuine experience of Uzbekistan.</p></div>
<div class="team-row" style="margin-top:36px">{"".join(f'<div>{avatar(g)}<h3>{g[1]}</h3><div class="role">{g[2]}</div><p>{g[3]}</p></div>' for g in GUIDES)}</div>
<div class="center" style="margin-top:30px"><a class="btn btn-teal" href="{{R}}guides/">Meet the Full Team</a></div></div></section>

<section class="section tint"><div class="wrap split">
 <div><div class="eyebrow">Getting oriented</div><h2>Where Is Uzbekistan?</h2>
 <p class="lead">In the heart of Central Asia, on the Silk Road between China and Europe — and easier to reach than you'd think.</p>
 <ul class="checks">
  <li><b>One stop from the U.S.</b> — fly via Istanbul, Dubai or a European hub into Tashkent</li>
  <li><b>Visa-free</b> for U.S. citizens for up to 30 days</li>
  <li><b>9–10 hours ahead</b> of New York time</li>
  <li><b>Airport pickup included</b> on multi-day tours — your guide meets you at arrivals</li>
  <li><b>Fast trains</b> connect Tashkent, Samarkand and Bukhara in about 2 hours each</li></ul>
 <p style="margin-top:22px"><a class="btn btn-orange" href="{{R}}contact/">Ask Us Anything</a></p></div>
 <img src="{img(21)}" alt="Charvak Reservoir and the Tian Shan mountains near Tashkent" loading="lazy">
</div></section>

<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">Planning your first trip</div><h2>Questions Americans Ask Us</h2></div>
{faq_block(FAQ)}</div></section>
{cta_band()}
"""
page("", "Uzbek Travel — Discover the Real Uzbekistan",
     "Private and group tours across Uzbekistan led by local guides. Tashkent, Samarkand, Bukhara, Tian Shan and beyond. English, Russian and Spanish.", home, "Home")

# ---------------------------------------------------------------- TOURS OVERVIEW
tours = hero("Our Tours", "From half-day excursions near Tashkent to multi-day journeys through the ancient Silk Road cities.", 24) + f"""
<section class="section"><div class="wrap"><div class="prose center" style="max-width:720px;margin-bottom:34px">
<p class="lead" style="margin:0 auto 1rem">We offer a range of tours across Uzbekistan. Every tour is led by one of our local guides and can be arranged as a private or group experience.</p>
<p>Not sure which tour is right for you? <a href="{{R}}contact/">Contact us</a> and we will design a custom itinerary around your interests, your schedule, and your group.</p></div>
<div class="filters">
 <button class="active" data-filter="all">All Tours</button><button data-filter="nature">Nature &amp; Mountains</button>
 <button data-filter="culture">Culture &amp; History</button><button data-filter="food">Food &amp; Wine</button>
 <button data-filter="multiday">Multi-Day</button><button data-filter="custom">Custom &amp; Private</button></div>
<div class="cards">
{tour_card("parkent","Parkent — Golden Sun &amp; Wine Stories","7 hours · Private · From €104 / $119","A solar furnace, a sacred mosque at 1,500m, a family winery, and a proper mountain lunch.",26,"nature food")}
{tour_card("bostanlyk","Bostanlyk — Mountains &amp; Ancient Legends","9 hours · Group · From $66 / €58 pp","8,000-year-old petroglyphs, a cable car, Charvak Reservoir and the Nanay waterfalls.",24,"nature culture")}
{tour_card("tashkent-bukhara","Tashkent to Bukhara — The Full Uzbekistan","5–7 days · Private · Price on request","The classic Silk Road journey through three extraordinary cities, with one guide throughout.","registan3","culture multiday")}
{tour_card("custom","Custom &amp; Private Tours","Any length · Private · Quote in 24h","Food days, photography, wine routes, ceramics, skiing — built around what you love.",20,"custom food nature culture")}
</div></div></section>{cta_band()}"""
page("tours/", "Tours in Uzbekistan — Private & Group | Uzbek Travel",
     "Mountain, wine, culture and multi-day Silk Road tours across Uzbekistan, led by local guides from Tashkent.", tours, "Tours")

# ---------------------------------------------------------------- TOUR: PARKENT
BOOK = "22% prepayment, remainder on the day. Free cancellation up to 48 hours before."
parkent = hero("Parkent — Golden Sun &amp; Wine Stories", "Uzbekistan has its own little France out here — and most visitors have no idea it exists.", 26) + f"""
<section class="section"><div class="wrap prose">
{facts([("Location","Tashkent Region, Parkent District"),("Duration","7 hours"),("Format","Private tour — 1 to 10 people"),
 ("Transport","Sedan (1–4 people) or minibus (up to 10), air-conditioned"),("Price","€104 / $119 for 1–3 people · €30 / $34 per person for 4–10 people"),
 ("Children","Welcome"),("Languages","English, Russian, Spanish"),("Booking",BOOK)])}
<p class="form-note" style="margin-top:-8px">Dollar prices are approximate (€1 ≈ $1.15); the exact amount follows the exchange rate on the day.</p>
<h2>What This Tour Is</h2>
<p>A full-day car and walking tour into the mountains of Parkent, one of the most underrated corners of the Tashkent region. This tour combines a unique scientific landmark, a sacred high-altitude mosque, local winemaking, and a proper mountain lunch into one memorable day.</p>
{gallery([34,7,8],"Parkent tour — mountains, lunch and viewpoints")}
<h2>The Route</h2>
{stops([
 ("Solar Furnace “Sun” Complex · 1–1.5 hours","One of only two solar furnace complexes in the world — the other is in southern France. A giant parabolic mirror focuses the sun to a single blazing point. Your guide explains the science and the history of the institute."),
 ("Ali Buva High-Mountain Mosque · 2 hours","At 1,500 meters above sea level, this sacred mosque is as much about the journey as the destination — calm, beautiful, with panoramic views of the mountains and valleys. Hear the legend of Ali Buva."),
 ("CRUCHON Winery, Zarkent · 1 hour incl. tasting","A family winery producing wines by traditional methods. Tour the production area and taste several varieties paired with local cheese — a genuine surprise for most visitors."),
 ("Ulfatlar Cafe, Sukok · 1–1.5 hours","Lunch at a beloved mountain cafe: shashlik (grilled meat skewers) and mastava (a rich meat and rice soup). Simple, delicious, completely authentic."),
 ("Champagne Parkent Vineyards · 30 minutes","Yes, this place is actually called Champagne. A walk through the vines, views of the foothills, and a chance to buy a bottle to take home.")])}
<h2>What You Will Learn</h2>{ul(["The history and science of the Solar Institute","The legend of Ali Buva and the Islamic history of the region","The winemaking traditions of Parkent and the Chirchik Valley","Local mountain food culture and the story of these villages"])}
<h2>Who This Tour Is For</h2>{ul(["Nature lovers and those who enjoy scenic mountain landscapes","Food and wine travelers — this tour has serious gastronomic content","Cultural explorers who want to go beyond the standard Tashkent itinerary","Families and small groups"])}
<h2>What to Bring</h2>{ul(["Warm layers — mountain weather can change quickly, especially spring and autumn","Comfortable walking shoes with grip — some paths are uneven","Water and sunscreen","Cash for any personal purchases"])}
<p class="form-note">Child seats available on request. First aid kit always in the vehicle. Altitude sickness remedies recommended for sensitive travelers.</p>
<h2>Meeting Point</h2><p>Agreed directly with your guide. You can discuss the exact pickup point after submitting your booking inquiry.</p>
</div></section>{cta_band("Book the Parkent Tour","From €104 / $119 for up to 3 people. Tell us your date and group size and we will confirm within 24 hours.","Book This Tour","?tour=parkent")}"""
page("tours/parkent/", "Parkent Tour — Golden Sun & Wine Stories | Uzbek Travel",
     "7-hour private tour from Tashkent: the Solar Furnace, Ali Buva mountain mosque, CRUCHON winery tasting and a mountain lunch. From €104.", parkent, "Tours")

# ---------------------------------------------------------------- TOUR: BOSTANLYK
bost = hero("Bostanlyk — Mountains, Nature &amp; Ancient Legends", "Touch 8,000-year-old rock carvings, ride a cable car over the valleys, and end the day at a waterfall.", 24) + f"""
<section class="section"><div class="wrap prose">
{facts([("Location","Bostanlyk District, Tashkent Region"),("Duration","9 hours"),("Format","Group tour — up to 16 people · Private option available"),
 ("Transport","Bus (included for groups up to 16)"),("Price","$66 / €58 per person (group) · $150–170 / €131–148 (private)"),("Children","Welcome"),
 ("Languages","English, Russian, Spanish"),("Extra costs","Lunch paid separately · Cable car approx. $9 / €8 per person"),("Booking",BOOK)])}
<h2>What This Tour Is</h2>
<p>A full-day journey into the Bostanlyk district, the wild and beautiful corner of the Tashkent region where the Tian Shan mountains begin. This tour connects ancient history, dramatic nature, and genuine Uzbek culture in a way that no city tour can match.</p>
{gallery([25,19,9],"Bostanlyk tour — waterfall, petroglyphs and Charvak Reservoir")}
<h2>The Route</h2>
{stops([
 ("Chakh Cham Village: Private Museum &amp; Mountain Herbs","A museum built by a local enthusiast out of love for the region. A herbalist shows you mountain plants used in folk medicine and lets you taste herbal teas."),
 ("Chinorkent Cable Car","An ascent with panoramic views over the Bostanlyk valley and mountain ridges — one of the best bird's-eye views in the Tashkent region."),
 ("Lunch at Sazanchik Teahouse","A traditional teahouse on the edge of the Charvak Reservoir. Lunch in a yurt or open pavilion with views over the water. (Lunch is paid separately.)"),
 ("Mesolithic Petroglyphs &amp; Ancient Plane Trees","Rock carvings over 8,000 years old depicting hunting scenes, rituals and daily life — among plane trees that have stood here for up to 850 years."),
 ("Charvak Reservoir Viewpoint","One of the best viewpoints over one of the largest artificial lakes in Uzbekistan. Outstanding for photography."),
 ("Ali Baba Grotto &amp; Guri Mug Cemetery","A natural grotto tied to local Ali Baba legends, beside a Zoroastrian burial ground that predates Islam in the region."),
 ("Pskem River Viewpoint &amp; Nanay Village","A glacial torrent of turquoise and white — a classic mountain landscape and a moment of calm."),
 ("Nanay Waterfalls","The stop guests remember most: a waterfall in a lush gorge, reached by a short walk or a ride in a Soviet-era UAZ jeep. Swim in summer.")])}
{gallery([31,22,12],"Grotto, Pskem river and waterfall")}
<h2>What You Will Learn</h2>{ul(["The history and culture of the Bostanlyk mountain communities","Traditional herbal medicine of the Tian Shan region","Mesolithic civilization and the meaning of petroglyphs","Zoroastrian culture and its legacy in Uzbekistan","The ecology of the Charvak Reservoir and Pskem River system","Uzbek teahouse culture and cuisine"])}
<h2>Who This Tour Is For</h2>{ul(["History and archaeology enthusiasts","Nature lovers and active travelers","Families with children — the cable car and waterfall are especially popular","Anyone who wants to leave the city and see a completely different Uzbekistan"])}
<h2>What to Bring</h2>{ul(["Comfortable walking shoes or light hiking boots","Layers — mornings can be cool in the mountains","Swimwear if visiting in summer","Cash for lunch and cable car","Camera"])}
<h2>Meeting Point</h2><p>Hotel pickup. Exact details confirmed after prepayment.</p>
</div></section>{cta_band("Book the Bostanlyk Tour","From $66 / €58 per person. Tell us your date and group size and we will confirm within 24 hours.","Book This Tour","?tour=bostanlyk")}"""
page("tours/bostanlyk/", "Bostanlyk Tour — Mountains, Petroglyphs & Waterfalls | Uzbek Travel",
     "9-hour tour into the Tian Shan foothills: 8,000-year-old petroglyphs, Chinorkent cable car, Charvak Reservoir and the Nanay waterfalls. From $66.", bost, "Tours")

# ---------------------------------------------------------------- TOUR: TASHKENT-BUKHARA
tb = hero("Tashkent to Bukhara — The Full Uzbekistan", "The classic Uzbekistan journey, done the right way.", "registan3") + f"""
<section class="section"><div class="wrap prose">
{facts([("Destinations","Tashkent, Samarkand, Bukhara"),("Duration","Multi-day (customizable — typically 5 to 7 days)"),("Format","Private tour"),
 ("Transport","Comfortable minivan + high-speed Afrosiab train between cities"),("Price","Available on request — contact us for a custom quote"),
 ("Children","Welcome"),("Languages","English, Russian, Spanish")])}
<h2>What This Tour Is</h2>
<p>Three cities, each completely different from the others, connected by the story of the Silk Road and the centuries of civilization that made this region one of the most culturally rich on earth.</p>
<p>This is a private tour. Your guide travels with you from Tashkent through Samarkand and on to Bukhara, giving you continuity, personal service, and the kind of insider knowledge you simply cannot get from a public tour group.</p>
<h2>Tashkent — Days 1 &amp; 2</h2>
{ul(["<b>Hazrati Imam Complex (Khast Imam)</b> — the spiritual heart of Tashkent, home to one of the oldest Qurans in the world","<b>Kukeldash Madrasah</b> — a 16th century theological school still active today","<b>Chorsu Bazaar</b> — the great domed market where Tashkent comes alive","<b>Mustaqillik Square</b> — independence square and the Soviet-era cityscape","<b>Navoi Opera and Ballet Theater</b> — a landmark of Soviet-era orientalist architecture","<b>Ankhor Embankment</b> — the canal-side promenade for evening walks"])}
<p><b>Where we eat:</b> Besh Kazan Plov Center (plov in giant cauldrons over open fire) · Ulfatlar · Navrutz Teahouse.</p>
<h2>Samarkand — Days 3 &amp; 4</h2>
{ul(["<b>Registan Square</b> — three madrasahs facing each other, covered in tile and mosaic","<b>Gur-Emir Mausoleum</b> — resting place of Timur (Tamerlane)","<b>Shah-i-Zinda Necropolis</b> — a street of mausoleums in the most intense shades of blue tile","<b>Bibi-Khanym Mosque</b> — once the largest mosque in the Islamic world","<b>Siab Bazaar</b> — spices, dried fruit and local bread"])}
<div class="quote">“Every stone in Samarkand is like a page from an ancient book.” — Sarvinoz, guide</div>
<p><b>Where we stay:</b> Guesthouse Musavvir — rated 9.5, in the old city, 10 minutes' walk to Registan, filled with antiques from the Imperial through the Soviet era.</p>
{gallery(["samarkand2","bukhara3",2],"Silk Road architecture of Samarkand and Bukhara")}
<h2>Bukhara — Days 5 &amp; 6</h2>
{ul(["<b>The Ark Fortress</b> — the ancient citadel, standing for over 1,500 years","<b>Kalon Minaret &amp; Mosque</b> — the minaret even Genghis Khan reportedly refused to destroy","<b>Lyabi-Hauz Ensemble</b> — a pool surrounded by mulberry trees, madrasahs and a caravanserai","<b>Chor Minor</b> — the four-towered gateway madrasah","<b>Trading Domes</b> — the ancient covered bazaars"])}
<p><b>Where we stay:</b> in the old city, so you can walk the mahallas at night when it feels medieval again — K. Khorezm Plaza and Orient Star are both good choices.</p>
<h2>Transport Between Cities</h2>
<p>Tashkent to Samarkand by Afrosiab high-speed train (about 2–2.5 hours), Samarkand to Bukhara by high-speed train (about 2.5 hours). Your guide books the tickets as part of the tour.</p>
<h2>What Is Included</h2>{ul(["All ground transport within cities in an air-conditioned minivan","Train tickets between cities (economy class)","Professional guide throughout the full journey","All museum and monument entrance fees","Airport pickup and drop-off in Tashkent","Bottled water in the vehicle","24/7 guide support"])}
<h2>What Is Not Included</h2>{ul(["International flights to and from Tashkent","Hotel accommodation (we recommend and help you book)","Lunches and dinners (we take you to the best places — you pay on the day)","Personal shopping and souvenirs","Travel insurance (strongly recommended)","Tips for guides and drivers"])}
<h2>Souvenirs — What to Buy and Where</h2>
<p><b>Ceramics:</b> the blue ceramics of Rishtan — cobalt glazes on red clay, patterns unchanged since the 9th century.<br>
<b>Textiles:</b> suzani embroidery, ikat silk and handwoven carpets — best in Samarkand and Bukhara; vintage pieces at Tashkent's Yangiabad Bazaar.<br>
<b>Knives:</b> handmade pchak knives from Kokand and Chust.<br>
<b>Spices &amp; dried fruit:</b> Chorsu Bazaar and Siab Bazaar — saffron, dried apricots, pistachios and walnuts.</p>
<p class="form-note">Antique items and archaeological artifacts require government export permits. Always buy from registered shops.</p>
</div></section>{cta_band("Get Your Custom Quote","Tell us your dates and group size and we will send a day-by-day plan and price within 24 hours.","Request a Quote","?tour=tashkent-bukhara")}"""
page("tours/tashkent-bukhara/", "Tashkent to Bukhara Private Tour — Samarkand & the Silk Road | Uzbek Travel",
     "5–7 day private tour through Tashkent, Samarkand and Bukhara with one guide throughout, Afrosiab trains, entrance fees and airport transfers included.", tb, "Tours")

# ---------------------------------------------------------------- TOUR: CUSTOM
custom = hero("Custom &amp; Private Tours", "Tell us what you are curious about. We will design a tour that fits.", 20) + f"""
<section class="section"><div class="wrap prose">
<h2>What Is a Custom Tour</h2>
<p>Not every journey fits a standard package. If you have specific interests, a different group size, limited time, or you simply want something designed around you — we will build it.</p>
<h2>Custom Tours We Have Done</h2>{ul(["A food-focused day in Tashkent — markets, cooking, and a family meal","A photography tour of Bukhara at sunrise and sunset","A wine route through the Chirchik Valley vineyards","A full day in Kokand and Rishtan focusing on ceramics","A skiing and snowshoeing day in Chimgan in winter","A family trip combining Magic City park with the old city for kids"])}
{gallery([8,35,16],"Custom tour ideas — food, skiing and mountains")}
<h2>Pricing</h2><p>Custom and private tours are priced individually based on duration, number of guests, transport required, and any special inclusions. Contact us with your details and we will send a quote within 24 hours.</p>
<h2>How to Book</h2><p>Fill out the booking form on our <a href="{{R}}contact/?tour=custom">Contact page</a>. Select “Custom / Private Tour” and describe what you have in mind in the message field. We will reply within 24 hours.</p>
</div></section>{cta_band("Design My Tour","Share your interests and dates — we will come back with an itinerary and a price within 24 hours.","Start Planning","?tour=custom")}"""
page("tours/custom/", "Custom & Private Tours in Uzbekistan | Uzbek Travel",
     "Private tours built around you — food, wine, photography, ceramics, skiing and family trips across Uzbekistan. Quote within 24 hours.", custom, "Tours")

# ---------------------------------------------------------------- DESTINATIONS
DEST = [
 ("tashkent","Tashkent &amp; Tashkent Region","The capital where history meets modern life","tashkent2",["tashkent1","tashkent3",11],
  """<p>Tashkent is Uzbekistan's capital and its largest city — a place where Islamic architecture, Soviet-era boulevards, and a genuinely modern city all exist side by side. Most visitors treat it as a transit stop. That is a mistake.</p>
<p>The old city around Khast Imam contains one of the oldest Qurans in the world. The Chorsu Bazaar is one of the great markets of Central Asia. And the city has some of the best food in the country.</p>
<h2>Key Sites</h2>""" + ul(["Hazrati Imam Complex (Khast Imam) — the religious center of Uzbekistan","Kukeldash Madrasah — 16th century, still in use","Chorsu Bazaar — the great covered market","Mustaqillik Square — Soviet-scale public space","Navoi Opera and Ballet Theater","Magic City and Dream Park — for families"]) +
  """<h2>Tashkent Region — Beyond the City</h2><p>Within an hour of Tashkent, the landscape changes completely. The Bostanlyk district is where the Tian Shan mountains begin. The Chirchik Valley has vineyards producing wines that will genuinely surprise you. Parkent has a solar furnace, mountain mosques, and a place called Champagne.</p>""" +
  ul(["Charvak Reservoir — the mountain lake an hour from the city","Chimgan and Amirsoy — skiing in winter, trekking in summer","Chirchik Valley wineries — CRUCHON, MSA Family Winery, Uzumfermer","Parkent — the Solar Furnace complex and Ali Buva mosque"])),
 ("samarkand","Samarkand","The crown jewel of the Silk Road","registan3",["samarkand2","registan0","samarkand3"],
  """<p>Samarkand is the city that travelers come to Uzbekistan for. It was the center of Timur's empire in the 14th century, and the monuments he built here are still among the most extraordinary architectural achievements anywhere on earth.</p>
<div class="quote">“Every stone in Samarkand is like a page from an ancient book.” — Sarvinoz</div><h2>Key Sites</h2>""" +
  ul(["Registan Square — three madrasahs facing each other across a vast tiled courtyard. The single most impressive sight in Uzbekistan.","Gur-Emir Mausoleum — Timur's tomb, under a fluted turquoise dome","Shah-i-Zinda — a necropolis of blue-tiled mausoleums on the edge of the old city","Bibi-Khanym Mosque — once the largest mosque in the Islamic world","Siab Bazaar — spices, bread, dried fruit, and the everyday life of the city","Afrosiab Museum — the archaeological site and museum of ancient Samarkand"])),
 ("bukhara","Bukhara","A living medieval city","bukhara3",["bukhara1","bukhara0",10],
  """<p>If Samarkand is about grandeur, Bukhara is about atmosphere. The old city is a labyrinth of mud-brick lanes, carved wooden doors, ancient caravanserais, and domed trading bazaars. Time moves differently here.</p>
<p>At its peak Bukhara had over 100 madrasahs and was known as the “City of Scholars.” Walking its streets at night, when the tourists have gone, is one of the most memorable experiences Uzbekistan offers.</p><h2>Key Sites</h2>""" +
  ul(["The Ark Fortress — the ancient citadel, inhabited for over 1,500 years","Kalon Minaret — the great tower that even Genghis Khan reportedly spared","Kalon Mosque — one of the largest in Central Asia","Lyabi-Hauz — the pool and square at the heart of the old city","Chor Minor — the four-towered madrasah hidden in the residential quarter","Trading Domes — the covered bazaars of the Silk Road","Zindan Prison Museum — where foreign hostages were held in the 19th century"])),
 ("kokand","Kokand &amp; the Fergana Valley","Silk, ceramics, and craftsmanship","ceramics0",["ceramics1","ceramics2",15],
  """<p>The Fergana Valley is the most densely populated part of Uzbekistan and one of the most culturally rich. This is where the famous crafts come from — the blue ceramics of Rishtan, the ikat silk of Margilan, the knives of Kokand and Chust.</p>
<p>Kokand was an important khanate until the Russian conquest in 1875. Its palaces and mosques speak of a sophisticated royal culture — and because it is less visited than Samarkand or Bukhara, you see it more honestly.</p><h2>Key Sites</h2>""" +
  ul(["Khudoyar Khan Palace — the last great palace of the Kokand Khanate","Rishtan ceramic workshops — master potters using thousand-year-old techniques","Margilan silk factory — ikat woven on traditional looms","Kokand bazaar — a real working market, not a tourist market"])),
 ("tian-shan","Tian Shan Mountains","Wild mountains, waterfalls, and open sky",22,[21,37,25],
  """<p>The western end of the Tian Shan range rises directly behind Tashkent. Within an hour you can be at 2,000 meters, surrounded by peaks, glacial rivers, and air that feels like it comes from another world.</p>
<p>In winter this is ski country. In summer it is for trekking, waterfalls, and complete escape from the heat of the cities. Elena, our mountain guide and ski instructor, knows every trail.</p><h2>Key Sites &amp; Activities</h2>""" +
  ul(["Chimgan — the main mountain resort area, 80km from Tashkent","Amirsoy Ski Resort — the best ski infrastructure in Uzbekistan","Charvak Reservoir — the turquoise glacial lake in the mountains","Nanay Waterfalls — accessible by jeep, spectacular in spring","Beldersay — a quieter alternative to Chimgan for trekking","Pskem River Valley — wild and barely visited"])),
]
dest = hero("Where We Take You", "Uzbekistan is not just one destination. It is a collection of completely different worlds.", 21) + f"""
<section class="section"><div class="wrap"><p class="lead center" style="margin:0 auto 36px">Ancient Silk Road cities, wild mountain landscapes, quiet valleys full of craftsmen, and a capital that surprises everyone who visits. Here is a guide to the places we know best.</p>
<div class="tiles">{"".join(tile(s,n,l,p, i==1) for i,(s,n,l,p,_,_) in enumerate(DEST))}</div></div></section>{cta_band()}"""
page("destinations/", "Destinations in Uzbekistan — Samarkand, Bukhara, Tashkent & Tian Shan | Uzbek Travel",
     "A local guide's view of Tashkent, Samarkand, Bukhara, Kokand and the Fergana Valley, and the Tian Shan mountains.", dest, "Destinations")
for slug, name, line, pic, gal, text in DEST:
    body = hero(name, line, pic) + f'<section class="section"><div class="wrap prose">{text}{gallery(gal, name)}</div></section>' + cta_band(
        f"Explore {name.split(' &amp;')[0]} With Us", "Tell us what you want to see and we will plan the day around you.", "Plan My Trip")
    plain = name.replace("&amp;", "&")
    page(f"destinations/{slug}/", f"{plain} — Travel Guide | Uzbek Travel", f"{plain}: {line}. What to see and how to experience it with a local guide from Uzbek Travel.", body, "Destinations")

# ---------------------------------------------------------------- GUIDES
PROFILES = {
 "mahmud": ("English, Russian, Uzbek", "Tashkent, Samarkand, Bukhara, multi-day tours, food and culture", """<p><b>Welcome to Uzbekistan.</b></p>
<p>I'm Mahmud, though most visitors just call me Mikhail. Born and raised in Tashkent, I've spent my whole life exploring what makes this country so remarkable: its layered history, stunning architecture, wild landscapes, and food that will genuinely surprise you.</p>
<p>I became a guide because I couldn't stop talking about this place. Every street in Samarkand, every dish in a family kitchen, every crumbling caravanserai has a story worth telling, and I've made it my business to know them all.</p>
<p>What I care most about is making sure you leave with something real. Not just photos, but a feeling for the place. So whether we're wandering a bazaar or sitting down to a proper plov, I'll make sure you understand what you're seeing and why it matters.</p><p><b>Let's get started.</b></p>"""),
 "sarvinoz": ("Russian, English, Spanish", "Tashkent, Samarkand, Bukhara, Kokand, Tian Shan region", """<p>Sarvinoz is a charismatic and deeply knowledgeable guide whose name has become well-known among travelers to Uzbekistan. She brings together an expert understanding of the region's culture and history with a genuine enthusiasm for sharing it.</p>
<p>“Tashkent is not just a city, it is a kaleidoscope of times and cultures,” she says, and she means it. Her tours move between the ancient and the contemporary with the ease of someone who has lived in both worlds.</p>
<p>In Samarkand she passes Registan Square and says: “Every stone here is like a page from an ancient book.” In Bukhara she takes guests through caravanserais connected to trade routes stretching to China. In Kokand she finds the residents who still remember the khanate era through family stories.</p>
<p>Every tour with Sarvinoz is more than a guided walk. It is a chance to become part of something greater.</p>"""),
 "konstantin": ("English, Uzbek, Russian", "Tashkent, Samarkand, Bukhara, Parkent, Kokand, Rishtan", """<p>Konstantin is a seasoned guide with deep expertise across Uzbekistan's most important historic corridors as well as the artisanal centers of Parkent, Kokand, and Rishtan. A native of Uzbekistan, he brings an unrivaled command of the region's history and culture to every tour.</p>
<p>His approach is individual. He takes time to understand what each guest is genuinely curious about, then builds the tour around that — as comfortable revealing hidden backstreets and family workshops as he is explaining the genius of Timur's court architects.</p>
<p>For Konstantin, guiding is not about delivering information. It is about creating the atmosphere of a genuine journey where every guest feels like a participant in the local culture, not just an observer.</p>
<p>He is warm, approachable, and easy to talk to — a guide who becomes a friend.</p>"""),
 "elena": ("Russian, English", "Tian Shan mountains, skiing, mountain trekking, Western Tian Shan", """<p>Elena is a professional mountain guide and ski instructor from Tashkent. The mountains are not just her workplace. They are her life.</p>
<p>She has spent years learning the routes, the weather patterns, the hidden valleys, and the stories of the Western Tian Shan — leading travelers through snowy passes, forested slopes, glacial rivers, and gorges that feel like they belong to another century.</p>
<div class="quote">“Today will be more than just a descent. We are here to feel these mountains.”</div>
<p>Whether working with complete beginners or experienced mountaineers, Elena teaches not just technique but confidence. “Skiing is not just a sport. It is a way to experience real freedom.”</p>
<p>With Elena, the Tian Shan is not a backdrop. It is the whole story.</p>"""),
}
# v2: guide bios from the client's "Guides profiles" doc (replace blueprint versions)
PROFILES["mahmud"] = ("English, Russian, Uzbek", "Tashkent, Samarkand, Bukhara, multi-day tours, food and culture · 21 years in tourism · rated 5★ on Tripster", PROFILES["mahmud"][2])
PROFILES["sarvinoz"] = ("Russian, English, Spanish", "Tashkent, Samarkand, Bukhara, Kokand, Tian Shan &amp; Tashkent region", """
<p>Sarvinoz is a young and charismatic guide whose name has become synonymous with unique travel experiences across Uzbekistan. Her expertise stretches from historic Tashkent to the majestic cities of Samarkand and Bukhara, from enchanting Kokand to the mysterious heights of the Tian Shan mountains. She effortlessly blends a deep knowledge of the region's culture and history with a genuine passion for sharing that richness with every traveler.</p>
<p>Sarvinoz begins every tour at the very heart of the capital, in Khast Imam Square, where she shares the city's thousand-year history — a place where Islamic architecture, Soviet heritage, and contemporary buildings stand side by side.</p>
<div class="quote">“Tashkent is not just a city, it is a kaleidoscope of times and cultures.”</div>
<p>In Samarkand she conveys the city's one-of-a-kind atmosphere as she passes the legendary Registan Square: “Every stone in Samarkand is like a page from an ancient book.” In Bukhara, the team's senior guides share stories of ancient caravanserais once connected to the Great Silk Road, and Kokand shows off its historic palaces and rich past as a center of cultural and commercial exchange.</p>
<p>When the journey leads to the Tian Shan, the tours become true adventures among breathtaking peaks — full of stories of local traditions and the deep connection between people and nature. In the valleys and green hills of the Tashkent region, she introduces guests to craftsmen keeping ancestral skills alive.</p>
<p>Every tour with Sarvinoz is more than a guided walk — it is a chance to become part of something greater.</p>""")
PROFILES["konstantin"] = ("English, Uzbek, Russian", "Tashkent, Samarkand, Bukhara · artisan hubs of Parkent, Kokand &amp; Rishtan", """
<p>Konstantin is a seasoned guide with an extensive reach across Uzbekistan, specializing in the historic corridors of Tashkent, Samarkand, and Bukhara, as well as the artisanal hubs of Parkent, Kokand, and Rishtan. A native of Uzbekistan, he has an unrivaled command of the region's history and culture. His tours are not merely sightseeing excursions but deeply immersive narratives that blend architectural expertise with firsthand cultural insight.</p>
<p>Konstantin is known for his intuitive approach, tailoring each itinerary to the specific curiosities of his guests. He has mastered the classic routes, but he takes real pride in revealing the hidden gems and quiet corners of the country that remain off the beaten path.</p>
<p>For Konstantin, guiding is an art form. He creates a journey where history is felt, not just heard — turning every traveler from an observer into a participant in the local culture.</p>""")
PROFILES["elena"] = ("Russian, English", "Western Tian Shan · mountain trekking · skiing &amp; ski instruction", """
<p>Elena is a professional mountain guide and ski instructor originally from Tashkent. Her life is a continuous adventure of majestic peaks and exhilarating descents, and she is eager to share the raw beauty of the Western Tian Shan with anyone ready to discover it.</p>
<p>From the early morning hours, as the first rays of sun touch the snow-capped summits, Elena is already on the move — leading travelers along some of the most scenic routes in the region: snowy passes, forested slopes, and the mysterious canyons of the Western Tian Shan. She knows this terrain intimately, and whether she is with seasoned adventurers or complete beginners, she is dedicated to making every day unforgettable.</p>
<div class="quote">“Today will be more than just a descent. We are here to learn to feel these mountains, and to understand how they breathe.”</div>
<p>Elena works closely with other guides, instructors, and local residents so that every guest feels safe and inspired, and she is always there through the most technical sections. On the slopes she becomes an instructor, explaining with ease how to balance, read the terrain, and enjoy the thrill of speed. “Skiing is not merely a sport, it is a way to experience true freedom,” she says. “It is essential not to fear, but to trust yourself.”</p>
<p>Along the way she shares stories of local mountain traditions and peaks that have guarded their secrets for millennia. With Elena, the mountains are not just routes on a map — they are stories you will want to live again and again.</p>""")

gbody = hero("The People Who Make the Difference", "A tour is only as good as the person leading it.", 20) + '<section class="section"><div class="wrap">' + \
 '<p class="lead center" style="margin:0 auto 40px">Our guides are not employees reading from a script. They are local experts who have spent years learning every layer of this country — its history, its architecture, its food, its stories — because they genuinely love it. Meet the team.</p>'
for g in GUIDES:
    langs, spec, bio = PROFILES[g[0]]
    gbody += f"""<div class="card" id="{g[0]}" style="flex-direction:row;gap:30px;padding:30px;margin-bottom:26px;align-items:flex-start;flex-wrap:wrap">
<div style="flex:0 0 180px;text-align:center">{avatar(g)}</div>
<div style="flex:1;min-width:260px"><div class="eyebrow">{g[2]}</div><h2 style="margin-bottom:.3em">{g[1]}</h2>
<p class="form-note" style="margin:0 0 14px"><b>Languages:</b> {langs}<br><b>Specialties:</b> {spec}</p>{bio}</div></div>"""
gbody += "</div></section>" + cta_band("Travel With One of Our Guides", "Tell us who you would like to travel with and what you want to see.", "Plan My Trip")
page("guides/", "Our Guides — Local Experts in Uzbekistan | Uzbek Travel",
     "Meet Mahmud, Sarvinoz, Konstantin and Elena — licensed local guides for Tashkent, Samarkand, Bukhara, Kokand and the Tian Shan.", gbody, "Our Guides")

# ---------------------------------------------------------------- ABOUT
about = hero("We Are Uzbek Travel", "Tourism is not our job. It is our way of life.", 1, "center 42%") + f"""
<section class="section"><div class="wrap prose">
<p class="lead">We are a team of local guides based in Tashkent, Uzbekistan. We have spent years learning the history, the architecture, the food, the stories, and the hidden corners of this extraordinary country so that we can share all of it with you.</p>
<p>Our routes are not standard excursions. They are carefully designed journeys that take you into the culture, the nature, and the history of Uzbekistan in a way that leaves you with something real. Not just photographs, but a genuine feeling for the place.</p>
<h2>Our Story</h2>
<p>Uzbek Travel grew out of a simple belief: that the best way to experience a country is through the eyes of someone who truly loves it. Our founder Mahmud began guiding visitors through Tashkent because he simply could not stop talking about the city he grew up in. That same passion brought together our team of guides, each one an expert in their own corner of Uzbekistan.</p>
<div class="gallery tall"><img src="{{R}}assets/img/pool/mahmut-coat.jpg" alt="Mahmud in a traditional chapan" loading="lazy"><img src="{img(6)}" alt="Mahmud with guests in Tashkent" loading="lazy"><img src="{{R}}assets/img/pool/mahmut-expo.jpg" alt="Mahmud representing Uzbek Travel at a travel expo" loading="lazy"></div>
<p>Today we lead private tours, group excursions, mountain adventures, wine and food experiences, and multi-day journeys from Tashkent all the way to Bukhara. Every tour is led by a licensed, experienced guide who speaks your language and knows this place inside out.</p>
<h2>What Makes Us Different</h2>{ul(["We are local. Born and raised here, not imported guides.","We keep groups small so every guest gets real attention.","We go off the standard route to show you places most tourists never find.","We speak English, Russian, and Spanish.","We handle the logistics so you can focus on the experience.","We are honest about what to expect — no surprises, no pressure."])}
<h2>Our Mission</h2><div class="quote">“To show every visitor the Uzbekistan that locals know and love — its layered history, its stunning landscapes, its extraordinary food, and above all, its people.”</div>
<h2>Listed On</h2><p>You can also find and review our tours on Tripster and Sputnik, two of the leading travel platforms for independent travelers in the region.</p>
<p><a class="btn btn-outline" href="{TRIP_TOURS}" target="_blank" rel="noopener">Our tours on Tripster</a> &nbsp; <a class="btn btn-outline" href="{TRIP_GUIDE}" target="_blank" rel="noopener">Guide profile</a></p>
</div></section>{cta_band()}"""
page("about/", "About Uzbek Travel — Local Guides From Tashkent",
     "Uzbek Travel is a small team of local guides from Tashkent leading private, group, mountain, wine and multi-day tours across Uzbekistan.", about, "About Us")

# ---------------------------------------------------------------- CONTACT
contact = hero("Plan Your Trip", "No obligation. No pressure. Just a conversation about how to make your time in Uzbekistan as good as it can be.", 24) + f"""
<section class="section"><div class="wrap">
<p class="lead center" style="margin:0 auto 34px">Tell us about your trip and we will get back to you within 24 hours with a plan, a price, and any questions we have.</p>
<form class="form" id="booking-form" action="https://formsubmit.co/ajax/{EMAIL}" method="POST">
 <div class="success" id="form-success">Thank you! We have received your enquiry and will reply to your email within 24 hours. We look forward to showing you Uzbekistan.</div>
 <input type="hidden" name="_subject" value="New tour enquiry — uzgbektravel.com"><input type="hidden" name="_template" value="table">
 <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
 <div class="row"><label for="f-name">Full Name *</label><input id="f-name" name="name" required></div>
 <div class="two"><div class="row"><label for="f-email">Email Address *</label><input id="f-email" type="email" name="email" required></div>
  <div class="row"><label for="f-country">Country You Are Traveling From *</label><input id="f-country" name="country" required></div></div>
 <div class="two"><div class="row"><label for="f-lang">Preferred Language *</label><select id="f-lang" name="language" required><option>English</option><option>Russian</option><option>Spanish</option></select></div>
  <div class="row"><label for="f-n">Number of Travelers *</label><input id="f-n" type="number" name="travelers" min="1" value="2" required></div></div>
 <div class="two"><div class="row"><label for="f-a">Arrival Date *</label><input id="f-a" type="date" name="arrival" required></div>
  <div class="row"><label for="f-d">Departure Date *</label><input id="f-d" type="date" name="departure" required></div></div>
 <div class="row"><label for="f-tour">Tour *</label><select id="f-tour" name="tour" required>{"".join(f'<option value="{v}">{t}</option>' for v,t in TOUR_OPTIONS)}</select></div>
 <div class="row"><label for="f-msg">Message / Special Requests</label><textarea id="f-msg" name="message" rows="5" placeholder="Tell us anything that would help us plan the perfect tour for you. Interests, mobility requirements, dietary needs, things you definitely want to see..."></textarea></div>
 <button class="btn btn-orange" type="submit" style="width:100%;justify-content:center">Send My Enquiry</button>
 <p class="form-note">We reply to all enquiries within 24 hours. During busy periods it may be slightly longer, but we will always get back to you.</p>
</form>
<div class="prose" style="margin-top:50px">
<h2>Direct Contact</h2><p>Prefer to write directly? Email us at <a href="mailto:{EMAIL}"><b>{EMAIL}</b></a> or message Mahmud on <a href="{TG}" target="_blank" rel="noopener">Telegram (@AhunjanovMahmut)</a>.</p>
<h3>Find Us On</h3><p><a href="{VK}" target="_blank" rel="noopener">VK</a> · <a href="{TRIP_TOURS}" target="_blank" rel="noopener">Tripster</a></p>
<h3>Common Questions</h3>{faq_block(FAQ[:4])}
<h3>Booking Conditions</h3>{ul(["A 22% prepayment is required to confirm your booking","The remaining balance is paid on the day of the tour","Free cancellation up to 48 hours before the tour start time","We accept cards from Russian and international banks via Tripster","For direct bookings, payment details will be provided in our reply"])}
</div></div></section>"""
page("contact/", "Contact & Book — Plan Your Uzbekistan Trip | Uzbek Travel",
     "Send us your dates, group size and interests and we will reply within 24 hours with a plan and a price. No obligation.", contact, "Contact & Book")

# ---------------------------------------------------------------- assets: logo, monogram avatars, sitemap, robots
open(os.path.join(ROOT, "assets/img/logo.svg"), "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
for slug, name, _, _, kind, color in []:  # letter avatars retired v2 (real photos now)
    if kind != "img":
        open(os.path.join(ROOT, f"assets/img/guides/{slug}.svg"), "w").write(
f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{color}"/>
<circle cx="100" cy="100" r="78" fill="none" stroke="#fafaf5" stroke-opacity=".35" stroke-width="3"/>
<text x="100" y="128" text-anchor="middle" font-family="Georgia,serif" font-size="86" font-weight="700" fill="#fafaf5">{name[0]}</text></svg>""")
paths = [""] + ["tours/", "tours/parkent/", "tours/bostanlyk/", "tours/tashkent-bukhara/", "tours/custom/", "destinations/"] + \
        [f"destinations/{d[0]}/" for d in DEST] + ["guides/", "about/", "contact/"]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}/{p}</loc></url>\n" for p in paths) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print(f"done: {len(paths)} pages + sitemap + robots")
