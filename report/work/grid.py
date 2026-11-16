"""Render PDF pages [first..last] at dpi into an RTL 3x2 grid image (QA visual pass helper)."""
import sys, glob, os, subprocess
from PIL import Image
pdf, first, last, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
dpi = sys.argv[5] if len(sys.argv) > 5 else "62"
for f in glob.glob("work/_g-*.png"):
    os.remove(f)
subprocess.run(["pdftoppm", "-png", "-r", dpi, "-f", str(first), "-l", str(last), pdf, "work/_g"], check=True)
ims = [Image.open(f) for f in sorted(glob.glob("work/_g-*.png"))]
w, h = ims[0].size
cols = 3
rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (w * cols, h * rows), "white")
for i, im in enumerate(ims):
    S.paste(im, ((cols - 1 - i % cols) * w, (i // cols) * h))
S.save(out)
print(out, S.size)
