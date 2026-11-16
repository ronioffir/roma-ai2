"""Page-fill helper: for each printed page given, report the lowest inked row of the text block
as % of the text-block height (body page N = PDF page N+4)."""
import sys, subprocess, glob, os
from PIL import Image
pdf = "report.pdf"
for n in sys.argv[1:]:
    p = int(n) + 4
    for f in glob.glob("work/_f-*.png"):
        os.remove(f)
    subprocess.run(["pdftoppm", "-png", "-r", "40", "-f", str(p), "-l", str(p), pdf, "work/_f"], check=True)
    im = Image.open(glob.glob("work/_f-*.png")[0]).convert("L")
    w, h = im.size
    top, bot = int(h * 0.115), int(h * 0.885)     # text block between header and footer
    last = top
    for y in range(top, bot):
        row = [im.getpixel((x, y)) for x in range(int(w * 0.1), int(w * 0.88), 2)]
        if min(row) < 200:
            last = y
    print(f"printed page {n}: filled to {100 * (last - top) / (bot - top):.0f}%")
