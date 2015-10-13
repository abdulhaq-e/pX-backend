(TeX-add-style-hook
 "student_grade_template"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "fontsize=14" "headinclude=true" "headsepline=true" "footsepline=true")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "paperwidth=210mm" "paperheight=297mm" "left=25mm" "right=25mm" "top=30mm" "bottom=30mm" "footskip=10mm" "headsep=0mm") ("enumitem" "inline")))
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
    "pgfplotstable")))

