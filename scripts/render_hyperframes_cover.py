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


SHIELD = [  # cubic/line segments of the shield, same control points as \auratwin@shieldpath (TikZ)
    ("M", (0.02, 1.68)), ("C", (0.35, 1.68), (0.60, 1.78), (0.80, 1.92)),
    ("C", (1.00, 1.78), (1.25, 1.68), (1.58, 1.68)), ("L", (1.58, 0.95)),
    ("C", (1.58, 0.45), (1.15, 0.15), (0.80, 0.00)), ("C", (0.45, 0.15), (0.02, 0.45), (0.02, 0.95)),
]


def logo_mark_svg(px: float = 100.0, **_ignored) -> str:
    """v1.4.0 Shield-Eye logo (security, trust, aesthetics); identical geometry to the TikZ \\auratwin@mark.
    Units: 1.6 x 1.92 box; svg_y = (1.95 - y) * px."""
    X = lambda x: round(x * px, 2)
    Y = lambda y: round((1.95 - y) * px, 2)

    def path(segs, cx=0.8, cy=0.96, s=1.0):
        tr = lambda p: (cx + (p[0] - cx) * s, cy + (p[1] - cy) * s)
        out = []
        for seg in segs:
            pts = " ".join(f"{X(tr(p)[0])},{Y(tr(p)[1])}" for p in seg[1:])
            out.append(f"{seg[0]}{pts}")
        return " ".join(out) + " Z"

    eye = (f"M{X(0.30)},{Y(1.12)} C{X(0.55)},{Y(1.43)} {X(1.05)},{Y(1.43)} {X(1.30)},{Y(1.12)} "
           f"C{X(1.05)},{Y(0.81)} {X(0.55)},{Y(0.81)} {X(0.30)},{Y(1.12)} Z")
    keyhole = (f"M{X(0.772)},{Y(1.15)} L{X(0.828)},{Y(1.15)} L{X(0.846)},{Y(1.005)} L{X(0.754)},{Y(1.005)} Z")
    a1 = f"M{X(0.40)},{Y(0.48)} L{X(0.40)},{Y(0.60)} A{0.14*px},{0.14*px} 0 0 1 {X(0.54)},{Y(0.74)} L{X(0.54)},{Y(0.48)} Z"
    a2 = f"M{X(0.68)},{Y(0.74)} L{X(0.68)},{Y(0.62)} A{0.12*px},{0.12*px} 0 0 0 {X(0.92)},{Y(0.62)} L{X(0.92)},{Y(0.74)} Z"
    a3 = f"M{X(1.06)},{Y(0.48)} L{X(1.06)},{Y(0.74)} A{0.14*px},{0.14*px} 0 0 1 {X(1.20)},{Y(0.60)} L{X(1.20)},{Y(0.48)} Z"
    return (f'<path d="{path(SHIELD)}" fill="{PAL["forest"]}"/>'
            f'<path d="{path(SHIELD, s=0.86)}" fill="none" stroke="{PAL["mustard"]}" stroke-width="{0.022*px}"/>'
            f'<path d="{eye}" fill="{PAL["eggnog"]}"/>'
            f'<circle cx="{X(0.8)}" cy="{Y(1.12)}" r="{0.205*px}" fill="{PAL["mustard"]}" stroke="{PAL["dust"]}" stroke-width="{0.016*px}"/>'
            f'<circle cx="{X(0.8)}" cy="{Y(1.165)}" r="{0.058*px}" fill="{PAL["forest"]}"/>'
            f'<path d="{keyhole}" fill="{PAL["forest"]}"/>'
            f'<circle cx="{X(0.885)}" cy="{Y(1.215)}" r="{0.03*px}" fill="{PAL["eggnog"]}"/>'
            f'<path d="{a1}" fill="{PAL["eggnog"]}"/><path d="{a2}" fill="{PAL["mustard"]}"/>'
            f'<path d="{a3}" fill="{PAL["dust"]}"/>')


def logo_html() -> str:
    mark = logo_mark_svg(150)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
 html,body{{margin:0;width:1000px;height:640px;overflow:hidden;background:{PAL['eggnog']};
   font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}}
 .card{{position:absolute;inset:28px;border:3px solid {PAL['forest']};outline:1.5px solid {PAL['mustard']};
   outline-offset:-12px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
 svg{{width:240px;height:293px;overflow:visible;filter:drop-shadow(0 10px 18px rgba(30,50,38,.25))}}
 h1{{margin:18px 0 0;font-weight:300;font-size:70px;letter-spacing:.06em;color:{PAL['forest']}}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 p{{margin:6px 0 0;font-size:18px;font-weight:600;letter-spacing:.34em;color:{PAL['dust']}}}
</style></head><body><div class="card">
<svg viewBox="0 0 240 293">{mark}</svg>
<h1>AuraTwin <b>AI</b></h1><p>SECURE · CALIBRATED · BEAUTIFUL</p></div></body></html>"""


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
    # v1.4.0: palette swatches only, without colour-name labels (user request: no clutter)
    sw = "".join(f'<div class="sw"><span style="background:{c}"></span></div>' for c, _ in SWATCHES)
    mark = logo_mark_svg(62)
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
 html,body{{margin:0;width:1600px;height:640px;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif}}
 .bg{{position:absolute;inset:0;background:
   radial-gradient(760px 520px at 80% 35%, rgba(111,125,123,.55), transparent 62%),
   radial-gradient(640px 520px at 8% 95%, rgba(194,126,53,.55), transparent 60%),
   linear-gradient(115deg,{PAL['forest']} 0%, #16261C 55%, #2A3A30 100%)}}
 .frame{{position:absolute;inset:18px;border:2px solid {PAL['mustard']}}}
 .mesh{{position:absolute;inset:0;width:1600px;height:640px}}
 .txt{{position:absolute;right:80px;top:58px;width:780px;color:{PAL['eggnog']}}}
 .logo{{direction:ltr;text-align:right}}
 .logo svg{{width:100px;height:121px;overflow:visible;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35))}}
 .kicker{{font-size:21px;letter-spacing:.28em;color:{PAL['mustard']};direction:ltr;text-align:right;margin-top:8px}}
 h1{{font-family:'Didot','Bodoni MT',Georgia,serif;font-weight:400;font-size:92px;margin:2px 0 0;
   direction:ltr;text-align:right;letter-spacing:.03em}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 .he{{font-size:31px;font-weight:600;line-height:1.35;margin-top:6px}}
 .swatches{{position:absolute;right:80px;bottom:44px;display:flex;gap:16px;direction:ltr}}
 .sw{{display:flex;flex-direction:column;align-items:center;color:{PAL['eggnog']};font-size:12px;letter-spacing:.12em}}
 .sw span{{width:66px;height:66px;border-radius:33px 33px 4px 4px;border:1.5px solid {PAL['mustard']}}}
</style></head><body><div class="bg"></div>{mesh_svg()}<div class="frame"></div>
<div class="txt"><div class="logo"><svg viewBox="0 0 100 121">{mark}</svg></div>
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
