# 03 — Chapter-writing prompts 1–8 (booklet §18.3–18.9), adapted for AuraTwin AI

Skills: `academic-source-researcher`, `beauty-ai-domain-architect`, `scientific-hebrew-writer`,
`visual-tikz-pgfplots-artist`.

## Prompt 1 — Set up the project
```text
You are a LaTeX expert for Hebrew/English documents. Create a LuaLaTeX project in report/ using our template
auratwin-report.cls: main.tex, coverpage.tex, references.bib, chapters/ and figures/. Use MiKTeX and biber.
Write nothing outside this folder. Create one file per chapter: ch1_intro, ch2_problem, ch3_literature, ch4_market,
ch5_alternatives, ch6_workplan, ch7_risks, ch8_summary.
Success: it compiles to a PDF with a cover, a TOC and 8 chapter titles.
```

## Prompt 2 — Outline with a page budget
```text
Read the AuraTwin AI problem statement in PRD.md and propose an outline for a 40-page preparatory report.
Page budget: intro 3 (pp. 1–3), problem 4 (4–7), literature 9 (8–16), market 6 (17–22), design 8 (23–30),
plan 4 (31–34), risk 2 (35–36), summary 1 (37), references 3 (38–40). Give sections and subsections for each
chapter, and one sentence on what each section must prove. Do not write the chapters yet.
```

## Prompt 3 — Real sources only
```text
Find peer-reviewed papers on: colour constancy and CIEDE2000; eye/sclera as illumination probes; SMPL-X and
monocular body/hand reconstruction; body-measurement estimation; diffusion virtual try-on (TryOnDiffusion,
IDM-VTON, StableVITON, LaDI-VTON, GP-VTON, VITON-HD, ControlNet, LDM); identity and perceptual metrics (ArcFace,
FID, LPIPS); multimodal retrieval and RAG (CLIP, BLIP-2, RAG, FAISS); fashion recommendation and trend forecasting.
Prefer the last 5 years (IEEE, ACM, CVF, NeurIPS/ICML, Springer). For each give title, authors, year, venue and
DOI only if certain. Do not invent anything. If you cannot verify a paper, leave it out.
Output report/references.bib and a table: paper, method, main result, limitation.
```
*Used with the restriction that web search was unavailable: only works the model could cite reliably were kept,
DOIs omitted unless certain, and every entry listed in `report/work/source_verification_checklist.md`.*

## Prompt 4 — Write one chapter (run once per chapter)
```text
Write report/chapters/ch3_literature.tex in Hebrew, about 9 pages (printed pages 8–16). Use PRD.md and
references.bib only. Structure: thematic and critical (4 pillars), not paper by paper. Include the literature
matrix (\cellok/\cellpartial/\cellno, last row "הפרויקט המוצע: AuraTwin AI — זה הפער"), the flagship Venn
figure, the flagship equations and a one-sentence gap. Style: third person, professional, English terms with
\en{} on first use, every number in \num{}. Every factual claim has a \cite{}. Do not cite anything else.
Use only the template's headings, tables and boxes; start with a managerbox. Reference every figure and table
in the text with one analytical sentence.
```
Per-chapter variations: ch1 funnel (Fig. 1.1); ch2 problem chain, research vs design table, requirements table
REQ-xxx-nn; ch4 TAM/SAM/SOM (labelled team estimates), competitor table, radar, log scatter; ch5 three alternatives,
Pugh matrix from `figures/data/pugh_stacked.csv`, sensitivity, architecture; ch6 WBS, RACI, Gantt; ch7 risk matrix
and tables; ch8 one page + three actions.

## Prompt 5 — A fancy figure
```text
Create a fancy TikZ figure of the AuraTwin AI data flow, right to left: selfie → on-device landmarks and
calibration → calibrated colour vector + keypoints → cloud SMPL-X fit and multimodal RAG → recommendations and
affiliate links → ad gate → latent-diffusion try-on. Put it inside the reportfigure environment and Hebrew labels
in \heb{}. Keep the width under 12.4 cm, no overlapping labels. Add a Hebrew caption and a \label, and one
sentence for the text that explains what we learn from it.
```

## Prompt 6 — A fancy table
```text
Turn the competitor data into the template's reporttable. The first column is on the right. All text is
right-aligned. Mark numbers with \num{}. Total width 12.4 cm. Caption above the table and a \label.
Highlight the AuraTwin AI row with \hlrow.
```

## Prompt 7 — Fix the build
```text
Run lualatex, biber, lualatex, lualatex (-jobname=report). Read report.log. Fix every line that starts with "!",
every undefined reference and every overfull box wider than 5pt. Do not change the template unless the problem
repeats (then follow prompts/04 B3). Report what you changed and why.
Success: 0 errors, and the page count (44) is printed.
```

## Prompt 8 — Page-by-page review
```text
Render every page of report.pdf to an image and look at each one. Report: a heading at the bottom of a page,
a split box or table, a nearly empty page, reversed Hebrew, overlapping labels, text outside the margins,
a figure not mentioned in the text. List page numbers. Then hand the list to the fixer, recompile and check again.
```

## How it was used in this project
- Data for every chart is produced by `scripts/generate_beauty_benchmarks.py` (CSV in `report/figures/data/`),
  so no plotted number is typed by hand; estimates and simulated data are labelled in captions.
- Prompt 8 is automated by `scripts/qa_detector_audit.py` (renders pages to `report/figures/previews/pages/`)
  and complemented by visual inspection of key pages.


---

## Round 3 — UX prompts (skill `ux-entrepreneur-strategist`)

### UX-1 — Human & cultural need (chapter 1)
```text
Write a section "הצורך האנושי: למה המראה היומיומי עדיין מנוחש" in third person: AI already assists writing,
coding, navigation and shopping, yet daily appearance is still guesswork. Name the cross-demographic audience
(teenage girls, women of all ages, men with high grooming awareness), the two decision moments (morning,
online shopping) and the product form (browser extension + companion app). No unsourced statistics.
Keep chapter 1 inside pages 1-3: compensate by removing text that the user journey now covers.
```

### UX-2 — Who pays the price (chapter 2)
```text
Add one sentence to 2.1.3 naming the groups who suffer from the uncalibrated photo. Describe users of the
problem, not users of the solution (booklet: a problem statement must not name the solution).
```

### UX-3 — Audience segments and user journey (chapter 4)
```text
Replace the segments table with a cross-demographic one: segment, usage moment, value proposition, revenue
line (each revenue line must already exist in the unit economics). Add a TikZ figure of the 4-step journey,
right to left: (1) onboarding in 30 s with eye colour, height, weight, circumferences and 3 snapshots;
(2) daily/shopping assistant; (3) optional value-exchange gate (15 s rewarded video or VIP);
(4) 1-click shop-the-look. Each step shows its time budget and the REQ that measures it. Width <= 12.4 cm.
```

### UX-4 — UI mockup (chapter 5)
```text
Build a TikZ/tcolorbox wireframe: a browser window on a partner product page with the AuraTwin side panel
(recommended size with ±1.2 cm, shade match %, trend match, gate button, "image stays on device") and the
companion phone app (calibrated shade with ΔE00, trend badge, three shop-the-look cards, gate and VIP
buttons). Use only palette colours and template commands; every mixed Hebrew/English label is ONE \heb{}
unit with \en/\num inside. Caption says the values are illustrative. Add one analytical paragraph tying
every on-screen number to a requirement, and state that there are no gendered defaults.
```
