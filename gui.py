# imports
import os
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
from controller import Controller
from functools import partial
from database import DatabaseManager


db_manager = DatabaseManager()


# tkinter object
# tkinterDnD has all tkinter functionality + file drag and drop
root = TkinterDnD.Tk()

# title of program
root.title("SecureBuddy")

# screen size
root.geometry("1980x1200")


# welcome page
welcome_page = tk.Frame(root, width=1980, height=1200)
welcome_page.place(x=0, y=0, relwidth=1, relheight=1)

# text to show
text = "Welcome to SecureBuddy"
# label for text
label = tk.Label(welcome_page, text=text,  font=("Arial", 30))
label.place(x=425, y=50)

# buttons for welcome page
# scan files
welcome_scan_files_button = tk.Button(welcome_page, text="Scan Files", font=("Arial", 16), command=lambda: show_page(scan_files_page))
# placing button
welcome_scan_files_button.place(x=100, y=250, width=300, height=250)

# scan history
welcome_scan_history_button = tk.Button(welcome_page, text="Scan History", font=("Arial", 16), command=lambda: show_page(scan_history_page))
# placing button
welcome_scan_history_button.place(x=500, y=250, width=300, height=250)

# education
welcome_education_button = tk.Button(welcome_page, text="Education", font=("Arial", 16), command=lambda: show_page(education_page))
# placing button
welcome_education_button.place(x=900, y=250, width=300, height=250)


# bool to check if the hamburger menu frame is visible
is_menu_visible = False



# function that handles functionality when hamburger button is clicked
def hamburger_menu():
    
    global is_menu_visible
    
    # check if menu is already visible
    if is_menu_visible:
        
        hide_menu() 
    else:
        display_menu()



# function to hide menu when hamburger button is clicked
def hide_menu():
    
    global is_menu_visible
    
    # slide frame towards the left, off screen
    for i in range(0, -1000, -15): 
        
        # display menu frame
        menu_frame.place(x=i, y=0) 
        
        # update each frame movement
        root.update()
        
    is_menu_visible = False


# function to display menu when hamburger button is clicked
def display_menu():
    
    global is_menu_visible
    
    # slide frame to be displayed on screen
    for i in range(-1000, 0, 50):
        
        # menu frame needs to be shown when hamburger button clicked
        menu_frame.tkraise()
        
        # display menu frame
        menu_frame.place(x=i, y=0)
        
        # update each frame movement
        root.update()
        
        # make animation smoother
        root.after(10)
        
    is_menu_visible = True


# function to display different pages
# page is dependant on what button is clicked in hamburger menu frame
def show_page(page):
    
    # raise the page on the top
    page.tkraise()
    
    # hide the menu frame
    hide_menu()
    
    # need to show hamburger button
    hamburger_button.tkraise()
    
    # display specific items only when that particular page is called
    if page == scan_files_page:
        
        upload_file_button.tkraise()
        
    # if scanning is complete, stop showing scanning.png
    if page == scan_report_page:
        
        scanning_image_label.place_forget()


# function to process the file from gui
#   from drag and drop, or button click
# done for modularity purposes
def process_file_gui(file_path):
    
    # if file path is valid
    if os.path.isfile(file_path):
        
        try:
            # create instance of controller class to manage file processing logic
            controller = Controller()
            
            # call process_file function from controller
            controller.process_file(file_path)
            
            # close controller for resource management
            controller.close()
            
            # extract file name from full file path
            file_name = os.path.basename(file_path)
            
            # update label with file name
            scanning_file_name_label.config(text=f"Selected file: {file_name}")
            
            # show scanning page
            scanning_page.tkraise()
            
            # simulate scanning with 2 second delay
            # switches to scan report page
            root.after(2000, lambda: show_page(scan_report_page))
            
        # handle errors during file processing
        except Exception as e:
            
            # display error message
            scanning_file_name_label.config(text=f"Error processing file: {e}")
    
    # if file path invalid
    else:
        
        # display error message
        scanning_file_name_label.config(text="Invalid file dropped")



# function to handle file upload via button
def upload_file():
    
    # open file dialog
    # get full file path
    file_path = filedialog.askopenfilename()
    
    # clean file path
    file_path = file_path.strip()
    
     # remove in future
    print(f"Selected file: {file_path}")

    # if a file path is selected
    if file_path:
        
        # process the file
        process_file_gui(file_path)
        
    # if no file is selected
    else:
        
        # display no file selected message
        scanning_file_name_label.config(text="No file selected")



# function to handle file upload via drag and drop
def on_drop(event):
    
    # clean file path
    file_path = event.data.strip()
    
     # remove in future
    print(f"Selected file: {file_path}")
    
    # process the file
    process_file_gui(file_path)



# hamburger menu icon (now placed as a child of welcome_page)
hamburger_button = tk.Button(root, text="☰", font=("Arial", 20), command=hamburger_menu)
hamburger_button.place(x=10, y=10)

# create side menu for hamburger button
# cover 3/4 of the screen
menu_frame = tk.Frame(root, bg="lightgray", width=800, height=1200)

# when program starts, position hamburger menu off screen
menu_frame.place(x=-1000, y=0) 

# buttons for menu_frame
scan_files_button = tk.Button(menu_frame, text="Scan Files", font=("Arial", 16), command=lambda: show_page(scan_files_page))
scan_history_button = tk.Button(menu_frame, text="Scan History", font=("Arial", 16), command=lambda: show_page(scan_history_page))
education_button = tk.Button(menu_frame, text="Education", font=("Arial", 16), command=lambda: show_page(education_page))

# manual button height
# TODO need to make this automatic
button_height = 225

# placing location for buttons
scan_files_button.place(x=0, y=0, width=800, height=button_height)
scan_history_button.place(x=0, y=button_height, width=800, height=button_height)
education_button.place(x=0, y=button_height * 2, width=800, height=button_height)



# scan files page
scan_files_page = tk.Frame(root, bg="white", width=1980, height=1200)
scan_files_page.place(x=0, y=0)

# scan files page header text
scan_files_header = "Scan Files"
scan_files_header_label = tk.Label(scan_files_page, text=scan_files_header, font=("Arial", 20))
scan_files_header_label.place(x=575, y=50)


# upload file button for scan files page
upload_file_button = tk.Button(scan_files_page, text="Upload File", font=("Arial", 16), command=upload_file)
upload_file_button.place(x=575, y=500, height=50, width=150)

# drag and drop for scan files page
drop_area = tk.Label(scan_files_page, text="Drag and drop a file here or click 'Upload File' button", font=("Arial", 16), relief="groove")
drop_area.place(x=200, y=150, width=900, height=300)

# bind drop event to on_drop function
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)


# scanning page
# once a file is uploaded - begin scanning
scanning_page = tk.Frame(root, bg="white", width=1980, height=1200)
scanning_page.place(x=0, y=0)

# scanning page header text
scanning_header = "Scanning"
scanning_header_label = tk.Label(scanning_page, text=scanning_header, font=("Arial", 20))
scanning_header_label.place(x=575, y=50)

# image for scanning
scanning_image = tk.PhotoImage(file="images/scanning.png")
scanning_image_label = tk.Label(scanning_page, image=scanning_image)
scanning_image_label.place(x=500, y=200)

# label to show selected file
scanning_file_name_label = tk.Label(scanning_page, text="No file selected", font=("Arial", 14))
scanning_file_name_label.place(x=500, y=500)


# scan complete
# once a file finished scanning - show report
scan_report_page = tk.Frame(root, bg="white", width=1980, height=1200)
scan_report_page.place(x=0, y=0)

# scan report header text
scan_report_header = "Scan Results"
scan_report_header_label = tk.Label(scan_report_page, text=scan_report_header, font=("Arial", 20))
scan_report_header_label.place(x=575, y=50)


# scan complete message
scan_complete_message = "Scan Complete. Here are your results"
scan_complete_message_label = tk.Label(scan_report_page, text=scan_complete_message, font=("Arial", 14))
scan_complete_message_label.place(x=500, y=150)

# dummy text scan results - malware
malware_dummy_message = "Malware Found: PHP script found within contents of file."
malware_dummy_message_label = tk.Label(scan_report_page, text=malware_dummy_message, font=("Arial", 14))
malware_dummy_message_label.place(x=10, y=300)


# TEMP PAGE FOR PHP MALWARE FOR DEMO PURPOSES
php_malware_page = tk.Frame(root, bg="white", width=1980, height=1200)
php_malware_page.place(x=0, y=0)

# php malware header text
php_malware_header = "PHP"
php_malware_header_label = tk.Label(php_malware_page, text=php_malware_header, font=("Arial", 20))
php_malware_header_label.place(x=600, y=50)

# text for php malware
php_malware_text_1 = "What is PHP?"
php_malware_text_1_label = tk.Label(php_malware_page, text=php_malware_text_1, font=("Arial", 15))
php_malware_text_1_label.place(x=10, y=150)

# text for php malware
php_malware_text_2 = "PHP is a computer language. It is a set of instructions written so a computer can do some intended functionality. This is known as a script."
php_malware_text_2_label = tk.Label(php_malware_page, text=php_malware_text_2, font=("Arial", 14), wraplength=900)
php_malware_text_2_label.place(x=10, y=200)

# text for php malware
php_malware_text_3 = "PHP scripts can be executed if the file is opened. Some examples of script execution can include:"
php_malware_text_3_label = tk.Label(php_malware_page, text=php_malware_text_3, font=("Arial", 14), wraplength=900)
php_malware_text_3_label.place(x=10, y=300)

# text for php malware
php_malware_text_4 = "Reading contents of files"
php_malware_text_4_label = tk.Label(php_malware_page, text=php_malware_text_4, font=("Arial", 14), wraplength=900)
php_malware_text_4_label.place(x=10, y=350)

# text for php malware
php_malware_text_5 = "Modifying files"
php_malware_text_5_label = tk.Label(php_malware_page, text=php_malware_text_5, font=("Arial", 14), wraplength=900)
php_malware_text_5_label.place(x=10, y=400)

# text for php malware
php_malware_text_6 = "Deleting files"
php_malware_text_6_label = tk.Label(php_malware_page, text=php_malware_text_6, font=("Arial", 14), wraplength=900)
php_malware_text_6_label.place(x=10, y=450)

# image for php malware
image_path = "images/php.png"
original_image = Image.open(image_path) 
resized_image = original_image.resize((300, 200))
php_image = ImageTk.PhotoImage(resized_image)

php_image_label = tk.Label(php_malware_page, image=php_image)
php_image_label.place(x=900, y=200)

# button for php - TEMP
more_info_php_malware_button =  tk.Button(scan_report_page, text="more info", font=("Arial, 12"), command=lambda: show_page(php_malware_page))
more_info_php_malware_button.place(x=1150, y=300, height=50, width=90)


# dummy text scan results - potential harm
potential_harm_dummy_message = "Potential Harm: Running this file could allow attackers to control your computer system. This means that they may access your files."
potential_harm_dummy_message_label = tk.Label(scan_report_page, text=potential_harm_dummy_message, font=("Arial", 14), wraplength=1200)
potential_harm_dummy_message_label.place(x=10, y=400)

# dummy button
potential_harm_dummy_button = tk.Button(scan_report_page, text="more info", font=("Arial, 12"))
potential_harm_dummy_button.place(x=1150, y=400, height=50, width=90)


# dummy text scan results - prevention tips
prevention_tips_dummy_message = "Prevention Tips: Only download files from trusted sources."
prevention_tips_dummy_message_label = tk.Label(scan_report_page, text=prevention_tips_dummy_message, font=("Arial", 14))
prevention_tips_dummy_message_label.place(x=10, y=500)

# dummy button
prevention_tips_dummy_button = tk.Button(scan_report_page, text="more info", font=("Arial, 12"))
prevention_tips_dummy_button.place(x=1150, y=500, height=50, width=90)



# scan history page
scan_history_page = tk.Frame(root, bg="white", width=1980, height=1200)
scan_history_page.place(x=0, y=0)

# scan history header text
scan_history_header = "Scan History"
scan_history_header_label = tk.Label(scan_history_page, text=scan_history_header, font=("Arial", 20))
scan_history_header_label.place(x=575, y=50)


# create canvas for scrollable scan rows
canvas = tk.Canvas(scan_history_page, bg="white", width=1500, height=800)
canvas.place(x=200, y=150)

# vertical scrollbar
scrollbar = tk.Scrollbar(scan_history_page, orient="vertical", command=canvas.yview)
scrollbar.place(x=1700, y=150, height=800)

# create frame inside canvas to hold rows
scan_rows_frame = tk.Frame(canvas, bg="white")

# add frame to canvas as window
canvas.create_window((0, 0), window=scan_rows_frame, anchor="nw")

# configure canvas to work with vertical scrollbar
canvas.configure(yscrollcommand=scrollbar.set)


# function to update scrollable region of canvas when content changes
def update_scroll_region(event=None):
    
    # update scroll region to catch all child widgets
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    
# bind resizing of scan_rows_frame to scroll region update function
scan_rows_frame.bind("<Configure>", update_scroll_region)


# function to handle scroll event using mouse wheel
def _on_mouse_wheel(event):
    
    # scroll canvas by 10 units when mouse wheel is moved
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    
# bind mouse wheel event to canvas
canvas.bind_all("<MouseWheel>", _on_mouse_wheel)


# function to populate scan history dynamically from db
def populate_scan_history():
    
    # clear any existing rows in scan_rows_frame
    for widget in scan_rows_frame.winfo_children():
        widget.destroy()

    # fetch scan history from db
    scan_history = db_manager.get_scan_history()

    # loop through scan history
    # add rows for each entry
    for index, (scan_id, file_name, scan_date) in enumerate(scan_history):
        
        # file name
        file_name_label = tk.Label(scan_rows_frame, text=file_name, font=("Arial", 14), bg="white")
        file_name_label.grid(row=index, column=0, padx=10, pady=5)

        # scan date
        scan_date_label = tk.Label(scan_rows_frame, text=scan_date, font=("Arial", 14), bg="white")
        scan_date_label.grid(row=index, column=1, padx=10, pady=5)

        # view scan button
        view_button = tk.Button(
            scan_rows_frame,
            text="View Scan",
            font=("Arial", 14),
            
            # using scan id to send to button
            command=partial(view_scan_details, scan_id)
        )
        
        # placing in grid layout
        view_button.grid(row=index, column=2, padx=10, pady=5)


# function to display details of specific scan in new page
def view_scan_details(scan_id):
    
    # fetch scan details from db for given scan id
    scan_details = db_manager.get_scan_details(scan_id)
    scanned_file_info = db_manager.get_scanned_file_info(scan_id)
    threat_info = db_manager.get_threat_info(scan_id)

    # create new page dynamically
    details_page = tk.Frame(root, bg="white")
    details_page.place(x=0, y=0, relwidth=1, relheight=1)

    # header
    header_label = tk.Label(details_page, text="Scan Details", font=("Arial", 24), bg="white")
    header_label.pack(pady=20)

    # display scanned file info
    if scanned_file_info:
        
        # unpack info
        file_name, scan_date, status, risk_level = scanned_file_info
        
        # display info in label
        scanned_file_label = tk.Label(
            
            details_page, 
            
            text=f"File Name: {file_name}\nScan Date: {scan_date}\nStatus: {status}\nRisk Level: {risk_level}",
            
            font=("Arial", 16), bg="white", justify="left"
        )
    
        # padding
        scanned_file_label.pack(pady=10)
        
    else:
        
        # if no info available, show message
        no_file_info_label = tk.Label(
            
            details_page, text="No scanned file information available.", font=("Arial", 16), bg="white"
        )
        
        # padding
        no_file_info_label.pack(pady=10)

    # display scan details
    if scan_details:
        
        # display each reason and risk category
        for reason, risk_category in scan_details:
            
            # display in label
            detail_label = tk.Label(
                
                details_page, 
                
                text=f"Reason: {reason}, Risk: {risk_category}",
                
                font=("Arial", 16), bg="white"
            )
            
            # padding
            detail_label.pack(pady=5)
            
    else:
        
        # message if no scan details available
        no_details_label = tk.Label(
            
            details_page, text="No scan details available.", font=("Arial", 16), bg="white"
        )
        
        # padding
        no_details_label.pack(pady=10)

    # display threat info
    if threat_info:
        
        # unpack info
        what_happens_if_run, prevention_tips = threat_info
        
        # display info in label
        threat_info_label = tk.Label(
            
            details_page, 
            
            text=f"What Happens If Run:\n{what_happens_if_run}\n\nPrevention Tips:\n{prevention_tips}",
            
            font=("Arial", 16), bg="white", justify="left"
        )
        
        # padding
        threat_info_label.pack(pady=10)
        
    else:
        
        # message if no info available
        no_threat_info_label = tk.Label(
            
            details_page, text="No threat information available.", font=("Arial", 16), bg="white"
        )
        
        # padding
        no_threat_info_label.pack(pady=10)

    # back button to go back to scan history page
    back_button = tk.Button(
        
        details_page, text="Back", font=("Arial", 16),
        
        # destroy page for memory efficiency
        command=lambda: details_page.destroy()
    )
    
    # padding
    back_button.pack(pady=20)


# populate scan history with data from db when page is loaded
populate_scan_history()


# education page
education_page = tk.Frame(root, bg="white", width=1980, height=1200)
education_page.place(x=0, y=0)

# education header text
education_header = "Education"
education_header_label = tk.Label(education_page, text=education_header, font=("Arial", 20))
education_header_label.place(x=575, y=50)

# buttons for education tab
# malware button
education_malware_button = tk.Button(education_page, text="Malware", font=("Arial", 16), command=lambda: show_page(malware_page))
# placing button
education_malware_button.place(x=100, y=250, width=300, height=250)

# file types button
education_file_types_button = tk.Button(education_page, text="File Types", font=("Arial", 16), command=lambda: show_page(file_types_page))
# placing button
education_file_types_button.place(x=500, y=250, width=300, height=250)

# prevention tips button
education_prevention_tips_button = tk.Button(education_page, text="Prevention Tips", font=("Arial", 16), command=lambda: show_page(prevention_tips_page))
# placing button
education_prevention_tips_button.place(x=900, y=250, width=300, height=250)


# malware page
malware_page = tk.Frame(root, bg="white", width=1980, height=1200)
malware_page.place(x=0, y=0)

# malware header text
malware_header = "Malware"
malware_header_label = tk.Label(malware_page, text=malware_header, font=("Arial", 20))
malware_header_label.place(x=575, y=50)


# file types page
file_types_page = tk.Frame(root, bg="white", width=1980, height=1200)
file_types_page.place(x=0, y=0)

# file types header text
file_types_header = "File Types"
file_types_header_label = tk.Label(file_types_page, text=file_types_header, font=("Arial", 20))
file_types_header_label.place(x=575, y=50)


# prevention tips page
prevention_tips_page = tk.Frame(root, bg="white", width=1980, height=1200)
prevention_tips_page.place(x=0, y=0)

# prevention tips header text
prevention_tips_header = "Prevention Tips"
prevention_tips_header_label = tk.Label(prevention_tips_page, text=prevention_tips_header, font=("Arial", 20))
prevention_tips_header_label.place(x=575, y=50)



# need to show at start
welcome_page.tkraise()

# need to show hamburger button
# TODO include for hamburger menu frame 'x' / 'esc' functionality
hamburger_button.tkraise()

# main loop
root.mainloop()