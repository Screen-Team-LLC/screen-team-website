# Shared HTML shell for Screen Team SEO expansion pages
from __future__ import annotations

ORG_SCHEMA = r'''  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://screenteamllc.com/#organization",
  "name": "The Screen Team LLC",
  "legalName": "The Screen Team LLC",
  "url": "https://screenteamllc.com",
  "logo": "https://screenteamllc.com/Images/Logo.png",
  "image": "https://screenteamllc.com/Images/ScreenTeamBanner.png",
  "telephone": "+1-727-386-6562",
  "email": "chris@screenteamllc.com",
  "founder": {
    "@id": "https://screenteamllc.com/about.html#person"
  },
  "contactPoint": {
    "@id": "https://screenteamllc.com/contact.html#contact-point"
  },
  "sameAs": [
    "https://x.com/ScreenTeamLLC",
    "https://www.facebook.com/profile.php?id=61588867359684",
    "https://www.linkedin.com/company/screen-team-llc/?viewAsMember=true",
    "https://nextdoor.com/page/screen-team-llc-safety-harbor-fl"
  ]
}
  </script>'''

BUSINESS_SCHEMA = r'''  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "@id": "https://screenteamllc.com/#business",
  "name": "The Screen Team LLC",
  "description": "Professional screen repair, pool cage rescreens, lanai screening, window screens, garage screens, super gutters, and gutter work across Tampa Bay, FL.",
  "url": "https://screenteamllc.com",
  "telephone": "+1-727-386-6562",
  "email": "chris@screenteamllc.com",
  "image": "https://screenteamllc.com/Images/ScreenTeamBanner.png",
  "logo": "https://screenteamllc.com/Images/Logo.png",
  "priceRange": "$$",
  "openingHours": "Mo-Sa 07:00-18:00",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "New Port Richey",
    "addressRegion": "FL",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 28.252,
    "longitude": -82.7265
  },
  "areaServed": [
    "New Port Richey, FL",
    "St. Petersburg, FL",
    "Clearwater, FL",
    "Tampa, FL",
    "Largo, FL",
    "Dunedin, FL",
    "Safety Harbor, FL",
    "Palm Harbor, FL",
    "Oldsmar, FL",
    "Tarpon Springs, FL",
    "Seminole, FL",
    "Pasco County, FL",
    "Pinellas County, FL",
    "Hillsborough County, FL"
  ],
  "parentOrganization": {
    "@id": "https://screenteamllc.com/#organization"
  },
  "founder": {
    "@id": "https://screenteamllc.com/about.html#person"
  },
  "contactPoint": {
    "@id": "https://screenteamllc.com/contact.html#contact-point"
  },
  "sameAs": [
    "https://x.com/ScreenTeamLLC",
    "https://www.facebook.com/profile.php?id=61588867359684",
    "https://www.linkedin.com/company/screen-team-llc/?viewAsMember=true",
    "https://nextdoor.com/page/screen-team-llc-safety-harbor-fl"
  ]
}
  </script>'''

SERVICE_OPTIONS = [
    "Full Pool Cage Rescreen",
    "New Pool Cage",
    "Super Gutters",
    "Super Gutter Repair",
    "Screen Enclosure Installation",
    "Rescreens",
    "Pool Enclosures",
    "Screen Lanais",
    "Window Screens",
    "Garage Screens",
    "Gutter Work",
    "Not sure - need advice",
]

AREAS_STRIP = '''    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">Where we work</p>
        <p>Serving <strong>New Port Richey</strong> and surrounding communities across <strong>Pinellas, Pasco, and Hillsborough counties</strong> &mdash; including <strong>St. Petersburg</strong>, <strong>Clearwater</strong>, <strong>Tampa</strong>, <strong>Largo</strong>, <strong>Palm Harbor</strong>, <strong>Safety Harbor</strong>, <strong>Dunedin</strong>, <strong>Oldsmar</strong>, <strong>Tarpon Springs</strong>, and <strong>Seminole</strong>. <a href="service-areas.html">See all service areas &rarr;</a></p>
      </div>
    </section>'''


def json_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("\r", "")
    )


def service_select(selected: str) -> str:
    lines = ['                  <option value="" disabled>Select a service...</option>']
    for opt in SERVICE_OPTIONS:
        sel = " selected" if opt == selected else ""
        lines.append(f"                  <option{sel}>{opt}</option>")
    return "\n".join(lines)


def faq_schema(faqs: list[dict]) -> str:
    entities = []
    for f in faqs:
        entities.append(
            "{\n"
            '        "@type": "Question",\n'
            f'        "name": "{json_escape(f["q"])}",\n'
            '        "acceptedAnswer": {\n'
            '          "@type": "Answer",\n'
            f'          "text": "{json_escape(f["a"])}"\n'
            "        }\n"
            "      }"
        )
    return (
        '  <script type="application/ld+json">\n'
        "  {\n"
        '    "@context": "https://schema.org",\n'
        '    "@type": "FAQPage",\n'
        '    "mainEntity": [\n'
        + ",\n".join(entities)
        + "\n    ]\n"
        "  }\n"
        "  </script>"
    )


def faq_html(faqs: list[dict], prefix: str) -> str:
    chevron = (
        '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<polyline points="6 9 12 15 18 9"/></svg>'
    )
    items = []
    for i, f in enumerate(faqs, 1):
        fid = f"{prefix}-faq-{i}"
        items.append(
            f'''          <div class="faq-item">
            <button class="faq-question" aria-expanded="false" aria-controls="{fid}">
              {f["q"]}
              {chevron}
            </button>
            <div class="faq-answer" id="{fid}" aria-hidden="true" inert>
              <div class="faq-answer-inner"><p>{f["a"]}</p></div>
            </div>
          </div>'''
        )
    return "\n\n".join(items)


def render_service_page(p: dict) -> str:
    slug = p["slug"]
    url = f"https://screenteamllc.com/{slug}"
    og_img = p["og_image"]
    if not og_img.startswith("http"):
        og_img_url = f"https://screenteamllc.com/{og_img}"
    else:
        og_img_url = og_img

    schema_faqs = p["schema_faqs"]
    local_faqs = p["local_faqs"]

    imgs = p["images"]
    process = p["process"]

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-NDQ7PTQM');</script>
<!-- End Google Tag Manager -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p["title"]}</title>
  <meta name="description" content="{p["description"]}">
    <meta name="keywords" content="{p["keywords"]}">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary">
  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI crawler summary">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="https://screenteamllc.com/sitemap.xml">
  <meta name="theme-color" content="#3da8d8">
<link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="author" content="The Screen Team LLC">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="New Port Richey, Florida">
  <meta name="geo.position" content="28.2520;-82.7265">
  <meta name="ICBM" content="28.2520, -82.7265">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{p["title"]}">
  <meta property="og:description" content="{p["description"]}">
  <meta property="og:image" content="{og_img_url}">
  <meta property="og:image:width" content="800">
  <meta property="og:image:height" content="600">
  <meta property="og:site_name" content="The Screen Team LLC">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{p["title"]}">
  <meta name="twitter:description" content="{p["description"]}">
  <meta name="twitter:image" content="{og_img_url}">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Service","@id":"{url}#service","name":"{json_escape(p["service_name"])}","description":"{json_escape(p["service_desc"])}","provider":{{"@id":"https://screenteamllc.com/#business"}},"areaServed":[{{"@type":"Place","name":"New Port Richey, FL"}},{{"@type":"Place","name":"St. Petersburg, FL"}},{{"@type":"Place","name":"Clearwater, FL"}},{{"@type":"Place","name":"Largo, FL"}},{{"@type":"Place","name":"Palm Harbor, FL"}},{{"@type":"Place","name":"Safety Harbor, FL"}},{{"@type":"Place","name":"Dunedin, FL"}},{{"@type":"Place","name":"Oldsmar, FL"}},{{"@type":"Place","name":"Tarpon Springs, FL"}},{{"@type":"Place","name":"Seminole, FL"}},{{"@type":"Place","name":"Tampa, FL"}}],"url":"{url}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","@id":"{url}#breadcrumb","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://screenteamllc.com/"}},{{"@type":"ListItem","position":2,"name":"Services","item":"https://screenteamllc.com/services.html"}},{{"@type":"ListItem","position":3,"name":"{json_escape(p["breadcrumb"])}","item":"{url}"}}]}}
  </script>
{faq_schema(schema_faqs)}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": "{url}#webpage",
    "url": "{url}",
    "name": "{json_escape(p["title"])}",
    "description": "{json_escape(p["description"])}",
    "isPartOf": {{"@id": "https://screenteamllc.com/#website"}},
    "about": {{"@id": "https://screenteamllc.com/#business"}},
    "mainEntity": {{"@id": "{url}#service"}},
    "breadcrumb": {{"@id": "{url}#breadcrumb"}},
    "inLanguage": "en-US"
  }}
  </script>
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="Images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="Images/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="Images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="image" href="{imgs["hero_left"]}" fetchpriority="high" media="(min-width: 769px)">
  <link rel="preload" as="image" href="{imgs["hero_top"]}" fetchpriority="high" media="(max-width: 768px)">
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
{ORG_SCHEMA}
{BUSINESS_SCHEMA}
  <link rel="stylesheet" href="styles.css">
<!-- Google Analytics 4 -->  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "x61prei2pi");
  </script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NDQ7PTQM"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

  <div id="site-header-include"></div>

  <main>

    <section class="sp-hero sp-hero--panels hero" aria-label="{p["breadcrumb"]}">
      <div class="hero-panels" aria-hidden="true">
        <div class="hero-panel hero-panel--left hero-panel--photo"><img src="{imgs["hero_left"]}" alt="{imgs["alt_left"]}" width="800" height="600" decoding="async"></div>
        <div class="hero-panel hero-panel--top hero-panel--photo"><img src="{imgs["hero_top"]}" alt="{imgs["alt_top"]}" width="800" height="600" decoding="async"></div>
        <div class="hero-panel hero-panel--bottom hero-panel--photo">
          <img class="hero-panel-img--desktop" src="{imgs["hero_bottom"]}" alt="{imgs["alt_bottom"]}" width="800" height="600" decoding="async">
          <img class="hero-panel-img--mobile" src="{imgs["hero_top"]}" alt="{imgs["alt_top"]}" width="800" height="600" decoding="async">
        </div>
        <div class="hero-panel hero-panel--right hero-panel--photo"><img src="{imgs["hero_right"]}" alt="{imgs["alt_right"]}" width="800" height="600" decoding="async"></div>
      </div>
      <div class="sp-hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <p class="eyebrow"><a href="/">Home</a> &rsaquo; <a href="services.html">Services</a> &rsaquo; {p["breadcrumb"]}</p>
        <h1>{p["h1"]}</h1>
        <p>{p["hero_lead"]}</p>
      </div>
    </section>

    <section class="section-shell">
      <div class="container sp-layout">

        <div class="sp-content" data-reveal>
{p["main_html"]}
        </div>

        <aside class="sp-sidebar">
          <div class="hero-card" aria-label="Get a free quote">
            <p class="card-eyebrow">Get a free quote</p>
            <h2 class="card-name">Talk to Chris Today</h2>
            <p class="card-note">Fill out the form and Chris will get back to you to discuss the job.</p>
            <form
              class="contact-form"
              action="https://formspree.io/f/xdabopjp"
              method="POST"
              id="hero-contact-form"
            >
              <div class="form-group">
                <label for="cf-name">Your Name</label>
                <input type="text" id="cf-name" name="name" placeholder="First and last name" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="cf-phone">Phone Number</label>
                <input type="tel" id="cf-phone" name="phone" placeholder="(727) 000-0000" autocomplete="tel">
              </div>
              <div class="form-group">
                <label for="cf-service">Service Needed</label>
                <select id="cf-service" name="service" required>
{service_select(p["form_selected"])}
                </select>
              </div>
              <div class="form-group">
                <label for="cf-message">Tell us about the job</label>
                <textarea id="cf-message" name="message" placeholder="What needs to be done? Location, size, condition..." rows="3"></textarea>
              </div>
              <input type="hidden" name="_subject" value="{p["form_subject"]} - The Screen Team LLC">
            <input type="hidden" name="_next" value="https://screenteamllc.com/thank-you.html">
              <div class="honeypot-field" aria-hidden="true">
                <label for="cf-gotcha">Leave this field blank</label>
                <input type="text" id="cf-gotcha" name="_gotcha" tabindex="-1" autocomplete="off">
              </div>
              <button type="submit" class="btn btn-primary btn-full">Send My Request</button>
              <p class="form-note">Or call directly: <a href="tel:7273866562">(727) 386-6562</a></p>
            </form>
            <div class="form-success" id="form-success" aria-live="polite" hidden>
              <p class="form-success-msg">Thanks! Chris will be in touch shortly.</p>
            </div>
          </div>
        </aside>

      </div>
    </section>

    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">Our process</p>
          <h2>{process["heading"]}</h2>
          <p>{process["sub"]}</p>
        </div>
        <div class="sp-process-grid" data-reveal>
          <div class="sp-process-card">
            <h3>1. {process["steps"][0]["title"]}</h3>
            <p>{process["steps"][0]["body"]}</p>
          </div>
          <div class="sp-process-card">
            <h3>2. {process["steps"][1]["title"]}</h3>
            <p>{process["steps"][1]["body"]}</p>
          </div>
          <div class="sp-process-card">
            <h3>3. {process["steps"][2]["title"]}</h3>
            <p>{process["steps"][2]["body"]}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section-shell" style="background: var(--bg-card); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
      <div class="container sp-layout">
        <div class="sp-content" data-reveal>
{p["local_html"]}
<div class="sp-photo-grid">
            <figure>
              <img src="{imgs["grid1"]}" alt="{imgs["grid1_alt"]}" width="800" height="600" loading="lazy" decoding="async">
              <figcaption>{imgs["grid1_cap"]}</figcaption>
            </figure>
            <figure>
              <img src="{imgs["grid2"]}" alt="{imgs["grid2_alt"]}" width="800" height="600" loading="lazy" decoding="async">
              <figcaption>{imgs["grid2_cap"]}</figcaption>
            </figure>
          </div>
          <p>Questions about your project? <a href="contact.html">Contact Chris</a> or see <a href="pricing.html">pricing ballparks</a>.</p>
        </div>
        <aside class="sp-sidebar" data-reveal>
          <div class="about-card">
            <h3>Why Screen Team</h3>
            <ul class="about-list">
              <li>{p["why"][0]}</li>
              <li>{p["why"][1]}</li>
              <li>{p["why"][2]}</li>
              <li>{p["why"][3]}</li>
            </ul>
            <a class="btn btn-primary btn-full" href="tel:7273866562">(727) 386-6562</a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section-shell faq-section">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">More questions</p>
          <h2>{p["local_faq_heading"]}</h2>
        </div>
        <div class="faq-list">
{faq_html(local_faqs, p["faq_prefix"] + "-local")}
        </div>
      </div>
    </section>

{AREAS_STRIP}

    <section id="faq" class="faq-section section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">Common questions</p>
          <h2>{p["schema_faq_heading"]}</h2>
          <p>{p["schema_faq_sub"]}</p>
        </div>
        <div class="faq-list">
{faq_html(schema_faqs, p["faq_prefix"])}
        </div>
      </div>
    </section>

    <section class="contact-section contact-section--parallax section-shell" data-parallax-overscan="0.30">
      <div class="container contact-inner">
        <p class="eyebrow">Ready to get started?</p>
        <h2>{p["cta_h2"]}</h2>
        <p>{p["cta_p"]}</p>
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


def render_policy_page(p: dict) -> str:
    url = f"https://screenteamllc.com/{p['slug']}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-NDQ7PTQM');</script>
<!-- End Google Tag Manager -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p["title"]}</title>
  <meta name="description" content="{p["description"]}">
    <meta name="keywords" content="{p["keywords"]}">
<link rel="canonical" href="{url}">
  <meta name="robots" content="noindex, follow">
  <meta name="author" content="The Screen Team LLC">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="New Port Richey, Florida">
  <meta name="geo.position" content="28.2520;-82.7265">
  <meta name="ICBM" content="28.2520, -82.7265">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{p["title"]}">
  <meta property="og:description" content="{p["description"]}">
  <meta property="og:image" content="https://screenteamllc.com/Images/ScreenTeamBanner.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="The Screen Team LLC">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{p["title"]}">
  <meta name="twitter:description" content="{p["description"]}">
  <meta name="twitter:image" content="https://screenteamllc.com/Images/ScreenTeamBanner.png">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","@id":"{url}#breadcrumb","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://screenteamllc.com/"}},{{"@type":"ListItem","position":2,"name":"{json_escape(p["breadcrumb"])}","item":"{url}"}}]}}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": "{url}#policy",
    "url": "{url}",
    "name": "{json_escape(p["title"])}",
    "description": "{json_escape(p["description"])}",
    "isPartOf": {{
      "@id": "https://screenteamllc.com/#website"
    }},
    "publisher": {{
      "@id": "https://screenteamllc.com/#business"
    }},
    "about": {{
      "@id": "https://screenteamllc.com/#business"
    }},
    "breadcrumb": {{
      "@id": "{url}#breadcrumb"
    }},
    "inLanguage": "en-US"
  }}
  </script>
{ORG_SCHEMA}
{BUSINESS_SCHEMA}
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="Images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="Images/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="Images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <link rel="stylesheet" href="styles.css">
  <!-- Google Analytics -->
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "x61prei2pi");
  </script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NDQ7PTQM"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

  <div id="site-header-include"></div>

  <main>

    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="/">Home</a> &rsaquo; {p["breadcrumb"]}</p>
        <h1>{p["h1"]}</h1>
        <p>Last updated: July 2026</p>
      </div>
    </section>

    <section class="section-shell">
      <div class="container" style="max-width: 760px;">

        <div class="sp-content" data-reveal>
{p["body_html"]}
        </div>
      </div>
    </section>

    <section class="contact-section contact-section--parallax section-shell" data-parallax-overscan="0.30">
      <div class="container contact-inner">
        <p class="eyebrow">Questions about this policy?</p>
        <h2>Call or text Chris Westcott.</h2>
        <p>We keep policies plain-language. If something is unclear, ask before work starts.</p>
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
