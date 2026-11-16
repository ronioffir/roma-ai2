# 00 — Initial master prompt (verbatim)

- **Author:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-16 (first user message of the session)
- **Scope:** the 40-page preparatory report directive for AuraTwin AI (skills, PRD, template, chapters, QA, GitHub).
- **Follow-ups:** the 3 booklet file paths (see `00_user_session_prompts_log.md`), then the rejects prompt
  (`01_user_rejects_ux_luxury_design_prompt.md`).

The prompt is reproduced verbatim below.

````text
40-PAGE PREPARATORY ENGINEERING REPORT (LUA-LATEX + MULTI-AGENT SKILLS + FULL QA LOOP + GITHUB SYNC)

You are an elite AI Systems Architect, Academic Research Director, and Master LuaLaTeX Typesetter operating in **Claude Code**.
We have **UNLIMITED TOKENS** and full terminal execution permissions. Do NOT take shortcuts, do NOT write thin summaries, do NOT use placeholder text (`TBD`, `Lorem Ipsum`, `...`), and do NOT stop until every single deliverable is generated, compiled, visually inspected page-by-page, verified with 0 errors, and pushed to our GitHub repository.

Our goal is to achieve a **perfect score of 100/100** in Dr. Yoram Segal's course ("יישומי AI ו-Vibe Coding במדע וביום-יום" / "סמינריון מחקרי בניהול טכנולוגיות", 2026) on the **Preparatory Report (דוח מכין / Preliminary Design Report)**.
Remember: Because we are aiming for a self-evaluation score of **100**, Dr. Segal's automated LLM Red-Team grading system will inspect our work with maximum strictness on every micro-detail. Every requirement below is a hard contract.

---

## 0. PROJECT METADATA, TEAM & GITHUB PARAMETERS
- **Group 8-char ID (`GROUP_ID`):** `roma-ai2`
- **GitHub Repository (PUBLIC):** `https://github.com/RONIOFFIR/roma-ai2.git` (User: `RONIOFFIR`, Repo: `roma-ai2`)
- **Student 1:** רוני אופיר (Roni Offir) — החוג לסטטיסטיקה, אוניברסיטת חיפה (ב-GitHub הציבורי הסווה ת"ז כ-`000000000` מטעמי פרטיות לפי הנחיות החוברת בעמ' 6 ו-75)
- **Student 2:** מעיין שירי (Maayan Shiri) — החוג לסטטיסטיקה, אוניברסיטת חיפה (ב-GitHub הציבורי הסווה ת"ז כ-`000000000`)
- **Academic Advisor:** ד"ר יורם סגל (Dr. Yoram Segal)
- **Industrial / Domain Partner (Simulated for Report):** מעבדת החדשנות של L'Oréal-ModiFace & Zara Inditex Tech Lab
- **Project Hebrew Title:** מערכת הפעלה רב-מודאלית מבוססת סוכני בינה מלאכותית להתאמה ביומטרית של אופנה וביוטי, כריית טרנדים חברתית והדמיה וירטואלית מותנית-מודל-עסקי
- **Project English Title:** AuraTwin AI: Multi-Modal Agentic Operating System for Self-Calibrated Biometric Beauty & Fashion Styling, Social Trend Mining, and Ad-Gated Generative Virtual Try-On
- **IMPORTANT EXCLUSION:** Do **NOT** generate the separate Word-template Moodle submission reporting file (`roma-ai2-exyy.pdf`). The students (Roni and Maayan) will fill out the Word template and export that submission form PDF themselves! Your sole PDF focus is compiling the **40-page Preparatory Report (`report/report.pdf`, 44 pages total with the 4 preliminary pages)** via LuaLaTeX.

---

## 1. STEP 1: INGEST THE INSTRUCTOR'S BOOKLETS (GROUND TRUTH)
Before writing a single line of report code, check the current working directory for the instructor's course booklets (PDFs such as `קובץ 1 לגמיני.pdf` / `קובץ 2 להעלות לגמיני.pdf` / `קובץ 3 להעלות.pdf` or any `.pdf` files in the folder).
If they are present in the directory, use Python (`pypdf`/`pdfplumber`) to inspect them and confirm you have internalized Dr. Yoram Segal's exact methodology from:
1. **"מהבעיה אל ה-PDF: המדריך לדוח המכין המקצועי" (From Problem to PDF: The Professional Preparatory Report)**
2. **"שיעור 3: מסמך PDF מקצועי בלטך – מתארים במילים, המודל כותב, אתם חותמים (L03)"**

Specifically, enforce every single rule from Dr. Segal's booklets:
- **Philosophical premise:** We are NOT actually building the mobile production app today; we ARE imagining and engineering the Preparatory Report (הדוח המכין) as a binding engineering & research contract (חוזה הנדסי ומחקרי בין המרצה לסטודנטיות) before development resources are spent. Think HUGE ("להמציא את גוגל של עולם הביוטי והאופנה"), look far ahead technologically, and combine deep statistical/algorithmic rigor with personal creative interpretation.
- **Exact Page Map (מפת העמודים - Table 1.1):**
  - **Preliminary Pages (חלקים מקדמיים): 4 pages** numbered separately in Hebrew letters (`א'–ד'`) or Roman numerals (`i–iv`), where the Cover Page has NO visible page number:
    1. Cover page (עמוד השער - ללא מספר עמוד גלוי, מסגרת כפולה, תמונת שער מקצועית, כותרת בעברית ובאנגלית בלי סיסמאות שיווקיות ובלי ראשי תיבות לא מוכרים, הגדרת המסמך כדוח מכין, פרטי צוות: רוני אופיר ומעיין שירי — החוג לסטטיסטיקה, אוניברסיטת חיפה, מנחה: ד"ר יורם סגל, תאריך, זכויות יוצרים `©`).
    2. Executive Summary + Keywords (תקציר מנהלים כחטיבה רציפה של 250–350 מילים + 5–7 מילות מפתח טכניות מתחתיו — *נכתב אחרון!*).
    3. Table of Contents (תוכן עניינים אוטומטי עד רמה 3).
    4. Lists & Abbreviations (רשימת איורים, רשימת טבלאות, וטבלת קיצורים ומונחים אלפביתית מלאה).
  - **Main Report Body (גוף הדוח): Exactly 40 pages (numbered 1 to 40)** distributed strictly according to Dr. Segal's Page Budget:
    - **Chapter 1: מבוא ורקע (Pages 1–3, Scope: 3 pages)** — Built as a funnel (משפך, איור 3.1): Macro technological/regulatory/performance trends -> Applied context (הארגון המארח/המעבדה) -> Engineering & economic motivation -> Report structure paragraph. No generic cliché openings like "הבינה המלאכותית משנה את העולם" without immediate quantitative grounding and citation!
    - **Chapter 2: הגדרת הבעיה, שאלת המחקר והיעדים (Pages 4–7, Scope: 4 pages)** — Quantitative problem formulation (המצב המצוי מול הרצוי במספרים חד-משמעיים, בלי קביעות עמומות ובלי להזכיר את הפתרון בהגדרת הבעיה), Research Question & Hypothesis vs. SMART Engineering Design Goals (Table 4.1 comparison), and a complete Engineering Requirements Specification Table (מפרט דרישות הנדסי - הטבלה המחייבת: מזהה `REQ-xxx-01`, הדרישה, סיווג תפקודית/אילוץ/ביצועים/אבטחה, ערך יעד כמותי ביחידות SI/סטטיסטיות, ושיטת אימות ובדיקה).
    - **Chapter 3: סקירת הספרות ומאמר הדגל (Pages 8–16, Scope: 9 pages)** — Thematic and critical review (NOT chronological paper-by-paper summaries!) divided into knowledge domains based on at least 15–20 real, verified peer-reviewed papers from IEEE, ACM, CVPR, ICCV, NeurIPS, ScienceDirect, Springer (last 5 years). Must include:
      - Literature Synthesis Matrix (מטריצת ספרות - Table 5.1: rows = papers, columns = core technological themes, empty cells = the gap, final row = "הפרויקט המוצע (AuraTwin AI) — זה הפער").
      - Flagship Paper Selection & Venn Diagram (בחירת מאמר הדגל - איור 5.1: חיתוך של במה שפיטה בדירוג גבוה, קרבה ישירה לבעיה, וחזרתיות/Replicability).
      - Deep Mathematical & Algorithmic Breakdown of the Flagship Paper (משוואות שולטות, סביבת הניסוי, מגבלות של הנחות תאורה/משאבים) leading directly to a sharp 1-sentence **Research/Engineering Gap (פער הידע)**.
    - **Chapter 4: חקר השוק והמוצרים הקיימים (Pages 17–22, Scope: 6 pages)** — Market sizing in 3 concentric layers (`TAM / SAM / SOM` + `CAGR` from verified analyst reports, illustrated with Figure 6.1) + Technical (non-marketing!) review of 4–5 commercial competitors alongside the Flagship Paper and our Proposed Solution in a Multi-Parametric Comparison Table (Table 6.1) + **Two mandatory data-driven `pgfplots` graphs**:
      1. Radar Chart (תרשים רדאר - פרופיל ביצועים על 6 צירים, איור 6.2).
      2. Scatter Plot (גרף פיזור - ביצועים/זמן תגובה מול עלות בסקאלה לוגריתמית ששובר את הטרייד-אוף המסורתי, איור 6.3).
    - **Chapter 5: חלופות תכן, בחירת פתרון וחדשנות (Pages 23–30, Scope: 8 pages)** — Systematic Engineering Design Process:
      - Stage 1: Presentation of 3 fundamentally different architectural alternatives (Table 7.1: חלופה, היתרון, המחיר/החיסרון) with detailed technical analysis of each.
      - Stage 2: Weighted Decision Matrix / Pugh Trade-off Study (מטריצת החלטה משוקללת - משוואה 7.1: $S_j = \sum_{i=1}^n w_i \cdot c_{ij}$ where $\sum w_i = 1.0$, scores 1–5, Table 7.2 showing raw score and weighted score in parentheses) + Sensitivity Analysis proving the decision isn't rigged backwards ("מטריצה שנכתבה אחורה" check) + Stacked Horizontal Bar Chart (`pgfplots`, איור 7.1).
      - Stage 3: Full System Architecture & Data Flow Diagram (`TikZ`, איור 7.2) detailing every module, API, calibration pipeline, RAG engine, Diffusion Try-On, and Ad-Gate/Affiliate router.
      - Stage 4: Explicit Innovation & Added Value justification (החדשנות והערך המוסף).
    - **Chapter 6: תוכנית עבודה: WBS, תפקידים ולוחות זמנים (Pages 31–34, Scope: 4 pages)** —
      - Work Breakdown Structure (`WBS` hierarchy diagram in `TikZ` איור 8.1 + Table 8.1 detailing 5 Work Packages `WP 1.0`–`WP 5.0`, sub-tasks, and concrete deliverables).
      - Responsibility Assignment Matrix (`RACI` - Table 8.2: `R` Responsible, `A` Accountable, `C` Consulted, `I` Informed across **רוני אופיר**, **מעיין שירי**, and **ד"ר יורם סגל (מנחה)**, ensuring single ownership `R` per sub-task).
      - 14-Week Implementation Schedule & Gantt Chart (`TikZ`/`pgfplots` איור 8.2 + Table 8.3 with tasks `TSK-1.1` to `TSK-5.2`, durations, dependencies, **Critical Path highlighted in red**, two major **Milestones in green** at Week 8 and Week 12, and 1-week reserve buffers before milestones).
    - **Chapter 7: ניתוח סיכונים ותוכנית הפחתה (Pages 35–36, Scope: 2 pages)** — Double quantification ($R = P \times I$, equation 9.1, where $P \in [1,5]$ and $I \in [1,5]$), 5x5 Risk Matrix Heatmap (`TikZ`, איור 9.1 highlighting critical risks $R \ge 12$ in red), Table 9.1 (זיהוי הסיכונים וכימותם across technical, algorithmic, data/privacy, operational, and business domains), and Table 9.2 (פעולות מנע Mitigation, תוכניות מגירה Contingency Plan, וציון שיורי $R_{\text{residual}}$ for every risk with $R \ge 12$).
    - **Chapter 8: פרק הסיכום: מוכנים לשלב המימוש (Page 37, Scope: 1 page)** — Design Readiness summary synthesizing the problem, scientific proof, techno-economic viability, selected architecture, and a `TikZ` diagram of the 3 immediate post-approval actions (איור 10.1: הקפאת תצורה והרשאות דאטה -> הקמת סביבת Git ו-CI/CD ב-`roma-ai2` -> פגישת התנעה לסמסטר ב').
    - **מקורות (References) (Pages 38–40, Scope: 3 pages)** — Managed automatically via `biblatex` + `biber` in strict `IEEE` format (`references.bib`), with 100% bi-directional consistency (every source in `references.bib` is cited via `\cite{}` in the text, and every `\cite{}` resolves cleanly without warnings).

---

## 2. STEP 2: CREATE THE AGENT SKILLS ECOSYSTEM (`.claude/skills/` AND `skills/`)
Dr. Segal explicitly requires building specialized agents as **Skills** (`SKILL.md` files) and using a **Preparatory Report Expert Committee** to define the criteria/PRD first, followed by specialized domain agents, and finally a strict two-agent QA loop (**Detector** and **Fixer** — "השוטר שכותב והשוטר שבודק", never mixing detection and fixing in the same skill!).

Create the directory `.claude/skills/` (and mirror it in `skills/` so it is clearly visible in GitHub) containing the following 9 professional `SKILL.md` files (each with proper YAML frontmatter `name` and `description` and comprehensive instructions):

1. `.claude/skills/expert-committee-prd/SKILL.md` — **וועדת מומחים לדוחות מכינים (Preparatory Report Expert Committee):**
   - Composed of 4 virtual personas: (a) Academic Seminar Chair (Dr. Yoram Segal's methodology enforcer), (b) Chief AI & Computer Vision Scientist (calibrating colorimetry, 3D mesh, Diffusion Try-On, and RAG), (c) Beauty-Tech Venture Architect (TAM/SAM/SOM, Ad-Gated unit economics, Zara/Sephora affiliate routing), and (d) Chief Systems Engineer (IEEE 29148 requirements, Pugh matrix, WBS/RACI/Gantt, ISO 31000 risk management).
   - **Task:** First produces the comprehensive `PRD.md` (Product Requirements Document & Grading Rubric for the 40-page Preparatory Report) before any LaTeX code is written.
2. `.claude/skills/cls-template-architect/SKILL.md` — **אדריכל תבנית הלטך ושכבת החברה (`base-report.cls` + `auratwin-report.cls`):**
   - Builds the two-layer LaTeX class architecture per Chapter 15 of the booklet (Base template handling LuaLaTeX + `polyglossia` + `luabidi` + Hebrew/English fonts + tables + 4 box types + automated headers/footers + `\needspace`; and Thin Company Layer setting AuraTwin AI brand palette, logo, document fields, and `PROMPT.md` documentation, plus `VERSION` and `CHANGELOG.md`).
3. `.claude/skills/academic-source-researcher/SKILL.md` — **חוקר מקורות ומאמרים שפיטים (Real Academic Source Researcher):**
   - Curates 20+ real, verifiable peer-reviewed papers (CVPR, ICCV, IEEE TPAMI, ACM TOG, NeurIPS, Springer, Management Review, ISO, PMBOK) on color constancy, 3D human body reconstruction (`SMPL-X`), virtual try-on diffusion models (`TryOnDiffusion`, `IDM-VTON`, `ControlNet`), fashion recommendation systems, and multimodal RAG. Verifies real DOIs/authors/years and builds `references.bib` + the Literature Matrix.
4. `.claude/skills/beauty-ai-domain-architect/SKILL.md` — **אדריכל המערכת והאלגוריתמיקה של AuraTwin AI:**
   - Formulates the mathematical equations (CIELAB $\Delta E_{00}$ color calibration using human-reported eye color as a spectral prior, SMPL-X anthropometric ratio vector, social trend velocity scoring, Pugh matrix equations, and Ad-Gate/Affiliate unit economics).
5. `.claude/skills/scientific-hebrew-writer/SKILL.md` — **כותב מדעי-הנדסי בעברית (Scientific Third-Person Writer):**
   - Writes rich, rigorous Hebrew prose in third person only (גוף שלישי בלבד, בנימה מקצועית, שקולה ומבוססת עובדות - Table 11.2), introducing every English technical term in parentheses on first mention, and adhering strictly to the page budget per chapter.
6. `.claude/skills/visual-tikz-pgfplots-artist/SKILL.md` — **מאייר ומומחה גרפיקה וקטורית (`TikZ`, `pgfplots`, `HyperFrames`):**
   - Builds all diagrams, system architectures, radar charts, log-scale scatter plots, stacked bar charts, WBS trees, 14-week Gantt charts, and 5x5 Risk Matrices wrapped safely in `\begin{english}...\end{english}` with Hebrew labels inside `\texthebrew{}` and widths strictly $\le 12.4\text{ cm}$ so nothing ever overflows margins. Also generates HTML/CSS visual cards rendered to high-res PNGs (`HyperFrames` style) for the cover page and README showcase.
7. `.claude/skills/bidi-qa-detector/SKILL.md` — **סוכן ביקורת איכות וזיהוי תקלות (QA Detector - "השוטר שבודק"):**
   - **STRICT DETECTOR ONLY — NEVER EDITS FILES!**
   - Runs automated Python + Visual inspection across all 9 QA families (Table 19.1: תבנית, דף שער, כיווניות BiDi, טבלאות, תמונות, קוד, עימוד, מקורות, מבנה קבצים) and checks the 4 visual clues (אות סופית בתחילת מילה `ךםןףץ`, מספר שנראה חשוד `0.1` במקום `1.0`, משהו שנוגע בקצה העמוד `Overfull \hbox`, שורה עם רווח גדול באמצע, כותרת יתומה בתחתית עמוד, תיבה חתוכה). Outputs a structured `report/work/qa_audit_report.md` listing exact page numbers, line numbers, and whether each issue is a **template-level repeating issue** or a **one-off text issue**.
8. `.claude/skills/bidi-qa-fixer/SKILL.md` — **סוכן תיקון תבנית וטקסט (QA Fixer - "השוטר שמתקן"):**
   - Reads `report/work/qa_audit_report.md` from the Detector. Applies Dr. Segal's Iron Rule of Fixing (איור 14.3 ופרק 15.6): **If a bug repeats across the document, fix it ONCE in the `.cls` template and bump the template version in `CHANGELOG.md`; if it is a one-off issue, fix it in the specific `chapters/chX.tex` file.** Never reverse Hebrew letters manually! Always re-run the 4-pass compilation (`lualatex -> biber -> lualatex -> lualatex`) after fixing.
9. `.claude/skills/red-team-examiner/SKILL.md` — **הצוות האדום (Strict Engineering Committee Red-Team Examiner):**
   - Simulates Dr. Yoram Segal's 100-score LLM grading engine. Audits the compiled 44-page PDF for the 10 weakest scientific, quantitative, or methodological points (Prompt 9 in booklet), logs them in `report/work/red_team_review.md`, and triggers an upgrade pass so all 10 points are fortified before final sign-off.

---

## 3. STEP 3: REPOSITORY STRUCTURE & COMPLETE PROMPT LOGGING (`prompts/`)
Dr. Segal places massive weight on documenting the engineering conversation and prompts in a dedicated folder in GitHub ("חובה לכלול ב-GitHub תיקייה ייעודית שתכיל את קובצי הפרומפטים שבאמצעותם הנחיתם את ה-LLM לבניית הפרויקט").
Build the following clean, modular project tree and **ensure every prompt we write to you (including this master prompt and any follow-up user prompts in our session) plus all sub-agent prompts are saved and pushed inside `prompts/`**:

```text
├── README.md                          # Professional visual README in Hebrew/English with embedded screenshots, architecture & badges
├── PRD.md                             # Comprehensive Product Requirements Document authored by the Expert Committee
├── CHANGELOG.md                       # Template & project version history
├── .claude/
│   └── skills/                        # All 9 Agent Skills (SKILL.md files)
├── skills/                            # Mirror of .claude/skills/ for immediate GitHub visibility
├── prompts/                           # Dedicated folder documenting ALL user & engineering prompts
│   ├── 00_user_session_prompts_log.md # Verbatim log of all prompts written by Roni & Maayan to Claude Code
│   ├── 01_committee_prd_prompt.md     # Prompt & instructions for the Preparatory Report Expert Committee
│   ├── 02_template_cls_prompts_C0_to_C5.md # Prompts C0-C5 for two-layer CLS template creation
│   ├── 03_chapter_writing_prompts_1_to_8.md # Prompts 1-6 for outlines, real sources, chapters & graphics
│   ├── 04_bidi_and_qa_prompts_B1_to_B4.md # Prompts B1-B4 & 7-8 for BiDi rules, Detector & Fixer loops
│   └── 05_red_team_audit_prompt.md    # Prompt 9 (Red Team strict examiner) & resolution log
├── scripts/                           # Python scripts for data simulation, visual QA rendering, and BiDi auditing
│   ├── generate_beauty_benchmarks.py  # Generates empirical benchmark data for Ch. 4 & Ch. 5 plots
│   ├── render_hyperframes_cover.py    # Renders cover illustration & README visuals
│   └── qa_detector_audit.py           # Automated text + log + PDF page-image detector script
└── report/                            # The modular LuaLaTeX Preparatory Report project
    ├── base-report.cls                # Base Hebrew/English LuaLaTeX class (v1.2)
    ├── auratwin-report.cls            # Thin company layer on top of base-report.cls
    ├── PROMPT.md                      # Self-documenting template manual & command reference (Table 15.3)
    ├── COMMANDS.md                    # Complete list of template commands & macros
    ├── main.tex                       # Master file (\documentclass{auratwin-report} + \input chapters)
    ├── coverpage.tex                  # Cover page & preliminary pages (א'–ד' / i–iv)
    ├── references.bib                 # 20+ verified BibTeX entries (IEEE style)
    ├── chapters/
    │   ├── ch1_intro.tex              # Chapter 1: מבוא ורקע (Pages 1–3, 3 pages)
    │   ├── ch2_problem.tex            # Chapter 2: הגדרת הבעיה, שאלת המחקר והיעדים (Pages 4–7, 4 pages)
    │   ├── ch3_literature.tex         # Chapter 3: סקירת הספרות ומאמר הדגל (Pages 8–16, 9 pages)
    │   ├── ch4_market.tex             # Chapter 4: חקר השוק והמוצרים הקיימים (Pages 17–22, 6 pages)
    │   ├── ch5_alternatives.tex       # Chapter 5: חלופות תכן, בחירת פתרון וחדשנות (Pages 23–30, 8 pages)
    │   ├── ch6_workplan.tex           # Chapter 6: תוכנית עבודה: WBS, תפקידים ולוחות זמנים (Pages 31–34, 4 pages)
    │   ├── ch7_risks.tex              # Chapter 7: ניתוח סיכונים ותוכנית הפחתה (Pages 35–36, 2 pages)
    │   └── ch8_summary.tex            # Chapter 8: פרק הסיכום: מוכנים לשלב המימוש (Page 37, 1 page)
    ├── figures/                       # Generated high-res assets & page previews for README
    ├── work/                          # Drafts, QA detector reports, Red Team critiques
    └── report.pdf                     # Final compiled 44-page Preparatory Report PDF (4 prelim + 40 body)

4. STEP 4: STRICT BiDi, TYPOGRAPHY & LATEX TEMPLATE RULES (CHAPTERS 11, 14, 15, 16)
Implement base-report.cls and auratwin-report.cls in stages (Table 15.2) and test them on a 1-page stress test (Prompt B4) before compiling the full 40-page body:

Compiler & Fonts: Use LuaLaTeX + polyglossia (\setdefaultlanguage{hebrew}, \setotherlanguage{english}) + fontspec. Use clean, installed Hebrew/English fonts (check fc-list :lang=he first so there are zero missing font or missing glyph warnings, and ensure the © symbol is always rendered via the English font \en{\copyright}).

Margins & Spacing (Table 11.1): 11pt or 12pt font, 1.5 line spacing (\onehalfspacing), justified text (Justified), 2.5 cm margins on all sides + 0.5 cm binding gutter (geometry package).

BiDi Protection Macros (Prompt B1 - Mandatory everywhere including titles, captions, tables, headers, footers, TOC):

\en{...} — Wraps every English word, acronym (AI, LLM, RAG, CIELAB, SMPL-X, GAN, VTON, API, GPU, SDK, CPA, CPC, TAM, SAM, SOM, CAGR, WBS, RACI), and multi-word English phrase as a single LTR unit. Never put Hebrew inside \en{}.

\num{...} — Wraps every number, decimal (1.0, 0.25, 39.5), range (10--20, 250--350), percentage (85\%), currency (\$180, \$2,200), and unit (35 ms, 1.8 W, 0.8 mm) as a single unbreakable LTR unit so 1.0 never becomes 0.1, 10-20 never becomes 02-01, and 1,500 never splits into 500,1.

\hebmath{...} — Safely embeds Hebrew words inside math equations (\text{\texthebrew{...}}).

Styled Boxes (tcolorbox - 4 distinct types that never split across pages breakable=false + \needspace):

managerbox ("למה זה חשוב למנהל" — Gold/Amber header, executive takeaway at the start of every chapter).

keymessagebox ("המסר המרכזי / חידוש הפרויקט" — Teal accent bar on the right).

warningbox ("מלכודת הנדסית / אזהרה" — Red/Coral accent).

examplebox ("יישום במערכת AuraTwin AI" — Royal Blue/Indigo accent).

Styled Tables (tabularx / booktabs / colortbl):

In Hebrew RTL tables, the first column is on the right (העמודה הראשונה מימין, בלי להפוך ידנית).

Colored header row, alternating subtle row tint, total width strictly $\le 12.4\text{ cm}$ so no table ever causes an Overfull \hbox.

Table caption ABOVE the table; Figure caption BELOW the figure (Table 11.1).

Iron Rule of Figures & Tables (סעיף 11.1): Every single figure and table MUST be explicitly referenced in the body text (איור~\ref{...}, טבלה~\ref{...}) accompanied by an analytical sentence explaining what we learn from it!

Diagrams & Plots (TikZ & pgfplots):

Wrap every tikzpicture in \begin{english} ... \end{english} so coordinates and axes never mirror or break, and wrap Hebrew node labels in \texthebrew{...}.

Keep every diagram width $\le 12.4\text{ cm}$ (max width=12.4cm).

Pagination & Layout Discipline (סעיף 19.4):

TOC, Executive Summary, each Chapter (\chapter), and Bibliography start on a new page (\clearpage).

Use \needspace{6\baselineskip} before every \section and \subsection so no heading is ever orphaned in the bottom quarter of a page.

No nearly-empty pages; pace content and visual elements so the main body lands on exactly pages 1 to 40 (and total PDF is 44 pages including the 4 preliminary pages).

5. STEP 5: DETAILED CHAPTER-BY-CHAPTER CONTENT BLUEPRINT FOR AURATWIN AI
Write deeply researched, quantitative, engineering-grade content in each chapter file:

coverpage.tex (Pages א'–ד', 4 pages):

Page א' (Cover Page, \thispagestyle{empty}): Double border frame, custom high-res graphic (figures/cover_banner.png), University/Faculty header, Hebrew & English descriptive titles, "דוח מכין (Preliminary Design Report) — קוד קבוצה: roma-ai2", Team metadata block (רוני אופיר ומעיין שירי — החוג לסטטיסטיקה, אוניברסיטת חיפה), Advisor (ד"ר יורם סגל), Date, and Copyright footer (\en{\copyright} 2026).

Page ב' (Executive Summary & Keywords): 250–350 word continuous synthesis of the beauty e-commerce return & mismatch crisis, the AuraTwin AI architecture, quantitative targets, Pugh selection, 14-week plan, and 7 technical keywords (Preliminary Design Report; Multi-Modal Biometric Calibration; CIELAB Color Constancy; 3D Anthropometric Mesh; Generative Virtual Try-On; Social Trend RAG; Ad-Gated Unit Economics).

Page ג' (Table of Contents): \tableofcontents up to depth 3.

Page ד' (Lists of Figures, Tables & Abbreviations): \listoffigures, \listoftables, and a comprehensive alphabetical Acronyms & Terminology Table.

chapters/ch1_intro.tex (Pages 1–3, 3 pages):

Funnel diagram (TikZ איור 1.1).

Global macro trends in AI-driven Beauty & Fashion e-commerce, high return rates in online apparel (30%–40% due to size/fit mismatch) and cosmetics (over 52% shade mismatch in foundations/lipsticks due to uncalibrated mobile camera lighting).

Applied context: Collaboration model between an academic Data & Decision Sciences / Statistics lab and a global retail partner (Zara / Sephora / L'Oréal style catalog integration).

Engineering & economic motivation: Why static size charts, quiz-based filters, and simple AR overlays fail.

Report structure roadmap.

chapters/ch2_problem.tex (Pages 4–7, 4 pages):

Problem-to-Specification chain diagram (TikZ איור 2.1).

Quantitative Problem Statement: Smartphone cameras under uncontrolled indoor illumination introduce color distortion of $\Delta E_{00} > 12.5$ in skin/hair/eye estimation (where human perception threshold is $\Delta E_{00} < 2.0$), while 2D photos without anthropometric scaling yield $\pm 4.8\text{ cm}$ circumference error, and cloud Diffusion Virtual Try-On costs $\$0.045$–$\$0.090$ per image generation—making free unlimited generation economically unsustainable without an Ad-Gated/Affiliate monetization architecture.

Table 2.1 comparing Research Project vs. System Engineering Design aspects in AuraTwin AI (Research question on self-supervised eye-color anchor calibration vs. SMART system targets).

Table 2.2: Full Engineering Requirements Specification (REQ-VIS-01 through REQ-BIZ-12) covering Colorimetric Calibration ($\Delta E_{00} \le 1.8$), 3D Body Circumference Estimation ($\text{MAE} \le 1.2\text{ cm}$), Nail & Hand Segmentation ($\text{IoU} \ge 0.94$), End-to-End Recommendation Latency ($\le 1.8\text{ s}$), Generative VTON Latency ($\le 4.5\text{ s}$), Identity Preservation (ArcFace Cosine Similarity $\ge 0.88$), Social Trend RAG Freshness ($\le 6\text{ hours}$), Sponsored SKU Match Precision@5 ($\ge 0.85$), Ad-Gate Conversion & Unit Margin ($\text{ARPU} > 2.4 \times \text{GPU Cost}$), and GDPR/Biometric Privacy compliance.

chapters/ch3_literature.tex (Pages 8–16, 9 pages):

Thematic & critical review across 4 scientific pillars:

Illumination-Invariant Color Constancy & Biometric Anchors (using human-verified iris/sclera priors to invert unknown lighting matrices in CIELAB space).

3D Anthropometric Body & Hand Mesh Reconstruction from Monocular Images + Sparse Tabular Priors (SMPL-X, HMR 2.0, FrankMocap).

Identity-Preserving Diffusion Virtual Try-On for Apparel, Makeup & Nail Art (TryOnDiffusion, IDM-VTON, StableVITON, ControlNet).

Multi-Modal Retrieval-Augmented Generation (MM-RAG) & Social Media Trend Mining (extracting embeddings from TikTok/Pinterest creator frames and matching them with pre-loaded seasonal color/body-type knowledge graphs).

Table 3.1: Comprehensive Literature Synthesis Matrix comparing 15+ peer-reviewed papers across 6 technological criteria, visually exposing the empty cells and our project's row ("הפרויקט המוצע: AuraTwin AI — זה הפער").

Figure 3.1 (TikZ Venn Diagram): Selection of the Flagship Paper (Zhu et al., "TryOnDiffusion: A Tale of Two UNets", CVPR 2023 or Choi et al., "IDM-VTON", ECCV 2024) and mathematical breakdown of its diffusion/warping equations, computational bottlenecks ($>8\text{ s}$ on A100 GPU, lack of colorimetric calibration under wild lighting, and lack of biometric-tabular fusion), culminating in the 1-sentence Research & Engineering Gap.

chapters/ch4_market.tex (Pages 17–22, 6 pages):

Market Sizing in 3 layers (TAM / SAM / SOM with TikZ concentric diagram איור 4.1): Global AI in Beauty & Fashion market (TAM $\approx \$18.4\text{B}$ by 2028, CAGR $28.4\%$), Mobile Virtual Try-On & Personalized Styling SaaS/Affiliate segment (SAM $\approx \$3.2\text{B}$), and initial 3-year target market in Israel & European tier-1 fashion/beauty retailers (SOM $\approx \$42\text{M}$).

Technical (non-marketing!) architectural teardown of 4 real competitors + manual baseline: (1) ModiFace (L'Oréal) (AR facial mesh, weak full-body & clothing integration), (2) Perfect Corp (YouCam Makeup) (strong AR filters, lacks generative clothing diffusion & anthropometric circumference fusion), (3) Zeekit / Walmart Virtual Try-On (apparel mapping, lacks eye/undertone colorimetry & nail/makeup synergy), (4) Stitch Fix Algorithms (tabular + human stylist, high operational latency & cost, no instant self-try-on), plus the Flagship Paper and AuraTwin AI.

Table 4.1: Multi-Parametric Technical Comparison Table across 8 engineering metrics.

Figure 4.2 (pgfplots Radar Chart across 6 normalized axes: דיוק כיול צבע, דיוק התאמת גזרה תלת-ממדית, פוטו-ריאליזם גנרטיבי, מהירות תגובה, כיסוי רב-קטגוריאלי, ורווחיות ליחידת חישוב).

Figure 4.3 (pgfplots Log-Scale Scatter Plot: End-to-End Inference Cost/Latency vs. Personalization Accuracy, demonstrating how AuraTwin AI breaks the traditional trade-off).

chapters/ch5_alternatives.tex (Pages 23–30, 8 pages):

Engineering Design Process comparing 3 distinct system architectures (Table 5.1):

Alternative 1: On-Device Edge AI Architecture (CoreML / MediaPipe / Quantized TinyDiffusion) — Zero cloud GPU cost and maximum privacy, but severe thermal throttling, mobile RAM limits ($<4\text{ GB}$), and poor photorealism in complex fabric draping.

Alternative 2: Monolithic Heavy Cloud Multimodal LLM + Unconditional Diffusion (GPT-4o Vision API + Cloud SDXL/Flux Pipeline) — Fast time-to-market and rich reasoning, but high token/GPU cost ($\$0.12$/session), high latency ($>9\text{ s}$), and poor deterministic control over exact Zara/Sephora SKU geometry.

Alternative 3 (Selected): Hybrid Split-Compute & Agentic RAG Architecture (Edge Biometric Calibration + Deterministic Style/Social RAG + Ad-Gated Cloud Latent Diffusion VTON) — Lightweight client-side iris/skin calibration & 3D keypoint extraction paired with instant server-side vector RAG for recommendations and affiliate links ($<1.2\text{ s}$, $\$0.002$/query), while gating the heavy GPU Diffusion Try-On behind a Rewarded Ad / Premium trigger that fully funds the compute cost!

Weighted Decision Matrix (Table 5.2) with explicit mathematical formulation ($S_j = \sum w_i c_{ij}$, $\sum w_i = 1.00$), sensitivity analysis testing weight perturbations (proving Alternative 3 wins robustly with $4.45$ vs. $3.15$ and $2.85$), and pgfplots Stacked Horizontal Bar Chart (איור 5.1).

Full System Architecture & Data Flow Diagram (TikZ איור 5.2) + Algorithmic & Business Innovation section.

chapters/ch6_workplan.tex (Pages 31–34, 4 pages):

Figure 6.1 (TikZ WBS Tree) + Table 6.1 detailing 5 Work Packages (WP 1.0 איסוף נתונים וכיול ביומטרי, WP 2.0 גרף ידע ומנוע כריית טרנדים מרשתות חברתיות, WP 3.0 מנוע דיפוזיה להדמיה וירטואלית וניתוב שותפים, WP 4.0 אינטגרציה, סימולציה ובדיקות עומסים, WP 5.0 תיעוד, פיילוט משתמשות והגנה).

Table 6.2: RACI Matrix assigning clear single R ownership per sub-task between רוני אופיר and מעיין שירי, with ד"ר יורם סגל as A (Accountable).

Figure 6.2 (TikZ 14-Week Gantt Chart showing Critical Path in red, non-critical tasks in blue, reserve buffers, and 2 green Milestones at Week 8 and Week 12) + Table 6.3 (TSK-1.1 to TSK-5.2).

chapters/ch7_risks.tex (Pages 35–36, 2 pages):

Double quantification ($R = P \times I$), Figure 7.1 (TikZ 5x5 Risk Matrix Heatmap with red critical zone $R \ge 12$), Table 7.1 (6 concrete risks across Illumination/Camera variance RSK-ALG-01, Diffusion Hallucination on hands/nails RSK-GEN-02, Social Media Scraping API rate-limits RSK-DAT-03, GPU Cloud Cost spike vs. Ad CPM drop RSK-BIZ-04, Biometric Privacy GDPR leak RSK-SEC-05, and Cold-Start Catalog sparsity RSK-OPS-06), and Table 7.2 (Mitigation, Contingency Plan, and Residual Risk $R_{\text{residual}}$ for every critical risk).

chapters/ch8_summary.tex (Page 37, 1 page):

Design Readiness synthesis + Figure 8.1 (TikZ 3 immediate actions post-approval).

references.bib (Pages 38–40, 3 pages):

22+ verified IEEE-formatted academic and industry references.

6. STEP 6: EXECUTION LOOP & AUTOMATIC PUSH TO GITHUB (RONIOFFIR/roma-ai2)
Execute the following autonomous loop without stopping:

Create all 9 Skills in .claude/skills/ and skills/.

Run Skill 1 (expert-committee-prd) to generate PRD.md and populate the prompts/ directory (including saving our verbatim user prompts in prompts/00_user_session_prompts_log.md and all stage prompts in prompts/01_... through 05_...).

Run Skill 2 (cls-template-architect) to create report/base-report.cls, report/auratwin-report.cls, report/PROMPT.md, report/COMMANDS.md, and CHANGELOG.md. Run the 1-page BiDi stress test (Prompt B4) and verify it compiles with 0 errors.

Run Skills 3, 4, 5, 6 to generate the benchmark data (scripts/generate_beauty_benchmarks.py), cover graphics (scripts/render_hyperframes_cover.py), report/references.bib, report/coverpage.tex, report/main.tex, and all 8 chapter files (report/chapters/ch1_intro.tex through ch8_summary.tex).

Run the 4-pass Compilation (Chapter 13.4):

cd report
lualatex -interaction=nonstopmode -jobname=report main.tex
biber report
lualatex -interaction=nonstopmode -jobname=report main.tex
lualatex -interaction=nonstopmode -jobname=report main.tex

Run Skill 7 (bidi-qa-detector) via scripts/qa_detector_audit.py:

Parse report.log for any ! errors, undefined citations/references (??), or Overfull \hbox $> 5\text{pt}$.

Extract text from report.pdf page-by-page using pypdf/pdfplumber and scan for Hebrew words starting with final letters (ך,ם,ן,ף,ץ), reversed numbers, or unrendered macros.

Render key pages of report.pdf to PNG images (pdftoppm -png -r 150 or pdf2image) into report/figures/previews/ and visually inspect them for margin overflows, split boxes, orphaned headings, or empty space.

Verify that the main body is 40 pages (pages 1–40) plus 4 preliminary pages (total 44 pages). If the body is shorter or longer than 40 pages, adjust section depth/spacing cleanly until it hits the exact 40-page target.

Run Skill 8 (bidi-qa-fixer): Fix any repeating issues in base-report.cls/auratwin-report.cls (and bump version in CHANGELOG.md) and any local issues in chapters/chX.tex, then re-run the 4-pass compilation and Detector until 0 errors, 0 undefined citations, and 0 visual defects remain.

Run Skill 9 (red-team-examiner): Perform the 10-point Red-Team critique (report/work/red_team_review.md), strengthen the chapters accordingly, and recompile report/report.pdf.

Generate README.md: Write a comprehensive, visually stunning README.md at the repository root embedding the rendered PNG screenshots from report/figures/previews/ (Cover page, TOC, Radar/Scatter plots, System Architecture, Gantt chart, Risk heatmap), architecture overview, agent skills table, and 4-pass compilation instructions.

Git Commit & Push to https://github.com/RONIOFFIR/roma-ai2.git:

Initialize or verify the git repository, set remote origin to https://github.com/RONIOFFIR/roma-ai2.git, stage all files (PRD.md, README.md, CHANGELOG.md, .claude/skills/, skills/, prompts/, scripts/, report/ including report/report.pdf), commit with a clear engineering message, and push to main.

Start immediately with Step 1 and execute the entire pipeline autonomously!
````
