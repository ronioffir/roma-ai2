"""One-off repair: table rows whose terminator lost a backslash ('... \' -> '... \\').
Used after a shell heredoc collapsed '\\' to '\'. Only touches lines that end with a
single backslash (optionally followed by \midrule)."""
import re, sys, io
for path in sys.argv[1:]:
    s = io.open(path, encoding="utf-8").read()
    lines = s.split("\n")
    n = 0
    for i, ln in enumerate(lines):
        m = re.match(r"^(.*[^\\])\\( \\midrule)?\s*$", ln)
        if m and not ln.rstrip().endswith("\\\\") and "&" in ln:
            lines[i] = m.group(1) + "\\\\" + (m.group(2) or "")
            n += 1
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(path, "fixed", n)
