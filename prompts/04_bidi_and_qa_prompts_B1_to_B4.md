# 04 — BiDi and QA prompts B1–B4 (+ 7–8), Detector and Fixer loop

Skills: `bidi-qa-detector` ("השוטר שבודק", read-only) and `bidi-qa-fixer` ("השוטר שמתקן").
Detection and fixing are never mixed in one pass (booklet Prompt B2: "Do not fix anything yet").

## Prompt B1 — Hebrew/English rules, before writing
```text
The document is Hebrew RTL with English LTR words. Follow these rules everywhere, including titles, captions,
tables, headers, footers and the cover page:
1. Mark every English word, name and acronym as English: \en{AuraTwin AI}, \en{SMPL-X}, \en{RAG}.
2. Mark a multi-word English phrase as one unit: \en{Latent Diffusion}; long titles that must wrap: \enlong{}.
3. Mark every number, decimal, range, percent, date, currency amount and version as one LTR unit, with its
   symbol and unit: \num{1.0}, \num{10--20}, \num{85\%}, \num{\$2,200}, \num{35 ms}, \num{$\Delta E_{00}\le 1.8$}.
4. Never put Hebrew inside an English-marked unit.
5. Hebrew inside a formula uses \hebmath{}.
6. Every diagram and every code box is built in an English environment (reportfigure, \begin{english}).
   Box frames are LTR, their content is RTL.
7. In tables the first column is on the right (the first column of the colspec) — never reverse by hand.
8. Use only the template's commands (report/COMMANDS.md). Do not invent new ones.
```

## Prompt B2 — BiDi audit of the finished PDF (Detector)
```text
Run: python scripts/qa_detector_audit.py --report-dir report
It extracts the text of report/report.pdf and checks it page by page:
- Hebrew words that start with a final letter (ך ם ן ף ץ);
- reversed English words and acronyms (GAR, MLL, BALEIC …);
- numbers split or reversed: decimals, ranges, currency;
- table of contents: reversed section numbers, left-aligned rows;
- log: lines starting with "!", undefined citations/references, Overfull \hbox > 5pt, missing characters;
- page budget (44 pages; chapters start on 1, 4, 8, 17, 23, 31, 35, 37; references 38);
- bibliography consistency and figure/table references.
Then render every page to an image and look for: diagrams or backgrounds touching the page edge, large gaps
inside a line, mirrored headers and footers, headings at the bottom of a page, split boxes.
Report page number, the exact text, the rule it breaks, and TEMPLATE-LEVEL or ONE-OFF.
Write report/work/qa_audit_report.md. Do not fix anything.
```

## Prompt B3 — Fix in the right place (Fixer)
```text
Read report/work/qa_audit_report.md. For each problem decide first: does it repeat across the document,
or is it one place? If it repeats, check VERSION and CHANGELOG.md and fix it once in base-report.cls
(or auratwin-report.cls if brand-specific), bump the version and add a CHANGELOG line. Do not patch every
occurrence. If it is one place, fix that sentence only in chapters/chX.tex. Never type Hebrew in reverse.
Recompile (lualatex → biber → lualatex → lualatex), run the detector again, and record before/after in
report/work/qa_fix_log.md.
```

## Prompt B4 — A stress test for a new template
```text
Create report/tests/stress_test.tex: one page that mixes Hebrew with English phrases, decimals (1.0), ranges
(10--20), percent (85%), currency ($1,500), a formula with Hebrew, a styled table, a TikZ diagram, a code box and
all four coloured boxes. Compile it and show me the page as an image.
```
Result: passed on template v1.2.0 with 0 errors after five template-level fixes (see `02_…C0_to_C5.md`).

## Prompt 7 — Fix the build / Prompt 8 — Page-by-page review
See `03_chapter_writing_prompts_1_to_8.md`; in this project they run inside the Detector → Fixer loop above.

## How it was used in this project
- Loop: compile → detector → fixer → compile → detector, until the verdict is PASS (0 errors, 0 undefined
  references/citations, no reversed text, page budget met).
- The four visual clues of booklet §14.5 are encoded in the detector: final letter at word start, suspicious
  number, something touching the page edge (Overfull), a large gap inside a line (visual pass).
