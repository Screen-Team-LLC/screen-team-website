#!/usr/bin/env python3
"""Sync Screen Team LLC GBP reviews into data/google-reviews.json."""

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


def update_homepage_schema(rating: float, count: int, reviews: list[dict]) -> None:
    """Keep index.html AggregateRating + Review graph in sync with GBP feed."""
    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")

    review_objs: list[str] = []
    for item in reviews[:12]:
        name = (
            str(item.get("name") or "Google reviewer")
            .replace("\\", "\\\\")
            .replace('"', '\\"')
        )
        text = (
            str(item.get("text") or "")
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", " ")
        )
        stars = int(item.get("stars") or 5)
        review_objs.append(
            "          {\n"
            '            "@type": "Review",\n'
            f'            "author": {{"@type": "Person", "name": "{name}"}},\n'
            f'            "reviewBody": "{text}",\n'
            "            \"reviewRating\": {\n"
            '              "@type": "Rating",\n'
            f'              "ratingValue": "{stars}",\n'
            '              "bestRating": "5"\n'
            "            }\n"
            "          }"
        )

    if float(rating) == int(rating):
        rating_str = str(int(rating))
    else:
        rating_str = f"{float(rating):.1f}"

    rating_block = (
        '"aggregateRating": {\n'
        '          "@type": "AggregateRating",\n'
        f'          "ratingValue": "{rating_str}",\n'
        f'          "reviewCount": "{count}",\n'
        '          "bestRating": "5"\n'
        "        }"
    )
    review_block = (
        '"review": [\n' + ",\n".join(review_objs) + "\n        ]"
        if review_objs
        else '"review": []'
    )

    html2, n1 = re.subn(
        r'"aggregateRating":\s*\{.*?\n\s*\}',
        rating_block,
        html,
        count=1,
        flags=re.S,
    )
    html3, n2 = re.subn(
        r'"review":\s*\[.*?\]',
        review_block,
        html2,
        count=1,
        flags=re.S,
    )
    if n1 and n2:
        index_path.write_text(html3, encoding="utf-8")
        print(
            f"Updated index.html schema — {rating_str} · {count} reviews "
            f"({len(review_objs)} listed)"
        )
    else:
        print(
            f"Warning: could not patch index.html schema "
            f"(aggregate={n1}, review={n2})"
        )


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
    update_homepage_schema(rating, count, carousel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
