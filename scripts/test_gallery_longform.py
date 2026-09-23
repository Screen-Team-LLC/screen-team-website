"""Screen Team job pages: two unique pages, no private facts, real site links."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gallery_longform import (  # noqa: E402
    MIN_WORDS,
    build_gallery_longform,
    clean_public_text,
    render_project_page,
    strip_html_words,
)


def _job(title: str, city: str = "Clearwater") -> dict:
    page = build_gallery_longform(
        {
            "id": "before-process-after-sample",
            "title": title,
            "city_name": city,
            "work_notes": "123 Main Street, call 727-555-0199, ticket ST-44521, total $2,500. Replaced the torn bays.",
            "photo_before": 3,
            "photo_process": 1,
            "photo_after": 2,
            "image": "Images/gallery/before-process-after-sample.webp",
        },
        root=ROOT,
    )
    return page


def test_two_pages_are_long_distinct_and_private() -> None:
    page = _job("Full pool cage rescreen")
    detail = page["detail"]["body_html"]
    scope = page["scope"]["body_html"]
    assert strip_html_words(detail) >= MIN_WORDS
    assert strip_html_words(scope) >= MIN_WORDS
    assert detail != scope
    blob = detail + scope
    assert "727-555-0199" not in blob
    assert "Main Street" not in blob
    assert "ST-44521" not in blob
    assert "$2,500" not in blob and "$2500" not in blob
    assert "$" not in blob
    assert "Faith Works" not in blob
    assert "Tyler" not in blob
    assert "Knight Group" not in blob
    assert "forestry" not in blob.lower()
    assert "clearwater-screen-repair.html" in blob
    assert "full-pool-cage-rescreen.html" in blob
    assert "gallery/before-process-after-sample-scope.html" in detail
    assert "gallery/before-process-after-sample.html" in scope
    assert "Images/gallery/before-process-after-sample.webp" in blob
    html_detail = render_project_page(page, "detail")
    html_scope = render_project_page(page, "scope")
    assert "application/ld+json" in html_detail
    assert 'base href="https://screenteamllc.com/"' in html_detail
    assert "Scope of work" in html_detail
    assert "Project details" in html_scope
    for href in re.findall(r'href="([^"]+\.html)"', html_detail + html_scope):
        if href.startswith(("http://", "https://", "gallery/")):
            continue
        assert (ROOT / href.split("#")[0]).is_file(), href


def test_notes_drop_estimate_boilerplate_and_missing_city_stays_regional() -> None:
    assert clean_public_text("Published Screen Team price. Nothing was sent.") == ""
    page = build_gallery_longform({"id": "lanai-job", "title": "Lanai screen repair"}, root=ROOT)
    assert page["city_name"] == "Tampa Bay"
    assert page["cluster"] == "lanai"
    assert "screen-lanais.html" in page["detail"]["body_html"]
    assert "service-areas.html" in page["detail"]["body_html"]


def test_panels_and_super_gutter_pick_their_own_service_pages() -> None:
    panels = build_gallery_longform({"id": "panels", "title": "Three roof panels", "city_name": "Lithia"}, root=ROOT)
    assert panels["cluster"] == "panels"
    assert panels["city_name"] == "Lithia"
    assert "hillsborough-county-screen-repair.html" in panels["detail"]["body_html"]
    assert "lithia-screen-repair.html" not in panels["detail"]["body_html"]
    gutter = build_gallery_longform({"id": "sg", "title": "Super gutter replacement"}, root=ROOT)
    assert gutter["cluster"] == "super_gutter"
    assert "super-gutters.html" in gutter["scope"]["body_html"]


if __name__ == "__main__":
    test_two_pages_are_long_distinct_and_private()
    test_notes_drop_estimate_boilerplate_and_missing_city_stays_regional()
    test_panels_and_super_gutter_pick_their_own_service_pages()
    print("test_gallery_longform: OK")
