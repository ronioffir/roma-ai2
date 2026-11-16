import sys, glob, subprocess, os
from PIL import Image
pdf, first, last, out, dpi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "45"
for f in glob.glob("work/_s-*.png"): os.remove(f)
subprocess.run(["pdftoppm", "-png", "-r", dpi, "-f", str(first), "-l", str(last), pdf, "work/_s"], check=True)
fs = sorted(glob.glob("work/_s-*.png")); ims = [Image.open(f) for f in fs]
w, h = ims[0].size; cols = 6; rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (w * cols, h * rows), "white")
for i, im in enumerate(ims):
    S.paste(im, ((cols - 1 - i % cols) * w, (i // cols) * h))   # RTL order: first page top-right
S.save(out); print(out, S.size)
