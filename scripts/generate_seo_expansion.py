#!/usr/bin/env python3
"""Generate Screen Team SEO expansion HTML pages and report word counts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo_expansion_shell import render_service_page, render_policy_page
from seo_pages_batch1a import PAGES_1
from seo_pages_batch1b import PAGES_1B
from seo_pages_batch1c import PAGES_1C
from seo_pages_batch2a import PAGES_2A
from seo_pages_batch2b import PAGES_2B
from seo_pages_hub_policies import SERVICES_HUB, POLICIES
from seo_expansions import EXPAND, POLICY_EXPAND


def apply_expansions(pages: list) -> None:
    for page in pages:
        extra = EXPAND.get(page["slug"], "")
        if extra:
            page["main_html"] = page["main_html"] + extra
    # Light trim for slightly over-long full cage page
    for page in pages:
        if page["slug"] == "full-pool-cage-rescreen.html":
            page["main_html"] = page["main_html"].replace(
                "Related work often pairs with a <a href=\"pool-cage-door-repair.html\">cage door repair</a>, <a href=\"super-gutters.html\">super gutter</a> check above the header, or a <a href=\"two-story-pool-cage-rescreen.html\">two-story rescreen</a> when height changes the setup. ",
                "Related: <a href=\"pool-cage-door-repair.html\">door repair</a>, <a href=\"super-gutters.html\">super gutters</a>, <a href=\"two-story-pool-cage-rescreen.html\">two-story rescreen</a>. ",
            )


def apply_policy_expansions(policies: list) -> None:
    for pol in policies:
        extra = POLICY_EXPAND.get(pol["slug"], "")
        if extra:
            pol["body_html"] = pol["body_html"] + extra


def visible_word_count(html: str) -> int:
    """Approximate visible body words (strip scripts/styles/tags)."""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    # Prefer main content if present
    m = re.search(r"(?is)<main\b[^>]*>(.*?)</main>", text)
    if m:
        text = m.group(1)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;|&#\d+;", " ", text)
    words = re.findall(r"[A-Za-z0-9']+", text)
    return len(words)


def main() -> None:
    service_pages = PAGES_1 + PAGES_1B + PAGES_1C + PAGES_2A + PAGES_2B + [SERVICES_HUB]
    apply_expansions(service_pages)
    apply_policy_expansions(POLICIES)
    results = []

    for page in service_pages:
        html = render_service_page(page)
        # Services hub breadcrumb: Home › Services only
        if page["slug"] == "services.html":
            html = html.replace(
                '<p class="eyebrow"><a href="/">Home</a> &rsaquo; <a href="services.html">Services</a> &rsaquo; Services</p>',
                '<p class="eyebrow"><a href="/">Home</a> &rsaquo; Services</p>',
            )
            html = html.replace(
                '{"@type":"ListItem","position":2,"name":"Services","item":"https://screenteamllc.com/services.html"},{"@type":"ListItem","position":3,"name":"Services","item":"https://screenteamllc.com/services.html"}',
                '{"@type":"ListItem","position":2,"name":"Services","item":"https://screenteamllc.com/services.html"}',
            )
        path = ROOT / page["slug"]
        path.write_text(html, encoding="utf-8")
        wc = visible_word_count(html)
        results.append((page["slug"], wc, "service"))
        print(f"Wrote {page['slug']} (~{wc} visible words)")

    for pol in POLICIES:
        html = render_policy_page(pol)
        path = ROOT / pol["slug"]
        path.write_text(html, encoding="utf-8")
        wc = visible_word_count(html)
        results.append((pol["slug"], wc, "policy"))
        print(f"Wrote {pol['slug']} (~{wc} visible words)")

    print("\n=== SUMMARY ===")
    for slug, wc, kind in results:
        flag = ""
        if kind == "service" and not (900 <= wc <= 1100):
            flag = " ** OUT OF RANGE **"
        if kind == "policy" and not (600 <= wc <= 900):
            flag = " ** CHECK **"
        print(f"{slug}: ~{wc}{flag}")


if __name__ == "__main__":
    main()
