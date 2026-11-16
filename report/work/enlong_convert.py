r"""One-off text fix (QA fixer): long English phrases (>= 3 words) inside the boxed \en{}
cannot break across lines and overflow the margin. Convert them to \enlong{} -- except when
the phrase is immediately followed by ', \en{' (a list of English units, where the boxed form
is required to keep comma order correct; see CHANGELOG v1.2.0)."""
import re, sys, io

PAT = re.compile(r"\\en\{([^{}$\\]*)\}")
for path in sys.argv[1:]:
    s = io.open(path, encoding="utf-8").read()
    out, last, n = [], 0, 0
    for m in PAT.finditer(s):
        words = m.group(1).split()
        follow = s[m.end():m.end() + 6]
        if len(words) >= 3 and not follow.startswith(", \\en{") and not follow.startswith(",\\en{"):
            out.append(s[last:m.start()] + "\\enlong{" + m.group(1) + "}")
            last = m.end(); n += 1
    out.append(s[last:])
    io.open(path, "w", encoding="utf-8").write("".join(out))
    print(path, n)
