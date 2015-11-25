(TeX-add-style-hook
 "form2_template"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "fontsize=15" "headinclude=true" "headsepline=false" "footsepline=false")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "paperwidth=210mm" "paperheight=297mm" "left=20mm" "right=30mm" "top=30mm" "bottom=30mm" "footskip=10mm" "headsep=0mm") ("enumitem" "inline") ("datetime2" "datesep=/" "useregional=numeric") ("setspace" "doublespacing")))
   (TeX-run-style-hooks
    "latex2e"
    "scrartcl"
    "scrartcl10"
    "scrlayer-scrpage"
    "geometry"
    "fontspec"
    "polyglossia"
    "booktabs"
    "eso-pic"
    "amssymb"
    "graphicx"
    "enumitem"
    "multirow"
    "tabularx"
    "tablefootnote"
    "pgfplots"
    "pgfplotstable"
    "dashrule"
    "fancybox"
    "datetime2"
    "setspace")
   (TeX-add-symbols
    "englishtoday"
    "newline")))

