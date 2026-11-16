%% ============================================================================
%% auratwin-report.cls -- THIN company layer for AuraTwin AI documents
%% ----------------------------------------------------------------------------
%% Loads base-report.cls unchanged and adds ONLY: brand palette, logo,
%% document fields, document types, cover page, header/footer texts.
%% Document types (class options): report (default) | proposal | spec
%% ============================================================================
\NeedsTeXFormat{LaTeX2e}
\def\auratwin@version{1.3.0}
\ProvidesClass{auratwin-report}[2026/11/16 v1.3.0 AuraTwin AI company layer]

\def\auratwin@doctype{report}
\DeclareOption{report}{\def\auratwin@doctype{report}}
\DeclareOption{proposal}{\def\auratwin@doctype{proposal}}
\DeclareOption{spec}{\def\auratwin@doctype{spec}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{base-report}}
\ProcessOptions\relax
\LoadClass{base-report}

%% ------------------------------------------------------------ brand palette --
%% "Luxury, Vintage, Bold" palette (v1.3.0, skill luxury-vintage-ui-designer).
%% These six colours (and their tints/shades) are the ONLY colours in the document.
%% Changing one value here recolours headings, boxes, tables, headers and charts.
\definecolor{auraEggNog}{HTML}{FBEDC3}        % 251,237,195 soft backgrounds, cards, logo field
\definecolor{auraMustard}{HTML}{CCB363}       % 204,179, 99 antique-gold rules, frames, highlights
\definecolor{auraDust}{HTML}{6F7D7B}          % 111,125,123 sub-headings, system boxes, axes
\definecolor{auraCopper}{HTML}{C27E35}        % 194,126, 53 examples, proposed solution, milestones path
\definecolor{auraGarnet}{HTML}{76290B}        % 118, 41, 11 warnings, critical risks, critical path
\definecolor{auraVelvetForest}{HTML}{1E3226}  %  30, 50, 38 chapter titles, cover, table headers
%% semantic names used by base-report.cls and by every chapter
\colorlet{brandprimary}{auraVelvetForest}
\colorlet{brandsecondary}{auraDust}
\colorlet{brandaccent}{auraMustard}
\colorlet{brandcream}{auraEggNog}
\colorlet{brandtint}{auraEggNog!45!white}
\colorlet{brandwarn}{auraGarnet}
\colorlet{brandexample}{auraCopper}
\colorlet{brandhighlight}{auraCopper}
\colorlet{brandmuted}{auraDust!80!auraVelvetForest}
\colorlet{brandgreen}{auraVelvetForest!85!auraDust}
\colorlet{brandgrey}{auraDust!60!white}

%% ------------------------------------------------------------------- logo --
%% Three interlocking arches from the palette card: Egg Nog top-left arch,
%% Mustard inverted-U dome (centre), Dust top-right arch; a Velvet Forest
%% eye/prism line across them symbolises biometric calibration.
\newcommand{\auratwin@mark}{%
    \fill[auraEggNog] (0,0) -- (0,0.42) arc[start angle=180,end angle=90,radius=0.58] -- (0.58,0) -- cycle;
    \fill[auraDust] (1.42,0) -- (1.42,1.0) arc[start angle=90,end angle=0,radius=0.58] -- (2.0,0) -- cycle;
    \fill[auraMustard,opacity=0.95] (0.5,1.0) -- (0.5,0.5) arc[start angle=180,end angle=360,radius=0.5] -- (1.5,1.0) -- cycle;
    \draw[auraVelvetForest,line width=0.9pt] (0.42,0.55) .. controls (0.75,0.86) and (1.25,0.86) .. (1.58,0.55)
          .. controls (1.25,0.24) and (0.75,0.24) .. (0.42,0.55) -- cycle;
    \fill[auraVelvetForest] (1.0,0.55) circle (0.13);
    \fill[auraEggNog] (1.04,0.59) circle (0.035);
    \draw[auraVelvetForest,line width=0.5pt] (0.0,-0.06) -- (2.0,-0.06);}
\newcommand{\auratwinlogo}[1][1]{%
  \begin{tikzpicture}[scale=#1,baseline=0pt]\auratwin@mark\end{tikzpicture}}
\newcommand{\auratwinwordmark}[1][1]{%
  \begin{tikzpicture}[scale=#1,baseline=(current bounding box.south)]
    \auratwin@mark
    \node[anchor=north,font=\fontsize{13}{15}\selectfont\headingfont,text=auraVelvetForest] at (1.0,-0.14)
      {\textenglish{AuraTwin\,\textcolor{auraCopper}{AI}}};
  \end{tikzpicture}}

%% ------------------------------------------------------- document fields --
%% Each field is its own command; nothing is hard-coded in the cover.
\newcommand{\auratwin@field}[2]{\expandafter\def\csname auratwin@#1\endcsname{#2}}
\newcommand{\docfield}[1]{\csname auratwin@#1\endcsname}
\newcommand{\doctitlehe}[1]{\auratwin@field{titlehe}{#1}}
\newcommand{\doctitleen}[1]{\auratwin@field{titleen}{#1}}
\newcommand{\docshorttitle}[1]{\auratwin@field{short}{#1}}
\newcommand{\docgroup}[1]{\auratwin@field{group}{#1}}
\newcommand{\docinstitution}[1]{\auratwin@field{inst}{#1}}
\newcommand{\doccourse}[1]{\auratwin@field{course}{#1}}
\newcommand{\docauthors}[1]{\auratwin@field{authors}{#1}}
\newcommand{\docauthorsshort}[1]{\auratwin@field{authorsshort}{#1}}
\newcommand{\docadvisor}[1]{\auratwin@field{advisor}{#1}}
\newcommand{\docpartner}[1]{\auratwin@field{partner}{#1}}
\newcommand{\docdate}[1]{\auratwin@field{date}{#1}}
\newcommand{\docversion}[1]{\auratwin@field{version}{#1}}
\newcommand{\doccoverimage}[1]{\auratwin@field{cover}{#1}}
\doctitlehe{}\doctitleen{}\docshorttitle{AuraTwin AI}\docgroup{}\docinstitution{}
\doccourse{}\docauthors{}\docauthorsshort{}\docadvisor{}\docpartner{}
\docdate{\today}\docversion{1.0}\doccoverimage{}

\newcommand{\auratwin@typename}{%
  \ifdefstring{\auratwin@doctype}{proposal}{הצעת פרויקט}{%
  \ifdefstring{\auratwin@doctype}{spec}{מסמך אפיון}{דוח מכין}}}
\newcommand{\auratwin@typenameen}{%
  \ifdefstring{\auratwin@doctype}{proposal}{Project Proposal}{%
  \ifdefstring{\auratwin@doctype}{spec}{Specification}{Preliminary Design Report}}}

%% Header / footer texts (directions are fixed inside every slot).
\AtBeginDocument{%
  \setheadleft{\raisebox{-1pt}{\auratwinlogo[0.17]}\ \en{\docfield{short}}\ \textbar\ \texthebrew{\auratwin@typename}\ \textbar\ \en{\docfield{group}}}%
  \setheadright{\copyrightsign\ \num{\the\year}\ \texthebrew{\docfield{authorsshort}}}}

%% ------------------------------------------------- editorial chapter opening --
%% Luxury tech-fashion journal look: chapter number in a Velvet Forest badge
%% with a Mustard ring, title in Velvet Forest, double rule Mustard + Dust.
\titleformat{\chapter}[hang]
  {\headingfont\bfseries\fontsize{22}{27}\selectfont\color{auraVelvetForest}}
  {\tikz[baseline=(n.base)]{\node[circle,fill=auraVelvetForest,draw=auraMustard,line width=1.6pt,
      text=auraEggNog,inner sep=2pt,minimum size=1.15cm,font=\headingfont\bfseries\fontsize{19}{22}\selectfont]
      (n){\thechapter};}}
  {0.5cm}{}
  [\vspace{3pt}{\color{auraMustard}\titlerule[1.6pt]}\vspace{1.6pt}{\color{auraDust}\titlerule[0.5pt]}]
\titleformat{\section}
  {\headingfont\bfseries\fontsize{15}{18}\selectfont\color{auraVelvetForest}}
  {\textcolor{auraCopper}{\thesection}}{0.6em}{}
\titleformat{\subsection}
  {\headingfont\bfseries\fontsize{12.5}{15}\selectfont\color{auraDust!85!black}}
  {\thesubsection}{0.6em}{}

%% ------------------------------------------------------------- cover page --
%% Egg Nog field, Velvet Forest double frame with a Mustard inner rule, logo,
%% banner, Hebrew + English titles, document type, team, advisor, date,
%% copyright in the English font, NO visible page number.
\newcommand{\makecoverpage}{%
  \clearpage\begingroup\thispagestyle{empty}%
  \begin{english}%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[auraEggNog!55!white] (current page.south west) rectangle (current page.north east);
    \draw[auraVelvetForest,line width=2.8pt]
      ([xshift=1.2cm,yshift=-1.2cm]current page.north west) rectangle
      ([xshift=-1.2cm,yshift=1.2cm]current page.south east);
    \draw[auraMustard,line width=1.0pt]
      ([xshift=1.45cm,yshift=-1.45cm]current page.north west) rectangle
      ([xshift=-1.45cm,yshift=1.45cm]current page.south east);
    \node[anchor=north] at ([yshift=-1.75cm]current page.north) {\auratwinwordmark[0.62]};
  \end{tikzpicture}%
  \end{english}\par   % v1.3.0 fix: end the overlay's paragraph so \vspace* applies before the text
  \centering\setstretch{1.1}%
  \vspace*{0.55cm}%
  {\headingfont\small\color{auraDust!85!black}\docfield{inst}\par}%
  \vspace{1pt}{\headingfont\small\color{auraDust!85!black}\docfield{course}\par}%
  \vspace{6pt}%
  \ifx\auratwin@cover\@empty\else
    {\setlength{\fboxsep}{0pt}\color{auraMustard}\fbox{\includegraphics[width=0.96\linewidth,height=5.0cm,keepaspectratio]{\docfield{cover}}}}\par
  \fi
  \vspace{9pt}%
  {\headingfont\bfseries\fontsize{18.5}{24}\selectfont\color{auraVelvetForest}\docfield{titlehe}\par}%
  \vspace{7pt}%
  {\begin{english}\centering\setstretch{1.05}\fontsize{12}{15.5}\selectfont\itshape\color{auraDust!85!black}%
    \docfield{titleen}\par\end{english}}%
  \vspace{8pt}%
  {\color{auraMustard}\rule{0.5\linewidth}{1.6pt}\par}\vspace{-1pt}{\color{auraDust}\rule{0.32\linewidth}{0.5pt}\par}\vspace{6pt}%
  {\headingfont\bfseries\Large\color{auraVelvetForest}\auratwin@typename\ \textenglish{(\auratwin@typenameen)}\par}%
  \vspace{3pt}%
  {\headingfont\normalsize\color{auraCopper}קוד קבוצה: \en{\texttt{\docfield{group}}}\ \textbar\ גרסה \num{\docfield{version}}\par}%
  \vfill
  \begin{tcolorbox}[enhanced,breakable=false,width=0.86\linewidth,colback=auraEggNog,
      colframe=auraMustard,boxrule=0.8pt,arc=4pt,left=10pt,right=10pt,top=7pt,bottom=7pt]
    \centering\setstretch{1.15}\color{auraVelvetForest}\docfield{authors}\par\vspace{4pt}%
    {\small מנחה אקדמי: \docfield{advisor}\par}%
    \ifx\auratwin@partner\@empty\else{\small \docfield{partner}\par}\fi
  \end{tcolorbox}%
  \vspace{7pt}%
  {\small\color{auraVelvetForest}תאריך הגשה: \docfield{date}\par}%
  \vspace{3pt}%
  {\footnotesize\color{auraDust!85!black}\copyrightsign\ \num{\the\year}\ \texthebrew{\docfield{authorsshort}}.\ כל הזכויות שמורות.
   \ \textenglish{All rights reserved.}\par}%
  \clearpage\endgroup}
\endinput
