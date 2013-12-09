(setq org-export-table-row-tags
      (cons '(if head
		 "<tr>"
	       (if (= (mod nline 2) 1)
		   "<tr class=\"tr-odd\">"
		 "<tr class=\"tr-even\">"))
	    "</tr>"))


(setq org-emphasis-alist (quote (("*" bold "<b>" "</b>")
				 ("/" italic "<i>" "</i>") 
				 ("_" underline "<span style=\"text-decoration:underline;\">" "</span>")
				 ("-" (:overline t) "<span style=\"text-decoration:overline;\">" "</span>")
				 ("=" org-code "<code>" "</code>" verbatim)
				 ("~" org-verbatim "<code>" "</code>" verbatim)
				 ("+" (:strike-through t) "<del>" "</del>"))))

