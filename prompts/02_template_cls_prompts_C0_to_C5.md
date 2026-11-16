# 02 — Template prompts C0–C5 (two-layer CLS)

Skill: `.claude/skills/cls-template-architect/SKILL.md` · Outputs: `report/base-report.cls`,
`report/auratwin-report.cls`, `report/PROMPT.md`, `report/COMMANDS.md`, `VERSION`, `CHANGELOG.md`.

## Prompt C0 — Build a Hebrew/English template (adapted)
```text
You are a LaTeX class designer. Create report/base-report.cls for LuaLaTeX with MiKTeX, for documents that mix
Hebrew RTL and English LTR. Work in six stages. After each stage, compile a test page, show it to me as an image:
1. Skeleton, Hebrew and English fonts (check `fc-list :lang=he` first: David, Arial, Times New Roman, Consolas),
   language switching with polyglossia; 12pt, 1.5 spacing, 2.5 cm margins + 0.5 cm binding gutter.
2. Commands that mark English words (\en), numbers (\num), Hebrew in math (\hebmath), © in the English font.
3. Chapters, sections, numbering by chapter, TOC depth 3, lists, Hebrew-letter preliminary page numbers (א'–ד'),
   \needspace before every section.
4. Styled tables (first column on the right, width ≤ 12.4 cm), four box types (managerbox, keymessagebox,
   warningbox, examplebox; never split), safe diagram wrapper (english environment), code boxes.
5. Header and footer with fixed direction in every slot, "עמוד N מתוך M".
6. biblatex + biber IEEE, a command list, a README (PROMPT.md), one full example.
Rules: one purpose per command. No Hebrew inside English units. Keep a version number and a changelog from day one.
```

## Prompt C1 — Learn the template before writing
```text
Before writing anything, learn the template in report/: read COMMANDS.md, PROMPT.md and tests/stress_test.tex.
Then tell me in 10 lines: the template version, which commands you will use, and which example you follow.
Use only commands that exist in the template.
```

## Prompt C2 — Use the template as the fixer
```text
This Hebrew/English problem repeats across report.pdf: [describe]. 1. Check the template version (VERSION).
2. Search CHANGELOG.md: was it already fixed? 3. If yes, upgrade and recompile — do not edit the chapter text.
4. If no, propose one fix in base-report.cls and say which documents it affects before changing anything.
```

## Prompt C3 — Add a function to the template
```text
Add keymessagebox to base-report.cls. Purpose: one highlighted message per chapter. Look: light teal background,
thick bar on the right, bold title. Default title "המסר המרכזי". It must work in Hebrew with English words inside
and never split across pages. Check that nothing similar exists, add an example to the stress test, show the image,
bump the version, add a CHANGELOG entry and a COMMANDS.md line. Change nothing else.
```

## Prompt C4 — Interview, then design (answers recorded)
| Question | Answer used |
|---|---|
| Brand name | AuraTwin AI |
| Logo | TikZ vector logo (two overlapping circles, plum + teal, amber pupil) — `\auratwinlogo` |
| Colours | plum `#4A2470` (primary), teal `#15807E` (AuraTwin / proposed), amber `#D4952B` (manager box, flagship), coral `#C8423B` (warnings, critical), indigo `#3949AB` (examples), green `#2E8B57` (milestones), grey `#8C8C99` (competitors) |
| Document types | report (default), proposal, spec |
| Fields | Hebrew title, English title, short title, group, institution, course, authors, short authors, advisor, partner, date, version, cover image |
| Header / footer | chapter title right, "AuraTwin AI \| דוח מכין \| roma-ai2" left; footer centre "עמוד N מתוך M", © right |
| Cover | double frame, banner image, Hebrew + English title, document type, team box, advisor, date, © |

## Prompt C5 — Build the company layer
```text
Build the approved brief as a thin layer report/auratwin-report.cls on top of base-report.cls. Do not edit or copy
the base. Document types are class options: report, proposal, spec. Each field is its own command. Brand colours
must reach headings, boxes and tables. Every header and footer slot sets its own direction. The Hebrew page count
reads right to left. © in the English font. Year from the compile date. Also create PROMPT.md with the rules for
writing new documents. Compile and show each example as an image.
```

## How it was used in this project — Prompt B4 stress-test result
`report/tests/stress_test.tex` (one page: Hebrew + English phrases, `1.0`, `10--20`, `85%`, `$1,500`, a formula with
Hebrew, a styled table, a TikZ diagram, all four boxes, a code box) compiled with **0 errors** after five
template-level fixes, released as **v1.2.0** (see `CHANGELOG.md`):

1. **`\en` is boxed** (`\mbox{\textenglish{…}}`): an unboxed `\textenglish` attached the comma after one English
   unit to the next one (`RAG, SMPL-X` rendered as `SMPL-XRAG`); isolated in `report/tests/bidi_comma_test.tex`.
   `\enlong{}` added as the unboxed, breakable variant for long titles.
2. **`Ligatures=TeX` on the English fonts**, so `\num{10--20}` prints an en dash.
3. **`tabularx` inside `reporttable`**: float/center opened in command form (`\table`, `\center`) so tabularx finds
   `\end{reporttable}` (error was "File ended while scanning use of \TX@get@body").
4. **Box titles** of `keymessagebox`/`warningbox` were printed in the white title colour (invisible); now printed in
   the accent colour.
5. **Footer "עמוד N מתוך M"** used `\ref` (gave a section number) — now `\pageref*` to the body-end label.

Preview: `report/figures/previews/stress_test_B4.png`.
