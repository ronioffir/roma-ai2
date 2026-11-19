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


def _sparkle(X, Y, cx, cy, r):
    """Four-point AI sparkle, same quadratic-style control points as \\auratwin@sparkle (TikZ)."""
    k = 0.18 * r
    return (f"M{X(cx)},{Y(cy + r)} Q{X(cx + k)},{Y(cy + k)} {X(cx + r)},{Y(cy)} "
            f"Q{X(cx + k)},{Y(cy - k)} {X(cx)},{Y(cy - r)} Q{X(cx - k)},{Y(cy - k)} {X(cx - r)},{Y(cy)} "
            f"Q{X(cx - k)},{Y(cy + k)} {X(cx)},{Y(cy + r)} Z")


def logo_mark_svg(px: float = 100.0, uid: str = "m", **_ignored) -> str:
    """v2.0 Pocket-Mirror logo: an opened vintage compact mirror at a 3/4 angle, in the brand palette.
    Identical geometry to the TikZ \\auratwin@mark. Units: 1.6 x 2.18 box; svg_y = (2.20 - y) * px."""
    X = lambda x: round(x * px, 2)
    Y = lambda y: round((2.20 - y) * px, 2)
    R = lambda r: round(r * px, 2)
    P = PAL
    band = (f"M{X(0.06)},{Y(0.36)} L{X(0.06)},{Y(0.24)} A{R(0.74)},{R(0.21)} 0 0 0 {X(1.54)},{Y(0.24)} "
            f"L{X(1.54)},{Y(0.36)} Z")
    band_edge = f"M{X(0.06)},{Y(0.24)} A{R(0.74)},{R(0.21)} 0 0 0 {X(1.54)},{Y(0.24)}"
    cx, cy = X(0.80), Y(1.31)
    stripe1 = f"M{X(-0.10)},{Y(0.60)} L{X(0.50)},{Y(1.95)} L{X(0.68)},{Y(1.95)} L{X(0.08)},{Y(0.60)} Z"
    stripe2 = f"M{X(0.16)},{Y(0.60)} L{X(0.76)},{Y(1.95)} L{X(0.82)},{Y(1.95)} L{X(0.22)},{Y(0.60)} Z"
    return (
        f'<defs><linearGradient id="g{uid}" x1="0" y1="1" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{P["dust"]}"/><stop offset="1" stop-color="{P["eggnog"]}"/></linearGradient>'
        f'<clipPath id="c{uid}"><ellipse cx="{cx}" cy="{cy}" rx="{R(0.49)}" ry="{R(0.55)}"/></clipPath></defs>'
        # base (compact pad in perspective)
        f'<path d="{band}" fill="{P["garnet"]}"/>'
        f'<path d="{band_edge}" fill="none" stroke="{P["mustard"]}" stroke-width="{R(0.018)}"/>'
        f'<ellipse cx="{X(0.8)}" cy="{Y(0.36)}" rx="{R(0.74)}" ry="{R(0.21)}" fill="{P["forest"]}" '
        f'stroke="{P["copper"]}" stroke-width="{R(0.021)}"/>'
        f'<ellipse cx="{X(0.8)}" cy="{Y(0.36)}" rx="{R(0.61)}" ry="{R(0.165)}" fill="none" '
        f'stroke="{P["mustard"]}" stroke-width="{R(0.028)}"/>'
        f'<ellipse cx="{X(0.8)}" cy="{Y(0.36)}" rx="{R(0.49)}" ry="{R(0.125)}" fill="{P["eggnog"]}"/>'
        f'<ellipse cx="{X(0.8)}" cy="{Y(0.36)}" rx="{R(0.33)}" ry="{R(0.08)}" fill="none" '
        f'stroke="{P["mustard"]}" stroke-width="{R(0.018)}"/>'
        # hinge
        f'<rect x="{X(0.67)}" y="{Y(0.62)}" width="{R(0.26)}" height="{R(0.12)}" rx="{R(0.02)}" fill="{P["mustard"]}"/>'
        f'<line x1="{X(0.8)}" y1="{Y(0.50)}" x2="{X(0.8)}" y2="{Y(0.62)}" stroke="{P["copper"]}" stroke-width="{R(0.014)}"/>'
        # lid, tilted (TikZ -7 deg = SVG +7 deg because the y axis is flipped)
        f'<g transform="rotate(7 {cx} {cy})">'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{R(0.64)}" ry="{R(0.70)}" fill="{P["forest"]}" '
        f'stroke="{P["copper"]}" stroke-width="{R(0.025)}"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{R(0.545)}" ry="{R(0.605)}" fill="none" '
        f'stroke="{P["mustard"]}" stroke-width="{R(0.056)}"/>'
        f'<g clip-path="url(#c{uid})"><rect x="{X(0.2)}" y="{Y(1.92)}" width="{R(1.2)}" height="{R(1.22)}" fill="url(#g{uid})"/>'
        f'<path d="{stripe1}" fill="{P["eggnog"]}"/><path d="{stripe2}" fill="{P["eggnog"]}"/></g>'
        f'<circle cx="{X(0.88)}" cy="{Y(1.22)}" r="{R(0.21)}" fill="none" stroke="{P["copper"]}" stroke-width="{R(0.019)}"/>'
        f'<path d="{_sparkle(X, Y, 0.88, 1.22, 0.15)}" fill="{P["mustard"]}"/>'
        f'<path d="{_sparkle(X, Y, 0.66, 0.96, 0.065)}" fill="{P["mustard"]}"/>'
        f'<rect x="{X(0.73)}" y="{Y(2.06)}" width="{R(0.14)}" height="{R(0.07)}" fill="{P["mustard"]}"/>'
        f'<circle cx="{X(0.8)}" cy="{Y(2.11)}" r="{R(0.065)}" fill="{P["eggnog"]}" stroke="{P["mustard"]}" '
        f'stroke-width="{R(0.018)}"/>'
        f'</g>')


def logo_html() -> str:
    mark = logo_mark_svg(150, uid='L')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
 html,body{{margin:0;width:1000px;height:640px;overflow:hidden;background:{PAL['eggnog']};
   font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}}
 .card{{position:absolute;inset:28px;border:3px solid {PAL['forest']};outline:1.5px solid {PAL['mustard']};
   outline-offset:-12px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
 svg{{width:240px;height:330px;overflow:visible;filter:drop-shadow(0 10px 18px rgba(30,50,38,.25))}}
 h1{{margin:18px 0 0;font-weight:300;font-size:70px;letter-spacing:.06em;color:{PAL['forest']}}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 p{{margin:6px 0 0;font-size:18px;font-weight:600;letter-spacing:.34em;color:{PAL['dust']}}}
</style></head><body><div class="card">
<svg viewBox="0 0 240 330">{mark}</svg>
<h1>AuraTwin <b>AI</b></h1><p>REFLECT · CALIBRATE · BEAUTIFY</p></div></body></html>"""


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
    mark = logo_mark_svg(62, uid='B')
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
 .logo svg{{width:100px;height:137px;overflow:visible;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35))}}
 .kicker{{font-size:21px;letter-spacing:.28em;color:{PAL['mustard']};direction:ltr;text-align:right;margin-top:8px}}
 h1{{font-family:'Didot','Bodoni MT',Georgia,serif;font-weight:400;font-size:92px;margin:2px 0 0;
   direction:ltr;text-align:right;letter-spacing:.03em}}
 h1 b{{color:{PAL['copper']};font-weight:600}}
 .he{{font-size:31px;font-weight:600;line-height:1.35;margin-top:6px}}
 .swatches{{position:absolute;right:80px;bottom:44px;display:flex;gap:16px;direction:ltr}}
 .sw{{display:flex;flex-direction:column;align-items:center;color:{PAL['eggnog']};font-size:12px;letter-spacing:.12em}}
 .sw span{{width:66px;height:66px;border-radius:33px 33px 4px 4px;border:1.5px solid {PAL['mustard']}}}
</style></head><body><div class="bg"></div>{mesh_svg()}<div class="frame"></div>
<div class="txt"><div class="logo"><svg viewBox="0 0 100 137">{mark}</svg></div>
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
