---
name: cls-template-architect
description: Builds and versions the two-layer LuaLaTeX class architecture for Hebrew/English reports — base-report.cls (languages, fonts, BiDi macros, tables, 4 box types, headers/footers, needspace) and the thin company layer auratwin-report.cls (brand palette, logo, document fields) — plus PROMPT.md, COMMANDS.md, VERSION and CHANGELOG.md. Use when creating, extending or upgrading the report template.
---

# CLS Template Architect (אדריכל תבנית הלטך ושכבת החברה)

Follows booklet chapter 15 (Prompts C0–C5) and chapter 14 (Prompt B1).

## Architecture
```
report/base-report.cls      # the factory: languages, fonts, BiDi, structure, tables, boxes, page style
report/auratwin-report.cls  # thin layer: \LoadClass{base-report}; palette, logo, fields, cover
report/PROMPT.md            # rules for any model writing a new document with this template
report/COMMANDS.md          # every public command, one line each
CHANGELOG.md / VERSION      # version from day one; every template fix bumps it
```
The company layer NEVER copies or edits the base class. One source, one version.

## Build in six stages (Table 15.2) — compile and look at a page image after each
1. Skeleton: `report` class, 12pt, A4, `geometry` 2.5 cm + 0.5 cm binding, `\onehalfspacing`,
   `polyglossia` (`\setdefaultlanguage{hebrew}`, `\setotherlanguage{english}`), `fontspec`.
   Run `fc-list :lang=he` first; choose fonts that exist (here: David / Arial / Times New Roman).
2. BiDi commands: `\en{}` (LTR English unit), `\num{}` (LTR number/range/currency/percent unit),
   `\hebmath{}` (Hebrew inside math), `\copyrightsign` (© in the English font).
3. Structure: chapters/sections/subsections with `\needspace`, chapter-based numbering,
   TOC depth 3, LoF, LoT, Hebrew-letter preliminary page numbers (א'–ד').
4. Tables (`tabularx` + `booktabs` + `colortbl`, header colour, zebra rows, width ≤ 12.4 cm,
   first column on the right — never reversed manually), four `tcolorbox` types
   (`managerbox`, `keymessagebox`, `warningbox`, `examplebox`; `breakable=false`),
   safe figure wrapper (`english` environment, ≤ 12.4 cm).
5. Cover page (double frame, no page number), header/footer with direction fixed in every slot,
   "page N of M" read right-to-left.
6. `biblatex` + `biber` IEEE style, COMMANDS.md, PROMPT.md, a full example, CHANGELOG entry.

## Stress test (Prompt B4)
`report/tests/stress_test.tex` — one page mixing Hebrew, English phrases, 1.0, 10--20, 85%,
\$1,500, a formula with Hebrew, a table, a TikZ diagram, a code box and all four boxes.
It must compile with 0 errors and be inspected as a PNG before chapters are written.

## Rules
- One purpose per command. No Hebrew inside an English unit.
- Name conflicts: do not load `siunitx` (the template owns `\num`).
- Every fix that repeats across the document goes here, with a version bump and a CHANGELOG line.
