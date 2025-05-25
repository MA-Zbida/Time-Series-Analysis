%
% Academic CV LaTeX Class File
% Author: Dubasi Pavan Kumar
% LinkedIn: https://www.linkedin.com/in/im-pavankumar/
% License: MIT
%
% For errors, suggestions, or improvements, please contact:
% Email: pavankumard.pg19.ma@nitp.ac.in
%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{academic-cv}[2024/01/01 Academic CV Class]

% Base class
\LoadClass[a4paper,11pt]{article}

% Package imports
\RequirePackage{latexsym}
\RequirePackage{xcolor}
\RequirePackage{float}
\RequirePackage{ragged2e}
\RequirePackage[empty]{fullpage}
\RequirePackage{wrapfig}
\RequirePackage{lipsum}
\RequirePackage{tabularx}
\RequirePackage{titlesec}
\RequirePackage{geometry}
\RequirePackage{marvosym}
\RequirePackage{verbatim}
\RequirePackage{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{multicol}
\RequirePackage{graphicx}
\RequirePackage{cfr-lm}
\RequirePackage[T1]{fontenc}
\RequirePackage{fontawesome5}

% Color definitions
\definecolor{darkblue}{RGB}{0,0,139}

% Page layout
\setlength{\multicolsep}{0pt} 
\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\geometry{left=1.4cm, top=0.8cm, right=1.2cm, bottom=1cm}
\setlength{\footskip}{5pt} % Addressing fancyhdr warning

% Hyperlink setup (moved after fancyhdr to address warning)
\RequirePackage[hidelinks]{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    filecolor=darkblue,
    urlcolor=darkblue,
}

% Custom box settings
\RequirePackage[most]{tcolorbox}
\tcbset{
    frame code={},
    center title,
    left=0pt,
    right=0pt,
    top=0pt,
    bottom=0pt,
    colback=gray!20,
    colframe=white,
    width=\dimexpr\textwidth\relax,
    enlarge left by=-2mm,
    boxsep=4pt,
    arc=0pt,outer arc=0pt,
}

% URL style
\urlstyle{same}

% Text alignment
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-7pt}]

% Custom commands
\newcommand{\resumeItem}[2]{
  \item{
    \textbf{#1}{\hspace{0.5mm}#2 \vspace{-0.5mm}}
  }
}

\newcommand{\resumePOR}[3]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1}\hspace{0.3mm}#2 & \textit{\small{#3}} 
    \end{tabular*}
    \vspace{-2mm}
}

\newcommand{\resumeSubheading}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1} & \textit{\footnotesize{#4}} \\
        \textit{\footnotesize{#3}} &  \footnotesize{#2}\\
    \end{tabular*}
    \vspace{-2.4mm}
}

\newcommand{\resumeProject}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1} & \textit{\footnotesize{#3}} \\
        \footnotesize{\textit{#2}} & \footnotesize{#4}
    \end{tabular*}
    \vspace{-2.4mm}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-4pt}}

\renewcommand{\labelitemi}{$\vcenter{\hbox{\tiny$\bullet$}}$}
\renewcommand{\labelitemii}{$\vcenter{\hbox{\tiny$\circ$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*,labelsep=1mm]}
\newcommand{\resumeHeadingSkillStart}{\begin{itemize}[leftmargin=*,itemsep=1.7mm, rightmargin=2ex]}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=*,labelsep=1mm,itemsep=0.5mm]}

\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{2mm}}
\newcommand{\resumeHeadingSkillEnd}{\end{itemize}\vspace{-2mm}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-2mm}}
\newcommand{\cvsection}[1]{%
\vspace{2mm}
\begin{tcolorbox}
    \textbf{\large #1}
\end{tcolorbox}
    \vspace{-4mm}
}

\newcolumntype{L}{>{\raggedright\arraybackslash}X}%
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}%
\newcolumntype{C}{>{\centering\arraybackslash}X}%

% Commands for icon sizing and positioning
\newcommand{\socialicon}[1]{\raisebox{-0.05em}{\resizebox{!}{1em}{#1}}}
\newcommand{\ieeeicon}[1]{\raisebox{-0.3em}{\resizebox{!}{1.3em}{#1}}}

% Font options
\newcommand{\headerfonti}{\fontfamily{phv}\selectfont} % Helvetica-like (similar to Arial/Calibri)
\newcommand{\headerfontii}{\fontfamily{ptm}\selectfont} % Times-like (similar to Times New Roman)
\newcommand{\headerfontiii}{\fontfamily{ppl}\selectfont} % Palatino (elegant serif)
\newcommand{\headerfontiv}{\fontfamily{pbk}\selectfont} % Bookman (readable serif)
\newcommand{\headerfontv}{\fontfamily{pag}\selectfont} % Avant Garde-like (similar to Trebuchet MS)
\newcommand{\headerfontvi}{\fontfamily{cmss}\selectfont} % Computer Modern Sans Serif
\newcommand{\headerfontvii}{\fontfamily{qhv}\selectfont} % Quasi-Helvetica (another Arial/Calibri alternative)
\newcommand{\headerfontviii}{\fontfamily{qpl}\selectfont} % Quasi-Palatino (another elegant serif option)
\newcommand{\headerfontix}{\fontfamily{qtm}\selectfont} % Quasi-Times (another Times New Roman alternative)
\newcommand{\headerfontx}{\fontfamily{bch}\selectfont} % Charter (clean serif font)

% Header commands for easy customization
\newcommand{\cvname}[1]{\def\@cvname{#1}}
\newcommand{\cvphone}[1]{\def\@cvphone{#1}}
\newcommand{\cvemail}[1]{\def\@cvemail{#1}}
\newcommand{\cvwebsite}[1]{\def\@cvwebsite{#1}}
\newcommand{\cvlinkedin}[1]{\def\@cvlinkedin{#1}}
\newcommand{\cvgithub}[1]{\def\@cvgithub{#1}}
\newcommand{\cvieee}[1]{\def\@cvieee{#1}}
\newcommand{\cvtwitter}[1]{\def\@cvtwitter{#1}}
\newcommand{\cvaddress}[1]{\def\@cvaddress{#1}}

% Command to create the header
\newcommand{\makeheader}{
    \headerfontiii
    \begin{center}
        {\Huge\textbf{\@cvname}}
    \end{center}
    \vspace{-6mm}
    
    \begin{center}
        \small{
        \@cvphone | \href{mailto:\@cvemail}{\@cvemail} | 
        \href{\@cvwebsite}{\@cvwebsite}
        }
    \end{center}
    \vspace{-6mm}
    
    \begin{center}
        \small{
        \socialicon{\faLinkedin} \href{https://www.linkedin.com/in/\@cvlinkedin}{\@cvlinkedin} | 
        \socialicon{\faGithub} \href{https://github.com/\@cvgithub}{\@cvgithub} | 
        \ieeeicon{\includegraphics[height=1.3em]{ieee_collabratec_icon.png}} \href{https://ieee-collabratec.ieee.org/app/p/\@cvieee}{\@cvieee} |
        \socialicon{\faTwitter} \href{https://twitter.com/\@cvtwitter}{\@cvtwitter}
        }
    \end{center}
    \vspace{-6mm}
    \begin{center}
        \small{\@cvaddress}
    \end{center}
    \vspace{-4mm}
}

\endinput