# COMMANDS.md — AuraTwin AI template command list (v1.2.0)

One line per public command. Use only these commands (booklet Prompt C1). Do not invent new ones —
if a pattern repeats three times, ask the template architect to add it (Prompt C3).

## BiDi units (Prompt B1)
| Command | Purpose | Example |
|---|---|---|
| `\en{…}` | One boxed LTR English unit (word, acronym, short phrase). Never Hebrew inside. | `\en{SMPL-X}` |
| `\enlong{…}` | Unboxed, line-breakable English text for long titles. Avoid before list commas. | `\enlong{A Tale of Two UNets}` |
| `\num{…}` | One unbreakable LTR numeric unit: decimals, ranges, percent, currency, units, math. | `\num{1.0}`, `\num{10--20}`, `\num{85\%}`, `\num{\$2,200}`, `\num{$\Delta E_{00}\le 1.8$}` |
| `\hebmath{…}` | Hebrew words inside math mode. | `$S_j \;\hebmath{ציון}$` |
| `\heb{…}` | Hebrew label inside an English/LTR environment (TikZ nodes). | `\node {\heb{כיול}};` |
| `\copyrightsign` | © in the English font. | |
| `\hq{…}` | Text in straight quotation marks. | |

## Structure
| Command | Purpose |
|---|---|
| `\frontmatterpages` | Start preliminary pages, numbered א׳, ב׳, ג׳, ד׳. |
| `\mainmatterpages` | Start the body, numbered 1…, footer "עמוד N מתוך M". |
| `\bodyend` | Put once at the last body page (sets M). |
| `\chapter`, `\section`, `\subsection` | New page per chapter; `\needspace` before sections. |
| `\printreferences[title]` | Bibliography chapter (Hebrew heading, LTR IEEE list). |
| `\templateversion` | Prints the template version. |

## Tables
| Command | Purpose |
|---|---|
| `\begin{reporttable}{caption}{label}{colspec}` | Floating styled table, caption above, width 12.4 cm, first column on the right. |
| `\begin{reporttable*}{caption}{label}{colspec}` | Same, non-floating (exact position). |
| `\headrow \hc{A} & \hc{B} \\ \midrule` | Coloured header row. |
| `\hlrow` | Highlight a row (e.g. the proposed solution). |
| `\cellok`, `\cellpartial`, `\cellno` | Literature-matrix marks: covered / partial / absent. |
| Column types `R L C`, `P{w}`, `Q{w}` | Right/left/centred X columns; fixed-width right/centred columns. |

## Figures
| Command | Purpose |
|---|---|
| `\begin{reportfigure}{caption}{label}` | Floating figure; content is LTR (TikZ/pgfplots safe); caption below. |
| `\begin{reportfigure*}{caption}{label}` | Same, non-floating. |
| `\maxobjwidth` | 12.4 cm — maximum width of any figure/table. |

## Boxes (never split across pages)
| Environment | Meaning | Colour |
|---|---|---|
| `managerbox[title]` | "למה זה חשוב למנהל" — start of every chapter | amber header |
| `keymessagebox[title]` | "המסר המרכזי" | teal bar on the right |
| `warningbox[title]` | "מלכודת הנדסית" | coral bar on the right |
| `examplebox[title]` | "יישום במערכת" | indigo header |
| `codebox` | Code listing (wrap in `\begin{english}`) | grey |

## Company layer (auratwin-report.cls)
Class options: `report` (default), `proposal`, `spec`.
Fields: `\doctitlehe` `\doctitleen` `\docshorttitle` `\docgroup` `\docinstitution` `\doccourse`
`\docauthors` `\docauthorsshort` `\docadvisor` `\docpartner` `\docdate` `\docversion` `\doccoverimage`.
`\makecoverpage` — double-frame cover without a page number. `\auratwinlogo[scale]` — TikZ logo.
Colours: `brandprimary` (plum), `brandsecondary` (teal = AuraTwin/proposed), `brandaccent` (amber = flagship),
`brandwarn` (red = critical), `brandexample` (indigo), `brandgreen` (milestones), `brandgrey` (competitors).
