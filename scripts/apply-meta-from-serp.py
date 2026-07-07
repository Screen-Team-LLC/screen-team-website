#!/usr/bin/env python3
"""Apply Serper-driven meta descriptions to Screen Team HTML + seo-keywords.json."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "seo" / "meta-descriptions.json"
SERP_PATH = ROOT / "seo" / "serp-meta-research.json"
SEO_KEYWORDS = ROOT / "data" / "seo-keywords.json"
MAX_LEN = 159
PRIMARY_WINDOW = 80

META_RE = re.compile(r'(<meta name="description" content=")([^"]*)(")', re.I)
OG_RE = re.compile(r'(<meta property="og:description" content=")([^"]*)(")', re.I)
TWITTER_RE = re.compile(r'(<meta name="twitter:description" content=")([^"]*)(")', re.I)

REQUIRED_TOKENS = (
    "screen",
    "pool",
    "lanai",
    "cage",
    "rescreen",
    "gutter",
    "tampa",
    "pinellas",
    "pasco",
    "hillsborough",
    "chris",
    "727",
    "repair",
    "panel",
    "storm",
    "pet",
    "pricing",
    "contact",
    "estimate",
)


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True).replace("&#x27;", "'")


BANNED_PHRASES = (
    "licensed and insured",
    "rescreen rescue",
    "bbb directory",
    "dead battery",
    "fix phones",
    "phone repair",
    "computer repair",
    "homeadvisor",
    "yelp",
)


def validate(description: str, path: str) -> list[str]:
    issues: list[str] = []
    lower = description.lower()
    if len(description) > MAX_LEN:
        issues.append(f"{path}: {len(description)} chars (max {MAX_LEN})")
    if len(description) < 70:
        issues.append(f"{path}: description may be too short ({len(description)} chars)")
    primary = description[:PRIMARY_WINDOW].lower()
    if not any(token in primary for token in REQUIRED_TOKENS):
        issues.append(f"{path}: primary keyword missing in first {PRIMARY_WINDOW} chars")
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            issues.append(f"{path}: banned phrase '{phrase}'")
    if lower.rstrip().endswith(" repai") or lower.rstrip().endswith(" pool."):
        issues.append(f"{path}: truncated or incomplete description")
    return issues


def apply_description(html_text: str, description: str) -> str:
    escaped = escape_attr(description)
    updated = META_RE.sub(rf"\1{escaped}\3", html_text, count=1)
    if OG_RE.search(updated):
        updated = OG_RE.sub(rf"\1{escaped}\3", updated, count=1)
    if TWITTER_RE.search(updated):
        updated = TWITTER_RE.sub(rf"\1{escaped}\3", updated, count=1)
    return updated


def sync_seo_keywords(pages: list[dict]) -> None:
    if not SEO_KEYWORDS.exists():
        return
    data = json.loads(SEO_KEYWORDS.read_text(encoding="utf-8"))
    kw_pages = data.setdefault("pages", {})
    for entry in pages:
        rel = entry["path"]
        desc = entry["description"]
        if rel not in kw_pages:
            continue
        kw_pages[rel]["meta_description"] = escape_attr(desc).replace("&#x27;", "'")
        kw_pages[rel]["meta_description_length"] = len(desc)
    data["serper_last_applied"] = json.loads(META_PATH.read_text(encoding="utf-8")).get(
        "serper_generated_at"
    )
    SEO_KEYWORDS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if not SERP_PATH.exists():
        print(f"Missing Serper research: {SERP_PATH.relative_to(ROOT)}")
        return 1
    if not META_PATH.exists():
        print("Run scripts/generate-meta-from-serp.py first.")
        return 1

    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    if not data.get("serper_generated_at"):
        print("meta-descriptions.json missing serper_generated_at.")
        return 1

    failures: list[str] = []
    changed = 0

    for entry in data["pages"]:
        rel_path = entry["path"]
        description = entry["description"].strip()
        path = ROOT / rel_path
        failures.extend(validate(description, rel_path))
        if not path.exists():
            failures.append(f"{rel_path}: file missing")
            continue
        original = path.read_text(encoding="utf-8")
        updated = apply_description(original, description)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        changed += 1
        print(f"updated: {rel_path} ({len(description)} chars)")

    sync_seo_keywords(data["pages"])

    if failures:
        print("\nValidation issues:")
        for issue in failures:
            print(f"  - {issue}")

    print(f"\n{changed} HTML files updated; seo-keywords.json synced.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
