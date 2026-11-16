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


---

## Round 3 — readability & math auditor prompts (skill `human-readability-math-auditor`)

### RM-1 — Audit (detects only)
```text
Run scripts/readability_math_audit.py --report-dir report. Check: \onehalfspacing, \parskip >= 6pt,
\arraystretch >= 1.25, box padding; for every numbered equation, that EVERY symbol is defined in Hebrew
right below it ("כאשר ..."); Hebrew inside math only via \hebmath; no space before . , : ; ) and none after (
next to Hebrew; no raw LaTeX in the PDF text. Write report/work/readability_math_audit.md. Do not fix.
```

### RM-2 — Fix (via the fixer rules)
```text
For each equation flagged, add the missing Hebrew definitions in the sentence right below it, without
changing notation. If the definitions push a chapter past its page budget, trim sentences that restate
earlier text, never data. Recompile with the 4-pass build and rerun both the QA detector and RM-1.
```

### Round 3 audit history
- Round 1: auditor bugs (read the local 0 pt \parskip; lost $...$ pairing around escaped \$) — fixed in
  the script; first real run lenient (passed equations with "כאשר" but undefined symbols).
- Round 2 (strict): 6 equations had undefined symbols (q, ℒ, ε_θ, θ, Z, γ, α; ratio-vector symbols defined
  only above) — definitions added in ch3, ch5, ch7.
- Final: readability & math audit **PASS**, QA detector **PASS**, 44 pages.

---

## Red-team examiner prompt (Prompt 9) and resolution log

# 05 — Red Team audit (booklet Prompt 9)

Skill: `.claude/skills/red-team-examiner/SKILL.md` · Output: `report/work/red_team_review.md`.
Run after the Detector verdict is PASS, ideally in a fresh context (booklet §18.10: "open a new conversation,
preferably with another model").

## Prompt 9 — Red team (adapted)
```text
You are a strict examiner on an engineering project committee grading the preparatory report of group roma-ai2
(AuraTwin AI) out of 100, using the rubric in PRD.md §8. Read report/report.pdf (extract with
`pdftotext -enc UTF-8 -layout`) and find its 10 weakest points: vague or untestable requirements, claims without
sources, market numbers without a source or an estimate label, unjustified weights in the decision matrix or a
matrix that looks written backwards, critical risks (R ≥ 12) without mitigation, contingency and residual score,
the same number stated differently in two chapters, a gap that is not one sharp sentence, figures or tables not
referenced in the text, page-budget violations. Do not praise it.
For each point give: #, page, the quoted sentence, the weakness, the required upgrade, severity 1–3.
Give the rubric score before the upgrade.
```

## Upgrade pass
The writer/fixer skills upgrade the chapters point by point; the examiner re-checks each point and marks it
RESOLVED or OPEN with evidence (page + new sentence). Final sign-off only when all 10 are RESOLVED and the
Detector verdict is PASS.

## Resolution log

| # | Page | Weakness | Upgrade applied | Status (examiner re-check) |
|---|---|---|---|---|
| 1 | 5 | H1 / power incoherent | H1a + H1b, Holm; participant unit; mixed model; cluster bootstrap; n = 56 (d = 0.4) → 120, 40 per ITA group | RESOLVED |
| 2 | 4–6 | simulation validity | solution moved out of ch2; P95 CI 4.20–5.48 shown; eye-neutrality assumption stated; FFCC/FC4 planned | PARTIAL |
| 3 | 17 | market untraceable | bottom-up ARPU $0.68, SAM $3.0B, SOM $27.4M (script); TAM declared unused | PARTIAL (inputs = estimates) |
| 4 | 20–21 | unit economics | ad OR affiliate expected value; 2.4× from 58 % margin; self-hosted cost derived; stress case | PARTIAL (inputs = estimates) |
| 5 | 24–25 | matrix asserted | anchored scales; 2 scores corrected (4.45 → 4.30); ±1 score sensitivity, 0 flips | PARTIAL |
| 6 | 27–29 | privacy contradiction | REQ-SEC-11 = 0 stored images, delete ≤ 60 s; text aligned | RESOLVED |
| 7 | 6, 31–33 | work-plan conflicts | 30-person dev sample; ethics, labelling, body validation; float fixed | RESOLVED |
| 8 | 35–36 | risk register | 8 risks (+ALG-07, +OPS-08); evidence per residual; band wording fixed | RESOLVED |
| 9 | 16 | gap statement | one sentence on the eye anchor, scoped to reviewed sources, tied to H1; [41] used correctly | PARTIAL |
| 10 | 5–7 | targets underived | derivation paragraph; IoU 0.90 (0.94 stretch); κ ≥ 0.6; relative ArcFace/LPIPS targets | PARTIAL |

Score: 73/100 before → 83/100 after the examiner's re-check (fresh-context Sonnet examiner). The round-2 new items N1–N6 were then fixed; see `report/work/red_team_review.md`.

<!-- Filled after the red-team pass; full review in report/work/red_team_review.md -->
