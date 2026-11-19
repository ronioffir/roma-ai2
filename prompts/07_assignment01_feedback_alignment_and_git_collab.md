# 07 — Alignment with the Assignment 01 feedback + two-author Git collaboration (verbatim)

- **Authors:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-19 (sixth user message of the session)
- **Execution record:** `CHANGELOG.md` [2.0] ("Assignment 01 feedback" section),
  `report/work/qa_fix_log.md` (round 5), `report/work/skills_execution_log.md` (round 5),
  `report/work/red_team_review.md` (iteration 3).

The prompt is reproduced verbatim below.

`````text
MANDATORY ALIGNMENT WITH LECTURER FEEDBACK FROM ASSIGNMENT 01 + DUAL-AUTHOR GIT COLLABORATION

Before finalizing and pushing `https://github.com/RONIOFFIR/roma-ai2.git`, audit and upgrade the project against **every single feedback point** our lecturer (Dr. Yoram Segal) gave us on Assignment 01 (remember: from this submission onward, Git collaboration and prompt logging are directly graded):

1. **Deep Integration with Our Field of Study — Statistics (החוג לסטטיסטיקה, אוניברסיטת חיפה):**
- Do NOT treat AuraTwin AI as pure software engineering alone. Ground the report deeply in **Statistical Modeling & Quantitative Inference** reflecting our Statistics degree:
- In Chapter 2 & Chapter 3: Formulate formal **statistical hypotheses ($H_0$ vs. $H_1$)** for the Self-Supervised Color Calibration (e.g., paired comparison of $\Delta E_{00}$ color error before vs. after eye-anchor calibration using a paired $t$-test / Wilcoxon signed-rank test, with 95% confidence intervals and $\alpha = 0.05$).
- In Chapter 4 & Chapter 5: Model anthropometric circumference estimation as a **multivariate regression / Bayesian prior fusion** combining noisy 2D monocular keypoints with user-reported tabular covariates (height, weight, circumferences), reporting MAE, RMSE, $R^2$, and residual variance.
- Include a **Monte Carlo / Weight-Perturbation Sensitivity Analysis** in Chapter 5 on the Pugh Decision Matrix to statistically prove that Alternative 3 wins robustly under weight uncertainty.

2. **Real Python Code Actually Driving the Report (`scripts/`):**
- Ensure our Python scripts in `scripts/` (`generate_beauty_benchmarks.py`, `statistical_validation.py`, `qa_detector_audit.py`) are **actually executed**, produce real `.csv` / `.json` data tables and `.png` outputs, and that the numbers inside our LaTeX `pgfplots` charts and tables in Chapters 2, 4, 5, and 7 match those Python-generated outputs 100%. Document how the Python pipeline drives the report inside `README.md`.

3. **Real, Numbered, Rich Prompt Sequence in `prompts/` (NO Thin Prompts, NO Broken Links):**
- Ensure `prompts/` contains a **complete, chronologically numbered sequence** (`00_...` through `07_...`) of the **actual, full-length prompts** showing how Roni and Maayan steered, corrected, and Red-Teamed the LLM step by step (including the initial 40-page Master Prompt, the UX & Luxury Vintage Rejects Prompt, the Pocket-Mirror Logo & Red-Team Polish Prompt, and this Feedback Alignment Prompt).
- **CRITICAL CHECK:** Verify that EVERY single file path and prompt filename mentioned in `README.md` actually exists in the repository (zero broken links or phantom filenames!).

4. **Professional `README.md` with Verified Real Screenshots:**
- Every screenshot/image embedded in `README.md` (Pocket-Mirror Logo, Cover Page, UX Mockup, Radar/Scatter plots, Architecture, Gantt, Risk Heatmap) MUST exist at the exact relative path in `report/figures/previews/` and render cleanly on GitHub.

5. **Creativity, Originality & Personal Voice:**
- Preserve our distinct personal voice as Statistics students & Beauty-Tech entrepreneurs inside dedicated callout boxes (`examplebox` / `keymessagebox`), highlighting our original insights from class (human-reported eye color as a spectral calibration anchor, Ad-Gated GPU economics, and the everyday aesthetic need for women, teenage girls, and men).

6. **Dual-Author Git History & Collaboration (`ronioffir@gmail.com` + `maayanshiri2002@gmail.com`):**
- The lecturer explicitly penalized having all pushes/commits from a single partner. Ensure **both** Roni Offir and Maayan Shiri appear clearly in commits and GitHub Contributors:
- Commit Roni's statistical/architectural/prompt updates using:
`git commit --author="Roni Offir <ronioffir@gmail.com>" -m "Feat(stats-arch): Roni Offir statistical hypothesis testing, Pugh sensitivity & prompt logs"`
- Commit Maayan's UX, luxury pocket-mirror design, Python benchmark/QA runs & Red-Team polish using:
`git commit --author="Maayan Shiri <maayanshiri2002@gmail.com>" -m "Polish(ux-mirror-qa): Maayan Shiri pocket-mirror logo, UX flow, Python validation & Red-Team QA"`
- Include BOTH co-author trailers on joint commits:
```
Co-authored-by: Roni Offir <ronioffir@gmail.com>
Co-authored-by: Maayan Shiri <maayanshiri2002@gmail.com>
```
- Save this prompt as `prompts/07_assignment01_feedback_alignment_and_git_collab.md`, run `git pull --rebase origin main`, push to `origin main`, and run `git log -n 6` to verify both authors and all files are live on GitHub!
`````

## How each point was executed

| # | Point | Result |
|---|---|---|
| 1a | H₀ vs H₁ (Ch. 2–3) | eq. 2.1, formal H₀a/H₁a (paired difference) and H₀b/H₁b (threshold 1.8); Wilcoxon + paired *t* + 95% CI, Holm, α = 0.05; simulated pilot run in Sec. 3.10.5 |
| 1b | Regression / Bayesian fusion | Ch. 5 Sec. 5.3.2: eq. 5.4 (precision-weighted fusion) and Table 5.5 (MAE, RMSE, R², residual variance, 3 models) |
| 1c | Monte-Carlo Pugh | Ch. 5 Sec. 5.2.4: 20,000 Dirichlet draws (Alt 3 wins 100%, 5th-pct margin 0.47) + uniform weights (89.2%); exact replay in `statistical_validation.py` |
| 2 | Python drives the report | new `scripts/statistical_validation.py` (JSON/CSV/PNG + `--check` of the numbers in the chapters: PASS); `generate_beauty_benchmarks.py` re-run, CSVs byte-identical |
| 3 | Prompt sequence + links | 00–07 present; every README path checked (0 missing) |
| 4 | README screenshots | 19 previews regenerated at 150 dpi from the final PDF + 3 Python plots |
| 5 | Personal voice | examplebox "בקול שלנו" (Ch. 4) + examplebox "כסטודנטיות לסטטיסטיקה" (Ch. 3) |
| 6 | Two-author history | separate `--author` commits for Roni and Maayan, joint co-author trailers |
