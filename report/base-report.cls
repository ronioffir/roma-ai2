%% ============================================================================
%% base-report.cls  --  Hebrew/English (RTL/LTR) report class for LuaLaTeX
%% ----------------------------------------------------------------------------
%% Layer 1 of 2 ("the factory"): languages, fonts, BiDi units, structure,
%% styled tables, four box types, page style, needspace discipline.
%% Company layers (e.g. auratwin-report.cls) load this class and only add
%% branding + document fields. NEVER copy or edit this file inside a layer.
%%
%% Compile:  lualatex -> biber -> lualatex -> lualatex   (MiKTeX, LuaHBTeX)
%% Version history: see ../CHANGELOG.md   Command list: COMMANDS.md
%% ============================================================================
\NeedsTeXFormat{LaTeX2e}
\def\basereport@version{1.2.1}
\def\basereport@date{2026/11/16}
\ProvidesClass{base-report}[2026/11/16 v1.2.1 Hebrew/English LuaLaTeX report base class]

\RequirePackage{iftex}
\ifluatex\else
  \ClassError{base-report}{This class requires LuaLaTeX}{Compile with lualatex.}
\fi

%% ---------------------------------------------------------------- options --
\newif\ifbasereport@draft
\DeclareOption{draft}{\basereport@drafttrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass[12pt,a4paper,oneside]{report}

%% ======================================================= STAGE 1: skeleton --
%% Page geometry (booklet Table 11.1): 2.5 cm on every side + 0.5 cm binding
%% gutter. In a Hebrew (RTL) document the binding edge is the RIGHT edge.
\RequirePackage[a4paper,top=2.5cm,bottom=2.5cm,left=2.5cm,right=3.0cm,
                headheight=15pt,headsep=0.6cm,footskip=1.0cm]{geometry}
\RequirePackage{setspace}
\onehalfspacing
\RequirePackage{amsmath,amssymb}
\RequirePackage{fontspec}
\RequirePackage{polyglossia}
\setdefaultlanguage{hebrew}
\setotherlanguage{english}

%% Fonts -- checked with `fc-list :lang=he` (Windows: David, Arial; Times New Roman)
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Consolas}[Scale=0.92]
\newfontfamily\hebrewfont{David}[Script=Hebrew,
    BoldFont={David Bold},
    ItalicFont={David}, ItalicFeatures={FakeSlant=0.15},
    BoldItalicFont={David Bold}, BoldItalicFeatures={FakeSlant=0.15}]
\newfontfamily\hebrewfontsf{Arial}[Script=Hebrew]
\newfontfamily\hebrewfonttt{Consolas}[Scale=0.92]
\newfontfamily\englishfont{Times New Roman}[Ligatures=TeX]   % v1.2.0: "--" -> en dash
\newfontfamily\englishfontsf{Arial}[Ligatures=TeX]
\newfontfamily\headingfont{Arial}[Script=Hebrew]

\RequirePackage[table,svgnames]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{etoolbox}
\RequirePackage{needspace}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,shapes.misc,calc,
                fit,backgrounds,shadows,decorations.pathreplacing,patterns}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{polar,groupplots}
\RequirePackage{tabularx,booktabs,colortbl,array,multirow,makecell}
\RequirePackage[most]{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{float}
\RequirePackage{lastpage}
\RequirePackage{multicol}

%% Default (neutral) palette -- a company layer overrides these names.
\definecolor{brandprimary}{HTML}{2E3A59}
\definecolor{brandsecondary}{HTML}{1A8C8C}
\definecolor{brandaccent}{HTML}{D99A1E}
\definecolor{brandtint}{HTML}{EEF1F6}
\definecolor{brandwarn}{HTML}{C8423B}
\definecolor{brandexample}{HTML}{3949AB}
\definecolor{brandtext}{HTML}{1B1B1F}
\definecolor{brandmuted}{HTML}{6B7280}

%% ===================================================== STAGE 2: BiDi units --
%% \en{...}     one LTR English unit (word, acronym, multi-word phrase).
%%              Never put Hebrew inside it.
%% \num{...}    one unbreakable LTR numeric unit: 1.0, 10--20, 85\%, \$2,200, 35 ms.
%% \hebmath{.}  Hebrew text inside math mode.
%% \heb{...}    Hebrew label inside an English (LTR) environment (e.g. TikZ).
%% \copyrightsign  (c) always set in the English font (David lacks the glyph).
%% v1.2.0 fix: \en is BOXED. With an unboxed \textenglish, a comma typed after
%% an English unit attached to the NEXT English unit ("SMPL-XRAG" bug found by
%% tests/bidi_comma_test.tex). \enlong is the unboxed, line-breakable variant
%% for long English phrases (titles) that are not followed by list punctuation.
\newcommand{\en}[1]{\mbox{\textenglish{#1}}}
\newcommand{\enlong}[1]{\textenglish{#1}}
\newcommand{\num}[1]{\mbox{\textenglish{#1}}}
\newcommand{\hebmath}[1]{\text{\texthebrew{#1}}}
\newcommand{\heb}[1]{\texthebrew{#1}}
\newcommand{\copyrightsign}{\textenglish{\textcopyright}}
\newcommand{\hq}[1]{\char"0022#1\char"0022}   % Hebrew quotation marks (straight)
%% Numbers that LaTeX itself generates (section, figure, page) are forced LTR,
%% so "1.2" never displays as "2.1" -- also inside the TOC and the lists.
\newcommand{\basereport@LTRnum}[1]{\LR{#1}}

%% ================================================ STAGE 3: structure, TOC --
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}   % chapter / section / subsection = 3 levels in the TOC

\renewcommand{\thechapter}{\arabic{chapter}}
\renewcommand{\thesection}{\basereport@LTRnum{\arabic{chapter}.\arabic{section}}}
\renewcommand{\thesubsection}{\basereport@LTRnum{\arabic{chapter}.\arabic{section}.\arabic{subsection}}}
\renewcommand{\thefigure}{\basereport@LTRnum{\arabic{chapter}.\arabic{figure}}}
\renewcommand{\thetable}{\basereport@LTRnum{\arabic{chapter}.\arabic{table}}}
\renewcommand{\theequation}{\basereport@LTRnum{\arabic{chapter}.\arabic{equation}}}

\titleformat{\chapter}[hang]
  {\headingfont\bfseries\fontsize{22}{26}\selectfont\color{brandprimary}}
  {\tikz[baseline=(n.base)]\node[fill=brandprimary,text=white,rounded corners=3pt,
      inner sep=5pt,minimum width=1.1cm,font=\headingfont\bfseries\fontsize{20}{24}\selectfont]
      (n){\thechapter};}
  {0.45cm}{}
  [\vspace{2pt}{\color{brandsecondary}\titlerule[1.4pt]}]
\titlespacing*{\chapter}{0pt}{-38pt}{14pt}
\titleformat{\section}
  {\headingfont\bfseries\fontsize{15}{18}\selectfont\color{brandprimary}}
  {\thesection}{0.6em}{}
\titlespacing*{\section}{0pt}{10pt plus 3pt minus 2pt}{4pt plus 1pt}
\titleformat{\subsection}
  {\headingfont\bfseries\fontsize{12.5}{15}\selectfont\color{brandsecondary}}
  {\thesubsection}{0.6em}{}
\titlespacing*{\subsection}{0pt}{7pt plus 2pt minus 2pt}{2pt plus 1pt}

%% Orphan-heading discipline (booklet 19.4): never leave a heading in the
%% bottom part of a page without room for text after it.
\AtBeginDocument{%
  \pretocmd{\section}{\needspace{6\baselineskip}}{}{}%
  \pretocmd{\subsection}{\needspace{5\baselineskip}}{}{}}

%% TOC / LoF / LoT appearance: compact, single spaced, page numbers LTR.
\titlecontents{chapter}[0pt]{\addvspace{3pt}\bfseries\color{brandprimary}}
  {\contentslabel[\thecontentslabel]{1.6em}}{}{\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{section}[1.6em]{}{\contentslabel[\thecontentslabel]{2.3em}}{}
  {\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{subsection}[3.9em]{}{\contentslabel[\thecontentslabel]{3.0em}}{}
  {\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{figure}[0pt]{}{\contentslabel[\thecontentslabel]{2.4em}}{}
  {\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{table}[0pt]{}{\contentslabel[\thecontentslabel]{2.4em}}{}
  {\titlerule*[0.5pc]{.}\contentspage}

%% Preliminary pages numbered with Hebrew letters (cover shows no number).
\newcommand{\basereport@hebalph}[1]{\texthebrew{\ifcase#1\or א׳\or ב׳\or ג׳\or ד׳\or ה׳\or ו׳\or ז׳\or ח׳\else\number#1\fi}}
\def\@hebalph#1{\basereport@hebalph{#1}}
\newcommand{\frontmatterpages}{\clearpage\pagenumbering{hebalph}\setcounter{page}{1}}
\newcommand{\mainmatterpages}{\clearpage\pagenumbering{arabic}\setcounter{page}{1}%
  \gdef\basereport@inbody{1}}
\gdef\basereport@inbody{0}

%% Compact preliminary pages (booklet Table 1.1: TOC = page ג׳, lists = page ד׳).
%% \compacttoc     -- TOC on one page, depth 3 (chapter/section/subsection).
%% \compactlists{<abbreviations>} -- LoF + LoT + abbreviation table on one page.
\newcommand{\basereport@minihead}[1]{\par\addvspace{4pt}%
  {\headingfont\bfseries\large\color{brandprimary}#1\par}%
  {\color{brandsecondary}\rule{\linewidth}{0.8pt}\par}\addvspace{2pt}}
\newcommand{\compacttoc}[1][תוכן עניינים]{%
  \chapter*{#1}\markboth{#1}{}%
  {\footnotesize\setstretch{0.95}\setlength{\parskip}{0pt}\let\addvspace\@gobble
   \@starttoc{toc}}}% v1.2.1: one page (no inter-chapter gaps)
\newcommand{\compactlists}[1]{%
  \chapter*{רשימות איורים, טבלאות וקיצורים}\markboth{רשימות}{}%
  {\scriptsize\setstretch{1.08}\setlength{\parskip}{0pt}% v1.2.1: one page
   \let\basereport@addvspace\addvspace\let\addvspace\@gobble
   \basereport@minihead{רשימת איורים}\@starttoc{lof}%
   \basereport@minihead{רשימת טבלאות}\@starttoc{lot}%
   \basereport@minihead{קיצורים ומונחים (סדר אלפביתי)}#1}}
%% Abbreviation table: \begin{abbrevtable} \abbr{CAGR}{...} ... \end{abbrevtable}
\newcommand{\abbr}[2]{\par\hangindent=1.55cm\hangafter=1\noindent
  \makebox[1.5cm][s]{\mbox{\textenglish{\textbf{#1}}}\hfill}#2\par}
\newenvironment{abbrevtable}{%
  \par\setlength{\columnsep}{16pt}\setlength{\parskip}{0.6pt}%
  \let\en\enlong   % expansions must wrap inside a narrow column
  \begin{multicols}{2}}{\end{multicols}}

%% Captions: table caption ABOVE, figure caption BELOW (booklet Table 11.1).
\RequirePackage[font={small,singlespacing},labelfont={bf,color=brandprimary},
  labelsep=colon,justification=centering,skip=5pt]{caption}
\captionsetup[table]{position=above}
\captionsetup[figure]{position=below}

%% Floats: keep figures/tables near their reference; never across chapters.
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.75}
\setcounter{topnumber}{3}\setcounter{bottomnumber}{2}\setcounter{totalnumber}{4}
\setlength{\textfloatsep}{10pt plus 3pt minus 3pt}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}

%% Lists
\setlist{itemsep=1pt,topsep=3pt,parsep=0pt,leftmargin=*}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt plus 1pt}
\emergencystretch=2em
\clubpenalty=10000 \widowpenalty=10000 \displaywidowpenalty=10000

%% ======================================= STAGE 4: tables, boxes, figures --
%% Maximum width of every table and figure: 12.4 cm (booklet 19.3).
\newlength{\maxobjwidth}\setlength{\maxobjwidth}{12.4cm}
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}   % RTL text column (first column on the right)
\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\newcolumntype{C}{>{\centering\arraybackslash}X}
\newcolumntype{P}[1]{>{\raggedleft\arraybackslash}p{#1}}
\newcolumntype{Q}[1]{>{\centering\arraybackslash}p{#1}}
\setlength{\arrayrulewidth}{0.4pt}
\renewcommand{\arraystretch}{1.18}

%% \begin{reporttable}{<caption>}{<label>}{<tabularx colspec>}
%%   \headrow \hc{A} & \hc{B} & \hc{C} \\ \midrule  rows...  \end{reporttable}
%% In RTL the FIRST column of the colspec is printed on the RIGHT, natively.
%% NOTE (v1.2.0 fix): tabularx scans for \end{<current environment>}, so the
%% float/center are opened with \table/\center (command form), which keeps
%% \@currenvir = reporttable.
%% Optional first argument: font size of the table body (default \small).
\newenvironment{reporttable}[4][\small]{%
  \table[!htbp]\centering#1\setstretch{1.0}%
  \caption{#2}\label{#3}%
  \rowcolors{2}{brandtint}{white}\setlength{\tabcolsep}{4pt}% v1.2.1: 6pt->4pt (narrow-column overflow)
  \tabularx{\maxobjwidth}{#4}\toprule
}{%
  \bottomrule\endtabularx\endtable}
%% Variant without float (for use inside boxes or when exact placement is needed)
\newenvironment{reporttable*}[4][\small]{%
  \par\needspace{8\baselineskip}\center#1\setstretch{1.0}%
  \captionof{table}{#2}\label{#3}%
  \rowcolors{2}{brandtint}{white}\setlength{\tabcolsep}{4pt}% v1.2.1: 6pt->4pt (narrow-column overflow)
  \tabularx{\maxobjwidth}{#4}\toprule
}{%
  \bottomrule\endtabularx\endcenter}
%% Header row:  \headrow \hc{A} & \hc{B} & \hc{C} \\ \midrule
\newcommand{\hc}[1]{\textcolor{white}{\headingfont\bfseries #1}}
\newcommand{\headrow}{\rowcolor{brandprimary}}
\newcommand{\hlrow}{\rowcolor{brandsecondary!18}}
\newcommand{\cellok}{\textcolor{brandsecondary}{\ensuremath{\bullet}}}
\newcommand{\cellpartial}{\textcolor{brandaccent}{\ensuremath{\circ}}}
\newcommand{\cellno}{\textcolor{brandmuted}{---}}

%% Figures: every TikZ/pgfplots picture goes through an English (LTR) wrapper,
%% so coordinates and axes never mirror. Hebrew labels use \heb{...}.
%% \begin{reportfigure}{<caption>}{<label>} <tikz/pgfplots> \end{reportfigure}
\newenvironment{reportfigure}[2]{%
  \def\basereport@figcap{#1}\def\basereport@figlab{#2}%
  \begin{figure}[!htbp]\centering\begin{english}\centering\setstretch{1.0}%
}{%
  \end{english}\caption{\basereport@figcap}\label{\basereport@figlab}\end{figure}}
\newenvironment{reportfigure*}[2]{%
  \def\basereport@figcap{#1}\def\basereport@figlab{#2}%
  \par\needspace{10\baselineskip}\begin{center}\begin{english}\centering\setstretch{1.0}%
}{%
  \end{english}\captionof{figure}{\basereport@figcap}\label{\basereport@figlab}\end{center}}

%% Four box types (tcolorbox). breakable=false: a box never splits.
\tcbset{basereport/.style={enhanced,breakable=false,arc=2pt,
    left=8pt,right=8pt,top=5pt,bottom=5pt,boxsep=0pt,
    fonttitle=\headingfont\bfseries\small,
    before skip=7pt,after skip=7pt,
    before upper={\setstretch{1.15}\setlength{\parskip}{3pt}}}}
%% 1. managerbox -- "Why it matters to a manager" (gold/amber header)
\newtcolorbox{managerbox}[1][למה זה חשוב למנהל]{basereport,
  colback=brandaccent!8,colframe=brandaccent,coltitle=black,
  colbacktitle=brandaccent!55,title={#1},boxrule=0.8pt,toptitle=2pt,bottomtitle=2pt,
  before={\par\needspace{5\baselineskip}}}
%% 2. keymessagebox -- teal bar on the right edge (RTL reading start)
\newtcolorbox{keymessagebox}[1][המסר המרכזי]{basereport,
  colback=brandsecondary!8,colframe=brandsecondary!8,boxrule=0pt,
  borderline east={4pt}{0pt}{brandsecondary},
  fontupper=\small,
  before upper={\setstretch{1.15}{\headingfont\bfseries\color{brandsecondary}#1:}\ },
  before={\par\needspace{4\baselineskip}}}
%% 3. warningbox -- engineering trap (red/coral)
\newtcolorbox{warningbox}[1][מלכודת הנדסית]{basereport,
  colback=brandwarn!6,colframe=brandwarn!6,boxrule=0pt,
  borderline east={4pt}{0pt}{brandwarn},fontupper=\small,
  before upper={\setstretch{1.15}{\headingfont\bfseries\color{brandwarn}#1:}\ },
  before={\par\needspace{4\baselineskip}}}
%% 4. examplebox -- application inside the system (royal blue / indigo)
\newtcolorbox{examplebox}[1][יישום במערכת]{basereport,
  colback=brandexample!6,colframe=brandexample,boxrule=0.6pt,
  colbacktitle=brandexample,coltitle=white,title={#1},fontupper=\small,
  toptitle=2pt,bottomtitle=2pt,before={\par\needspace{5\baselineskip}}}
%% Code box: always LTR (wrap the call in \begin{english} ... \end{english}).
\newtcblisting{codebox}[1][]{enhanced,breakable=false,listing only,arc=2pt,
  colback=black!3,colframe=black!25,boxrule=0.5pt,left=6pt,right=6pt,
  listing options={basicstyle=\ttfamily\footnotesize,columns=fullflexible,
     breaklines=true,showstringspaces=false},#1}

%% ===================================== STAGE 5: header/footer, page count --
\RequirePackage{fancyhdr}
\newcommand{\basereport@headleft}{}
\newcommand{\basereport@headright}{}
\newcommand{\setheadleft}[1]{\renewcommand{\basereport@headleft}{#1}}
\newcommand{\setheadright}[1]{\renewcommand{\basereport@headright}{#1}}
%% In RTL, fancyhdr's "R" slot is the reading start. Every slot sets its own
%% direction explicitly (booklet Table 14.3: header reversed on some pages).
\fancypagestyle{basereport}{%
  \fancyhf{}%
  \fancyhead[R]{\small\color{brandmuted}\texthebrew{\leftmark}}%
  \fancyhead[L]{\small\color{brandmuted}\basereport@headleft}%
  \fancyfoot[C]{\small\color{brandmuted}\basereport@pagelabel}%
  \fancyfoot[R]{\scriptsize\color{brandmuted}\basereport@headright}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\headrule}{{\color{brandsecondary!60}\hrule height\headrulewidth}}%
  \renewcommand{\footrulewidth}{0pt}}
\fancypagestyle{plain}{%
  \fancyhf{}\fancyfoot[C]{\small\color{brandmuted}\basereport@pagelabel}%
  \fancyfoot[R]{\scriptsize\color{brandmuted}\basereport@headright}%
  \renewcommand{\headrulewidth}{0pt}}
%% "page N of M" reads right-to-left in Hebrew; numbers are LTR units.
%% M = last page of the body (label placed by \bodyend).
\newcommand{\basereport@pagelabel}{%
  \ifnum\basereport@inbody=1\relax
    \texthebrew{עמוד \num{\thepage} מתוך \num{\pageref*{basereport@bodyend}}}%
  \else\texthebrew{\thepage}\fi}
\newcommand{\bodyend}{\label{basereport@bodyend}}
\renewcommand{\chaptermark}[1]{\markboth{\thechapter.\ #1}{}}
\pagestyle{basereport}

%% Every chapter, the TOC and the bibliography start on a new page.
\pretocmd{\chapter}{\clearpage}{}{}

%% ======================================== STAGE 6: bibliography, metadata --
\RequirePackage[backend=biber,style=ieee,sorting=none,maxnames=6,minnames=3,
  doi=true,url=false,isbn=false,dashed=false]{biblatex}
%% Citations are LTR units inside Hebrew sentences: "[3]", "[4]--[6]".
\AtBeginDocument{\let\basereport@origcite\cite
  \renewcommand{\cite}[1]{\mbox{\textenglish{\basereport@origcite{#1}}}}}
\newcommand{\printreferences}[1][מקורות]{%
  \chapter*{#1}\addcontentsline{toc}{chapter}{#1}\markboth{#1}{}%
  \begin{english}\footnotesize\setstretch{1.0}%
  \setlength{\bibitemsep}{1.2pt}\setlength{\biblabelsep}{6pt}%
  \printbibliography[heading=none]\end{english}}
%% v1.2.1: bibliography set in \footnotesize, single spacing -- the 3-page
%% budget of booklet Table 1.1 for ~45 IEEE entries (detector finding QA-034).

\RequirePackage[hidelinks,bookmarksnumbered,pdfencoding=auto,
  hypertexnames=false]{hyperref}
\newcommand{\templateversion}{\num{v\basereport@version}}
\endinput
