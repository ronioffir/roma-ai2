# Benchmarks summary (seed 2026)

## Calibration simulation (spectral v3, n=4000 synthetic selfies, CIEDE2000 on skin)

| method | mean | median | p95 | % <= 2.0 |
|---|---|---|---|---|
| Uncorrected camera | 6.58 | 6.22 | 12.40 | 5.0 |
| Gray-world AWB | 16.03 | 15.97 | 24.17 | 0.0 |
| Sclera anchor (diagonal, no mask) | 2.66 | 2.29 | 5.88 | 43.0 |
| Sclera + iris prior (diagonal, masked) | 2.72 | 2.31 | 6.05 | 42.2 |
| Flash delta only | 2.53 | 2.22 | 5.25 | 42.9 |
| AURAM: flash delta + eye anchor (Bayesian) | 2.08 | 1.86 | 4.25 | 55.2 |

## Pugh matrix

- Alt1 Edge: 3.40
- Alt2 Cloud LLM: 2.85
- Alt3 Hybrid: 4.30

Extreme booklet check (latency 0.45, cost 0.00): {'Alt1 Edge': 2.676923076923077, 'Alt2 Cloud LLM': 2.396153846153846, 'Alt3 Hybrid': 4.253846153846154}

One-at-a-time +-0.05/0.10: winner always Alt3 = True

Dirichlet(40*w) Monte-Carlo: Alt3 wins 100.0% ; 5th pct margin 0.47
Uniform-random weights: Alt3 wins 89.6%

Previous scores (v1, before red-team re-anchoring): {'Alt1 Edge': 3.1500000000000004, 'Alt2 Cloud LLM': 2.85, 'Alt3 Hybrid': 4.45}

Score sensitivity: 28 single +-1 score changes, winner flips 0; smallest margin 0.65 at Alt1 Edge/acc+1
Adversarial double change (Alt3 -1 on acc & cost, Alt1 +1 on lat & real): {'Alt1 Edge': 3.7, 'Alt2 Cloud LLM': 2.85, 'Alt3 Hybrid': 3.85}

## Median error by illuminant family (metameric failure of diagonal anchors)

| method | D65 | A | F11 | LED |
|---|---|---|---|---|
| Sclera anchor (diagonal, no mask) | 1.30 | 1.84 | 2.79 | 3.33 |
| Sclera + iris prior (diagonal, masked) | 1.18 | 2.09 | 2.77 | 3.30 |
| Flash delta only | 2.19 | 2.33 | 2.15 | 2.21 |
| AURAM: flash delta + eye anchor (Bayesian) | 1.31 | 1.91 | 2.08 | 2.22 |

Fusion error models (fitted on the seed-99 training simulation): var_a0=0.00062, var_a1=0.0113, flash scale=0.945

## Calibration by skin-tone subgroup (proposed method)

- light (ITA>41): n=1089, median 2.47, p95 4.35
- intermediate (10<ITA<=41): n=1203, median 1.52, p95 3.28
- tan/brown (ITA<=10): n=1708, median 1.79, p95 4.56

## Power (from simulation)

{'dz_capture': 1.311503766848837, 'dz_participant': 1.6589356252531022, 'n_planning': 56, 'power_threshold_test': np.float64(0.01), 'p95_ci': (3.898912646908245, 4.508516250683063)}

## Unit economics

{'base': {'beta': 0.10729586082894003, 'keep_micro': 0.7247796636776955, 'keep_ad': 0.19999999999999998, 'req': 10.2, 'n_gen': 9.077101027804996, 'uplift': 0.10400000000000001, 'rev_aff': 0.29952, 'rev_gen': 1.0900753151141598, 'rev_sub': 0.20374499999999998, 'revenue': 1.5933403151141599, 'cost': 0.14815651541707495, 'margin': 1.4451837996970849, 'gross_margin': 0.9070151467256009, 'ltv': 12.043198330809041, 'ltv_cac': 6.0215991654045204, 'per_tryon_rev': 0.12009068884162889, 'biz12_ratio': 8.00604592277526, 'gpu_cost': 0.015, 'churn': 0.12}, 'grid': [(0.008, 0.08, 9.429521918073249), (0.008, 0.12, 6.2863479453821665), (0.008, 0.2, 3.7718087672292997), (0.015, 0.08, 9.03239874810678), (0.015, 0.12, 6.0215991654045204), (0.015, 0.2, 3.612959499242712), (0.025, 0.08, 8.465079933868969), (0.025, 0.12, 5.643386622579313), (0.025, 0.2, 3.3860319735475874)], 'worst_biz12': 4.803627553665155}

## Market build-up

{'arpu': 1.5933403151141599, 'b2b_som': 14400000.0, 'b2c_som': 30592134.05019187, 'som': 44992134.05019187, 'b2b_sam': 1800000000, 'b2c_sam': 2868012567.2054877, 'sam': 4668012567.205488}
