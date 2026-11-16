r"""Template v1.3.0 (skills luxury-vintage-ui-designer + human-readability-math-auditor):
readability spacing and palette-driven boxes in base-report.cls. Each replacement must match once."""
import io
p = "C:/Users/Ella/roma-ai2/report/base-report.cls"
s = io.open(p, encoding="utf-8").read()
R = [
 (r"\def\basereport@version{1.2.1}", r"\def\basereport@version{1.3.0}"),
 (r"[2026/11/16 v1.2.1 Hebrew/English LuaLaTeX report base class]", r"[2026/11/16 v1.3.0 Hebrew/English LuaLaTeX report base class]"),
 (r"\definecolor{brandmuted}{HTML}{6B7280}",
  "\\definecolor{brandmuted}{HTML}{6B7280}\n"
  "\\definecolor{brandcream}{HTML}{F7F3EA}      % v1.3.0: soft box background (layer overrides)\n"
  "\\colorlet{brandhighlight}{brandsecondary}   % v1.3.0: proposed-solution series in charts\n"
  "\\definecolor{brandgreen}{HTML}{2E8B57}\n\\definecolor{brandgrey}{HTML}{8C8C99}"),
 (r"\setlength{\parskip}{4pt plus 1pt}", r"\setlength{\parskip}{6pt plus 1pt}   % v1.3.0 readability: 6 pt between paragraphs"),
 (r"\renewcommand{\arraystretch}{1.18}", r"\renewcommand{\arraystretch}{1.25}   % v1.3.0 readability: roomier rows"),
 ("    left=8pt,right=8pt,top=5pt,bottom=5pt,boxsep=0pt,", "    left=9pt,right=9pt,top=6pt,bottom=6pt,boxsep=0pt,   % v1.3.0 padding"),
 ("    before skip=7pt,after skip=7pt,", "    before skip=9pt,after skip=9pt,"),
 ("  colback=brandaccent!8,colframe=brandaccent,coltitle=black,",
  "  colback=brandcream!70!white,colframe=brandaccent,coltitle=brandprimary,"),
 ("  colback=brandsecondary!8,colframe=brandsecondary!8,boxrule=0pt,",
  "  colback=brandcream!45!white,colframe=brandcream!45!white,boxrule=0pt,"),
 ("  colback=brandexample!6,colframe=brandexample,boxrule=0.6pt,",
  "  colback=brandcream!35!white,colframe=brandexample,boxrule=0.6pt,"),
 (r"  \renewcommand{\headrule}{{\color{brandsecondary!60}\hrule height\headrulewidth}}%",
  r"  \renewcommand{\headrule}{{\color{brandaccent}\hrule height\headrulewidth}}%"),
]
for a, b in R:
    n = s.count(a)
    assert n == 1, (n, a)
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("base-report.cls -> v1.3.0")
