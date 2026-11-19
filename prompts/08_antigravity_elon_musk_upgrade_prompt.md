# 08 — AURAM rebrand + tier-1 research & venture upgrade (verbatim)

- **Authors:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-19 (seventh user message of the session)
- **Origin:** written after the autonomous red-team audit by Antigravity, whose input prompt Roni committed as
  `prompts/prompt_01_antigravity` (commits 336260d, 265bdfb, 98562a2).
- **Execution record:** `CHANGELOG.md` [3.0], `report/work/qa_fix_log.md` (round 6),
  `report/work/skills_execution_log.md` (round 6), `report/work/red_team_review.md` (iteration 4).

The prompt is reproduced verbatim below.

`````text
MASTER UPGRADE DIRECTIVE: REBRANDING TO AURAM + ELEVATING THE REPORT TO A TIER-1 AI RESEARCH & VENTURE BLUEPRINT

Act as the Principal AI Architect, Lead Biometric Scientist, and Senior Luxury UX Director for our project, which we are officially rebranding from AuraTwin AI to **AURAM** (group roma-ai2, by Roni Offir and Maayan Shiri, Department of Statistics, University of Haifa; Advisor: Dr. Yoram Segal).

First, run `git pull --rebase origin main` so you sync Roni's latest `prompts_antigravity/` commit.
An autonomous tier-1 Red-Team audit (by Antigravity) has exposed critical vulnerabilities in our physical assumptions, business economics, statistical rigor, visual presentation, and student voice, and we are also introducing a signature brand rename (**AURAM**).

Execute a comprehensive, uncompromising upgrade across the entire repository while strictly maintaining:
1. The exact 44-page budget (4 preliminary pages + 40 body pages 1–40; references on 38–40).
2. The LuaLaTeX / biber 4-pass compilation with 0 errors and 0 warnings.
3. Exact data synchronization between `scripts/generate_beauty_benchmarks.py`, `scripts/statistical_validation.py`, `report/figures/data/*.csv`, `stats_summary.json`, and the LaTeX tables/text.
4. Academic tone compliance (Dr. Segal Section 11.2): keep the main body prose in crisp, authoritative third-person Hebrew, and express our personal team voice inside dedicated callout boxes (`examplebox` / `keymessagebox`).
5. Complete Git authorship integrity for Roni Offir and Maayan Shiri.

---

## PILLAR 0: OFFICIAL BRAND RENAME TO "AURAM" (Aura + RAM)
- Globally replace every occurrence of `AuraTwin AI` / `AuraTwin` across the entire repository (`report/coverpage.tex`, `report/main.tex`, `report/auratwin-report.cls`, all `report/chapters/*.tex`, `README.md`, `PRD.md`, `report/figures/`, pocket-mirror logo label, and the App UI Mockup Fig. 5.5) with **AURAM** (styled cleanly with `\en{AURAM}` in Hebrew text).
- Keep the Luxury Vintage Pocket-Mirror logo, updating its brand typography to **AURAM**.
- **Explicit Brand Etymology in the Report:** In Chapter 1 (`ch1_intro.tex`) and in a dedicated personal callout box (`\begin{examplebox}[הבחירה בשם \en{AURAM}: בין הילה אישית לזיכרון חישובי]`), explicitly explain the original portmanteau created by the team: **AURAM** combines **Aura** (personal aura, visual presence, and aesthetic harmony) with **RAM** (Random Access Memory — representing high-speed, real-time retrieval of the user's biometric calibration, anthropometric profile, and live social trend embeddings).

---

## PILLAR 1: PHYSICAL OPTICS, SCLERA CALIBRATION & METAMERISM RIGOR
In `report/chapters/ch2_problem.tex`, `ch3_literature.tex`, and `ch5_alternatives.tex`:
- Cease treating the sclera as an idealized flat white card. Integrate the physiological reality: the sclera is covered by the vascularized episclera and bulbar conjunctiva, subject to sub-clinical redness, age-related lipid/bilirubin deposition (yellowness), and non-Lambertian specular reflections from the tear film.
- Formulate the physical image formation equation under spectral reflectance $S(\lambda)$, illuminant spectrum $E(\lambda)$, and camera spectral sensitivities $Q_k(\lambda)$:
  $$\rho_k = \int_{\Lambda} E(\lambda) S(\lambda) Q_k(\lambda) \, d\lambda + \epsilon_k, \quad k \in \{R,G,B\}$$
- Explicitly explain Metameric Failure: why a simple 3-channel diagonal gain matrix $\mathbf{M} = \text{diag}(\boldsymbol{\ell})$ fails under narrow-band fluorescent or low-CRI LED sources, and how AURAM's Bayesian formulation combines the screen-flash delta ($\Delta \mathbf{I}_{\text{flash}} = \mathbf{I}_{\text{flash}} - \mathbf{I}_{\text{ambient}}$) to isolate ambient illumination from surface reflectance.
- Upgrade `scripts/generate_beauty_benchmarks.py`: replace naive uniform RGB multipliers with simulated standard CIE illuminants ($D_{65}$, Illuminant $A$, $F_{11}$, and narrow-band LED phosphor spectra), and introduce an explicit tear-film specular mask and log-normal vascular redness noise.

---

## PILLAR 2: BUSINESS VIABILITY, UNIT ECONOMICS & ANTI-CHURN REDESIGN
In `report/chapters/ch1_intro.tex`, `ch4_market.tex`, and `ch5_alternatives.tex`:
- Dismantle the "15-second unskippable Rewarded Ad" friction trap (which causes 80%+ conversion drop-off at the decision point) and replace it with a high-conversion, multi-tier value-exchange engine:
  1. Tier 1 (Instant & Free): Real-time edge color-matching and SMPL-X parametric 2D garment silhouette overlay (< 300 ms, zero GPU cost).
  2. Tier 2 (Sponsor-Subsidized Generative VTON): Retailer/brand-sponsored generation (retailers pay $0.02 per try-on as a high-intent engagement SKU fee driving a 3x higher add-to-cart rate).
  3. Tier 3 (Rewarded Value Exchange): Non-intrusive 3-second brand aesthetic micro-interactions, micro-credits earned via post-purchase reviews or closet uploads, or VIP/Pro styling subscription ($7.99/mo).
- Recalculate Eq. 4.1 in `ch4_market.tex`: provide a transparent sensitivity matrix across realistic serverless GPU inference costs ($0.008 to $0.025 including cold starts, queuing, and 20% headroom), model user drop-off curves ($e^{-\beta t}$), and prove $\text{LTV}/\text{CAC} > 3.8$.

---

## PILLAR 3: CREATIVE 10x MOONSHOT & SPATIAL AI INNOVATION
In `report/chapters/ch3_literature.tex` and `ch5_alternatives.tex`:
- Contrast AURAM against obsolete 2D warping (`VITON-HD`) and static diffusion inpainting (`IDM-VTON`).
- Introduce the Next-Gen Spatial Pipeline:
  1. Relightable Neural Garment Avatars: decomposing ambient illumination into spherical harmonics ($L_{lm}$) for Dynamic Environment Re-Lighting ("Office Fluorescent", "Candlelit Evening", "Outdoor Mediterranean Sunlight").
  2. 4D Gaussian Splatting / Neural Cloth Dynamics: volumetric drape and tension mapping along metric body contours.
  3. Autonomous Personal Stylist Agent: a proactive agentic loop connecting calendar events (e.g., job interview, outdoor wedding) and local weather forecasts to personalized SKU selection.

---

## PILLAR 4: ACADEMIC & STATISTICAL CREDIBILITY (STATISTICS MAJOR LEVEL)
In `report/chapters/ch2_problem.tex`, `ch3_literature.tex`, and `scripts/statistical_validation.py`:
- Eliminate reporting astronomical $t$-statistics ($t=30.9, p=10^{-59}$) on synthetic data without qualification.
- Restructure the pilot analysis into a formal Two-Level Hierarchical Mixed-Effects Model:
  $$y_{ij} = \beta_0 + \beta_1 \cdot \text{Method}_{ij} + u_i + v_j + \epsilon_{ij}$$
  where $u_i \sim \mathcal{N}(0, \sigma_{\text{participant}}^2)$ represents participant random effects, $v_j \sim \mathcal{N}(0, \sigma_{\text{light}}^2)$ represents illuminant random effects, and $\epsilon_{ij}$ is heteroscedastic residual error across Fitzpatrick/ITA skin tone brackets.
- Re-run `scripts/statistical_validation.py` to compute empirical statistical power as a function of $N \in [30, 180]$, Cohen's $d \in [0.25, 0.60]$, and intra-class correlation $\text{ICC} \in [0.3, 0.7]$, outputting clean tables in `report/figures/data/` and ensuring exact match across all chapters.

---

## PILLAR 5: DESIGN, VISUAL POLISH & EDITORIAL TYPOGRAPHY
In `report/chapters/`, `report/auratwin-report.cls`, and `report/coverpage.tex`:
- UI Mockup Upgrade (Fig. 5.5): Refactor the TikZ mockup in `ch5_alternatives.tex` into a razor-sharp luxury mobile interface branded **AURAM** with refined micro-typography, sleek pill badges, and our exact palette (`#1E3226` Velvet Forest, `#CCB363` Mustard, `#C27E35` Copper, `#FBEDC3` Egg Nog).
- Chart Typography & BiDi Spacing: Inspect every pgfplots chart (`fig:calib`, `fig:radar`, `fig:scatter`, `fig:stacked`, `fig:sens`) so axis labels, legends, and `nodes near coords` have clean padding and zero overlapping labels.
- Eliminate dangling mathematical operators, isolated punctuation marks, and awkward line breaks in tables (`tab:req`, `tab:compare`, `tab:som`, `tab:mitig`), ensuring centered headers and fixed-width numeric alignment.

---

## PILLAR 6: PERSONAL TEAM VOICE & INTELLECTUAL IDENTITY
In `report/coverpage.tex`, `ch1_intro.tex`, `ch3_literature.tex`, `ch4_market.tex`, and `ch8_summary.tex`:
- Strip away sterile robotic transitions while keeping formal third-person academic style in main prose.
- Infuse the authentic intellectual conviction of Roni Offir and Maayan Shiri inside dedicated callout boxes (`\begin{examplebox}[בקול שלנו: ...]`), explaining why traditional CV engineers fail at beauty (treating skin as an RGB matrix rather than a biological/cultural identity), why **AURAM** captures both aesthetics (Aura) and high-speed computational memory (RAM), and highlighting the personal origin of the idea: standing under bad bathroom lighting, dealing with online return rates, and realizing self-reported eye color is a free Bayesian prior overlooked by computer scientists.

---

## EXECUTION, PROMPT LOGGING & VERIFICATION PROTOCOL
1. Save this prompt verbatim inside `prompts/08_antigravity_elon_musk_upgrade_prompt.md` and update `README.md` (reflecting **AURAM** and ensuring every linked file exists).
2. Execute all edits in `report/chapters/*.tex`, `report/auratwin-report.cls`, `report/coverpage.tex`, `PRD.md`, and `scripts/*.py`.
3. Re-run `python scripts/generate_beauty_benchmarks.py` and `python scripts/statistical_validation.py --check`.
4. Compile the PDF using the 4-pass pipeline (`lualatex -> biber -> lualatex -> lualatex`) and confirm 0 errors, 0 warnings, and exact 44-page count (4 prelim + 40 body).
5. Run `python scripts/qa_detector_audit.py` and `python scripts/readability_math_audit.py` and verify 100% PASS.
6. Refresh PNG previews in `report/figures/previews/` for `README.md`.
7. Stage, commit, and push under dual-author Git identity:
   git add -A
   git commit --author="Roni Offir <ronioffir@gmail.com>" -m "Feat(auram-core): Roni Offir AURAM rebrand, physical optics, hierarchical Bayesian modeling & statistical rigor"
   git commit --allow-empty --author="Maayan Shiri <maayanshiri2002@gmail.com>" -m "Polish(auram-visual-voice): Maayan Shiri AURAM luxury UI overhaul, anti-churn economics & personal team voice"
   git push -u origin main
`````

## Notes on execution (deviations stated openly)

- **Empty commit not used.** An `--allow-empty` commit would attribute the UI/economics/voice work to Maayan
  without containing it. The changes were instead split into two real, non-empty commits, one per author, each
  with the other partner as co-author.
- **"Prove LTV/CAC > 3.8".** The ratio is computed from labelled assumptions, not solved for. The result
  (Table 4.4) holds at every GPU cost up to $0.025 as long as monthly churn is at most 12%, and fails at 20%.
  The report says so.
- **Spectral simulation changed the calibration results.** Under physically based illuminants AURAM reaches
  P95 = 4.25 (meets the 4.5 target) but median = 1.86 (just above 1.8); in the simulated pilot H0b is not
  rejected. This is reported as a result and as risk RSK-ALG-07, not tuned away.
- **Verbatim records left unchanged.** Prompts in `prompts/` and historical logs keep the old brand name;
  internal file/macro names (`auratwin-report.cls`, `\auratwinlogo`) were kept to avoid breaking the build.
