# PRD — AuraTwin AI Preparatory Report (דוח מכין)

**Document:** Product Requirements Document & grading rubric for the 40-page preparatory report
**Group:** `roma-ai2` · **Authors:** רוני אופיר, מעיין שירי (החוג לסטטיסטיקה, אוניברסיטת חיפה) · **Advisor:** ד"ר יורם סגל
**Produced by:** skill `expert-committee-prd` (Preparatory Report Expert Committee), before any LaTeX was written
**Template:** `report/base-report.cls` + `report/auratwin-report.cls`, v1.2.0 · **Date:** 2026-11-16

---

## 0. The committee

| Persona | Signs section(s) | Role |
|---|---|---|
| (a) Academic Seminar Chair — Segal-methodology enforcer | 1, 2, 3, 7 | Page map, funnel structure, style, iron rule of figures/tables, IEEE references |
| (b) Chief AI & Computer-Vision Scientist | 3, 4, 6 | CIELAB ΔE00 calibration, SMPL-X anthropometry, diffusion VTON, multimodal RAG, flagship-paper maths |
| (c) Beauty-Tech Venture Architect | 3 (ch. 4), 6 | TAM/SAM/SOM, competitors, ad-gated unit economics, affiliate routing |
| (d) Chief Systems Engineer | 3 (ch. 2, 5–7), 5, 8, 9 | IEEE 29148 requirements, Pugh matrix, WBS/RACI/Gantt, ISO 31000 risk |

---

## 1. Vision & premise (Chair)

The preparatory report is **an engineering and research contract** between the students and the advisor, written
*before* development resources are spent (booklet §1.1). It does not ship the mobile app. It proves that:
1. the problem is real and quantified;
2. the solution is feasible, grounded in peer-reviewed literature and a flagship paper;
3. there is a binding plan (WBS, RACI, 14-week Gantt) and a risk plan.

Scope of the imagined product: **AuraTwin AI** — a multimodal agentic system that calibrates a selfie's colour using
the user's own eye (sclera + self-reported iris colour) as a biometric anchor, estimates body measurements
(SMPL-X), recommends beauty/fashion SKUs through a social-trend RAG engine, and gates the expensive diffusion
virtual try-on behind a rewarded-ad / affiliate business model.

The industrial partner (L'Oréal-ModiFace & Zara Inditex Tech Lab) is **simulated for the report** and must be
labelled as simulated wherever it appears (cover page, ch. 1).

---

## 2. Page map (Chair) — booklet Table 1.1

| Part | Printed pages | Budget | File |
|---|---|---|---|
| Cover (no visible number) | א׳ | 1 | `report/coverpage.tex` |
| Executive summary (250–350 words) + 5–7 keywords | ב׳ | 1 | `report/coverpage.tex` |
| Table of contents (depth 3) | ג׳ | 1 | `report/coverpage.tex` |
| Lists of figures/tables + abbreviations | ד׳ | 1 | `report/coverpage.tex` |
| Ch. 1 Introduction & background | 1–3 | 3 | `chapters/ch1_intro.tex` |
| Ch. 2 Problem, research question, goals | 4–7 | 4 | `chapters/ch2_problem.tex` |
| Ch. 3 Literature review & flagship paper | 8–16 | 9 | `chapters/ch3_literature.tex` |
| Ch. 4 Market & existing products | 17–22 | 6 | `chapters/ch4_market.tex` |
| Ch. 5 Design alternatives, selection, innovation | 23–30 | 8 | `chapters/ch5_alternatives.tex` |
| Ch. 6 Work plan: WBS, RACI, Gantt | 31–34 | 4 | `chapters/ch6_workplan.tex` |
| Ch. 7 Risk analysis & mitigation | 35–36 | 2 | `chapters/ch7_risks.tex` |
| Ch. 8 Summary: ready for implementation | 37 | 1 | `chapters/ch8_summary.tex` |
| References (IEEE, biber) | 38–40 | 3 | `references.bib` |
| **Total PDF** | **44 pages** | 4 + 40 | `report/report.pdf` |

---

## 3. Per-chapter requirements

### Ch. 1 — מבוא ורקע (Chair)
- Funnel structure (Fig. 1.1): macro trends → applied context (simulated partner lab) → engineering/economic motivation → report roadmap.
- No cliché opening without a number in the same sentence.
- Motivation explains why static size charts, quiz filters and plain AR overlays fail.

### Ch. 2 — הגדרת הבעיה (Systems Engineer + CV Scientist)
- Problem stated in numbers, current vs desired, **without naming the solution**.
- Problem numbers come from the computed calibration simulation (`scripts/generate_beauty_benchmarks.py`, n = 4000 synthetic selfies, CIEDE2000 on skin):

| Method | Mean ΔE00 | Median | P95 | % ≤ 2.0 |
|---|---|---|---|---|
| Uncorrected camera | 4.89 | — | 8.89 | — |
| Gray-world AWB | 9.77 | — | — | 0.0 |
| Sclera anchor | 2.82 | — | — | — |
| Sclera + iris prior | 2.74 | — | — | — |
| Enrolment + iris prior (AuraTwin) | 1.82 | 1.37 | 4.81 | 69.6 |

- Research question + falsifiable hypothesis vs SMART design goals (Table 2.1, after booklet Table 4.1).
- Requirements table (Table 2.2): ID `REQ-xxx-nn`, requirement, class (functional / constraint / performance / security), quantitative target in SI or statistical units, verification method. Mandatory rows include:
  - **REQ-VIS-01**: median ΔE00 ≤ 1.8 **and** P95 ≤ 4.5 on skin (the simulation meets the median but not yet the P95; this gap is stated openly as the research question).
  - body circumference MAE ≤ 1.2 cm; nail/hand IoU ≥ 0.94; recommendation latency ≤ 1.8 s; VTON latency ≤ 4.5 s; ArcFace cosine ≥ 0.88; trend freshness ≤ 6 h; sponsored Precision@5 ≥ 0.85; ARPU > 2.4 × GPU cost; GDPR biometric compliance.

### Ch. 3 — סקירת ספרות (CV Scientist + Chair)
- Thematic and critical, never chronological: 4 pillars (colour constancy & biometric anchors; 3D body/hand reconstruction; diffusion VTON; multimodal RAG & trend mining).
- Literature matrix (Table 3.1): rows = papers, 6 theme columns, final row "הפרויקט המוצע: AuraTwin AI — זה הפער".
- Flagship paper chosen through a Venn diagram (Fig. 3.1: high-ranked venue ∩ closeness to problem ∩ replicability): TryOnDiffusion (CVPR 2023), with IDM-VTON (ECCV 2024) as the alternate.
- Governing equations of the flagship, its experimental setting, its limits, and a **one-sentence gap**.

### Ch. 4 — חקר שוק (Venture Architect)
- TAM / SAM / SOM concentric diagram (Fig. 4.1) with a bottom-up SOM derivation. All market figures are labelled **"אומדן הצוות"** (team estimate).
- Technical teardown of ModiFace, Perfect Corp (YouCam), Zeekit/Walmart, Stitch Fix + manual baseline + flagship + AuraTwin (Table 4.1, 8 metrics).
- Radar chart (Fig. 4.2, 6 axes) and log-scale scatter (Fig. 4.3), both pgfplots from CSVs, captions marked "(הערכת הצוות)".

### Ch. 5 — חלופות תכן (Systems Engineer)
- Three fundamentally different alternatives (Table 5.1): Alt1 On-device Edge; Alt2 Monolithic Cloud LLM + diffusion; Alt3 Hybrid split-compute + agentic RAG + ad-gated cloud VTON.
- Weighted decision matrix, Eq. $S_j=\sum_i w_i c_{ij}$, $\sum w_i = 1.00$, integer scores 1–5, Table 5.2 with raw (weighted) cells.
- **Weights and integer scores were frozen in this PRD before the totals were computed** (anti "matrix written backwards"):

| Criterion | Weight | Alt1 Edge | Alt2 Cloud LLM | Alt3 Hybrid |
|---|---|---|---|---|
| Personalisation accuracy | 0.25 | 3 | 3 | 5 |
| Unit cost | 0.20 | 5 | 2 | 4 |
| Latency | 0.15 | 2 | 1 | 5 |
| Photorealism | 0.15 | 1 | 5 | 5 |
| Biometric privacy | 0.15 | 5 | 2 | 4 |
| Development effort | 0.10 | 2 | 5 | 3 |
| **Total $S_j$** | **1.00** | **3.15** | **2.85** | **4.45** |

- Sensitivity analysis: one-at-a-time ±0.05/±0.10 perturbation, the booklet's extreme check (latency 0.45, cost 0.00), Dirichlet Monte-Carlo. Stacked horizontal bar chart (Fig. 5.1).
- Full architecture & data-flow TikZ diagram (Fig. 5.2) + innovation section.
- Unit economics of the ad gate: revenue per gated generation **$0.1086** = 2.41× a $0.045 GPU generation but only 1.21× a $0.090 one — so the requirement ARPU > 2.4 × GPU forces the low-cost inference tier (feeds risk RSK-BIZ-04).

> **PRD revision v1.1 (2026-11-16, after the red-team review, `report/work/red_team_review.md`).**
> The **weights above are unchanged**. Anchored 1–5 scoring scales were added (report Table 5.4), and two
> scores that did not match their anchor were corrected: Alt1 accuracy 3 → 4 (it runs the eye-anchored
> calibration on-device) and Alt3 latency 5 → 4 (the try-on path sits exactly at the 4.5 s limit).
> New totals: **Alt3 4.30 · Alt1 3.40 · Alt2 2.85**. The ranking did not change, and a ±1 score-sensitivity test
> was added: 0 flips in 28 changes.
> Unit economics corrected: the gate is ad **or** affiliate (expected value with q = 0.5), so
> r̄ = $0.054. That is 0.60–1.21× a commercial try-on API (status quo) and **10.2×** a self-hosted
> distilled model ($0.0053). The 2.4× threshold now derives from a 58 % gross-margin target.
> Market corrected to a traceable bottom-up build: ARPU $0.68/month, SAM ≈ $3.0B, SOM ≈ $27.4M.
> Other changes: REQ-HND-04 target 0.90 (0.94 stretch); REQ-SEC-11 = no stored images, ephemeral ≤ 60 s;
> H1 split into H1a (paired improvement) and H1b (median < 1.8), with Holm correction, participant-level
> analysis and cluster bootstrap; 2 new risks (RSK-ALG-07, RSK-OPS-08).

### Ch. 6 — תוכנית עבודה (Systems Engineer)
- WBS tree (Fig. 6.1) + Table 6.1 with WP 1.0–5.0, sub-tasks, deliverables.
- RACI (Table 6.2): exactly one **R** per sub-task (רוני אופיר / מעיין שירי), ד"ר יורם סגל = **A**.
- 14-week Gantt (Fig. 6.2) + Table 6.3 (TSK-1.1 … TSK-5.2): critical path in red, milestones in green at weeks 8 and 12, a one-week buffer before each milestone.

### Ch. 7 — סיכונים (Systems Engineer)
- $R = P \times I$, $P, I \in [1,5]$; 5×5 heatmap (Fig. 7.1) with $R \ge 12$ in red.
- Table 7.1: six risks RSK-ALG-01, RSK-GEN-02, RSK-DAT-03, RSK-BIZ-04, RSK-SEC-05, RSK-OPS-06.
- Table 7.2: mitigation, contingency and $R_{\text{residual}}$ for every risk with $R \ge 12$.

### Ch. 8 — סיכום (Chair)
- One page: need, scientific proof, techno-economic viability, decision, readiness; Fig. 8.1 with the three post-approval actions (configuration freeze & data permissions → Git + CI/CD in `roma-ai2` → semester-B kick-off).

---

## 4. Visual requirements (CV Scientist + Chair)
- Every TikZ/pgfplots figure inside the template's LTR wrapper, Hebrew labels in `\heb{}`, width ≤ 12.4 cm.
- Captions: table above, figure below; every figure and table referenced in the text with an analytical sentence.
- Colour semantics are fixed across the report: teal = AuraTwin/proposed, amber = flagship, grey = competitors, red = critical, green = milestone.
- Data plots read `report/figures/data/*.csv` generated by `scripts/generate_beauty_benchmarks.py`. Simulated/estimated data are labelled.
- Cover image `report/figures/cover_banner.png` rendered from HTML by `scripts/render_hyperframes_cover.py`.

## 5. Template requirements (Systems Engineer)
- Two layers: `base-report.cls` (factory) + `auratwin-report.cls` (thin brand layer). The layer never edits the base.
- LuaLaTeX + polyglossia + fontspec; David/Arial/Times New Roman (checked with `fc-list :lang=he`).
- 12 pt, 1.5 spacing, justified, 2.5 cm margins + 0.5 cm binding gutter.
- BiDi units `\en`, `\num`, `\hebmath`, `\heb`, `\copyrightsign`; four boxes (manager, key message, warning, example) that never split; `\needspace` before every section.
- One-page stress test (Prompt B4) passes with 0 errors before chapters are written — **passed on v1.2.0**.
- VERSION, CHANGELOG.md, PROMPT.md, COMMANDS.md maintained.

## 6. Source policy (CV Scientist + Venture Architect)
- No invented papers, authors, venues, page ranges or DOIs. Uncertain fields are omitted; uncertain papers are dropped.
- ≥ 30 references, mostly from the last 5 years; foundational older works allowed when said so.
- Bi-directional consistency: every `.bib` entry cited, every `\cite` resolves.
- **Web verification was unavailable in this session** (the user declined web search and asked to work from the booklets only). Therefore:
  - every market/industry number is labelled in the text as a team estimate ("אומדן הצוות") and is never given a citation it does not have;
  - `report/work/source_verification_checklist.md` lists every reference and every estimate for the students to verify (booklet §17, three-step check).

## 7. QA & sign-off (Chair)
- 4-pass compile: `lualatex → biber → lualatex → lualatex`, 0 lines starting with `!`.
- Detector (`bidi-qa-detector`, `scripts/qa_detector_audit.py`) → `report/work/qa_audit_report.md`; Fixer (`bidi-qa-fixer`) applies the iron rule: repeating issue → template + version bump; one-off → chapter file. Detection and fixing are never mixed.
- Red team (`red-team-examiner`, Prompt 9) → `report/work/red_team_review.md`; all 10 points resolved.
- Sign-off list (booklet §19.5): 0 errors and no unresolved reference; no reversed Hebrew, nothing outside margins; tables aligned, all images present; every source checked; every page inspected visually; summary readable by an outsider.

## 8. Grading rubric (100 points)

| # | Item | Pts | Owner |
|---|---|---|---|
| R1 | Preliminary pages complete (cover, summary 250–350 words + keywords, TOC, lists, abbreviations) | 8 | Chair |
| R2 | Page budget respected (44 pages; chapters on budgeted pages) | 6 | Chair |
| R3 | Introduction as funnel, quantitative grounding, no cliché | 5 | Chair |
| R4 | Quantitative problem without the solution; research question vs SMART goals | 7 | Systems Eng. |
| R5 | Requirements table: IDs, class, SI targets, verification for every row | 8 | Systems Eng. |
| R6 | Thematic critical review with ≥ 15 peer-reviewed sources + literature matrix | 9 | CV Scientist |
| R7 | Flagship paper: Venn selection, equations, limits, one-sentence gap | 7 | CV Scientist |
| R8 | Market sizing TAM/SAM/SOM with labelled estimates + bottom-up SOM | 5 | Venture Arch. |
| R9 | Technical competitor table + radar + log scatter | 6 | Venture Arch. |
| R10 | Three distinct alternatives + weighted matrix (Σw = 1.00) + sensitivity | 9 | Systems Eng. |
| R11 | Architecture/data-flow diagram + justified innovation | 5 | CV Scientist |
| R12 | WBS + RACI (single R) + Gantt (critical path, 2 milestones, buffers) | 8 | Systems Eng. |
| R13 | Risks: R = P×I, heatmap, mitigation + contingency + residual for R ≥ 12 | 5 | Systems Eng. |
| R14 | Summary & three immediate actions | 2 | Chair |
| R15 | Typography/BiDi/template quality (0 errors, 0 reversed text, template-level fixes) | 5 | Chair |
| R16 | Repository: skills, prompts log, scripts, README, CHANGELOG | 5 | Chair |
| | **Total** | **100** | |

## 9. Traceability

| Rubric | Chapter file | Figure / table labels | QA check (`qa_detector_audit.py` / review) |
|---|---|---|---|
| R1 | `coverpage.tex` | — | cover has no page number; word count 250–350; TOC/LoF/LoT present |
| R2 | all | — | total pages == 44; chapter start pages 1,4,8,17,23,31,35,37; refs 38 |
| R3 | `ch1_intro.tex` | `fig:funnel` | label referenced; red team point "cliché" |
| R4 | `ch2_problem.tex` | `fig:problemchain`, `tab:research-vs-design` | labels referenced; red team "solution in problem" |
| R5 | `ch2_problem.tex` | `tab:requirements` | red team "untestable requirement" |
| R6 | `ch3_literature.tex` | `tab:litmatrix` | bib ⇄ cite consistency; ≥ 15 papers cited |
| R7 | `ch3_literature.tex` | `fig:venn` | gap sentence present; equations numbered |
| R8 | `ch4_market.tex` | `fig:tamsamsom` | "אומדן הצוות" label present |
| R9 | `ch4_market.tex` | `tab:competitors`, `fig:radar`, `fig:scatter` | labels referenced; CSV-driven plots |
| R10 | `ch5_alternatives.tex` | `tab:alternatives`, `tab:pugh`, `fig:pughbars`, `fig:sensitivity` | Σw = 1.00; red team "matrix written backwards" |
| R11 | `ch5_alternatives.tex` | `fig:architecture` | width ≤ 12.4 cm; no Overfull |
| R12 | `ch6_workplan.tex` | `fig:wbs`, `tab:wbs`, `tab:raci`, `fig:gantt`, `tab:tasks` | one R per row; milestones weeks 8 & 12 |
| R13 | `ch7_risks.tex` | `fig:riskmatrix`, `tab:risks`, `tab:mitigation` | every R ≥ 12 has mitigation/contingency/residual |
| R14 | `ch8_summary.tex` | `fig:nextsteps` | 1 page |
| R15 | `base-report.cls`, `auratwin-report.cls` | `tests/stress_test.tex` | log errors, final letters at word start, reversed acronyms, `??` |
| R16 | repo root | — | file-structure family in detector |

---

## 10. PRD revision v1.2 (2026-11-16) — user "rejects" prompt: UX, identity, readability

New committee members (skills 10–12) added binding requirements. The original rubric weights are unchanged;
these items are acceptance criteria inside the existing rubric lines (chapters 1, 2, 4, 5; visual; template; QA).

| ID | Requirement | Acceptance criterion | Owner skill | Evidence |
|---|---|---|---|---|
| PRD-UX-01 | Human & cultural need, cross-demographic audience | Ch.1 section naming teenage girls, women of all ages, grooming-aware men, the two decision moments, extension + app; no unsourced statistics | ux-entrepreneur-strategist | Ch.1 §1.2 |
| PRD-UX-02 | Audience framed as users of the problem | Ch.2 names who pays the price without naming the solution | ux-entrepreneur-strategist | Ch.2 §2.1.3 |
| PRD-UX-03 | Segments tied to revenue lines | each segment maps to a revenue line already in the unit economics | ux-entrepreneur-strategist | Table 4.4 |
| PRD-UX-04 | 4-step user journey with time budgets and REQs | figure, right-to-left, ≤ 12.4 cm, each step with budget + REQ | ux-entrepreneur-strategist | Fig. 4.4 |
| PRD-UX-05 | UI wireframe (extension + app) | TikZ/tcolorbox, palette only, analytical paragraph, values marked illustrative | ux-entrepreneur-strategist | Fig. 5.5 |
| PRD-ID-01 | "Luxury, Vintage, Bold" palette only | six colours wired through semantic names; detector finds no raw colours or `\textcolor` in chapters | luxury-vintage-ui-designer | `auratwin-report.cls` v1.3.0 |
| PRD-ID-02 | 3-arch + eye logo | TikZ macro on cover and headers; PNG for README; same geometry | luxury-vintage-ui-designer | `report/figures/auratwin_logo.png` |
| PRD-ID-03 | Editorial chapter openings + cover | badge + Mustard/Dust rules; Egg Nog cover with double frame | luxury-vintage-ui-designer | previews |
| PRD-RD-01 | Breathing room | 1.5 spacing, parskip ≥ 6 pt, arraystretch ≥ 1.25, box padding ≥ 8/6 pt; 40-page body kept | human-readability-math-auditor | `readability_math_audit.md` §1 |
| PRD-RD-02 | Equation integrity | every numbered equation followed by Hebrew definitions of every symbol; no Hebrew in math outside `\hebmath` | human-readability-math-auditor | `readability_math_audit.md` §2–3 |
| PRD-RD-03 | BiDi punctuation | no space before . , : ; ) next to Hebrew; mixed labels as one `\heb{}` unit | human-readability-math-auditor | `readability_math_audit.md` §4 |
