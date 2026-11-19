"""statistical_validation.py -- statistical layer of the AuraTwin AI report (group roma-ai2).

Three analyses, all seeded and reproducible. Every number quoted in the report text comes from
report/figures/data/stats_summary.json, and `--check` verifies that the LaTeX sources contain them.

  A. Paired hypothesis test of the eye-anchor calibration (report Ch.2 Sec. 2.2 (hypotheses, eq. 2.x) and Ch.3 Sec. 3.10.5 (results)):
     a simulated pilot of the planned study, n = 120 participants x 4 illuminants, drawn from
     the 4,000-selfie calibration simulation of generate_beauty_benchmarks.py. The analysis unit is
     the participant mean of the paired difference d_i = DeltaE00(camera) - DeltaE00(AuraTwin).
       H0a: median(d) <= 0      vs  H1a: median(d) > 0      (Wilcoxon signed-rank, one-sided)
       H0b: median(DeltaE00) >= 1.8  vs  H1b: median < 1.8  (cluster bootstrap, one-sided 95% bound)
     A paired t-test and its 95% CI are reported alongside; Holm correction over {H1a, H1b}, alpha = 0.05.
  B. Anthropometric circumference model (report Ch.5, Sec. 5.3): waist circumference estimated from
     (1) noisy monocular 2D keypoints only, (2) an OLS regression on self-reported covariates
     (height, weight, BMI), and (3) a Bayesian precision-weighted fusion of the regression prior,
     the multi-frame keypoint estimate and a self-reported tape measurement. Out-of-sample MAE, RMSE,
     R^2 and residual variance on a 30% hold-out.
  C. Monte-Carlo weight perturbation of the Pugh matrix (report Ch.5, Sec. 5.2.4): replays the exact
     random stream of generate_beauty_benchmarks.py (seed 2026), so the figures in the report are the
     same draws -- Dirichlet(40 w), 20,000 weight vectors, plus 20,000 uniform weight vectors.

Synthetic data only: the parameters are design assumptions stated in the report, not measurements.

Usage:  python scripts/statistical_validation.py            # compute, write CSV/JSON/PNG
        python scripts/statistical_validation.py --check    # also verify the numbers in the .tex files
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_beauty_benchmarks as gb  # noqa: E402

DATA = ROOT / "report" / "figures" / "data"
PLOTS = ROOT / "report" / "figures" / "stats"
CHAP = ROOT / "report" / "chapters"
PAL = {"forest": "#1E3226", "garnet": "#76290B", "copper": "#C27E35", "mustard": "#CCB363",
       "dust": "#6F7D7B", "eggnog": "#FBEDC3"}


# ------------------------------------------------------------------ A. paired test
def paired_pilot(cal, rng, n_part=120, n_light=4, boot=4000):
    cam = cal["Uncorrected camera"]
    aur = cal["Enrolment + iris prior (AuraTwin)"]
    idx = rng.integers(0, len(cam), (n_part, n_light))          # captures of each participant
    d = (cam[idx] - aur[idx]).mean(1)                            # participant-level paired difference
    t = stats.ttest_1samp(d, 0.0, alternative="greater")
    ci = stats.t.interval(0.95, n_part - 1, loc=d.mean(), scale=stats.sem(d))
    w = stats.wilcoxon(d, alternative="greater")
    dz = d.mean() / d.std(ddof=1)
    # H1b: pooled capture-level median of AuraTwin < 1.8, cluster bootstrap over participants
    a = aur[idx]
    meds = np.array([np.median(a[rng.integers(0, n_part, n_part)].ravel()) for _ in range(boot)])
    upper95 = float(np.percentile(meds, 95))
    p_b = float((meds >= 1.8).mean())                            # bootstrap one-sided p-value
    p = np.array([w.pvalue, p_b])
    order = np.argsort(p)
    holm = np.empty(2)
    holm[order[0]] = min(1.0, 2 * p[order[0]])
    holm[order[1]] = min(1.0, max(holm[order[0]], p[order[1]]))
    out = {"n": n_part, "n_light": n_light, "mean_diff": float(d.mean()), "sd_diff": float(d.std(ddof=1)),
           "ci95_low": float(ci[0]), "ci95_high": float(ci[1]), "t": float(t.statistic), "df": n_part - 1,
           "p_t": float(t.pvalue), "wilcoxon_W": float(w.statistic), "p_wilcoxon": float(w.pvalue),
           "dz": float(dz), "median_aur": float(np.median(a)), "median_upper95": upper95,
           "p_h1b": p_b, "holm_h1a": float(holm[0]), "holm_h1b": float(holm[1]),
           "reject_h0a": bool(holm[0] < 0.05), "reject_h0b": bool(holm[1] < 0.05)}
    return out, d


# --------------------------------------------------- B. circumference regression + fusion
def circumference_model(rng, n=2000):
    female = rng.random(n) < 0.6
    height = np.where(female, rng.normal(164, 6.5, n), rng.normal(177, 7.0, n))       # cm
    bmi = np.clip(rng.lognormal(np.log(23.5), 0.15, n), 16, 40)
    weight = bmi * (height / 100) ** 2                                                 # kg
    waist = 18 + 2.25 * bmi + 0.12 * height + 4.0 * (~female) + rng.normal(0, 3.4, n)  # true waist, cm
    # observations
    h_rep = height + rng.normal(0, 1.0, n)                 # self-reported height
    w_rep = weight + rng.normal(0, 1.5, n)                 # self-reported weight
    tape = waist + rng.normal(0, 1.5, n)                   # self-reported tape measurement
    kp = waist[:, None] + 1.0 + rng.normal(0, 3.0, (n, 3))         # 3 monocular frames, +1 cm silhouette bias
    kp_mean = kp.mean(1)
    tr = rng.random(n) < 0.7
    te = ~tr
    bmi_rep = w_rep / (h_rep / 100) ** 2
    X = np.column_stack([np.ones(n), h_rep, w_rep, bmi_rep, (~female).astype(float)])
    beta, *_ = np.linalg.lstsq(X[tr], waist[tr], rcond=None)
    pred_reg = X @ beta
    s2_reg = float(np.var(waist[tr] - pred_reg[tr], ddof=X.shape[1]))
    # keypoint model: bias removed with the training mean residual; variance from training residuals
    bias_kp = float(np.mean(kp_mean[tr] - waist[tr]))
    pred_kp = kp_mean - bias_kp
    s2_kp = float(np.var(waist[tr] - pred_kp[tr], ddof=1))
    s2_tape = float(np.var(waist[tr] - tape[tr], ddof=1))
    prec = np.array([1 / s2_reg, 1 / s2_kp, 1 / s2_tape])
    pred_fus = (prec[0] * pred_reg + prec[1] * pred_kp + prec[2] * tape) / prec.sum()
    post_sd = float(np.sqrt(1 / prec.sum()))

    def metr(pred):
        e = waist[te] - pred[te]
        return {"MAE": float(np.mean(np.abs(e))), "RMSE": float(np.sqrt(np.mean(e ** 2))),
                "R2": float(1 - np.sum(e ** 2) / np.sum((waist[te] - waist[te].mean()) ** 2)),
                "resid_var": float(np.var(e, ddof=1))}
    res = {"keypoints": metr(pred_kp), "regression": metr(pred_reg), "fusion": metr(pred_fus)}
    res["meta"] = {"n": n, "n_test": int(te.sum()), "beta": [float(b) for b in beta],
                   "sigma_reg": float(np.sqrt(s2_reg)), "sigma_kp": float(np.sqrt(s2_kp)),
                   "sigma_tape": float(np.sqrt(s2_tape)), "posterior_sd": post_sd,
                   "weights": [float(p / prec.sum()) for p in prec]}
    return res, waist[te], pred_fus[te], pred_kp[te]


# ------------------------------------------------------------- C. Monte-Carlo Pugh
def pugh_montecarlo():
    """Replay generate_beauty_benchmarks.main()'s random stream exactly (seed 2026)."""
    rng = np.random.default_rng(2026)
    cal = gb.calibration_study(rng)
    cal.pop("_ita")
    gb.power_from_simulation(cal, rng)
    state = rng.bit_generator.state
    rows, extreme, win, margin5, win2 = gb.sensitivity(rng)
    rng.bit_generator.state = state                       # same draws again, keep the full distribution
    base = np.array([c[3] for c in gb.CRITERIA])
    # sensitivity() draws nothing before its Dirichlet sample, so the restored stream yields the same W
    W = rng.dirichlet(base * 40, 20000)
    S = W @ np.array(list(gb.ALTERNATIVES.values()), float).T
    margin = S[:, 2] - S[:, :2].max(1)
    assert abs((S.argmax(1) == 2).mean() - win) < 1e-12
    return {"draws": 20000, "dirichlet_conc": 40, "p_win_alt3": float(win), "margin_p5": float(margin5),
            "margin_mean": float(margin.mean()), "p_win_uniform": float(win2)}, margin, cal


# ----------------------------------------------------------------- outputs + checks
def write_plots(d, pilot, waist_te, fus_te, kp_te, margin):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib missing: PNG plots skipped")
        return
    PLOTS.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": PAL["dust"]})
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=160)
    ax.hist(d, bins=22, color=PAL["copper"], edgecolor="white")
    ax.axvline(0, color=PAL["garnet"], ls="--", lw=1.2, label="H0: no improvement")
    ax.axvspan(pilot["ci95_low"], pilot["ci95_high"], color=PAL["forest"], alpha=0.25, label="95% CI of mean")
    ax.set_xlabel("paired difference  ΔE00(camera) − ΔE00(AuraTwin)")
    ax.set_ylabel("participants")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(PLOTS / "paired_test.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(4.4, 4.0), dpi=160)
    ax.scatter(waist_te, kp_te, s=7, color=PAL["dust"], alpha=0.55, label="keypoints only")
    ax.scatter(waist_te, fus_te, s=7, color=PAL["copper"], alpha=0.8, label="Bayesian fusion")
    lo, hi = waist_te.min() - 2, waist_te.max() + 2
    ax.plot([lo, hi], [lo, hi], color=PAL["forest"], lw=1)
    ax.set_xlabel("true waist (cm)"); ax.set_ylabel("estimated waist (cm)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(PLOTS / "circumference_fusion.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2, 3.0), dpi=160)
    ax.hist(margin, bins=40, color=PAL["forest"], edgecolor="white")
    ax.axvline(0, color=PAL["garnet"], ls="--", lw=1.2, label="Alt 3 would lose")
    ax.axvline(np.percentile(margin, 5), color=PAL["mustard"], lw=1.6, label="5th percentile")
    ax.set_xlabel("winning margin of Alt 3 (points), 20,000 Dirichlet weight draws")
    ax.set_ylabel("draws"); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(PLOTS / "pugh_montecarlo.png"); plt.close(fig)


def tex_checks(s):
    """(formatted value, chapter file) pairs that must appear verbatim in the LaTeX."""
    p, c, m = s["paired_test"], s["circumference"], s["pugh_montecarlo"]
    f2 = lambda x: f"{x:.2f}"
    return [
        (f2(p["mean_diff"]), "ch3_literature.tex"), (f2(p["ci95_low"]), "ch3_literature.tex"),
        (f2(p["ci95_high"]), "ch3_literature.tex"), (f"{p['t']:.1f}", "ch3_literature.tex"),
        (f2(p["dz"]), "ch3_literature.tex"), (f2(p["median_upper95"]), "ch3_literature.tex"),
        (f2(c["keypoints"]["MAE"]), "ch5_alternatives.tex"), (f2(c["regression"]["MAE"]), "ch5_alternatives.tex"),
        (f2(c["fusion"]["MAE"]), "ch5_alternatives.tex"), (f2(c["fusion"]["RMSE"]), "ch5_alternatives.tex"),
        (f2(c["fusion"]["R2"]), "ch5_alternatives.tex"), (f2(c["fusion"]["resid_var"]), "ch5_alternatives.tex"),
        (f2(c["regression"]["R2"]), "ch5_alternatives.tex"), (f2(c["keypoints"]["R2"]), "ch5_alternatives.tex"),
        (f"{m['p_win_uniform'] * 100:.1f}", "ch5_alternatives.tex"), (f2(m["margin_p5"]), "ch5_alternatives.tex"),
        ("20,000", "ch5_alternatives.tex"),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify the numbers in the LaTeX chapters")
    args = ap.parse_args()

    mc, margin, cal = pugh_montecarlo()
    pilot, d = paired_pilot(cal, np.random.default_rng(2027))
    circ, waist_te, fus_te, kp_te = circumference_model(np.random.default_rng(2028))
    summary = {"seed": {"pugh_and_calibration": 2026, "paired_pilot": 2027, "circumference": 2028},
               "paired_test": pilot, "circumference": circ, "pugh_montecarlo": mc}

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "stats_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    np.savetxt(DATA / "paired_differences.csv", d, delimiter=",", header="d_participant", comments="", fmt="%.4f")
    with open(DATA / "circumference_metrics.csv", "w", encoding="utf-8") as f:
        f.write("model,MAE,RMSE,R2,resid_var\n")
        for k in ("keypoints", "regression", "fusion"):
            r = circ[k]
            f.write(f"{k},{r['MAE']:.3f},{r['RMSE']:.3f},{r['R2']:.3f},{r['resid_var']:.3f}\n")
    hist, edges = np.histogram(margin, bins=40)
    with open(DATA / "pugh_montecarlo.csv", "w", encoding="utf-8") as f:
        f.write("margin_lo,margin_hi,draws\n")
        for h, a, b in zip(hist, edges[:-1], edges[1:]):
            f.write(f"{a:.4f},{b:.4f},{h}\n")
    write_plots(d, pilot, waist_te, fus_te, kp_te, margin)

    p, c = pilot, circ
    print(f"A  paired pilot n={p['n']}: mean d={p['mean_diff']:.2f} 95% CI [{p['ci95_low']:.2f}, {p['ci95_high']:.2f}]"
          f"  t({p['df']})={p['t']:.1f} p={p['p_t']:.1e}  Wilcoxon W={p['wilcoxon_W']:.0f} p={p['p_wilcoxon']:.1e}"
          f"  dz={p['dz']:.2f}  median={p['median_aur']:.2f} upper95={p['median_upper95']:.2f}"
          f"  Holm: H0a {p['reject_h0a']}, H0b {p['reject_h0b']} (p_b={p['p_h1b']:.4f})")
    for k in ("keypoints", "regression", "fusion"):
        r = c[k]
        print(f"B  {k:10s} MAE={r['MAE']:.2f} RMSE={r['RMSE']:.2f} R2={r['R2']:.2f} resid_var={r['resid_var']:.2f}")
    print(f"B  sigmas reg/kp/tape = {c['meta']['sigma_reg']:.2f}/{c['meta']['sigma_kp']:.2f}/"
          f"{c['meta']['sigma_tape']:.2f}  weights={[round(w, 2) for w in c['meta']['weights']]}"
          f"  posterior sd={c['meta']['posterior_sd']:.2f}")
    print(f"C  Pugh MC: Alt3 wins {mc['p_win_alt3']*100:.1f}%  margin p5={mc['margin_p5']:.2f}"
          f"  mean={mc['margin_mean']:.2f}  uniform weights: {mc['p_win_uniform']*100:.1f}%")

    if args.check:
        bad = [(v, f) for v, f in tex_checks(summary) if v not in (CHAP / f).read_text(encoding="utf-8")]
        for v, f in bad:
            print(f"MISSING in {f}: {v}")
        print("NUMBER CHECK:", "PASS" if not bad else f"FAIL ({len(bad)} missing)")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
