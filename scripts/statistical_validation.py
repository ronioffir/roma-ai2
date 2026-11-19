"""statistical_validation.py -- statistical layer of the AURAM report (group roma-ai2).

Every number quoted in the report's statistical passages comes from
report/figures/data/stats_summary.json; `--check` verifies that the LaTeX chapters contain them.

  A. Simulated pilot of the planned study (report Ch.2 Sec. 2.2, Ch.3 Sec. 3.10.5):
     120 participants x 4 illuminant families (D65, A, F11, LED), both methods on every capture,
     drawn from the spectral simulation of generate_beauty_benchmarks.py. Persistent person traits
     make captures of the same person correlated (the v2 pilot drew them independently and
     inflated the effect -- the "t = 30.9" problem).
       Two-level crossed mixed-effects model
           y_ij = b0 + b1*Method_ij + u_i + v_j + e_ij,   u_i ~ N(0, s2_part), v_j ~ N(0, s2_light)
       H0a: b1 >= 0 vs H1a: b1 < 0 (AURAM lowers the error)  -- Wald test, 95% CI
       H0b: median error of AURAM >= 1.8 vs H1b: < 1.8       -- cluster bootstrap, one-sided 95% bound
       Holm over {H1a, H1b}, alpha = 0.05. Residual SD per ITA bracket = heteroscedasticity check.
  B. Power grid (planning): N in {30..180}, Cohen's d in {0.25, 0.40, 0.60}, ICC in {0.3, 0.5, 0.7};
     4 captures per participant, one-sided Wilcoxon on participant means at alpha = 0.025 (Holm).
  C. Anthropometric circumference model (Ch.5 eq. 5.4, Table 5.5): keypoints vs OLS regression vs
     Bayesian precision-weighted fusion; MAE, RMSE, R^2, residual variance on a 30% hold-out.
  D. Monte-Carlo weight perturbation of the Pugh matrix (Ch.5 Sec. 5.2.4): exact replay of the random
     stream of generate_beauty_benchmarks.py (seed 2026).

Synthetic data only: the parameters are design assumptions stated in the report, not measurements.

Usage:  python scripts/statistical_validation.py [--check]
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_beauty_benchmarks as gb  # noqa: E402

DATA = ROOT / "report" / "figures" / "data"
PLOTS = ROOT / "report" / "figures" / "stats"
CHAP = ROOT / "report" / "chapters"
PAL = {"forest": "#1E3226", "garnet": "#76290B", "copper": "#C27E35", "mustard": "#CCB363",
       "dust": "#6F7D7B", "eggnog": "#FBEDC3"}


# ---------------------------------------------------------- A. mixed-effects pilot
def mixed_pilot(rng, n_part=120, boot=4000):
    import statsmodels.formula.api as smf
    gb.fit_fusion_weights()
    P = gb.draw_persons(rng, n_part)
    rep = {k: np.repeat(v, 4) for k, v in P.items()}          # 4 captures per person
    fam = np.tile(np.arange(4), n_part)
    res, lab = gb.simulate_captures(rng, rep, fam)
    pid = np.repeat(np.arange(n_part), 4)
    ita = np.degrees(np.arctan2(lab[:, 0] - 50, lab[:, 2]))
    cam, aur = res["Uncorrected camera"], res[gb.PROPOSED]
    df = pd.DataFrame({"y": np.r_[cam, aur], "method": np.r_[np.zeros_like(cam), np.ones_like(aur)],
                       "pid": np.r_[pid, pid], "light": np.r_[fam, fam], "ita": np.r_[ita, ita], "g": 1})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.mixedlm("y ~ method", df, groups="g", re_formula="0",
                        vc_formula={"pid": "0 + C(pid)", "light": "0 + C(light)"}).fit(reml=True)
    b1 = float(m.params["method"]); se = float(m.bse["method"])
    vc = dict(zip(m.model.exog_vc.names, np.asarray(m.vcomp)))
    s2p, s2l, s2e = float(vc["pid"]), float(vc["light"]), float(m.scale)
    p_a = float(stats.norm.cdf(b1 / se))                      # one-sided, H1a: b1 < 0
    resid = df["y"] - m.fittedvalues
    brackets = {"light": df["ita"] > 41, "intermediate": (df["ita"] > 10) & (df["ita"] <= 41),
                "tan_brown": df["ita"] <= 10}
    resid_sd = {k: float(resid[v].std(ddof=1)) for k, v in brackets.items()}
    d = (cam - aur).reshape(n_part, 4).mean(1)                # participant-mean paired differences
    w = stats.wilcoxon(d, alternative="greater")
    a = aur.reshape(n_part, 4)
    meds = np.array([np.median(a[rng.integers(0, n_part, n_part)]) for _ in range(boot)])
    upper95 = float(np.percentile(meds, 95))
    p_b = float((meds >= 1.8).mean())
    p = np.array([p_a, p_b]); o = np.argsort(p); holm = np.empty(2)
    holm[o[0]] = min(1.0, 2 * p[o[0]]); holm[o[1]] = min(1.0, max(holm[o[0]], p[o[1]]))
    out = {"n": n_part, "n_light": 4, "b0": float(m.params["Intercept"]), "b1": b1, "se_b1": se,
           "ci95_low": b1 - 1.96 * se, "ci95_high": b1 + 1.96 * se,
           "s2_part": s2p, "s2_light": s2l, "s2_resid": s2e,
           "icc_part": s2p / (s2p + s2l + s2e), "resid_sd_by_ita": resid_sd,
           "median_aur": float(np.median(aur)), "median_upper95": upper95,
           "p_h1a": p_a, "p_h1b": p_b, "holm_h1a": float(holm[0]), "holm_h1b": float(holm[1]),
           "reject_h0a": bool(holm[0] < 0.05), "reject_h0b": bool(holm[1] < 0.05),
           "wilcoxon_p": float(w.pvalue), "mean_diff_participant": float(d.mean())}
    return out, d


# --------------------------------------------------------------- B. power grid
def power_grid(rng, reps=1000, alpha=0.025, k=4):
    rows = []
    for icc in (0.3, 0.5, 0.7):
        for dd in (0.25, 0.40, 0.60):
            for n in (30, 60, 90, 120, 150, 180):
                u = rng.normal(0, np.sqrt(icc), (reps, n, 1))
                e = rng.normal(0, np.sqrt(1 - icc), (reps, n, k))
                x = (dd + u + e).mean(2)                        # participant means of the paired difference
                pv = stats.wilcoxon(x, alternative="greater", axis=1).pvalue
                rows.append((icc, dd, n, float((pv < alpha).mean())))
    return rows


# --------------------------------------------------- C. circumference regression + fusion
def circumference_model(rng, n=2000):
    female = rng.random(n) < 0.6
    height = np.where(female, rng.normal(164, 6.5, n), rng.normal(177, 7.0, n))
    bmi = np.clip(rng.lognormal(np.log(23.5), 0.15, n), 16, 40)
    weight = bmi * (height / 100) ** 2
    waist = 18 + 2.25 * bmi + 0.12 * height + 4.0 * (~female) + rng.normal(0, 3.4, n)
    h_rep = height + rng.normal(0, 1.0, n)
    w_rep = weight + rng.normal(0, 1.5, n)
    tape = waist + rng.normal(0, 1.5, n)
    kp = waist[:, None] + 1.0 + rng.normal(0, 3.0, (n, 3))
    kp_mean = kp.mean(1)
    tr = rng.random(n) < 0.7
    te = ~tr
    bmi_rep = w_rep / (h_rep / 100) ** 2
    X = np.column_stack([np.ones(n), h_rep, w_rep, bmi_rep, (~female).astype(float)])
    beta, *_ = np.linalg.lstsq(X[tr], waist[tr], rcond=None)
    pred_reg = X @ beta
    s2_reg = float(np.var(waist[tr] - pred_reg[tr], ddof=X.shape[1]))
    bias_kp = float(np.mean(kp_mean[tr] - waist[tr]))
    pred_kp = kp_mean - bias_kp
    s2_kp = float(np.var(waist[tr] - pred_kp[tr], ddof=1))
    s2_tape = float(np.var(waist[tr] - tape[tr], ddof=1))
    prec = np.array([1 / s2_reg, 1 / s2_kp, 1 / s2_tape])
    pred_fus = (prec[0] * pred_reg + prec[1] * pred_kp + prec[2] * tape) / prec.sum()

    def metr(pred):
        e = waist[te] - pred[te]
        return {"MAE": float(np.mean(np.abs(e))), "RMSE": float(np.sqrt(np.mean(e ** 2))),
                "R2": float(1 - np.sum(e ** 2) / np.sum((waist[te] - waist[te].mean()) ** 2)),
                "resid_var": float(np.var(e, ddof=1))}
    res = {"keypoints": metr(pred_kp), "regression": metr(pred_reg), "fusion": metr(pred_fus)}
    res["meta"] = {"n": n, "n_test": int(te.sum()), "beta": [float(b) for b in beta],
                   "sigma_reg": float(np.sqrt(s2_reg)), "sigma_kp": float(np.sqrt(s2_kp)),
                   "sigma_tape": float(np.sqrt(s2_tape)), "posterior_sd": float(np.sqrt(1 / prec.sum())),
                   "weights": [float(p / prec.sum()) for p in prec]}
    return res, waist[te], pred_fus[te], pred_kp[te]


# ------------------------------------------------------------- D. Monte-Carlo Pugh
def pugh_montecarlo():
    """Replay generate_beauty_benchmarks.main()'s random stream exactly (seed 2026)."""
    rng = np.random.default_rng(2026)
    cal = gb.calibration_study(rng)
    cal.pop("_ita"); cal.pop("_fam")
    gb.power_from_simulation(cal, rng)
    state = rng.bit_generator.state
    rows, extreme, win, margin5, win2 = gb.sensitivity(rng)
    rng.bit_generator.state = state           # sensitivity() draws nothing before its Dirichlet sample
    base = np.array([c[3] for c in gb.CRITERIA])
    W = rng.dirichlet(base * 40, 20000)
    S = W @ np.array(list(gb.ALTERNATIVES.values()), float).T
    margin = S[:, 2] - S[:, :2].max(1)
    assert abs((S.argmax(1) == 2).mean() - win) < 1e-12
    return {"draws": 20000, "dirichlet_conc": 40, "p_win_alt3": float(win), "margin_p5": float(margin5),
            "margin_mean": float(margin.mean()), "p_win_uniform": float(win2)}, margin


# ----------------------------------------------------------------- outputs + checks
def write_plots(grid, waist_te, fus_te, kp_te, margin):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib missing: PNG plots skipped")
        return
    PLOTS.mkdir(parents=True, exist_ok=True)
    (PLOTS / "paired_test.png").unlink(missing_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": PAL["dust"]})
    fig, ax = plt.subplots(figsize=(5.4, 3.3), dpi=160)
    cols = {0.25: PAL["dust"], 0.4: PAL["copper"], 0.6: PAL["forest"]}
    g = pd.DataFrame(grid, columns=["icc", "d", "n", "power"])
    for dd, sub in g[g.icc == 0.5].groupby("d"):
        ax.plot(sub.n, sub.power, marker="o", color=cols[round(dd, 2)], label=f"d = {dd:.2f}")
    ax.axhline(0.9, color=PAL["garnet"], ls="--", lw=1.1, label="power 0.90")
    ax.set_xlabel("participants N (4 captures each, ICC = 0.5)"); ax.set_ylabel("power (Wilcoxon, alpha = 0.025)")
    ax.set_ylim(0, 1.02); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(PLOTS / "power_grid.png"); plt.close(fig)

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


def min_n(grid, icc, d, target=0.9):
    ok = [n for (i, dd, n, pw) in grid if i == icc and abs(dd - d) < 1e-9 and pw >= target]
    return min(ok) if ok else None


def tex_checks(s):
    """(formatted value, chapter file) pairs that must appear verbatim in the LaTeX."""
    p, c, m = s["mixed_pilot"], s["circumference"], s["pugh_montecarlo"]
    f2 = lambda x: f"{x:.2f}"
    return [
        (f2(p["b1"]), "ch3_literature.tex"), (f2(p["ci95_low"]), "ch3_literature.tex"),
        (f2(p["ci95_high"]), "ch3_literature.tex"), (f2(p["icc_part"]), "ch3_literature.tex"),
        (f2(p["median_upper95"]), "ch3_literature.tex"),
        (str(s["power"]["min_n_d040_icc05"]), "ch2_problem.tex"),
        (f2(c["keypoints"]["MAE"]), "ch5_alternatives.tex"), (f2(c["regression"]["MAE"]), "ch5_alternatives.tex"),
        (f2(c["fusion"]["MAE"]), "ch5_alternatives.tex"), (f2(c["fusion"]["RMSE"]), "ch5_alternatives.tex"),
        (f2(c["fusion"]["R2"]), "ch5_alternatives.tex"), (f2(c["fusion"]["resid_var"]), "ch5_alternatives.tex"),
        (f"{m['p_win_uniform'] * 100:.1f}", "ch5_alternatives.tex"), (f2(m["margin_p5"]), "ch5_alternatives.tex"),
        ("20,000", "ch5_alternatives.tex"),
    ] + data_checks()


def data_checks():
    """Numbers produced by generate_beauty_benchmarks.py (CSV + functions) that the chapters quote."""
    cal = pd.read_csv(DATA / "calibration.csv").set_index("method")
    cam, gw, aur = cal.loc["Uncorrected camera"], cal.loc["Gray-world AWB"], cal.loc[gb.PROPOSED]
    ill = pd.read_csv(DATA / "calibration_by_illuminant.csv", dtype=str)
    ue = gb.unit_economics()["base"]
    mk = gb.market_build()
    f2 = lambda x: f"{x:.2f}"
    out = [(f2(cam["mean"]), "ch2_problem.tex"), (f2(cam["p95"]), "ch2_problem.tex"), (f2(gw["mean"]), "ch2_problem.tex"),
           (f2(aur["median"]), "ch5_alternatives.tex"), (f2(aur["mean"]), "ch5_alternatives.tex"),
           (f2(aur["p95"]), "ch5_alternatives.tex"), (f"{aur['pct_below_2']:.1f}", "ch5_alternatives.tex"),
           (f"{ue['ltv_cac']:.1f}", "ch4_market.tex"), (f2(ue["revenue"]), "ch4_market.tex"),
           (f2(ue["margin"]), "ch4_market.tex"), (f2(ue["n_gen"]), "ch4_market.tex"),
           (f"{ue['uplift']:.3f}", "ch4_market.tex"), (f"{ue['per_tryon_rev']:.3f}", "ch4_market.tex"),
           (f"{ue['biz12_ratio']:.1f}", "ch4_market.tex"), (f"{gb.unit_economics()['worst_biz12']:.1f}", "ch4_market.tex"),
           (f"{mk['som'] / 1e6:.1f}M", "ch4_market.tex"), (f"{mk['sam'] / 1e9:.1f}B", "ch4_market.tex")]
    out += [(f"{v:.2f}", "ch4_market.tex") for v in pd.read_csv(DATA / "ltv_cac_grid.csv")["ltv_cac"]]
    out += [(v, "ch5_alternatives.tex") for c in ill.columns[1:] for v in ill[c]]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify the numbers in the LaTeX chapters")
    args = ap.parse_args()

    mc, margin = pugh_montecarlo()
    pilot, d = mixed_pilot(np.random.default_rng(2027))
    grid = power_grid(np.random.default_rng(2029))
    circ, waist_te, fus_te, kp_te = circumference_model(np.random.default_rng(2028))
    power = {"min_n_d040_icc05": min_n(grid, 0.5, 0.40), "min_n_d025_icc05": min_n(grid, 0.5, 0.25),
             "min_n_d040_icc07": min_n(grid, 0.7, 0.40), "min_n_d040_icc03": min_n(grid, 0.3, 0.40)}
    summary = {"seed": {"pugh_and_calibration": 2026, "pilot": 2027, "circumference": 2028, "power": 2029},
               "mixed_pilot": pilot, "power": power, "circumference": circ, "pugh_montecarlo": mc}

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "stats_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (DATA / "paired_differences.csv").unlink(missing_ok=True)
    np.savetxt(DATA / "pilot_participant_differences.csv", d, delimiter=",", header="d_participant",
               comments="", fmt="%.4f")
    pd.DataFrame(grid, columns=["icc", "d", "n", "power"]).to_csv(DATA / "power_grid.csv", index=False,
                                                                   float_format="%.3f")
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
    write_plots(grid, waist_te, fus_te, kp_te, margin)

    p = pilot
    print(f"A  mixed model n={p['n']}x4: b1={p['b1']:.2f} [{p['ci95_low']:.2f}, {p['ci95_high']:.2f}]"
          f"  s2 part/light/resid = {p['s2_part']:.2f}/{p['s2_light']:.2f}/{p['s2_resid']:.2f}  ICC={p['icc_part']:.2f}"
          f"  resid SD by ITA {', '.join(f'{k} {v:.2f}' for k, v in p['resid_sd_by_ita'].items())}")
    print(f"A  median AURAM={p['median_aur']:.2f} upper95={p['median_upper95']:.2f} p_b={p['p_h1b']:.3f}"
          f"  Holm: H0a rejected {p['reject_h0a']}, H0b rejected {p['reject_h0b']}"
          f"  (participant mean diff {p['mean_diff_participant']:.2f}, Wilcoxon p={p['wilcoxon_p']:.1e})")
    print(f"B  power 0.9: d=0.40/ICC0.5 N={power['min_n_d040_icc05']}, d=0.25/ICC0.5 N={power['min_n_d025_icc05']},"
          f" d=0.40/ICC0.7 N={power['min_n_d040_icc07']}, d=0.40/ICC0.3 N={power['min_n_d040_icc03']}")
    for k in ("keypoints", "regression", "fusion"):
        r = circ[k]
        print(f"C  {k:10s} MAE={r['MAE']:.2f} RMSE={r['RMSE']:.2f} R2={r['R2']:.2f} resid_var={r['resid_var']:.2f}")
    print(f"D  Pugh MC: Alt3 wins {mc['p_win_alt3']*100:.1f}%  margin p5={mc['margin_p5']:.2f}"
          f"  uniform weights: {mc['p_win_uniform']*100:.1f}%")

    if args.check:
        bad = [(v, f) for v, f in tex_checks(summary) if v not in (CHAP / f).read_text(encoding="utf-8")]
        for v, f in bad:
            print(f"MISSING in {f}: {v}")
        print("NUMBER CHECK:", "PASS" if not bad else f"FAIL ({len(bad)} missing)")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
