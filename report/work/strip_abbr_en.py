r"""One-off text fix: drop the parenthesised English expansions inside \abbr{..}{..} lines of
coverpage.tex (they wrapped badly in the 2-column abbreviation list on page ד׳)."""
import io, re
p = "coverpage.tex"
s = io.open(p, encoding="utf-8").read()
s2 = re.sub(r" \(\\en\{[^{}]*\}\)(?=\}\s*$)", "", s, flags=re.M)
io.open(p, "w", encoding="utf-8").write(s2)
print(s.count("\\abbr{"), "abbr lines;", len(s) - len(s2), "chars removed")
