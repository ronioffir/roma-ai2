"""Attribute Overfull/Underfull boxes in report.log to the source file being read (helper)."""
import re, sys, collections
log = open(sys.argv[1] if len(sys.argv) > 1 else "report.log", encoding="utf-8", errors="replace").read()
stack, out = [], collections.Counter()
for m in re.finditer(r"\((\./[^\s()]+\.(?:tex|lot|lof|toc|bbl))|(\))|Overfull \\hbox \(([\d.]+)pt too wide\) in (?:paragraph|alignment) at lines (\d+)--(\d+)", log):
    if m.group(1):
        stack.append(m.group(1))
    elif m.group(2):
        if stack:
            stack.pop()
    else:
        f = stack[-1] if stack else "?"
        if float(m.group(3)) > 1.0:
            out[(f, m.group(4))] = max(out[(f, m.group(4))], float(m.group(3)))
for (f, l), w in sorted(out.items()):
    print(f"{f}:{l}  max {w:.1f}pt")
