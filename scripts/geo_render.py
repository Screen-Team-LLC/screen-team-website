#!/usr/bin/env python3
"""HTML render helpers for Screen Team geo / city SEO pages."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-NDQ7PTQM');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NDQ7PTQM"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

CLARITY = """  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "x61prei2pi");
  </script>"""


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def faq_html(prefix: str, faqs: list[tuple[str, str]]) -> str:
    items = []
    for i, (q, a) in enumerate(faqs, 1):
        items.append(
            f'''          <div class="faq-item">
            <button class="faq-question" aria-expanded="false" aria-controls="{prefix}-faq-{i}">{q} <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg></button>
            <div class="faq-answer" id="{prefix}-faq-{i}" aria-hidden="true" inert><div class="faq-answer-inner"><p>{a}</p></div></div>
          </div>'''
        )
    return "\n".join(items)


def faq_schema(faqs: list[tuple[str, str]]) -> str:
    parts = []
    for q, a in faqs:
        qj = html.escape(strip_tags(q), quote=True)
        aj = html.escape(strip_tags(a), quote=True)
        parts.append(
            f'{{"@type":"Question","name":"{qj}","acceptedAnswer":{{"@type":"Answer","text":"{aj}"}}}}'
        )
    return ",".join(parts)


def paras(blocks: list[str]) -> str:
    return "\n".join(f"          <p>{p}</p>" for p in blocks)


def list_items(items: list[tuple[str, str]], linked: bool = False) -> str:
    out = []
    for name, desc in items:
        out.append(f"            <li>{name} — {desc}</li>")
    return "\n".join(out)


def nearby_links(links: list[tuple[str, str]]) -> str:
    bits = [f'<a href="{slug}">{label}</a>' for slug, label in links]
    return " · ".join(bits)


def render_city(c: dict) -> str:
    slug = c["slug"]
    prefix = slug.replace("-screen-repair", "").replace("-county", "")
    url = f"https://screenteamllc.com/{slug}.html"
    city = c["city"]
    county = c["county"]
    county_link = c["county_link"]

    hero_panels = "\n".join(
        f'        <div class="hero-panel hero-panel--{"left" if i==0 else "top" if i==1 else "bottom" if i==2 else "right"} hero-panel--photo"><img src="{src}" alt="{alt}" width="800" height="600" decoding="async"></div>'
        for i, (src, alt) in enumerate(c["hero_imgs"])
    )
    neighborhoods = list_items(c["neighborhoods"])
    gallery = "\n".join(
        f'''        <figure>
          <img src="{src}" alt="{cap}" width="800" height="600" loading="lazy" decoding="async">
          <figcaption>{cap}</figcaption>
        </figure>'''
        for src, cap in c["gallery"]
    )
    scheduling = "\n".join(
        f"            <li>{title} — {desc}</li>" for title, desc in c["scheduling"]
    )
    services = "\n".join(f"            <li>{item}</li>" for item in c["services"])
    process = c.get(
        "process",
        [
            (
                "1. Photos + city",
                f"Text wide and close-up shots of the {city} cage or lanai — Chris ballparks many jobs before driving.",
            ),
            (
                "2. Frame & gutter check",
                "On site he inspects posts, doors, and any super gutter / header drainage issues before mesh goes up.",
            ),
            (
                "3. Rescreen or repair",
                "Failed panels or full-cage mesh, proper spline tension, cleanup — most residential jobs finish in a day.",
            ),
        ],
    )
    process_cards = "\n".join(
        f'''          <div class="sp-process-card">
            <h3>{t}</h3>
            <p>{d}</p>
          </div>'''
        for t, d in process
    )

    area_served_type = c.get("area_type", "City")
    breadcrumb_name = city

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{GTM_HEAD}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c["title"]}</title>
  <meta name="description" content="{c["meta_desc"]}">
  <meta name="keywords" content="{c["keywords"]}">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary">
  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI crawler summary">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="https://screenteamllc.com/sitemap.xml">
  <meta name="theme-color" content="#3da8d8">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="{city}, Florida">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="The Screen Team LLC">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{c["title"]}">
  <meta property="og:description" content="{c["meta_desc"]}">
  <meta property="og:image" content="https://screenteamllc.com/{c["og_img"]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{c["title"]}">
  <meta name="twitter:description" content="{c["meta_desc"]}">
  <meta name="twitter:image" content="https://screenteamllc.com/{c["og_img"]}">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Service","@id":"{url}#service","name":"Screen Repair {city} FL","description":"{strip_tags(c.get("schema_desc", f"Pool cage rescreens, lanai screen repair, super gutters, and enclosure work in {city}, Florida."))}","provider":{{"@id":"https://screenteamllc.com/#business"}},"areaServed":{{"@type":"{area_served_type}","name":"{city}, FL"}},"url":"{url}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema(c["faq"])}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","@id":"{url}#breadcrumb","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://screenteamllc.com/"}},{{"@type":"ListItem","position":2,"name":"Service Areas","item":"https://screenteamllc.com/service-areas.html"}},{{"@type":"ListItem","position":3,"name":"{breadcrumb_name}","item":"{url}"}}]}}
  </script>
  <link rel="stylesheet" href="styles.css">
{CLARITY}
</head>
<body>
{GTM_BODY}
  <a class="skip-nav" href="#main-content">Skip to main content</a>
  <div id="site-header-include"></div>

  <main id="main-content">
    <section class="sp-hero sp-hero--panels hero" aria-label="{city} screen repair">
      <div class="hero-panels" aria-hidden="true">
{hero_panels}
      </div>
      <div class="sp-hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <p class="breadcrumb-trail"><a href="/">Home</a> &rsaquo; <a href="service-areas.html">Service Areas</a> &rsaquo; {city}</p>
        <h1>{c["h1"]}</h1>
        <p>{c["hero_lead"]}</p>
      </div>
    </section>

    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content" data-reveal>
          <h2>{c["intro_title"]}</h2>
{paras(c["intro"])}
          <p>Call <a href="tel:7273866562">(727) 386-6562</a> or see our <a href="{county_link}">{county} County hub</a> for regional routing.</p>

          <h2>{c["neighborhoods_title"]}</h2>
          <ul class="about-list">
{neighborhoods}
          </ul>

          <div class="city-local-note">{c["local_note"]}</div>

          <h2>{c["priority_title"]}</h2>
{paras(c["priority"])}

          <h2>{c["conditions_title"]}</h2>
{paras(c["conditions"])}

          <h2>Screen &amp; gutter services in {city}</h2>
          <ul class="about-list">
{services}
          </ul>
          <p><a href="pricing.html">Pricing</a> · <a href="gallery.html">Gallery</a> · <a href="contact.html">Contact</a> · $150 minimum job charge.</p>

          <h2>Project photos — {city} area</h2>
          <div class="city-gallery-teaser">
{gallery}
          </div>
          <p><a href="gallery.html">View full project gallery &rarr;</a></p>

          <h2>How scheduling works in {city}</h2>
          <ol>
{scheduling}
          </ol>

          <p><strong>Nearby:</strong> {nearby_links(c["nearby"])}</p>
        </div>
        <aside class="sp-sidebar" data-reveal>
          <div class="about-card">
            <h3>Free {city} estimate</h3>
            <p>Owner on every job — {county} County routes. Rescreens, new-enclosure inquiries &amp; super gutters.</p>
            <a class="btn btn-primary btn-full" href="tel:7273866562">(727) 386-6562</a>
            <a class="btn btn-ghost btn-full" href="contact.html" style="margin-top:12px;">Contact form</a>
            <p style="margin-top:14px;font-size:0.85rem;color:var(--muted);">Based in New Port Richey &middot; $150 minimum</p>
          </div>
        </aside>
      </div>
    </section>

    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">Our process</p>
          <h2>How Chris handles {city} jobs</h2>
          <p>Owner-direct from New Port Richey — no rotating crew, no call-center quote.</p>
        </div>
        <div class="sp-process-grid" data-reveal>
{process_cards}
        </div>
      </div>
    </section>

    <section class="section-shell faq-section">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">{city} screen repair FAQ</p>
          <h2>Common questions</h2>
        </div>
        <div class="faq-list">
{faq_html(prefix, c["faq"])}
        </div>
      </div>
    </section>

    <section class="areas-strip"><div class="container"><p class="eyebrow">{county} County</p><p><a href="{county_link}">{county} County screen repair</a> · <a href="service-areas.html">All service areas &rarr;</a></p></div></section>

    <section class="contact-section contact-section--parallax section-shell" data-parallax-overscan="0.30">
      <div class="container contact-inner" data-reveal>
        <p class="eyebrow">Get your quote</p>
        <h2>{c["cta"]}</h2>
        <p>Full pool cage rescreens · new enclosure partner path · super gutters · small panel jobs</p>
        <a class="btn btn-primary btn-lg" href="tel:7273866562">(727) 386-6562</a>
      </div>
    </section>
  </main>

  <div id="site-footer-include"></div>
  <script src="includes.js"></script>
  <script src="script.js"></script>
</body>
</html>
'''


def render_county(c: dict) -> str:
    """County hubs use areaServed AdministrativeArea and a city-list section."""
    # Reuse city renderer with overrides already in dict
    html_out = render_city(c)
    # Fix areaServed type if needed — already set via area_type
    return html_out


def word_count_main(html_text: str) -> int:
    m = re.search(r"<main[\s\S]*?</main>", html_text, re.I)
    if not m:
        return 0
    text = strip_tags(m.group(0))
    return len(re.findall(r"\b\w+\b", text))
