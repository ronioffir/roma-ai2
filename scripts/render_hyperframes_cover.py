#!/usr/bin/env python3
"""
render_hyperframes_cover.py -- HyperFrames-style raster assets for the report and README.

Writes HTML/CSS "cards" (Hebrew + English, brand palette) to report/figures/html/ and renders
them to PNG with a headless Chromium browser (Microsoft Edge or Google Chrome):
    report/figures/cover_banner.png      -- cover-page image
    report/figures/readme_hero.png       -- README hero banner
Booklet rule (16.4): text inside an image is not searchable, so every number shown in these
cards also appears in the report text or tables.

Usage: python scripts/render_hyperframes_cover.py
"""
from __future__ import annotations

import math
import random
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "report" / "figures"
HTML = FIG / "html"

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium",
]

PALETTE = {"plum": "#4A2470", "teal": "#15807E", "amber": "#D4952B", "tint": "#F3EEF8"}


def mesh_svg(w=1600, h=640, seed=8) -> str:
    """Abstract face-mesh / body-landmark constellation (pure SVG, deterministic)."""
    rnd = random.Random(seed)
    pts = []
    cx, cy = 400, 300
    for k in range(70):  # an ellipse-ish head + shoulders constellation
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(0.15, 1.0)
        pts.append((cx + 170 * r * math.cos(a), cy - 40 + 220 * r * math.sin(a)))
    for k in range(40):
        x = rnd.uniform(110, 690)
        pts.append((x, 560 - 0.0009 * (x - 400) ** 2 + rnd.uniform(-20, 20)))
    lines = []
    for i, p in enumerate(pts):
        d = sorted(pts, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)[1:4]
        for q in d:
            lines.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}"/>')
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2"/>' for x, y in pts)
    return (f'<svg class="mesh" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<g stroke="rgba(255,255,255,.28)" stroke-width="1.2">{"".join(lines)}</g>'
            f'<g fill="rgba(255,255,255,.85)">{dots}</g></svg>')


SWATCHES = [("#F1C9A5", "L*72 a*14 b*22"), ("#D9A27A", "L*61 a*16 b*26"),
            ("#A8714D", "L*46 a*17 b*27"), ("#6E4630", "L*32 a*13 b*20"),
            ("#4F7A9A", "iris prior"), ("#7A5A2E", "iris prior")]


def cover_html() -> str:
    sw = "".join(f'<div class="sw"><span style="background:{c}"></span><em>{t}</em></div>'
                 for c, t in SWATCHES)
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<style>
 html,body{{margin:0;width:1600px;height:640px;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif}}
 .bg{{position:absolute;inset:0;background:
     radial-gradient(900px 500px at 78% 40%, rgba(21,128,126,.95), transparent 60%),
     radial-gradient(700px 600px at 10% 90%, rgba(212,149,43,.55), transparent 60%),
     linear-gradient(120deg,{PALETTE['plum']} 0%, #2B1446 55%, #0E4F4E 100%)}}
 .mesh{{position:absolute;inset:0;width:1600px;height:640px}}
 .txt{{position:absolute;right:70px;top:70px;width:760px;color:#fff}}
 .kicker{{font-size:24px;letter-spacing:.06em;opacity:.85;direction:ltr;text-align:right}}
 h1{{font-size:96px;margin:6px 0 4px;direction:ltr;text-align:right;font-weight:800}}
 h1 b{{color:{PALETTE['amber']}}}
 .he{{font-size:34px;font-weight:600;line-height:1.35;margin-top:8px}}
 .pills{{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap;direction:ltr;justify-content:flex-end}}
 .pill{{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);border-radius:40px;
        padding:9px 18px;font-size:21px}}
 .swatches{{position:absolute;right:70px;bottom:40px;display:flex;gap:14px;direction:ltr}}
 .sw{{display:flex;flex-direction:column;align-items:center;color:#fff;font-size:15px;opacity:.95}}
 .sw span{{width:62px;height:62px;border-radius:14px;border:2px solid rgba(255,255,255,.75);
          box-shadow:0 6px 18px rgba(0,0,0,.25)}}
 .sw em{{font-style:normal;margin-top:6px}}
</style></head><body><div class="bg"></div>{mesh_svg()}
<div class="txt"><div class="kicker">PRELIMINARY DESIGN REPORT · roma-ai2</div>
<h1>AuraTwin <b>AI</b></h1>
<div class="he">התאמה ביומטרית מכוילת של אופנה וביוטי, כריית טרנדים והדמיה וירטואלית מותנית-מודל-עסקי</div>
<div class="pills"><span class="pill">CIELAB ΔE₀₀</span><span class="pill">SMPL-X</span>
<span class="pill">Multimodal RAG</span><span class="pill">Latent Diffusion VTON</span>
<span class="pill">Ad-Gated Economics</span></div></div>
<div class="swatches">{sw}</div></body></html>"""


def find_browser() -> str | None:
    for b in BROWSERS:
        if Path(b).exists() or shutil.which(b):
            return b
    return None


def render(html_path: Path, png_path: Path, w: int, h: int) -> bool:
    browser = find_browser()
    if not browser:
        print("No Chromium browser found; HTML written only:", html_path)
        return False
    cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--window-size={w},{h}", "--force-device-scale-factor=1",
           f"--screenshot={png_path}", html_path.resolve().as_uri()]
    subprocess.run(cmd, check=False, capture_output=True, timeout=120)
    ok = png_path.exists() and png_path.stat().st_size > 10_000
    print(("rendered " if ok else "FAILED ") + str(png_path))
    return ok


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    page = HTML / "cover_banner.html"
    page.write_text(cover_html(), encoding="utf-8")
    render(page, FIG / "cover_banner.png", 1600, 640)
    shutil.copyfile(FIG / "cover_banner.png", FIG / "readme_hero.png")


if __name__ == "__main__":
    main()
