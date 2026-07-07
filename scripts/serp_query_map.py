#!/usr/bin/env python3
"""Page → Serper query map for Screen Team LLC (screen repair Tampa Bay)."""

from __future__ import annotations

from pathlib import Path

LOCATION_BY_COUNTY = {
    "pinellas": "Pinellas County, Florida, United States",
    "pasco": "Pasco County, Florida, United States",
    "hillsborough": "Hillsborough County, Florida, United States",
}

DEFAULT_LOCATION = "Tampa Bay, Florida, United States"

PAGE_LOCATIONS: dict[str, str] = {
    "index.html": DEFAULT_LOCATION,
    "contact.html": DEFAULT_LOCATION,
    "pricing.html": DEFAULT_LOCATION,
    "pool-enclosures.html": DEFAULT_LOCATION,
    "pool-cage-repair.html": DEFAULT_LOCATION,
    "rescreens.html": DEFAULT_LOCATION,
    "screen-lanais.html": DEFAULT_LOCATION,
    "lanai-screen-replacement.html": DEFAULT_LOCATION,
    "storm-screen-repair.html": DEFAULT_LOCATION,
    "gutters-and-screens.html": DEFAULT_LOCATION,
    "pet-resistant-screen-mesh.html": LOCATION_BY_COUNTY["pinellas"],
    "screen-panel-repair.html": DEFAULT_LOCATION,
    "pinellas-county-screen-repair.html": LOCATION_BY_COUNTY["pinellas"],
    "pasco-county-screen-repair.html": LOCATION_BY_COUNTY["pasco"],
    "hillsborough-county-screen-repair.html": LOCATION_BY_COUNTY["hillsborough"],
    "clearwater-screen-repair.html": "Clearwater, Florida, United States",
    "st-petersburg-screen-repair.html": "St. Petersburg, Florida, United States",
    "tampa-screen-repair.html": "Tampa, Florida, United States",
    "largo-screen-repair.html": "Largo, Florida, United States",
    "seminole-screen-repair.html": "Seminole, Florida, United States",
    "pinellas-park-screen-repair.html": "Pinellas Park, Florida, United States",
    "gulfport-screen-repair.html": "Gulfport, Florida, United States",
    "new-port-richey-screen-repair.html": "New Port Richey, Florida, United States",
    "brandon-screen-repair.html": "Brandon, Florida, United States",
    "wesley-chapel-screen-repair.html": "Wesley Chapel, Florida, United States",
    "holiday-screen-repair.html": "Holiday, Florida, United States",
    "hudson-screen-repair.html": "Hudson, Florida, United States",
    "land-o-lakes-screen-repair.html": "Land O Lakes, Florida, United States",
    "belleair-screen-repair.html": "Belleair, Florida, United States",
}

# GSC-informed primary + secondary queries per page (unique intent per URL).
PAGE_QUERY_MAP: dict[str, list[str]] = {
    "index.html": [
        "screen repair tampa bay",
        "pool cage rescreen tampa bay",
        "the screen team llc",
    ],
    "pool-cage-repair.html": [
        "pool cage repair",
        "pool cage screen repair",
        "pool cage repair tampa bay",
    ],
    "pool-enclosures.html": [
        "pool enclosure repair tampa bay",
        "pool cage repair near me",
    ],
    "rescreens.html": [
        "pool cage rescreen",
        "pool cage rescreening",
        "pool rescreen tampa bay",
    ],
    "screen-lanais.html": [
        "lanai screen repair",
        "lanai screen repair near me",
        "rescreen lanai",
    ],
    "lanai-screen-replacement.html": [
        "lanai screen replacement",
        "lanai screen replacement pinellas county",
    ],
    "screen-panel-repair.html": [
        "screen panel repair",
        "screen replacements tampa",
    ],
    "storm-screen-repair.html": [
        "storm screen repair",
        "hurricane screen repair pinellas county",
    ],
    "gutters-and-screens.html": [
        "gutters and screens",
        "gutter repair tampa bay fl",
    ],
    "pet-resistant-screen-mesh.html": [
        "pet resistant pool screen pinellas",
        "superscreen pool cage repair pinellas",
    ],
    "pinellas-county-screen-repair.html": [
        "screen repair company pinellas county",
        "pool cage rescreen pinellas county",
        "lanai screen repair pinellas county",
    ],
    "pasco-county-screen-repair.html": [
        "screen repair pasco county",
        "pool cage rescreen pasco county",
    ],
    "hillsborough-county-screen-repair.html": [
        "screen repair hillsborough county",
        "pool screen repair tampa",
    ],
    "clearwater-screen-repair.html": [
        "pool cage repair clearwater fl",
        "screen repair clearwater fl",
    ],
    "seminole-screen-repair.html": [
        "lanai screen repair seminole fl",
        "screen repair seminole fl",
    ],
    "pinellas-park-screen-repair.html": [
        "pool screen repair pinellas park fl",
    ],
    "gulfport-screen-repair.html": [
        "pool cage rescreen gulfport fl",
    ],
    "tampa-screen-repair.html": [
        "screen repair tampa fl",
        "pool cage rescreen tampa",
    ],
    "new-port-richey-screen-repair.html": [
        "screen enclosures new port richey",
        "pool screens new port richey fl",
    ],
    "brandon-screen-repair.html": [
        "pool screen repair brandon fl",
    ],
    "contact.html": [
        "screen repair tampa bay phone",
        "pool cage repair estimate tampa",
    ],
    "pricing.html": [
        "pool cage rescreen cost tampa bay",
        "screen repair cost tampa bay",
    ],
}


def query_locations(page: str) -> str:
    return PAGE_LOCATIONS.get(page, DEFAULT_LOCATION)


def build_full_page_query_map() -> dict[str, list[str]]:
    """Return page map plus auto-discovered city pages from the repo."""
    merged = dict(PAGE_QUERY_MAP)
    root = Path(__file__).resolve().parents[1]
    for path in sorted(root.glob("*-screen-repair.html")):
        page = path.name
        if page in merged:
            continue
        city_slug = page.replace("-screen-repair.html", "")
        city_words = city_slug.replace("-", " ")
        merged[page] = [
            f"pool screen repair {city_words} fl",
            f"screen repair {city_words} fl",
        ]
    return merged
