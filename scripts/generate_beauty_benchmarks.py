#!/usr/bin/env python3
"""
generate_beauty_benchmarks.py -- data generator for the AURAM preparatory report.

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

import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


# ------------------------------------------------------------- calibration study (spectral, v3)
# v3 (AURAM, prompt 08): physically based image formation (scripts/spectral_optics.py) replaces
# the v1/v2 uniform RGB multipliers. Four illuminant families (D65, A, F11, low-CRI LED), a sclera
# with yellowing + log-normal vascular redness + tear-film specular highlights, and a screen-flash
# delta frame. Method names are the row labels of report Fig. 2.2 / Fig. 5.2.
import spectral_optics as so  # noqa: E402

METHODS = ["Uncorrected camera", "Gray-world AWB", "Sclera anchor (diagonal, no mask)",
           "Sclera + iris prior (diagonal, masked)", "Flash delta only",
           "AURAM: flash delta + eye anchor (Bayesian)"]
PROPOSED = METHODS[-1]
_CCM = {}
VAR_A0, VAR_A1, VAR_F_SCALE = 0.02, 1.5, 1.0   # error models of the two estimators; set by fit_fusion_weights()


def fit_fusion_weights(n=3000, seed=99):
    """Design-time calibration of AURAM's fusion on a SEPARATE training simulation (seed 99, never
    used for evaluation): relative squared error of the eye-anchor estimate regressed on the squared
    iris discrepancy (the metamerism detector), and the scale of the flash noise model."""
    global VAR_A0, VAR_A1, VAR_F_SCALE
    rng = np.random.default_rng(seed)
    P = draw_persons(rng, n)
    I = simulate_captures(rng, P, rng.integers(0, 4, n), internals=True)
    rel = lambda x: (np.linalg.norm(x - I["xyz_true"], axis=1) / np.linalg.norm(I["xyz_true"], axis=1)) ** 2 / 3
    X = np.column_stack([np.ones(n), I["disc"] ** 2])
    (a0, a1), *_ = np.linalg.lstsq(X, rel(I["xyz_a"]), rcond=None)
    VAR_A0, VAR_A1 = max(float(a0), 1e-6), max(float(a1), 0.0)
    VAR_F_SCALE = float(np.mean(rel(I["xyz_f"])) / np.mean(I["var_f0"]))
    return {"var_a0": VAR_A0, "var_a1": VAR_A1, "var_f_scale": VAR_F_SCALE}


def _ccms():
    if not _CCM:
        rng = np.random.default_rng(7)                      # fixed calibration set of the "factory"
        S = so.training_reflectances(rng)
        _CCM["D65"] = so.fit_ccm(so.ILLUM["D65"], S)
        _CCM["SCREEN"] = so.fit_ccm(so.SCREEN, S)
        # camera exposure constant: unbiased skin luminance under D65 with the camera's own AE rule
        # (face priority, highlights protected) -- a well-calibrated phone under daylight
        _CCM["scl_pop"] = so.sclera_reflectance(np.array([0.12]), np.array([0.10]))[0]
        sk = so.skin_reflectance(rng.uniform(0.3, 4.5, 2000), rng.uniform(0.3, 2.2, 2000))
        rho = so.render(so.ILLUM["D65"], sk)
        rs = so.render(so.ILLUM["D65"], _CCM["scl_pop"][None])
        expo = np.minimum(0.45 / rho[:, 1:2], 0.92 / rs.max())
        _CCM["k_cam"] = float(np.median(so.xyz_d65(sk)[:, 1] / ((rho * expo) @ _CCM["D65"])[:, 1]))
    return _CCM


def draw_persons(rng, n):
    """Persistent traits of n people (skin, sclera, iris)."""
    return {"mel": rng.uniform(0.3, 4.5, n), "hb": rng.uniform(0.3, 2.2, n),
            "yellow": np.clip(rng.lognormal(np.log(0.10), 0.5, n), 0, 0.6),     # age-related deposition
            "red": rng.lognormal(np.log(0.08), 0.6, n),                             # baseline vascular redness
            "iris": rng.integers(0, 4, n), "iris_scale": rng.lognormal(0, 0.18, n)}


HW_DEFAULT = {"flash_ratio": (0.08, 0.40),   # screen-flash / ambient irradiance on the face (range)
              "burst": 8,                    # aligned frames averaged per delta image
              "noise_scale": 1.0}            # sensor-noise multiplier (1 = mid-range phone)


def simulate_captures(rng, P, fam, internals=False, hw=None):
    """One capture per row of the trait dict P under illuminant family index fam (n,).
    Returns {method: DeltaE00 array} and the true skin Lab.
    hw (v3.5, scripts/uncertainty_voi.py) overrides the hardware assumptions of HW_DEFAULT; the
    number and order of random draws do not depend on it, so the default stream is unchanged."""
    hw = {**HW_DEFAULT, **(hw or {})}
    C = _ccms()
    n = fam.size
    E = np.stack([so.ILLUM[so.ILLUM_NAMES[f]] for f in fam])
    w = rng.uniform(0, 0.25, n)[:, None]                     # some daylight through a window
    E = (1 - w) * E + w * so.ILLUM["D65"][None]
    skin = so.skin_reflectance(P["mel"], P["hb"])
    red_now = P["red"] * rng.lognormal(0, 0.45, n)           # fatigue / irritation on the day
    scl = so.sclera_reflectance(P["yellow"], red_now)
    iris = so.iris_reflectance(P["iris"], P["iris_scale"])
    spec = rng.beta(1.5, 14, n)                              # tear-film specular fraction (non-Lambertian)
    spec_res = 0.25 * spec                                   # residual after the explicit highlight mask
    scl_raw = (1 - spec)[:, None] * scl + spec[:, None]
    scl_msk = (1 - spec_res)[:, None] * scl + spec_res[:, None]
    bg = np.clip(0.35 + rng.normal(0, 0.12, (n, 1)) + 0.1 * np.sin(so.LAM[None] / rng.uniform(20, 60, (n, 1))), 0.05, 0.9)

    rho = {k: so.render(E, s) for k, s in {"skin": skin, "scl_raw": scl_raw, "scl_msk": scl_msk,
                                           "iris": iris, "bg": bg}.items()}
    expo = 0.45 / rho["skin"][:, 1:2] * rng.uniform(0.85, 1.15, (n, 1))   # face-priority auto-exposure
    expo = np.minimum(expo, 0.92 / rho["scl_raw"].max(1, keepdims=True))     # ...but highlights are protected
    sd = {"skin": 0.0015, "scl_raw": 0.002, "scl_msk": 0.0025, "iris": 0.003, "bg": 0.002}
    obs = {k: np.clip(v * expo + rng.normal(0, sd[k], v.shape), 1e-4, 1.0) for k, v in rho.items()}

    true_lab = so.xyz_to_lab(so.xyz_d65(skin))
    to_lab = lambda rgb, M: so.xyz_to_lab(np.clip(rgb @ M, 1e-6, None))
    res = {}
    # 1-2: camera white balance (partial and full gray-world), fixed exposure constant
    scene = 0.45 * obs["skin"] + 0.40 * obs["bg"] + 0.15 * obs["scl_raw"]
    awb = scene.mean(1, keepdims=True) / scene
    for name, g in (("Uncorrected camera", 1 + 0.35 * (awb - 1)), ("Gray-world AWB", awb)):
        res[name] = gb_ciede(to_lab(obs["skin"] * g * C["k_cam"], C["D65"]), true_lab)
    # 3: naive diagonal sclera anchor -- population sclera, no specular mask
    ref_pop = so.render(so.ILLUM["D65"], C["scl_pop"][None])
    g3 = ref_pop / obs["scl_raw"]
    res[METHODS[2]] = gb_ciede(to_lab(obs["skin"] * g3, C["D65"]), true_lab)
    # 4: diagonal MAP on log-gains: masked sclera (population) + iris prior of the reported category
    ref_iris = so.render(so.ILLUM["D65"], np.stack([so.IRIS_BASE[c] for c in so.IRIS_CATS])[P["iris"]])
    ws_, wi_ = 1 / 0.03 ** 2, 1 / 0.12 ** 2
    lg = (ws_ * np.log(ref_pop / obs["scl_msk"]) + wi_ * np.log(ref_iris / obs["iris"])) / (ws_ + wi_)
    lg += np.log(ref_pop / obs["scl_msk"]).mean(1, keepdims=True) - lg.mean(1, keepdims=True)
    res[METHODS[3]] = gb_ciede(to_lab(obs["skin"] * np.exp(lg), C["D65"]), true_lab)
    # 5: screen-flash delta frame: dI = I_flash - I_ambient = reflectance under the KNOWN screen spectrum
    f_abs = rng.uniform(*hw["flash_ratio"], (n, 1))          # screen at full white, ~30 cm, vs the room light
    def delta(S, amb):
        clean = so.render(so.SCREEN, S) * expo * f_abs / so.render(so.SCREEN, np.ones((1, so.LAM.size)))[:, 1:2] \
            * so.render(E, np.ones((1, so.LAM.size)))[:, 1:2]
        # aligned burst (8 frames by default): sensor + residual motion/flicker
        noise_sd = hw["noise_scale"] * (np.sqrt(2) * 0.0015 + 0.002 * amb) / np.sqrt(hw["burst"])
        return clean + rng.normal(0, 1, clean.shape) * noise_sd, noise_sd
    d_skin, nsd_skin = delta(skin, obs["skin"])
    d_scl, _ = delta(scl_msk, obs["scl_msk"])
    d_iris, _ = delta(iris, obs["iris"])
    # enrolment: the user's own sclera measured once under the screen in a dim room (low noise)
    scl_enr = so.sclera_reflectance(P["yellow"], P["red"])
    enr_scr = so.render(so.SCREEN, scl_enr) * (1 + rng.normal(0, 0.01, (n, 3)))
    k = enr_scr[:, 1:2] / np.clip(d_scl[:, 1:2], 1e-5, None)
    xyz_flash = np.clip((d_skin * k) @ C["SCREEN"], 1e-6, None)
    res[METHODS[4]] = gb_ciede(so.xyz_to_lab(xyz_flash), true_lab)
    # 6: AURAM -- enrolment-referenced eye anchor (diagonal) fused with the flash estimate.
    ref_enr = so.render(so.ILLUM["D65"], scl_enr) * (1 + rng.normal(0, 0.01, (n, 3)))
    lg6 = (ws_ * np.log(ref_enr / obs["scl_msk"]) + wi_ * np.log(ref_iris / obs["iris"])) / (ws_ + wi_)
    lg6 += np.log(ref_enr / obs["scl_msk"]).mean(1, keepdims=True) - lg6.mean(1, keepdims=True)
    xyz_anchor = np.clip((obs["skin"] * np.exp(lg6)) @ C["D65"], 1e-6, None)
    # metamerism detector: the iris seen through the anchor vs the iris seen by the flash
    iris_a = (obs["iris"] * np.exp(lg6)) @ C["D65"]
    iris_f = (d_iris * k) @ C["SCREEN"]
    disc = np.linalg.norm(iris_a - iris_f, axis=1) / np.clip(np.linalg.norm(iris_f, axis=1), 1e-6, None)
    var_a = (VAR_A0 + VAR_A1 * disc ** 2)[:, None]
    var_f = VAR_F_SCALE * ((nsd_skin / np.clip(d_skin, 1e-5, None)) ** 2).mean(1, keepdims=True)
    if internals:
        return {"xyz_a": xyz_anchor, "xyz_f": xyz_flash, "disc": disc, "var_f0": var_f / VAR_F_SCALE,
                "xyz_true": so.xyz_d65(skin)}
    xyz6 = (xyz_anchor / var_a + xyz_flash / var_f) / (1 / var_a + 1 / var_f)
    res[PROPOSED] = gb_ciede(so.xyz_to_lab(xyz6), true_lab)
    return res, true_lab


def gb_ciede(a, b):
    return ciede2000(a, b)


def calibration_study(rng, n=4000):
    fit_fusion_weights()
    P = draw_persons(rng, n)
    fam = rng.integers(0, 4, n)
    res, lab = simulate_captures(rng, P, fam)
    res["_ita"] = np.degrees(np.arctan2(lab[:, 0] - 50, lab[:, 2]))
    res["_fam"] = fam
    return res


def power_from_simulation(res, rng, n_part=120, n_light=4, reps=2000):
    """Effect size and power estimated from the simulation itself (cluster = participant).
    Each simulated participant contributes n_light captures; the analysis unit is the
    participant mean of the paired difference (camera - proposed)."""
    d = res["Uncorrected camera"] - res[PROPOSED]
    a = res[PROPOSED]
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
    "AURAM (target)": [4.5, 4.0, 4.5, 4.0, 5.0, 4.5],
}
SCATTER = [  # name, cost per styling session (USD), personalisation accuracy index (0-100)
    ("ModiFace", 0.004, 62), ("YouCam", 0.003, 58), ("Zeekit", 0.030, 55),
    ("Stitch Fix", 8.00, 74), ("IDM-VTON", 0.090, 60), ("Cloud LLM (Alt2)", 0.120, 70),
    ("AURAM", 0.025, 88),
]


# ------------------------------------------------------------------ unit economics
# ------------------------------------------------------------------ unit economics (v3, tiers)
# v3 (AURAM, prompt 08): the 15-second rewarded-ad gate is replaced by three tiers. Every input is a
# TEAM ASSUMPTION, labelled as such in the report (Table 4.3); the outputs are what the assumptions
# imply -- nothing is solved backwards from a target.
ECON = {
    "sessions": 6, "recs": 3, "ctr": 0.08, "conv": 0.04, "aov": 65.0, "comm": 0.08,  # affiliate path
    "tryons_per_session": 1.7,
    "share_sponsored": 0.60,        # share of try-on requests on items of a sponsoring retailer (Tier 2)
    "sponsor_fee": 0.02,            # USD the retailer pays per generated try-on (engagement SKU fee)
    "conv_uplift": 1.5,             # purchase multiplier after a try-on (3x add-to-cart -> 1.5x purchase)
    "micro_seconds": 3.0,           # Tier 3 brand micro-interaction
    "ad_seconds": 15.0,             # the old gate, for comparison
    "dropoff_15s": 0.80,            # assumed share lost by a 15 s unskippable ad -> beta = ln(5)/15
    "micro_ecpm": 8.0,              # USD per 1000 completed 3 s micro-interactions
    "sub_rate": 0.03, "sub_price": 7.99, "pay_fee": 0.15,     # VIP / Pro subscription
    "rec_cost": 0.002,              # cloud cost of one recommendation session
    "gpu_cost": 0.015,              # all-in serverless cost of one generated try-on (base)
    "gpu_grid": (0.008, 0.015, 0.025),
    "churn": 0.12,                  # monthly churn (base); LTV horizon = 1 / churn months
    "churn_grid": (0.08, 0.12, 0.20),
    "cac": 2.00,                    # blended customer-acquisition cost, USD
}


def tier_economics(gpu_cost=None, churn=None, e=ECON):
    """Monthly contribution of one active user under the three-tier engine."""
    c = e["gpu_cost"] if gpu_cost is None else gpu_cost
    lam = e["churn"] if churn is None else churn
    beta = math.log(1 / (1 - e["dropoff_15s"])) / e["ad_seconds"]          # drop-off rate per second of friction
    keep_micro = math.exp(-beta * e["micro_seconds"])
    keep_ad = math.exp(-beta * e["ad_seconds"])
    req = e["sessions"] * e["tryons_per_session"]                            # try-on requests / month (Tier 1 serves all)
    n_spon = req * e["share_sponsored"]
    n_micro = req * (1 - e["share_sponsored"]) * keep_micro
    n_gen = n_spon + n_micro                                                 # generated try-ons / month
    uplift = e["conv"] * (e["conv_uplift"] - 1) * e["aov"] * e["comm"]       # extra commission per try-on
    rev_aff = e["sessions"] * e["recs"] * e["ctr"] * e["conv"] * e["aov"] * e["comm"]
    rev_gen = n_spon * e["sponsor_fee"] + n_micro * e["micro_ecpm"] / 1000 + n_gen * uplift
    rev_sub = e["sub_rate"] * e["sub_price"] * (1 - e["pay_fee"])
    revenue = rev_aff + rev_gen + rev_sub
    cost = n_gen * c + e["sessions"] * e["rec_cost"]
    margin = revenue - cost
    ltv = margin / lam
    per_tryon_rev = (n_spon * e["sponsor_fee"] + n_micro * e["micro_ecpm"] / 1000) / n_gen + uplift
    return {"beta": beta, "keep_micro": keep_micro, "keep_ad": keep_ad, "req": req, "n_gen": n_gen,
            "uplift": uplift, "rev_aff": rev_aff, "rev_gen": rev_gen, "rev_sub": rev_sub,
            "revenue": revenue, "cost": cost, "margin": margin, "gross_margin": margin / revenue,
            "ltv": ltv, "ltv_cac": ltv / e["cac"], "per_tryon_rev": per_tryon_rev,
            "biz12_ratio": per_tryon_rev / c, "gpu_cost": c, "churn": lam}


def unit_economics():
    base = tier_economics()
    grid = [(c, lam, tier_economics(c, lam)["ltv_cac"]) for c in ECON["gpu_grid"] for lam in ECON["churn_grid"]]
    worst_biz12 = tier_economics(max(ECON["gpu_grid"]))["biz12_ratio"]
    return {"base": base, "grid": grid, "worst_biz12": worst_biz12}


def market_build():
    """Bottom-up SAM and SOM (team assumptions). B2C ARPU = monthly revenue of the tier engine."""
    arpu = tier_economics()["revenue"]
    b2b_som = 12 * 2_000_000 * 0.60       # 12 retailers x 2M online orders/yr x $0.60 per order
    b2c_som = 1_600_000 * arpu * 12
    b2b_sam = 3000 * 600_000              # 3,000 retailers with >$50M online revenue x $0.6M
    b2c_sam = 150_000_000 * arpu * 12     # monthly users of beauty/fashion apps in the regions
    return {"arpu": arpu, "b2b_som": b2b_som, "b2c_som": b2c_som, "som": b2b_som + b2c_som,
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
    fam = cal.pop("_fam")
    cal_rows = [(k, np.mean(v), np.median(v), np.percentile(v, 95), (v <= 2.0).mean() * 100)
                for k, v in cal.items()]
    prop = cal[PROPOSED]
    ita_groups = {"light (ITA>41)": ita > 41, "intermediate (10<ITA<=41)": (ita > 10) & (ita <= 41),
                  "tan/brown (ITA<=10)": ita <= 10}
    ita_rows = [(g, int(m.sum()), float(np.median(prop[m])), float(np.percentile(prop[m], 95)))
                for g, m in ita_groups.items()]
    pw = power_from_simulation(cal, rng)
    write_csv(DATA / "calibration.csv", ["method", "mean", "median", "p95", "pct_below_2"],
              [(r[0], *[round(x, 2) for x in r[1:]]) for r in cal_rows])
    write_csv(DATA / "calibration_bars.csv", ["idx", "mean", "p95"],
              [(i, round(r[1], 2), round(r[3], 2)) for i, r in enumerate(cal_rows)])
    # metameric failure: median error per illuminant family for the four calibration methods
    import spectral_optics as so
    ill_rows = [(m, *[f"{float(np.median(cal[m][fam == f])):.2f}" for f in range(4)]) for m in METHODS[2:]]
    write_csv(DATA / "calibration_by_illuminant.csv", ["method", *so.ILLUM_NAMES], ill_rows)

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
    write_csv(DATA / "ltv_cac_grid.csv", ["gpu_cost", "churn", "ltv_cac"],
              [(c, l, round(v, 2)) for c, l, v in ue["grid"]])

    WORK.mkdir(parents=True, exist_ok=True)
    with open(WORK / "benchmarks_summary.md", "w", encoding="utf-8") as f:
        f.write(f"# Benchmarks summary (seed {args.seed})\n\n")
        f.write("## Calibration simulation (spectral v3, n=4000 synthetic selfies, CIEDE2000 on skin)\n\n")
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
        f.write("\n## Median error by illuminant family (metameric failure of diagonal anchors)\n\n")
        f.write("| method | " + " | ".join(so.ILLUM_NAMES) + " |\n|---|---|---|---|---|\n")
        for r in ill_rows:
            f.write(f"| {r[0]} | " + " | ".join(r[1:]) + " |\n")
        f.write(f"\nFusion error models (fitted on the seed-99 training simulation): "
                f"var_a0={VAR_A0:.5f}, var_a1={VAR_A1:.4f}, flash scale={VAR_F_SCALE:.3f}\n")
        f.write("\n## Calibration by skin-tone subgroup (proposed method)\n\n")
        for g in ita_rows:
            f.write(f"- {g[0]}: n={g[1]}, median {g[2]:.2f}, p95 {g[3]:.2f}\n")
        f.write(f"\n## Power (from simulation)\n\n{pw}\n")
        f.write(f"\n## Unit economics\n\n{ue}\n")
        f.write(f"\n## Market build-up\n\n{market_build()}\n")
    print(open(WORK / "benchmarks_summary.md", encoding="utf-8").read())


if __name__ == "__main__":
    main()
