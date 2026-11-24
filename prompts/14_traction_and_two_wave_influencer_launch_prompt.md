# 14 — Prompt 13 re-issued with go-to-market traction and a two-wave influencer launch (verbatim)

- **Authors:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-24
- **Execution record:** `CHANGELOG.md` [3.6]. Everything except the new "Required Go-To-Market Traction &
  Influencer Growth Additions" section was already executed under prompt 13 (`CHANGELOG.md` [3.5]).

`````text
You are working on the **AURAM** preparatory report repository and LuaLaTeX build for group `roma-ai2` (**Roni Offir** and **Maayan Shiri**, Department of Statistics, University of Haifa, advisor **Dr. Yoram Segal**).

### Repository & Git Sync Reminder
- **GitHub Repository:** `https://github.com/RONIOFFIR/roma-ai2.git`
- **Prompt Archiving & Push Requirement:** Save this prompt into the repository (e.g., under `prompts/` or the project's established prompt archive file) alongside all report upgrades, and commit & push everything cleanly to `https://github.com/RONIOFFIR/roma-ai2.git` (`origin main`) once verified.

### Language Requirement (Hebrew-First Preparatory Report)
- **All report content must be in Hebrew**: body prose, section/subsection headings, captions, table headers/cells, callout boxes, visual annotations, go-to-market/growth sections, and the narrative rationale for the pocket-mirror logo.
- Keep technical terms in English only when standard Hebrew usage does not fit cleanly or when referring to code, LuaLaTeX commands/packages, file paths, or identifiers (such as `roma-ai2`, `AURAM`, `Pro`, or Git commit messages/identifiers). Ensure right-to-left (RTL) Hebrew directionality and BiDi formatting are clean and consistent throughout the LuaLaTeX document.

### Mandatory Cover Page & Table Layout Fixes
1. **Cover Page Updates:**
   - **Remove ID Numbers:** Completely remove Roni Offir's and Maayan Shiri's ID numbers (תעודות זהות / ת"ז) from the cover page. Keep names, group (`roma-ai2`), institution/department, and advisor (`ד"ר יורם סגל`) clean and well-balanced.
   - **Update Submission Date:** Set the submission date on the cover page (and any document metadata/headers that display it) to **November 24, 2026** (`24 בנובמבר 2026` / `24.11.2026`, matching the report's Hebrew date format).
2. **Table Layout, Width & Typography Overhaul (No Mid-Word Line Breaks):**
   - Audit **every single table** across the entire document. Currently, several tables are overly narrow or poorly proportioned, causing Hebrew words to wrap/break awkwardly across two lines (`שבירת מילים לשתי שורות`).
   - Widen tables to utilize the available text width properly (`\textwidth` / `tabularx` / properly calibrated `p{...}` or `X` columns), adjust column ratios to match actual content length, increase cell padding (`\arraystretch` and horizontal padding), and apply `\raggedleft` / `\arraybackslash` or `\mbox{}` where needed so **no Hebrew words break mid-word or wrap awkwardly onto two lines**.
   - Make all tables visually crisp, balanced, and editorial, styled harmoniously with our luxury vintage palette.

### Required Go-To-Market Traction & Influencer Growth Additions (in Hebrew)
Integrate these two concrete pillars cleanly into the relevant sections of the preparatory report (e.g., validation/traction, product-market pull, marketing/go-to-market strategy, and unit-economics/budget implications):
1. **Organic Social Proof & High-Intent Demand From Extension Content:**
   - Document in Hebrew that publishing short-form videos about the extension on **TikTok** and **Instagram Reels** generated broad organic traffic—**hundreds of thousands of views**, **thousands of likes**, and **hundreds of comments** asking for the app's name or how to get access.
   - Frame this as a concrete demand signal showing curiosity, pull, and readiness for the main app launch (while keeping claims accurate to what was observed and linking naturally to conversion/onboarding and statistical funnel/uncertainty modeling where relevant).
2. **Two-Tier Influencer Launch & Paid Acceleration Strategy:**
   - **First Wave (Nano/Micro-Creators via Pro Subscription Exchange):** Execute the initial social launch of the app using smaller creators/micro-influencers who receive a **Pro subscription (`מנוי Pro`)** in exchange for publishing content—building authentic grassroots coverage and cost-efficient early social proof.
   - **Second Wave (3 High-Impact Paid Creators From Ad Budget):** Allocate part of the advertising budget to select **3 especially strong, high-reach creators** on a paid basis so AURAM reaches its target audience rapidly at scale, connecting this choice explicitly to budget allocation, reach/conversion dynamics, and unit-economics trade-offs.

### Context & Core Premise
Our grader evaluates submissions comparatively against all other projects. In this context, **creativity is measured by meaningful differentiation from the cohort average**—not gimmicks or fluff, but original choices in framing, statistical rigor, engineering trade-offs, narrative convergence, and visual design that make AURAM unmistakably distinct while remaining accurate, grounded, and defensible.

Review the current repository files, LuaLaTeX sources, data/model assets, and Git history, and upgrade the preparatory report with high-leverage originality across the following six dimensions (writing all report prose and labels in Hebrew):

1. **Statistical Uncertainty as the Hero (Not a Single Point Estimate)**
   - Replace generic single-number claims in Hebrew with explicit uncertainty quantification grounded in our hierarchical Bayesian modeling perspective.
   - Show posterior distributions, sensitivity to optical/operational assumptions, and **Value of Information (VoI)** (מוצג ומוסבר בעברית)—identifying which future measurement or experiment would reduce uncertainty the most rather than hiding model limitations.

2. **Hardware/Optical Constraints vs. Mathematical & Unit-Economics Trade-Offs**
   - Avoid isolated "chapter silos" that read like textbook summaries.
   - Build clear tension and trade-offs between optical physics/hardware limits (weight, heat, component cost, physical boundaries) and the statistical/unit-economics architecture of AURAM. Show explicitly in Hebrew where an engineering constraint forces an adjustment in modeling or unit economics, and how the design resolves that tension.

3. **Documenting Intellectual Evolution & Convergence (Not Just the Final Answer)**
   - Leverage our iterative workflow, red-team critiques, and Git commit history to show *how* assumptions, framing, or structure evolved across iterations—what was challenged, revised, or dropped after stress-testing, and why.
   - Keep this crisp and analytical in Hebrew so it demonstrates scientific maturity and real iteration rather than post-hoc polishing.

4. **The "Transparent Layer" & User/Environmental Perspective**
   - Connect the **AURAM** identity (portmanteau of *Aura* and computer *RAM*) to how the system operates seamlessly in the background in Hebrew: reducing cognitive/manual friction, preserving context/memory intelligently, and preventing early errors rather than merely fixing them after the fact.

5. **Design Creativity & Editorial Differentiation (LuaLaTeX + Luxury Visual Craft + Pocket-Mirror Identity)**
   - Move beyond standard academic PDF templates and generic Hebrew section headings.
   - Apply our visual identity deliberately: the luxury vintage bold color palette (`#FBEDC3`, `#CCB363`, `#6F7D7B`, `#C27E35`, `#76290B`, `#1E3226`) and tri-color Egg Nog / Mustard / Dust logo motif, paired with disciplined whitespace, clean hierarchy, and crisp Hebrew/English BiDi formatting in LuaLaTeX.
   - **Pocket-Mirror Watermark Below Every Page Number:** Include a subtle, refined watermark of our **pocket-mirror logo** positioned cleanly beneath every page number across the report in LuaLaTeX, keeping opacity and scale delicate so it reads as an editorial signature without interfering with legibility or page numbering.
   - **Articulate Why the Pocket Mirror Fits AURAM So Naturally (in Elegant Hebrew):** Dedicate a refined, high-craft Hebrew section or callout explaining the symbolic and aesthetic power of the **pocket mirror**—it is inherently timeless, perpetually reinterpretable across countless silhouettes and finishes while always remaining recognizable, enduring across eras without losing relevance, and serving as a natural emblem of aesthetic discernment, beauty, and intentional sartorial/style choices.
   - Make visual elements **argument-driven**: every figure, table, or callout box should have a clear Hebrew title/caption communicating its core takeaway, avoid visual clutter or repetitive templates, and maintain strict consistency between model terminology, metrics, and graphics.

6. **Comparative Cohort Differentiation Audit ("The 10-Groups Test")**
   - For major sections and claims, check: *What would ten other student teams write here, and what can only AURAM write authentically from its specific choices?* Sharpen any generic Hebrew prose into distinctive, high-signal argument.

### Execution & Workflow
- Work iteratively and cleanly across passes (cover page & table layout overhaul -> content, traction & statistical/economic differentiation in Hebrew -> LuaLaTeX visual & design craft -> Hebrew/English BiDi & editorial polish -> red-team audit).
- Keep all LaTeX files compiling cleanly in LuaLaTeX with proper RTL Hebrew and BiDi directionality, zero overfull/underfull table boxes, and zero broken references.
- Save this prompt in the repository (`https://github.com/RONIOFFIR/roma-ai2.git`) and push all commits cleanly to GitHub.
- Before making sweeping edits, summarize in Hebrew the highest-impact originality, traction, and layout upgrades you plan to apply to each part of the report and ask for confirmation if any structural or scope choices need alignment.
`````
