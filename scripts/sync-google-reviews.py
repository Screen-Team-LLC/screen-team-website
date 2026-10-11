#!/usr/bin/env python3
"""Sync Screen Team LLC GBP reviews into data/google-reviews.json.

The JSON feeds the visible on-page review carousel only. No review/rating
structured data is written to index.html (see strip_homepage_review_schema).
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROWTH_POSTER = Path(r"E:\KnightLogics-Growth-System\Social\Social-Media-Manager")
sys.path.insert(0, str(GROWTH_POSTER))

from poster.gbp_api import (  # noqa: E402
    LOCAL_POSTS_API_ROOT,
    _http_json,
    load_gbp_secrets,
    refresh_access_token,
)

# Screen Team LLC GBP (poster/accounts.py gbp_st)
ST_LOCATION_ID = "4667456483992971896"
REVIEWS_OUT = ROOT / "data" / "google-reviews.json"
MAX_CAROUSEL = 12

STAR_MAP = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
}

AVATAR_COLORS = [
    "#1e6b2e",
    "#c0392b",
    "#1a56c4",
    "#FBBC05",
    "#c9a227",
    "#8e44ad",
    "#2c3e50",
    "#e67e22",
    "#16a085",
    "#d35400",
]


def star_int(value: object) -> int:
    if isinstance(value, (int, float)):
        return max(1, min(5, int(value)))
    text = str(value or "").upper().strip()
    if text in STAR_MAP:
        return STAR_MAP[text]
    digits = re.search(r"\d+", text)
    if digits:
        return max(1, min(5, int(digits.group(0))))
    return 5


def relative_date(iso: str) -> str:
    if not iso:
        return ""
    try:
        created = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return iso[:10]
    now = datetime.now(timezone.utc)
    days = max(0, (now - created).days)
    if days < 7:
        return "This week"
    if days < 30:
        weeks = max(1, days // 7)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    if days < 365:
        months = max(1, days // 30)
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = max(1, days // 365)
    return f"{years} year{'s' if years != 1 else ''} ago"


def fetch_reviews(access_token: str) -> tuple[float, int, list[dict]]:
    parent = f"accounts/-/locations/{ST_LOCATION_ID}"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    reviews: list[dict] = []
    page_token = ""
    average = 5.0
    total = 0
    payload: dict | None = None

    while True:
        params: dict[str, str | int] = {"pageSize": 50}
        if page_token:
            params["pageToken"] = page_token
        query = urllib.parse.urlencode(params)
        status, payload = _http_json(
            "GET",
            f"{LOCAL_POSTS_API_ROOT}/{parent}/reviews?{query}",
            headers=headers,
        )
        if status >= 400:
            raise RuntimeError(f"GBP reviews list failed ({status}): {payload}")
        if not isinstance(payload, dict):
            raise RuntimeError(f"Unexpected GBP reviews payload: {payload!r}")

        if "averageRating" in payload:
            try:
                average = float(payload["averageRating"])
            except (TypeError, ValueError):
                pass
        if "totalReviewCount" in payload:
            try:
                total = int(payload["totalReviewCount"])
            except (TypeError, ValueError):
                pass

        reviews.extend(payload.get("reviews") or [])
        page_token = payload.get("nextPageToken") or ""
        if not page_token:
            break

    if not total:
        total = len(reviews)
    if reviews and average == 5.0 and payload and "averageRating" not in payload:
        average = sum(star_int(r.get("starRating")) for r in reviews) / len(reviews)

    return round(average, 1), total, reviews


def to_carousel(raw_reviews: list[dict]) -> list[dict]:
    candidates: list[dict] = []
    for item in raw_reviews:
        stars = star_int(item.get("starRating"))
        if stars < 4:
            continue
        reviewer = item.get("reviewer") or {}
        name = str(reviewer.get("displayName") or "Google reviewer").strip()
        if reviewer.get("isAnonymous"):
            name = "Google reviewer"
        comment = str(item.get("comment") or "").strip()
        if "(Translated by Google)" in comment:
            comment = comment.split("(Translated by Google)")[0].strip()
        if not comment:
            continue
        candidates.append(
            {
                "name": name,
                "meta": "Google review",
                "date": relative_date(str(item.get("createTime") or "")),
                "text": comment,
                "stars": stars,
                "avatarColor": AVATAR_COLORS[len(candidates) % len(AVATAR_COLORS)],
            }
        )
        if len(candidates) >= MAX_CAROUSEL:
            break
    return candidates


def strip_homepage_review_schema() -> None:
    """Make sure index.html carries no AggregateRating/Review JSON-LD.

    Google treats self-served review markup on a LocalBusiness as ineligible
    self-serving reviews (Search Console review-snippet warnings). The reviews
    stay visible on the page via data/google-reviews.json + script.js; they are
    intentionally NOT copied into structured data. Do not re-add them here.
    """
    index_path = ROOT / "index.html"
    raw = index_path.read_bytes()
    html = raw.decode("utf-8")
    cleaned, n1 = re.subn(
        r'\r?\n[ \t]*"aggregateRating":\s*\{.*?\r?\n[ \t]*\},(?=\r?\n)',
        "",
        html,
        count=1,
        flags=re.S,
    )
    cleaned, n2 = re.subn(
        r'\r?\n[ \t]*"review":\s*\[.*?\r?\n[ \t]*\],(?=\r?\n)',
        "",
        cleaned,
        count=1,
        flags=re.S,
    )
    if n1 or n2:
        index_path.write_bytes(cleaned.encode("utf-8"))
        print(f"Removed review schema from index.html (aggregate={n1}, review={n2})")


def main() -> int:
    secrets = load_gbp_secrets()
    token = refresh_access_token(secrets)
    rating, count, raw = fetch_reviews(token)
    carousel = to_carousel(raw)

    if not carousel and REVIEWS_OUT.exists():
        existing = json.loads(REVIEWS_OUT.read_text(encoding="utf-8"))
        carousel = existing.get("reviews") or []

    REVIEWS_OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ratingValue": rating,
        "reviewCount": count,
        "syncedAt": datetime.now(timezone.utc).isoformat(),
        "locationId": ST_LOCATION_ID,
        "reviews": carousel,
    }
    REVIEWS_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {REVIEWS_OUT.relative_to(ROOT)} — {rating} · {count} reviews "
        f"({len(carousel)} carousel)"
    )
    strip_homepage_review_schema()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
