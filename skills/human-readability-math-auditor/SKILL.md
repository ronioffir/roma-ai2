---
name: human-readability-math-auditor
description: Senior Hebrew scientific copy-editor, typesetting readability inspector and mathematical LaTeX auditor. Checks breathing room (1.5 spacing, 6pt paragraph skip, box/table padding), Hebrew/English BiDi punctuation, and the integrity of every equation (numbering, variables defined in Hebrew right below, no raw LaTeX leaks, Hebrew in math only via \hebmath). Runs scripts/readability_math_audit.py and writes report/work/readability_math_audit.md. Use after content or template changes, before the red team.
---

# Human Readability & Math Auditor (מומחה קריאות, פיסוק ונוסחאות)

Like the QA detector, this skill **audits**; template fixes go through `bidi-qa-fixer`
(template-level) or the chapter author (one-off). It may propose exact replacement text.

## 1. Breathing room (אווריריות)
- `\onehalfspacing` in the body; `\parskip` = 6 pt (+1 pt stretch);
- `tcolorbox` inner padding ≥ 8 pt horizontally, ≥ 6 pt vertically; ≥ 8 pt before/after each box;
- table `\arraystretch` ≥ 1.25 and `\tabcolsep` ≥ 4 pt;
- visual pass: no page denser than ~33 text lines without a figure, box or heading break.

## 2. BiDi punctuation (פיסוק תקני)
- Hebrew punctuation follows the Hebrew word; periods/commas after an `\en{}`/`\num{}` unit sit on its left;
- no space before `.`, `,`, `:`, `;`, `)`; no space after `(`;
- Hebrew prefix letters attach with a hyphen to numbers/English (`ל-\num{1.8}`, `ב-\en{CVPR}`);
- no reversed English or numbers (cross-check with the detector's BiDi family);
- arrows in Hebrew sentences point right-to-left (`\leftarrow`).

## 3. Mathematical integrity (תקינות נוסחאות)
For every `equation`/`align`:
- it is numbered (chapter.number) and referenced or explained in the text;
- **every symbol is defined in Hebrew within the paragraph that follows** ("כאשר …");
- no Hebrew letters inside math except via `\hebmath{}`/`\text{\texthebrew{}}`;
- no raw LaTeX leaks in the PDF text (`\frac`, `\mathbf`, `$`);
- consistent notation across chapters (ΔE₀₀, S_j, R = P×I, r̄, T(s)).

## Run
```
python scripts/readability_math_audit.py --report-dir report
```
Output: `report/work/readability_math_audit.md` — one row per equation (label, file:line, symbols found,
symbols defined, verdict) + punctuation findings + spacing settings found in the class.
