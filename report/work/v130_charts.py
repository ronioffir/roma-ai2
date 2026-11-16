r"""Skill luxury-vintage-ui-designer: chart series roles in the new palette.
Proposed solution = Copper (brandhighlight); flagship = Mustard; competitors = Dust tints;
critical = Garnet; status-quo bars = Dust + Mustard. Each replacement must match the expected count."""
import io
B = "C:/Users/Ella/roma-ai2/report/chapters/"
E = {
 "ch2_problem.tex": [
  (r"\addplot[fill=brandgrey!70,draw=brandgrey] table[x=mean", r"\addplot[fill=brandsecondary!75,draw=brandsecondary] table[x=mean", 1),
  (r"\addplot[fill=brandsecondary!70,draw=brandsecondary] table[x=p95", r"\addplot[fill=brandaccent!85,draw=brandaccent!80!black] table[x=p95", 1)],
 "ch5_alternatives.tex": [
  (r"\addplot[fill=brandgrey!70,draw=brandgrey] table[x=mean", r"\addplot[fill=brandsecondary!75,draw=brandsecondary] table[x=mean", 1),
  (r"\addplot[fill=brandsecondary!70,draw=brandsecondary] table[x=p95", r"\addplot[fill=brandaccent!85,draw=brandaccent!80!black] table[x=p95", 1),
  (r"\addplot[fill=brandsecondary,draw=white] table[x=acc", r"\addplot[fill=brandhighlight,draw=white] table[x=acc", 1),
  (r"\addplot[fill=brandexample!80,draw=white] table[x=lat", r"\addplot[fill=brandsecondary,draw=white] table[x=lat", 1),
  (r"\addplot[fill=brandgreen!70,draw=white] table[x=priv", r"\addplot[fill=brandwarn!75,draw=white] table[x=priv", 1),
  (r"\addplot[fill=brandgrey!70,draw=white] table[x=dev", r"\addplot[fill=brandcream!80!brandaccent,draw=white] table[x=dev", 1),
  (r"\addplot[brandsecondary,very thick] table[x=w,y=alt3]", r"\addplot[brandhighlight,very thick] table[x=w,y=alt3]", 2),
  (r"\addplot[brandgrey,thick] table[x=w,y=alt1]", r"\addplot[brandsecondary,thick] table[x=w,y=alt1]", 2)],
 "ch4_market.tex": [
  (r"\addplot[brandexample!70,thick,dotted,mark=none]", r"\addplot[brandsecondary,thick,dotted,mark=none]", 1),
  (r"\addplot[brandsecondary,ultra thick,fill=brandsecondary,", r"\addplot[brandhighlight,ultra thick,fill=brandhighlight,", 1),
  (r"\addplot[only marks, mark=star, mark size=6pt, brandsecondary, very thick]", r"\addplot[only marks, mark=star, mark size=6pt, brandhighlight, very thick]", 1),
  (r"\node[font=\scriptsize,text=brandsecondary,anchor=north] at (axis cs:0.011,84)", r"\node[font=\scriptsize,text=brandhighlight,anchor=north] at (axis cs:0.011,84)", 1),
  (r"\addplot[only marks, mark=*, mark size=3pt, brandgrey,", r"\addplot[only marks, mark=*, mark size=3pt, brandsecondary,", 1)],
 "ch6_workplan.tex": [("brandexample!70}", "brandsecondary!75}", 6)],
}
for f, reps in E.items():
    s = io.open(B + f, encoding="utf-8").read()
    for a, b, n in reps:
        c = s.count(a)
        assert c == n, (f, c, n, a)
        s = s.replace(a, b)
    io.open(B + f, "w", encoding="utf-8").write(s)
print("charts recoloured")
