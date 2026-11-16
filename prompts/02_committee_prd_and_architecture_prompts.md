# 01 — Expert Committee → PRD.md

Skill: `.claude/skills/expert-committee-prd/SKILL.md` · Output: `PRD.md` · Run: before any LaTeX was written.

## Prompt (as used for AuraTwin AI)

```text
You are the Preparatory Report Expert Committee, four personas who each sign their own section:
(a) Academic Seminar Chair — enforcer of Dr. Yoram Segal's methodology ("From Problem to PDF");
(b) Chief AI & Computer-Vision Scientist — CIELAB ΔE00 calibration, SMPL-X, diffusion virtual try-on, multimodal RAG;
(c) Beauty-Tech Venture Architect — TAM/SAM/SOM, competitor teardown, ad-gated and affiliate unit economics;
(d) Chief Systems Engineer — ISO/IEC/IEEE 29148 requirements, Pugh matrix, WBS/RACI/Gantt, ISO 31000 risk.

Context: group roma-ai2 (רוני אופיר, מעיין שירי — Statistics, University of Haifa; advisor ד"ר יורם סגל).
Project: AuraTwin AI — multimodal agentic system for self-calibrated biometric beauty & fashion styling,
social trend mining and ad-gated generative virtual try-on. The industrial partner is SIMULATED and must be
labelled as such.

Read the booklets in this folder with `pdftotext -enc UTF-8` (PyMuPDF reverses Hebrew word order).
Do not write any LaTeX. Produce PRD.md with sections:
1 Vision & premise, 2 Page map (booklet Table 1.1: א'–ד' + 40 body pages = 44), 3 Per-chapter requirements,
4 Visual requirements, 5 Template requirements, 6 Source policy, 7 QA & sign-off, 8 Rubric (100 points),
9 Traceability (rubric item → chapter file → figure/table label → QA check).

Hard rules:
- Freeze the decision-matrix weights and integer scores in the PRD BEFORE any total is computed.
- Every market number needs a source or the label "אומדן הצוות"; never an invented citation.
- Every requirement has an ID, a class, a quantitative SI/statistical target and a verification method.
- A problem statement must not name the solution.
Success: PRD.md exists; rubric sums to 100; every rubric row has a QA check.
```

## How it was used in this project
- Run after the booklets were ingested and before `base-report.cls` was written.
- Web search was declined by the user, so the committee added the rule that market figures are labelled team
  estimates and created a student verification checklist (`report/work/source_verification_checklist.md`).
- Decision-matrix inputs frozen in the PRD: weights accuracy 0.25, unit cost 0.20, latency 0.15, photorealism 0.15,
  privacy 0.15, development effort 0.10 (Σ = 1.00) and integer scores per alternative; the totals 4.45 / 3.15 / 2.85
  were computed afterwards by `scripts/generate_beauty_benchmarks.py`.
- The calibration-simulation results were added to the PRD once computed, and REQ-VIS-01 was set to
  median ΔE00 ≤ 1.8 and P95 ≤ 4.5 (the simulation meets the median, not yet the P95 — stated as the research question).


---

## Domain-architect prompts (skill `beauty-ai-domain-architect`)

### DA-1 — Canonical equations
```text
You are the domain architect of AuraTwin AI. Fix ONE notation for the whole report and write it into
.claude/skills/beauty-ai-domain-architect/SKILL.md: CIEDE2000 ΔE00; von Kries diag(ℓ); the MAP calibration
M̂ = argmin Σ λk ΔE00(M⁻¹c_obs, μ(k)) + γ‖M − I‖²_F with sclera + iris anchors; SMPL-X M(β,θ,ψ) and the
ratio vector r = (C_chest, C_waist, C_hip, L_inseam)/H; trend score T(s); Pugh S_j = Σ w_i c_ij; R = P × I.
Every chapter must reuse these symbols exactly. Define every symbol in Hebrew right below its equation.
```

### DA-2 — Simulation instead of invented numbers
```text
Do not type benchmark numbers by hand. Write scripts/generate_beauty_benchmarks.py: a CIEDE2000
implementation checked against Sharma et al. test pairs, a Monte-Carlo of 4,000 synthetic selfies under
2700-6500 K light, and five correction methods (camera, gray-world, sclera, sclera+iris, enrolment+iris prior).
Also compute the Pugh totals, one-at-a-time and Dirichlet weight sensitivity, ±1 score sensitivity,
the cluster-bootstrap power analysis, the gate unit economics and the bottom-up SAM/SOM.
Write CSVs for every chart and a summary the chapters quote.
```

### DA-3 — Red-team corrections (round 2)
```text
Model the gate as ad OR affiliate (expected value with share q), separate the commercial try-on API
(status quo) from the self-hosted distilled model, derive the 2.4x threshold from a gross-margin target,
and re-anchor the Pugh scores to explicit 1/3/5 scales. Report every changed number in PRD revision v1.1.
```
