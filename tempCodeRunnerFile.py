# TEMP PAGE FOR PHP MALWARE FOR DEMO PURPOSES
php_malware_page = tk.Frame(root, bg="white", width=1980, height=1200)
php_malware_page.place(x=0, y=0)

# php malware header text
php_malware_header = "PHP Malware"
php_malware_header_label = tk.Label(php_malware_page, text=php_malware_header, font=("Arial", 20))
php_malware_header_label.place(x=575, y=50)

# text for php malware
php_malware_text_1 = "lorem ipsum"
php_malware_text_1_label = tk.Label(php_malware_page, text=php_malware_text_1, font=("Arial", 20))
php_malware_text_1_label.place(x=10, y=150)


# button for php - TEMP
more_info_php_malware_button =  tk.Button(scan_report_page, text="more info", font=("Arial, 12"), command=lambda: show_page(php_malware_page))
more_info_php_malware_button.place(x=1150, y=300, height=50, width=90)