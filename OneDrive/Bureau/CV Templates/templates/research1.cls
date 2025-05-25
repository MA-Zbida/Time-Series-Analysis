%
% Biographical Sketch LaTeX Class File
% Based on Jennifer E. Hoffman's template
% License: MIT
%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{biosketch}[2024/01/01 Biographical Sketch Class]

% Base class
\LoadClass[12pt]{article}

% Define some new colors
\RequirePackage{xcolor}
\definecolor{mBlue}{RGB}{51, 77, 167}
\newcommand{\blue}[1]{{\color{mBlue}#1}}

% Page and text formatting
\RequirePackage[left=1.0in, right=1.0in, top=1.0in, bottom=1.0in]{geometry} % margins
\RequirePackage{setspace}
\singlespacing % No more than 6 lines of text per inch
\RequirePackage{amsmath, amsfonts}
\RequirePackage[T1]{fontenc}
\RequirePackage{times}

% Make the sections start with (a), (b), etc.
\renewcommand\thesection{(\alph{section})}
\renewcommand\thesubsection{(\alph{subsection})}

% Set up footer
\RequirePackage{fancyhdr}
\fancypagestyle{CVfooter}
{
 \lhead{}
 \chead{}
 \rhead{}
 \lfoot{\small{\@authorname}}
 \cfoot{\small{\today}}
 \rfoot{\small{\thepage/\@totalpages}}
 \renewcommand{\headrulewidth}{0.0pt}
 \renewcommand{\footrulewidth}{0.5pt}
}

% Set up hyperlinks
\RequirePackage[linktoc=page]{hyperref}
\hypersetup{
  colorlinks = true,
  urlcolor = mBlue,
  citecolor = mBlue,
  linkcolor = mBlue,
}

% Set up citations and bibliography
\RequirePackage{bibunits}
\RequirePackage[sort&compress,super]{natbib}
\defaultbibliographystyle{apsrev4-2}
\setcitestyle{comma}
\setlength{\bibsep}{0pt}
\renewcommand{\bibnumfmt}[1]{\ \ \ #1.}
\renewcommand\refname{\vspace{-7mm}}

% This allows us to start a bibliography with arbitrary number
\RequirePackage{etoolbox}
\makeatletter
\newcommand*{\newbibstartnumber}[1]{%
  \apptocmd{\thebibliography}{%
    \global\c@NAT@ctr #1\relax
    \addtocounter{NAT@ctr}{-1}%
  }{}{}%
}
\makeatother

% Reduce whitespace around lists (globally)
\RequirePackage{enumitem}
\setlist[itemize]{nosep,left=0pt}
\setlist[enumerate]{nosep}
\setlist[description]{nosep}

% Formatting for sections
\RequirePackage[compact]{titlesec}
\titleformat*{\section}{\normalsize\bfseries}
\titlespacing*{\section}{0mm}{2mm}{1mm}[0mm] % left top bottom right
\titleformat*{\subsection}{\normalsize\bfseries}
\titlespacing*{\subsection}{0mm}{2mm}{1mm}[0mm]
\titleformat*{\subsubsection}{\normalsize\bfseries\itshape}
\titlespacing*{\subsubsection}{0mm}{1mm}{0mm}[0mm]

% Custom commands for personal information
\newcommand{\authorname}[1]{\def\@authorname{#1}}
\newcommand{\authortitle}[1]{\def\@authortitle{#1}}
\newcommand{\authorinstitution}[1]{\def\@authorinstitution{#1}}
\newcommand{\authoraddress}[1]{\def\@authoraddress{#1}}
\newcommand{\authoremail}[1]{\def\@authoremail{#1}}
\newcommand{\authorweb}[1]{\def\@authorweb{#1}}
\newcommand{\authorphone}[1]{\def\@authorphone{#1}}
\newcommand{\authorfax}[1]{\def\@authorfax{#1}}
\newcommand{\totalpages}[1]{\def\@totalpages{#1}}

% Default values
\authorname{Author Name}
\authortitle{Title}
\authorinstitution{Institution}
\authoraddress{Address}
\authoremail{email@example.com}
\authorweb{http://www.example.com}
\authorphone{000-000-0000}
\authorfax{000-000-0000}
\totalpages{2}

% Command to create the header
\newcommand{\makeheader}{
    \pagestyle{CVfooter}
    
    \noindent \textbf{\uppercase{Biographical Sketch}}
    \vspace{2mm}
    
    \noindent \textbf{\@authorname}
    \vspace{1mm}
    
    \noindent\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l r}
    \@authortitle & Email: \href{mailto:\@authoremail}{\@authoremail} \\
    \@authorinstitution & Web: \href{\@authorweb}{\@authorweb} \\
    \@authoraddress & Phone: \@authorphone \\
     & Fax: \@authorfax \\
    \hline
    \end{tabular*}
}

% Education table environment
\newenvironment{educationtable}{
    \begin{tabular}{l l l l}
}{
    \end{tabular}
}

% Experience table environment
\newenvironment{experiencetable}{
    \begin{tabular}{l l}
}{
    \end{tabular}
}

% Bibliography sections
\newcommand{\relatedpubs}[1]{
    \vspace{2mm}
    \noindent \textbf{\textit{\ \ Most closely related}}
    \begin{bibunit}
    \nocite{apsrev42Control}
    \nocite{#1}
    \putbib[publications]
    \end{bibunit}
}

\newcommand{\otherpubs}[2]{
    \vspace{2mm}
    \noindent \textbf{\textit{\ \ Other significant publications}}
    \newbibstartnumber{#1}
    \begin{bibunit}
    \nocite{apsrev42Control}
    \nocite{#2}
    \putbib[publications]
    \end{bibunit}
}

% Convenient commands for common formatting
\newcommand{\award}[3]{\item #1, ``#2'', #3}
\newcommand{\position}[2]{#1 & #2 \\}
\newcommand{\education}[4]{#1 & #2 & #3 & #4 \\}

\endinput