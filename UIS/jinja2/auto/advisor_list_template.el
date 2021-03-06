(TeX-add-style-hook
 "advisor_list_template"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "fontsize=14" "headinclude=true" "headsepline=true" "footsepline=true" "open=any" "twoside=false")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("scrlayer-scrpage" "automark") ("geometry" "paperwidth=210mm" "paperheight=297mm" "left=25mm" "right=25mm" "top=30mm" "bottom=30mm" "footskip=10mm" "headsep=0mm") ("enumitem" "inline")))
   (TeX-run-style-hooks
    "latex2e"
    "scrartcl"
    "scrartcl10"
    "scrlayer-scrpage"
    "geometry"
    "fontspec"
    "polyglossia"
    "booktabs"
    "longtable"
    "bidi-longtable"
    "amssymb"
    "graphicx"
    "enumitem")))

