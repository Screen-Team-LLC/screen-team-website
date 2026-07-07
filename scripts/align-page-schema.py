#!/usr/bin/env python3
"""Add full Organization, HomeAndConstructionBusiness, WebPage schema + ai.txt links."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"header.html", "footer.html", "404.html", "thank-you.html", "privacy-policy.html"}
SITE = "https://screenteamllc.com"

AREA_SERVED = [
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
    "Pinellas Park, FL",
    "Gulfport, FL",
    "Brandon, FL",
    "Wesley Chapel, FL",
    "Holiday, FL",
    "Hudson, FL",
    "Land O Lakes, FL",
    "Belleair, FL",
    "Pasco County, FL",
    "Pinellas County, FL",
    "Hillsborough County, FL",
]

ORGANIZATION_BLOCK = """  <script type="application/ld+json">
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
  </script>"""


def business_block() -> str:
    area_json = json.dumps(AREA_SERVED, indent=4)
    area_lines = "\n".join(f"    {line}" for line in area_json.splitlines())
    return f"""  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "@id": "https://screenteamllc.com/#business",
  "name": "The Screen Team LLC",
  "description": "Professional screen repair, pool cage rescreens, lanai screening, window screens, garage screens, and gutter work across Tampa Bay, FL.",
  "url": "https://screenteamllc.com",
  "telephone": "+1-727-386-6562",
  "email": "chris@screenteamllc.com",
  "image": "https://screenteamllc.com/Images/ScreenTeamBanner.png",
  "logo": "https://screenteamllc.com/Images/Logo.png",
  "priceRange": "$$",
  "openingHours": "Mo-Sa 07:00-18:00",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "New Port Richey",
    "addressRegion": "FL",
    "addressCountry": "US"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": 28.252,
    "longitude": -82.7265
  }},
  "areaServed": {area_json},
  "parentOrganization": {{
    "@id": "https://screenteamllc.com/#organization"
  }},
  "founder": {{
    "@id": "https://screenteamllc.com/about.html#person"
  }},
  "contactPoint": {{
    "@id": "https://screenteamllc.com/contact.html#contact-point"
  }},
  "sameAs": [
    "https://x.com/ScreenTeamLLC",
    "https://www.facebook.com/profile.php?id=61588867359684",
    "https://www.linkedin.com/company/screen-team-llc/?viewAsMember=true",
    "https://nextdoor.com/page/screen-team-llc-safety-harbor-fl"
  ]
}}
  </script>"""


def has_schema_type(text: str, schema_type: str) -> bool:
    return f'"@type": "{schema_type}"' in text or f'"@type":"{schema_type}"' in text


def page_meta(text: str) -> tuple[str, str, str]:
    title_m = re.search(r"<title>([^<]*)</title>", text, re.I)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', text, re.I)
    canon_m = re.search(r'<link rel="canonical" href="([^"]*)"', text, re.I)
    title = html.unescape(title_m.group(1).strip()) if title_m else ""
    desc = html.unescape(desc_m.group(1).strip()) if desc_m else ""
    url = canon_m.group(1).strip() if canon_m else ""
    return title, desc, url


def city_name_from_page(page: str) -> str | None:
    if not page.endswith("-screen-repair.html"):
        return None
    slug = page.replace("-screen-repair.html", "")
    if slug.endswith("-county"):
        return None
    words = slug.replace("-", " ").title()
    if words == "Land O Lakes":
        return "Land O Lakes"
    if words == "New Port Richey":
        return "New Port Richey"
    if words == "St Petersburg":
        return "St. Petersburg"
    return words


def county_name_from_page(page: str) -> str | None:
    if page == "pinellas-county-screen-repair.html":
        return "Pinellas County, FL"
    if page == "pasco-county-screen-repair.html":
        return "Pasco County, FL"
    if page == "hillsborough-county-screen-repair.html":
        return "Hillsborough County, FL"
    return None


def build_webpage_block(page: str, text: str) -> str:
    title, desc, url = page_meta(text)
    if not url:
        url = f"{SITE}/{page}"
    service_id = f"{url}#service"
    breadcrumb_id = f"{url}#breadcrumb"
    webpage_id = f"{url}#webpage"

    county = county_name_from_page(page)
    city = city_name_from_page(page)

    if county:
        about = [
            {"@id": f"{SITE}/#business"},
            {"@type": "AdministrativeArea", "name": county},
        ]
    elif city:
        about = [
            {"@id": f"{SITE}/#business"},
            {"@type": "Place", "name": f"{city}, FL"},
        ]
    else:
        about = {"@id": service_id}

    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": webpage_id,
        "url": url,
        "name": title,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": about,
        "breadcrumb": {"@id": breadcrumb_id},
        "publisher": {"@id": f"{SITE}/#organization"},
        "inLanguage": "en-US",
        "mainEntity": {"@id": service_id},
    }
    if desc:
        payload["description"] = desc

    return f'  <script type="application/ld+json">\n  {json.dumps(payload, indent=2)}\n  </script>'


def insert_before_stylesheet(text: str, blocks: str) -> str:
    marker = '  <link rel="stylesheet" href="styles.css">'
    if marker not in text:
        marker = "<link rel=\"stylesheet\" href=\"styles.css\">"
    if marker not in text:
        raise ValueError("styles.css link not found")
    return text.replace(marker, blocks + "\n" + marker, 1)


def add_ai_txt_link(text: str) -> str:
    if "/ai.txt" in text:
        return text
    llms = '<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary">'
    ai = (
        '<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary">\n'
        '  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI crawler summary">'
    )
    if llms in text:
        return text.replace(llms, ai, 1)
    return text


def update_index_area_served(text: str) -> str:
    old = '''        "areaServed": [
          "New Port Richey, FL", "St. Petersburg, FL", "Clearwater, FL", "Tampa, FL",
          "Largo, FL", "Dunedin, FL", "Safety Harbor, FL", "Palm Harbor, FL",
          "Oldsmar, FL", "Tarpon Springs, FL", "Seminole, FL", "Pasco County, FL",
          "Pinellas County, FL", "Hillsborough County, FL"
        ],'''
    cities = ",\n          ".join(f'"{c}"' for c in AREA_SERVED)
    new = f'''        "areaServed": [
          {cities}
        ],'''
    return text.replace(old, new)


def main() -> int:
    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name in EXCLUDE:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        blocks_to_add = ""

        if path.name != "index.html":
            if not has_schema_type(text, "Organization"):
                blocks_to_add += "\n" + ORGANIZATION_BLOCK
            if not has_schema_type(text, "HomeAndConstructionBusiness"):
                blocks_to_add += "\n" + business_block()
            if not has_schema_type(text, "WebPage") and has_schema_type(text, "Service"):
                blocks_to_add += "\n" + build_webpage_block(path.name, text)

        text = add_ai_txt_link(text)

        if blocks_to_add:
            text = insert_before_stylesheet(text, blocks_to_add.strip())

        if path.name == "index.html":
            text = update_index_area_served(text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated: {path.name}")

    print(f"\n{changed} files updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
