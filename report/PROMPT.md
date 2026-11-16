# PROMPT.md — how a model writes a new document with the AuraTwin AI template

This file is the self-documenting manual of the template (booklet §15.4, Table 15.3).
A new model reads this file, `COMMANDS.md`, `../CHANGELOG.md` and `main.tex` before writing.

## Help system (booklet Table 15.3)
| Question | Where the answer is |
|---|---|
| Which version do I have? | `../VERSION`, `\templateversion`, first lines of both `.cls` files |
| What changed in this version? | `../CHANGELOG.md` |
| Which commands exist? | `COMMANDS.md` (one line each) |
| Is there documentation on a topic? | this file + comments in `base-report.cls` (search with grep) |
| Is there a ready example? | `tests/stress_test.tex` (one page), `main.tex` (full 44-page report) |

## Rules for writing (copy into the first message of every writing session)
1. Hebrew is the document language; English and numbers are LTR units: `\en{}` for words and
   acronyms, `\num{}` for every number, range, percent, currency and unit. Never Hebrew inside them.
2. Long English titles that must wrap: `\enlong{}`. Never put list commas after `\enlong`.
3. Math in `$…$`; Hebrew inside math: `\hebmath{}`.
4. Every TikZ/pgfplots picture goes inside `reportfigure` (LTR); Hebrew node text in `\heb{}`;
   width ≤ 12.4 cm.
5. Tables only through `reporttable`; the first column of the colspec is printed on the right —
   never reverse the column order by hand.
6. Every figure and table is referenced in the text (`איור~\ref{}`, `טבלה~\ref{}`) with one sentence
   that says what the reader learns from it.
7. Third person, professional tone; first mention of a technical term: Hebrew (English).
8. Every factual claim has `\cite{}`; numbers that are team estimates or simulated data say so.
9. No manual formatting (`\textcolor`, `\fontsize`, big `\vspace`) in chapter files. A repeated
   need becomes a template command (Prompt C3) with a version bump.
10. Never type Hebrew in reverse to make it "look right" — mark the direction instead.
11. (v1.3.0) Colours only through semantic names or `\accenttext`/`\mutedtext`; in charts the proposed
    solution is `brandhighlight` (Copper), the flagship `brandaccent` (Mustard), competitors `brandsecondary`
    (Dust) tints, critical items `brandwarn` (Garnet).
12. (v1.3.0) Inside an LTR TikZ node, a mixed Hebrew/English label is ONE `\heb{…}` unit with `\en{}`/`\num{}`
    inside — separate `\heb{}` and `\en{}` pieces are laid out left-to-right in the wrong order.
13. (v1.3.0) Every numbered equation is followed by a Hebrew "כאשר …" sentence that defines every symbol
    (checked by `scripts/readability_math_audit.py`).

## Compile (booklet §13.4)
```
cd report
lualatex -interaction=nonstopmode -jobname=report main.tex
biber report
lualatex -interaction=nonstopmode -jobname=report main.tex
lualatex -interaction=nonstopmode -jobname=report main.tex
```
Success screen: `Output written on report.pdf (44 pages …)` and no line starting with `!` in `report.log`.

## Starting a new document of another type
```latex
\documentclass[proposal]{auratwin-report}   % report | proposal | spec
\addbibresource{references.bib}
\doctitlehe{...}\doctitleen{...}\docgroup{...}\docauthors{...}\docauthorsshort{...}
\begin{document}
\makecoverpage \frontmatterpages ... \mainmatterpages ... \bodyend
\end{document}
```
