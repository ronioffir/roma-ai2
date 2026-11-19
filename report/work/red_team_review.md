# Red Team review: דוח מכין AuraTwin AI (Prompt 9)

Examiner: strict committee member, fresh context. Input judged: compiled PDF only (44 pages, 4 preliminary + 40 body).
Page numbers below are the **printed** page numbers (body pages "עמוד N מתוך 40"; preliminary pages א׳–ד׳).
Quotes are exact Hebrew from the PDF.

## Rubric score BEFORE upgrades (PRD section 8): 73 / 100

| # | Item | Max | Score | Basis |
|---|---|---|---|---|
| R1 | Preliminary pages | 8 | 6 | Cover, TOC, lists, abbreviations present. Abstract (p. ב׳) is about 235 words, below the required 250–350. |
| R2 | Page budget | 6 | 6 | 44 pages; chapters start on 1, 4, 8, 17, 23, 31, 35, 37; references 38–40. |
| R3 | Intro as funnel | 5 | 3 | Funnel figure exists, but the only hard number in ch.1 is the unsourced "30%–40%" returns rate (p.1). Quantitative grounding is thin. |
| R4 | Quantitative problem, no solution; RQ vs SMART | 7 | 5 | Fig. 2.2 (p.4) shows the proposed solution ("רישום + קשתית (מוצע)") inside the "problem without the solution" chapter. H1 is badly designed (point 1). |
| R5 | Requirements table | 8 | 6 | IDs, class, targets and verification are present for 12 rows. Several targets have no derivation or feasibility evidence (point 10). |
| R6 | Critical review, ≥15 peer-reviewed sources, matrix | 9 | 7 | 46 references and a matrix. No search protocol. The course booklet [1] is cited as support for factual claims. The matrix is self-scored. |
| R7 | Flagship paper, gap in one sentence | 7 | 5 | Venn, equations and limits are present. The gap "sentence" is a 4-way conjunction with an absolute "never tested" claim (point 9). |
| R8 | TAM/SAM/SOM with labelled estimates, bottom-up SOM | 5 | 2 | Labelled, but nothing is traceable: no base, no source, ARPU unexplained (point 3). |
| R9 | Competitor table, radar, log scatter | 6 | 4 | All three exist. Every score is a team assessment, and the target product is plotted against them (see "Other deductions"). |
| R10 | Three alternatives, Σw = 1.00, sensitivity | 9 | 7 | Arithmetic checks out and the sensitivity analysis is rich. Weights and scores are not independently justified; alternatives are bundled (point 5). |
| R11 | Architecture and innovation | 5 | 3 | Diagram is clear, but the privacy claim is contradicted one page later (point 6). |
| R12 | WBS + RACI + Gantt | 8 | 6 | Single R per task, critical path, two milestones and buffers are present. Inconsistent float, SMART-goal timing and missing ethics/recruitment (point 7). |
| R13 | Risks | 5 | 4 | R = P×I, heatmap, and mitigation/contingency/residual are present. Residuals are asserted and the register is incomplete (point 8). |
| R14 | Summary and three actions | 2 | 1 | The three "immediate actions" are administrative (freeze config, repo, kickoff). None attacks the two open questions the summary itself names. |
| R15 | Typography/BiDi/template | 5 | 4 | No visible defects found. Final-letter extraction artefacts are a tool effect, not scored. |
| R16 | Repository | 5 | 4 | Not assessable from the PDF alone. Assumed mostly in order. |
| | **Total** | **100** | **73** | |

---

## The 10 weakest points

### 1. Hypothesis test and power analysis are internally incoherent (severity 3)
- **Page:** 5 (continues on p.6)
- **Quote:** "חישוב עוצמה לגודל אפקט d = 0.4 ולעוצמה של 0.9 מחייב 68 משתתפות לפחות."
- **Weakness:**
  - H1 is a conjunction of two different claims: median paired difference > 0, **and** method median < 1.8. A single Wilcoxon signed-rank test on differences tests only the first. The second, which is the actual requirement, needs a one-sample test or a confidence bound against 1.8.
  - d = 0.4 is a parametric paired-t effect size. The report's own simulation (Fig. 2.2) shows a mean gap of roughly 3 ΔE00, which implies an effect far larger than 0.4. The assumed effect is therefore unconnected to any evidence.
  - Each participant is photographed under 4 lightings (p.6). The 480 observations are clustered, not independent, and the design ignores this (no mixed model, no cluster-robust CI).
  - REQVIS01 also requires P95 ≤ 4.5. With 120 people, a P95 estimate has a very wide interval, and no test or CI method is specified for it.
  - The "subgroup analysis by skin tone" has no number of strata and no multiplicity control. At 120 people, each stratum has only a few dozen participants.
  - No ethics approval or recruitment-bias plan is stated.
- **Required upgrade:**
  - Split H1 into H1a (paired superiority) and H1b (median < 1.8, one-sided, by bootstrap or Wilcoxon one-sample).
  - Compute power for the actual test. Show the assumed effect and its source (simulation SD).
  - Analyse per-participant medians, or use a mixed model with participant as a random effect.
  - Specify the P95 CI method (bootstrap), the strata and the multiplicity correction (Holm).
  - Add an ethics-approval line.

### 2. The headline evidence is a self-built simulation with a straw-man baseline, and it already misses a requirement (severity 3)
- **Page:** 4 (and 6, 9, 37)
- **Quote:** "הממצא החשוב יותר הוא שאיזון לבן גלובלי בשיטת "העולם האפור" מחמיר את השגיאה ל-9.77 בממוצע"
- **Companion quote (p.6):** "בסימולציה המקדימה השיטה הגיעה לחציון 1.37 ולאחוזון 95 של 4.81."
- **Weakness:**
  - The same team generated the synthetic data, the eye prior and the correction method. Nothing validates that the simulated eye/sclera model matches real eyes. Sclera is not a neutral reflector: it has redness, yellowing and age effects, and the chapter 3 assumption "משטח כמעט ניטרלי" is stated without evidence.
  - The only baseline beaten is Gray World, a method known to fail when skin dominates the frame.
  - The report itself surveys stronger baselines (FFCC [21], FC4 [22], Afifi [10]) in ch.3, but none is run in the simulation.
  - Fig. 2.2 reports means and P95. The text, abstract and requirement use the median (1.37), and the median is not in the figure. No CI or SD is shown for n = 4,000.
  - The P95 of 4.81 already exceeds the REQVIS01 target of 4.5. The abstract (p. ב׳) and the summary (p.37) present the 1.37 median as a result and mention P95 only as an "open question".
  - Fig. 2.2 includes the proposed solution row inside the chapter that promises "the problem without the solution".
- **Required upgrade:**
  - Add FFCC/FC4 or a learned white-balance baseline, and a "camera AWB" baseline, to the simulation.
  - Add a sensitivity study of the sclera-neutrality assumption (tint, redness, eyelid occlusion, lens).
  - Report median, IQR, P95 and CI per method in one table.
  - State plainly that the simulation is optimistic and that P95 currently fails.
  - Move the "proposed" row out of the ch.2 problem figure into ch.5 or ch.8.

### 3. Market sizing is not traceable; ARPU and B2B revenue are unexplained (severity 3)
- **Page:** 17 (table on p.18)
- **Quote:** "ההכנסה הממוצעת למשתמשת (ARPU) של $1.45 לחודש אינה מנוי: היא סכום של הכנסות פרסום מתגמל ועמלות שותפים, שחישובן מפורט בסעיף 4.4."
- **Weakness:**
  - Section 4.4 computes revenue **per simulation** ($0.109, Table 4.3). It never derives a monthly ARPU: there is no simulations-per-user assumption. The cross-reference is false.
  - B2C accounts for $27.8M of the $42.2M SOM (66%). It rests on "1.6 million active users" in Israel plus tier-1 EU retailers, with no penetration logic.
  - B2B is "12 retailers × $1.2M" with no price benchmark.
  - TAM $18.4B (2028) with CAGR 28.4% and SAM $3.2B have no base year, no derivation and no source. The chapter itself admits (p.17) that the numbers "יוחלפו במספרים מדוחות אנליסטים לפני הגשת הספר הסופי", i.e. they are placeholders. The label "אומדן הצוות" does not make a number defensible.
  - The SOM/SAM = 1.3% ratio is presented as "conservative" without a benchmark.
- **Required upgrade:**
  - Give TAM and SAM a source (analyst report, with year) or a bottom-up derivation: users × penetration × ARPU, with each factor labelled.
  - Add the missing ARPU bridge (sessions/month, simulation share, per-simulation revenue).
  - Provide a range (low/base/high) for SOM and for each B2C/B2B driver.
  - Remove the "will be replaced later" sentence by actually replacing the numbers.

### 4. Unit economics: unsourced inputs, an additive error, and a threshold that looks reverse-engineered (severity 3)
- **Page:** 21 (also p. ב׳, p.5)
- **Quote:** "מהטבלה עולה שדרישת REQBIZ12, הכנסה של לפחות פי 2.4 מעלות החישוב, מתקיימת רק בתרחיש הבסיס, שבו עלות ההדמיה היא $0.045."
- **Weakness:**
  - eCPM = $15, conversion 1.8%, AOV $65 and commission 8% have no source. The affiliate leg is 86% of revenue ($0.094 of $0.109).
  - The gate is an either/or ("צפייה במודעה ... או מעבר לדף המוצר", p.21), but Eq. 4.1 and Table 4.3 add both streams per simulation. The $0.109 is overstated for any single path.
  - The requirement is ≥ 2.4×, and the base case gives 2.42 (0.109/0.045). The pass margin is about 1%. The target looks fitted to the result, which is exactly the "written backwards" pattern. The full-model ratio is 1.21.
  - Chapter 2 and the abstract state $0.045–0.090 as the **current-state** cost that makes the service "לא בר-קיימא", whereas ch.4 uses the same range as the cost of the **proposed** distilled vs. full model. The same number plays two roles.
  - No sensitivity of the ratio to conversion rate or eCPM is given.
- **Required upgrade:**
  - Source each input (or give a range plus a literature or benchmark anchor).
  - Compute revenue per path (ad **or** affiliate) with a path-share assumption.
  - Add a tornado or break-even analysis: conversion and eCPM at which the ratio falls to 2.4 and to 1.0.
  - Justify 2.4 independently (target margin) and state the pass margin.
  - Unify the meaning of $0.045–0.090.

### 5. Decision matrix: weights and scores are asserted, scoring is inconsistent with the report's own tables (severity 3)
- **Page:** 25
- **Quote:** "חלופה 3 מקבלת 5 בדיוק, כי היא היחידה שמשלבת כיול ומידות, ו-4 בעלות ובפרטיות, כי היא משתמשת בענן, אבל רק לווקטורים."
- **Companion (p.25):** "לכן המשקלים והציונים בטבלאות 5.3 ו-5.4 הוקפאו במסמך הדרישות (PRD) לפני שחושבו הסכומים."
- **Weakness:**
  - The "freeze" evidence is a document the committee cannot see. The weights in Table 5.3 are justified only by one phrase each ("לב הבעיה", "קיימות כלכלית"). Nothing explains why accuracy = 0.25 and not 0.20.
  - Alternatives are bundled. Alt 3 is defined as "the project's own innovations" (eye anchor, metric sizes, gate). Alt 1 also contains calibration and a body model (Table 5.2 marks REQVIS01 as met), yet gets accuracy 3 vs. 5. Accuracy is the very quantity the project must still prove, so the score is an expectation, not a measurement.
  - Alt 3 gets latency 5, but Table 5.6 puts the simulation path at exactly 4.50 s = the limit, and Table 5.2 marks it "חלקי".
  - Privacy 4 contradicts the architecture text (point 6).
  - The integer 1–5 scores come from one rater (the team), with no inter-rater check.
  - Sensitivity covers only **weights**. The Dirichlet concentration is not given. A ±1 perturbation of the scores is not tested, though it would be the more likely error.
- **Required upgrade:**
  - Give each weight a quantified rationale (for example, AHP pairwise comparisons, or the cost/accuracy impact derived from ch.2).
  - Score every cell against a rubric tied to a requirement number.
  - Make the alternatives comparable (the calibration pipeline in all three, varying only where compute runs, or state explicitly that they differ in more than compute).
  - Add a score-perturbation Monte Carlo and state the Dirichlet parameters.
  - Reproduce the weight-freeze in the report (a dated table) instead of pointing to the PRD.

### 6. The privacy claim is contradicted inside the same chapter (severity 3)
- **Page:** 27, contradicted on 28
- **Quote (p.27):** "אף חץ אינו מעביר תמונה גולמית אל הענן."
- **Contradiction (p.28):** "החריג היחיד הוא מודל ההדמיה, שמקבל את תמונת המשתמשת."
- **Weakness:**
  - The VTON model runs in the cloud ("Distilled VTON" in Fig. 5.4, Table 5.5: location "ענן (GPU)") and must receive the user's photo.
  - Yet REQSEC11 requires "0 תמונות גולמיות בשרת" (Table 2.2). The abstract states the compute is gated, and §5.3.5 says "וקטורים בלבד בענן, ללא תמונות" (ADR5).
  - The architecture figure, ADR5, REQSEC11 and the privacy score 4 in the matrix all disagree with Table 5.5.
  - The requirement is violated by design, and the risk register treats RSKSEC05 (R = 10) as non-critical on the strength of this claim.
  - This is the biometric-data core of the GDPR/AI Act argument made in ch.1.
- **Required upgrade:**
  - Either change the design (VTON only on-device or on an edge-confined path), or restate REQSEC11 honestly ("no raw images are retained, and raw images are transiently processed only with explicit per-simulation consent, deleted ≤ X s").
  - Redraw Fig. 5.4 with the photo arrow.
  - Re-score privacy in Table 5.4 and re-run the sensitivity analysis.
  - Re-rate RSKSEC05 with a likelihood and impact that reflect transient cloud processing.

### 7. Work plan inconsistent with its own SMART goals, float claims and validation load (severity 2)
- **Page:** 32 (with 6, 33, 31)
- **Quote:** "לכן המשימה הראשונה, ניסוי הבסיס, מתחילה בשבוע הראשון ממש, בלי תלות בשותף."
- **Weakness:**
  - SMART goal (1), p.6: "עד סוף שבוע 8, צינור הכיול רץ על המכשיר ועומד ב-REQVIS01 על מדגם האימות". The validation experiment (TSK4.2) is in weeks 9–11 (Table 6.3). The goal is unattainable by its own schedule.
  - TSK1.1 (baseline experiment and data collection) is allotted weeks 1–2, while ch.2 requires 120 participants × 4 lightings with a spectrophotometer. This is implausible before ethics approval and recruitment.
  - TSK2.2 (weeks 4–6) is a listed predecessor of TSK4.1 (weeks 6–7). Finish-to-start gives zero or negative float. This contradicts the p.32 claim that "מנוע הטרנדים והשער נהנות ממרווח של שבוע עד שלושה שבועות".
  - The critical path fills exactly 14 weeks with no slack outside the two reserve weeks.
  - REQBOD03 (60 participants, double tape measure), the 500-image eye labelling (REQVIS02) and the 300-image nail labelling have no task and no duration in the WBS.
  - The ±4.8 cm baseline (p.5) is said to be validated in TSK1.1, but TSK1.1 is the colour experiment.
  - No ethics-approval task exists.
- **Required upgrade:**
  - Rebuild Table 6.3 with explicit start/finish, free float and total float per task, and verify the finish-to-start logic.
  - Align SMART goal (1) with the milestone that actually tests it.
  - Add tasks for ethics approval, recruitment, body-measurement validation and labelling.
  - Add an effort estimate (person-days) per task.

### 8. Risk register: residual scores asserted, obvious risks missing (severity 2)
- **Page:** 36 (and 37)
- **Quote:** "הטבלה מראה שאף ציון שיורי אינו נשאר באזור הקריטי."
- **Companion (p.37):** "וארבעה סיכונים קריטיים שציונם השיורי ירד לאזור הבינוני"
- **Weakness:**
  - Residuals were obtained by cutting probability to 2 (RSKALG01 4→2, RSKGEN02 4→2, RSKBIZ04 3→2) with no evidence that the mitigation reduces likelihood that much. These are self-assessed numbers.
  - Table 7.2: RSKDAT03 residual = 4, which is in the "low" band (R ≤ 5) per Fig. 7.1, not "medium" as the summary says.
  - The contingency for RSKALG01 ("מעבר לכיול בעזרת דף לבן מודפס") abandons the project's central premise (eye anchor, no reference card) and gives no expected ΔE or compatibility with REQVIS01.
  - Missing risks the report itself exposes: P95 above target (4.81 vs 4.5, p.6); simulated eye model not matching real data; participant recruitment/ethics delay; the partner and its catalogue are fictional (p.2); the pass-margin of REQBIZ12 is about 1%; the hybrid's cloud image processing (point 6).
  - Owners are named but no budgeted contingency (weeks or cost) is allocated to the critical ones.
- **Required upgrade:**
  - Justify each residual P and I (pilot data, historical rate, or a cited analogue). Recompute the summary statement.
  - Add the missing risks with P, I, R and mitigation, contingency and residual (at least four).
  - Give each contingency a measurable trigger (already partly in Table 6.4), a time or cost budget, and the expected requirement impact.

### 9. The gap statement is not one sharp, testable sentence and rests on an unreferenced negative (severity 2)
- **Page:** 16
- **Quote:** "פער הידע: עד כה לא נבדק אם עיגון צבע ביומטרי בעין, המשולב עם מידות גוף מטריות ועם שער כלכלי לחישוב, מאפשר המלצה והדמיה וירטואלית שנאמנות גם לצבע וגם לגזרה של המשתמשת, בתאורה לא מבוקרת ובעלות ממומנת ליחידה."
- **Weakness:**
  - It stitches together four contributions (eye colour anchor, metric size, economic gate, VTON/recommendation fidelity). The conjunction can be "novel" only because the combination is unusual. Each element on its own (eye as light probe [24], height-conditioned measurement [26], gated compute) is known.
  - The gap is formulated as "never tested", with no search protocol: no databases, search strings, date window or hit counts (§3.1 lists venues only). This is an absence-of-evidence claim.
  - The cited authority [41] (Sandberg & Alvesson) is the paper that **criticises** gap-spotting as a way to build research questions.
  - H1 tests only the colour element. The size, gate and fidelity elements of the "gap" have no corresponding hypothesis.
  - The matrix (Table 3.2) gives the proposed project five filled circles, which is a self-score.
- **Required upgrade:**
  - Reduce the gap to one sentence with one testable core (for example: "no published method calibrates skin colour in a selfie using sclera and self-reported iris colour as priors and reports ΔE00 against a spectrophotometer").
  - Present the other elements as secondary contributions.
  - Document the search (database, strings, years, N screened/N included).
  - Replace or reframe [41].
  - Mark the project row of Table 3.2 as "target" and the gap cells as "not found in the N screened papers".

### 10. Requirement targets lack derivation and feasibility evidence; two are asserted feasible with no source (severity 2)
- **Page:** 5 (with 7 and 10)
- **Quote:** "לפי אומדן הצוות, שיתוקף בניסוי הבסיס (משימה TSK1.1), השגיאה האופיינית בהיקף מותן הנאמד מתמונה כזו היא בסדר גודל של ±4.8 cm"
- **Weakness:**
  - The 4.8 cm baseline is a team estimate with no source or simulation, yet the body-measurement target MAE ≤ 1.2 cm requires a four-fold improvement. No preliminary evidence is given. The abstract still lists MAE ≤ 1.2 cm as a main design goal.
  - Tape-measure ground truth has its own inter-rater error of about 1 cm, so a 1.2 cm MAE is near the noise floor of the reference. No reliability study is planned, and no P95 is set.
  - p.10 states that detection plus SAM "מאפשר פילוח ציפורניים שעומד ביעד IoU ≥ 0.94". Neither cited paper ([9], [27]) reports nail segmentation, and 0.94 on small regions is very high.
  - Other thresholds (ArcFace cosine ≥ 0.88, LPIPS ≤ 0.15, P@5 ≥ 0.85 judged by 3 stylists, "≥ 97%" with IoU ≥ 0.85) have no derivation. P@5 has no number of queries and no inter-rater agreement.
  - "פחות החזרות" is claimed as a benefit but is not measurable by any requirement.
- **Required upgrade:**
  - For each target add a derivation column ("source / baseline / why this value").
  - Give a small preliminary measurement or literature value for body error and nail IoU.
  - Add a tape-measure reliability protocol, with agreement as part of the verification.
  - Define sample sizes for REQREC10 and the inter-rater statistic (κ).
  - Delete or substantiate the feasibility sentence on p.10.

---

## Other deductions noticed (not in the top 10)
- **p. ב׳ abstract:** about 235 words, below the 250–350 required (R1). It also presents simulation results (4.89, 9.77, 1.37) as findings without the "simulated" caveat next to each number.
- **p.1 and p.3:** "שיעור ההחזרות בהלבשה מקוונת עומד על 30%–40%" has no source ("אומדני הצוות ... ייבדקו מול דוחות אנליסטים בשלב המימוש"). The chapter with the quantitative-funnel job contains almost no sourced figure.
- **p.17–19, Fig. 4.2 and 4.3:** radar scores and the "personalisation accuracy index" are team assessments. The regression y = 68.8 + 4.5·log10 x is fitted on about six self-assigned points, with no CI. AuraTwin (88) is a **target** plotted next to assessed competitors, then "28 points above the line" is read as a result. The claim "the only profile with no axis below 4" is circular.
- **p.22:** "מאגר כזה אינו קיים כיום בציבור" is an absolute claim without a source. The data moat is 120 participants, which L'Oréal could replicate.
- **p.18 and p.19:** competitor cost-per-session values ($0.003, $0.004, $0.03, $8) are team estimates without a source.
- **p.14 and p.29:** the 8 s on an A100 for the flagship is an estimate. The distillation to 8 steps is assumed to hold quality (realism 5 in the matrix), with no citation or pilot.
- **Cross-chapter numbers:** Table 5.1 says hybrid recommendation "< 1.2 s", while Table 5.6 gives 1.46 s (both under 1.8 s, but the number differs). The matrix gives the same latency score 5 to both. The $0.011 per-session cost in Table 4.2 has no derivation.
- **p.1 to p.3, [1]:** the instructor's course booklet is cited as support for method claims (5+ places). It is not an independent peer-reviewed source.
- **p.37:** the three "immediate actions" are administrative, none targets the P95 or latency open questions that the same page says are "in the critical path".

---

## Resolution log

Round 2 re-check of the rebuilt PDF (44 pages, same layout of chapters). Evidence pages are printed page numbers.

| # | Point (short) | Severity | Status | Evidence / what is still missing |
|---|---|---|---|---|
| 1 | H1 and power analysis incoherent (p.5) | 3 | RESOLVED | p.5–6: "השאלה מפורקת לשתי השערות, שנקבעות מראש ונבחנות עם תיקון הולם (Holm)". H1a is a one-sided Wilcoxon on per-participant means plus a mixed model with a participant random effect. H1b is a bootstrap upper bound over whole participants, below 1.8. P95 is reported with a CI and explicitly "אינו מבחן השערה". Power: "גודל אפקט שמרני של d = 0.4, כרבע מגודל האפקט שנמדד בסימולציה ... נדרשות 56 משתתפות", with 120 recruited, 40 per ITA group. The ethics request is added (p.32, p.37, Table 6.3). Residual nits: Table 2.1 still says "שאלה והשערה H1 ... דחיית H0 ב-α = 0.05, n = 120" and §5.4 still says "בהשערה H1". The Holm family is only loosely described, because the mixed model and the Wilcoxon test are two analyses for H1a. |
| 2 | Simulation validity, straw-man baseline, P95 above target | 3 | PARTIALLY RESOLVED | Fixed: Fig. 2.2 (p.4) is now the status quo only ("מצלמה, ללא תיקון" and Gray World), and the proposed row moved to Fig. 5.4 (p.28). P95 is no longer hidden: "האחוזון ה-95 ... 4.81, ורווח הסמך שלו בתכנון של 120 משתתפות, 4.20–5.48, חוצה את היעד של 4.5 ... מוגדרת כסיכון RSKALG07" (p.28). Sclera neutrality is now flagged as a working assumption: "בסימולציה לובן העין אינו ניטרלי לגמרי ... היא הנחת עבודה שתיבדק בניסוי הבסיס". Subgroup results by ITA are reported. Still missing: FFCC and FC4 are not in the simulation ("יתווספו בניסוי האמיתי"), so the only learned or stronger baselines are deferred. The sclera and iris variability model is not specified (distributions, tint range). The data are still self-generated. Fig. 5.4 reports means and P95, while the median 1.37 appears only in the text. |
| 3 | Market sizing and ARPU untraceable (p.17) | 3 | PARTIALLY RESOLVED | The ARPU is now derived (p.17): affiliate 6×3×8%×4%×8%×$65 = $0.30, rewarded ads $0.09, premium 3%×$9.99 = $0.30, total $0.69. I recomputed it and Table 4.1 (SAM $1.80B + $1.24B, SOM $14.4M + $13.2M = $27.6M, SOM/SAM 0.9%), and the arithmetic is correct. The TAM is declared "תרחיש עליון בלבד: הוא אינו משמש לשום החלטה". Still missing: every driver (8% click, 4% purchase, 3% premium, $9.99, 150M users, 3,000 retailers × $0.6M, 2M orders × $0.60) is an unsourced team assumption, and TAM $18.4B and CAGR 28.4% still have no source. No low/base/high range for the SOM. The p.17 sentence "יוחלפו במספרים מדוחות אנליסטים לפני הגשת הספר הסופי" is still there. See new issues N5 and N6. |
| 4 | Unit economics: unsourced inputs, additive error, 2.4 vs 2.42 | 3 | PARTIALLY RESOLVED | Fixed: Eq. 4.1 is now a weighted mean "ולא סכומם" with q = 0.5, so r̄ = $0.054 (I verified). REQBIZ12 is derived: "היחס 2.4 נגזר מיעד של מרווח גולמי של כ-58%" (p.20). The cost of the distilled self-hosted model is derived ($0.80/h L4, 4.5 s, 30% utilisation, ×1.6 overhead = $0.0053, ratio 10.2). A stress case gives 6.2, and a cost ceiling of $0.023 is stated. The two roles of $0.045–0.090 are separated: "מצב מצוי ... יחס 0.60–1.21" versus the self-hosted model (p.20–21). The abstract (p. ב׳) is consistent with this. Still missing: eCPM $15, conversion 1.8%, AOV $65 and commission 8% are unsourced ("כולן אומדנים שייבדקו מול נתוני השותף"). Utilisation 30% and overhead 1.6 are unsourced. Only q and eCPM are stressed. See N5. |
| 5 | Decision matrix weights and scores | 3 | PARTIALLY RESOLVED | Fixed: an anchored scoring scale (Table 5.5) for each criterion; scores recomputed (Alt 3 = 4.30, Alt 1 = 3.40, Alt 2 = 2.85, sums verified); Alt 1 accuracy now 4, Alt 3 latency 4, privacy 4 with "תמונה ארעית רק בהדמיה ובהסכמה"; a score-perturbation test: "בכל 28 השינויים האפשריים של ציון יחיד ב-±1, המנצחת לא התחלפה" and a double hostile change still leaves Alt 3 ahead (3.85 vs 3.70). Still missing: the weights in Table 5.3 are justified only by a requirement link, with no quantified derivation (AHP or similar). The freeze evidence is "PRD.md, במאגר הציבורי", which the committee does not see in the report. The Dirichlet concentration is still not stated. Alternatives still differ in more than the location of compute. See N1. |
| 6 | Privacy claim contradicted (p.27 vs 28; REQSEC11) | 3 | RESOLVED | Table 2.2 now says "0 תמונות שמורות; מחיקה ≤ 60 s". p.27: "במסלול ההמלצה אף חץ אינו מעביר תמונה אל הענן. במסלול ההדמיה התמונה עוברת רק בהסכמה פרטנית לכל הדמיה, מעובדת בזיכרון בלבד, ונמחקת בתוך 60 שניות (REQSEC11)". p.29 repeats it, and the Table 5.5 scale for privacy and the matrix score of 4 match. The text, requirement, figure and matrix now agree. |
| 7 | Work plan: SMART timing, float, missing tasks, ethics | 2 | RESOLVED | SMART goal (1) (p.6): "על מדגם הפיתוח של ניסוי הבסיס (30 משתתפות), והאימות המלא על 120 משתתפות מסתיים בשבוע 11". TSK1.1 is now "גיוס ואתיקה; ניסוי בסיס, 30 משתתפות ... תיוג 500 תמונות עין ו-300 תמונות יד" (Table 6.1). TSK4.2 covers "צבע ומידות" with 60 of the 120 also for measurements. The ethics request is a predecessor in Table 6.3 ("אישור אתיקה") and an immediate action (p.37). The float claim is now explicit: "מנוע הטרנדים מסתיים בשבוע 4 ונדרש לאינטגרציה רק בשבוע 6, והשער מסתיים בשבוע 7 ונדרש לבדיקת העומס רק בשבוע 9". Residual nits: still no person-days per task, and the ethics approval is assumed to come "לפני תחילת הסמסטר". |
| 8 | Risk register: residuals and missing risks | 2 | RESOLVED | Register grows to 8 risks, with new RSKALG07 (P95 above 4.5) and RSKOPS08 (ethics and recruitment delay), and RSKOPS06 now includes "היעדר שותף אמיתי, כי השותף בדוח מדומה" (p.35). Six risks are critical, and each has a mitigation, contingency and residual with its evidence test (Table 7.2: "שיעור הכשל בניסוי הבסיס", "רווח סמך באבן דרך א׳", "אישור בכתב לפני שבוע 1"). The ALG01 contingency no longer abandons the premise: "הדף הלבן מופעל רק אצל המשתמשות שאצלן העין אינה זמינה, וגם אז הוא משלים את העוגן ולא מחליף אותו" (p.36). The summary now says "שציונם השיורי ירד לאזור הבינוני או הנמוך" (p.37), which matches DAT03 = 4. Caveat: the residual reductions rely on tests not yet run (stated openly), and ALG07 keeps P = 2 although the simulated CI straddles the target. |
| 9 | Gap statement not one sharp sentence | 2 | PARTIALLY RESOLVED | New gap (p.16): "הפתרונות הקיימים להדמיה ולהמלצה מניחים שצבעי תמונת הסלפי נכונים, ובמקורות שנסקרו לא נמצאה עבודה שבודקת אם העין, בעזרת לובן העין וצבע עיניים מדווח, יכולה לשמש עוגן לכיול גוון העור בתאורה לא מבוקרת". It is single-themed, tied to H1, scoped to "המקורות שנסקרו", and [41] is now used correctly (Problematization). Sizes and the gate are explicitly excluded from the claim. Still missing: the search protocol is only "מתוכנן כחלק ממשימה TSK1.1", so the negative claim is not yet backed by an executed search (no strings, counts, dates). The sentence is two clauses and long. Table 3.2 still gives the project row five filled circles (unchanged). |
| 10 | Requirement targets without derivation | 2 | PARTIALLY RESOLVED | New "מקור ערכי היעד" paragraph (p.6–7): perceptual threshold; MAE ≤ 1.2 cm is "כשליש ממרווח טיפוסי של 4 cm", with the reference being the mean of two trained measurers and ICC reported; 97% is derived from the fallback rate (< 3%); κ ≥ 0.6 for the stylists; ArcFace 0.88 and LPIPS 0.15 are declared starting values to be updated in week 3 against the reproduced flagship; the IoU target is lowered to 0.90 with 0.94 aspirational. Still missing: the ±4.8 cm baseline (p.5) is still an unsourced "אומדן הצוות", and the claim that body error will drop four-fold has no preliminary evidence. The p.10 sentence "פילוח ציפורניים שעומד ביעד IoU ≥ 0.94 של REQHND04" is unchanged and now contradicts Table 2.2 (0.90). No source for nail IoU feasibility. P@5 sample size is still not stated. |

Status count: RESOLVED 4 (points 1, 6, 7, 8); PARTIALLY RESOLVED 6 (points 2, 3, 4, 5, 9, 10); OPEN 0.

## Other deductions: re-check
- Abstract length: now about 283 words (within 250–350). Fixed.
- p.1 "שיעור ההחזרות בהלבשה מקוונת עומד על 30%–40%": unchanged, still unsourced. OPEN.
- Radar and scatter (p.19–20): caveat added ("הרדאר אינו הוכחה לעליונות, אלא תרגום חזותי של יעדי המפרט"), and the $0.011 session cost is now derived (1 recommendation + 1.7 simulations). The scores and the regression on about 6 team-assigned points remain. PARTIALLY FIXED.
- p.21 data-moat claim: softened to "במקורות שנסקרו לא נמצא מאגר ציבורי כזה ... היתרון הוא בזמן", with the 120-participant replication admitted. Fixed.
- Competitor session costs ($0.003, $0.004, $0.03, $8) and the 8 s A100 estimate: still unsourced team estimates. OPEN.
- Table 5.1 recommendation time now "≤ 1.5 s", consistent with Table 5.6 (1.46 s). Fixed.
- Course booklet [1] cited for factual claims: unchanged. OPEN.
- Immediate actions (p.37): the ethics request was added, so the first action now has substance. The other two are still administrative. PARTIALLY FIXED.

## New weaknesses introduced by the revision
- **N1 (p.25, sev 2):** the matrix paragraph says "בבדיקת הצוות האדום התברר ששני ציונים לא תאמו את הסולם, והם תוקנו: הציון של חלופה 3 ירד מ-4.45 ל-4.30". This is process history of the review leaked into a committee-facing report. It is also an admission that the earlier scores were not scale-based, and it names an internal exercise the committee did not ask to see.
- **N2 (p. ב׳, sev 2):** "כל מספר בדוח מופק מקוד שזמין במאגר הציבורי של הפרויקט, ולכן ניתן לשחזר אותו" is an over-claim. Market inputs, price estimates, literature values and the team's score tables are assumptions, not code outputs. The committee cannot verify the repository from the PDF.
- **N3 (p.6, p.30, sev 1):** hypothesis naming is inconsistent after the H1 split. Table 2.1 and §5.4 still speak of a single "H1", and the summary says "שתי השערות".
- **N4 (p.10 vs p.7, sev 2):** nail IoU target is 0.94 in the literature section and 0.90 in Table 2.2, with an unchanged feasibility claim.
- **N5 (p.17, p.20–21, sev 2):** the ARPU basis does not match the gate economics. ARPU assumes 6 sessions × 2 simulations, with the affiliate leg at 8% click × 4% purchase. The session cost uses 1.7 simulations per session, and Table 4.3 uses a different affiliate conversion (1.8%) and q = 0.5. The ARPU uses neither Eq. 4.1 nor the same parameters. Also 43% of ARPU ($0.30 of $0.69) is a premium subscription ($9.99, 3% uptake) that appears neither in Table 4.4 (segments and revenue models) nor in the architecture.
- **N6 (p.18, sev 2):** inconsistent price per retailer. The SAM uses $0.6M per retailer (3,000 × $0.6M), while the SOM implies $1.2M per retailer (12 retailers, $14.4M = 2M × 12 × $0.60). No explanation is given, and the SOM per-retailer price is double the SAM average.

## Score after upgrades (round 2): 83 / 100

| # | Item | Max | Before | After | Basis |
|---|---|---|---|---|---|
| R1 | Preliminary pages | 8 | 6 | 8 | Abstract about 283 words; all other preliminary elements present. |
| R2 | Page budget | 6 | 6 | 6 | 44 pages; chapters on budget. |
| R3 | Intro as funnel | 5 | 3 | 3 | Unchanged; the 30%–40% figure is still unsourced. |
| R4 | Quantitative problem, RQ vs SMART | 7 | 5 | 6 | Solution row removed from the problem figure; H1a and H1b are testable. Nits remain in Table 2.1. |
| R5 | Requirements table | 8 | 6 | 7 | Derivation paragraph added; ±4.8 cm baseline and the 0.94 vs 0.90 mismatch remain. |
| R6 | Critical review, sources, matrix | 9 | 7 | 7 | Unchanged; the booklet [1] still carries factual claims; the search protocol is deferred. |
| R7 | Flagship paper and gap | 7 | 5 | 6 | Sharper, scoped gap with correct use of [41]; the negative claim is unevidenced. |
| R8 | TAM/SAM/SOM | 5 | 2 | 3 | Bottom-up arithmetic now checks out; all drivers and TAM are unsourced; N5 and N6. |
| R9 | Competitor table, radar, scatter | 6 | 4 | 4 | Caveats added; the underlying scores remain team assessments. |
| R10 | Alternatives, matrix, sensitivity | 9 | 7 | 8 | Anchored scales and score-perturbation test; weights still label-justified; N1. |
| R11 | Architecture and innovation | 5 | 3 | 4 | Privacy contradiction removed. |
| R12 | WBS, RACI, Gantt | 8 | 6 | 7 | Ethics, labelling and body-validation tasks added; float stated; no effort estimates. |
| R13 | Risks | 5 | 4 | 5 | Eight risks, evidence-linked residuals, revised contingency. |
| R14 | Summary and three actions | 2 | 1 | 1 | Summary updated and honest about P95; actions still mostly administrative. |
| R15 | Typography/BiDi/template | 5 | 4 | 4 | No visible defects found; N1 and N2 are content, not typography. |
| R16 | Repository | 5 | 4 | 4 | Not assessable from the PDF; N2 over-claims about it. |
| | **Total** | **100** | **73** | **83** | |

Sign-off is not yet possible. Four points are RESOLVED, six remain PARTIALLY RESOLVED, and the new items N1, N2, N4, N5 and N6 need a fix.


---

## Author response to the round-2 re-check (written by the report authors, NOT an examiner verdict)

All five new items flagged as needing a fix, plus N3, were corrected in chapters and data, then
recompiled (4 passes) and re-audited. Result: 44 pages, 0 errors, detector verdict PASS.

| Item | Fix | Where |
|---|---|---|
| N1 internal review leaked | "בבדיקת הצוות האדום התברר…" replaced with "בבדיקה חוזרת של הציונים מול הסולמות התברר…" | ch5, warning box in §5.2 |
| N2 over-claim | "כל מספר בדוח מופק מקוד" narrowed to "כל התוצאות המחושבות בדוח, מהסימולציה ועד מטריצת ההחלטה" | executive summary |
| N3 H1 naming | Table 2.1 now says H1a/H1b and H0a/H0b (Holm); §5.4 says H1a and H1b | ch2, ch5 |
| N4 nail IoU 0.94 vs 0.90 | the ch3 sentence now refers to the REQ-HND-04 target only (0.90) | ch3 §3.3 |
| N5 ARPU vs gate basis | ARPU now uses the same 1.7 try-ons per session as Table 4.3 (ads $0.08, ARPU $0.68). The text explains the two conversion rates (4 % after choosing a recommendation, 1.8 % after a gate click-through) and states that premium is a third channel and the RSK-BIZ-04 contingency. SOM is recomputed to ≈ $27.4M (SAM ≈ $3.0B) by the script | ch4 §4.1, abstract, ch8 |
| N6 $0.6M vs $1.2M per retailer | explained: average licence for 3,000 mid-size retailers (SAM) vs per-order pricing for 12 tier-1 retailers (SOM) | ch4 §4.1 |

Still open by design (documented, not hidden):
- Market, eCPM, conversion and GPU-utilisation inputs are team assumptions. They will be replaced by sourced values
  (`source_verification_checklist.md`) because web verification was unavailable in this session.
- The ±4.8 cm baseline and the A100 timing are estimates, to be measured in TSK-1.1 and TSK-3.1.
- The systematic search protocol for the gap statement is planned in TSK-1.1, and the gap is scoped to "המקורות שנסקרו".
- The P95 ≤ 4.5 requirement is not yet supported (simulation CI 4.20–5.48). It is a declared open question (RSK-ALG-07).

---

## Iteration 3 (prompts 06-iteration3 and 07): visual red-team pass + lecturer-feedback alignment

**Examiner:** a separate sub-agent (Sonnet) with fresh context. It judged the rendered PDF only (all 44 pages at
70 dpi, zooms on pp. 8, 22 and 34) and was read-only. **Score: 78 / 100** for visual and typographic quality,
with 20 ranked items; several were marked "uncertain" by the examiner because they were seen at low resolution.

### Resolution of the 20 items

| # | Finding (PDF page) | Action | Status |
|---|---|---|---|
| 1 | Table 4.1: lone words wrap; "×" signs dangle at line starts (BiDi) | middle column 4.0 → 4.7 cm; each product chain is one LTR unit (`\en{150M × $0.68 × 12}`); same fix in the ARPU paragraph | fixed |
| 2 | Tables 3.2/3.3: "---" fillers read as unfinished; "--" in last row; lone markers wrap | `\cellno` is now an empty cell (the caption says empty cells are the gap); last row reworded; Table 3.3 columns widened | fixed |
| 3 | Scatter/radar labels small, series hard to tell apart | not changed: zoomed renders show the labels legible; marked uncertain by the examiner | open (minor) |
| 4 | Fig. 2.2 small value labels | not changed this round | open (minor) |
| 5 | Fig. 5.3 dense architecture | not changed this round (page budget) | open (minor) |
| 6 | Fig. 5.4 labels near guide lines | not changed this round | open (minor) |
| 7 | Mockup caption "clipped" | checked at 140 dpi: not clipped (crop artefact of the examiner's render) | not a defect |
| 8 | Gantt labels small | not changed this round (page budget) | open (minor) |
| 9 | Heatmap: R = 10 cell colour | checked: 10 is "medium" (6–11) by the legend, colour correct | not a defect |
| 10 | Funnel band contrast | not changed this round | open (minor) |
| 11 | Venn labels small | Venn already redrawn in v1.4.0 with a clearance search; scaled 0.88 to remove an orphaned heading | partly |
| 12 | Cover: masked IDs; two rules | IDs are masked **by requirement** (master prompt); rules are the cover's design | not a defect |
| 13 | TOC leaders | cosmetic, unchanged | open (cosmetic) |
| 14 | Chapter-end blank space | chapter starts are fixed by the page budget; blank space at a chapter end is by design | not a defect |
| 15 | Tables 5.3/5.4 order 1-3-5 | unchanged: score 1 → 5 left-to-right matches the anchored-scale definition | open (style) |
| 16-17 | Repetitive "Table X shows" openers; intro repeating the box | several restating sentences removed or shortened (Ch. 2, 5); two boxes that duplicated adjacent text removed | fixed |
| 18 | Table 2.2 narrow target column | columns rebalanced (target 2.6 → 3.0 cm), body `\footnotesize` | fixed |
| 19 | Table 4.2 header wraps | intentional `\newline` in two-word names | open (style) |
| 20 | RACI/Table 6.3 comma placement in ID lists | not changed this round | open (minor) |

### Template-level findings from this pass (logged in CHANGELOG [2.0])

- **Orphaned section heading (p. 18):** the automatic `\needspace` before a subsection inserted a legal break
  *between* a section and its first subsection. Fixed in `base-report.cls` with an `\if@nobreak` guard.
- **Early page breaks before headings:** `\needspace` offers TeX a cheap optional break (`\penalty-100` with stretch
  equal to the request). A global rewrite was tried and **reverted** because it broke Chapter 4's float placement;
  the two affected chapter ends were fixed locally instead. Documented as a known limitation.
- **67 → 0 LaTeX warnings:** `fix-cm`, `\pdfstringdefDisableCommands` for the BiDi wrappers, `hypcap=false` for
  `\captionof`, biblatex `standard` → `manual` alias and a Hebrew → English language mapping.

### Lecturer feedback (Assignment 01) addressed in this round

Formal H₀/H₁ (eq. 2.1) with a simulated pilot (Sec. 3.10.5); regression + Bayesian fusion for circumferences
(eq. 5.4, Table 5.5); Monte-Carlo Pugh replayed exactly by `scripts/statistical_validation.py`, whose `--check`
verifies the numbers in the chapters; personal-voice boxes (Ch. 3, Ch. 4); prompt sequence 00–07.

**Not re-scored.** No fresh examiner pass was run after these fixes, so no new score is claimed.
