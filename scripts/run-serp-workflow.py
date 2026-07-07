#!/usr/bin/env python3
"""Run full Screen Team Serper SEO workflow: research → meta JSON → apply to HTML."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

ALL_STEPS = [
    ("Serper SERP research", [sys.executable, str(SCRIPTS / "serp-meta-research.py")]),
    ("Generate meta-descriptions.json", [sys.executable, str(SCRIPTS / "generate-meta-from-serp.py")]),
    ("Apply meta to HTML", [sys.executable, str(SCRIPTS / "apply-meta-from-serp.py")]),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Screen Team Serper SEO workflow")
    parser.add_argument(
        "--skip-research",
        action="store_true",
        help="Reuse existing seo/serp-meta-research.json (regenerate meta + apply only)",
    )
    args = parser.parse_args()

    steps = ALL_STEPS[1:] if args.skip_research else ALL_STEPS
    for label, cmd in steps:
        print(f"\n=== {label} ===")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"FAILED: {label}")
            return result.returncode
    print("\nSerper workflow complete.")
    print("Next: review seo/serp-meta-research.md, commit, push, resubmit sitemap in GSC.")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
