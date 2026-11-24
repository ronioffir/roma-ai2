"""uncertainty_voi.py -- uncertainty layer of the AURAM report (group roma-ai2, v3.5, prompt 13).

Replaces single point estimates with distributions and ranks what to measure next. Every number
quoted in the report's uncertainty passages comes from report/figures/data/uncertainty_summary.json;
`--check` verifies that the LaTeX chapters contain them.

  A. Hierarchical Bayesian model of the simulated pilot (same draw as statistical_validation.py,
     seed 2027: 120 participants x 4 illuminant families), on the log colour error of AURAM:
         log y_ij = eta_j + u_i + e_ij,   eta_j ~ N(mu, tau_l^2),  u_i ~ N(0, tau_p^2),  e_ij ~ N(0, s_j^2)
     (the residual variance differs per family: daylight errors are tighter than LED errors)
     Gibbs sampler (conjugate updates). Reported: posterior of the median error per illuminant
     family, over the four tested families, and for a NEW family; P(median <= 1.8) for each.
  B. Pre-posterior design comparison: how wide the interval of the population median stays for
     alternative designs (participants x illuminant families) -- the value of each design.
  C. Hardware sensitivity: median error against the flash-to-ambient ratio (screen luminance vs
     room light) and the burst length (sensor noise vs capture time).
  D. Unit economics as a distribution: Monte Carlo over the team's assumptions, then the expected
     value of perfect information (EVPI) and of partial perfect information (EVPPI) per measurement,
     for the go / no-go decision against the team's LTV/CAC target of 3.8.
  E. Constraint map: diffusion steps vs latency (REQ-GEN-06) vs margin (REQ-BIZ-12).

Synthetic data and team assumptions only. The priors of part D are the team's stated uncertainty
about its own assumptions, not measurements.

Usage:  python scripts/uncertainty_voi.py [--check]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_beauty_benchmarks as gb  # noqa: E402

DATA = ROOT / "report" / "figures" / "data"
CHAP = ROOT / "report" / "chapters"
TARGET = 1.8            # REQ-VIS-01, median DeltaE00
LTV_TARGET = 3.8        # team threshold for LTV/CAC (report Sec. 4.4)
FAMILIES = ["D65", "A", "F11", "LED"]


# ------------------------------------------------------- A. hierarchical posterior
def pilot_draw(seed=2027, n_part=120):
    """The pilot of statistical_validation.mixed_pilot(), reproduced draw for draw."""
    rng = np.random.default_rng(seed)
    gb.fit_fusion_weights()
    P = gb.draw_persons(rng, n_part)
    rep = {k: np.repeat(v, 4) for k, v in P.items()}
    fam = np.tile(np.arange(4), n_part)
    res, _ = gb.simulate_captures(rng, rep, fam)
    return res[gb.PROPOSED].reshape(n_part, 4)


def gibbs(z, rng, iters=24000, burn=4000, light_scale=0.25):
    """z: (n, J) log errors. Priors: mu flat; variances scaled-inverse-chi2 with 1 d.o.f.
    (scale 0.25 on the log scale for the two random effects, 0.5 for the residual)."""
    n, J = z.shape
    a_p, b_p = 0.5, 0.5 * 0.25 ** 2
    a_l, b_l = 0.5, 0.5 * light_scale ** 2
    a_e, b_e = 0.5, 0.5 * 0.5 ** 2
    eta = z.mean(0).copy(); u = np.zeros(n); mu = eta.mean()
    s2, tp2, tl2 = np.full(J, z.var()), 0.05, 0.05
    keep = iters - burn
    out = {k: np.empty(keep) for k in ("mu", "tp2", "tl2")}
    out["eta"] = np.empty((keep, J)); out["s2"] = np.empty((keep, J))
    for t in range(iters):
        prec = n / s2 + 1 / tl2
        eta = rng.normal(((z - u[:, None]).sum(0) / s2 + mu / tl2) / prec, np.sqrt(1 / prec))
        prec = (1 / s2).sum() + 1 / tp2
        u = rng.normal(((z - eta[None]) / s2[None]).sum(1) / prec, np.sqrt(1 / prec))
        mu = rng.normal(eta.mean(), np.sqrt(tl2 / J))
        sse = ((z - eta[None] - u[:, None]) ** 2).sum(0)
        s2 = 1 / rng.gamma(a_e + n / 2, 1 / (b_e + sse / 2))
        tp2 = 1 / rng.gamma(a_p + n / 2, 1 / (b_p + (u ** 2).sum() / 2))
        tl2 = 1 / rng.gamma(a_l + J / 2, 1 / (b_l + ((eta - mu) ** 2).sum() / 2))
        if t >= burn:
            i = t - burn
            out["mu"][i], out["tp2"][i], out["tl2"][i] = mu, tp2, tl2
            out["eta"][i] = eta; out["s2"][i] = s2
    return out


def mixture_median(eta, sd):
    """Median of an equal mixture of lognormals LN(eta_j, sd_j^2), per posterior draw (bisection)."""
    lo, hi = eta.min(1) - 1, eta.max(1) + 1
    for _ in range(50):
        mid = (lo + hi) / 2
        cdf = stats.norm.cdf((mid[:, None] - eta) / sd).mean(1)
        lo = np.where(cdf < 0.5, mid, lo); hi = np.where(cdf >= 0.5, mid, hi)
    return np.exp((lo + hi) / 2)


def q(x, ps=(2.5, 25, 50, 75, 97.5)):
    return [float(v) for v in np.percentile(x, ps)]


def posterior_block(y, rng):
    z = np.log(y)
    g = gibbs(z, rng)
    sd_within = np.sqrt(g["tp2"][:, None] + g["s2"])
    med_tested = mixture_median(g["eta"], sd_within)
    med_pop = np.exp(g["mu"])
    med_new = np.exp(rng.normal(g["mu"], np.sqrt(g["tl2"])))
    rows = [(FAMILIES[j], np.exp(g["eta"][:, j])) for j in range(4)]
    rows += [("tested", med_tested), ("new", med_new)]
    table = [{"key": k, "q": q(v), "p_meets": float((v <= TARGET).mean())} for k, v in rows]
    # prior sensitivity of the between-family scale (the weakest-identified parameter: J = 4)
    sens = {}
    for sc in (0.10, 0.50):
        g2 = gibbs(z, np.random.default_rng(31 + int(sc * 100)), iters=12000, burn=2000, light_scale=sc)
        v = np.exp(np.random.default_rng(5).normal(g2["mu"], np.sqrt(g2["tl2"])))
        sens[f"{sc:.2f}"] = {"p_new_meets": float((v <= TARGET).mean()), "new_q": q(v)}
    hist, edges = np.histogram(med_tested, bins=36, range=(1.55, 2.45), density=True)
    hist_new, _ = np.histogram(med_new, bins=36, range=(0.6, 4.2), density=True)
    comp = {"sd_light": float(np.sqrt(g["tl2"]).mean()), "sd_part": float(np.sqrt(g["tp2"]).mean()),
            "sd_resid": float(np.sqrt(g["s2"].mean(1)).mean()),
            "sd_resid_by_family": [float(v) for v in np.sqrt(g["s2"]).mean(0)],
            "tl2": float(np.median(g["tl2"])), "tp2": float(np.median(g["tp2"])),
            "s2": float(np.median(g["s2"].mean(1)))}
    return {"empirical_median": float(np.median(y)), "table": table, "components": comp,
            "pop_q": q(med_pop), "p_pop_meets": float((med_pop <= TARGET).mean()),
            "prior_sensitivity": sens,
            "lognormal_qq_r": float(stats.probplot((z - z.mean(0)).ravel(), dist="norm")[1][2])}, \
        (hist, edges), g


# ----------------------------------------------------- B. pre-posterior design value
def design_value(comp, designs=((120, 4), (240, 4), (60, 8), (120, 8), (120, 12))):
    """Approximate 95% interval of the population median (multiplicative half-width) per design,
    from the posterior medians of the variance components:  Var(mu_hat) = tl2/J + tp2/n + s2/(nJ)."""
    out = []
    for n, J in designs:
        parts = {"light": comp["tl2"] / J, "part": comp["tp2"] / n, "resid": comp["s2"] / (n * J)}
        var = sum(parts.values())
        out.append({"n": n, "J": J, "captures": n * J, "sd_log": float(math.sqrt(var)),
                    "half_width_pct": float((math.exp(1.96 * math.sqrt(var)) - 1) * 100),
                    "share_light_pct": float(parts["light"] / var * 100)})
    return out


# ------------------------------------------------------------ C. hardware sensitivity
SCREEN_NITS, SCREEN_AREA, DIST = 600.0, 0.065 * 0.140, 0.30    # mid-range phone, full white, 30 cm


def flash_ratio(ambient_lux, nits=SCREEN_NITS):
    """Illuminance of the screen on the face (small Lambertian source) over the room illuminance."""
    return nits * SCREEN_AREA / DIST ** 2 / ambient_lux


def hardware_grid(n=3000, seed=2031):
    gb.fit_fusion_weights()
    rows = []
    for lux in (100, 200, 400, 800, 1600, 3200):
        r = flash_ratio(lux)
        for burst in (4, 8, 16, 32):
            rng = np.random.default_rng(seed)                 # common random numbers across the grid
            P = gb.draw_persons(rng, n)
            res, _ = gb.simulate_captures(rng, P, rng.integers(0, 4, n),
                                          hw={"flash_ratio": (r, r), "burst": burst})
            a, f = res[gb.PROPOSED], res["Flash delta only"]
            rows.append({"lux": lux, "ratio": float(r), "burst": burst,
                         "median": float(np.median(a)), "p95": float(np.percentile(a, 95)),
                         "flash_only_median": float(np.median(f)),
                         "capture_ms": float(2 * burst * 1000 / 30)})   # flash + ambient bursts at 30 fps
    return rows


# --------------------------------------------------------- D. economics distribution + VoI
def beta_ms(rng, mean, sd, size):
    k = mean * (1 - mean) / sd ** 2 - 1
    return rng.beta(mean * k, (1 - mean) * k, size)


PRIORS = {  # name: (kind, centre, spread) -- the team's uncertainty about its own assumptions
    "conv": ("beta", 0.04, 0.012), "ctr": ("beta", 0.08, 0.02), "conv_uplift": ("1+lognorm", 0.5, 0.5),
    "churn": ("beta", 0.12, 0.035), "cac": ("lognorm", 2.00, 0.35), "gpu_cost": ("lognorm", 0.015, 0.35),
    "share_sponsored": ("beta", 0.60, 0.10), "sub_rate": ("beta", 0.03, 0.01),
    "dropoff_15s": ("beta", 0.80, 0.06), "micro_ecpm": ("lognorm", 8.0, 0.30),
    "sponsor_fee": ("lognorm", 0.02, 0.30), "aov": ("lognorm", 65.0, 0.15),
}
GROUPS = {  # one planned measurement resolves one group
    "partner_ab": ["conv", "ctr", "conv_uplift", "aov"],      # partner A/B test (RSK-BIZ-04)
    "churn": ["churn"],                                       # retention cohort
    "cac": ["cac"],                                           # acquisition pilot
    "gpu": ["gpu_cost"],                                      # load test TSK-4.3
    "gate_mix": ["share_sponsored", "dropoff_15s", "micro_ecpm", "sponsor_fee"],
    "subscription": ["sub_rate"],
}


def draw_priors(rng, n):
    d = {}
    for k, (kind, c, s) in PRIORS.items():
        if kind == "beta":
            d[k] = beta_ms(rng, c, s, n)
        elif kind == "lognorm":
            d[k] = c * rng.lognormal(0, s, n)
        else:
            d[k] = 1 + c * rng.lognormal(0, s, n)
    return d


def tier_vec(d, e=gb.ECON):
    """Vectorised copy of gb.tier_economics(); checked against it at the base point."""
    g = lambda k: d.get(k, e[k])
    beta = np.log(1 / (1 - g("dropoff_15s"))) / e["ad_seconds"]
    keep_micro = np.exp(-beta * e["micro_seconds"])
    req = e["sessions"] * e["tryons_per_session"]
    n_spon = req * g("share_sponsored")
    n_micro = req * (1 - g("share_sponsored")) * keep_micro
    n_gen = n_spon + n_micro
    uplift = g("conv") * (g("conv_uplift") - 1) * g("aov") * e["comm"]
    rev_aff = e["sessions"] * e["recs"] * g("ctr") * g("conv") * g("aov") * e["comm"]
    rev_gen = n_spon * g("sponsor_fee") + n_micro * g("micro_ecpm") / 1000 + n_gen * uplift
    rev_sub = g("sub_rate") * e["sub_price"] * (1 - e["pay_fee"])
    margin = rev_aff + rev_gen + rev_sub - n_gen * g("gpu_cost") - e["sessions"] * e["rec_cost"]
    ltv = margin / g("churn")
    return {"margin": margin, "ltv": ltv, "ltv_cac": ltv / g("cac"), "cac": g("cac")}


def cond_mean(nb, X):
    """E[NB | X] by least squares on a cubic polynomial basis with pairwise interactions."""
    Z = (X - X.mean(0)) / X.std(0)
    cols = [np.ones(len(nb))] + [Z[:, j] ** p for j in range(Z.shape[1]) for p in (1, 2, 3)]
    cols += [Z[:, i] * Z[:, j] for i in range(Z.shape[1]) for j in range(i + 1, Z.shape[1])]
    A = np.column_stack(cols)
    coef, *_ = np.linalg.lstsq(A, nb, rcond=None)
    return A @ coef


def economics_voi(n=200_000, seed=2032):
    base = gb.tier_economics()
    chk = tier_vec({})
    assert abs(chk["ltv_cac"] - base["ltv_cac"]) < 1e-9 and abs(chk["margin"] - base["margin"]) < 1e-9
    rng = np.random.default_rng(seed)
    d = draw_priors(rng, n)
    r = tier_vec(d)
    ratio = r["ltv_cac"]
    nb = r["ltv"] - LTV_TARGET * r["cac"]                      # USD per acquired user above the target
    ev_now = max(nb.mean(), 0.0)
    evpi = float(np.maximum(nb, 0).mean() - ev_now)
    var_log = np.var(np.log(np.clip(ratio, 1e-6, None)))
    voi = {}
    for name, keys in GROUPS.items():
        X = np.column_stack([d[k] for k in keys])
        fit = cond_mean(nb, X)
        fit_log = cond_mean(np.log(np.clip(ratio, 1e-6, None)), X)
        voi[name] = {"evppi": float(max(np.maximum(fit, 0).mean() - ev_now, 0.0)),
                     "var_share_pct": float(np.var(fit_log) / var_log * 100)}
    for v in voi.values():
        v["evppi_share_pct"] = float(v["evppi"] / evpi * 100) if evpi > 0 else 0.0
    hist, edges = np.histogram(ratio, bins=40, range=(0, 20))
    return {"draws": n, "base_ltv_cac": float(base["ltv_cac"]), "q": q(ratio, (5, 25, 50, 75, 95)),
            "mean": float(ratio.mean()), "p_above_target": float((ratio >= LTV_TARGET).mean()),
            "p_above_3": float((ratio >= 3.0).mean()), "p_below_1": float((ratio < 1.0).mean()),
            "nb_mean": float(nb.mean()), "evpi": evpi, "voi": voi,
            "decision_now": "go" if nb.mean() > 0 else "no-go"}, (hist / n * 100, edges)


# ------------------------------------------------------------------ E. constraint map
FIXED_S, PER_STEP_S, BASE_STEPS = 1.3, 0.4, 8      # try-on path: 4.5 s = 1.3 s fixed + 8 x 0.4 s
LAT_LIMIT, BIZ_LIMIT = 4.5, 2.4


def constraint_map():
    base = gb.tier_economics()
    rows = []
    for steps in (4, 8, 12, 20, 30):
        cost = gb.ECON["gpu_cost"] * steps / BASE_STEPS       # GPU seconds scale with the step count
        t = FIXED_S + PER_STEP_S * steps
        e = gb.tier_economics(gpu_cost=cost)
        rows.append({"steps": steps, "time_s": t, "cost": cost, "biz12": float(e["biz12_ratio"]),
                     "ltv_cac": float(e["ltv_cac"]), "lat_ok": t <= LAT_LIMIT + 1e-9,
                     "biz_ok": e["biz12_ratio"] >= BIZ_LIMIT})
    max_cost = base["per_tryon_rev"] / BIZ_LIMIT
    return {"rows": rows, "max_steps_latency": (LAT_LIMIT - FIXED_S) / PER_STEP_S,
            "max_steps_margin": float(max_cost / gb.ECON["gpu_cost"] * BASE_STEPS),
            "max_cost": float(max_cost), "cost_slack": float(max_cost / gb.ECON["gpu_cost"])}


# ----------------------------------------------------------------------- outputs
def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(v) for v in r) + "\n")


def tex_checks(s):
    f2 = lambda x: f"{x:.2f}"
    f0 = lambda x: f"{x:.0f}"
    t = {r["key"]: r for r in s["posterior"]["table"]}
    e, c = s["economics"], s["constraints"]
    d = {(r["n"], r["J"]): r for r in s["design"]}
    return [
        (f2(t["tested"]["q"][0]), "ch5_alternatives.tex"), (f2(t["tested"]["q"][4]), "ch5_alternatives.tex"),
        (f2(t["new"]["q"][0]), "ch5_alternatives.tex"), (f2(t["new"]["q"][4]), "ch5_alternatives.tex"),
        (f0(t["new"]["p_meets"] * 100) + "\\%", "ch5_alternatives.tex"),
        (f0(d[(120, 4)]["half_width_pct"]) + "\\%", "ch5_alternatives.tex"),
        (f0(d[(60, 8)]["half_width_pct"]) + "\\%", "ch5_alternatives.tex"),
        (f"{e['q'][0]:.1f}", "ch4_market.tex"), (f"{e['q'][2]:.1f}", "ch4_market.tex"),
        (f"{e['q'][4]:.1f}", "ch4_market.tex"), (f0(e["p_above_target"] * 100) + "\\%", "ch4_market.tex"),
        (f2(e["evpi"]), "ch4_market.tex"), (f"{c['cost_slack']:.1f}", "ch5_alternatives.tex"),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify the numbers in the LaTeX chapters")
    args = ap.parse_args()

    y = pilot_draw()
    post, (hist, edges), g = posterior_block(y, np.random.default_rng(2030))
    design = design_value(post["components"])
    hw = hardware_grid()
    econ, (ehist, eedges) = economics_voi()
    cons = constraint_map()
    summary = {"seed": {"pilot": 2027, "gibbs": 2030, "hardware": 2031, "economics": 2032},
               "targets": {"median_dE": TARGET, "ltv_cac": LTV_TARGET},
               "posterior": post, "design": design, "hardware": hw, "economics": econ,
               "constraints": cons, "priors": {k: list(v) for k, v in PRIORS.items()}}
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "uncertainty_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    order = ["D65", "A", "F11", "LED", "tested", "new"]
    t = {r["key"]: r for r in post["table"]}
    write_csv(DATA / "posterior_median.csv", ["pos", "key", "lo95", "lo50", "med", "hi50", "hi95", "p_pct"],
              [(len(order) - i, k, *[f"{v:.3f}" for v in t[k]["q"]], f"{t[k]['p_meets'] * 100:.0f}")
               for i, k in enumerate(order)])
    write_csv(DATA / "posterior_tested_density.csv", ["median", "density"],
              [(f"{(a + b) / 2:.4f}", f"{h:.4f}") for h, a, b in zip(hist, edges[:-1], edges[1:])])
    for b in (4, 8, 16, 32):
        write_csv(DATA / f"hardware_burst{b}.csv", ["lux", "ratio", "median", "p95", "flash_only"],
                  [(r["lux"], f"{r['ratio']:.4f}", f"{r['median']:.3f}", f"{r['p95']:.3f}",
                    f"{r['flash_only_median']:.3f}") for r in hw if r["burst"] == b])
    write_csv(DATA / "ltv_cac_distribution.csv", ["ratio", "pct"],
              [(f"{(a + b) / 2:.2f}", f"{h:.3f}") for h, a, b in zip(ehist, eedges[:-1], eedges[1:])])
    names = ["partner_ab", "cac", "churn", "gpu", "gate_mix", "subscription"]   # display order of Fig. 4.5
    write_csv(DATA / "voi_ranking.csv", ["pos", "key", "evppi", "evppi_share_pct", "var_share_pct"],
              [(len(names) - i, k, f"{econ['voi'][k]['evppi']:.4f}", f"{econ['voi'][k]['evppi_share_pct']:.1f}",
                f"{econ['voi'][k]['var_share_pct']:.1f}") for i, k in enumerate(names)])

    print(f"A  empirical median {post['empirical_median']:.2f}; lognormal QQ r = {post['lognormal_qq_r']:.3f}")
    for r in post["table"]:
        print(f"A  {r['key']:7s} median {r['q'][2]:.2f} [{r['q'][0]:.2f}, {r['q'][4]:.2f}]  P(<=1.8) = {r['p_meets']:.3f}")
    print(f"A  population median exp(mu) [{post['pop_q'][0]:.2f}, {post['pop_q'][4]:.2f}] P = {post['p_pop_meets']:.3f}"
          f"  SDs light/part/resid = {post['components']['sd_light']:.2f}/{post['components']['sd_part']:.2f}/"
          f"{post['components']['sd_resid']:.2f}  prior sens: {post['prior_sensitivity']}")
    for r in design:
        print(f"B  n={r['n']:3d} J={r['J']:2d} captures={r['captures']:4d}  +/-{r['half_width_pct']:.0f}%"
              f"  light share {r['share_light_pct']:.0f}%")
    for r in hw:
        print(f"C  {r['lux']:4d} lux ratio {r['ratio']:.3f} burst {r['burst']:2d} ({r['capture_ms']:.0f} ms):"
              f" median {r['median']:.2f} p95 {r['p95']:.2f} flash-only {r['flash_only_median']:.2f}")
    print(f"D  LTV/CAC 5/25/50/75/95 = {[round(v, 1) for v in econ['q']]}  P(>=3.8) = {econ['p_above_target']:.3f}"
          f"  P(<1) = {econ['p_below_1']:.4f}  EVPI = ${econ['evpi']:.3f}/user  decision now: {econ['decision_now']}")
    for k in names:
        v = econ["voi"][k]
        print(f"D  {k:12s} EVPPI ${v['evppi']:.3f} ({v['evppi_share_pct']:.0f}% of EVPI)  variance share {v['var_share_pct']:.0f}%")
    for r in cons["rows"]:
        print(f"E  {r['steps']:2d} steps: {r['time_s']:.1f} s  ${r['cost']:.4f}  BIZ-12 x{r['biz12']:.1f}"
              f"  LTV/CAC {r['ltv_cac']:.2f}  latency {'ok' if r['lat_ok'] else 'FAIL'}  margin {'ok' if r['biz_ok'] else 'FAIL'}")
    print(f"E  max steps: latency {cons['max_steps_latency']:.1f}, margin {cons['max_steps_margin']:.1f};"
          f" cost slack x{cons['cost_slack']:.1f}")

    if args.check:
        bad = [(v, f) for v, f in tex_checks(summary) if v not in (CHAP / f).read_text(encoding="utf-8")]
        for v, f in bad:
            print(f"MISSING in {f}: {v}")
        print("NUMBER CHECK:", "PASS" if not bad else f"FAIL ({len(bad)} missing)")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
