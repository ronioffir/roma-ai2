"""spectral_optics.py -- physically based image formation for the AURAM calibration study.

rho_k = sum_lambda E(lambda) S(lambda) Q_k(lambda) dlambda + eps_k,  k in {R, G, B}   (report eq. 2.1)

* Spectra on 400..700 nm in 10 nm steps.
* Illuminants E: D65 and Illuminant A (Planck approximations, 6504 K / 2856 K), F11 (tri-band
  fluorescent: three narrow peaks + weak continuum) and a low-CRI phosphor LED (blue pump + broad
  phosphor). All are approximations built from closed forms -- not the tabulated CIE data.
* Camera sensitivities Q_k: Gaussian approximations; they are NOT linear combinations of the colour
  matching functions, which is exactly what makes metameric failure possible.
* CIE 1931 colour matching functions: multi-lobe Gaussian fit of Wyman, Sloan & Shirley (2013).
* Surfaces: skin (melanin + haemoglobin absorption), sclera (white with age-related yellowing,
  log-normal vascular redness and a non-Lambertian tear-film specular term), iris (four
  self-reported categories).
Synthetic data only; parameters are design assumptions stated in the report.
"""
from __future__ import annotations

import numpy as np

LAM = np.arange(400.0, 701.0, 10.0)
DL = 10.0


def _g(lam, mu, s1, s2):
    s = np.where(lam < mu, s1, s2)
    return np.exp(-0.5 * ((lam - mu) / s) ** 2)


def cmf(lam=LAM):
    x = 1.056 * _g(lam, 599.8, 37.9, 31.0) + 0.362 * _g(lam, 442.0, 16.0, 26.7) - 0.065 * _g(lam, 501.1, 20.4, 26.2)
    y = 0.821 * _g(lam, 568.8, 46.9, 40.5) + 0.286 * _g(lam, 530.9, 16.3, 31.1)
    z = 1.217 * _g(lam, 437.0, 11.8, 36.0) + 0.681 * _g(lam, 459.0, 26.0, 13.8)
    return np.stack([x, y, z])                                  # (3, L)


def planck(T, lam=LAM):
    l = lam * 1e-9
    b = 1.0 / (l ** 5 * (np.exp(1.4388e-2 / (l * T)) - 1.0))
    return b / b.max()


def gauss(mu, s, lam=LAM):
    return np.exp(-0.5 * ((lam - mu) / s) ** 2)


ILLUM = {
    "D65": planck(6504),
    "A": planck(2856),
    "F11": 0.10 * planck(4000) + 0.55 * gauss(435, 5) + 1.00 * gauss(545, 5) + 0.80 * gauss(611, 6),
    "LED": 1.00 * gauss(450, 10) + 0.85 * gauss(565, 52),
}
ILLUM = {k: v / v.max() for k, v in ILLUM.items()}
ILLUM_NAMES = list(ILLUM)
# phone screen at full white (OLED primaries), the known "flash" of the enrolment and of every capture
SCREEN = 0.85 * gauss(458, 11) + 1.0 * gauss(530, 17) + 0.95 * gauss(618, 10)
SCREEN = SCREEN / SCREEN.max()
QCAM = np.stack([gauss(600, 33), gauss(535, 38), gauss(458, 26)])   # camera R, G, B sensitivities (3, L)

CMF = cmf()
WHITE_XYZ = (CMF * ILLUM["D65"]).sum(1) * DL                       # perfect reflector under D65


def melanin_abs(lam=LAM):
    return (lam / 500.0) ** -3.46


def hb_abs(lam=LAM):
    # oxy-haemoglobin alpha/beta bands (542 / 577 nm) and the tail of the Soret band
    return 1.0 * gauss(542, 12) + 1.1 * gauss(577, 10) + 1.6 * gauss(410, 14)


def skin_reflectance(mel, hb):
    """mel, hb: (n,) concentrations -> (n, L) diffuse reflectance."""
    return 0.04 + 0.62 * np.exp(-mel[:, None] * 0.55 * melanin_abs()[None]) \
        * np.exp(-hb[:, None] * 0.35 * hb_abs()[None])


def sclera_reflectance(yellow, red):
    """Sclera is not a white card: episcleral/conjunctival vessels (red, log-normal) and
    age-related lipid/bilirubin deposition (yellow) both absorb."""
    return 0.80 * (1 - yellow[:, None] * gauss(455, 35)[None]) * np.exp(-red[:, None] * hb_abs()[None])


IRIS_BASE = {
    "brown": 0.03 + 0.22 / (1 + np.exp(-(LAM - 610) / 35)),
    "hazel": 0.05 + 0.22 / (1 + np.exp(-(LAM - 570) / 40)),
    "green": 0.06 + 0.16 * gauss(540, 45),
    "blue": 0.07 + 0.16 * gauss(470, 45),
}
IRIS_CATS = list(IRIS_BASE)


def iris_reflectance(cat_idx, scale):
    base = np.stack([IRIS_BASE[c] for c in IRIS_CATS])          # (4, L)
    return base[cat_idx] * scale[:, None]


def render(E, S):
    """Camera responses rho_k = sum E S Q_k dlambda.  E: (n,L) or (L,), S: (n,L) -> (n,3)."""
    return (np.atleast_2d(E) * S) @ QCAM.T * DL


def xyz_d65(S):
    return (ILLUM["D65"][None] * S) @ CMF.T * DL


def xyz_to_lab(xyz):
    t = xyz / WHITE_XYZ
    d = 6 / 29
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4 / 29)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], -1)


def training_reflectances(rng, n=3000):
    """Smooth random reflectances + skin samples, used to fit 3x3 colour-correction matrices."""
    k = rng.integers(2, 6, n)
    S = np.zeros((n, LAM.size))
    for i in range(n):
        mus = rng.uniform(380, 720, k[i]); ws = rng.uniform(25, 120, k[i]); a = rng.uniform(-1, 1, k[i])
        S[i] = 0.4 + sum(a[j] * gauss(mus[j], ws[j]) for j in range(k[i]))
    S = np.clip(S, 0.02, 0.95)
    skin = skin_reflectance(rng.uniform(0.3, 4.5, n // 2), rng.uniform(0.3, 2.2, n // 2))
    return np.vstack([S, skin])


def fit_ccm(E, S_train):
    """Least-squares 3x3 matrix: camera RGB under illuminant E -> CIE XYZ under D65."""
    A = render(E, S_train)
    B = xyz_d65(S_train)
    M, *_ = np.linalg.lstsq(A, B, rcond=None)
    return M                                                     # rgb @ M -> xyz
