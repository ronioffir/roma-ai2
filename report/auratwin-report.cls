%% ============================================================================
%% auratwin-report.cls -- THIN company layer for AuraTwin AI documents
%% ----------------------------------------------------------------------------
%% Loads base-report.cls unchanged and adds ONLY: brand palette, logo,
%% document fields, document types, cover page, header/footer texts.
%% Document types (class options): report (default) | proposal | spec
%% ============================================================================
\NeedsTeXFormat{LaTeX2e}
\def\auratwin@version{1.2.1}
\ProvidesClass{auratwin-report}[2026/11/16 v1.2.1 AuraTwin AI company layer]

\def\auratwin@doctype{report}
\DeclareOption{report}{\def\auratwin@doctype{report}}
\DeclareOption{proposal}{\def\auratwin@doctype{proposal}}
\DeclareOption{spec}{\def\auratwin@doctype{spec}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{base-report}}
\ProcessOptions\relax
\LoadClass{base-report}

%% ------------------------------------------------------------ brand palette --
%% Changing one value here recolours headings, boxes, tables and headers.
\definecolor{brandprimary}{HTML}{4A2470}   % Aura plum   -- headings, table headers
\definecolor{brandsecondary}{HTML}{15807E} % Twin teal   -- AuraTwin / proposed solution
\definecolor{brandaccent}{HTML}{D4952B}    % Amber       -- manager box, flagship paper
\definecolor{brandtint}{HTML}{F3EEF8}      % row tint
\definecolor{brandwarn}{HTML}{C8423B}      % coral red   -- warnings, critical
\definecolor{brandexample}{HTML}{3949AB}   % indigo      -- examples
\definecolor{brandmuted}{HTML}{6B6478}
\definecolor{brandgreen}{HTML}{2E8B57}     % milestones
\definecolor{brandgrey}{HTML}{8C8C99}      % competitors

%% ------------------------------------------------------------------- logo --
\newcommand{\auratwinlogo}[1][1]{%
  \begin{tikzpicture}[scale=#1,baseline=-0.5ex]
    \fill[brandprimary] (0,0) circle (0.42);
    \fill[brandsecondary,opacity=0.85] (0.30,0) circle (0.42);
    \fill[white] (0.15,0) circle (0.13);
    \fill[brandaccent] (0.15,0) circle (0.06);
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
  \setheadleft{\en{\docfield{short}}\ \textbar\ \texthebrew{\auratwin@typename}\ \textbar\ \en{\docfield{group}}}%
  \setheadright{\copyrightsign\ \num{\the\year}\ \texthebrew{\docfield{authorsshort}}}}

%% ------------------------------------------------------------- cover page --
%% Double frame, cover image, Hebrew + English titles, document type, team,
%% advisor, date, copyright in the English font, NO visible page number.
\newcommand{\makecoverpage}{%
  \clearpage\begingroup\thispagestyle{empty}%
  \begin{english}%
  \begin{tikzpicture}[remember picture,overlay]
    \draw[brandprimary,line width=2.6pt]
      ([xshift=1.2cm,yshift=-1.2cm]current page.north west) rectangle
      ([xshift=-1.2cm,yshift=1.2cm]current page.south east);
    \draw[brandsecondary,line width=0.8pt]
      ([xshift=1.42cm,yshift=-1.42cm]current page.north west) rectangle
      ([xshift=-1.42cm,yshift=1.42cm]current page.south east);
  \end{tikzpicture}%
  \end{english}%
  \centering\setstretch{1.1}%
  \vspace*{-1.2cm}%
  {\headingfont\small\color{brandmuted}\docfield{inst}\par}%
  \vspace{1pt}{\headingfont\small\color{brandmuted}\docfield{course}\par}%
  \vspace{8pt}%
  \ifx\auratwin@cover\@empty\else
    \includegraphics[width=\linewidth,height=6.1cm,keepaspectratio]{\docfield{cover}}\par
  \fi
  \vspace{10pt}%
  {\headingfont\bfseries\fontsize{19}{25}\selectfont\color{brandprimary}\docfield{titlehe}\par}%
  \vspace{8pt}%
  {\begin{english}\centering\setstretch{1.05}\fontsize{12.5}{16}\selectfont\itshape\color{brandsecondary!85!black}%
    \docfield{titleen}\par\end{english}}%
  \vspace{10pt}%
  {\color{brandaccent}\rule{0.55\linewidth}{1.2pt}\par}\vspace{6pt}%
  {\headingfont\bfseries\Large\auratwin@typename\ \textenglish{(\auratwin@typenameen)}\par}%
  \vspace{3pt}%
  {\headingfont\normalsize קוד קבוצה: \en{\texttt{\docfield{group}}}\ \textbar\ גרסה \num{\docfield{version}}\par}%
  \vfill
  \begin{tcolorbox}[enhanced,breakable=false,width=0.86\linewidth,colback=brandtint,
      colframe=brandprimary!60,boxrule=0.6pt,arc=3pt,left=10pt,right=10pt,top=6pt,bottom=6pt]
    \centering\setstretch{1.15}\docfield{authors}\par\vspace{4pt}%
    {\small מנחה אקדמי: \docfield{advisor}\par}%
    \ifx\auratwin@partner\@empty\else{\small \docfield{partner}\par}\fi
  \end{tcolorbox}%
  \vspace{8pt}%
  {\small תאריך הגשה: \docfield{date}\par}%
  \vspace{4pt}%
  {\footnotesize\color{brandmuted}\copyrightsign\ \num{\the\year}\ \texthebrew{\docfield{authorsshort}}.\ כל הזכויות שמורות.
   \ \textenglish{All rights reserved.}\par}%
  \clearpage\endgroup}
\endinput
