# CHANGELOG — AuraTwin AI report template & project

Template = `report/base-report.cls` (base layer) + `report/auratwin-report.cls` (thin company layer).
Version source of truth: `VERSION`. Rule (booklet §15.6): a problem that repeats across the
document is fixed **once** in the template, with a version bump and an entry here.

## [1.2.1] — 2026-11-16 — fixes from the QA detector/fixer loop on the full report
### Fixed (template-level — each finding repeated on ≥ 3 pages or originated in the class)
- **Bibliography exceeded its 3-page budget** (5 pages, QA-034): `\printreferences` now sets the IEEE
  list in `\footnotesize`, single spacing, `\bibitemsep` 1.2 pt.
- **Narrow table columns overflowed** (Overfull \hbox 5–9 pt in 4 tables): `\tabcolsep` 6 pt → 4 pt
  inside `reporttable` / `reporttable*`; both environments gained an optional font-size argument
  (`\begin{reporttable}[\footnotesize]{…}`).
- **TOC and lists spilled to 2 pages each** (preliminary pages = 6 instead of 4): `\compacttoc`
  in `\footnotesize`; `\compactlists` in `\scriptsize`; inter-chapter `\addvspace` suppressed in both.
- TOC subsection entries were larger than section entries (leftover `\small`) — removed.
- `abbrevtable`: `\en` is mapped to the breakable `\enlong` inside the 2-column list.
### Added
- `\compacttoc`, `\compactlists{…}`, `abbrevtable` + `\abbr{…}{…}` (preliminary pages ג׳–ד׳).
### Text-level (one-off) fixes, logged in `report/work/qa_fix_log.md`
- Long boxed English phrases → `\enlong` (25 occurrences, script `report/work/enlong_convert.py`).
- RTL arrow direction in the critical-path sentence (`\to` → `\leftarrow`), table column widths,
  equation split (eq. 5.4/5.5), floating table 7.2 pinned, Ch.3–6 page budgets.

## [1.2.0] — 2026-11-16 — fixes from the Prompt B4 stress test
### Fixed (template-level)
- **`\en` is now boxed** (`\mbox{\textenglish{…}}`). With an unboxed `\textenglish`, the comma typed
  after one English unit was rendered next to the *following* unit (`RAG, SMPL-X` → `SMPL-XRAG`).
  Reproduced in `report/tests/bidi_comma_test.tex` (variant ג is the fix). Added `\enlong{}` as the
  unboxed, line-breakable variant for long English titles.
- English fonts get `Ligatures=TeX`, so `\num{10--20}` prints an en dash instead of `--`.
- `tabularx` inside `reporttable`: the float/center are now opened in command form
  (`\table`/`\center`) so `tabularx` finds `\end{reporttable}` (was: "File ended while scanning
  use of \TX@get@body").
- `keymessagebox` / `warningbox` titles were set in the (white) title colour and were invisible;
  the title is now printed in the accent colour at the start of the box text.
- Footer "עמוד N מתוך M": M used `\ref` (gave a section number) — now `\pageref*` to the body-end label.

## [1.1.0] — 2026-11-16 — stages 4–6 (booklet Table 15.2)
### Added
- Styled tables `reporttable` / `reporttable*` (header row `\headrow` + `\hc{}`, zebra rows,
  width 12.4 cm, first column on the right natively), matrix cell marks `\cellok` `\cellpartial` `\cellno`.
- Four boxes: `managerbox`, `keymessagebox`, `warningbox`, `examplebox` (never split) + `codebox`.
- `reportfigure` / `reportfigure*` wrappers (English LTR environment, caption below).
- Header/footer with per-slot direction; "page N of M" right-to-left.
- biblatex + biber IEEE, `\printreferences` (English LTR list under a Hebrew heading).
- Company layer `auratwin-report.cls`: palette, TikZ logo, document fields (`\doctitlehe` …),
  document types (`report`/`proposal`/`spec`), double-frame cover page, © in the English font,
  year taken from the compile date.

## [1.0.0] — 2026-11-16 — stages 1–3
### Added
- LuaLaTeX + polyglossia (Hebrew default, English other), fonts checked with `fc-list :lang=he`
  (David / Arial / Times New Roman / Consolas).
- Geometry 2.5 cm all sides + 0.5 cm binding gutter (right edge, RTL), 12 pt, 1.5 line spacing.
- BiDi units `\en`, `\num`, `\hebmath`, `\heb`, `\copyrightsign`; generated numbers
  (sections, figures, tables, equations) forced LTR so 1.2 never shows as 2.1.
- Chapter-based numbering, TOC depth 3, `\needspace` before every section/subsection,
  every chapter on a new page, Hebrew-letter preliminary page numbers (א׳–ד׳).

---
## Project log
- 2026-11-16 — Skills (9), PRD, prompts log, template v1.2.0, stress test passed (0 errors).
- 2026-11-16 — Full report (8 chapters). The QA detector/fixer loop converged in 6 rounds and the template moved to v1.2.1.
- 2026-11-16 — Red-team pass 1 (fresh context, Sonnet) scored **73/100** with 10 weaknesses. The upgrade pass changed:
  - **Statistics:** H1a/H1b with Holm correction, cluster bootstrap, and a power analysis taken from the simulation.
  - **Decision matrix:** anchored Pugh scales and score sensitivity. The totals are now 4.30 / 3.40 / 2.85.
  - **Economics:** the gate is modelled as ad *or* affiliate; the commercial API vs self-hosted distilled costs are separated;
    and the market is built bottom-up (SAM ≈ $3.0B, SOM ≈ $27.4M).
  - **Privacy:** contradiction fixed (REQ-SEC-11).
  - **Work plan:** ethics, labelling and validation tasks added; dependencies and float fixed.
  - **Risks:** 2 new risks, and each residual is now tied to evidence.
  - **Gap statement:** sharpened.
- 2026-11-16 — Red-team re-check: **83/100**, with 4 points resolved, 6 partial and 0 open. The 6 new items N1–N6 were fixed.
  Detector verdict **PASS**: 44 pages, 0 errors, 0 undefined references, 0 overfull > 5 pt.
