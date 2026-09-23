"""Odd photo counts must fill the column — no empty placeholder cells."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-before-process-after-composite.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("st_composite", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_three_photos_bottom_spans_full_width() -> None:
    builder = _load_builder()
    boxes = builder.layout_boxes(3, 0, 0, 400, 300, gap=8, pad=8)
    assert len(boxes) == 3
    inner_w = 400 - 16
    assert boxes[2][0] == 8
    assert boxes[2][2] == inner_w
    assert boxes[0][2] + 8 + boxes[1][2] == inner_w


def test_three_before_column_has_no_surface_hole(tmp_path: Path) -> None:
    builder = _load_builder()
    folder = tmp_path / "shots"
    folder.mkdir()
    Image.new("RGB", (800, 600), (200, 30, 30)).save(folder / "before-01.jpg", "JPEG")
    Image.new("RGB", (800, 600), (30, 200, 30)).save(folder / "before-02.jpg", "JPEG")
    Image.new("RGB", (800, 600), (30, 30, 200)).save(folder / "before-03.jpg", "JPEG")
    Image.new("RGB", (800, 600), (200, 200, 30)).save(folder / "process-01.jpg", "JPEG")
    Image.new("RGB", (800, 600), (200, 30, 200)).save(folder / "after-01.jpg", "JPEG")
    Image.new("RGB", (800, 600), (30, 200, 200)).save(folder / "after-02.jpg", "JPEG")
    Image.new("RGB", (800, 600), (180, 180, 180)).save(folder / "after-03.jpg", "JPEG")
    out = tmp_path / "out"
    built = builder.build(folder, "Screen Panel Replacement", out, "layout-test", gbp_safe=True)
    with Image.open(built["webp"]) as im:
        rgb = im.convert("RGB")
        assert im.size == (1600, 900)
    surface = builder.hex_color(builder.CONFIG["surface"])
    pixel = rgb.getpixel((480, 680))
    assert pixel != surface, f"placeholder surface still visible at {pixel}"
    assert built["social_jpg"].is_file()
    assert built["gbp_jpg"].is_file()
    assert "screenteam" in builder.CONFIG["website"]


if __name__ == "__main__":
    import tempfile

    test_three_photos_bottom_spans_full_width()
    with tempfile.TemporaryDirectory() as tmp:
        test_three_before_column_has_no_surface_hole(Path(tmp))
    print("test_composite_layout: OK")
