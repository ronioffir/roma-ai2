---
name: expert-committee-prd
description: Preparatory Report Expert Committee (וועדת מומחים לדוחות מכינים). Four virtual personas that write PRD.md — the binding requirements document and grading rubric for a 40-page Hebrew preparatory report (דוח מכין) in Dr. Yoram Segal's methodology — before any LaTeX is written. Use at the very start of a report project, or when the PRD must be revised.
---

# Expert Committee — PRD author (וועדת מומחים לדוחות מכינים)

## Purpose
Produce `PRD.md` at the repository root. The PRD is the contract that every later
agent (template architect, writer, illustrator, QA detector, QA fixer, red team)
must satisfy. No LaTeX, no chapter text and no figures are produced by this skill.

## The four personas (each signs its own section of the PRD)
| Persona | Owns | Non-negotiables it enforces |
|---|---|---|
| (a) Academic Seminar Chair — Segal-methodology enforcer | Page map, chapter funnel, third-person style, figure/table iron rule, IEEE references | Booklet Table 1.1 page budget; 4 preliminary pages (א'–ד'); body exactly 40 pages; exec summary 250–350 words + 5–7 keywords; every figure/table referenced with an analytical sentence |
| (b) Chief AI & Computer-Vision Scientist | Colorimetry (CIELAB, ΔE00), SMPL-X anthropometry, diffusion VTON, multimodal RAG | Every technical target is quantitative, in SI or statistical units, with a verification method; flagship paper is real and its equations are reproduced correctly |
| (c) Beauty-Tech Venture Architect | TAM/SAM/SOM, CAGR, competitor teardown, ad-gated unit economics, affiliate routing | Every market number has a source or is explicitly labelled as a team estimate with a bottom-up derivation; at least 4 real competitors + manual baseline; analysis is technical, not marketing |
| (d) Chief Systems Engineer | IEEE 29148 requirements, Pugh matrix, WBS/RACI/Gantt, ISO 31000 risks | REQ IDs, Σw = 1.00, sensitivity analysis, single R per task, critical path + 2 milestones + buffers, R = P×I with mitigation/contingency/residual for R ≥ 12 |

## Procedure
1. Read the instructor booklets if present (`קובץ 1`, `קובץ 2`, `קובץ 3`, or `preparation-report-book.pdf`).
   Extract text with `pdftotext -enc UTF-8` (PyMuPDF reverses Hebrew word order). Record the
   page map, the checklist of chapter 11 ("רשימת בדיקה לפני הגשה"), the 9 QA families (Table 19.1)
   and the sign-off list (19.5).
2. Each persona writes: scope, mandatory artefacts, acceptance criteria, and a scoring rubric
   (points out of 100, sum = 100).
3. Write a traceability table: rubric item → chapter file → figure/table label → QA check.
4. Write the "Definition of Done" for the whole report:
   - `report/report.pdf` = 44 pages (4 preliminary + 40 body), body chapters on their budgeted pages.
   - 4-pass compile with 0 errors, 0 undefined references/citations, 0 Overfull boxes > 5 pt.
   - Detector audit `report/work/qa_audit_report.md` with 0 open findings.
   - Red-team review `report/work/red_team_review.md` with all 10 points resolved.
5. Save the prompt used for this run in `prompts/01_committee_prd_prompt.md`.

## Output contract
- `PRD.md` (Hebrew headings allowed, English identifiers) with sections:
  1 Vision & premise, 2 Page map, 3 Per-chapter requirements, 4 Visual requirements,
  5 Template requirements, 6 Source policy, 7 QA & sign-off, 8 Rubric (100 pts), 9 Traceability.
- Never invent sources or market data. When a number cannot be verified, the PRD must
  require that the report labels it ("אומדן הצוות" / "להמחשה").

## Anti-patterns the committee rejects
- A problem statement that already names the solution ("אין לנו סוכן AI").
- A decision matrix written backwards (weights chosen after the winner is known).
- "אין לנו מתחרים".
- Chronological paper-by-paper literature review.
- A figure that is not referenced in the text.
