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
