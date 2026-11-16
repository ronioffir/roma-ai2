# 01 — User "rejects" prompt: UX, Luxury Vintage redesign, 3 new skills, prompts, GitHub (verbatim)

- **Author:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-16 (third user message of the session)
- **Attachment:** "Colour palette inspiration — Luxury, Vintage, Bold" board
  (`Screenshot 2026-11-16 143117.png`), with six arch swatches:
  Egg Nog `#FBEDC3`, Mustard `#CCB363`, Dust `#6F7D7B`, Copper `#C27E35`, Garnet `#76290B`,
  Velvet Forest `#1E3226`.
- **Execution record:** see `report/work/skills_execution_log.md`, `CHANGELOG.md` [1.3.0] and
  `prompts/03_…`–`05_…`.

The prompt is reproduced verbatim below.

````text
# MANDATORY REJECTS, UX & LUXURY VINTAGE REDESIGN, NEW AGENT SKILLS, AND FULL GITHUB PUSH DIRECTIVE

We reviewed your first draft of the Preparatory Report. While the engineering, calculations, and mathematical depth are strong, **we are aiming for a strict 100/100 score**, and several critical elements are missing or require immediate upgrade.

Execute ALL of the following instructions autonomously from start to finish. Do NOT stop until the LaTeX report is recompiled with the new design, all 12 Agent Skills are documented and executed, the `README.md` and `prompts/` folder (including the previous Master Prompt AND this Rejects Prompt!) are updated, and the entire repository is pushed live to `https://github.com/RONIOFFIR/roma-ai2.git`.

---

## 1. VERIFY & EXPAND THE MULTI-AGENT SKILLS ECOSYSTEM (12 SKILLS TOTAL)
First, verify that all 9 original skills exist in `.claude/skills/` AND are mirrored in `skills/`. Then, create **3 NEW specialized Agent Skills** and actually invoke/apply their expertise directly into the report chapters and `.cls` template:

### New Skill 10: `.claude/skills/ux-entrepreneur-strategist/SKILL.md` (יזם ומומחה חוויית משתמש - UX & Product Visionary)
- **Role & Persona:** Serial Beauty-Tech Entrepreneur & Chief UX Strategist.
- **What must be added to the Report (Chapters 1, 2, 4, and 5):**
  1. **The Human & Cultural Need (למה העולם חייב את התוסף הזה עכשיו):** Today, humanity uses AI for every daily task (writing, coding, navigation, shopping). Yet daily appearance, fashion styling, makeup, and nail aesthetics remain stuck in manual guesswork. Explain clearly why there is a **massive, cross-demographic target audience**: teenage girls, women of all ages, and increasingly **men with high aesthetic and grooming awareness** who want to maximize their personal appearance ("למקסם את הופעתם") effortlessly every morning or while shopping online via a simple, frictionless AI browser extension & mobile companion app.
  2. **End-to-End User Experience (UX) & User Journey (מסע המשתמש/ת וחוויית השימוש):** Add a dedicated section and visual diagram/mockup showing the 4-step frictionless UX flow:
     - **Step 1 (Onboarding in 30 Seconds):** Entering baseline traits (eye color, height, weight, body circumferences) + uploading 3 quick snapshots (face, full body, hands/nails).
     - **Step 2 (Instant Daily / Shopping Assistant):** Receiving hyper-personalized outfit, makeup shade, and nail polish recommendations aligned with live TikTok/Pinterest trends and seasonal color theory.
     - **Step 3 (Value-Exchange Ad-Gate / Freemium UX):** A smooth, non-intrusive UX prompt where watching a 15-second rewarded brand video (or holding a VIP subscription) unlocks a photorealistic Generative AI Virtual Try-On image of the user herself/himself wearing the exact recommended look.
     - **Step 4 (1-Click Sponsored Shop-the-Look):** Direct clickable cards to paying retail partners (e.g., a recommended crimson halter top links directly to the matching sponsored Zara item; a lipstick links to Sephora).
  3. **Visual UI Mockup inside the LaTeX Report:** Build a `TikZ` / `tcolorbox` visual wireframe mockup of the **AuraTwin AI App & Browser Extension Interface** inside Chapter 5 so the reader can visually see how sleek, intuitive, and desirable the product looks!

### New Skill 11: `.claude/skills/luxury-vintage-ui-designer/SKILL.md` (מעצב עלית לתוסף ולמסמך - Luxury, Vintage, Bold Palette & Logo Architect)
- **Role & Persona:** Luxury Editorial Art Director & LaTeX `CLS` Visual Designer.
- **Mandatory Color Palette ("Luxury, Vintage, Bold" — Exact Hex Codes from our Brand Inspiration Board):**
  Update `report/base-report.cls`, `report/auratwin-report.cls`, all `tcolorbox` styles, all table headers/row tints, all `TikZ` diagrams, and all `pgfplots` charts to use **ONLY this cohesive, high-fashion luxury vintage palette** (replacing any boring default blue/grey colors):
  - **Egg Nog (חמאה יוקרתית - רקעים רכים של תיבות, כרטיסים ורקע לוגו):** `#FBEDC3` (`RGB: 251, 237, 195`)
  - **Mustard (חרדל-ירקרק וינטג' - הדגשות, מסגרות זהובות-עתיקות וגרפים):** `#CCB363` (`RGB: 204, 179, 99`)
  - **Dust (טורקיז-אפור מעושן - כותרות משנה, תיבות מערכת וצירי גרפים):** `#6F7D7B` (`RGB: 111, 125, 123`)
  - **Copper (נחושת חמה - תיבות דוגמה, הדגשת נתיב/אבני דרך וגרפים):** `#C27E35` (`RGB: 194, 126, 53`)
  - **Garnet (בורדו-גרנט עמוק - תיבות אזהרה/סיכונים קריטיים והדגשות בולטות):** `#76290B` (`RGB: 118, 41, 11`)
  - **Velvet Forest (ירוק יער קטיפתי כהה - צבע ראשי לכותרות פרקים, שער, כותרות טבלאות וטקסט מודגש):** `#1E3226` (`RGB: 30, 50, 38`)
- **Mandatory App Logo & Icon Design:**
  - Design an iconic, high-fashion **App Logo & Icon** for AuraTwin AI (both as a reusable LaTeX `TikZ` macro `\auratwinlogo` on the Cover Page & Page Headers AND as a high-res PNG `report/figures/auratwin_logo.png` for `README.md`).
  - **Exact Logo Specification:** Must combine the **three top palette colors** in interlocking vintage-modern arch/dome geometric shapes (inspired by our palette card):
    1. **Butter / Egg Nog (`#FBEDC3`)** — Top-left curved arch shape.
    2. **Greenish-Mustard (`#CCB363`)** — Top-center inverted U-dome shape.
    3. **Greyish-Turquoise / Dust (`#6F7D7B`)** — Top-right curved arch shape.
    Framed with thin **Velvet Forest (`#1E3226`)** typography and a subtle minimalist silhouette of an eye/prism symbolizing biometric style calibration.
- **Make the Document Visually "Fancy", Editorial & Unforgettable:**
  - Upgrade `auratwin-report.cls` so every chapter opening looks like a luxury tech-fashion journal (using Velvet Forest `#1E3226` headers, Mustard `#CCB363` & Dust `#6F7D7B` decorative rules, Egg Nog `#FBEDC3` soft callout backgrounds, and Copper `#C27E35` / Garnet `#76290B` badges).

### New Skill 12: `.claude/skills/human-readability-math-auditor/SKILL.md` (מומחה קריאות אנושית, פיסוק, ריווח ונוסחאות מתמטיקה)
- **Role & Persona:** Senior Hebrew Scientific Copyeditor, Typesetting Readability Inspector & Mathematical LaTeX Auditor.
- **Mandatory Readability & Math Checks across all 44 pages:**
  1. **Breathing Room & Line Spacing (אווריריות וריווח):** Ensure 1.5 line spacing (`\onehalfspacing`), generous paragraph spacing (`\setlength{\parskip}{6pt}`), and adequate padding inside and around tables and `tcolorbox` environments so NO page ever looks cramped, dense, or overwhelming to a human reader.
  2. **Strict BiDi & Punctuation (עקרונות BiDi ופיסוק תקני):** Verify that all punctuation marks (periods, commas, colons, parentheses, dashes) sit on the correct Hebrew RTL side, no English words or numbers are reversed, no hyphens are glued awkwardly, and all tables flow naturally from right to left.
  3. **100% Mathematical Formula Integrity (תקינות נוסחאות מתמטיקה):** Inspect every single equation (`equation`, `align`, inline `$...$`) across all chapters (CIELAB $\Delta E_{00}$, SMPL-X loss functions, Diffusion objective, RAG cosine similarity, Pugh weighted sum $S_j = \sum w_i c_{ij}$, Risk $R = P \times I$). Ensure every variable is clearly defined in Hebrew immediately below the equation, no raw LaTeX syntax leaks into text, no Hebrew text inside math mode is reversed (use `\hebmath{...}`), and all equations are numbered cleanly on the margin.

Also create `report/work/skills_execution_log.md` documenting how all **12 Skills** were invoked step-by-step and what concrete changes each Skill contributed to the final report.

---

## 2. CRITICAL: SAVE ALL PROMPTS IN `prompts/` (INCLUDING THE PREVIOUS PROMPT!)
Dr. Segal grades the `prompts/` directory in GitHub as a core requirement. You MUST ensure that `prompts/` contains:
1. `prompts/00_initial_master_prompt.md` — **The complete, verbatim Master Prompt we gave you in the previous turn** (40-Page Preparatory Engineering Report directive for AuraTwin AI, group `roma-ai2`, Roni Offir & Maayan Shiri). *Do NOT lose or overwrite this!*
2. `prompts/01_user_rejects_ux_luxury_design_prompt.md` — **This exact second prompt** (adding UX Entrepreneur Skill, Luxury Vintage Bold palette `#FBEDC3`, `#CCB363`, `#6F7D7B`, `#C27E35`, `#76290B`, `#1E3226`, the 3-color App Logo, Readability & Math Auditor Skill, and GitHub synchronization).
3. `prompts/02_committee_prd_and_architecture_prompts.md` — Prompts used by the Expert Committee & Domain Architect skills.
4. `prompts/03_cls_template_and_luxury_styling_prompts.md` — Prompts C0–C5 used to build and upgrade `base-report.cls` and `auratwin-report.cls`.
5. `prompts/04_chapter_writing_and_ux_prompts.md` — Prompts used to author Chapters 1–8 and the UX/User Journey sections.
6. `prompts/05_bidi_readability_and_red_team_prompts.md` — Prompts B1–B4, Detector, Fixer, Readability/Math Auditor, and Red Team Examiner prompts.

---

## 3. RECOMPILE, RENDER PREVIEWS, UPDATE `README.md`, AND PUSH TO GITHUB (`RONIOFFIR/roma-ai2`)
Execute the following terminal actions and verify every single one succeeds:

1. **Recompile the 44-page Report (4-Pass LuaLaTeX + Biber):**
   ```bash
   cd report
   lualatex -interaction=nonstopmode -jobname=report main.tex
   biber report
   lualatex -interaction=nonstopmode -jobname=report main.tex
   lualatex -interaction=nonstopmode -jobname=report main.tex
Verify report/report.pdf exists, has 0 compilation errors, 0 undefined references/citations, and maintains the 4 preliminary pages + 40 body pages = 44 pages structure with spacious, luxury editorial layout.

Render Fresh Visual Screenshots for README.md: Render PNG previews (pdftoppm -png -r 150 or Python pdf2image/pypdfium2) of:

Cover Page (showing the new Luxury Vintage Bold design & 3-color App Logo)

UX & App Interface Mockup Page

Radar & Scatter Plots Page (in the new Luxury Vintage palette)

System Architecture & Data Flow Diagram Page

14-Week Gantt Chart & Risk Matrix Heatmap Page Save them in report/figures/previews/ so they display directly in README.md.

Create/Update a Comprehensive Root README.md: Ensure README.md in the root of the repository is written in rich, professional Hebrew & English and includes:

Embedded AuraTwin AI Logo (report/figures/auratwin_logo.png) and "Luxury, Vintage, Bold" color palette swatches table.

Executive project overview & UX vision (including why women, teenage girls, and men use AuraTwin AI daily).

Embedded visual screenshots of the compiled PDF pages from report/figures/previews/.

Full table of all 12 Agent Skills (.claude/skills/ & skills/) and how the Detector + Fixer + Readability + Red Team loop operated.

Links to PRD.md, prompts/, CHANGELOG.md, and report/report.pdf.

PUSH EVERYTHING TO GITHUB (https://github.com/RONIOFFIR/roma-ai2.git): Previously, the project, README.md, and prompts/ were NOT pushed to GitHub! Fix this immediately:

git init
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/RONIOFFIR/roma-ai2.git
git add -A
git status
git commit -m "Feat(roma-ai2): Full 44-page Luxury Vintage Preparatory Report, 12 Agent Skills (UX, UI Palette, Readability), PRD, Prompts & Visual README"
git push -u origin main --force
After running git push, run git status and git log -n 2 and verify that the push to https://github.com/RONIOFFIR/roma-ai2.git succeeded completely! If authentication or credentials are required by the terminal, prompt us clearly or use the configured gh / git credential helper.
````
