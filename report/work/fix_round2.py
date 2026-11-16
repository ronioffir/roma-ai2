r"""QA fixer, red-team round 2 (new issues N1-N6 + market numbers after aligning try-ons/session).
Every replacement must match exactly the expected number of times, otherwise the script stops."""
import io, sys

ROOT = "C:/Users/Ella/roma-ai2/"
EDITS = {
    "report/chapters/ch4_market.tex": [
        (r"\en{SOM} $\approx$ \$27.6M", r"\en{SOM} $\approx$ \$27.4M", 1),
        (r"בכ-\num{\$27.6M}", r"בכ-\num{\$27.4M}", 1),
        (r"\num{6} סשנים $\times$ \num{2} הדמיות $\times$ מחציתן דרך מודעה $\times$ \num{\$0.015} $=$ \num{\$0.09}",
         r"\num{6} סשנים $\times$ \num{1.7} הדמיות $\times$ מחציתן דרך מודעה $\times$ \num{\$0.015} $=$ \num{\$0.08}", 1),
        (r"בסך הכול \num{\$0.69} לחודש", r"בסך הכול \num{\$0.68} לחודש", 1),
        (r"\num{150M} פעילות $\times$ \num{\$0.69} $\times$ \num{12} & \num{\$1.24B}",
         r"\num{150M} פעילות $\times$ \num{\$0.68} $\times$ \num{12} & \num{\$1.22B}", 1),
        (r"\num{1.6M} פעילות $\times$ \num{\$0.69} $\times$ \num{12} & \num{\$13.2M}",
         r"\num{1.6M} פעילות $\times$ \num{\$0.68} $\times$ \num{12} & \num{\$13.0M}", 1),
        (r"\textbf{\num{\$27.6M}}", r"\textbf{\num{\$27.4M}}", 1),
        (r"הטבלה מראה שה-\en{SOM} נשען כמעט שווה בשווה על שני ערוצים בלתי תלויים, ולכן כשל של ערוץ אחד אינו מבטל את המודל.",
         r"הטבלה מראה שה-\en{SOM} נשען כמעט שווה בשווה על שני ערוצים בלתי תלויים, ולכן כשל של ערוץ אחד אינו מבטל את המודל. "
         r"ההבדל במחיר לקמעונאית מכוון: ב-\en{SAM} נלקח רישוי ממוצע של \num{\$0.6M} לקמעונאית בינונית, ואילו ב-\en{SOM} נבחרו \num{12} קמעונאיות מהשורה הראשונה, שהתמחור שלהן לפי הזמנה מגיע ל-\num{\$1.2M}. "
         r"גם שיעורי ההמרה שונים בכוונה: \num{4\%} רכישה לאחר לחיצה על המלצה שהמשתמשת בחרה, מול \num{1.8\%} לאחר לחיצה שנעשתה רק כדי לפתוח את שער ההדמיה (סעיף~\ref{sec:unit}). "
         r"מנוי הפרימיום הוא ערוץ שלישי, שמשמש גם תוכנית מגירה לסיכון \en{RSK-BIZ-04}.", 1),
    ],
    "report/chapters/ch8_summary.tex": [
        (r"\en{SOM} של כ-\num{\$27.6M}", r"\en{SOM} של כ-\num{\$27.4M}", 1),
    ],
    "report/coverpage.tex": [
        (r"נאמד בכ-\num{\$27.6M}", r"נאמד בכ-\num{\$27.4M}", 1),
        (r"כל מספר בדוח מופק מקוד שזמין במאגר הציבורי של הפרויקט, ולכן ניתן לשחזר אותו ולבדוק אותו.",
         r"כל התוצאות המחושבות בדוח, מהסימולציה ועד מטריצת ההחלטה, מופקות מקוד שזמין במאגר הציבורי של הפרויקט, ולכן ניתן לשחזר ולבדוק אותן.", 1),
    ],
    "report/chapters/ch2_problem.tex": [
        (r"הניסוח & שאלה והשערה \en{$H_1$} &", r"הניסוח & שאלה ושתי השערות, $H_{1a}$ ו-$H_{1b}$ &", 1),
        (r"הוכחת הצלחה & דחיית \en{$H_0$} ב-\num{$\alpha = 0.05$}, \num{$n = 120$} &",
         r"הוכחת הצלחה & דחיית $H_{0a}$ ו-$H_{0b}$ (הולם), \num{$n = 120$} &", 1),
    ],
    "report/chapters/ch5_alternatives.tex": [
        (r"בבדיקת הצוות האדום התברר ששני ציונים לא תאמו את הסולם, והם תוקנו:",
         r"בבדיקה חוזרת של הציונים מול הסולמות התברר ששניים מהם לא תאמו, והם תוקנו:", 1),
        (r"והיא נבחנת בהשערה $H_1$.", r"והיא נבחנת בהשערות $H_{1a}$ ו-$H_{1b}$.", 1),
    ],
    "report/chapters/ch3_literature.tex": [
        (r"מאפשר פילוח ציפורניים שעומד ביעד \num{$\text{IoU} \ge 0.94$} של \en{REQ-HND-04}",
         r"מאפשר פילוח ציפורניים שעומד ביעד \num{$\text{IoU} \ge 0.90$} של \en{REQ-HND-04}, ואולי אף ביעד השאפתני של \num{0.94}", 1),
    ],
    "README.md": [("SOM ≈ $27.6M", "SOM ≈ $27.4M", 1)],
    "PRD.md": [("ARPU $0.69/month, SAM ≈ $3.0B, SOM ≈ $27.6M", "ARPU $0.68/month, SAM ≈ $3.0B, SOM ≈ $27.4M", 1)],
    "report/work/source_verification_checklist.md": [
        (r"SOM ≈ \$27.6M", r"SOM ≈ \$27.4M", 1),
        (r"× \$0.69 × 12", r"× \$0.68 × 12", 2),
        (r"\$0.09 ads + \$0.30 premium = \$0.69", r"\$0.08 ads + \$0.30 premium = \$0.68", 1),
    ],
}
ok = True
for f, reps in EDITS.items():
    p = ROOT + f
    s = io.open(p, encoding="utf-8").read()
    for old, new, n in reps:
        c = s.count(old)
        if c != n:
            print(f"MISMATCH {f}: expected {n}, found {c}: {old[:70]}")
            ok = False
            continue
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
print("done" if ok else "done with mismatches")
