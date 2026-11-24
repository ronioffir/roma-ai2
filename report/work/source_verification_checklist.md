# Source verification checklist — for Roni & Maayan

> **Automated metadata check, 2026-11-24:** steps 1–2 (existence; title, authors, year, venue, DOI) were run for every row of section A against Crossref, arXiv, the NeurIPS/PMLR/ICLR proceedings sites, Open Library and the EU Publications Office (DBLP refused automated access); confirmed DOIs were added to `references.bib` (this supersedes the "only `sharma2005ciede2000` carries a DOI" remark below), and the outcome per entry is in the Status column.
> **Reading each abstract and confirming it says what the report attributes to it (step 3) was not automated and remains the authors’ responsibility**, as do the rows marked "NOT FOUND" or "indirectly".

Booklet §5.3 and §17 ("אף פעם לא נאמין למודל שפה... פתחו כל מקור, ודאו שהוא קיים, וקראו אותו") require every
source to be checked by the authors. In the session that produced this report, **web search was declined**, so the
references were chosen from works the model could cite reliably, **without live verification**. Therefore:

- **DOIs were deliberately omitted wherever they were not certain** (only `sharma2005ciede2000` carries a DOI);
  page ranges were omitted for most conference papers for the same reason. Adding a DOI after you confirm it on the
  publisher page is encouraged.
- Three-step check for every row (booklet §17): (1) search the exact title in Google Scholar / IEEE Xplore /
  CVF Open Access / ACM DL / arXiv; (2) confirm authors, year, venue and DOI against the publisher page;
  (3) read at least the abstract and confirm it says what the report attributes to it.

## A. Bibliography entries (`report/references.bib`)

| # | Key | What to search | What to confirm | Status |
|---|---|---|---|---|
| 1 | segal2026booklet | Course booklet "From Problem to PDF: The Professional Preparatory Report" | Author Y. Segal, year 2026, exact title as on the cover | course material, not in public databases — not checked automatically; authors to confirm title/year against the booklet cover |
| 2 | segal2026l03 | Lesson-3 booklet (L03) | Exact title wording (Hebrew title translated), year 2026 | course material, not in public databases — not checked automatically; authors to confirm title/year against the booklet cover |
| 3 | ulrich2020product | "Product Design and Development" 7th ed. | Ulrich, Eppinger, Yang; McGraw-Hill 2020; edition | metadata confirmed (Open Library, ISBN 9781260043655, 2026-11-24), no DOI exists; note: the record gives publication date 2019 (copyright year 2020) and no edition number — check the copyright page for "7th ed." — abstract still to be read by students |
| 4 | doran1981smart | "There's a S.M.A.R.T. way to write management's goals and objectives" | Doran; Management Review 70(11):35–36, 1981 | NOT FOUND in Crossref/OpenAlex (Management Review is not indexed there; the citation only matches the reference list of the Wikipedia article "SMART criteria") — students must check |
| 5 | webster2002literature | "Analyzing the past to prepare for the future: Writing a literature review" | Webster & Watson; MIS Quarterly 26(2), 2002, pp. xiii–xxiii | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 6 | sandberg2011gap | "Ways of constructing research questions: Gap-spotting or problematization?" | Sandberg & Alvesson; Organization 18(1):23–44, 2011 | metadata confirmed (Crossref, 2026-11-24; online first 2010, print issue 18(1) January 2011), DOI added — abstract still to be read by students |
| 7 | pugh1991total | "Total Design: Integrated Methods for Successful Product Engineering" | Pugh; Addison-Wesley 1991 | metadata confirmed (Open Library: Addison-Wesley, Wokingham, 1991, 2026-11-24), no DOI exists — abstract still to be read by students |
| 8 | kerzner2017pm | "Project Management: A Systems Approach…" 12th ed. | Kerzner; Wiley 2017; edition | metadata confirmed (Open Library, ISBN 9781119165354, Wiley 2017, 2026-11-24), no DOI exists; note: the record carries no edition number — check the copyright page for "12th ed." — abstract still to be read by students |
| 9 | pmi2021pmbok | PMBOK Guide 7th ed. | PMI 2021, edition | metadata confirmed (Open Library: PMI, Seventh Edition, 2021, 2026-11-24), no DOI exists — abstract still to be read by students |
| 10 | iso31000 | ISO 31000:2018 Risk management — Guidelines | Standard number and year (iso.org) | metadata confirmed only indirectly (2026-11-24: iso.org blocks automated access; the 2018 edition is corroborated by the Crossref record of BS 31100:2021 "...implementation of BS ISO 31000:2018"), no DOI exists — students must open iso.org; standard text still to be read by students |
| 11 | ieee29148 | ISO/IEC/IEEE 29148:2018 | Exact title and year (iso.org / IEEE SA) | metadata confirmed (Crossref: IEEE standard record, approved 2018-10-23, 2026-11-24), DOI added — abstract still to be read by students |
| 12 | gdpr2016 | Regulation (EU) 2016/679 | OJ L 119, 2016 (eur-lex.europa.eu) | metadata confirmed (EU Publications Office/EUR-Lex, CELEX 32016R0679, dated 27 April 2016, 2026-11-24), no DOI exists; bib title is an abridged form of the official title; OJ L 119 number not machine-checked — abstract still to be read by students |
| 13 | euaiact2024 | Regulation (EU) 2024/1689 (AI Act) | Regulation number, year, official title (eur-lex) | metadata confirmed (EU Publications Office/EUR-Lex, CELEX 32024R1689, dated 13 June 2024, 2026-11-24), no DOI exists; bib title is an abridged form of the official title — abstract still to be read by students |
| 14 | sharma2005ciede2000 | "The CIEDE2000 color-difference formula: Implementation notes…" | Sharma, Wu, Dalal; Color Res. Appl. 30(1):21–30, 2005; DOI 10.1002/col.20070 | metadata confirmed (Crossref, 2026-11-24), existing DOI 10.1002/col.20070 confirmed — abstract still to be read by students |
| 15 | barron2017ffcc | "Fast Fourier Color Constancy" | Barron & Tsai; CVPR 2017 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 16 | hu2017fc4 | "FC4: Fully Convolutional Color Constancy with Confidence-Weighted Pooling" | Hu, Wang, Lin; CVPR 2017 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 17 | afifi2019wb | "When Color Constancy Goes Wrong: Correcting Improperly White-Balanced Images" | Afifi, Price, Cohen, Brown; CVPR 2019 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 18 | finlayson2015rootpoly | "Color Correction Using Root-Polynomial Regression" | Finlayson, Mackiewicz, Hurlbert; IEEE TIP 24(5), 2015 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 19 | nishino2004eyes | "Eyes for Relighting" | Nishino & Nayar; ACM TOG 23(3) (SIGGRAPH 2004) | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 20 | thong2023skin | "Beyond Skin Tone: A Multidimensional Measure of Apparent Skin Color" | Thong, Joniak, Xiang; ICCV 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 21 | pavlakos2019smplx | "Expressive Body Capture: 3D Hands, Face, and Body from a Single Image" | Pavlakos et al.; CVPR 2019 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 22 | goel2023hmr2 | "Humans in 4D: Reconstructing and Tracking Humans with Transformers" | Goel et al.; ICCV 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 23 | rong2021frankmocap | "FrankMocap: A Monocular 3D Whole-Body Pose Estimation System…" | Rong, Shiratori, Joo; ICCV Workshops 2021 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 24 | ruiz2022bodym | "Human Body Measurement Estimation with Adversarial Augmentation" | Ruiz et al.; 3DV 2022; author list | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 25 | zhang2020mediapipe | "MediaPipe Hands: On-device Real-time Hand Tracking" | Zhang et al.; arXiv:2006.10214, 2020 | metadata confirmed (arXiv API, arXiv:2006.10214, 2026-11-24), no DOI exists (arXiv-only preprint) — abstract still to be read by students |
| 26 | kirillov2023sam | "Segment Anything" | Kirillov et al.; ICCV 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 27 | ho2020ddpm | "Denoising Diffusion Probabilistic Models" | Ho, Jain, Abbeel; NeurIPS 2020 (vol. 33) | metadata confirmed (proceedings.neurips.cc, NeurIPS 2020 vol. 33, and arXiv:2006.11239, 2026-11-24), no DOI exists — abstract still to be read by students |
| 28 | rombach2022ldm | "High-Resolution Image Synthesis with Latent Diffusion Models" | Rombach et al.; CVPR 2022 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 29 | zhang2023controlnet | "Adding Conditional Control to Text-to-Image Diffusion Models" | Zhang, Rao, Agrawala; ICCV 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 30 | choi2021vitonhd | "VITON-HD: High-Resolution Virtual Try-On via Misalignment-Aware Normalization" | Choi, Park, Lee, Choo; CVPR 2021 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 31 | xie2023gpvton | "GP-VTON: Towards General Purpose Virtual Try-on…" | Xie et al.; CVPR 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 32 | zhu2023tryondiffusion | "TryOnDiffusion: A Tale of Two UNets" (flagship) | Zhu et al.; CVPR 2023; **also confirm every equation, dataset and runtime figure quoted in ch. 3** | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 33 | morelli2023ladivton | "LaDI-VTON: Latent Diffusion Textual-Inversion Enhanced Virtual Try-On" | Morelli et al.; ACM MM 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 34 | kim2024stableviton | "StableVITON: Learning Semantic Correspondence with Latent Diffusion Model for Virtual Try-On" | Kim et al.; CVPR 2024 | metadata confirmed (Crossref, 2026-11-24; IEEE record spells the title "Stable VITON"), DOI added — abstract still to be read by students |
| 35 | choi2024idmvton | "Improving Diffusion Models for Authentic Virtual Try-on in the Wild" (IDM-VTON) | Choi et al.; ECCV 2024 | metadata confirmed (Crossref, 2026-11-24; ECCV 2024, Springer LNCS, pp. 206–235), DOI added — abstract still to be read by students |
| 36 | jiang2020psgan | "PSGAN: Pose and Expression Robust Spatial-Aware GAN for Customizable Makeup Transfer" | Jiang et al.; CVPR 2020 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 37 | deng2019arcface | "ArcFace: Additive Angular Margin Loss for Deep Face Recognition" | Deng et al.; CVPR 2019 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 38 | heusel2017fid | "GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium" | Heusel et al.; NeurIPS 2017 | metadata confirmed (proceedings.neurips.cc, NIPS 2017 vol. 30, and arXiv:1706.08500, 2026-11-24), no DOI exists — abstract still to be read by students |
| 39 | zhang2018lpips | "The Unreasonable Effectiveness of Deep Features as a Perceptual Metric" | Zhang et al.; CVPR 2018 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 40 | radford2021clip | "Learning Transferable Visual Models From Natural Language Supervision" | Radford et al.; ICML 2021 | metadata confirmed (proceedings.mlr.press v139, ICML 2021, pp. 8748–8763, and arXiv:2103.00020, 2026-11-24), no DOI exists — abstract still to be read by students |
| 41 | li2023blip2 | "BLIP-2: Bootstrapping Language-Image Pre-training…" | Li, Li, Savarese, Hoi; ICML 2023 | metadata confirmed (proceedings.mlr.press v202, ICML 2023, pp. 19730–19742, and arXiv:2301.12597, 2026-11-24), no DOI exists — abstract still to be read by students |
| 42 | lewis2020rag | "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" | Lewis et al.; NeurIPS 2020 | metadata confirmed (proceedings.neurips.cc, NeurIPS 2020 vol. 33, and arXiv:2005.11401, 2026-11-24), no DOI exists — abstract still to be read by students |
| 43 | johnson2021faiss | "Billion-Scale Similarity Search with GPUs" | Johnson, Douze, Jégou; IEEE Trans. Big Data 7(3), 2021 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 44 | deldjoo2023fashionrec | "A Review of Modern Fashion Recommender Systems" | Deldjoo et al.; ACM Computing Surveys 56(4), 2023 | metadata confirmed (Crossref, 2026-11-24), DOI added; note: published online 21 Oct 2023, issue 56(4) is dated April 2024 — authors to decide which year to print — abstract still to be read by students |
| 45 | alhalah2017fashionforward | "Fashion Forward: Forecasting Visual Style in Fashion" | Al-Halah, Stiefelhagen, Grauman; ICCV 2017 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |
| 46 | ma2020fashiontrend | "Knowledge Enhanced Neural Fashion Trend Forecasting" | Ma et al.; ICMR 2020 | metadata confirmed (Crossref, 2026-11-24), DOI added — abstract still to be read by students |

If any entry cannot be confirmed: remove it from `references.bib` **and** remove/replace its `\cite{}` in the text
(the QA detector reports both directions of the mismatch).

## B. Numbers the report labels as team estimates ("אומדן הצוות")

None of these numbers carries a citation in the report. Before submission, either replace each one with a sourced
figure (and add the source to `references.bib`) or keep the explicit estimate label. Suggested places to look are
**suggestions only, not citations**.

| Number in the report | Where | Suggested public sources to check |
|---|---|---|
| TAM ≈ \$18.4B by 2028, CAGR ≈ 28.4% (AI in beauty & fashion) | ch. 4, Fig. 4.1 | Market-research reports on "AI in fashion" and "AI in beauty/cosmetics" (e.g., Grand View Research, MarketsandMarkets, Precedence Research, Statista summaries); compare definitions and base years |
| SAM ≈ \$3.0B, bottom-up: 3,000 retailers (>\$50M online revenue, EU+IL+US) × \$0.6M licence + 150M app users × \$0.68 × 12 | ch. 4, Table 4.1 | Retailer counts (Eurostat e-commerce statistics, annual reports); monthly active users of beauty/fashion apps (app-analytics reports) |
| SOM ≈ \$27.4M (year 3): 12 retailers × 2M orders × \$0.60 + 1.6M users × \$0.68 × 12 | ch. 4, Table 4.1 | Retailer order volumes; per-order pricing of comparable SaaS; user-acquisition benchmarks |
| Online apparel return rates 30–40% (size/fit main reason) | ch. 1–2 | Retail returns surveys (e.g., NRF/Appriss Retail returns reports), academic studies on fashion e-commerce returns |
| Shade-mismatch claims for foundation/lipstick bought online | ch. 1–2 | Consumer surveys by beauty retailers/brands; academic work on shade matching; otherwise keep as estimate |
| Diffusion try-on cost \$0.045–0.090 per image (commercial API, status quo) and \$0.0053 self-hosted (L4 \$0.80/h, 4.5 s, 30 % utilisation, ×1.6 overhead) | ch. 2, ch. 4 Table 4.3 | Public API price lists; cloud GPU on-demand hourly prices; measured seconds per image after distillation |
| Rewarded-video eCPM \$15 (tier-1); ARPU components \$0.30 affiliate + \$0.08 ads + \$0.30 premium = \$0.68 | ch. 4 | Mobile ad-network benchmark reports; subscription conversion benchmarks |
| Affiliate funnel 1.8% conversion × \$65 AOV × 8% commission | ch. 5 unit economics | Affiliate-network commission tables for fashion/beauty; e-commerce conversion benchmarks |
| Derived: expected revenue per gated generation \$0.054 (q = 0.5) → 0.60–1.21× commercial API, 10.2× self-hosted; stress case 6.2× | ch. 2 REQ-BIZ-12, ch. 4, ch. 7 | Recomputed automatically by `scripts/generate_beauty_benchmarks.py` once the inputs above are updated |
| Competitor radar/scatter scores | ch. 4 Fig. 4.2–4.3 | Team technical assessment (labelled "הערכת הצוות"); document the rationale per score |

## C. Computed (not estimated) numbers

The calibration-simulation results (ΔE00 by method) and the Pugh-matrix totals/sensitivity are **computed** by
`scripts/generate_beauty_benchmarks.py` (seed 2026) and are reproducible; they are synthetic-simulation results and
are labelled as such in the report.

## D. References added in iteration 4 (prompt 08, AURAM) -- verify before submission

| Key | Claimed source | Check |
|---|---|---|
| `kerbl2023gaussian` | Kerbl et al., "3D Gaussian Splatting for Real-Time Radiance Field Rendering", ACM TOG 42(4), 2023 | [ ] |
| `ramamoorthi2001sh` | Ramamoorthi & Hanrahan, "An Efficient Representation for Irradiance Environment Maps", SIGGRAPH 2001 | [ ] |
| `wu2024gaussian4d` | Wu et al., "4D Gaussian Splatting for Real-Time Dynamic Scene Rendering", CVPR 2024 | [ ] |
| `yao2023react` | Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023 | [ ] |

Also new in iteration 4: the spectral simulation (`scripts/spectral_optics.py`) uses **analytic approximations**
(Planck curves for D65 and A, Gaussian peaks for F11 and the LED, the Wyman-Sloan-Shirley CMF fit, Gaussian camera
sensitivities), not the tabulated CIE data. All economics inputs in Table 4.3 are team assumptions.

## E. Web sources added in v3.7 (opened 2026-11-24; re-open before the final submission)

| Key | Figure used in the report | Kind of source |
|---|---|---|
| `coresight2023returns` | 24.4% online apparel return rate (US); size/fit top reason for 53% of surveyed retailers | research firm report page |
| `nrf2025returns` | 19.3% of online sales returned (US, 2025) | trade-association press release |
| `fbi2026vfr` | virtual fitting room market USD 6.86bn (2025), CAGR 17.7% to 2034 | analyst summary (secondary) |
| `kings2024aibeauty` | AI in beauty and cosmetics USD 3.54bn (2023), CAGR 19.14% to 2031 | analyst summary (secondary) |
| `loreal2018modiface` | ModiFace acquired by L'Oréal, 2018 | company news release |
| `walmart2021zeekit` | Zeekit acquisition announced by Walmart, 2021 | company announcement |
| `perfect2026results` | 859 brand clients | 6-K text read through a mirror site; the original filing was not reachable |
| `stitchfix2026tenk` | USD 20 styling fee per Fix | SEC Form 10-K |
| `google2026vertex` | Virtual Try-On USD 0.06 per image | official pricing page (prices change) |

Not sourced, still team assumptions: SAM/SOM inputs, competitor cost per session, CAC of USD 2.00,
monthly churn of 12%, the 80% drop-off for a 15-second ad.
