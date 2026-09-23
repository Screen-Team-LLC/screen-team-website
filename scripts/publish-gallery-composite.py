#!/usr/bin/env python3
"""Register one composite in the brand gallery and optionally queue/deploy it."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gallery_longform import build_gallery_longform, render_project_page  # noqa: E402
CONFIG = json.loads((ROOT / "scripts" / "composite-brand.json").read_text(encoding="utf-8"))
GALLERY_DIR = ROOT / CONFIG["gallery_dir"]
MANIFEST_PATH = ROOT / CONFIG["job_manifest"]
DETAIL_DIR = ROOT / "gallery"
SMM_ROOT = Path(r"E:\KnightLogics-Growth-System\Social\Social-Media-Manager")
POPULATOR = SMM_ROOT / "scheduled_brand_posting" / "populate_brand_gallery.py"
MEDIA_LIB = SMM_ROOT / "scheduled_brand_posting" / "media_library" / str(CONFIG.get("brand") or "st")


def run(cmd: list[str], *, cwd: Path = ROOT) -> None:
    print("+", " ".join(str(item) for item in cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def load_manifest() -> dict:
    if not MANIFEST_PATH.is_file():
        return {"version": 1, "brand": CONFIG["brand"], "projects": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def load_facts(path: Path | None) -> dict:
    if not path or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def update_manifest(base: str, title: str, facts: dict, longform: dict) -> dict:
    manifest = load_manifest()
    projects = manifest.setdefault("projects", [])
    public = CONFIG["gallery_public_path"]
    entry = {
        "id": base,
        "title": title,
        "summary": longform["summary"],
        "image": f"{public}/{base}.webp",
        "social_image": f"{public}/{base}-social.jpg",
        "gbp_image": f"{public}/{base}-gbp.jpg",
        "detail_url": longform["detail"]["path"],
        "scope_url": longform["scope"]["path"],
        "service": longform["service"],
        "city_name": longform["city_name"],
        "county_name": longform["county_name"],
        "photo_before": int(facts.get("photo_before") or 0),
        "photo_process": int(facts.get("photo_process") or 0),
        "photo_after": int(facts.get("photo_after") or 0),
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    existing = next((item for item in projects if item.get("id") == base), None)
    if existing:
        existing.update(entry)
        entry = existing
    else:
        projects.insert(0, entry)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry


def write_pages(longform: dict) -> tuple[Path, Path]:
    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    detail = DETAIL_DIR / f"{longform['id']}.html"
    scope = DETAIL_DIR / f"{longform['id']}-scope.html"
    detail.write_text(render_project_page(longform, "detail"), encoding="utf-8")
    scope.write_text(render_project_page(longform, "scope"), encoding="utf-8")
    return detail, scope


def refresh_ai_indexes(manifest: dict) -> None:
    lines = []
    for project in manifest.get("projects") or []:
        title = str(project.get("title") or project.get("id") or "Project").strip()
        detail = str(project.get("detail_url") or "").strip()
        scope = str(project.get("scope_url") or "").strip()
        if detail:
            lines.append(f"- [{title}]({CONFIG['website_url']}/{detail})")
        if scope:
            lines.append(f"- [{title} scope of work]({CONFIG['website_url']}/{scope})")
    block = "\n".join(lines) if lines else "- None published yet."
    section = (
        "## Completed job pages\n\n"
        "Each composite has a project page and a separate scope page. "
        "Streets, customer phones, and invoice amounts are not published.\n\n"
        f"{block}\n"
    )
    for name in ("llms.txt", "ai.txt"):
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        start = "<!-- screen-team-job-pages:start -->"
        end = "<!-- screen-team-job-pages:end -->"
        wrapped = f"{start}\n{section}{end}\n"
        if start in text and end in text:
            text = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", wrapped, text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + wrapped
        path.write_text(text, encoding="utf-8")


def update_sitemap(detail_url: str) -> None:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        return
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    tree = ET.parse(path)
    root = tree.getroot()
    target = f"{CONFIG['website_url']}/{detail_url}"
    if any((node.text or "").strip() == target for node in root.findall(f"{{{namespace}}}url/{{{namespace}}}loc")):
        return
    url = ET.SubElement(root, f"{{{namespace}}}url")
    ET.SubElement(url, f"{{{namespace}}}loc").text = target
    ET.SubElement(url, f"{{{namespace}}}lastmod").text = datetime.now(timezone.utc).date().isoformat()
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--basename", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--facts-json", type=Path, default=None)
    parser.add_argument("--fan-out", action="store_true")
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--commit-message", default="")
    args = parser.parse_args()
    base = re.sub(r"[^a-z0-9-]+", "-", args.basename.lower()).strip("-")
    if re.search(r"(^|-)(test|demo)(-|$)", base):
        raise SystemExit(f"Refusing to publish a test or demo composite: {base}")
    webp = GALLERY_DIR / f"{base}.webp"
    social = GALLERY_DIR / f"{base}-social.jpg"
    gbp = GALLERY_DIR / f"{base}-gbp.jpg"
    missing = [path for path in (webp, social) if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(str(path) for path in missing)}")
    facts = load_facts(args.facts_json)
    title = args.title.strip() or str(facts.get("title") or "").strip()
    if not title:
        title = re.sub(r"^before-process-after-", "", base).replace("-", " ").title()
    longform = build_gallery_longform(
        {
            "id": base,
            "title": title,
            "city_name": facts.get("city_name") or "",
            "work_notes": facts.get("work_notes") or "",
            "photo_before": facts.get("photo_before") or 0,
            "photo_process": facts.get("photo_process") or 0,
            "photo_after": facts.get("photo_after") or 0,
            "image": f"{CONFIG['gallery_public_path']}/{base}.webp",
        }
    )
    entry = update_manifest(base, title, facts, longform)
    detail, scope = write_pages(longform)
    refresh_ai_indexes(load_manifest())
    MEDIA_LIB.mkdir(parents=True, exist_ok=True)
    shutil.copy2(social, MEDIA_LIB / social.name)
    if gbp.is_file():
        shutil.copy2(gbp, MEDIA_LIB / gbp.name)
    if CONFIG.get("build_command"):
        run([sys.executable, str(ROOT / CONFIG["build_command"])])
    update_sitemap(entry["detail_url"])
    update_sitemap(entry["scope_url"])
    if args.fan_out:
        if not POPULATOR.is_file():
            raise SystemExit(f"Missing Social Ops populator: {POPULATOR}")
        run([sys.executable, str(POPULATOR), "--brand", CONFIG["brand"], "--only", base, "--status", "ready", "--fan-out"], cwd=SMM_ROOT)
    if args.deploy:
        paths = [
            webp.relative_to(ROOT),
            social.relative_to(ROOT),
            MANIFEST_PATH.relative_to(ROOT),
            detail.relative_to(ROOT),
            scope.relative_to(ROOT),
        ]
        if gbp.is_file():
            paths.append(gbp.relative_to(ROOT))
        for generated in (ROOT / "gallery.html", ROOT / "sitemap.xml", ROOT / "llms.txt", ROOT / "ai.txt"):
            if generated.is_file():
                paths.append(generated.relative_to(ROOT))
        run(["git", "add", *[str(path) for path in paths]])
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if staged.returncode == 1:
            run(["git", "commit", "-m", args.commit_message or f"Add {CONFIG['brand'].upper()} project composite {base}"])
        elif staged.returncode != 0:
            raise SystemExit("Unable to inspect staged website changes")
        run(["git", "push", "origin", "main"])
    print(json.dumps({"status": "ok", "entry": entry, "manifest": str(MANIFEST_PATH), "detail": str(detail), "scope": str(scope)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
