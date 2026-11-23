# QA fix log — bidi-qa-fixer ("השוטר שמתקן")

Input for every round: `report/work/qa_audit_report.md` written by `bidi-qa-detector`
(`scripts/qa_detector_audit.py`). Rule (booklet Fig. 14.3 / §15.6): repeating → template (+version);
one-off → chapter file. After every round: `lualatex → biber → lualatex → lualatex`, then detector again.

| Round | Detector verdict | Findings | Main actions |
|---|---|---|---|
| 0 (fork, draft 19 pp.) | FAIL | 72 | chapters not yet written — baseline only |
| 1 (all chapters, 40 pp.) | FAIL | 35 | see R1 |
| 2 (47 pp.) | FAIL | 69 | see R2 (one LaTeX error introduced by a shell heredoc) |
| 3 (46 pp.) | FAIL | 24 | see R3 |
| 4 (44 pp.) | FAIL | 18 → 7 | see R4 (detector precision fixes) |
| 5 (44 pp.) | FAIL | 3 | only README / skills mirror (repository tasks, not report defects) |

## R1 — 40 pages, chapters 3–6 short, references 5 pages
| Finding | Class | Fix | Where |
|---|---|---|---|
| QA-029..033 chapter start pages early (ch4 p.15 … ch8 p.31) | TEMPLATE-LEVEL (pagination) | content added where the booklet budget required it: Ch.3 ΔE00 equation, method/limitation table, critical synthesis, take/change/add table; Ch.4 barriers & segments; Ch.5 feasibility screen, interfaces, privacy-by-design, value table; Ch.6 control & KPIs | chapters/ch3–ch6 |
| QA-034 references 5 pages | TEMPLATE-LEVEL | `\printreferences` footnotesize, single spacing | base-report.cls v1.2.1 |
| QA-032 Overfull 38.6 pt (eq. score) | ONE-OFF | split into eq. 5.4 and 5.5 | ch5_alternatives.tex |

## R2 — "Misplaced \noalign" at ch4:171
| Finding | Class | Fix |
|---|---|---|
| `!` error, table rows ending with `\` instead of `\\` | ONE-OFF (tooling) | text appended via a Bash heredoc had `\\` collapsed; repaired with `work/fix_rowends.py` (ch4: 5 rows, ch6: 7 rows). Lesson: never write LaTeX through heredocs in this shell. |

## R3 — overflow in tables and boxed English phrases
| Finding | Class | Fix | Where |
|---|---|---|---|
| Overfull 5–9 pt in 4 tables | TEMPLATE-LEVEL | `\tabcolsep` 4 pt | base-report.cls |
| Overfull from long `\en{…}` phrases (e.g. "(Maximum a Posteriori)", "Work Breakdown Structure") | ONE-OFF ×25 | → `\enlong{…}` (`work/enlong_convert.py`, skips phrases followed by `, \en{` to keep the v1.2.0 comma fix) | ch2–ch6 |
| preliminary pages 6 instead of 4 | TEMPLATE-LEVEL | `\compacttoc` footnotesize; `\compactlists` scriptsize; no inter-chapter gaps | base-report.cls |
| abbreviation expansions wrapping across columns | ONE-OFF | Hebrew-only definitions (`work/strip_abbr_en.py`) | coverpage.tex |

## R4 — visual pass (page-by-page renders at 62 dpi, `work/grid.py`)
| Page (printed) | Finding | Class | Fix |
|---|---|---|---|
| 7 | requirements table: ID column clipped ("EQ-BOD-03"), half-empty page | ONE-OFF | ID column 2.3 cm, table `\small`, target `P@5` |
| 21 | "(יחס 2.41" — parenthesis wrapped to the wrong side | ONE-OFF | "; יחס 2.41" |
| 20 | scatter labels ModiFace/YouCam touching | ONE-OFF | labels anchored west |
| 27 | architecture lane labels hidden behind nodes | ONE-OFF | labels moved to the right edge, partner row lowered |
| 30 | last page of Ch.5 ~30 % full | ONE-OFF | design-decision log (ADR table 5.8) |
| 32 | critical-path arrows pointed backwards in RTL (`\to`) | ONE-OFF | `\leftarrow` |
| 36 | table 7.2 floated alone onto a page | ONE-OFF | `reporttable*` + ISO 31000 monitoring table 7.3 |
| ג׳ | TOC subsection entries larger than sections | TEMPLATE-LEVEL | `titlecontents{subsection}` font removed |

### Detector precision (the detector script itself, not the report)
- NUM-REV false positives (10): "5.4", "7.1" are LaTeX-generated section/table/equation numbers whose
  mirrors ("4.5 s", "1.7") also occur in the source. The detector now whitelists numbers from the
  `\newlabel` entries of `report.aux`.
- COVER-FIELD false positive: Times New Roman's hyphen is extracted as U+00AD (soft hyphen); the
  detector normalises it to "-" before matching ("roma-ai2", "REQ-VIS-01").

## Final state (round 5)
44 pages (4 + 40), 0 `!` errors, 0 undefined references/citations, 0 Overfull boxes > 5 pt,
all 8 chapters + references start on their budgeted pages (1, 4, 8, 17, 23, 31, 35, 37, 38),
46/46 bibliography entries cited.

---

## Round 3 — rejects prompt: identity, UX and readability (template v1.3.0)

| Finding (detector / auditor / visual) | Class | Fix | Where |
|---|---|---|---|
| Body grew 40 → 42 pages after parskip 6 pt / arraystretch 1.25 | TEMPLATE-LEVEL | body 11.5 pt (booklet range 11–12 pt), 1.5 spacing kept | base-report.cls |
| Cover: wordmark overlapped the institution line | TEMPLATE-LEVEL | wordmark moved into the overlay; `\par` after the overlay so `\vspace*` applies first | auratwin-report.cls |
| `\textcolor` in chapter figures ("manual formatting") | TEMPLATE-LEVEL (new commands) | `\accenttext` / `\mutedtext` in the base class; chapters converted | base-report.cls, ch4, ch5 |
| Detector expected 9 skills | tooling | expects 12 | scripts/qa_detector_audit.py |
| Mixed Hebrew/English labels in the mockup in the wrong order | ONE-OFF ×5 | one `\heb{}` unit with `\en`/`\num` inside | ch5 Fig. 5.5 |
| Journey figure too small; REQ labels overflowing the boxes | ONE-OFF | boxes widened to 12.4 cm total; REQ labels `\tiny` | ch4 Fig. 4.4 |
| 7 equations with undefined symbols (strict auditor) | ONE-OFF | Hebrew "כאשר …" definitions added | ch3, ch5, ch7 |
| Ch.3 and Ch.5 one page over budget after the definitions and UX content | ONE-OFF | redundant sentences trimmed; feasibility table condensed to a paragraph | ch3, ch5 |
| A build pass hung once; killing it truncated the aux files | tooling | per-pass `timeout 300` in build.sh; clean rebuild | report/build.sh |

Final: QA detector **PASS** (0 findings), readability & math audit **PASS**, 44 pages, 0 errors.

---

## Round 4 — design corrections (user prompt 06, template v1.4.0)

| Page | Finding (user + visual pass) | Fix | Verification |
|---|---|---|---|
| 1 | seminar wording in the course line | removed from `\doccourse` | cover render |
| 1 | logo lacked a trust/security cue; colour names under swatches | Shield-Eye logo (TikZ + PNG); swatch labels removed | cover + banner renders |
| 5 | arrow and its labels overlapped the funnel; layer texts too long | arrow outside the funnel, labels above and below it; shorter texts, compact layers | crop render |
| 17 | Venn labels crossing circle lines; similar hues | distinct hues, outside pills; label positions from `venn_layout.py` (≥ 0.16 cm clearance) | crop render |
| 21 | TAM/SAM/SOM text over circles | leader-line label column, short tags only inside | page render |
| 34 | mockup looked raw | modern UI styling; header/CTA/shade-card overflows fixed; halter-top silhouette | crop renders (3 iterations) |
| 39 | pale fills, small numbers, labels covering scores | solid fills, larger type, taller cells, labels below scores | crop renders (3 iterations) |
| build | `shadows.blur` triggered a silent MiKTeX package install, so passes hung | library removed; shadows drawn with standard TikZ | clean 4-pass build |

Final: QA detector **PASS**, readability & math audit **PASS**, 44 pages, 0 errors.

---

## Round 5: pocket-mirror logo, red-team polish, Assignment 01 feedback (template v2.0)

| Finding | Level | Fix | Verification |
|---|---|---|---|
| 67 LaTeX warnings (hyperref tokens, font sizes, hypcap, biblatex) | template | fix-cm, `\pdfstringdefDisableCommands`, `hypcap=false`, biblatex alias and mapping | log: 0 warnings |
| Tables cramped and plain | template | arraystretch 1.35, Mustard rules, Egg Nog header text and zebra | page renders |
| Orphaned "3.10" heading + half-blank page | template | `\if@nobreak` guard on the automatic `\needspace` (found with `\tracingpages`) | Ch. 3 back to 9 pages |
| Global `\needspace` rewrite | template, tried | reverted: broke Ch. 4 float placement (47 pages) | rebuild |
| Ch. 2 / Ch. 5 closing boxes spilled to a new page after the statistics additions | one-off | removed two boxes that duplicated adjacent text; trimmed restating sentences | 44 pages |
| Table 4.1 + ARPU paragraph: dangling × (BiDi) | one-off | product chains as single `\en{}` units | page render |
| Eq. 2.1 ".vs" | one-off | `\mathrm{vs.}` | 150 dpi crop |
| Tables 2.2 / 3.2 / 3.3 / 6.4 wraps | one-off | column widths; `\cellno` empty | page renders |
| Table 5.5 label wraps "(שלוש תמונות)" | one-off, **accepted** | shortening it moved Ch. 5's breaks to 45 pages; restored | open (minor) |

Final: **44 pages**, 0 errors, **0 warnings**, QA detector PASS, readability & math PASS, `statistical_validation.py --check` PASS.

---

## Round 6: AURAM, prompt 08 (template v3.0)

| Finding | Level | Fix | Verification |
|---|---|---|---|
| 48 pages after the content upgrade | one-off | trims of duplicated prose (Ch.1, 3, 4, 5); latency table → one sentence with the same numbers; roadmap moved to Ch.6 §6.5 (Ch.6 had 9 cm free) | 44 pages, starts on budget |
| §1.5 and §3.9 headings pushed to a new page with 17–40% free | one-off | `\@nobreaktrue` before those two headings | page renders |
| Overfull 16.8 pt in Table 4.3, 7.1 pt in §3.10.5 | one-off | unbreakable `\en{}` chains split; script name in `\enlong` | detector PASS |
| eq. 2.1: R, G, B undefined | one-off | defined in the "כאשר" sentence | readability PASS |
| eq. 4.1 too wide (number pushed down) | one-off | third line in `gathered` | 90 dpi crop |
| `--check`: "1.30" missing | data format | illuminant CSV written with two decimals; table updated | NUMBER CHECK PASS |
| Mockup CTA text cramped | one-off | shorter text | 120 dpi crop |
| Build killed by the OS (low memory) | environment | passes run one per call in the foreground; aux files cleaned | rebuild |

Final: **44 pages**, 0 errors, **0 warnings**, QA detector PASS, readability & math PASS (19 equations), number check PASS.

---

## Round 7: Pass 1 completeness (prompt 09)

| Finding | Fix | Verification |
|---|---|---|
| Edge-case table pushed Ch.7 to 3 pages | 5 single-line rows, intro folded into one sentence | 44 pages |

Final: 44 pages, 0 errors, 0 warnings, detector PASS, readability PASS, number check PASS.
