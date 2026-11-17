"""Find a Venn geometry + label positions so that every label box lies fully inside its required
region with clearance from every circle line (visual-artist skill helper)."""
import itertools, math
import numpy as np

# label: (w, h) in cm, required membership (top, left, right)
LABELS = {
    "TryOnDiffusion": ((1.10, 0.68), (1, 1, 0)),
    "ControlNet+GP-VTON": ((1.45, 0.68), (1, 0, 1)),
    "VITON-HD":       ((1.40, 0.42), (0, 1, 1)),
    "IDM-VTON":       ((1.75, 0.46), (1, 1, 1)),
}


def clearance(cx, cy, w, h, circles, member):
    pts = [(cx + dx * w / 2, cy + dy * h / 2) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    worst = 9.0
    for (ox, oy, r), m in zip(circles, member):
        for x, y in pts:
            d = math.hypot(x - ox, y - oy)
            c = (r - d) if m else (d - r)
            worst = min(worst, c)
    return worst


best = None
for r in (2.3, 2.45, 2.6):
    for a in (1.25, 1.4, 1.55):
        for b in (0.85, 1.0, 1.15):
            top_y = b + 0.1
            circles = [(0, top_y, r), (-a, -b, r), (a, -b, r)]
            pos, total, ok = {}, 9.0, True
            for name, ((w, h), mem) in LABELS.items():
                cand = None
                for x in np.arange(-3, 3.01, 0.05):
                    for y in np.arange(-3.2, 3.01, 0.05):
                        c = clearance(x, y, w, h, circles, mem)
                        if cand is None or c > cand[0]:
                            cand = (c, round(x, 2), round(y, 2))
                pos[name] = cand
                total = min(total, cand[0])
            # the two labels sharing a region must not overlap each other
            if best is None or total > best[0]:
                best = (total, r, a, b, top_y, pos)
print("min clearance %.2f cm  r=%.2f a=%.2f b=%.2f top_y=%.2f" % best[:5])
for k, v in best[5].items():
    print(k, v)
