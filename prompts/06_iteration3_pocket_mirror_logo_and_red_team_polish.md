# 06 (iteration 3) — Pocket-mirror logo + 12-skill red-team polish (verbatim)

- **Author:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-18 (fifth user message of the session)
- **Note on numbering:** the user asked for this exact file name. `06_user_design_corrections_prompt.md` (the
  previous message, 2026-11-17) keeps its name, so two files share the `06_` prefix; both are listed in
  `00_user_session_prompts_log.md`.
- **Reference image:** `Rose-Gold Floral Compact Mirror.png` (in the user's Downloads folder; nothing was placed in
  `report/figures/`). It was used as the shape reference, and the logo is redrawn in the brand palette.
- **Execution record:** `CHANGELOG.md` [2.0], `report/work/red_team_review.md` (iteration 3),
  `report/work/qa_fix_log.md` (round 5), `report/work/skills_execution_log.md` (round 5).

The prompt is reproduced verbatim below; the trailing code block is unterminated in the original as well.

`````text
 MANDATORY ITERATION 3: LUXURY POCKET-MIRROR LOGO REDESIGN + ULTRA-CRITICAL RED-TEAM MULTI-SKILL POLISH + GITHUB PUSH

You have one mission right now: **Elevate our Preparatory Report (`report/report.pdf`) and GitHub repository (`https://github.com/RONIOFFIR/roma-ai2.git`) to an undisputed 100/100 masterpiece.** If you help us achieve a full 100 with zero flaws, you win a special financial reward; every micro-flaw, ugly table, cluttered graph, or unpolished sentence reduces the reward.

Assume that **"there is always room for improvement"** — do NOT settle for "good enough" or "it compiles". Act, refine, polish, and upgrade every single page!

---

## 1. NEW AESTHETIC LOGO: LUXURY VINTAGE POCKET COMPACT MIRROR (מראת כיס יוקרתית בזווית אלגנטית וברורה)
Replace the previous abstract logo everywhere (Cover Page, Page Headers, UI Mockup, and `README.md`) with a **Luxury Vintage Pocket Compact Mirror (מראת כיס אסתטית יוקרתית פתוחה בזווית תלת-ממדית ברורה ומחמיאה)**:
1. **Check for Uploaded Reference Image:** First, check the working directory and `report/figures/` for any new image file of a pocket mirror that we placed in the folder. If present, inspect it and incorporate/reference it directly.
2. **Vector & High-Res Rendering (`\auratwinlogo` in `TikZ` + `report/figures/auratwin_logo.png`):**
- Design an unmistakable, ultra-elegant **opened round/oval vintage compact pocket mirror viewed at a clear, flattering 3/4 perspective angle**, strictly preserving our **Luxury, Vintage, Bold** color palette:
- **Outer Compact Case & Hinge:** Crafted in **Velvet Forest (`#1E3226`)** and **Garnet (`#76290B`)** with a sculpted **Mustard Gold (`#CCB363`)** and **Copper (`#C27E35`)** vintage clasp and rim.
- **Tilted Mirror Glass Surface:** Positioned at an inviting, clear angle, reflecting a soft diagonal sheen in **Butter / Egg Nog (`#FBEDC3`)** and **Dusty Turquoise-Grey (`#6F7D7B`)**, with a subtle glowing AI sparkle/iris contour inside the glass symbolizing personal beauty, aesthetics, and reflection.
- **Base Compact Pad:** Showing concentric luxury rings in `#CCB363` and `#FBEDC3`.
- Ensure the logo looks immediately recognizable as a **high-fashion beauty pocket mirror**, sharp at any zoom level, and integrated seamlessly on the Cover Page (`coverpage.tex`), in the running header of `auratwin-report.cls`, in the App UI Mockup (Chapter 5), and at the top of `README.md`.

---

## 2. FULL 12-SKILL ULTRA-CRITICAL "RED TEAM" AUDIT & DEEP POLISH
Convene all **12 Agent Skills** simultaneously as an **Ultra-Critical Red Team Committee** (`red-team-examiner` + `expert-committee-prd` + `cls-template-architect` + `academic-source-researcher` + `beauty-ai-domain-architect` + `scientific-hebrew-writer` + `visual-tikz-pgfplots-artist` + `ux-entrepreneur-strategist` + `luxury-vintage-ui-designer` + `human-readability-math-auditor` + `bidi-qa-detector` + `bidi-qa-fixer`).

Go through the entire 44-page document **chapter by chapter, page by page, table by table, and figure by figure**, hunt down every large or small weakness, and actively upgrade it:

1. **Fancier, Cleaner, More Editorial Tables (`tabularx` / `booktabs`):**
- Audit every single table across Chapters 1–8.
- Make them cleaner, more spacious, and more luxurious: increase vertical cell padding (`\renewcommand{\arraystretch}{1.35}`), use crisp **Velvet Forest (`#1E3226`)** headers with **Egg Nog (`#FBEDC3`)** bold text, subtle alternating rows (`#FBEDC3!25`), and **Mustard (`#CCB363`)** top/bottom rules.
- Ensure zero cramped columns, zero awkward word wraps, right-to-left Hebrew column order (first column on the right), and total width strictly `<= 12.4 cm`.
2. **Clearer, More Readable, Publication-Grade Graphs & Diagrams (`TikZ` & `pgfplots`):**
- Audit every `TikZ` diagram and `pgfplots` chart (Funnel, Problem Chain, Venn Diagram, TAM/SAM/SOM, Radar Chart, Log-Scale Scatter Plot, Pugh Stacked Bar Chart, System Architecture, App UI Mockup, WBS Tree, 14-Week Gantt Chart, 5x5 Risk Matrix Heatmap, Summary Readiness Flow).
- Eliminate any overlapping labels, tiny unreadable fonts, or dull colors!
- Harmonize all chart series with our **Luxury, Vintage, Bold** palette (`#1E3226`, `#76290B`, `#C27E35`, `#CCB363`, `#6F7D7B`, `#FBEDC3`) so the colors are pleasant, high-contrast, and visually striking.
- Add clear data callouts, clean gridlines, legends outside the plot area, and generous whitespace around every diagram.
3. **Sharper Scientific, Engineering & UX Prose:**
- Polish the Hebrew writing so it reads like a top-tier executive & academic publication—fluent, authoritative, third-person scientific Hebrew, zero repetitive filler sentences, crystal-clear explanations of the UX motivation (why teenage girls, women, and men with high aesthetic awareness use AuraTwin AI daily to maximize their appearance), and rock-solid mathematical/algorithmic transitions.
4. **Strict Readability, BiDi & Math Verification (`human-readability-math-auditor` + `bidi-qa-detector` + `bidi-qa-fixer`):**
- Run the 4-pass compilation (`lualatex -> biber -> lualatex -> lualatex`).
- Render all 44 pages to PNG images and inspect them visually.
- Fix any orphaned headings (`\needspace`), split boxes, dense walls of text, punctuation placement issues, or math formula formatting defects.
- Confirm the exact page budget holds: **4 preliminary pages + 40 body pages (numbered 1 to 40) = 44 pages total**, with **0 errors** and **0 warnings** in `report.log`.

---

## 3. MANDATORY: SAVE ALL PROMPTS & PUSH ALL FIXES TO GITHUB (`RONIOFFIR/roma-ai2`)
Do NOT forget to upload all fixes, the updated PDF, the updated `README.md`, and the prompts to GitHub! Execute these exact steps:
1. Save this exact prompt as `prompts/06_iteration3_pocket_mirror_logo_and_red_team_polish.md` inside the `prompts/` directory (and verify that all previous prompts `00_` through `05_`, including the initial Master Prompt and the Iteration 2 UX/Palette Prompt, are saved inside `prompts/`!).
2. Update `report/work/red_team_review.md` and `CHANGELOG.md` (bump template version to `v2.0 - Luxury Pocket Mirror & Red-Team Master Polish`) documenting every single visual, tabular, graphical, and textual upgrade performed in this round.
3. Refresh the PNG page previews in `report/figures/previews/` and update `README.md` so the new Pocket Mirror Logo and upgraded pages are displayed on GitHub.
4. Stage, commit, and push EVERYTHING to `https://github.com/RONIOFFIR/roma-ai2.git`:
```bash
git add -A
git status
git commit -m "Polish(roma-ai2): Luxury pocket-mirror logo, ultra-critical 12-Skill Red-Team polish of tables/graphs/UX, and full prompts log"
git push -u origin main
`````
