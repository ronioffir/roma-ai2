#!/usr/bin/env python3
"""
render_hyperframes_cover.py -- HyperFrames-style raster assets in the "Luxury, Vintage, Bold" palette.

Writes HTML/SVG cards to report/figures/html/ and renders them with headless Edge/Chrome:
    report/figures/auratwin_logo.png   -- app logo / icon (README, store icon)
    report/figures/cover_banner.png    -- cover-page banner
    report/figures/readme_hero.png     -- README hero (same as the banner)
The logo geometry is identical to the TikZ macro \\auratwin@mark in report/auratwin-report.cls
(units: 1 TikZ cm = 100 SVG px, y axis flipped). Booklet rule 16.4: numbers shown in images also
appear in the report text.

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

PAL = {  # "Luxury, Vintage, Bold" -- the only colours used
    "eggnog": "#FBEDC3", "mustard": "#CCB363", "dust": "#6F7D7B",
    "copper": "#C27E35", "garnet": "#76290B", "forest": "#1E3226",
}
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium",
]


def logo_mark_svg(px: float = 100.0, stroke: str = PAL["forest"]) -> str:
    """The three arches + eye, same coordinates as the TikZ mark (2.0 x 1.0 units)."""
    H = 1.0  # flip y: svg_y = (H - y) * px
    X = lambda x: x * px
    Y = lambda y: (H - y) * px
    r1, r2, r3 = 0.58 * px, 0.5 * px, 0.58 * px
    egg = (f"M{X(0)},{Y(0)} L{X(0)},{Y(0.42)} A{r1},{r1} 0 0 1 {X(0.58)},{Y(1.0)} "
           f"L{X(0.58)},{Y(0)} Z")
    dust = (f"M{X(1.42)},{Y(0)} L{X(1.42)},{Y(1.0)} A{r3},{r3} 0 0 1 {X(2.0)},{Y(0.42)} "
            f"L{X(2.0)},{Y(0)} Z")
    must = (f"M{X(0.5)},{Y(1.0)} L{X(0.5)},{Y(0.5)} A{r2},{r2} 0 0 0 {X(1.5)},{Y(0.5)} "
            f"L{X(1.5)},{Y(1.0)} Z")
    eye = (f"M{X(0.42)},{Y(0.55)} C{X(0.75)},{Y(0.86)} {X(1.25)},{Y(0.86)} {X(1.58)},{Y(0.55)} "
           f"C{X(1.25)},{Y(0.24)} {X(0.75)},{Y(0.24)} {X(0.42)},{Y(0.55)} Z")
    return (f'<path d="{egg}" fill="{PAL["eggnog"]}" stroke="{PAL["mustard"]}" stroke-width="{0.012*px}"/>'
            f'<path d="{dust}" fill="{PAL["dust"]}"/>'
            f'<path d="{must}" fill="{PAL["mustard"]}" fill-opacity="0.95"/>'
            f'<path d="{eye}" fill="none" stroke="{stroke}" stroke-width="{0.032*px}"/>'
            f'<circle cx="{X(1.0)}" cy="{Y(0.55)}" r="{0.13*px}" fill="{stroke}"/>'
            f'<circle cx="{X(1.04)}" cy="{Y(0.59)}" r="{0.035*px}" fill="{PAL["eggnog"]}"/>'
            f'<line x1="{X(0)}" y1="{Y(-0.06)}" x2="{X(2.0)}" y2="{Y(-0.06)}" stroke="{stroke}" stroke-width="{0.018*px}"/>')


def logo_html() -> str:
    mark = logo_mark_svg(220)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
 html,body{{margin:0;width:1000px;height:640px;overflow:hidden;background:{PAL['eggnog']};
   font-family:'Didot','Bodoni MT','Georgia',serif}}
 .card{{position:absolute;inset:28px;border:3px solid {PAL['forest']};outline:1.5px solid {PAL['mustard']};
   outline-offset:-12px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
 svg{{width:440px;height:244px;overflow:visible}}
 h1{{margin:26px 0 0;font-weight:400;font-size:76px;letter-spacing:.04em;color:{PAL['forest']}}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 p{{margin:6px 0 0;font:500 20px 'Segoe UI',Arial,sans-serif;letter-spacing:.32em;color:{PAL['dust']}}}
</style></head><body><div class="card">
<svg viewBox="0 -10 440 244">{mark}</svg>
<h1>AuraTwin <b>AI</b></h1><p>CALIBRATED · BEAUTY · STYLE</p></div></body></html>"""


def mesh_svg(w=1600, h=640, seed=8) -> str:
    rnd = random.Random(seed)
    pts = []
    cx, cy = 400, 300
    for _ in range(70):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(0.15, 1.0)
        pts.append((cx + 170 * r * math.cos(a), cy - 40 + 220 * r * math.sin(a)))
    for _ in range(40):
        x = rnd.uniform(110, 690)
        pts.append((x, 560 - 0.0009 * (x - 400) ** 2 + rnd.uniform(-20, 20)))
    lines = []
    for p in pts:
        for q in sorted(pts, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)[1:4]:
            lines.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}"/>')
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2"/>' for x, y in pts)
    return (f'<svg class="mesh" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<g stroke="rgba(251,237,195,.30)" stroke-width="1.2">{"".join(lines)}</g>'
            f'<g fill="rgba(251,237,195,.85)">{dots}</g></svg>')


SWATCHES = [(PAL["eggnog"], "EGG NOG"), (PAL["mustard"], "MUSTARD"), (PAL["dust"], "DUST"),
            (PAL["copper"], "COPPER"), (PAL["garnet"], "GARNET"), (PAL["forest"], "VELVET FOREST")]


def cover_html() -> str:
    sw = "".join(f'<div class="sw"><span style="background:{c}"></span><em>{t}</em></div>' for c, t in SWATCHES)
    mark = logo_mark_svg(90, stroke=PAL["eggnog"])
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
 html,body{{margin:0;width:1600px;height:640px;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif}}
 .bg{{position:absolute;inset:0;background:
   radial-gradient(760px 520px at 80% 35%, rgba(111,125,123,.55), transparent 62%),
   radial-gradient(640px 520px at 8% 95%, rgba(194,126,53,.55), transparent 60%),
   linear-gradient(115deg,{PAL['forest']} 0%, #16261C 55%, #2A3A30 100%)}}
 .frame{{position:absolute;inset:18px;border:2px solid {PAL['mustard']}}}
 .mesh{{position:absolute;inset:0;width:1600px;height:640px}}
 .txt{{position:absolute;right:80px;top:58px;width:780px;color:{PAL['eggnog']}}}
 .logo{{direction:ltr;text-align:right}} .logo svg{{width:200px;height:110px;overflow:visible}}
 .kicker{{font-size:21px;letter-spacing:.28em;color:{PAL['mustard']};direction:ltr;text-align:right;margin-top:8px}}
 h1{{font-family:'Didot','Bodoni MT',Georgia,serif;font-weight:400;font-size:92px;margin:2px 0 0;
   direction:ltr;text-align:right;letter-spacing:.03em}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 .he{{font-size:31px;font-weight:600;line-height:1.35;margin-top:6px}}
 .swatches{{position:absolute;right:80px;bottom:44px;display:flex;gap:16px;direction:ltr}}
 .sw{{display:flex;flex-direction:column;align-items:center;color:{PAL['eggnog']};font-size:12px;letter-spacing:.12em}}
 .sw span{{width:66px;height:66px;border-radius:33px 33px 4px 4px;border:1.5px solid {PAL['mustard']}}}
 .sw em{{font-style:normal;margin-top:7px}}
</style></head><body><div class="bg"></div>{mesh_svg()}<div class="frame"></div>
<div class="txt"><div class="logo"><svg viewBox="0 -8 180 100">{mark}</svg></div>
<div class="kicker">PRELIMINARY DESIGN REPORT · ROMA-AI2</div>
<h1>AuraTwin <b>AI</b></h1>
<div class="he">התאמה ביומטרית מכוילת של אופנה וביוטי, כריית טרנדים והדמיה וירטואלית מותנית-מודל-עסקי</div></div>
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
    ok = png_path.exists() and png_path.stat().st_size > 5_000
    print(("rendered " if ok else "FAILED ") + str(png_path))
    return ok


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    (HTML / "auratwin_logo.html").write_text(logo_html(), encoding="utf-8")
    render(HTML / "auratwin_logo.html", FIG / "auratwin_logo.png", 1000, 640)
    (HTML / "cover_banner.html").write_text(cover_html(), encoding="utf-8")
    render(HTML / "cover_banner.html", FIG / "cover_banner.png", 1600, 640)
    shutil.copyfile(FIG / "cover_banner.png", FIG / "readme_hero.png")


if __name__ == "__main__":
    main()
