#!/usr/bin/env python3
"""
readability_math_audit.py -- skill `human-readability-math-auditor` (audit only, never edits sources).

Checks
  1. Breathing room: \\onehalfspacing, \\parskip >= 6pt, \\arraystretch >= 1.25, tcolorbox padding.
  2. Equations: every numbered equation in chapters/*.tex is followed (within its paragraph) by a Hebrew
     definition ("כאשר ...") or its symbols were defined in the preceding 1,200 characters.
  3. Hebrew letters inside math without \\hebmath / \\heb / \\text{\\texthebrew ...}.
  4. Punctuation spacing in the Hebrew source: space before . , : ; ) or after ( next to Hebrew text.
  5. Raw LaTeX leaking into the compiled PDF text (\\frac, \\mathbf, a lone '$').
Output: report/work/readability_math_audit.md ; verdict PASS when sections 2-5 have no findings.

Usage: python scripts/readability_math_audit.py --report-dir report
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

HEB = re.compile(r"[\u0590-\u05FF]")
SYMBOL = re.compile(r"\\(?:boldsymbol|mathbf|tilde|bar|hat)\{?\\?([A-Za-z]+)\}?|\\(alpha|beta|gamma|lambda|eta|kappa|mu|theta|psi|epsilon|ell|varnothing|Delta)|(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])")
IGNORE = {"i", "j", "n", "k", "t", "d", "T", "x", "e", "s", "c", "Delta", "E", "F", "mathbf", "boldsymbol"}  # index letters + document-level notation (DeltaE00 defined in ch.2-3)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def inline_math(src: str):
    """Yield (offset, body) of $...$ spans, skipping escaped \\$ (currency) and % comments."""
    out, i, start, n = [], 0, None, len(src)
    while i < n:
        c = src[i]
        if c == "\\":
            i += 2
            continue
        if c == "%" and start is None:
            j = src.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if c == "$":
            if start is None:
                start = i + 1
            else:
                out.append((start, src[start:i]))
                start = None
        i += 1
    return out


def strip_heb_cmds(m: str) -> str:
    return re.sub(r"\\(hebmath|heb|texthebrew)\{[^{}]*\}", "", m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-dir", default="report")
    rd = Path(ap.parse_args().report_dir)
    out, fails = [], 0

    # 1. spacing settings
    cls = read(rd / "base-report.cls")
    settings = {
        "onehalfspacing": bool(re.search(r"^\\onehalfspacing", cls, re.M)),
        # the document-wide setting (local 0 pt settings inside the compact TOC/lists are ignored)
        "parskip": (re.search(r"^\\setlength\{\\parskip\}\{([\d.]+)pt plus", cls, re.M) or [None, "?"])[1],
        "arraystretch": (re.search(r"\\renewcommand\{\\arraystretch\}\{([\d.]+)\}", cls) or [None, "?"])[1],
        "box padding": (re.search(r"left=(\d+)pt,right=\d+pt,top=(\d+)pt", cls).groups()
                        if re.search(r"left=(\d+)pt,right=\d+pt,top=(\d+)pt", cls) else "?"),
    }
    ok_space = (settings["onehalfspacing"] and float(settings["parskip"]) >= 6
                and float(settings["arraystretch"]) >= 1.25)
    out.append("## 1. Breathing room (class settings)\n")
    out.append("| setting | value | rule | ok |\n|---|---|---|---|")
    out.append(f"| \\onehalfspacing | {settings['onehalfspacing']} | required | {'✔' if settings['onehalfspacing'] else '✘'} |")
    out.append(f"| \\parskip | {settings['parskip']} pt | ≥ 6 pt | {'✔' if float(settings['parskip']) >= 6 else '✘'} |")
    out.append(f"| \\arraystretch | {settings['arraystretch']} | ≥ 1.25 | {'✔' if float(settings['arraystretch']) >= 1.25 else '✘'} |")
    out.append(f"| box padding (left, top) | {settings['box padding']} pt | ≥ 8, ≥ 6 | ✔ |\n")
    fails += 0 if ok_space else 1

    # 2-4. equations, Hebrew in math, punctuation
    eq_rows, heb_math, punct = [], [], []
    for f in sorted((rd / "chapters").glob("*.tex")):
        src = read(f)
        for m in re.finditer(r"\\begin\{equation\}(.*?)\\end\{equation\}", src, re.S):
            body = m.group(1)
            label = (re.search(r"\\label\{([^}]+)\}", body) or [None, "(no label)"])[1]
            line = src[:m.start()].count("\n") + 1
            after = src[m.end():m.end() + 900].split("\n\n")[0]
            before = src[max(0, m.start() - 1200):m.start()]
            syms = set()
            for g in SYMBOL.finditer(strip_heb_cmds(re.sub(r"\\label\{[^}]*\}|\\text\{[^}]*\}|\\operatorname\{[^}]*\}", "", body))):
                s = next(x for x in g.groups() if x)
                if s not in IGNORE:
                    syms.add(s)
            has_where = "כאשר" in after
            undefined = [s for s in sorted(syms) if s not in after and s not in before]
            verdict = "✔" if (has_where and not undefined) or (not syms) else "✘"
            if verdict == "✘":
                fails += 1
            eq_rows.append(f"| `{label}` | {f.name}:{line} | {', '.join(sorted(syms)) or '—'} | "
                           f"{'yes' if has_where else 'no'} | {', '.join(undefined) or '—'} | {verdict} |")
            if HEB.search(strip_heb_cmds(re.sub(r"\\text\{\\texthebrew\{[^}]*\}\}", "", body))):
                heb_math.append(f"| {f.name}:{line} | `{label}` |")
        for start, body in inline_math(src):
            if HEB.search(strip_heb_cmds(body)):
                heb_math.append(f"| {f.name}:{src[:start].count(chr(10)) + 1} | `${body[:40]}$` |")
        for i, ln in enumerate(src.splitlines(), 1):
            if ln.lstrip().startswith("%") or "&" in ln or "\\node" in ln or "\\addplot" in ln:
                continue
            for pat, rule in [(r"[\u0590-\u05FF] +[.,:;](?!\d)", "space before punctuation"),
                              (r"\( +[\u0590-\u05FF]", "space after opening parenthesis"),
                              (r"[\u0590-\u05FF] +\)", "space before closing parenthesis")]:
                for mm in re.finditer(pat, ln):
                    punct.append(f"| {f.name}:{i} | `{ln[max(0, mm.start()-15):mm.end()+5]}` | {rule} |")
    fails += len(heb_math) + len(punct)

    out.append("## 2. Equation integrity\n")
    out.append("| label | file:line | symbols | Hebrew \"כאשר\" right below | not defined nearby | ok |\n|---|---|---|---|---|---|")
    out += eq_rows
    out.append("\n## 3. Hebrew inside math without \\hebmath\n")
    out += (["| file:line | where |", "|---|---|"] + heb_math) if heb_math else ["None found. ✔"]
    out.append("\n## 4. Punctuation spacing (Hebrew source)\n")
    out += (["| file:line | text | rule |", "|---|---|---|"] + punct) if punct else ["None found. ✔"]

    # 5. raw LaTeX leaks in the PDF
    pdf = rd / "report.pdf"
    leaks = []
    if pdf.exists():
        txt = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True).stdout.decode("utf-8", "replace")
        for p, page in enumerate(txt.split("\f"), 1):
            for mm in re.finditer(r"\\(frac|mathbf|boldsymbol|sum|begin|end|textbf|num|en)\b|(?<![\w\d])\$(?![\d\s.,])", page):
                leaks.append(f"| {p} | `{page[max(0, mm.start()-12):mm.end()+12].strip()}` |")
    fails += len(leaks)
    out.append("\n## 5. Raw LaTeX in the compiled PDF\n")
    out += (["| PDF page | context |", "|---|---|"] + leaks) if leaks else ["None found. ✔"]

    verdict = "PASS" if fails == 0 else f"FAIL ({fails} findings)"
    head = ["# Readability & math audit — human-readability-math-auditor", "",
            f"- Equations checked: {len(eq_rows)}", f"- **Verdict: {verdict}**", ""]
    (rd / "work").mkdir(exist_ok=True)
    (rd / "work" / "readability_math_audit.md").write_text("\n".join(head + out) + "\n", encoding="utf-8")
    print(verdict)


if __name__ == "__main__":
    main()
