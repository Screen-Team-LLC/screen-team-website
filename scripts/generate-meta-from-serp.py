#!/usr/bin/env python3
"""Build seo/meta-descriptions.json from Serper research for Screen Team LLC."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from serp_query_map import build_full_page_query_map  # noqa: E402

ROOT = SCRIPT_DIR.parent
SEO = ROOT / "seo"
SERP_PATH = SEO / "serp-meta-research.json"
OUT_PATH = SEO / "meta-descriptions.json"
SEO_KEYWORDS = ROOT / "data" / "seo-keywords.json"
MAX_LEN = 159


def load_serp_templates():
    spec = importlib.util.spec_from_file_location(
        "serp_meta_research", SCRIPT_DIR / "serp-meta-research.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.suggested_meta_description


suggested_meta_description = load_serp_templates()


def clip(text: str) -> str:
    text = " ".join(text.split())
    if len(text) <= MAX_LEN:
        return text
    return text[: MAX_LEN - 3].rstrip() + "..."


def load_existing_descriptions() -> dict[str, str]:
    if not SEO_KEYWORDS.exists():
        return {}
    data = json.loads(SEO_KEYWORDS.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for page, entry in (data.get("pages") or {}).items():
        desc = str(entry.get("meta_description") or "").replace("&amp;", "&")
        if desc:
            out[page] = desc
    return out


def best_serp_description(serp_rows: list[dict], page_path: str) -> tuple[str, list[str], str]:
    matches = [row for row in serp_rows if row.get("target_page") == page_path and not row.get("error")]
    queries = [str(row.get("query") or "") for row in matches]
    if not matches:
        return "", queries, ""

    def sort_key(row: dict) -> tuple:
        source_score = 0 if row.get("source") == "page_map" else 1
        rank = row.get("screenteam_rank")
        rank_score = rank if isinstance(rank, int) else 99
        impr = 0
        raw = row.get("gsc_impressions")
        if str(raw or "").isdigit():
            impr = int(raw)
        return (source_score, rank_score, -impr)

    ranked = sorted(matches, key=sort_key)
    primary = ranked[0]
    suggested = suggested_meta_description(primary).strip()
    note_parts = []
    for row in ranked[:2]:
        competitors = row.get("competitor_title_angles") or []
        if competitors:
            note_parts.append(f"{row.get('query')}: vs {competitors[0][:50]}")
    return clip(suggested), queries, "; ".join(note_parts)


def main() -> int:
    if not SERP_PATH.exists():
        print("Run scripts/serp-meta-research.py first.")
        return 1

    serp = json.loads(SERP_PATH.read_text(encoding="utf-8"))
    serp_rows = list(serp.get("results") or [])
    page_map = build_full_page_query_map()
    existing = load_existing_descriptions()

    pages: list[dict] = []
    for page_path in sorted(page_map.keys()):
        if not (ROOT / page_path).is_file():
            continue
        description, queries, note = best_serp_description(serp_rows, page_path)
        if not description:
            description = clip(
                suggested_meta_description({"target_page": page_path, "query": "", "intent": ""})
            )
        if not description:
            description = clip(existing.get(page_path, ""))
        pages.append(
            {
                "path": page_path,
                "gsc_queries": queries,
                "serper_note": note,
                "description": description,
            }
        )

    payload = {
        "serper_research": "seo/serp-meta-research.json",
        "serper_generated_at": serp.get("generated_at"),
        "pages": pages,
    }
    SEO.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(pages)} meta entries to {OUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
