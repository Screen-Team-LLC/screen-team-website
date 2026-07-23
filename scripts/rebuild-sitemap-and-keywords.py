#!/usr/bin/env python3
"""Regenerate sitemap.xml and merge new URLs into data/seo-keywords.json."""
from pathlib import Path
from datetime import date
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"header.html", "footer.html", "404.html", "thank-you.html"}
today = date.today().isoformat()

pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in EXCLUDE)

priority = {
    "index.html": "1.00",
    "services.html": "0.95",
    "contact.html": "0.90",
    "pricing.html": "0.90",
    "full-pool-cage-rescreen.html": "0.94",
    "super-gutters.html": "0.94",
    "super-gutter-installation.html": "0.93",
    "new-pool-cage-installation.html": "0.93",
    "screen-enclosure-installation.html": "0.92",
    "rescreens.html": "0.92",
    "pool-enclosures.html": "0.91",
    "service-areas.html": "0.90",
    "super-gutter-repair.html": "0.90",
    "pool-cage-gutter-replacement.html": "0.90",
    "seamless-gutters.html": "0.88",
    "two-story-pool-cage-rescreen.html": "0.90",
}

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for name in pages:
    loc = "https://screenteamllc.com/" if name == "index.html" else f"https://screenteamllc.com/{name}"
    if name in priority:
        pri = priority[name]
    elif "county" in name:
        pri = "0.88"
    elif name.endswith("-screen-repair.html"):
        pri = "0.84"
    elif name in {
        "privacy-policy.html",
        "terms-of-service.html",
        "payment-policy.html",
        "warranty-terms.html",
        "image-use-policy.html",
    }:
        pri = "0.40"
    else:
        pri = "0.82"
    lines += [
        "  <url>",
        f"    <loc>{loc}</loc>",
        f"    <lastmod>{today}</lastmod>",
        "    <changefreq>monthly</changefreq>",
        f"    <priority>{pri}</priority>",
        "  </url>",
    ]
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"sitemap urls: {len(pages)}")

TITLE_MAP = {
    "full-pool-cage-rescreen": (
        "Full Pool Cage Rescreen Tampa Bay | Screen Team",
        "Full pool cage rescreen Tampa Bay from $1,995. Large enclosure mesh jobs. Call (727) 386-6562.",
        ["full pool cage rescreen Tampa Bay", "large pool cage rescreen"],
    ),
    "two-story-pool-cage-rescreen": (
        "Two-Story Pool Cage Rescreen Tampa Bay | Screen Team",
        "Two-story pool cage rescreen — tall ladder work across Tampa Bay. Call (727) 386-6562.",
        ["two story pool cage rescreen", "tall pool cage rescreen"],
    ),
    "pool-cage-door-repair": (
        "Pool Cage Door Repair Tampa Bay | Screen Team",
        "Pool cage door repair — torn door panels & latch issues. Call (727) 386-6562.",
        ["pool cage door repair", "lanai door screen repair"],
    ),
    "spa-enclosure-rescreen": (
        "Spa Enclosure Rescreen Tampa Bay | Screen Team",
        "Spa enclosure & spa wing rescreens across Tampa Bay. Call (727) 386-6562.",
        ["spa enclosure rescreen", "spa wing screen repair"],
    ),
    "new-pool-cage-installation": (
        "New Pool Cage Installation Tampa Bay | Screen Team",
        "New pool cage installation — Screen Team scoping with licensed partners. (727) 386-6562.",
        ["new pool cage installation Tampa Bay", "pool cage installation"],
    ),
    "screen-enclosure-installation": (
        "Screen Enclosure Installation Tampa Bay | Screen Team",
        "Screen enclosure installation for Tampa Bay homes. Call (727) 386-6562.",
        ["screen enclosure installation", "new screen enclosure Florida"],
    ),
    "new-lanai-enclosure": (
        "New Lanai Enclosure Tampa Bay | Screen Team",
        "New lanai enclosure builds coordinated for Tampa Bay. Call (727) 386-6562.",
        ["new lanai enclosure", "screened lanai installation"],
    ),
    "custom-screen-enclosure": (
        "Custom Screen Enclosure Tampa Bay | Screen Team",
        "Custom screen enclosure design & build coordination. Call (727) 386-6562.",
        ["custom screen enclosure", "custom pool cage Tampa Bay"],
    ),
    "super-gutters": (
        "Super Gutters Tampa Bay | Pool Cage Gutters | Screen Team",
        "Super gutters Tampa Bay — structural gutters for pool cages & lanais. Call (727) 386-6562.",
        ["super gutters Tampa Bay", "screen enclosure gutter"],
    ),
    "super-gutter-installation": (
        "Super Gutter Installation Tampa Bay | Screen Team",
        "Super gutter installation for Florida pool cages. Call (727) 386-6562.",
        ["super gutter installation", "7 inch super gutter"],
    ),
    "super-gutter-repair": (
        "Super Gutter Repair Tampa Bay | Screen Team",
        "Super gutter repair — sagging, leaking cage gutters fixed. Call (727) 386-6562.",
        ["super gutter repair", "sagging pool cage gutter"],
    ),
    "pool-cage-gutter-replacement": (
        "Pool Cage Gutter Replacement Tampa Bay | Screen Team",
        "Pool cage gutter replacement to stop overflow & fascia rot. Call (727) 386-6562.",
        ["pool cage gutter replacement", "lanai gutter replacement"],
    ),
    "seamless-gutters": (
        "Seamless Gutters Tampa Bay | Screen Team",
        "Seamless aluminum gutters Tampa Bay — often bundled with screen work. (727) 386-6562.",
        ["seamless gutters Tampa Bay", "seamless aluminum gutters"],
    ),
    "screen-door-repair": (
        "Screen Door Repair Tampa Bay | Screen Team",
        "Screen door repair for pool cages & lanais. Call (727) 386-6562.",
        ["screen door repair Tampa Bay", "pool cage screen door"],
    ),
    "no-see-um-screen": (
        "No-See-Um Screen Tampa Bay | Fine Mesh | Screen Team",
        "No-see-um fine mesh for pool cages & lanais. Call (727) 386-6562.",
        ["no-see-um screen Tampa Bay", "fine mesh pool screen"],
    ),
    "services": (
        "Screen Enclosure & Super Gutter Services | Screen Team",
        "Full services: rescreens, new enclosures, super gutters & small jobs. (727) 386-6562.",
        ["screen enclosure services Tampa Bay", "pool cage and gutter services"],
    ),
    "terms-of-service": (
        "Terms of Service | Screen Team LLC",
        "Terms of service for The Screen Team LLC website and services.",
        ["Screen Team terms of service"],
    ),
    "payment-policy": (
        "Payment Policy | Screen Team LLC",
        "Payment policy for Screen Team LLC jobs — cash, check, cards.",
        ["Screen Team payment policy"],
    ),
    "warranty-terms": (
        "Warranty Terms | Screen Team LLC",
        "Workmanship warranty terms for Screen Team LLC screen and gutter work.",
        ["Screen Team warranty"],
    ),
    "image-use-policy": (
        "Image Use Policy | Screen Team LLC",
        "How Screen Team LLC uses and licenses project photos.",
        ["image use policy"],
    ),
}


def meta_for(name: str):
    stem = name.replace(".html", "")
    if stem in TITLE_MAP:
        return TITLE_MAP[stem]
    if stem.endswith("-screen-repair"):
        city = stem.replace("-screen-repair", "").replace("-", " ").title()
        replacements = {
            "Land O Lakes": "Land O Lakes",
            "Town N Country": "Town 'n' Country",
            "St Petersburg": "St. Petersburg",
            "New Port Richey": "New Port Richey",
            "Pinellas Park": "Pinellas Park",
            "East Lake": "East Lake",
            "Feather Sound": "Feather Sound",
            "Kenneth City": "Kenneth City",
            "Madeira Beach": "Madeira Beach",
            "Treasure Island": "Treasure Island",
            "Port Richey": "Port Richey",
            "Dade City": "Dade City",
            "Temple Terrace": "Temple Terrace",
            "Citrus Park": "Citrus Park",
            "Plant City": "Plant City",
        }
        for k, v in replacements.items():
            if city == k:
                city = v
                break
        t = f"Screen Repair {city} FL | Pool Cage & Super Gutters | Screen Team"
        d = f"Pool cage rescreens, new enclosure quotes &amp; super gutters in {city}, FL. Call (727) 386-6562."
        return t, d, [f"screen repair {city}", f"pool cage rescreen {city}", f"super gutter {city}"]
    return None


kw_path = ROOT / "data" / "seo-keywords.json"
data = json.loads(kw_path.read_text(encoding="utf-8"))
existing = data.get("pages", {})
added = 0
for name in pages:
    if name in existing:
        continue
    meta = meta_for(name)
    if not meta:
        continue
    t, d, k = meta
    url = "https://screenteamllc.com/" if name == "index.html" else f"https://screenteamllc.com/{name}"
    existing[name] = {
        "url": url,
        "meta_title": t,
        "meta_title_length": len(t),
        "meta_description": d,
        "meta_description_length": len(re.sub(r"&amp;", "&", d)),
        "keywords": k,
    }
    added += 1

# Update homepage meta in keywords map
existing["index.html"] = {
    **existing.get("index.html", {}),
    "url": "https://screenteamllc.com/",
    "meta_title": "Pool Cage Rescreen & Super Gutters Tampa Bay | Screen Team",
    "meta_title_length": 58,
    "meta_description": "Full pool cage rescreens, new enclosure coordination &amp; super gutters across Tampa Bay. Chris Westcott on every job. Call (727) 386-6562.",
    "meta_description_length": 139,
    "keywords": [
        "pool cage rescreen Tampa Bay",
        "super gutters Tampa Bay",
        "new pool cage installation",
        "screen enclosure Tampa Bay",
        "Chris Westcott",
    ],
}

data["pages"] = existing
data["updated"] = today
city_count = sum(1 for p in pages if p.endswith("-screen-repair.html") and "county" not in p)
data["sitemap"] = {
    "url": "https://screenteamllc.com/sitemap.xml",
    "indexable_pages": len(pages),
    "excluded_noindex": ["404.html", "thank-you.html"],
}
data["prepush_checklist"] = data.get("prepush_checklist", {})
data["prepush_checklist"]["sitemap_urls"] = len(pages)
data["prepush_checklist"]["indexed_pages"] = [
    "index.html",
    "about.html",
    "contact.html",
    "gallery.html",
    "pricing.html",
    "service-areas.html",
    "services.html",
    "service-guarantee.html",
    "enclosure + super gutter service cluster",
    "3 county hubs",
    f"{city_count} city pages",
    "policy pages",
]
data["prepush_checklist"]["excluded_noindex"] = ["404.html", "thank-you.html"]
kw_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"seo-keywords pages: {len(existing)} (added {added})")
print(f"city pages: {city_count}")
