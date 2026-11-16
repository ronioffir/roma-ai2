"""Helper (QA fixer): replace an inclusive 1-based line range of a UTF-8 file with given text.
Usage: python cut_lines.py FILE FIRST LAST "replacement text (may be empty)" """
import io, sys
path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rep = sys.argv[4] if len(sys.argv) > 4 else ""
lines = io.open(path, encoding="utf-8").read().split("\n")
new = lines[:a - 1] + ([rep] if rep else []) + lines[b:]
io.open(path, "w", encoding="utf-8").write("\n".join(new))
print(f"{path}: replaced lines {a}-{b} ({b - a + 1} lines)")
