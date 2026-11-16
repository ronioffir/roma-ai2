---
name: beauty-ai-domain-architect
description: Formulates the mathematics, system architecture and unit economics of AuraTwin AI — CIELAB ΔE00 calibration with a user-reported eye colour as a spectral prior, SMPL-X anthropometric ratio vectors, social trend velocity scoring, the Pugh weighted decision matrix with sensitivity analysis, and ad-gated / affiliate unit economics. Use when writing chapters 2, 3, 5 or 7 or when checking equations and numbers.
---

# Beauty-AI Domain Architect (אדריכל המערכת והאלגוריתמיקה)

## Canonical equations (use these symbols everywhere — consistency is graded)
1. Colour-difference metric: $\Delta E_{00}$ (CIEDE2000, Sharma et al. 2005). Perception threshold ≈ 2.0.
2. Illumination model (von Kries / diagonal + 3×3 correction):
   $\mathbf{c}_{\text{obs}} = \mathbf{M}\,\mathbf{c}_{\text{true}} + \boldsymbol{\epsilon}$;
   estimate $\hat{\mathbf{M}}$ by minimising
   $\mathcal{L}(\mathbf{M}) = \sum_{k\in\mathcal{A}} \lambda_k \,\Delta E_{00}\big(\mathbf{M}^{-1}\mathbf{c}^{(k)}_{\text{obs}},\ \boldsymbol{\mu}^{(k)}_{\text{prior}}\big) + \gamma \lVert \mathbf{M}-\mathbf{I}\rVert_F^2$,
   where the anchor set $\mathcal{A}$ = {sclera (neutral), iris (user-reported category prior), teeth (optional)}.
3. Bayesian fusion of the self-reported eye colour: prior $p(\mathbf{c}_{\text{iris}}\mid \text{label})=\mathcal{N}(\boldsymbol{\mu}_\ell,\boldsymbol{\Sigma}_\ell)$ in CIELAB.
4. Anthropometry: SMPL-X shape $\boldsymbol{\beta}\in\mathbb{R}^{10}$; ratio vector
   $\mathbf{r} = (C_{\text{chest}}, C_{\text{waist}}, C_{\text{hip}}, L_{\text{inseam}}) / H$, scaled by the user-reported height $H$.
   Metric: MAE in cm against tape measurement.
5. Trend velocity: $v_t(s) = \frac{d}{dt}\log\big(1+n_t(s)\big)$ with exponential smoothing; trend score
   $T(s) = \alpha\, \tilde v_t(s) + (1-\alpha)\, \tilde e_t(s)$ (engagement), freshness ≤ 6 h.
6. Pugh: $S_j=\sum_{i=1}^{n} w_i c_{ij}$, $\sum_i w_i = 1.00$, $c_{ij}\in\{1..5\}$; sensitivity: perturb each
   $w_i$ by ±0.05/±0.10 with renormalisation and report the rank stability.
7. Unit economics of the ad gate: margin per generation
   $\pi = \text{eCPM}_{\text{rew}}/1000 + p_{\text{conv}}\cdot \text{AOV}\cdot r_{\text{aff}} - C_{\text{GPU}}$; requirement ARPU > 2.4 × GPU cost.
8. Risk: $R = P \times I$, critical if $R \ge 12$.

## Architecture of the selected alternative (Alternative 3 — hybrid split compute)
Edge (on-device): face/iris/sclera landmarks, calibration $\hat{\mathbf M}$, hand & nail segmentation,
2D keypoints → server only receives calibrated colour vectors + keypoints (privacy by design).
Cloud: SMPL-X fitting, vector RAG (CLIP embeddings + FAISS) over catalogue + trend knowledge graph,
trend miner, ad-gate / affiliate router, latent-diffusion try-on (only after the gate opens).

## Rules
- Every number in the report must be consistent with these definitions and with Table 2.2 (REQs).
- Illustrative or simulated values are labelled as such ("נתונים מדומים / להמחשה").
