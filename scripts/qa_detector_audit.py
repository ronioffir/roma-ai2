#!/usr/bin/env python3
"""
qa_detector_audit.py -- "השוטר שבודק": the read-only QA Detector of the AuraTwin AI report.

Implements skill .claude/skills/bidi-qa-detector (booklet Prompt B2, Table 19.1, §14.5, §19.4).
It NEVER edits sources. Its only outputs are:
    <report-dir>/work/qa_audit_report.md
    <report-dir>/figures/previews/pages/*.png   (page renders for the visual pass)
    <report-dir>/figures/previews/key_*.png     (with --key-pages)

Checks, grouped by the 9 QA families of booklet Table 19.1:
    תבנית        template version consistency; manual formatting in chapter files
    דף שער       cover page: no visible page number, key fields present
    כיווניות     final Hebrew letter at word start, reversed acronyms, reversed numbers/ranges,
                 comma-led amounts, unrendered macros, '??'
    טבלאות/קוד   Overfull \\hbox > 5pt (with source line numbers)
    תמונות       missing graphic files; every fig:/tab: label referenced
    עימוד        total pages, body pages, chapter start pages vs budget, nearly-empty pages
    מקורות       '!' errors, undefined citations/references, bib <-> \\cite consistency
    מבנה קבצים   expected repository tree

Each finding is classified TEMPLATE-LEVEL (same rule on >= 3 pages, or rooted in a .cls) or ONE-OFF.

Usage:
    python scripts/qa_detector_audit.py --report-dir report [--key-pages 1,2,3,9] [--no-render]
Exit code is always 0; the verdict is written to the report (PASS / FAIL).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import shutil
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

# ----------------------------------------------------------------- configuration
PRELIM_PAGES = 4
EXPECTED_TOTAL = 44
EXPECTED_BODY = 40
# printed start page of each chapter (in order) and of the references
CHAPTER_BUDGET = [1, 4, 8, 17, 23, 31, 35, 37]
REFERENCES_START = 38
OVERFULL_LIMIT_PT = 5.0
NEARLY_EMPTY_RATIO = 0.25
TEMPLATE_LEVEL_MIN_PAGES = 3

FINAL_LETTERS = "ךםןףץ"
ACRONYMS = ["RAG", "LLM", "CIELAB", "SMPL-X", "VTON", "API", "GPU", "SDK", "TAM", "SAM", "SOM",
            "CAGR", "WBS", "RACI", "ARPU", "GDPR", "CLIP", "FAISS"]
BIDI_MARKS = re.compile("[\u200e\u200f\u202a-\u202e\u2066-\u2069]")
HEB_TOKEN = re.compile(r"[\u05D0-\u05EA]+")

FAMILIES = ["תבנית", "דף שער", "כיווניות BiDi", "טבלאות", "תמונות", "קוד", "עימוד", "מקורות",
            "מבנה קבצים"]

EXPECTED_TREE = [
    "README.md", "PRD.md", "CHANGELOG.md", "VERSION",
    ".claude/skills", "skills", "prompts/00_user_session_prompts_log.md",
    "scripts/generate_beauty_benchmarks.py", "scripts/render_hyperframes_cover.py",
    "scripts/qa_detector_audit.py",
    "report/base-report.cls", "report/auratwin-report.cls", "report/PROMPT.md", "report/COMMANDS.md",
    "report/main.tex", "report/coverpage.tex", "report/references.bib",
    "report/chapters/ch1_intro.tex", "report/chapters/ch2_problem.tex",
    "report/chapters/ch3_literature.tex", "report/chapters/ch4_market.tex",
    "report/chapters/ch5_alternatives.tex", "report/chapters/ch6_workplan.tex",
    "report/chapters/ch7_risks.tex", "report/chapters/ch8_summary.tex",
]


# ----------------------------------------------------------------------- helpers
class Finding:
    __slots__ = ("family", "page", "loc", "text", "rule", "rule_id", "cls")

    def __init__(self, family, rule_id, rule, text="", page=None, loc="", cls=None):
        self.family, self.rule_id, self.rule = family, rule_id, rule
        self.text, self.page, self.loc, self.cls = text, page, loc, cls


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=300)
        return p.returncode, p.stdout.decode("utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def printed_page(pdf_page: int | None) -> str:
    if pdf_page is None:
        return "—"
    if pdf_page <= PRELIM_PAGES:
        return "אבגד"[pdf_page - 1] + "׳"
    return str(pdf_page - PRELIM_PAGES)


def brace_args(s: str, start: int) -> tuple[list[str], int]:
    """Read consecutive {..} groups starting at s[start] (balanced braces)."""
    args, i = [], start
    while i < len(s) and s[i] in " \t":
        i += 1
    while i < len(s) and s[i] == "{":
        depth, j = 0, i
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        args.append(s[i + 1:j])
        i = j + 1
    return args, i


def strip_tex(s: str) -> str:
    s = re.sub(r"\\(?:en|enlong|num|heb|texthebrew|textenglish|LR|mbox|textbf|emph)\s*\{", "{", s)
    s = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]]*\])?", " ", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ").replace("$", "")
    return re.sub(r"\s+", " ", s).strip()


# ----------------------------------------------------------------- the detector
class Detector:
    def __init__(self, report_dir: Path, render: bool, key_pages: list[int], use_layout: bool):
        self.rd = report_dir
        self.root = report_dir.parent
        self.render = render
        self.key_pages = key_pages
        self.use_layout = use_layout
        self.findings: list[Finding] = []
        self.pages: list[str] = []
        self.n_pages = 0
        self.notes: list[str] = []

    def add(self, *a, **k):
        self.findings.append(Finding(*a, **k))

    # ------------------------------------------------------------- sources
    def tex_files(self) -> list[Path]:
        files = [self.rd / "main.tex", self.rd / "coverpage.tex"]
        files += sorted((self.rd / "chapters").glob("*.tex"))
        return [f for f in files if f.exists()]

    # ------------------------------------------------------------------ log
    def check_log(self):
        log_path = self.rd / "report.log"
        log = read(log_path)
        if not log:
            self.add("מקורות", "LOG-MISSING", "report.log not found -- compile first", str(log_path))
            return
        lines = log.splitlines()
        current_file = "?"
        # last opened source/auxiliary file (TOC/LoF/LoT overfulls are attributed to report.toc etc.)
        file_re = re.compile(r"\((\./[^\s()]+\.(?:tex|cls|toc|lof|lot|bbl))")
        for i, line in enumerate(lines):
            for m in file_re.finditer(line):
                current_file = m.group(1)[2:]
            if line.startswith("!"):
                ctx = " ".join(l.strip() for l in lines[i:i + 3])
                lm = re.search(r"l\.(\d+)", " ".join(lines[i:i + 8]))
                loc = f"{current_file}:{lm.group(1)}" if lm else current_file
                fam = "תבנית" if current_file.endswith(".cls") else "מקורות"
                self.add(fam, "LOG-ERROR", "line starting with '!' in report.log", ctx[:200], loc=loc,
                         cls="TEMPLATE-LEVEL" if current_file.endswith(".cls") else None)
            m = re.search(r"Citation [`'](.+?)' on page (\S+) undefined", line)
            if m:
                self.add("מקורות", "CITE-UNDEF", "undefined citation", m.group(1), loc=f"page {m.group(2)}")
            m = re.search(r"Reference [`'](.+?)' on page (\S+) undefined", line)
            if m:
                self.add("מקורות", "REF-UNDEF", "undefined reference", m.group(1), loc=f"page {m.group(2)}")
            m = re.search(r"Overfull \\hbox \(([\d.]+)pt too wide\).*?lines? (\d+)(?:--(\d+))?", line)
            if m and float(m.group(1)) > OVERFULL_LIMIT_PT:
                fam = ("עימוד" if current_file.endswith((".toc", ".lof", ".lot"))
                       else "טבלאות" if current_file.endswith(".tex") else "קוד")
                self.add(fam, "OVERFULL", f"Overfull \\hbox > {OVERFULL_LIMIT_PT:g}pt (text touches margin)",
                         f"{m.group(1)}pt", loc=f"{current_file}:{m.group(2)}")
            if "Missing character" in line:
                self.add("כיווניות BiDi", "MISSING-GLYPH", "missing glyph in font", line.strip()[:160],
                         loc=current_file)
            m = re.search(r"File [`'](.+?)' not found", line)
            if m:
                self.add("תמונות", "FILE-MISSING", "file not found", m.group(1), loc=current_file)
        if "There were undefined references" in log or "Please (re)run Biber" in log:
            self.add("מקורות", "RERUN", "log asks for another run (biber/lualatex)", "", loc="report.log")

    # ------------------------------------------------------------------ pdf
    def load_pdf(self) -> bool:
        pdf = self.rd / "report.pdf"
        if not pdf.exists():
            self.add("עימוד", "PDF-MISSING", "report.pdf not found -- compile first", str(pdf))
            return False
        if not shutil.which("pdftotext") or not shutil.which("pdfinfo"):
            self.add("מבנה קבצים", "TOOLS", "pdftotext/pdfinfo not on PATH", "")
            return False
        _, info = run(["pdfinfo", str(pdf)])
        m = re.search(r"Pages:\s+(\d+)", info)
        self.n_pages = int(m.group(1)) if m else 0
        for i in range(1, self.n_pages + 1):
            cmd = ["pdftotext", "-enc", "UTF-8", "-f", str(i), "-l", str(i)]
            if self.use_layout:
                cmd.append("-layout")
            _, txt = run(cmd + [str(pdf), "-"])
            # Times New Roman's hyphen glyph is extracted as U+00AD (soft hyphen); it is printed
            # as a normal hyphen, so normalise it before matching ("roma-ai2", "REQ-VIS-01").
            self.pages.append(BIDI_MARKS.sub("", txt).replace("­", "-"))
        return True

    def check_pdf_text(self):
        src = "\n".join(read(f) for f in self.tex_files())
        src_decimals = set(re.findall(r"\d+\.\d+", src))
        # Numbers generated by LaTeX itself (section / figure / table / equation numbers such as
        # "5.4" or "7.1") are legitimate even if their mirror appears in the source; take them from
        # the \newlabel entries of the .aux file so the NUM-REV heuristic does not flag them.
        aux = read(self.rd / "report.aux") if (self.rd / "report.aux").exists() else ""
        generated = set(re.findall(r"\\newlabel\{[^}]*\}\{\{(?:\\LR \{|\\LR\{)?(\d+\.\d+)", aux))
        generated |= set(re.findall(r"\{(?:section|subsection|figure|table|equation)\}\{\\numberline \{(?:\\LR \{)?(\d+\.\d+)", aux))
        src_decimals |= generated
        src_ranges = set(re.findall(r"(\d+)\s*--\s*(\d+)", src))
        for p, txt in enumerate(self.pages, start=1):
            # 1. final letter at the start of a Hebrew word
            for tok in HEB_TOKEN.findall(txt):
                if len(tok) > 1 and tok[0] in FINAL_LETTERS:
                    self.add("כיווניות BiDi", "FINAL-LETTER", "Hebrew word starts with a final letter (reversed?)",
                             tok, page=p)
            # 2. reversed acronyms
            for a in ACRONYMS:
                rev = a[::-1]
                if rev != a and re.search(r"(?<![A-Za-z])" + re.escape(rev) + r"(?![A-Za-z])", txt):
                    self.add("כיווניות BiDi", "ACRONYM-REV", f"reversed acronym ({a})", rev, page=p)
            # 3. suspicious decimals: d.d in PDF whose mirror exists in sources but itself does not
            for d in set(re.findall(r"(?<![\d.])(\d)\.(\d)(?![\d.])", txt)):
                shown, mirror = f"{d[0]}.{d[1]}", f"{d[1]}.{d[0]}"
                if shown != mirror and shown not in src_decimals and mirror in src_decimals:
                    self.add("כיווניות BiDi", "NUM-REV", "decimal possibly reversed", f"{shown} (source: {mirror})",
                             page=p)
            # 4. reversed ranges
            for a, b in set(re.findall(r"(?<!\d)(\d+)\s*[–-]\s*(\d+)(?!\d)", txt)):
                if int(a) > int(b) and (b, a) in src_ranges and (a, b) not in src_ranges:
                    self.add("כיווניות BiDi", "RANGE-REV", "range printed largest-first", f"{a}–{b}", page=p)
            # 5. amounts that start with a comma ("500,1")
            for m in re.finditer(r"(?<![\d,.])\d{3},\d(?!\d)", txt):
                self.add("כיווניות BiDi", "AMOUNT-SPLIT", "amount split around the comma", m.group(0), page=p)
            # 6. unresolved references and unrendered macros
            if "??" in txt:
                self.add("מקורות", "QQ", "'??' in PDF text (unresolved reference)", "??", page=p)
            for m in set(re.findall(r"\\[A-Za-z]{2,}", txt)):
                self.add("כיווניות BiDi", "MACRO-LEAK", "unrendered macro in PDF text", m, page=p)

    def check_cover(self):
        if not self.pages:
            return
        cover = self.pages[0]
        last = [l.strip() for l in cover.splitlines() if l.strip()]
        if last and re.fullmatch(r"(\d+|[אב]׳?|i)", last[-1]):
            self.add("דף שער", "COVER-PAGENUM", "cover shows a page number", last[-1], page=1)
        for needle, rule in [("©", "copyright sign missing"), ("roma-ai2", "group code missing"),
                             ("AuraTwin", "English title missing"), ("דוח מכין", "document type missing")]:
            if needle not in cover:
                self.add("דף שער", "COVER-FIELD", rule, needle, page=1)

    def check_pagination(self):
        if not self.n_pages:
            return
        if self.n_pages != EXPECTED_TOTAL:
            self.add("עימוד", "PAGE-TOTAL", f"total pages must be {EXPECTED_TOTAL}", str(self.n_pages))
        body = self.n_pages - PRELIM_PAGES
        if body != EXPECTED_BODY:
            self.add("עימוד", "PAGE-BODY", f"body pages must be {EXPECTED_BODY}", str(body))
        # chapter start pages from the .toc (reliable), fallback: PDF text search
        toc = read(self.rd / "report.toc")
        starts: list[tuple[str, int]] = []
        for m in re.finditer(r"\\contentsline\s*", toc):
            args, _ = brace_args(toc, m.end())
            if len(args) >= 3 and args[0] == "chapter":
                pg = re.sub(r"[^\d]", "", args[2])
                if pg:
                    starts.append((strip_tex(args[1]), int(pg)))
        if not starts:
            starts = self._chapter_starts_from_text()
        expected = CHAPTER_BUDGET + [REFERENCES_START]
        for i, (title, pg) in enumerate(starts[: len(expected)]):
            if pg != expected[i]:
                self.add("עימוד", "BUDGET", f"chapter must start on printed page {expected[i]}",
                         f"{title[:60]} starts on page {pg}", page=pg + PRELIM_PAGES)
        if len(starts) < len(expected):
            self.notes.append(f"Only {len(starts)} chapter entries found in report.toc (expected {len(expected)}).")
        # nearly-empty pages (exclude cover and prelim pages)
        counts = [len(re.sub(r"\s", "", t)) for t in self.pages]
        body_counts = counts[PRELIM_PAGES:] or counts
        med = statistics.median(body_counts) if body_counts else 0
        for p, c in enumerate(counts, start=1):
            if p == 1:
                continue
            if med and c < NEARLY_EMPTY_RATIO * med:
                self.add("עימוד", "NEARLY-EMPTY", f"page text < {int(NEARLY_EMPTY_RATIO*100)}% of median page",
                         f"{c} chars (median {int(med)})", page=p)

    def _chapter_starts_from_text(self) -> list[tuple[str, int]]:
        out = []
        for f in sorted((self.rd / "chapters").glob("ch*.tex")):
            s = read(f)
            m = re.search(r"\\chapter\*?\s*", s)
            if not m:
                continue
            args, _ = brace_args(s, m.end())
            title = strip_tex(args[0]) if args else ""
            key = " ".join(title.split()[:3])
            for p in range(PRELIM_PAGES + 1, self.n_pages + 1):
                if key and key in re.sub(r"\s+", " ", self.pages[p - 1]):
                    out.append((title, p - PRELIM_PAGES))
                    break
        return out

    # ------------------------------------------------------------ sources
    def check_bib_and_labels(self):
        bib = read(self.rd / "references.bib")
        keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib))
        cited: dict[str, str] = {}
        labels: dict[str, str] = {}
        refs: set[str] = set()
        for f in self.tex_files():
            for n, line in enumerate(read(f).splitlines(), start=1):
                code = line.split("%")[0] if not line.lstrip().startswith("%") else ""
                for m in re.finditer(r"\\(?:cite|parencite|textcite|nocite)\*?(?:\[[^\]]*\])?\{([^}]*)\}", code):
                    for k in m.group(1).split(","):
                        cited.setdefault(k.strip(), f"{f.relative_to(self.rd)}:{n}")
                for m in re.finditer(r"\\label\{((?:fig|tab):[^}]*)\}", code):
                    labels[m.group(1)] = f"{f.relative_to(self.rd)}:{n}"
                for m in re.finditer(r"\{((?:fig|tab):[^}]*)\}", code):
                    if not re.search(r"\\label\{" + re.escape(m.group(1)) + r"\}", code):
                        refs.add(m.group(1))
                for m in re.finditer(r"\\(?:ref|pageref|autoref|cref)\*?\{([^}]*)\}", code):
                    refs.add(m.group(1))
        if "*" in cited:
            cited.pop("*")
            self.notes.append("\\nocite{*} used -- uncited entries would be printed.")
        for k in sorted(keys - set(cited)):
            self.add("מקורות", "BIB-UNCITED", "bib entry never cited", k, loc="references.bib")
        for k in sorted(set(cited) - keys):
            self.add("מקורות", "CITE-NOBIB", "cited key missing from references.bib", k, loc=cited[k])
        for lab, loc in sorted(labels.items()):
            if lab not in refs:
                self.add("תמונות", "LABEL-UNREF", "figure/table never referenced in the text (iron rule 11.1)",
                         lab, loc=loc)
        self.notes.append(f"Bibliography: {len(keys)} entries, {len(cited)} distinct cited keys; "
                          f"{len(labels)} figure/table labels.")

    def check_template(self):
        ver = read(self.root / "VERSION").strip()
        for cls in ("base-report.cls", "auratwin-report.cls"):
            s = read(self.rd / cls)
            m = re.search(r"\\def\\\w+@version\{([\d.]+)\}", s)
            if not s:
                self.add("תבנית", "CLS-MISSING", "class file missing", cls, cls="TEMPLATE-LEVEL")
            elif ver and m and m.group(1) != ver:
                self.add("תבנית", "VERSION", "class version differs from VERSION", f"{cls} {m.group(1)} != {ver}",
                         loc=cls, cls="TEMPLATE-LEVEL")
        manual = re.compile(r"\\(textcolor|color\{|fontsize|selectfont)|\\vspace\*?\{\s*-?\s*([1-9]\d*(\.\d+)?)\s*cm")
        for f in sorted((self.rd / "chapters").glob("*.tex")):
            for n, line in enumerate(read(f).splitlines(), start=1):
                if line.lstrip().startswith("%"):
                    continue
                # manual formatting outside figures is a template smell
                if manual.search(line) and "tikz" not in line and "node" not in line and "draw" not in line \
                        and "addplot" not in line and "\\fill" not in line:
                    self.add("תבנית", "MANUAL-FMT", "manual formatting in chapter file (use a template command)",
                             line.strip()[:100], loc=f"{f.relative_to(self.rd)}:{n}")

    def check_tree(self):
        for rel in EXPECTED_TREE:
            if not (self.root / rel).exists():
                self.add("מבנה קבצים", "TREE", "expected path missing", rel)
        skills = list((self.root / ".claude" / "skills").glob("*/SKILL.md"))
        mirror = list((self.root / "skills").glob("*/SKILL.md"))
        if len(skills) != 12:
            self.add("מבנה קבצים", "SKILLS", "expected 12 skills in .claude/skills", str(len(skills)))
        if len(mirror) != len(skills):
            self.add("מבנה קבצים", "SKILLS-MIRROR", "skills/ mirror differs from .claude/skills",
                     f"{len(mirror)} vs {len(skills)}")

    # ------------------------------------------------------------ rendering
    def render_pages(self):
        pdf = self.rd / "report.pdf"
        if not (self.render and pdf.exists() and shutil.which("pdftoppm")):
            return
        out = self.rd / "figures" / "previews" / "pages"
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("p-*.png"):
            old.unlink()
        run(["pdftoppm", "-png", "-r", "50", str(pdf), str(out / "p")])
        for k in self.key_pages:
            run(["pdftoppm", "-png", "-r", "110", "-f", str(k), "-l", str(k), "-singlefile", str(pdf),
                 str(self.rd / "figures" / "previews" / f"key_p{k:02d}")])
        self.notes.append(f"Rendered {self.n_pages} pages at 50 dpi to {out.relative_to(self.root)}"
                          + (f"; key pages {self.key_pages} at 110 dpi." if self.key_pages else "."))

    # ------------------------------------------------------------ classify & write
    def classify(self):
        pages_by_rule = defaultdict(set)
        for f in self.findings:
            if f.page is not None:
                pages_by_rule[f.rule_id].add(f.page)
        for f in self.findings:
            if f.cls is None:
                f.cls = "TEMPLATE-LEVEL" if len(pages_by_rule[f.rule_id]) >= TEMPLATE_LEVEL_MIN_PAGES \
                    else "ONE-OFF"

    def write(self) -> Path:
        out = self.rd / "work" / "qa_audit_report.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        verdict = "PASS" if not self.findings else "FAIL"
        by_fam = defaultdict(int)
        for f in self.findings:
            by_fam[f.family] += 1
        L = [f"# QA audit report — bidi-qa-detector", "",
             f"- Generated: {_dt.datetime.now():%Y-%m-%d %H:%M}",
             f"- PDF: `{(self.rd / 'report.pdf').relative_to(self.root)}` — {self.n_pages} pages "
             f"(expected {EXPECTED_TOTAL} = {PRELIM_PAGES} preliminary + {EXPECTED_BODY} body)",
             f"- Detector is read-only: no source file was modified.",
             f"- **Verdict: {verdict}** ({len(self.findings)} findings)", "",
             "## Summary per family (booklet Table 19.1)", "", "| Family | Findings |", "|---|---|"]
        L += [f"| {fam} | {by_fam.get(fam, 0)} |" for fam in FAMILIES]
        L += ["", "## Findings", ""]
        if self.findings:
            L += ["| ID | Family | PDF page | Printed page | File:line | Text | Rule | Class |",
                  "|---|---|---|---|---|---|---|---|"]
            for i, f in enumerate(self.findings, start=1):
                txt = str(f.text).replace("|", "\\|").replace("\n", " ")[:120]
                L.append(f"| QA-{i:03d} | {f.family} | {f.page or '—'} | {printed_page(f.page)} | "
                         f"{f.loc or '—'} | `{txt}` | {f.rule} | **{f.cls}** |")
        else:
            L.append("No findings.")
        L += ["", "## Notes", ""] + [f"- {n}" for n in self.notes]
        L += ["", "## Visual pass (manual, booklet §14.5 / §19.4)", "",
              "Inspect the renders for: a heading in the bottom quarter of a page, a split box or table, "
              "something touching the page edge, a large gap inside a line, mirrored headers/footers, "
              "overlapping labels. Record visual findings below with page numbers.", ""]
        out.write_text("\n".join(L) + "\n", encoding="utf-8")
        return out

    def run_all(self) -> Path:
        self.check_tree()
        self.check_template()
        self.check_log()
        if self.load_pdf():
            self.check_cover()
            self.check_pdf_text()
            self.check_pagination()
        self.check_bib_and_labels()
        self.render_pages()
        self.classify()
        return self.write()


def main():
    ap = argparse.ArgumentParser(description="Read-only QA detector for the AuraTwin AI report "
                                             "(writes <report-dir>/work/qa_audit_report.md).")
    ap.add_argument("--report-dir", default="report", help="LaTeX project folder (default: report)")
    ap.add_argument("--key-pages", default="", help="comma-separated PDF pages to render at 110 dpi")
    ap.add_argument("--no-render", action="store_true", help="skip page rendering")
    ap.add_argument("--no-layout", action="store_true", help="extract text without pdftotext -layout")
    a = ap.parse_args()
    rd = Path(a.report_dir).resolve()
    keys = [int(x) for x in a.key_pages.split(",") if x.strip().isdigit()]
    d = Detector(rd, render=not a.no_render, key_pages=keys, use_layout=not a.no_layout)
    out = d.run_all()
    verdict = "PASS" if not d.findings else "FAIL"
    print(f"QA detector: {len(d.findings)} findings -> {verdict}. Report: {out}")
    counts = defaultdict(int)
    for f in d.findings:
        counts[f.rule_id] += 1
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
