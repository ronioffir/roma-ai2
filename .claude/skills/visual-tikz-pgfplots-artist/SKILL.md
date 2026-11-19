---
name: visual-tikz-pgfplots-artist
description: Builds every figure of the report — TikZ diagrams (funnel, problem chain, Venn, concentric TAM/SAM/SOM, architecture/data flow, WBS tree, 14-week Gantt, 5×5 risk heatmap, post-approval actions) and pgfplots charts (radar, log-scale scatter, stacked horizontal bars, sensitivity lines) — BiDi-safe and ≤ 12.4 cm wide; also renders HTML/CSS "HyperFrames-style" cards to PNG for the cover and README. Use whenever a figure is created or repaired.
---

# Visual Artist — TikZ, pgfplots, HyperFrames (מאייר)

Implements booklet chapter 16 and Prompt 5 ("A fancy figure").

## Choosing the tool (Fig. 16.1)
- Process or structure → TikZ. Numeric data → pgfplots. Showcase visual → HTML/CSS card rendered to PNG.

## Safety rules (never break)
1. Every `tikzpicture` sits inside `\begin{english} ... \end{english}` (the template's `\safefigure`
   wrapper does this). Coordinates are therefore LTR and never mirrored.
2. Hebrew labels are wrapped in `\texthebrew{...}` (template shortcut `\heb{...}`).
3. Width ≤ 12.4 cm: `\resizebox` is a last resort; prefer explicit coordinates / `width=12cm` axes.
4. No overlapping labels; legend outside the data area; consistent colour semantics across the report:
   brand teal = AURAM / proposed, amber = flagship paper, grey = competitors, red = critical, green = milestone.
5. Caption BELOW the figure, in Hebrew, says what the reader sees; `\label{fig:...}`.
6. Data plots read their numbers from `report/figures/data/*.csv` produced by
   `scripts/generate_beauty_benchmarks.py`; simulated data are labelled "(נתונים מדומים)".

## HyperFrames-style raster assets
`scripts/render_hyperframes_cover.py` writes HTML cards and renders them with headless Edge/Chrome
(`--headless --screenshot --window-size=...`) to `report/figures/cover_banner.png` and README cards.
Every important number shown in an image is repeated in a table or the text (images are not searchable).

## Deliverable check
After compiling, render the page with the figure (`pdftoppm -r 110`) and inspect it: no clipping at the
margin, no mirrored axis, readable 8 pt minimum, labels not colliding.
