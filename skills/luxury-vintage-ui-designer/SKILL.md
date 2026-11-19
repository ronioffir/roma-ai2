---
name: luxury-vintage-ui-designer
description: Luxury editorial art director and LaTeX CLS visual designer. Applies the "Luxury, Vintage, Bold" palette (Egg Nog #FBEDC3, Mustard #CCB363, Dust #6F7D7B, Copper #C27E35, Garnet #76290B, Velvet Forest #1E3226) to the template, boxes, tables, TikZ and pgfplots; designs the AURAM logo (TikZ macro + PNG) and editorial chapter openings and cover. Use for any brand, palette, logo or visual-identity change.
---

# Luxury Vintage UI Designer (מעצב עלית למסמך ולתוסף)

## Palette — the ONLY colours allowed in the document (tints/shades of these are allowed)
| Name | Hex | RGB | Semantic role in the report |
|---|---|---|---|
| Egg Nog | `#FBEDC3` | 251, 237, 195 | soft backgrounds of boxes, cards, zebra rows, logo field |
| Mustard | `#CCB363` | 204, 179, 99 | antique-gold rules and frames, manager box, highlights, chart series |
| Dust | `#6F7D7B` | 111, 125, 123 | sub-headings, key-message bar, system boxes, chart axes, competitors |
| Copper | `#C27E35` | 194, 126, 53 | example boxes, **AURAM / proposed solution** series, milestones path |
| Garnet | `#76290B` | 118, 41, 11 | warnings, critical risks, critical path |
| Velvet Forest | `#1E3226` | 30, 50, 38 | chapter titles, cover, table headers, bold text, milestones |

Source: the team's "Colour palette inspiration — Luxury, Vintage, Bold" board.

## Where the palette is wired (one change recolours everything)
`auratwin-report.cls` defines `brandprimary`=Velvet Forest, `brandsecondary`=Dust, `brandaccent`=Mustard,
`brandtint`=Egg Nog tint, `brandwarn`=Garnet, `brandexample`=Copper, `brandhighlight`=Copper,
`brandgreen`=Velvet Forest tint (milestones), `brandgrey`=Dust tint (competitors), `brandcream`=Egg Nog.
Chapters never use raw colour names (`red`, `blue`, …); the fixer replaces any it finds.

## Logo specification (`\auratwinlogo[scale]` and `report/figures/auratwin_logo.png`)
Three interlocking arch/dome shapes on one baseline, as on the palette card:
1. Egg Nog quarter-arch (top-left rounded) — left;
2. Mustard inverted-U dome (rounded bottom) — centre, overlapping both neighbours;
3. Dust arch (top-right rounded) — right;
plus a minimalist eye/prism line in Velvet Forest across the centre (biometric calibration), and the
word-mark "AURAM" in thin Velvet Forest type. Same geometry in TikZ and in the SVG used for the PNG.

## Editorial rules
- Chapter opening: chapter number in a Velvet Forest badge with Mustard ring; title in Velvet Forest;
  double rule Mustard (thick) + Dust (thin).
- Cover: Egg Nog field, Velvet Forest double frame with Mustard inner rule, logo, banner in the palette.
- Headers: logo mark + short title; footer rule in Mustard.
- Tables: Velvet Forest header, Egg Nog zebra rows; highlighted row = Mustard tint.
- Charts: proposed solution always Copper; flagship Mustard; competitors Dust tints; critical Garnet.

## Output
Updated `.cls` files (version bump + CHANGELOG), logo PNG via `scripts/render_hyperframes_cover.py`,
re-rendered cover banner, entry in `report/work/skills_execution_log.md`.
