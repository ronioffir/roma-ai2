# CHANGELOG — AuraTwin AI report template & project

Template = `report/base-report.cls` (base layer) + `report/auratwin-report.cls` (thin company layer).
Version source of truth: `VERSION`. Rule (booklet §15.6): a problem that repeats across the
document is fixed **once** in the template, with a version bump and an entry here.

## [3.5] — 2026-11-24 — Cover fixes, table overhaul, pocket-mirror watermark (prompt 13, pass 1)
### Changed
- **Cover:** the ID-number line was removed from the author box (names, department, advisor and the hypothetical
  partner remain); submission date is now 24.11.2026.
- **Tables (template-level, `base-report.cls`):** every `reporttable` now spans the full text block
  (`\tableobjwidth` = 15.5 cm) instead of 12.4 cm; side padding 4.5 pt → 6 pt; `\arraystretch` 1.35 → 1.4
  (1.5 was tried first and cost a page once the new content was in);
  `\hyphenpenalty` and `\exhyphenpenalty` are 10000 inside tables, so a cell never breaks inside a word or after
  a hyphen (e.g. "מיקרו-" / "אינטראקציה"). Figures keep the 12.4 cm limit.
  **Note:** this deliberately departs from the 12.4 cm object width the template took from booklet §19.3.
- **Tables (per table):** the column ratios of all 26 tables were recalibrated to their content; Table 7.2 moved
  from `\scriptsize` to `\footnotesize`.
- **Watermark:** `\setpagemark` (base) + `\auratwinwatermark` (layer) set the pocket-mirror mark, scale 0.17 and
  45% opacity, under every page number (preliminary and body pages; the cover has no page number).
### Added: uncertainty as the headline (passes 2-3)
- **`scripts/uncertainty_voi.py`** (new, `--check` verifies 13 quoted values) and
  `report/figures/data/uncertainty_summary.json` plus 8 CSVs. Synthetic data and team assumptions only.
  - **Hierarchical Bayesian posterior** of the median colour error on the simulated 120 x 4 pilot (Gibbs sampler,
    log scale, random participant and illuminant-family effects, residual variance per family). Tested families:
    median 1.87, 95% credible interval 1.75-2.00, P(median <= 1.8) = 12%. A new family: 0.89-3.87, P = 47%.
  - **Design value:** 94% of the uncertainty of the population median comes from having only four illuminant
    families. 240 x 4 leaves the interval at +/-29% (from +/-30%); the same 480 captures as 60 x 8 give +/-22%.
  - **Hardware sensitivity:** median error against room light (600-nit screen at 30 cm) and burst length. The
    8-frame burst meets the target up to about 200 lux; SNR scales with flash ratio x sqrt(frames).
    `simulate_captures()` gained an optional `hw` argument; the default random stream is unchanged, and
    `statistical_validation.py --check` still passes.
  - **Economics as a distribution:** 200,000 Monte Carlo draws over 12 team assumptions. LTV/CAC median 6.1,
    90% interval 2.2-18.3, P(>= 3.8) = 78%. EVPI = $0.68 per acquired user; EVPPI ranks the partner conversion
    A/B test first (26%), then CAC (12%), churn (3%); GPU cost is worth 0.
  - **Constraint map:** latency caps the diffusion at 8 steps, the margin requirement only at about 26, so
    there is a 3.3x unused cost margin.
- **Report:** Sec. 5.3.2 (posterior, Fig. 5.5), Sec. 5.3.7 (hardware against model and economics, Fig. 5.7,
  Table 5.7), Sec. 4.4 (LTV/CAC distribution and value of information, Fig. 4.4), Sec. 6.5 (convergence log,
  Table 6.5, from this changelog and `report/work/red_team_review.md`), a fifth contribution in Sec. 5.4, the
  "transparent layer" box in Sec. 1.2, and the pocket-mirror callout (`mirrorbox`) on the abstract page.
  The abstract, Ch.8 and the open decisions now quote intervals and probabilities.
- **Hebrew-first:** every chart label, legend and diagram node is Hebrew (architecture, Gantt, risk matrix,
  market layers, radar, scatter, bars); keywords are Hebrew; eleven captions now state the takeaway.
### Removed or condensed, to stay at 40 body pages
- Ch.3: the DDPM forward-process equation (textbook), the body-reconstruction warning box (folded into the
  paragraph), and shorter reviews of domains B-D and of the flagship limitations.
- Ch.4: the five product paragraphs became one. Ch.5: shorter descriptions of the alternatives, one merged
  architecture paragraph, and the closing relighting sentence. Ch.6: the spherical-harmonics equation (the
  roadmap is now one paragraph) and the milestone example box (now a sentence).
- Charts were made 10-20% shorter; Tables 4.1, 4.3, 5.1-5.3 moved to `\footnotesize`.
### Verified
- 44 pages (4 + 40), chapter starts 1/4/8/16/22/31/35/37, references 38 (50 entries). 0 errors, 0 undefined
  references, 0 overfull boxes, 0 bad boxes inside tables (3 underfull boxes remain: two in the abbreviation
  list, one in Sec. 3.1). Both `--check` scripts pass. Abstract about 345 words.

## [3.4] — 2026-11-23 — Pass 4: final audit fixes (prompt 12)
Fresh-context examiner (Sonnet, PDF text only): **66/100**, 15 items. Each was verified against the source before
any fix; the resolution is in `report/work/red_team_review.md` (iteration 5).
### Fixed
- **Median framing:** "on the target" → the median of 1.86 **exceeds** the 1.8 target and does not meet it yet
  (abstract, Ch.5, Table 8.1).
- **Session cost:** the AURAM session cost was still $0.011 in Table 4.2 and in the scatter-plot star; it is now
  $0.025, as in the text and `scatter.csv`. The persuasive "26 points above the line" was removed.
- **Ch.2 box:** "×2.4 above the threshold" → ×3.3. **Ch.7:** "four" → "five" residuals in the medium zone
  (Table 7.2).
- **Literature search:** it was attributed to the wrong task (TSK-1.1, the baseline experiment) and now sits in
  work package 1.
- **Cover:** the hypothetical partner no longer names real companies (L'Oréal-ModiFace was also analysed as a
  competitor).
- **Economics labelling:** labelled "team assumptions not yet validated" in the abstract and the summary.
  "Independent channels" became "separate channels" that share retailer conversions, and 3.8 is called the team's
  target threshold.
- **Power:** the observed ICC of 0.12 is below the planned range, which only raises H0a power; H0b power is low
  while the median is near 1.8.
- **Privacy:** "reduces regulatory exposure in advance" became "reduces but does not remove". Minors need parental
  consent (GDPR Art. 8), and compliance will go through legal review. The open decisions now include the legal
  framework (minors' consent, liability for a wrong recommendation). The mockup now says "the photo is not
  stored" instead of "stays on the device".
- **Ranking bias:** the score contains no commission or sponsorship term, and a ranking audit is planned for the
  pilot.
- **Defensibility:** eye-based illumination estimation is prior art [Nishino & Nayar]; the novelty is the
  combination with the flash and the prior, so the advantage is time, not a patent.
- **Body sizing:** the result is stated as a simulation under an independence assumption, to be tested on 60
  participants.
- **Notation:** "הולם" → `Holm`.
### Not changed (with reason)
- **Pugh accuracy score:** the examiner read the *latency* anchor ("both paths on target") as the accuracy anchor.
  Accuracy 5 is "eye calibration + full metric body", which AURAM has.
- **ID placeholder on the cover:** IDs are masked by requirement (master prompt).
- **Half-page scope/assumptions section:** no room in the 44-page budget. The material exists in §2.1.4 (assumptions
  and constraints) and Table 8.1 + the out-of-scope line.
### Verified
- 44 pages, chapter starts on budget, 0 errors, 0 warnings, 0 undefined references.
- Detector, readability and number check PASS.

## [3.3] — 2026-11-23 — Pass 3: language, BiDi & readability (prompt 11)
### Changed (prose; no new content or numbers)
- **Topic sentences:** 15 paragraph openers of the form "From the figure / table it emerges that…" are rewritten
  as direct topic sentences (Ch. 2–7). This was the filler pattern flagged by the red-team examiner.
- **Terminology:** the obsolete "ad gate" (שער הפרסום) wording is unified to the value-exchange gate in the
  Ch.4 manager box, comparison Table 4.2 and task TSK-3.2 (Tables 6.1, 6.3).
- **Typo:** "שששה" → "שישה" (Ch.7).
- **Density:** the densest paragraph (Ch.3 colour-constancy methods) is tightened, with the same facts and citations.
### Verified by scan
- **Spacing:** no double spaces, no space before punctuation, no space inside parentheses.
- **Words:** no doubled words.
- **BiDi:** no Latin text in a Hebrew paragraph outside `\en{}`, `\num{}` or math (custom scan).
- **Audits:** readability & math audit PASS (punctuation spacing, Hebrew in math, symbols defined); QA detector BiDi
  families PASS.
- **Build:** 44 pages, chapter starts on budget, 0 errors, 0 warnings, 0 undefined references; number check PASS.

## [3.2] — 2026-11-23 — Pass 2: visual polish & layout cleanliness (prompt 10)
### Changed (template)
- Abbreviation list in **three columns** (`abbrevtable`). Preliminary page ד׳ had overflowed its text block by
  10.7 pt and ran into the footer; it now has a clean bottom margin.
### Fixed (figures)
- **Value labels:** the value labels of Figs 2.2 and 5.4 go from `\tiny` to `\scriptsize`, with two fixed
  decimals (12.40, not 12.4), matching the text and the CSVs.
- **Legends:** the Fig. 2.2 legend moves top-right (it covered the gray-world P95 bar), and the Fig. 5.4 legend is
  enlarged.
- **Radar:** tick labels `\tiny` → `\scriptsize`.
- **User journey (Fig. 4.4):** time labels `\tiny` → `\scriptsize`, in Dust instead of a pale grey (contrast).
- **Architecture (Fig. 5.3):**
  - edge labels → `\scriptsize`;
  - "funded" label removed: it overlapped the router box in a gap narrower than the word, and the text states it;
  - "Lab, keypoints, H" moved off the cloud-lane title.
- **WBS / Gantt (Figs 6.1–6.2):** task, week and row labels `\tiny` → `\scriptsize`.
- The UI mockup keeps its small UI micro-typography on purpose.
### Fixed (tables and captions)
- Column widths in Tables 2.2, 3.2, 4.2 and 7.1: unbreakable IDs were 2–4 pt wider than their columns.
- Overfull lines: 17 → 5, all < 5 pt. Overfull vboxes: 2 → 0.
- Shorter captions for Table 5.6 and Fig. 5.5, so each fits one line in the lists.
### Tried and reverted
- `\@nobreaktrue` before §3.3 (to fill a 20% gap on p.9). It pushed the report to 45 pages; reverted.
### Verified
- 44 pages, chapter starts 1/4/8/17/23/31/35/37, references 38.
- 0 errors, 0 warnings, 0 undefined references.
- QA detector PASS, readability & math PASS, number check PASS.

## [3.1] — 2026-11-23 — Pass 1: report completeness & investor sharpness (prompt 09)
### Changed (content only; layout, template and page budget unchanged)
- **Ch.1 manager box:** purpose of the report, its three decision-makers (advisor/committee, partner, team) and
  "why now". It is rewritten at the same length.
- **Ch.4 §4.5:** the three moats are condensed into one paragraph. A new **three-step gated go-to-market** follows:
  1. one partner retailer with an A/B test on returns and add-to-cart;
  2. the companion app for users acquired via the extension;
  3. licensing to further retailers only after a proven drop in returns.

  CAC and conversion uplift are flagged as unvalidated pilot targets.
- **Ch.7 Table 7.3 (new):** edge cases and failure modes. These cover glasses, makeup or lashes, night-mode screen,
  mixed light, skin change or red/yellow sclera (no medical inference), and the sponsored-ranking conflict of
  interest (sponsorship sets try-on availability, not the score).
- **Ch.8:** the 3-actions figure is replaced by Table 8.1, the **evidence status** of colour, body, try-on,
  economics and partner (what exists today vs what is still open). It is followed by the prioritized open decisions
  with triggers and fallbacks, an explicit **out-of-scope** line, and the immediate actions (now in text).
- **Grounding:** no new numbers were introduced.
### Verified
- 44 pages, chapter starts 1/4/8/17/23/31/35/37, references 38, 0 errors, 0 warnings.
- QA detector PASS, readability & math PASS, number check PASS.
### Skills applied
- `red-team-examiner` (checklist applied in this session; no fresh-context examiner run).
- `expert-committee-prd`, `ux-entrepreneur-strategist`, `scientific-hebrew-writer`.
- `bidi-qa-detector` / `bidi-qa-fixer`, `human-readability-math-auditor`.
- The repository has no GitHub-workflow skill; the established two-author commit convention was followed.

## [3.0] — 2026-11-19 — AURAM: rebrand, spectral physics, hierarchical statistics, tiered economics (prompt 08)
### Brand
- The product is renamed **AURAM** (Aura + RAM) in the chapters, cover, `main.tex`, classes, scripts, README, PRD and
  skills. The wordmark is letter-spaced "AURAM" under the pocket mirror (TikZ and PNG). A Ch.1 examplebox explains
  the name.
- Not renamed, on purpose:
  - verbatim prompts and historical logs (they are records);
  - test fixtures;
  - internal names `auratwin-report.cls` and `\auratwinlogo`, which are API names, and renaming them would break
    builds and documentation.
### Physics (Pillar 1)
- New `scripts/spectral_optics.py` provides the spectral pieces of the simulation, all as analytic approximations:
  - **Illuminants:** D65, A, F11 and a low-CRI LED.
  - **Colour matching functions:** the Wyman-Sloan-Shirley CMF fit.
  - **Camera:** Gaussian camera sensitivities.
  - **Skin:** melanin and haemoglobin.
  - **Sclera:** yellowing plus log-normal vascular redness plus a tear-film specular term, with an explicit
    highlight mask.
  - **Iris:** four categories.
  - **Screen flash:** the flash spectrum.
- `generate_beauty_benchmarks.py`: the calibration study is now spectral, with 6 methods, including the
  screen-flash delta and AURAM's precision-weighted fusion. The fusion's error models are fitted on a **separate**
  training simulation (seed 99). A new output `calibration_by_illuminant.csv` shows the metameric failure.
- Ch.2 eq. 2.1 gives image formation. Ch.3 now covers sclera physiology and the von Kries limitation. Ch.5 adds
  eq. 5.3 (flash delta + fusion) and Table 5.5 (per-illuminant medians).
- **Results changed and are reported as they are:**

  | Measure | Old | New | Target |
  |---|---|---|---|
  | Uncorrected camera, mean ΔE₀₀ | 4.89 | 6.58 | — |
  | Gray-world AWB, mean ΔE₀₀ | 9.77 | 16.03 | — |
  | AURAM P95 | 4.81 | 4.25 | ≤ 4.5 (now met) |
  | AURAM median | 1.37 | 1.86 | ≤ 1.8 (now at the edge) |

  RSK-ALG-07 is redefined as the median risk.
### Statistics (Pillar 4)
- `statistical_validation.py` now uses:
  - a crossed mixed-effects pilot (participant × illuminant, statsmodels), where the same person's captures are
    correlated;
  - residual SD per ITA bracket;
  - Wilcoxon on participant means as a sensitivity analysis;
  - a cluster bootstrap for H0b;
  - Holm correction;
  - a power grid over N 30–180, d 0.25–0.60 and ICC 0.3–0.7 (`power_grid.csv`).

  The t = 30.9 report was removed.
- **Results:** β₁ = −4.43 [−4.68, −4.18], ICC 0.12. H0a is rejected. **H0b is not rejected** (median 1.94, upper
  bound 2.06).
- **Power:** N = 60 gives power 0.9 at d = 0.40 (ICC 0.5), and the planned N = 120 still holds at d = 0.25.
- `--check` now also verifies the calibration and economics numbers, the per-illuminant table and the LTV/CAC grid
  (52 values).
### Economics (Pillar 2)
- The 15 s ad gate is replaced by three tiers: an instant edge silhouette, a sponsored try-on at $0.02, and a 3 s
  micro-interaction / credits / VIP at $7.99.
- Eq. 4.1 adds the e^(−βt) friction drop-off: 72% are kept at 3 s versus 20% at 15 s.
- Table 4.3 gives the assumptions and outputs, and Table 4.4 an LTV/CAC grid over GPU cost $0.008–0.025 × monthly
  churn 8–20%.
- **Base LTV/CAC is 6.0.** It stays above 3.8 at every GPU cost only while churn is at most 12%, and fails at 20%.
  This is stated in the report; nothing was solved backwards.
- Revenue per try-on is $0.120, so REQ-BIZ-12 holds even at $0.025 (4.8×).
- The market is rebuilt from the new ARPU of $1.59: SAM ≈ $4.7B and SOM ≈ $45.0M. The scatter point moves to the
  all-in session cost of $0.025.
- Text changed to match: the journey figure, segments table, mockup CTAs, architecture nodes, risks RSK-BIZ-04 and
  RSK-ALG-07, the summary and the abstract.
### Moonshot (Pillar 3) and voice (Pillar 6)
- Ch.3 cites 3D Gaussian splatting and spherical-harmonic lighting.
- Ch.5 contrasts VITON-HD and IDM-VTON with relightable AURAM.
- **New Ch.6 §6.5 roadmap:** eq. 6.1 SH relighting with presets, 4D Gaussian splatting and a ReAct stylist agent,
  explicitly outside the 14 weeks. It sits in Ch.6 because Ch.5 had no room left in its 8-page budget.
- Four new references (`kerbl2023gaussian`, `ramamoorthi2001sh`, `wu2024gaussian4d`, `yao2023react`) are added to
  the verification checklist.
- **Voice boxes:**
  - Ch.1: the name.
  - Ch.3: skin is not an RGB matrix.
  - Ch.4: the origin of the idea (bathroom light, returns, the free prior).
  - Ch.8: why AURAM.
### Template
- v3.0. One-off `\@nobreaktrue` before two headings (§1.5, §3.9) where the cheap `\needspace` break left
  17–40% of a page blank.
- Verified: 44 pages, chapter starts 1/4/8/17/23/31/35/37, references 38, 0 errors, 0 warnings.

## [2.0] — 2026-11-19 — Luxury Pocket Mirror & Red-Team Master Polish (+ Assignment 01 feedback)
### Changed (company layer `auratwin-report.cls`)
- **New Pocket-Mirror logo** replaces Shield-Eye everywhere (cover, every header, app mockup, README). It is an
  opened vintage compact at a 3/4 angle, with these parts:
  - **Lid:** a Velvet Forest case with a Copper edge and a Mustard rim, tilted −7°.
  - **Glass:** an Egg Nog → Dust diagonal sheen with an AI sparkle inside a Copper iris contour.
  - **Clasp:** an Egg Nog pearl on a Mustard collar.
  - **Base:** a Garnet band with concentric Mustard / Egg Nog rings.

  The shape reference is the user's "Rose-Gold Floral Compact Mirror" image. `scripts/render_hyperframes_cover.py`
  draws the identical SVG (`auratwin_logo.png`, `cover_banner.png`, `readme_hero.png`). Cover spacing was
  0.55 → 0.95 cm and the header mark 0.14 → 0.155.
- Colour tokens `brandzebra` (Egg Nog!25) and `brandheadtext` (Egg Nog).
### Changed (base `base-report.cls`): editorial tables
- `\arraystretch` 1.25 → **1.35**, booktabs rules in **Mustard** (`\heavyrulewidth` 1.1 pt), zero rule separation
  so fills touch the rules, header text in the layer token (Egg Nog on Velvet Forest), zebra rows Egg Nog!25,
  `\tabcolsep` 4 → 4.5 pt.
- `\cellno` is now an empty cell. The examiner read "---" as an unfinished table, and the matrix caption already
  defines empty cells as the gap.
### Fixed (base): 67 → **0** LaTeX warnings
- `fix-cm` provides scalable CM math fonts at 11.5 pt (6 font warnings).
- `\pdfstringdefDisableCommands` makes `\LR`, `\RL`, `\textenglish` and `\texthebrew` transparent in bookmarks
  (53 hyperref warnings).
- `hypcap=false` before `\captionof` in `reporttable*` and `reportfigure*` (4 warnings).
- biblatex: `\DeclareBibliographyAlias{standard}{manual}`, `\DeclareLanguageMapping{hebrew}{english}`,
  `language=english, autolang=none` (3 warnings).
### Fixed (base): orphaned section headings
- The automatic `\needspace` before a subsection is skipped directly after another heading (`\if@nobreak`). Its
  penalty was a legal break *between* a section and its first subsection, found with `\tracingpages`.
- Known limitation, documented in the class: `\needspace`'s cheap optional break. A global rewrite was tried and
  reverted (it broke float placement in Ch. 4).
### Added (content, Assignment 01 feedback: statistics as the home discipline)
- Ch. 2, eq. 2.1: formal H₀a/H₁a (paired difference of ΔE₀₀) and H₀b/H₁b (threshold 1.8). Wilcoxon signed-rank +
  paired *t* with a 95% CI, Holm, α = 0.05.
- Ch. 3, Sec. 3.10.5: simulated pilot of the planned test (n = 120 × 4), plus the statistics-student examplebox
  explaining why the simulated effect size is inflated.
- Ch. 5, Sec. 5.3.2: eq. 5.4 Bayesian precision-weighted fusion of keypoints, OLS regression on reported covariates
  and tape measurement; Table 5.5 MAE / RMSE / R² / residual variance.
- Ch. 4: personal-voice examplebox "בקול שלנו" (eye as a colour ruler, self-funding gate, everyday need across ages
  and genders).
- `scripts/statistical_validation.py` writes JSON, CSV and PNG outputs. It replays the exact random stream of
  `generate_beauty_benchmarks.py`, so the Monte-Carlo Pugh numbers match, and `--check` verifies 17 numbers in
  the chapters.
### Changed (content, red-team pass 78/100)
- Tables 2.2, 3.2, 3.3, 4.1, 6.4 rebalanced (no lone words or markers). Products in Table 4.1 and the ARPU
  paragraph are set as single LTR units (no dangling ×).
- Eq. 2.1 uses `\mathrm{vs.}` (`\text{vs.}` rendered ".vs" in RTL).
- Repetitive "Table X shows" sentences trimmed (Ch. 2, 5). Two boxes that duplicated adjacent text were removed:
  the Ch. 2 REQ-VIS-01 test box (now in eq. 2.1 + Table 2.2) and the Ch. 5 novelty box (folded into Sec. 5.4's
  opening).
- Venn scaled 0.88. The Sec. 5.2.4 sensitivity paragraph was condensed (same numbers).
- Verified: 44 pages, chapter starts 1/4/8/17/23/31/35/37, references 38, 0 errors, 0 warnings. QA detector PASS,
  readability & math PASS, number check PASS.

## [1.4.0] — 2026-11-17 — design corrections (user prompt 02)
### Changed (company layer)
- **New "Shield-Eye" logo** (security, trust and aesthetics). It is a Velvet Forest heraldic shield with a Mustard
  inner rim, holding an Egg Nog eye whose Mustard iris contains a keyhole pupil, with three small palette arches
  at the base. The TikZ macro and the PNG (`scripts/render_hyperframes_cover.py`) use identical geometry; the header
  mark is scaled to 0.14.
- Cover course line: the seminar wording was removed (`\doccourse` in main.tex). Every other cover field is unchanged.
- Cover banner: palette swatches without colour-name labels; the new logo is used.
### Changed (figures, one-off)
- p.5 funnel: the direction arrow and its labels moved outside the funnel (no overlap), the layer texts were shortened
  to fit inside each trapezoid, and the layers were made more compact.
- p.17 Venn: three distinct hues (Velvet Forest / Copper / Dust), criterion names as solid pills outside the circles,
  and every paper label fully inside its region. The positions come from a clearance search
  (`report/work/venn_layout.py`, minimum clearance 0.16 cm).
- p.21 TAM/SAM/SOM: nested circles in three distinct solid colours with only short tags inside; values and
  descriptions moved to a leader-line column (no text over circles).
- p.34 UI mockup: modern product styling. It has a sans-serif UI font, soft card shadows (two low-opacity layers), a
  lock icon in the URL bar, a "מאובטח" chip, a circular match ring, gradient capsule buttons, a phone bezel with a
  status bar, a halter-top product illustration and the new logo.
- p.39 risk heatmap: solid opaque fills (Garnet / Mustard / Dust), larger cells and numbers, risk IDs in white pills
  placed below the scores.
### Fixed
- `shadows.blur` (package pgf-blur) is not installed, and MiKTeX's silent on-the-fly install froze every pass. The
  dependency was removed and the soft shadows are drawn with standard TikZ.

## [1.3.0] — 2026-11-16 — "Luxury, Vintage, Bold" identity, logo, readability (skills 11 + 12)
### Added (company layer `auratwin-report.cls`)
- Palette colours `auraEggNog` #FBEDC3, `auraMustard` #CCB363, `auraDust` #6F7D7B, `auraCopper` #C27E35,
  `auraGarnet` #76290B, `auraVelvetForest` #1E3226, mapped onto the semantic names (`brandprimary`=Velvet Forest,
  `brandsecondary`=Dust, `brandaccent`=Mustard, `brandcream`/`brandtint`=Egg Nog, `brandwarn`=Garnet,
  `brandexample`=`brandhighlight`=Copper). Every heading, box, table, header, TikZ and pgfplots colour follows.
- Logo: `\auratwinlogo[scale]` (Egg Nog top-left arch + Mustard inverted dome + Dust top-right arch + Velvet
  Forest eye and baseline) and `\auratwinwordmark[scale]`; the mark is in every page header.
- Editorial chapter opening: number in a Velvet Forest badge with a Mustard ring, Mustard + Dust double rule,
  Copper section numbers. New cover: Egg Nog field, Velvet Forest double frame with Mustard inner rule, wordmark.
### Added (base `base-report.cls`)
- `\accenttext{}` / `\mutedtext{}` semantic text colours; chapters no longer call `\textcolor`
  (detector rule "manual formatting").
- `brandcream`, `brandhighlight` default colour names.
### Changed (readability, skill human-readability-math-auditor)
- `\parskip` 4 → **6 pt**; `\arraystretch` 1.18 → **1.25**; box padding 8/5 → **9/6 pt**, 9 pt before/after boxes.
- Body text **11.5 pt** (booklet Table 11.1 allows 11–12 pt), with `\onehalfspacing`. This keeps the 40-page body
  budget with the new spacing and the UX content.
- Manager / key-message / example boxes on Egg Nog backgrounds; header rule in Mustard.
### Fixed
- Cover: the overlay picture opened a paragraph, so `\vspace*` was applied after the first text line and the
  wordmark overlapped the institution line → `\par` after the overlay.
- `build.sh`: each pass has a 300 s timeout (a pass hung once; after killing it, the aux files must be deleted).

## [1.2.1] — 2026-11-16 — fixes from the QA detector/fixer loop on the full report
### Fixed (template-level — each finding repeated on ≥ 3 pages or originated in the class)
- **Bibliography exceeded its 3-page budget** (5 pages, QA-034): `\printreferences` now sets the IEEE
  list in `\footnotesize`, single spacing, `\bibitemsep` 1.2 pt.
- **Narrow table columns overflowed** (Overfull \hbox 5–9 pt in 4 tables): `\tabcolsep` 6 pt → 4 pt
  inside `reporttable` / `reporttable*`; both environments gained an optional font-size argument
  (`\begin{reporttable}[\footnotesize]{…}`).
- **TOC and lists spilled to 2 pages each** (preliminary pages = 6 instead of 4): `\compacttoc`
  in `\footnotesize`; `\compactlists` in `\scriptsize`; inter-chapter `\addvspace` suppressed in both.
- TOC subsection entries were larger than section entries (leftover `\small`) — removed.
- `abbrevtable`: `\en` is mapped to the breakable `\enlong` inside the 2-column list.
### Added
- `\compacttoc`, `\compactlists{…}`, `abbrevtable` + `\abbr{…}{…}` (preliminary pages ג׳–ד׳).
### Text-level (one-off) fixes, logged in `report/work/qa_fix_log.md`
- Long boxed English phrases → `\enlong` (25 occurrences, script `report/work/enlong_convert.py`).
- RTL arrow direction in the critical-path sentence (`\to` → `\leftarrow`), table column widths,
  equation split (eq. 5.4/5.5), floating table 7.2 pinned, Ch.3–6 page budgets.

## [1.2.0] — 2026-11-16 — fixes from the Prompt B4 stress test
### Fixed (template-level)
- **`\en` is now boxed** (`\mbox{\textenglish{…}}`). With an unboxed `\textenglish`, the comma typed
  after one English unit was rendered next to the *following* unit (`RAG, SMPL-X` → `SMPL-XRAG`).
  Reproduced in `report/tests/bidi_comma_test.tex` (variant ג is the fix). Added `\enlong{}` as the
  unboxed, line-breakable variant for long English titles.
- English fonts get `Ligatures=TeX`, so `\num{10--20}` prints an en dash instead of `--`.
- `tabularx` inside `reporttable`: the float/center are now opened in command form
  (`\table`/`\center`) so `tabularx` finds `\end{reporttable}` (was: "File ended while scanning
  use of \TX@get@body").
- `keymessagebox` / `warningbox` titles were set in the (white) title colour and were invisible;
  the title is now printed in the accent colour at the start of the box text.
- Footer "עמוד N מתוך M": M used `\ref` (gave a section number) — now `\pageref*` to the body-end label.

## [1.1.0] — 2026-11-16 — stages 4–6 (booklet Table 15.2)
### Added
- Styled tables `reporttable` / `reporttable*` (header row `\headrow` + `\hc{}`, zebra rows,
  width 12.4 cm, first column on the right natively), matrix cell marks `\cellok` `\cellpartial` `\cellno`.
- Four boxes: `managerbox`, `keymessagebox`, `warningbox`, `examplebox` (never split) + `codebox`.
- `reportfigure` / `reportfigure*` wrappers (English LTR environment, caption below).
- Header/footer with per-slot direction; "page N of M" right-to-left.
- biblatex + biber IEEE, `\printreferences` (English LTR list under a Hebrew heading).
- Company layer `auratwin-report.cls`: palette, TikZ logo, document fields (`\doctitlehe` …),
  document types (`report`/`proposal`/`spec`), double-frame cover page, © in the English font,
  year taken from the compile date.

## [1.0.0] — 2026-11-16 — stages 1–3
### Added
- LuaLaTeX + polyglossia (Hebrew default, English other), fonts checked with `fc-list :lang=he`
  (David / Arial / Times New Roman / Consolas).
- Geometry 2.5 cm all sides + 0.5 cm binding gutter (right edge, RTL), 12 pt, 1.5 line spacing.
- BiDi units `\en`, `\num`, `\hebmath`, `\heb`, `\copyrightsign`; generated numbers
  (sections, figures, tables, equations) forced LTR so 1.2 never shows as 2.1.
- Chapter-based numbering, TOC depth 3, `\needspace` before every section/subsection,
  every chapter on a new page, Hebrew-letter preliminary page numbers (א׳–ד׳).

---
## Project log
- 2026-11-16 — Skills (9), PRD, prompts log, template v1.2.0, stress test passed (0 errors).
- 2026-11-16 — Full report (8 chapters). The QA detector/fixer loop converged in 6 rounds and the template moved to v1.2.1.
- 2026-11-16 — Red-team pass 1 (fresh context, Sonnet) scored **73/100** with 10 weaknesses. The upgrade pass changed:
  - **Statistics:** H1a/H1b with Holm correction, cluster bootstrap, and a power analysis taken from the simulation.
  - **Decision matrix:** anchored Pugh scales and score sensitivity. The totals are now 4.30 / 3.40 / 2.85.
  - **Economics:** the gate is modelled as ad *or* affiliate; the commercial API vs self-hosted distilled costs are separated;
    and the market is built bottom-up (SAM ≈ $3.0B, SOM ≈ $27.4M).
  - **Privacy:** contradiction fixed (REQ-SEC-11).
  - **Work plan:** ethics, labelling and validation tasks added; dependencies and float fixed.
  - **Risks:** 2 new risks, and each residual is now tied to evidence.
  - **Gap statement:** sharpened.
- 2026-11-16 — Red-team re-check: **83/100**, with 4 points resolved, 6 partial and 0 open. The 6 new items N1–N6 were fixed.
  Detector verdict **PASS**: 44 pages, 0 errors, 0 undefined references, 0 overfull > 5 pt.
