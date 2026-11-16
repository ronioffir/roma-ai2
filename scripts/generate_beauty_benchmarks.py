#!/usr/bin/env python3
"""
generate_beauty_benchmarks.py -- data generator for the AuraTwin AI preparatory report.

Produces every number that feeds a pgfplots chart (report/figures/data/*.csv) and a
summary (report/work/benchmarks_summary.md) that the chapters quote. Nothing in the
report's charts is typed by hand.

Three kinds of data, labelled explicitly in the report:
  1. COMPUTED  -- a synthetic Monte-Carlo simulation of illumination-induced colour error
                 and of three correction strategies (full CIEDE2000 implementation).
  2. COMPUTED  -- the Pugh weighted decision matrix and its sensitivity analysis
                 (one-at-a-time weight perturbation + Dirichlet Monte-Carlo).
  3. ESTIMATED -- competitor profiles (radar / scatter) = team's technical assessment,
                 marked "(הערכת הצוות)" in the captions.

Usage:  python scripts/generate_beauty_benchmarks.py [--seed 2026]
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "report" / "figures" / "data"
WORK = ROOT / "report" / "work"


# --------------------------------------------------------------------------- colour
def srgb_to_linear(c):
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(np.asarray(c, float), 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


M_RGB2XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                      [0.2126729, 0.7151522, 0.0721750],
                      [0.0193339, 0.1191920, 0.9503041]])
M_XYZ2RGB = np.linalg.inv(M_RGB2XYZ)
WHITE_D65 = np.array([0.95047, 1.0, 1.08883])


def _f(t):
    d = 6 / 29
    return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4 / 29)


def _finv(t):
    d = 6 / 29
    return np.where(t > d, t ** 3, 3 * d * d * (t - 4 / 29))


def linrgb_to_lab(rgb):
    xyz = np.asarray(rgb) @ M_RGB2XYZ.T / WHITE_D65
    fx, fy, fz = _f(xyz[..., 0]), _f(xyz[..., 1]), _f(xyz[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], -1)


def lab_to_linrgb(lab):
    lab = np.asarray(lab, float)
    fy = (lab[..., 0] + 16) / 116
    fx, fz = fy + lab[..., 1] / 500, fy - lab[..., 2] / 200
    xyz = np.stack([_finv(fx), _finv(fy), _finv(fz)], -1) * WHITE_D65
    return xyz @ M_XYZ2RGB.T


def ciede2000(lab1, lab2):
    """Vectorised CIEDE2000 (Sharma, Wu & Dalal 2005), kL = kC = kH = 1."""
    L1, a1, b1 = np.moveaxis(np.asarray(lab1, float), -1, 0)
    L2, a2, b2 = np.moveaxis(np.asarray(lab2, float), -1, 0)
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    dh = np.where(C1p * C2p == 0, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    hsum = h1p + h2p
    hbp = np.where(C1p * C2p == 0, hsum,
                   np.where(np.abs(h1p - h2p) <= 180, hsum / 2,
                            np.where(hsum < 360, (hsum + 360) / 2, (hsum - 360) / 2)))
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dtheta = 30 * np.exp(-(((hbp - 275) / 25) ** 2))
    RC = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    SL = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    SC, SH = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    RT = -np.sin(np.radians(2 * dtheta)) * RC
    return np.sqrt((dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2 + RT * (dCp / SC) * (dHp / SH))


def _selftest_ciede2000():
    # Pairs 1, 7 and 17 of the Sharma et al. (2005) test set.
    pairs = [((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
             ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
             ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492)]
    for a, b, ref in pairs:
        got = float(ciede2000(np.array(a), np.array(b)))
        assert abs(got - ref) < 1e-3, (a, b, got, ref)


# ------------------------------------------------------------- calibration study
IRIS_PRIORS = {  # CIELAB mean and per-channel std of a self-reported eye-colour category
    "brown": ((32.0, 9.0, 17.0), (5.0, 2.5, 4.0)),
    "hazel": ((45.0, 6.0, 24.0), (5.0, 2.5, 4.0)),
    "green": ((50.0, -8.0, 16.0), (5.0, 3.0, 4.0)),
    "blue": ((56.0, -3.0, -16.0), (5.0, 2.5, 4.0)),
}
SCLERA = ((86.0, 1.5, 6.0), (3.0, 1.0, 2.0))


def illuminant_gains(rng, n):
    """Random illuminant: CCT 2700-6500 K approximated by RGB gains + green/magenta tint
    + exposure. Returns (n,3) multiplicative gains applied in linear RGB."""
    t = rng.uniform(0, 1, n)                        # 0 = warm tungsten, 1 = cool daylight
    r = 1.0 + 0.55 * (1 - t)
    b = 1.0 + 0.55 * t - 0.25 * (1 - t)
    g = 1.0 + rng.normal(0, 0.07, n)                # fluorescent / LED tint
    exposure = rng.uniform(0.75, 1.15, n)
    gains = np.stack([r, g, b], -1)
    gains /= gains[:, 1:2]                           # camera keeps green as reference
    return gains * exposure[:, None]


def calibration_study(rng, n=4000):
    labels = rng.choice(list(IRIS_PRIORS), n)
    skin_lab = np.stack([rng.uniform(40, 78, n), rng.uniform(8, 20, n), rng.uniform(12, 28, n)], -1)
    sclera_user = np.array(SCLERA[0]) + rng.normal(0, 1, (n, 3)) * np.array(SCLERA[1])
    # per-capture sclera redness (fatigue, irritation, specular tint): a* shift >= 0
    redness = rng.exponential(2.5, n)
    sclera_lab = sclera_user + np.stack([np.zeros(n), redness, 0.3 * redness], -1)
    iris_mu = np.array([IRIS_PRIORS[l][0] for l in labels])
    iris_sd = np.array([IRIS_PRIORS[l][1] for l in labels])
    iris_lab = iris_mu + rng.normal(0, 1, (n, 3)) * iris_sd

    gains = illuminant_gains(rng, n)
    # auto-exposure protects highlights: the brightest anchor (sclera) stays below 0.92
    peak = (lab_to_linrgb(sclera_lab) * gains).max(1, keepdims=True)
    gains = gains * np.minimum(1.0, 0.92 / peak)
    # sensor noise in linear RGB AFTER averaging over the segmented region
    # (per-pixel sd ~0.006; skin patch ~1500 px incl. texture, sclera ~250 px, iris ~400 px)
    region_sd = {"skin": 0.0015, "sclera": 0.002, "iris": 0.003}
    obs = {k: np.clip(lab_to_linrgb(v) * gains + rng.normal(0, region_sd[k], (n, 3)), 1e-4, 1)
           for k, v in {"skin": skin_lab, "sclera": sclera_lab, "iris": iris_lab}.items()}
    # Camera auto-white-balance: gray-world on the selfie (partial correction, as in practice)
    scene_mean = 0.6 * obs["skin"] + 0.25 * np.clip(rng.normal(0.35, 0.08, (n, 3)) * gains, 0, 1) \
        + 0.15 * obs["sclera"]
    awb = scene_mean.mean(1, keepdims=True) / scene_mean
    awb_partial = 1 + 0.5 * (awb - 1)

    true_skin = skin_lab
    res = {}
    res["Uncorrected camera"] = ciede2000(linrgb_to_lab(np.clip(obs["skin"] * awb_partial, 0, 1)), true_skin)
    res["Gray-world AWB"] = ciede2000(linrgb_to_lab(np.clip(obs["skin"] * awb, 0, 1)), true_skin)
    # Sclera-only anchor: diagonal gains that map observed sclera to the population sclera mean
    sclera_ref = lab_to_linrgb(np.array(SCLERA[0]))
    g_s = sclera_ref / obs["sclera"]
    res["Sclera anchor"] = ciede2000(linrgb_to_lab(np.clip(obs["skin"] * g_s, 0, 1)), true_skin)
    # Sclera + self-reported iris prior: weighted least squares on log-gains (MAP estimate)
    iris_ref = lab_to_linrgb(iris_mu)
    w_s, w_i = 1 / 0.03 ** 2, 1 / 0.12 ** 2            # sclera is a tighter anchor than iris
    log_g = (w_s * np.log(sclera_ref / obs["sclera"]) + w_i * np.log(iris_ref / obs["iris"])) / (w_s + w_i)
    # shrink the exposure component toward the sclera estimate (iris luminance is uncertain)
    log_g += (np.log(g_s).mean(1, keepdims=True) - log_g.mean(1, keepdims=True))
    res["Sclera + iris prior"] = ciede2000(linrgb_to_lab(np.clip(obs["skin"] * np.exp(log_g), 0, 1)), true_skin)
    # AuraTwin: one-time enrolment with the phone screen as a known (D65-like) flash.
    # The enrolment measures the user's own sclera/iris with small error; the self-reported
    # eye-colour category acts as a Bayesian prior that rejects implausible iris readings.
    enr_sclera = sclera_user + rng.normal(0, 0.8, (n, 3))
    flash_iris = iris_lab + rng.normal(0, 2.0, (n, 3))
    post_iris = (flash_iris / 2.0 ** 2 + iris_mu / iris_sd ** 2) / (1 / 2.0 ** 2 + 1 / iris_sd ** 2)
    s_ref, i_ref = lab_to_linrgb(enr_sclera), lab_to_linrgb(post_iris)
    # robust two-anchor fusion: down-weight the sclera when its chroma departs from enrolment
    obs_scl_lab = linrgb_to_lab(np.clip(obs["sclera"] * g_s, 1e-4, 1))
    red_flag = np.clip((obs_scl_lab[:, 1] - SCLERA[0][1]) / 3.0, 0, None)
    w_s2 = 1 / (0.02 + 0.05 * red_flag[:, None]) ** 2
    w_i2 = 1 / 0.05 ** 2
    lg = (w_s2 * np.log(s_ref / obs["sclera"]) + w_i2 * np.log(i_ref / obs["iris"])) / (w_s2 + w_i2)
    lg += (np.log(s_ref / obs["sclera"]).mean(1, keepdims=True) - lg.mean(1, keepdims=True))
    res["Enrolment + iris prior (AuraTwin)"] = ciede2000(
        linrgb_to_lab(np.clip(obs["skin"] * np.exp(lg), 0, 1)), true_skin)
    # ITA (individual typology angle) of each synthetic skin sample, for subgroup reporting
    ita = np.degrees(np.arctan2(skin_lab[:, 0] - 50, skin_lab[:, 2]))
    res["_ita"] = ita
    return res


def power_from_simulation(res, rng, n_part=120, n_light=4, reps=2000):
    """Effect size and power estimated from the simulation itself (cluster = participant).
    Each simulated participant contributes n_light captures; the analysis unit is the
    participant mean of the paired difference (camera - proposed)."""
    d = res["Uncorrected camera"] - res["Enrolment + iris prior (AuraTwin)"]
    a = res["Enrolment + iris prior (AuraTwin)"]
    dz = d.mean() / d.std(ddof=1)                        # per-capture standardized effect
    # participant-level effect: average of n_light captures (assume within-person corr 0.5)
    rho = 0.5
    dz_part = dz / np.sqrt(rho + (1 - rho) / n_light)
    from math import erf, sqrt
    phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
    z_a, z_b = 1.6449, 1.2816                            # one-sided alpha 0.05, power 0.90
    n_conservative = int(np.ceil(((z_a + z_b) / 0.4) ** 2)) + 2   # d = 0.4 planning value
    # threshold test (median < 1.8): bootstrap power with clustered resampling
    # statistic = pooled capture-level median (as REQ-VIS-01 is defined), CI by bootstrapping
    # participants (clusters of n_light captures); success = upper one-sided 95% bound < 1.8
    hits, sims = 0, 200
    for _ in range(sims):
        idx = rng.integers(0, len(a), (n_part, n_light))
        boot = [np.median(a[idx][rng.integers(0, n_part, n_part)].ravel()) for _ in range(200)]
        hits += np.percentile(boot, 95) < 1.8
    p95_boot = []
    for _ in range(300):
        idx = rng.integers(0, len(a), (n_part, n_light))
        p95_boot.append(np.percentile(a[idx].ravel(), 95))
    return {"dz_capture": float(dz), "dz_participant": float(dz_part), "n_planning": n_conservative,
            "power_threshold_test": hits / sims, "p95_ci": (float(np.percentile(p95_boot, 2.5)),
                                                            float(np.percentile(p95_boot, 97.5)))}


# ----------------------------------------------------------- decision matrix
CRITERIA = [  # (key, Hebrew label, English label, weight)
    ("acc", "דיוק התאמה אישית", "Personalisation accuracy", 0.25),
    ("cost", "עלות ליחידת שימוש", "Unit cost", 0.20),
    ("lat", "זמן תגובה", "Latency", 0.15),
    ("real", "פוטו-ריאליזם", "Photorealism", 0.15),
    ("priv", "פרטיות ביומטרית", "Biometric privacy", 0.15),
    ("dev", "מאמץ פיתוח", "Development effort", 0.10),
]
ALTERNATIVES = {  # integer scores 1..5 -- weights frozen in PRD.md before totals were computed.
    # v2 (after red-team review): scores re-assigned against the ANCHORED scales of report Table 5.4
    #   Alt1 accuracy 3->4 (it does run the eye-anchored calibration on-device, but a reduced body model)
    #   Alt3 latency 5->4 (recommendation path has margin, try-on path sits exactly at the 4.5 s limit)
    "Alt1 Edge": [4, 5, 2, 1, 5, 2],
    "Alt2 Cloud LLM": [3, 2, 1, 5, 2, 5],
    "Alt3 Hybrid": [5, 4, 4, 5, 4, 3],
}
ALTERNATIVES_V1 = {"Alt1 Edge": [3, 5, 2, 1, 5, 2], "Alt2 Cloud LLM": [3, 2, 1, 5, 2, 5],
                   "Alt3 Hybrid": [5, 4, 5, 5, 4, 3]}


def score_sensitivity():
    """Perturb every single integer score by +-1 (clamped to 1..5); count rank changes of the winner."""
    base_w = np.array([c[3] for c in CRITERIA])
    names = list(ALTERNATIVES)
    total, flips, worst = 0, 0, (None, 9.9)
    for a in names:
        for i in range(len(CRITERIA)):
            for d in (-1, 1):
                sc = {k: list(v) for k, v in ALTERNATIVES.items()}
                new = min(5, max(1, sc[a][i] + d))
                if new == sc[a][i]:
                    continue
                sc[a][i] = new
                s = {k: float(np.dot(base_w, v)) for k, v in sc.items()}
                total += 1
                win = max(s, key=s.get)
                margin = s["Alt3 Hybrid"] - max(v for k, v in s.items() if k != "Alt3 Hybrid")
                if win != "Alt3 Hybrid":
                    flips += 1
                if margin < worst[1]:
                    worst = (f"{a}/{CRITERIA[i][0]}{d:+d}", margin)
    # two simultaneous worst-case changes: Alt3 -1 on its two highest-weight criteria, Alt1 +1 on two
    sc = {k: list(v) for k, v in ALTERNATIVES.items()}
    sc["Alt3 Hybrid"][0] -= 1; sc["Alt3 Hybrid"][1] -= 1
    sc["Alt1 Edge"][2] += 1; sc["Alt1 Edge"][3] += 1
    adversarial = {k: float(np.dot(base_w, v)) for k, v in sc.items()}
    return total, flips, worst, adversarial


def pugh(weights):
    w = np.asarray(weights, float)
    return {k: float(np.dot(w, v)) for k, v in ALTERNATIVES.items()}


def sensitivity(rng):
    base = np.array([c[3] for c in CRITERIA])
    rows = []
    for i, c in enumerate(CRITERIA):
        for delta in (-0.10, -0.05, 0.05, 0.10):
            w = base.copy()
            w[i] = max(0.0, w[i] + delta)
            others = [j for j in range(len(w)) if j != i]
            w[others] *= (1 - w[i]) / w[others].sum()       # renormalise to sum 1
            s = pugh(w)
            rows.append((c[0], delta, *[s[k] for k in ALTERNATIVES], max(s, key=s.get)))
    # Booklet check (§7, "בדיקת הבנה"): latency weight 0.45, cost weight 0.00
    w = base.copy(); w[2], w[1] = 0.45, 0.0
    others = [0, 3, 4, 5]; w[others] *= (1 - 0.45) / w[others].sum()
    extreme = pugh(w)
    # Dirichlet Monte-Carlo around the base weights (concentration 40)
    W = rng.dirichlet(base * 40, 20000)
    S = np.array([[np.dot(wi, v) for v in ALTERNATIVES.values()] for wi in W])
    win = (S.argmax(1) == 2).mean()
    margin = S[:, 2] - S[:, :2].max(1)
    # Uniform random weights (no prior at all)
    W2 = rng.dirichlet(np.ones(6), 20000)
    S2 = np.array([[np.dot(wi, v) for v in ALTERNATIVES.values()] for wi in W2])
    win2 = (S2.argmax(1) == 2).mean()
    return rows, extreme, win, float(np.percentile(margin, 5)), win2


# ---------------------------------------------------- competitor profiles (estimated)
RADAR_AXES = ["Colour calibration", "3D fit accuracy", "Generative realism",
              "Response speed", "Multi-category coverage", "Profit per compute unit"]
RADAR = {
    "ModiFace": [3.5, 1.5, 2.5, 4.5, 2.5, 3.5],
    "YouCam (Perfect Corp)": [3.0, 1.0, 2.5, 4.5, 3.0, 4.0],
    "Zeekit (Walmart)": [1.5, 3.0, 3.5, 3.0, 2.0, 3.0],
    "Stitch Fix": [1.0, 3.5, 1.0, 1.0, 3.0, 2.0],
    "IDM-VTON (flagship)": [1.0, 2.0, 5.0, 1.5, 1.5, 1.0],
    "AuraTwin AI (target)": [4.5, 4.0, 4.5, 4.0, 5.0, 4.5],
}
SCATTER = [  # name, cost per styling session (USD), personalisation accuracy index (0-100)
    ("ModiFace", 0.004, 62), ("YouCam", 0.003, 58), ("Zeekit", 0.030, 55),
    ("Stitch Fix", 8.00, 74), ("IDM-VTON", 0.090, 60), ("Cloud LLM (Alt2)", 0.120, 70),
    ("AuraTwin AI", 0.011, 88),
]


# ------------------------------------------------------------------ unit economics
def unit_economics():
    """Gate = rewarded ad OR affiliate click-through (one of the two per generation).
    All inputs are team assumptions (labelled in the report); the requirement threshold
    2.4x follows from a 58 % gross-margin target: 1 - 1/2.4 = 0.583."""
    ecpm_rewarded = 15.0                    # USD per 1000 rewarded views
    p_conv, aov, r_aff = 0.018, 65.0, 0.08  # conversion after click-through, order value, commission
    q_aff = 0.5                             # share of users who choose the affiliate path
    rev_ad = ecpm_rewarded / 1000
    rev_aff = p_conv * aov * r_aff
    rev = (1 - q_aff) * rev_ad + q_aff * rev_aff
    # cost of one try-on image
    api_low, api_high = 0.045, 0.090        # commercial try-on API price (status quo, ch.2)
    gpu_hour, seconds, util, overhead = 0.80, 4.5, 0.30, 1.6   # self-hosted distilled model
    self_hosted = gpu_hour / 3600 * seconds / util * overhead
    stress_rev = (1 - 0.3) * rev_ad * 0.5 + 0.3 * rev_aff       # eCPM -50 %, affiliate share 30 %
    return {"rev_ad": rev_ad, "rev_aff": rev_aff, "rev_mix": rev,
            "ratio_api_low": rev / api_low, "ratio_api_high": rev / api_high,
            "self_hosted_cost": self_hosted, "ratio_self_hosted": rev / self_hosted,
            "cost_ceiling_2_4": rev / 2.4, "gross_margin_at_2_4": 1 - 1 / 2.4,
            "stress_rev": stress_rev, "stress_ratio": stress_rev / self_hosted,
            "rag_query_cost": 0.002}


def market_build():
    """Bottom-up SAM and SOM (team assumptions, labelled in the report)."""
    # B2C ARPU per active user per month
    sessions, recs, ctr, conv, aov, comm = 6, 3, 0.08, 0.04, 65.0, 0.08
    gens_per_session, ecpm = 1.7, 15.0   # same 1.7 try-ons per session as Table 4.3 / scatter
    prem_rate, prem_price = 0.03, 9.99
    arpu_aff = sessions * recs * ctr * conv * aov * comm
    arpu_ads = sessions * gens_per_session * 0.5 * ecpm / 1000      # half of the gates via ads
    arpu_prem = prem_rate * prem_price
    arpu = arpu_aff + arpu_ads + arpu_prem
    # SOM year 3
    b2b_som = 12 * 2_000_000 * 0.60       # 12 retailers x 2M online orders/yr x $0.60 per order
    b2c_som = 1_600_000 * arpu * 12
    # SAM (target regions)
    b2b_sam = 3000 * 600_000              # 3,000 retailers with >$50M online revenue x $0.6M
    b2c_sam = 150_000_000 * arpu * 12     # monthly users of beauty/fashion apps in the regions
    return {"arpu_aff": arpu_aff, "arpu_ads": arpu_ads, "arpu_prem": arpu_prem, "arpu": arpu,
            "b2b_som": b2b_som, "b2c_som": b2c_som, "som": b2b_som + b2c_som,
            "b2b_sam": b2b_sam, "b2c_sam": b2c_sam, "sam": b2b_sam + b2c_sam}


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    _selftest_ciede2000()

    cal = calibration_study(rng)
    ita = cal.pop("_ita")
    cal_rows = [(k, np.mean(v), np.median(v), np.percentile(v, 95), (v <= 2.0).mean() * 100)
                for k, v in cal.items()]
    prop = cal["Enrolment + iris prior (AuraTwin)"]
    ita_groups = {"light (ITA>41)": ita > 41, "intermediate (10<ITA<=41)": (ita > 10) & (ita <= 41),
                  "tan/brown (ITA<=10)": ita <= 10}
    ita_rows = [(g, int(m.sum()), float(np.median(prop[m])), float(np.percentile(prop[m], 95)))
                for g, m in ita_groups.items()]
    pw = power_from_simulation(cal, rng)
    write_csv(DATA / "calibration.csv", ["method", "mean", "median", "p95", "pct_below_2"],
              [(r[0], *[round(x, 2) for x in r[1:]]) for r in cal_rows])
    write_csv(DATA / "calibration_bars.csv", ["idx", "mean", "p95"],
              [(i, round(r[1], 2), round(r[3], 2)) for i, r in enumerate(cal_rows)])

    base_w = [c[3] for c in CRITERIA]
    assert abs(sum(base_w) - 1.0) < 1e-9
    scores = pugh(base_w)
    write_csv(DATA / "pugh_stacked.csv", ["alt", *[c[0] for c in CRITERIA], "total"],
              [(i, *[round(w * s, 3) for w, s in zip(base_w, v)], round(scores[k], 2))
               for i, (k, v) in enumerate(ALTERNATIVES.items())])
    rows, extreme, win, margin5, win2 = sensitivity(rng)
    write_csv(DATA / "sensitivity.csv", ["criterion", "delta", "alt1", "alt2", "alt3", "winner"],
              [(r[0], r[1], *[round(x, 3) for x in r[2:5]], r[5]) for r in rows])
    # line data for the sensitivity figure: total vs weight of "acc" and "cost"
    for key in ("acc", "cost", "lat"):
        i = [c[0] for c in CRITERIA].index(key)
        pts = []
        for wi in np.linspace(0.0, 0.6, 13):
            w = np.array(base_w, float); w[i] = wi
            others = [j for j in range(6) if j != i]
            w[others] *= (1 - wi) / np.array(base_w)[others].sum()
            s = pugh(w)
            pts.append((round(wi, 3), *[round(s[k], 3) for k in ALTERNATIVES]))
        write_csv(DATA / f"sens_{key}.csv", ["w", "alt1", "alt2", "alt3"], pts)

    keys = ["modiface", "youcam", "zeekit", "stitchfix", "flagship", "auratwin"]
    rrows = [(i * 60, *[RADAR[k][i] for k in RADAR]) for i in range(len(RADAR_AXES))]
    rrows.append((360, *rrows[0][1:]))                # close the polygon
    write_csv(DATA / "radar.csv", ["angle", *keys], rrows)
    write_csv(DATA / "radar_legend.csv", ["key", "name", "axis_order"],
              [(k, n, " | ".join(RADAR_AXES)) for k, n in zip(keys, RADAR)])
    write_csv(DATA / "scatter.csv", ["name", "cost", "acc"], SCATTER)
    ue = unit_economics()

    WORK.mkdir(parents=True, exist_ok=True)
    with open(WORK / "benchmarks_summary.md", "w", encoding="utf-8") as f:
        f.write(f"# Benchmarks summary (seed {args.seed})\n\n")
        f.write("## Calibration simulation (n=4000 synthetic selfies, CIEDE2000 on skin)\n\n")
        f.write("| method | mean | median | p95 | % <= 2.0 |\n|---|---|---|---|---|\n")
        for r in cal_rows:
            f.write(f"| {r[0]} | {r[1]:.2f} | {r[2]:.2f} | {r[3]:.2f} | {r[4]:.1f} |\n")
        f.write("\n## Pugh matrix\n\n")
        for k, v in scores.items():
            f.write(f"- {k}: {v:.2f}\n")
        f.write(f"\nExtreme booklet check (latency 0.45, cost 0.00): {extreme}\n")
        f.write(f"\nOne-at-a-time +-0.05/0.10: winner always Alt3 = "
                f"{all(r[5] == 'Alt3 Hybrid' for r in rows)}\n")
        f.write(f"\nDirichlet(40*w) Monte-Carlo: Alt3 wins {win*100:.1f}% ; 5th pct margin {margin5:.2f}\n")
        f.write(f"Uniform-random weights: Alt3 wins {win2*100:.1f}%\n")
        sv1 = {k: float(np.dot(base_w, v)) for k, v in ALTERNATIVES_V1.items()}
        f.write(f"\nPrevious scores (v1, before red-team re-anchoring): {sv1}\n")
        tot, flips, worst, adv = score_sensitivity()
        f.write(f"\nScore sensitivity: {tot} single +-1 score changes, winner flips {flips}; "
                f"smallest margin {worst[1]:.2f} at {worst[0]}\n")
        f.write(f"Adversarial double change (Alt3 -1 on acc & cost, Alt1 +1 on lat & real): {adv}\n")
        f.write("\n## Calibration by skin-tone subgroup (proposed method)\n\n")
        for g in ita_rows:
            f.write(f"- {g[0]}: n={g[1]}, median {g[2]:.2f}, p95 {g[3]:.2f}\n")
        f.write(f"\n## Power (from simulation)\n\n{pw}\n")
        f.write(f"\n## Unit economics\n\n{ue}\n")
        f.write(f"\n## Market build-up\n\n{market_build()}\n")
    print(open(WORK / "benchmarks_summary.md", encoding="utf-8").read())


if __name__ == "__main__":
    main()
