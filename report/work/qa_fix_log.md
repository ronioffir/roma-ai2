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
