#!/usr/bin/env python3
"""
Screen Team geo SEO expansion — generate unique city & county pages.

  python scripts/generate-geo-seo-pages.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geo_content import all_cities  # noqa: E402
from geo_render import ROOT, render_city, word_count_main  # noqa: E402


def count_internal_links(html: str) -> int:
    # href to local .html pages (not tel:, http, #, / alone)
    return len(re.findall(r'href="(?!tel:|https?:|#|mailto:)([^"]+\.html)"', html))


def main() -> None:
    cities, counties = all_cities()
    pages = list(cities) + list(counties)
    rows = []
    for c in pages:
        html = render_city(c)
        out = ROOT / f"{c['slug']}.html"
        out.write_text(html, encoding="utf-8")
        words = word_count_main(html)
        links = count_internal_links(html)
        status = "OK" if words >= 900 and links >= 8 else "CHECK"
        rows.append((out.name, words, links, status))
        print(f"{status:5} {out.name:45} {words:4} words  {links:2} links")

    thin = [r for r in rows if r[3] != "OK"]
    print(f"\nWrote {len(rows)} pages. Below target: {len(thin)}")
    if thin:
        for name, words, links, _ in thin:
            print(f"  - {name}: {words} words, {links} links")


if __name__ == "__main__":
    main()
