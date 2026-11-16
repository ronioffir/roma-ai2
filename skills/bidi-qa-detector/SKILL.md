---
name: bidi-qa-detector
description: QA Detector ("השוטר שבודק") — strictly read-only audit of the compiled report across the 9 QA families of booklet Table 19.1 and the 4 visual clues of section 14.5. Parses the log, extracts PDF text page by page, renders pages to PNG, checks page budget and bibliography consistency, and writes report/work/qa_audit_report.md. NEVER edits source files. Use after every compilation.
---

# BiDi & QA Detector — "השוטר שבודק"

## ABSOLUTE RULE
This skill DETECTS ONLY. It must not modify any `.tex`, `.cls`, `.bib` or script file.
Its only write target is `report/work/qa_audit_report.md` (and preview PNGs). Fixing is the job of
`bidi-qa-fixer`. Mixing detection and fixing in one pass is forbidden (booklet Prompt B2: "Do not fix anything yet").

## Run
```
python scripts/qa_detector_audit.py --report-dir report
```

## What is checked
| Family (Table 19.1) | Automated check |
|---|---|
| תבנית | template version in `.cls` == `VERSION`; no manual formatting commands in chapters (`\textcolor`, `\vspace` > 1cm, `\fontsize`) |
| דף שער | page 1 has no visible page number; ©, both titles, team, advisor, date present |
| כיווניות BiDi | Hebrew tokens starting with a final letter ךםןףץ; reversed acronyms (dictionary of known acronyms reversed); suspicious decimals (`0.1` where source says `1.0`); reversed ranges (larger number first) |
| טבלאות | Overfull \hbox inside tabular; table width vs 12.4 cm |
| תמונות | missing files; every `\label{fig:}`/`\label{tab:}` referenced by a `\ref` |
| קוד | code boxes inside margin (Overfull) |
| עימוד | total pages = 44; body = 40; chapter start pages vs budget; headings in the last 15% of a page; nearly-empty pages (< 25% text) |
| מקורות | `!` errors, undefined citations/references, `??` in the PDF text, every bib key cited and every cite in bib |
| מבנה קבצים | expected tree exists (skills, prompts, scripts, report files) |

## Output format (`report/work/qa_audit_report.md`)
For every finding: ID, family, page (PDF page and printed page), file:line if known, exact text,
rule broken, and classification **TEMPLATE-LEVEL (repeating)** or **ONE-OFF (local text)**.
A finding is template-level if the same pattern appears on ≥ 3 pages or originates in a `.cls` macro.
End with a summary count per family and the verdict `PASS` (0 findings) or `FAIL`.

## Visual pass
Render pages with `pdftoppm -png -r 60` (all) and `-r 110` (key pages) into `report/figures/previews/`
and look at them: margin touches, split boxes, orphan headings, large gaps inside a line, mirrored headers.
