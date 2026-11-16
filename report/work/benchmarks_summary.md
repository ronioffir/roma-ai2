# Benchmarks summary (seed 2026)

## Calibration simulation (n=4000 synthetic selfies, CIEDE2000 on skin)

| method | mean | median | p95 | % <= 2.0 |
|---|---|---|---|---|
| Uncorrected camera | 4.89 | 4.68 | 8.89 | 8.1 |
| Gray-world AWB | 9.77 | 9.75 | 14.13 | 0.0 |
| Sclera anchor | 2.82 | 2.46 | 6.03 | 37.0 |
| Sclera + iris prior | 2.74 | 2.41 | 5.79 | 38.0 |
| Enrolment + iris prior (AuraTwin) | 1.82 | 1.37 | 4.81 | 69.6 |

## Pugh matrix

- Alt1 Edge: 3.40
- Alt2 Cloud LLM: 2.85
- Alt3 Hybrid: 4.30

Extreme booklet check (latency 0.45, cost 0.00): {'Alt1 Edge': 2.676923076923077, 'Alt2 Cloud LLM': 2.396153846153846, 'Alt3 Hybrid': 4.253846153846154}

One-at-a-time +-0.05/0.10: winner always Alt3 = True

Dirichlet(40*w) Monte-Carlo: Alt3 wins 100.0% ; 5th pct margin 0.47
Uniform-random weights: Alt3 wins 89.2%

Previous scores (v1, before red-team re-anchoring): {'Alt1 Edge': 3.1500000000000004, 'Alt2 Cloud LLM': 2.85, 'Alt3 Hybrid': 4.45}

Score sensitivity: 28 single +-1 score changes, winner flips 0; smallest margin 0.65 at Alt1 Edge/acc+1
Adversarial double change (Alt3 -1 on acc & cost, Alt1 +1 on lat & real): {'Alt1 Edge': 3.7, 'Alt2 Cloud LLM': 2.85, 'Alt3 Hybrid': 3.85}

## Calibration by skin-tone subgroup (proposed method)

- light (ITA>41): n=1139, median 1.61, p95 5.68
- intermediate (10<ITA<=41): n=1483, median 1.34, p95 4.79
- tan/brown (ITA<=10): n=1378, median 1.26, p95 4.04

## Power (from simulation)

{'dz_capture': 1.2542418930646324, 'dz_participant': 1.5865044475542336, 'n_planning': 56, 'power_threshold_test': np.float64(1.0), 'p95_ci': (4.204645809486159, 5.475875522939361)}

## Unit economics

{'rev_ad': 0.015, 'rev_aff': 0.0936, 'rev_mix': 0.0543, 'ratio_api_low': 1.2066666666666668, 'ratio_api_high': 0.6033333333333334, 'self_hosted_cost': 0.005333333333333334, 'ratio_self_hosted': 10.181249999999999, 'cost_ceiling_2_4': 0.022625000000000003, 'gross_margin_at_2_4': 0.5833333333333333, 'stress_rev': 0.03333, 'stress_ratio': 6.249374999999999, 'rag_query_cost': 0.002}

## Market build-up

{'arpu_aff': 0.29952, 'arpu_ads': 0.0765, 'arpu_prem': 0.2997, 'arpu': 0.6757200000000001, 'b2b_som': 14400000.0, 'b2c_som': 12973824.000000004, 'som': 27373824.000000004, 'b2b_sam': 1800000000, 'b2c_sam': 1216296000.0000002, 'sam': 3016296000.0}
