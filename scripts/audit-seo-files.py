#!/usr/bin/env python3
"""Audit sitemap, robots, schema, and meta across indexable HTML pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"header.html", "footer.html", "404.html", "thank-you.html", "privacy-policy.html"}


def main() -> int:
    html_files = sorted(p.name for p in ROOT.glob("*.html") if p.name not in EXCLUDE)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = re.findall(r"<loc>https://screenteamllc.com/([^<]*)</loc>", sitemap)
    sitemap_pages = ["index.html" if u in ("", "/") else u for u in sitemap_urls]

    issues: list[str] = []
    missing_sitemap = [f for f in html_files if f not in sitemap_pages]
    extra_sitemap = [f for f in sitemap_pages if f not in html_files]

    for name in html_files:
        text = (ROOT / name).read_text(encoding="utf-8", errors="replace")
        if "application/ld+json" not in text:
            issues.append(f"{name}: missing JSON-LD")
        if not re.search(r'<meta name="description"', text, re.I):
            issues.append(f"{name}: missing meta description")
        if not re.search(r'<meta property="og:title"', text, re.I):
            issues.append(f"{name}: missing og:title")
        if not re.search(r'<meta property="og:description"', text, re.I):
            issues.append(f"{name}: missing og:description")
        if not re.search(r'<meta name="twitter:card"', text, re.I):
            issues.append(f"{name}: missing twitter:card")
        if not re.search(r'<link rel="canonical"', text, re.I):
            issues.append(f"{name}: missing canonical")
        if "licensed and insured" in text.lower():
            issues.append(f"{name}: contains 'licensed and insured'")

        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', text, re.S | re.I
        )
        for index, block in enumerate(blocks, start=1):
            try:
                data = json.loads(block.strip())
            except json.JSONDecodeError as exc:
                issues.append(f"{name}: invalid JSON-LD block {index}: {exc}")
                continue
            nodes = data if isinstance(data, list) else [data]
            if isinstance(data, dict) and "@graph" in data:
                nodes = data["@graph"]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                if node.get("@type") == "Service" and node.get("provider"):
                    provider = json.dumps(node["provider"])
                    if "screenteamllc.com" not in provider and "Screen Team" not in provider:
                        issues.append(f"{name}: Service provider not Screen Team")

    seo_kw = json.loads((ROOT / "data/seo-keywords.json").read_text(encoding="utf-8"))
    kw_pages = set(seo_kw.get("pages", {}).keys())
    missing_kw = [f for f in html_files if f not in kw_pages]
    extra_kw = [f for f in kw_pages if f not in html_files]

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://screenteamllc.com/sitemap.xml" not in robots:
        issues.append("robots.txt: missing sitemap directive")

    # Deep consistency checks
    missing_webpage: list[str] = []
    missing_org: list[str] = []
    missing_business: list[str] = []
    short_meta: list[str] = []
    no_ai_txt: list[str] = []
    schema_type_counts: dict[int, int] = {}

    for name in html_files:
        text = (ROOT / name).read_text(encoding="utf-8", errors="replace")
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', text, re.S | re.I
        )
        types: list[str] = []
        for block in blocks:
            try:
                data = json.loads(block.strip())
            except json.JSONDecodeError:
                continue
            nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
            if isinstance(nodes, dict):
                nodes = [nodes]
            for node in nodes:
                if isinstance(node, dict) and "@type" in node:
                    ty = node["@type"]
                    types.append(ty if isinstance(ty, str) else "/".join(ty))
        schema_type_counts[len(types)] = schema_type_counts.get(len(types), 0) + 1
        if "WebPage" not in types:
            missing_webpage.append(name)
        if "Organization" not in types and name != "index.html":
            missing_org.append(name)
        if "HomeAndConstructionBusiness" not in types and name != "index.html":
            missing_business.append(name)
        meta = re.search(r'<meta name="description" content="([^"]*)"', text, re.I)
        if meta and len(meta.group(1)) < 70:
            short_meta.append(f"{name} ({len(meta.group(1))} chars)")
        if "/ai.txt" not in text:
            no_ai_txt.append(name)

    print(f"Indexable HTML pages: {len(html_files)}")
    print(f"Sitemap URLs: {len(sitemap_pages)}")
    print(f"seo-keywords entries: {len(kw_pages)}")
    print()
    if missing_sitemap:
        print("MISSING from sitemap:", missing_sitemap)
    if extra_sitemap:
        print("EXTRA in sitemap:", extra_sitemap)
    if missing_kw:
        print("MISSING from seo-keywords:", missing_kw)
    if extra_kw:
        print("EXTRA in seo-keywords:", extra_kw)
    print()
    print(f"Issues ({len(issues)}):")
    for issue in issues:
        print(f"  - {issue}")
    print()
    print("Schema depth (types per page):", dict(sorted(schema_type_counts.items())))
    if missing_webpage:
        print(f"Missing WebPage schema ({len(missing_webpage)}):", missing_webpage)
    if missing_org:
        print(f"Missing inline Organization ({len(missing_org)}):", missing_org)
    if missing_business:
        print(f"Missing inline HomeAndConstructionBusiness ({len(missing_business)}):", missing_business)
    if short_meta:
        print("Short meta descriptions:", short_meta)
    if no_ai_txt:
        print(f"Missing ai.txt link ({len(no_ai_txt)}):", no_ai_txt)
    return 1 if issues or missing_sitemap or extra_sitemap or missing_kw else 0


if __name__ == "__main__":
    raise SystemExit(main())
