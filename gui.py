import os
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import filedialog, font
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
from controller import Controller
from functools import partial
from ttkbootstrap import Style


# instatiate controller object
controller = Controller()

# main application window using TkinterDnD for drag + drop support
root = TkinterDnD.Tk()

# title of application window
root.title("SecureBuddy")

# ttkbootstrap lib for light visual theme
style = Style(theme="lumen")

# set application window to use full screen width and height
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# page for welcome / home screen
welcome_page = tk.Frame(root)

# frame fits whole window
welcome_page.place(relwidth=1, relheight=1)

# welcome text
text = "Welcome to SecureBuddy"
label = tk.Label(
    
    welcome_page, 
    text=text, 
    font=("Helvetica", 40, "bold"), 
    fg="white"
)
label.place(relx=0.5, rely=0.1, anchor="center")

# introduction info text
welcome_text = "Select one of the options below to get started!"
welcome_page_label = tk.Label(
    welcome_page, 
    text=welcome_text, 
    font=("Helvetica", 20, "bold"), 
    fg="white"
)
welcome_page_label.place(relx=0.5, rely=0.25, anchor="center")

# load and resize image for scan files button
scan_files_image_path = "images/mag_glass.png"
scan_files_image = Image.open(scan_files_image_path).resize((110, 120))
scan_files_icon = ImageTk.PhotoImage(scan_files_image)

# scan files button
scan_files_button = tk.Button(
    
    welcome_page,
    text="Scan Files",
    font=("Helvetica", 20, "bold"),
    image=scan_files_icon,
    compound="top",
    bg="white",
    fg="black",
    relief="flat",
    command=lambda: show_page(scan_files_page),
    pady=15
)
# keep reference to image to avoid garbage collection
scan_files_button.image = scan_files_icon
scan_files_button.place(relx=0.09, rely=0.4, relwidth=0.25, relheight=0.35)

# load and resize image for scan history button
scan_history_image_path = "images/history.png"
scan_history_image = Image.open(scan_history_image_path).resize((100, 100))
scan_history_icon = ImageTk.PhotoImage(scan_history_image)

# scan history button
scan_history_button = tk.Button(
    
    welcome_page,
    text="Scan History",
    font=("Helvetica", 20, "bold"),
    image=scan_history_icon,
    compound="top",
    bg="white",
    fg="black",
    relief="flat",
    command=lambda: show_page(scan_history_page),
    pady=15
)
# keep reference to image to avoid garbage collection
scan_history_button.image = scan_history_icon
scan_history_button.place(relx=0.37, rely=0.4, relwidth=0.25, relheight=0.35)

# load and resize image for education button
education_image_path = "images/books.png"
education_image = Image.open(education_image_path).resize((200, 100))
education_icon = ImageTk.PhotoImage(education_image)

# education button
education_button = tk.Button(
    
    welcome_page,
    text="Education",
    font=("Helvetica", 20, "bold"),
    image=education_icon,
    compound="top",
    bg="white",
    fg="black",
    relief="flat",
    command=lambda: show_page(education_page),
    pady=15
)
# keep reference to image to avoid garbage collection
education_button.image = education_icon
education_button.place(relx=0.65, rely=0.4, relwidth=0.25, relheight=0.35)


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
        
        # show hamburger button
        hamburger_button.tkraise()
        
        # show home button
        home_button.tkraise()
        
    is_menu_visible = True
    

# function to display different pages
def show_page(page):
    
    # raise the page on the top
    page.tkraise()
    
    # hide the menu frame
    hide_menu()
    
    # show hamburger button
    hamburger_button.tkraise() 
    
    # show home button
    home_button.tkraise()
    
    # display specific items only when that particular page is called
    if page == scan_files_page:
        
        # show upload file button
        upload_file_button.tkraise()
        
    if page == quiz_page:
        
        # dynamically place quiz buttons
        place_quiz_buttons()
        
    if page == scan_history_page:
        
        # update the scan history tab to include new scans
        update_scan_history()
        
        # ensure mouse wheel is working for page scrolling
        restore_mousewheel_binding()
        
    if page == executables_page3:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Executables")
        
    if page == file_spoofing3_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("File Spoofing")
        
    if page == obfuscation4_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Obfuscation")
        
    if page == remote_access3_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Remote Access Control")
        
    if page == viruses_page3:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Viruses")
        
    if page == credential_stealers3_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Credential Stealers")

    if page == compressed_files3_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Compressed Files")
        
    if page == macros3_page:
        
        # marking topic as read if user reaches this page
        controller.mark_topic_as_read("Macros")
    

# function to process the file from gui
# from drag and drop and button
def process_file_gui(file_path):
    
    # check if provided path is valid file
    if os.path.isfile(file_path):
        
        try:
            # extract file name only from file path
            file_name = os.path.basename(file_path)
            
            # update label on scanning page to show selected file name
            scanning_file_name_label.config(text=f"Selected file: {file_name}")

            # bring scanning page to the front
            scanning_page.tkraise()

            # delay scanning
            def delayed_scan():
                
                try:
                    
                    # call controller to process the file
                    # return scan result ID
                    scanned_file_id = controller.process_file(file_path)
            
                    # show scan results after 2.5 seconds
                    # simulate processing
                    root.after(2500, lambda: show_scan_results_from_controller(controller, scanned_file_id))

                # catch error
                except Exception as e:
                    
                    # logging
                    print(f"Error: {e}")

            # call scan in next event loop tick
            root.after(100, delayed_scan)

        # catch error
        except Exception as e:
            
            # logging
            print(f"Error: {e}")
            
    else:
        # show that an invalid file has been inputted
        scanning_file_name_label.config(text="Invalid file dropped")


# function to display scan results using controller and scanned file ID
def show_scan_results_from_controller(controller, scanned_file_id):
    
    try:
        # get both file metadata and results of scan from controller
        scanned_file_info, scan_details = controller.get_scan_details_and_info(scanned_file_id)

        # pass info to function that handles displaying results
        show_scan_results(scanned_file_info, scan_details)

    # catch error
    except Exception as e:
        
        # logging
        print(f"Error: {e}")


# function to display scan results on the scan report page
def show_scan_results(scanned_file_info, scan_details):
    
    # clear all existing wdigets from page
    # avoid duplicate widgets
    for widget in scan_report_page.winfo_children():
        
        widget.destroy()

    # header text
    scan_report_header = "Scan Results"
    scan_report_header_label = tk.Label(
        
        scan_report_page,
        text=scan_report_header,
        font=("Helvetica", 40, "bold"),
        fg="white",
        bg="black"
    )
    scan_report_header_label.place(relx=0.5, rely=0.1, anchor="center")

    # scan complete message
    scan_complete_message_label = tk.Label(
        scan_report_page,
        text="Scan Complete, here are your results",
        font=("Helvetica", 20, "bold"),
        fg="black",
        bg="white"
    )
    scan_complete_message_label.place(relx=0.5, rely=0.2, anchor="center")

    # y position for starting dynamic result display
    y_offset = 200

    # display file info
    # if there are details available
    if scanned_file_info:
        file_name, scan_date, status, risk_level = scanned_file_info
        
        # create label pairs for each field
        labels = [
            
            ("File Name:", file_name),
            ("Scan Date:", scan_date),
            ("Status:", status),
            ("Risk Level:", risk_level)
        ]

        # create label row for each field
        for label_title, result in labels:
            
            # title label
            title_label = tk.Label(
                
                scan_report_page,
                text=label_title,
                font=("Helvetica", 18, "bold"),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            title_label.place(x=50, y=y_offset)
            
            # result label
            result_label = tk.Label(
                scan_report_page,
                text=result,
                font=("Helvetica", 18),
                bg="white",
                padx=13, pady=5,
                anchor="w"
            )
            result_label.place(x=230, y=y_offset)
            
            # padding
            y_offset += 50
           
    # no scan details available 
    else:
        
        no_info = tk.Label(
            
        scan_report_page,
        text="No scanned file information available.",
        font=("Helvetica", 16),
        bg="white",
        pady=10
        )
        no_info.place(x=50, y=y_offset)
        
        # padding
        y_offset += 50

    # if there are details available
    if scan_details:
        
        # loop through details
        for reason, risk_category in scan_details:
            
            # reason label for flag
            reason_label = tk.Label(
                
            scan_report_page,
            text="Reason:",
            font=("Helvetica", 18, "bold"),
            bg="white",
            padx=10, pady=5,
            anchor="w"
            )
            reason_label.place(x=50, y=y_offset)

            # reason result
            reason_result_label = tk.Label(
                
                scan_report_page,
                text=reason,
                font=("Helvetica", 18),
                bg="white",
                padx=13, pady=5,
                anchor="w",
                wraplength=1000
            )
            reason_result_label.place(x=230, y=y_offset)
            
            # padding
            y_offset += 50
            
            
            # label header
            risk_category_label = tk.Label(
                
                scan_report_page,
                text="Risk Category:",
                font=("Helvetica", 18, "bold"),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            risk_category_label.place(x=50, y=y_offset)
            
            # result label
            risk_category_result_label = tk.Label(
                scan_report_page,
                text=risk_category,
                font=("Helvetica", 18),
                bg="white",
                padx=13, pady=5,
                anchor="w"
            )
            risk_category_result_label.place(x=230, y=y_offset)
            
            # padding
            y_offset += 110
            
    # no details available
    else:
        
        no_details = tk.Label(
            
        scan_report_page,
        text="No scan details available.",
        font=("Helvetica", 18),
        bg="white",
        padx=10, pady=10
        )
        no_details.place(x=50, y=y_offset)
        
        # padding
        y_offset += 110
  

    # dictionary linking risk categories to their educational pages
    educational_pages = {
        
        "Executables": executables_page,
        "File Spoofing": file_spoofing_page,
        "Remote Access Control": remote_access_page,
        "Virus": viruses_page,
        "Credential Stealer": credential_stealers_page,
        "Compressed Files": compressed_files_page,
        "Macros": macros_page,
        "Obfuscation": obfuscation_page,
    }

    # check if scan details are available
    if scan_details:
        
        # get last reason and risk category from list of scan results
        _, risk_category = scan_details[-1]

        # check if risk category has corresponding educational page
        if risk_category in educational_pages:
            
            # create button to link to educational page
            educational_button = tk.Button(
                
                scan_report_page,
                text=f"Learn More About {risk_category}",
                font=("Helvetica", 18, "bold"),
                command=lambda: show_page(educational_pages[risk_category])
            )
            educational_button.place(relx=0.35, rely=y_offset / root.winfo_height(), anchor="center")

    # button to scan another file
    scan_another_file_button = tk.Button(
        
        scan_report_page,
        text="Scan Another File",
        font=("Helvetica", 18, "bold"),
        width=20,
        command=lambda: show_page(scan_files_page)
    )
    scan_another_file_button.place(relx=0.7, rely=(y_offset) / root.winfo_height(), anchor="center")

    # show scan report page
    show_page(scan_report_page)


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


# hamburger menu button
hamburger_button = tk.Button(root, text="☰", font=("Helvetica", 30), command=hamburger_menu)
hamburger_button.place(x=10, y=10)

# load and resize image for home button
home_icon_path = "images/home_icon.png"
home_icon_image = Image.open(home_icon_path)
home_icon_image = home_icon_image.resize((70, 70))
home_icon = ImageTk.PhotoImage(home_icon_image)

# home button
home_button = tk.Button(root, image=home_icon, font=("Helvetica", 20), command=lambda: show_page(welcome_page))
home_button.place(x=1200, y=10)

# side menu for hamburger button
# cover 3/4 of the screen
menu_frame = tk.Frame(root, bg="lightgray", width=800, height=1200)

# when program starts position hamburger menu off screen
menu_frame.place(x=-1000, y=0)

# style for hamburger menu frame buttons
style.configure("Custom.TButton", 
                font=("Helvetica", 30, "bold"),
                padding=10,
                relief="solid",
                borderwidth=8, 
                foreground="white", 
                background="#4bb9e6",  
                highlightthickness=0)

# scan files button for hamburger menu frame
scan_files_button = ttkb.Button(
    
    menu_frame,
    text="Scan Files",
    style="Custom.TButton",
    command=lambda: show_page(scan_files_page)
)

# scan history button for hamburger menu frame
scan_history_button = ttkb.Button(
    
    menu_frame,
    text="Scan History",
    style="Custom.TButton",
    command=lambda: show_page(scan_history_page)
)

# educational button for hamburger menu frame
education_button = ttkb.Button(
    
    menu_frame,
    text="Education",
    style="Custom.TButton",
    command=lambda: show_page(education_page)
)

# height of buttons for menu frame buttons
button_height = 225

# placing location for buttons
scan_files_button.place(x=0, y=0, width=800, height=button_height)
scan_history_button.place(x=0, y=button_height, width=800, height=button_height)
education_button.place(x=0, y=button_height * 2, width=800, height=button_height)


# scan files page
scan_files_page = tk.Frame(root)

# takes up entire screen dynamically
scan_files_page.place(relwidth=1, relheight=1)

# scan files header title
scan_files_header = "Scan Files"
scan_files_header_label = tk.Label(
    
    scan_files_page,
    text=scan_files_header,
    font=("Helvetica", 40, "bold"),
    fg="white"
)
scan_files_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# upload file button on scan files page
upload_file_button = tk.Button(scan_files_page, text="Upload File", font=("Helvetica", 20, "bold"), command=upload_file)
upload_file_button.place(relx=0.5, rely=0.8, width=175, height=90, anchor="center")

# style for label for drag and drop area
style.configure("Custom.TLabel",
                font=("Helvetica", 20, "bold"),
                background="#2596be",  
                foreground="white",   
                anchor="center",      
                padding=20) 

# drop area label for drag and drop
drop_area = ttkb.Label(scan_files_page, 
                       text="Drag and drop a file here or click the 'Upload File' button to get started", 
                       style="Custom.TLabel", 
                       wraplength=860, 
                       justify="center",
                       relief="groove") 
drop_area.place(x=200, y=150, width=900, height=300)

# register drop area to accept file drops
drop_area.drop_target_register(DND_FILES)

# bind drop event to call on_drop function
drop_area.dnd_bind('<<Drop>>', on_drop)


# scanning page
scanning_page = tk.Frame(root)

# takes up entire screen dynamically
scanning_page.place(relwidth=1, relheight=1)

# scanning page header text
scanning_header = "Scanning"
scanning_header_label = tk.Label(
    
    scanning_page, 
    text=scanning_header, 
    font=("Helvetica", 40, "bold"), 
    fg="white"
)
scanning_header_label.place(relx=0.5, rely=0.1, anchor="center")

# text to show that file is being scanned
scanning_text = "Scanning file, please wait..."
scanning_text_label = tk.Label(
    
    scanning_page, 
    text=scanning_text, 
    font=("Helvetica", 20, "bold"), 
    fg="white"
)
scanning_text_label.place(relx=0.5, rely=0.2, anchor="center")

# gif size dimensions
gif_width = 250
gif_height = 250

# open gif file
gif = Image.open("images/loading_gif.gif")

# create empty list to hold gif frames
gif_frames = []

# loop through each frame in the gif
for frame_index in range(gif.n_frames):
    
    # go to current frame
    gif.seek(frame_index)
    
    # rezie frame 
    resized_frame = gif.copy().resize((gif_width, gif_height), Image.LANCZOS)
    
    # convert resized frame to tkinter compatible format
    frame_image = ImageTk.PhotoImage(resized_frame.convert("RGBA"))
    
    # add processed frame to list
    gif_frames.append(frame_image)
    
# label to display animated gif
scanning_image_label = tk.Label(scanning_page)
scanning_image_label.place(relx=0.5, rely=0.5, anchor="center")


# function to update gif animation frame by frame
def update_gif(frame_index=0):
    
    # set current frame image
    frame = gif_frames[frame_index]
    scanning_image_label.configure(image=frame)
    
    # determine index of next frame
    next_frame_index = (frame_index + 1) % len(gif_frames)
    
    # schedule next frame update after 33ms
    # 30fps
    root.after(33, update_gif, next_frame_index)
    
# start gif animation loop
update_gif()

# label to show name of selected file
scanning_file_name_label = tk.Label(
    
    scanning_page, 
    text="No file selected", 
    font=("Helvetica", 20, "bold"), 
    fg="black",
    bg="white"
)
scanning_file_name_label.place(relx=0.5, rely=0.75, anchor="center") 

# once a file finished scanning show report
scan_report_page = tk.Frame(root)

# takes up entire screen dynamically
scan_report_page.place(relwidth=1, relheight=1)

# scan history page
scan_history_page = tk.Frame(root)

# takes up entire screen dynamically
scan_history_page.place(relwidth=1, relheight=1)

# scan history header text
scan_history_header = "Scan History"
scan_history_header_label = tk.Label(
    
    scan_history_page,
    text=scan_history_header,
    font=("Helvetica", 40, "bold"),
    fg="white"
)
scan_history_header_label.place(relx=0.5, rely=0.1, anchor="center")

# scan history info text
scan_history_text = "View your previous scans"
scan_history_text_label = tk.Label(
    
    scan_history_page,
    text=scan_history_text,
    font=("Helvetica", 18, "bold"),
    fg="white"
)
scan_history_text_label.place(relx=0.5, rely=0.17, anchor="center")

# canvas to told scrollable scan entries
canvas_scan_history = tk.Canvas(scan_history_page, bg="white", highlightthickness=0, width=1500, height=800)

# vertical scrollbar linked to canvas
scrollbar_scan_history = tk.Scrollbar(scan_history_page, orient="vertical", command=canvas_scan_history.yview, width=20)

# place canvas on page
canvas_scan_history.place(x=200, y=150)

# place scrollbar on page
scrollbar_scan_history.place(x=1255, y=150, height=800)

# create a frame that will sit inside the canvas
# holds scan history rows
scan_rows_frame = tk.Frame(canvas_scan_history, bg="white")

# update scroll region when inner frame resizes
scan_rows_frame.bind("<Configure>", lambda e: canvas_scan_history.configure(scrollregion=canvas_scan_history.bbox("all")))

# add scrollable frame to canvas
canvas_scan_history.create_window((0, 0), window=scan_rows_frame, anchor="nw")

# configure canvas to use scrollbar
canvas_scan_history.configure(yscrollcommand=scrollbar_scan_history.set)

# function to restore mouse wheel scrolling on scan history page
def restore_mousewheel_binding():
    
    # function that runs when the user scrolls mouse wheel
    def on_scan_history_mousewheel(event):
        
        # scroll canvas content vertically when mouse wheel is used
        canvas_scan_history.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # bind mouse wheel event to scan history page
    scan_history_page.bind_all("<MouseWheel>", on_scan_history_mousewheel)


# function to populate scan history page with entires from db
def populate_scan_history(scan_history):

    # remove all existing widgets from scan rows frame
    # avoid duplicates
    for widget in scan_rows_frame.winfo_children():
        
        widget.destroy()
        
    # check if scan history is empty
    if not scan_history:
        
        # display a message indicating no scans are available
        no_scans_label = tk.Label(
            
            scan_rows_frame,
            text="No scans to display, upload a file to scan to get started!",
            font=("Helvetica", 18, "bold"),
        )
        no_scans_label.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="w")
        
        # button to allow user to scan new file
        scan_another_file_history_button = tk.Button(
        scan_rows_frame,
        text="Scan a File",
        font=("Helvetica", 18, "bold"),
        command=lambda: show_page(scan_files_page)
        )
        scan_another_file_history_button.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
        
        return

    # loop through scan history and create UI elements
    for index, (scan_id, file_name, scan_date) in enumerate(scan_history):
        
        # file name
        file_name_label = tk.Label(scan_rows_frame, text=file_name, font=("Helvetica", 18), bg="white")
        file_name_label.grid(row=index, column=0, padx=10, pady=5)

        # scan date
        scan_date_label = tk.Label(scan_rows_frame, text=scan_date, font=("Helvetica", 18), bg="white")
        scan_date_label.grid(row=index, column=1, padx=10, pady=5)

        # view scan button
        view_button = tk.Button(
            
            scan_rows_frame,
            text="View Scan",
            font=("Helvetica", 18, "bold"),
            command=partial(view_scan_details, scan_id)
        )
        
        # placing in grid layout
        view_button.grid(row=index, column=2, padx=10, pady=5)


# function to update scan history view with latest data
def update_scan_history():

    # fetch latest scan history records using controller from db
    scan_history = controller.fetch_scan_history()
    
    # populate scan history UI with fetched data
    populate_scan_history(scan_history)


# function to display specific scan details in a dynamically created page
def view_scan_details(scan_id):
    
    # fetch data of scanned file from controller using scan id
    scanned_file_info, scan_details = controller.get_scan_details_and_info(scan_id)

    # create new dynamic page
    details_page = tk.Frame(root, bg="white")
    
    # takes up entire screen dynamically
    details_page.place(x=0, y=0, relwidth=1, relheight=1)

    # header label
    header_label = tk.Label(
        details_page, 
        text="Scan Details", 
        font=("Helvetica", 40, "bold"),
        fg="white",
    )
    header_label.place(relx=0.5, rely=0.1, anchor="center")

    # vertical starting position for other widgets
    y_offset = 150

    # if there is file info available
    if scanned_file_info:
        
        # unpack data
        file_name, scan_date, status, risk_level = scanned_file_info
        
        # titles and values for file info section
        labels = [
            
            ("File Name:", file_name),
            ("Scan Date:", scan_date),
            ("Status:", status),
            ("Risk Level:", risk_level)
        ]

        # loop through labels to create UI elements for each
        for label_title, result in labels:
            
            # title label
            title_label = tk.Label(
                
                details_page,
                text=label_title,
                font=("Helvetica", 16, "bold"),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            title_label.place(x=50, y=y_offset)
            
            # result label
            result_label = tk.Label(
                
                details_page,
                text=result,
                font=("Helvetica", 16),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            result_label.place(x=210, y=y_offset)
            
            # padding
            y_offset += 50

    # if no data is available
    else:
        no_info = tk.Label(
            
            details_page,
            text="No scanned file information available.",
            font=("Helvetica", 16),
            bg="white",
            pady=10
        )
        no_info.place(x=50, y=y_offset)
        
        # padding
        y_offset += 50

    # if there is data available
    if scan_details:
        
        # loop through each pair
        for reason, risk_category in scan_details:
            
            # header label
            reason_label = tk.Label(
                
                details_page,
                text="Reason:",
                font=("Helvetica", 16, "bold"),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            reason_label.place(x=50, y=y_offset)

            # result label
            reason_result_label = tk.Label(
                
                details_page,
                text=reason,
                font=("Helvetica", 16),
                bg="white",
                padx=10, pady=5,
                anchor="w",
                wraplength=1000
            )
            reason_result_label.place(x=210, y=y_offset)
            
            # padding
            y_offset += 50

            # label header
            risk_category_label = tk.Label(
                
                details_page,
                text="Risk Category:",
                font=("Helvetica", 16, "bold"),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            risk_category_label.place(x=50, y=y_offset)

            # result label
            risk_category_result_label = tk.Label(
                
                details_page,
                text=risk_category,
                font=("Helvetica", 16),
                bg="white",
                padx=10, pady=5,
                anchor="w"
            )
            risk_category_result_label.place(x=210, y=y_offset)
            
            # padding
            y_offset += 70

    # if no data available
    else:
        no_details = tk.Label(
            
            details_page,
            text="No scan details available.",
            font=("Helvetica", 16),
            bg="white",
            padx=10, pady=10
        )
        no_details.place(x=50, y=y_offset)
        
        # padding
        y_offset += 70
        
    # mapping from risk categories to educational pages
    educational_pages = {
        
        "Executables": executables_page,
        "File Spoofing": file_spoofing_page,
        "Remote Access Control": remote_access_page,
        "Virus": viruses_page,
        "Credential Stealer": credential_stealers_page,
        "Compressed Files": compressed_files_page,
        "Macros": macros_page,
        "Obfuscation": obfuscation_page,
    }
    
    # if scan details available
    if scan_details:
        
        # take last risk category to link education
        _, risk_category = scan_details[-1]

        # check if detected risk category has matching educational page
        if risk_category in educational_pages:
            
            # button to link to educational page
            educational_button = tk.Button(
                
                details_page,
                text=f"Learn More About {risk_category}",
                font=("Helvetica", 18, "bold"),
                command=lambda: show_page(educational_pages[risk_category])
            )
            educational_button.place(x=425, y=y_offset)
            
            # padding
            y_offset += 60

    # button to go back to scan history
    # destroys current page
    back_button = tk.Button(
        
        details_page,
        text="Back",
        font=("Helvetica", 18, "bold"),
        command=lambda: details_page.destroy()
    )
    back_button.place(x=600, y=y_offset)
    
    # show hamburger button
    hamburger_button.tkraise()
    
    # show home button
    home_button.tkraise()
    
# education page
education_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
education_page.place(relwidth=1, relheight=1)

# education header
education_header = "Education"
education_header_label = tk.Label(
    
    education_page,
    text=education_header,
    font=("Helvetica", 40, "bold"),
    fg="black"
)
education_header_label.place(relx=0.5, rely=0.1, anchor="center")

# education info
education_text = "Learn about different types of malware using the 'Malware' button"
education_text_label = tk.Label(
    
    education_page,
    text=education_text,
    font=("Helvetica", 20, "bold"),
    fg="black"
)
education_text_label.place(relx=0.5, rely=0.21, anchor="center")

# education info
education_text1 = "Or test your knowledge through 'Quizzes'"
education_text1_label = tk.Label(
    
    education_page,
    text=education_text1,
    font=("Helvetica", 20, "bold"),
    fg="black"
)
education_text1_label.place(relx=0.5, rely=0.29, anchor="center")

# load and resize image for malware button
malware_image_path = "images/malware.png"
malware_image = Image.open(malware_image_path).resize((110, 120))
malware_icon = ImageTk.PhotoImage(malware_image)

# malware button on education page
education_malware_button = tk.Button(
    
    education_page,
    text="Malware & Vulnerabilities",
    font=("Helvetica", 20, "bold"),
    image=malware_icon,
    compound="top",
    command=lambda: show_page(malware_page),
    pady=15
)
# prevent garbage collection
education_malware_button.image = malware_icon

# load and resize image for quiz button
quiz_image_path = "images/quiz.png"
quiz_image = Image.open(quiz_image_path).resize((110, 120))
quiz_icon = ImageTk.PhotoImage(quiz_image)

# quiz button on education page
education_quiz_button = tk.Button(
    
    education_page,
    text="Quizzes",
    font=("Helvetica", 20, "bold"),
    image=quiz_icon,
    compound="top",
    command=lambda: show_page(quiz_page),
    pady=15
)
# prevent garbage collection
education_quiz_button.image = quiz_icon

# calculate frame dimensions before using them
root.update_idletasks()

# get current width of application window
frame_width = root.winfo_width()

# if width too small - window not fully loaded
if frame_width < 100:
    
    # fallback
    frame_width = 1280

# layout constants for education buttons
edu_btn_width = 400
edu_btn_height = 250
edu_btn_gap = 100

# total width of both buttons and gap
edu_total_width = (edu_btn_width * 2) + edu_btn_gap

# center buttons horizontally
edu_start_x = (frame_width - edu_total_width) // 2

# vertical y position for both buttons
edu_y_position = 250

# place malware button using calculated coordinates
education_malware_button.place(
    
    x=edu_start_x,
    y=edu_y_position,
    width=edu_btn_width,
    height=edu_btn_height
)

# place malware button using calculated coordinates
education_quiz_button.place(
    
    x=edu_start_x + edu_btn_width + edu_btn_gap,
    y=edu_y_position,
    width=edu_btn_width,
    height=edu_btn_height
)

# quiz page
quiz_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_page.place(relwidth=1, relheight=1)

# quiz header
quiz_header = "Quizzes"
quiz_header_label = tk.Label(
    
    quiz_page, 
    text=quiz_header, 
    font=("Helvetica", 40, "bold"),
    fg="black", 
    bg="white"
)
quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")


# quiz info
quiz_text_1 = "Test your knowledge from what you learned!"
quiz_text_label_1 = tk.Label(
    
    quiz_page, 
    text=quiz_text_1, 
    font=("Helvetica", 20, "bold"),
    fg="black", 
    bg="white", 
    wraplength=1000
)
quiz_text_label_1.place(relx=0.5, rely=0.2, anchor="center")


# quiz info
quiz_text_2 = "Choose a quiz topic to get started!"
quiz_text_label_2 = tk.Label(
    
    quiz_page, 
    text=quiz_text_2, 
    font=("Helvetica", 20, "bold"),
    fg="black", 
    bg="white", 
    wraplength=1000
)
quiz_text_label_2.place(relx=0.5, rely=0.25, anchor="center")

# load and resize image for green check image
check_image_path = "images/green_check.png"
check_image = Image.open(check_image_path)
check_image = check_image.resize((150, 45))
check_icon = ImageTk.PhotoImage(check_image)

# dictionary to store referecnes of all checkmark labels for each quiz
check_labels_quiz = {}

# function to dynamically place quiz buttons and checkmarks
def place_quiz_buttons():
    
    # get list of quizzes user has passed from controller
    passed_quizzes = controller.get_passed_quizzes()
        
    # get current window width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # button size
    button_width = 350
    button_height = 80
    
    # padding
    vertical_spacing = 20
    checkmark_offset = 20

    # x position for buttons on left column
    left_x = 0.1 * window_width
    
    # x position for buttons on right column
    right_x = 0.55 * window_width

    # stating y position so all buttons are vertically centered
    starting_y = (window_height - (4 * button_height + 3 * vertical_spacing)) // 2 + 70

    # each quiz button with its label and x,y coordinates
    buttons = [
        
        (quiz_executables_button, "Executables", left_x, starting_y),
        (quiz_file_spoofing_button, "File Spoofing", left_x, starting_y + button_height + vertical_spacing),
        (quiz_obfuscation_button, "Obfuscation", left_x, starting_y + 2 * (button_height + vertical_spacing)),
        (quiz_remote_access_button, "Remote Access Control", left_x, starting_y + 3 * (button_height + vertical_spacing)),
        (quiz_viruses_button, "Viruses", right_x, starting_y),
        (quiz_credential_stealers_button, "Credential Stealers", right_x, starting_y + button_height + vertical_spacing),
        (quiz_compressed_files_button, "Compressed Files", right_x, starting_y + 2 * (button_height + vertical_spacing)),
        (quiz_macros_button, "Macros", right_x, starting_y + 3 * (button_height + vertical_spacing)),
    ]

    # loop through each button and place it
    for button, quiz, x, y in buttons:
        
        # place button
        button.place(x=x, y=y, width=button_width, height=button_height)

        # check if quiz has been passed
        if quiz in passed_quizzes:
            
            # if check mark already exists
            if quiz in check_labels_quiz:
                
                # reposition it
                check_labels_quiz[quiz].place(x=x + button_width + checkmark_offset, y=y + 25)
                
            # check mark does not exist
            else:
                
                # new check mark label and place it
                check_label = tk.Label(quiz_page, image=check_icon, bg="white")
                check_label.place(x=x + button_width + checkmark_offset, y=y + 25)
                
                # save reference to avoid duplication
                check_labels_quiz[quiz] = check_label

# bind resizing of window to replace quiz buttons when quiz page is visible
root.bind("<Configure>", lambda event: place_quiz_buttons() if quiz_page.winfo_ismapped() else None)

# quiz page buttons
# executables quiz button
quiz_executables_button = tk.Button(
    
    quiz_page,
    text="Executables",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_executables)
)

# file spoofing quiz button
quiz_file_spoofing_button = tk.Button(
    
    quiz_page,
    text="File Spoofing",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_file_spoofing)
)

# obfuscation quiz button
quiz_obfuscation_button = tk.Button(
    
    quiz_page,
    text="Obfuscation & High Entropy",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_obfuscation)
)

# rat quiz button
quiz_remote_access_button = tk.Button(
    
    quiz_page,
    text="Remote Access Tools",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_rats)
)

# viruses quiz button
quiz_viruses_button = tk.Button(
    
    quiz_page,
    text="Viruses",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_viruses)
)

# credential stealers quiz button
quiz_credential_stealers_button = tk.Button(
    
    quiz_page,
    text="Credential Stealers",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_credential_stealers)
)

# compressed files quiz button
quiz_compressed_files_button = tk.Button(
    
    quiz_page,
    text="Compressed Files",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_compressed_files)
)

# macros quiz button
quiz_macros_button = tk.Button(
    
    quiz_page,
    text="Macros",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(quiz_macros)
)

# dictionary to hold check mark labels for malware page
check_labels = {}

# malware page
malware_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
malware_page.place(relwidth=1, relheight=1)

# malware header
malware_header = "Malware & Vulnerabilities"
malware_header_label = tk.Label(
    
    malware_page, 
    text=malware_header, 
    font=("Helvetica", 40, "bold"), 
    fg="black",
    bg="white",
)
malware_header_label.place(relx=0.5, rely=0.1, anchor="center")

# malware page info
explanation_text_1 = "Below are various topics about malware and vulnerabilities"
explanation_label_1 = tk.Label(
    
    malware_page, 
    text=explanation_text_1, 
    font=("Helvetica", 20, "bold"),
    fg="black", 
    bg="white", 
    wraplength=1000
)
explanation_label_1.place(relx=0.5, rely=0.2, anchor="center")

# malware page info
explanation_text_2 = "Click on a topic to start learning!"
explanation_label_2 = tk.Label(
    
    malware_page, 
    text=explanation_text_2, 
    font=("Helvetica", 20, "bold"),
    fg="black", 
    bg="white", 
    wraplength=1000
)
explanation_label_2.place(relx=0.5, rely=0.25, anchor="center")


# function to dynamically place educational buttons and checkmarks
def place_buttons_dynamically():
    
    # get list of topics user has read from controller
    read_topics = controller.get_read_topics()
    
    # get current window width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # button size
    button_width = 350
    button_height = 80
    
    # padding
    vertical_spacing = 20
    checkmark_offset = 20

    # x position for buttons on left column
    left_x = 0.1 * window_width
    
    # x position for buttons on right column
    right_x = 0.55 * window_width
    
    # stating y position so all buttons are vertically centered
    starting_y = (window_height - (4 * button_height + 3 * vertical_spacing)) // 2 + 70
    
    # each educational button with its label and x,y coordinates
    buttons = [
        
        (executables_button, "Executables", left_x, starting_y),
        (file_spoofing_button, "File Spoofing", left_x, starting_y + button_height + vertical_spacing),
        (obfuscation_button, "Obfuscation", left_x, starting_y + 2 * (button_height + vertical_spacing)),
        (remote_access_button, "Remote Access Control", left_x, starting_y + 3 * (button_height + vertical_spacing)),
        (viruses_button, "Viruses", right_x, starting_y),
        (credential_stealers_button, "Credential Stealers", right_x, starting_y + button_height + vertical_spacing),
        (compressed_files_button, "Compressed Files", right_x, starting_y + 2 * (button_height + vertical_spacing)),
        (macros_button, "Macros", right_x, starting_y + 3 * (button_height + vertical_spacing)),
    ]
    
    # loop through each button and place it
    for button, topic, x, y in buttons:
        
        # place button
        button.place(x=x, y=y, width=button_width, height=button_height)

        # check if topic has been read
        if topic in read_topics:
            
            # if check mark already exists
            if topic in check_labels:
                
                # reposition it
                check_labels[topic].place(x=x + button_width + checkmark_offset, y=y + 25)
                
            # check mark does not exist
            else:
                
                # new check mark label and place it
                check_label = tk.Label(malware_page, image=check_icon, bg="white")
                check_label.place(x=x + button_width + checkmark_offset, y=y + 25)
                
                # save reference to avoid duplication
                check_labels[topic] = check_label

# bind resizing of window to replace educational buttons when malware page is visible
root.bind("<Configure>", lambda event: place_buttons_dynamically())

# educational buttons
# executables education button
executables_button = tk.Button(
    
    malware_page,
    text="Executables",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(executables_page)
)

# file spoofing education button
file_spoofing_button = tk.Button(
    
    malware_page,
    text="File Spoofing",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(file_spoofing_page)
)

# obfuscation education button
obfuscation_button = tk.Button(
    
    malware_page,
    text="Obfuscation & High Entropy",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation_page)
)

# rat education button
remote_access_button = tk.Button(
    
    malware_page,
    text="Remote Access Tools",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(remote_access_page)
)

# viruses education button
viruses_button = tk.Button(
    
    malware_page,
    text="Viruses",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(viruses_page)
)

# credential stealers education button
credential_stealers_button = tk.Button(
    
    malware_page,
    text="Credential Stealers",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(credential_stealers_page)
)

# compressed files education button
compressed_files_button = tk.Button(
    malware_page,
    
    text="Compressed Files",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(compressed_files_page)
)

# macros education button
macros_button = tk.Button(
    
    malware_page,
    text="Macros",
    font=("Helvetica", 20, "bold"),
    command=lambda: show_page(macros_page)
)

# function to create bullet point with text in educational pages
def create_bullet_point_edu(parent, text, x, y, wraplength=700, font=("Helvetica", 20)):
    
    # bullet symbol using label
    bullet_label = tk.Label(parent, text="•", font=font, bg="white", anchor="w")
    bullet_label.place(x=x, y=y)
    
    # label where text goes beside bullet point 
    text_label = tk.Label(
        
        parent,
        text=text,
        font=font,
        bg="white",
        wraplength=wraplength,
        anchor="w",
        justify="left"
    )
    text_label.place(x=x + 20, y=y)
    
    # padding
    spacing = 15
    
    # return updated y position for next bullet below
    return text_label.winfo_reqheight() + y + spacing

# executables page
executables_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
executables_page.place(relwidth=1, relheight=1)

# executables header
executables_header = "Executables"
executables_header_label = tk.Label(
    
    executables_page, 
    text=executables_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
executables_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
subheading = tk.Label(
    
    executables_page, 
    text="What are Executables?", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
subheading.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_are_executables = [
    
    "Executables are files that contain instructions for a computer to perform specific tasks or run programs.",
    "When these files are executed, they interact with the computer's operating system and launch applications.",
    "List of executable file extensions: '.exe', '.bat', '.cmd', '.sh', '.bin', '.run', '.py', '.pl', '.php', '.rb', '.jar', '.apk', '.com', '.msi', '.vbs', '.wsf', '.gadget'."
]

# loop through each list text 
for point in what_are_executables:
    
    # create bullet point
    y_start = create_bullet_point_edu(executables_page, point, 50, y_start)

# load and resize image
executables_image = Image.open("images/executable.png")
executables_image = executables_image.resize((400,400), Image.LANCZOS)
executables_image = ImageTk.PhotoImage(executables_image)
executables_image_label = tk.Label(executables_page, image=executables_image)

# place image right of text
executables_image_label.place(relx=0.6, rely=0.2)

# back button to return to previous page
back_button = tk.Button(
    
    executables_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    executables_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page1)
)
next_button.place(relx=0.55, rely=0.8, anchor="center") 

# progress label of current page
progress_label = tk.Label(
    
    executables_page, 
    text="25% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label.place(relx=0.5, rely=0.9, anchor="center")

# executables
executables_page1 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
executables_page1.place(relwidth=1, relheight=1)

# executables header
executables1_header = "Executables"
executables1_header_label = tk.Label(
    
    executables_page1, 
    text=executables1_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
executables1_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title1 = tk.Label(
    
    executables_page1, 
    text="Why are Executables Dangerous?", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title1.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150 

# info
why_dangerous = [
    
    "Executables are dangerous because they interact with the computer system. It gives attackers direct access to computers which will allow them to maliciously modify the system.",
    "Attackers disguise malicious payloads in seemingly safe executables to gain unauthorized access to the victim's computer.",
    "Executables are used to modify system settings and run automatically on boot up and in the background."
]

# loop through each list text 
for point in why_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(executables_page1, point, 50, y_start)

# load and resize image
executables_image1 = Image.open("images/hacker1.png")
executables_image1 = executables_image1.resize((400, 400), Image.LANCZOS)
executables_image1 = ImageTk.PhotoImage(executables_image1)
executables_image1_label = tk.Label(executables_page1, image=executables_image1)

# place image right of text
executables_image1_label.place(relx=0.6, rely=0.2)

# back button to return to previous page
back_button1 = tk.Button(
    
    executables_page1,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page)
)
back_button1.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button1 = tk.Button(
    
    executables_page1,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page2)
)
next_button1.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_executables1 = tk.Label(
    
    executables_page1, 
    text="50% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_executables1.place(relx=0.5, rely=0.9, anchor="center")

# executables page
executables_page2 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
executables_page2.place(relwidth=1, relheight=1)

# executables header
executables2_header = "Executables"
executables2_header_label = tk.Label(
    
    executables_page2, 
    text=executables2_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
executables2_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    executables_page2, 
    text="How Executables are Obtained", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_obtained = [
    
    "Email attachments through phishing links",
    "Fake software downloads",
    "USB drives that contain auto-run executables",
    "Hidden downloaded files when visiting malicious websites"
]

# loop through each list text 
for point in how_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(executables_page2, point, 50, y_start)

# load and resize image
executables_image2 = Image.open("images/warning1.png")
executables_image2 = executables_image2.resize((400, 400), Image.LANCZOS)
executables_image2 = ImageTk.PhotoImage(executables_image2)
executables_image2_label = tk.Label(executables_page2, image=executables_image2)

# place image right of text
executables_image2_label.place(relx=0.6, rely=0.2)

# back button to return to previous page
back_button2 = tk.Button(
    
    executables_page2,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page1)
)
back_button2.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button2 = tk.Button(
    executables_page2,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page3)
)
next_button2.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_executables2 = tk.Label(
    executables_page2, 
    text="75% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_executables2.place(relx=0.5, rely=0.9, anchor="center")

# executables page
executables_page3 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
executables_page3.place(relwidth=1, relheight=1)

# executables header
executables3_header = "Executables"
executables3_header_label = tk.Label(
    
    executables_page3, 
    text=executables3_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
executables3_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title3 = tk.Label(
    
    executables_page3, 
    text="Prevention Tips", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title3.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info 
prevention_tips = [
    
    "Only download from trusted official websites.",
    "Ensure you have real-time scanning enabled.",
    "Restrict user permissions to prevent unauthorized access."
]

# loop through each list text
for point in prevention_tips:
    
     # create bullet point
    y_start = create_bullet_point_edu(executables_page3, point, 50, y_start)

# load and resize image
executables_image3 = Image.open("images/safe4.png")
executables_image3 = executables_image3.resize((400, 300), Image.LANCZOS)
executables_image3 = ImageTk.PhotoImage(executables_image3)
executables_image3_label = tk.Label(executables_page3, image=executables_image3)

# place image right of text
executables_image3_label.place(relx=0.6, rely=0.2)

# back button to return to previous page
back_button3 = tk.Button(
    
    executables_page3,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(executables_page2)
)
back_button3.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button3 = tk.Button(
    
    executables_page3,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_executables)
)
next_button3.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_executables3 = tk.Label(
    executables_page3, 
    text="100% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_executables3.place(relx=0.5, rely=0.9, anchor="center")

# file Spoofing page
file_spoofing_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
file_spoofing_page.place(relwidth=1, relheight=1)

# header
file_spoofing_header = "File Spoofing"
file_spoofing_header_label = tk.Label(
    
    file_spoofing_page, 
    text=file_spoofing_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
file_spoofing_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    file_spoofing_page, 
    text="What is Spoofing?", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_is_spoofing = [
    
    "File spoofing is a technique done by attackers to disguise a malicious file as a safe one.",
    "They do this by altering the extension of the file which affects how the computer operating system reads the file.",
    "Look out for double file extensions such as image.jpg.exe",
    "File icons can be spoofed where a trusted application icon is applied to the malicious file"
]

# loop through each list text 
for point in what_is_spoofing:
    
    # create bullet point
    y_start = create_bullet_point_edu(file_spoofing_page, point, 50, y_start)

# load and resize image
file_spoofing_image = Image.open("images/x_file.png")
file_spoofing_image = file_spoofing_image.resize((400, 300), Image.LANCZOS)
file_spoofing_image = ImageTk.PhotoImage(file_spoofing_image)
file_spoofing_image_label = tk.Label(file_spoofing_page, image=file_spoofing_image)

# place image right of text
file_spoofing_image_label.place(relx=0.6, rely=0.2)

# back button to return to previous page
back_button = tk.Button(
    
    file_spoofing_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    file_spoofing_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_file_spoofing = tk.Label(
    
    file_spoofing_page, 
    text="25% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_file_spoofing.place(relx=0.5, rely=0.9, anchor="center")


# file spoofing page
file_spoofing1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
file_spoofing1_page.place(relwidth=1, relheight=1)

# header
file_spoofing1_header = "File Spoofing"
file_spoofing1_header_label = tk.Label(
    
    file_spoofing1_page, 
    text=file_spoofing1_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
file_spoofing1_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    file_spoofing1_page, 
    text="Why File Spoofing is Dangerous", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_dangerous = [
    
    "Users might unknowingly open malicious files because they appear harmless.",
    "Sometimes, security software does not always recognize manipulated extensions.",
    "Spoofed files tend to contain malicious code that installs malware, steals information, or compromises the operating system."
]

# loop through each list text 
for point in why_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(file_spoofing1_page, point, 50, y_start)

# load and resize image
file_spoofing_image1 = Image.open("images/hacker2.png")
file_spoofing_image1 = file_spoofing_image1.resize((400, 400), Image.LANCZOS)
file_spoofing_image1 = ImageTk.PhotoImage(file_spoofing_image1)
file_spoofing_image1_label = tk.Label(file_spoofing1_page, image=file_spoofing_image1)

# place image right of text
file_spoofing_image1_label.place(relx=0.6, rely=0.25)

# back button to return to previous page
back_button = tk.Button(
    
    file_spoofing1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    file_spoofing1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_file_spoofing1 = tk.Label(
    
    file_spoofing1_page, 
    text="50% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_file_spoofing1.place(relx=0.5, rely=0.9, anchor="center")

# file Spoofing page
file_spoofing2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
file_spoofing2_page.place(relwidth=1, relheight=1)

# header
file_spoofing2_header = "File Spoofing"
file_spoofing2_header_label = tk.Label(
    
    file_spoofing2_page, 
    text=file_spoofing2_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
file_spoofing2_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    file_spoofing2_page, 
    text="How Spoofed Files are Obtained", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_obtained = [
    
    "Embedded in USB drives dropped in public areas by attackers.",
    "Sent via email with file extensions hidden using Unicode tricks.",
    "Downloaded as attachments from social media messages",
    "Hidden downloaded files when visiting malicious websites"
]

# loop through each list text 
for point in how_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(file_spoofing2_page, point, 50, y_start)

# load and resize image
file_spoofing_image2 = Image.open("images/steal.png")
file_spoofing_image2 = file_spoofing_image2.resize((300, 300), Image.LANCZOS)
file_spoofing_image2 = ImageTk.PhotoImage(file_spoofing_image2)
file_spoofing_image2_label = tk.Label(file_spoofing2_page, image=file_spoofing_image2)

# place image right of text
file_spoofing_image2_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    file_spoofing2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    file_spoofing2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_file_spoofing2 = tk.Label(
    file_spoofing2_page, 
    text="75% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_file_spoofing2.place(relx=0.5, rely=0.9, anchor="center")

# file Spoofing page
file_spoofing3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
file_spoofing3_page.place(relwidth=1, relheight=1)

# header
file_spoofing3_header = "File Spoofing"
file_spoofing3_header_label = tk.Label(
    
    file_spoofing3_page, 
    text=file_spoofing3_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
file_spoofing3_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    file_spoofing3_page, 
    text="Prevention Tips", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Enable viewing of full file extensions in your operating system.",
    "Be cautious of file names with excessive spacing, dots, or strange characters.",
    "Avoid opening files from unknown sources, even if the icon or name looks familiar.",
    "Only download from trusted official websites."
]

# loop through each list text 
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(file_spoofing3_page, point, 50, y_start)

# load and resize image
file_spoofing_image3 = Image.open("images/safe2.png")
file_spoofing_image3 = file_spoofing_image3.resize((300, 300), Image.LANCZOS)
file_spoofing_image3 = ImageTk.PhotoImage(file_spoofing_image3)
file_spoofing_image3_label = tk.Label(file_spoofing3_page, image=file_spoofing_image3)

# place image right of text
file_spoofing_image3_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    file_spoofing3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(file_spoofing2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    file_spoofing3_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_file_spoofing)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_file_spoofing3 = tk.Label(
    
    file_spoofing3_page, 
    text="100% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_file_spoofing3.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation_page.place(relwidth=1, relheight=1)

# header
obfuscation_header = "Obfuscation & High Entropy"
obfuscation_header_label = tk.Label(
    
    obfuscation_page, 
    text=obfuscation_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    obfuscation_page, 
    text="What is Obfuscation", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_is_obfuscation = [
    
    "Obfuscation is a technique done to make a file difficult to understand or analyse.",
    "Attackers do this to hide the true nature of their malicious files.",
    "An example of obfuscation is code packing, which means hiding the real code by compressing it into a file that only unpacks and runs when opened."

]

# loop through each list text
for point in what_is_obfuscation:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation_page, point, 50, y_start)

# load and resize image
obfuscation_image = Image.open("images/confused.png")
obfuscation_image = obfuscation_image.resize((300, 300), Image.LANCZOS)
obfuscation_image = ImageTk.PhotoImage(obfuscation_image)
obfuscation_image_label = tk.Label(obfuscation_page, image=obfuscation_image)

# place image right of text
obfuscation_image_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation05_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation_page = tk.Label(
    
    obfuscation_page, 
    text="17% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation_page.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation05_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation05_page.place(relwidth=1, relheight=1)

# header
obfuscation05_header = "Obfuscation & High Entropy"
obfuscation05_header_label = tk.Label(
    
    obfuscation05_page, 
    text=obfuscation05_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation05_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    obfuscation05_page, 
    text="What is Obfuscation - continued", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
obfuscation_continued = [
    
    "Obfuscation can be using encoding methods to hide malicious scripts.",
    "It can also be changing file code to meaningless characters like 'a1b2c3' to make it harder to read or understand.",
    "Obfuscation may also involve encrypting important strings like file paths so attackers can hide what the file is really doing."
]

# loop through each list text
for point in obfuscation_continued:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation05_page, point, 50, y_start)

# load and resize image
obfuscation05_image = Image.open("images/confused.png")
obfuscation05_image = obfuscation05_image.resize((300, 300), Image.LANCZOS)
obfuscation05_image = ImageTk.PhotoImage(obfuscation05_image)
obfuscation05_image_label = tk.Label(obfuscation05_page, image=obfuscation05_image)

# place image right of text
obfuscation05_image_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation05_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation05_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation05_page = tk.Label(
    
    obfuscation05_page, 
    text="34% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation05_page.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation1_page.place(relwidth=1, relheight=1)

# header
obfuscation1_header = "Obfuscation & High Entropy"
obfuscation1_header_label = tk.Label(
    
    obfuscation1_page, 
    text=obfuscation1_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation1_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    obfuscation1_page, 
    text="What is High Entropy", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_is_high_entropy = [
    
    "High entropy refers to data that appears random and lacks any recognisable patterns.",
    "This is done to make malware detection more difficult.",
    "For example, imagine all the letters in the alphabet are scrambled in a random order. It becomes very difficult to understand what the message means because nothing is in the usual place."
]

# loop through each list text
for point in what_is_high_entropy:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation1_page, point, 50, y_start)

# load and resize image
obfuscation_image1 = Image.open("images/confusing.png")
obfuscation_image1 = obfuscation_image1.resize((300, 300), Image.LANCZOS)
obfuscation_image1 = ImageTk.PhotoImage(obfuscation_image1)
obfuscation_image1_label = tk.Label(obfuscation1_page, image=obfuscation_image1)

# place image right of text
obfuscation_image1_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation05_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation1_page = tk.Label(
    
    obfuscation1_page, 
    text="51% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation1_page.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation2_page.place(relwidth=1, relheight=1)

# header
obfuscation2_header = "Obfuscation & High Entropy"
obfuscation2_header_label = tk.Label(
    
    obfuscation2_page, 
    text=obfuscation2_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation2_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    obfuscation2_page, 
    text="Why Obfuscation & High Entropy is Dangerous", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_dangerous = [
    
    "Security software relies on patterns to detect malware. Obfuscation hides these patterns which makes malicious files harder to detect.",
    "Obfuscated code conceals malicious payloads until it's executed.",
    "High entropy files are difficult for experts to reverse engineer or study.",
    "Obfuscated and high entropy files may avoid detection only until they are executed."
]

# loop through each list text
for point in why_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation2_page, point, 50, y_start)

# load and resize image
obfuscation_image2 = Image.open("images/hacker3.png")
obfuscation_image2 = obfuscation_image2.resize((300, 300), Image.LANCZOS)
obfuscation_image2 = ImageTk.PhotoImage(obfuscation_image2)
obfuscation_image2_label = tk.Label(obfuscation2_page, image=obfuscation_image2)

# place image right of text
obfuscation_image2_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation2_page = tk.Label(
    
    obfuscation2_page, 
    text="68% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation2_page.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation3_page.place(relwidth=1, relheight=1)

# header
obfuscation3_header = "Obfuscation & High Entropy"
obfuscation3_header_label = tk.Label(
    
    obfuscation3_page, 
    text=obfuscation3_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation3_header_label.place(relx=0.5, rely=0.1, anchor="center") 

# header
section_title = tk.Label(
    
    obfuscation3_page, 
    text="How Obfuscated & High Entropy Files are Obtained", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_obtained = [
    
    "Downloaded from malicious websites or pirated software.",
    "Files disguised as useful programs like computer cleaners or optimizers.",
    "Shared in online forums disguised as game mods or tools.",
    "Received via email as strange-looking attachments with random names."
]


# loop through each list text
for point in how_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation3_page, point, 50, y_start)

# load and resize image
obfuscation_image3 = Image.open("images/warning.png")
obfuscation_image3 = obfuscation_image3.resize((300, 300), Image.LANCZOS)
obfuscation_image3 = ImageTk.PhotoImage(obfuscation_image3)
obfuscation_image3_label = tk.Label(obfuscation3_page, image=obfuscation_image3)

# place image right of text
obfuscation_image3_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation3_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation4_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation3_page = tk.Label(
    
    obfuscation3_page, 
    text="85% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation3_page.place(relx=0.5, rely=0.9, anchor="center")

# obfuscation page
obfuscation4_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
obfuscation4_page.place(relwidth=1, relheight=1)

# header
obfuscation4_header = "Obfuscation & High Entropy"
obfuscation4_header_label = tk.Label(
    
    obfuscation4_page, 
    text=obfuscation4_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
obfuscation4_header_label.place(relx=0.5, rely=0.1, anchor="center") 

# header
section_title = tk.Label(
    
    obfuscation4_page, 
    text="Prevention Tips", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Watch for files with strange names such as 'a9x$gh29.exe'.",
    "Look for abnormally small or large file sizes.",
    "Be careful with files that trigger antivirus warnings but still run.",
    "Avoid running unknown programs that suddenly unpack or install extra files."
]


# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(obfuscation4_page, point, 50, y_start)

# load and resize image
obfuscation_image4 = Image.open("images/safe3.png")
obfuscation_image4 = obfuscation_image4.resize((300, 300), Image.LANCZOS)
obfuscation_image4 = ImageTk.PhotoImage(obfuscation_image4)
obfuscation_image4_label = tk.Label(obfuscation4_page, image=obfuscation_image4)

# place image right of text
obfuscation_image4_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    obfuscation4_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(obfuscation3_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    obfuscation4_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_obfuscation)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_obfuscation4_page = tk.Label(
    
    obfuscation4_page, 
    text="100% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_obfuscation4_page.place(relx=0.5, rely=0.9, anchor="center")

# rat page
remote_access_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
remote_access_page.place(relwidth=1, relheight=1)

# header
remote_access_header = "Remote Access Tools"
remote_access_header_label = tk.Label(
    
    remote_access_page, 
    text=remote_access_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
remote_access_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    remote_access_page, 
    text="What are Remote Access Tools", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_is_rat = [
    
    "Remote access tools (RATs) are software applications that allow users to access and control a computer remotely.",
    "This control can be done over a network or the internet.",
    "These tools are used by companies and organizations for IT support or remote work.",
    "Some examples of safe tools include TeamViewer and AnyDesk."
]

# loop through each list text
for point in what_is_rat:
    
    # create bullet point
    y_start = create_bullet_point_edu(remote_access_page, point, 50, y_start)

# load and resize image
rat_image = Image.open("images/hacker4.png")
rat_image = rat_image.resize((300, 300), Image.LANCZOS)
rat_image = ImageTk.PhotoImage(rat_image)
rat_image_label = tk.Label(remote_access_page, image=rat_image)

# place image right of text
rat_image_label.place(relx=0.6, rely=0.3)

# back button to return to previous page
back_button = tk.Button(
    
    remote_access_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    remote_access_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_access_page = tk.Label(
    remote_access_page, 
    text="25% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_remote_access_page.place(relx=0.5, rely=0.9, anchor="center")

# rat page
remote_access1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
remote_access1_page.place(relwidth=1, relheight=1)

# header
remote_access_header = "Remote Access Tools"
remote_access_header_label = tk.Label(
    
    remote_access1_page, 
    text=remote_access_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
remote_access_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    remote_access1_page, 
    text="Why are Remote Access Tools Dangerous", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_rats_dangerous = [
    
    "Attackers use malicious RATs to gain unauthorized access to computer systems.",
    "Malicious RATs work in the background quietly, without the victim knowing of its presence.",
    "They can be used to monitor activity, steal data, install malware, or control the victim's computer.",
    "RATs serve as backdoors, allowing attackers to enter the victim's system at any time."
]

# loop through each list text
for point in why_rats_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(remote_access1_page, point, 50, y_start)

# load and resize image
rat_image1 = Image.open("images/noaccess.png")
rat_image1 = rat_image1.resize((300, 300), Image.LANCZOS)
rat_image1 = ImageTk.PhotoImage(rat_image1)
rat_image1_label = tk.Label(remote_access1_page, image=rat_image1)

# place image right of text
rat_image1_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    remote_access1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    remote_access1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_access1_page = tk.Label(
    
    remote_access1_page, 
    text="50% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_remote_access1_page.place(relx=0.5, rely=0.9, anchor="center")

# rat page
remote_access2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
remote_access2_page.place(relwidth=1, relheight=1)

# header
remote_access_header = "Remote Access Tools"
remote_access_header_label = tk.Label(
    
    remote_access2_page, 
    text=remote_access_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
remote_access_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    remote_access2_page, 
    text="How Remote Access Tools are Obtained", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_rats_obtained = [
    
    "RATs can be obtained through phishing emails via attachments or links.",
    "Legitimate-seeming applications could be bundled with malicious RATs.",
    "Malicious websites may have dangerous download links that trigger the download of a RAT.",
    "Scammers pretend to be tech support from big companies to trick people into giving them access to their computers."
]

# loop through each list text
for point in how_rats_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(remote_access2_page, point, 50, y_start)

# load and resize image
rat_image2 = Image.open("images/scam.png")
rat_image2 = rat_image2.resize((300, 300), Image.LANCZOS)
rat_image2 = ImageTk.PhotoImage(rat_image2)
rat_image2_label = tk.Label(remote_access2_page, image=rat_image2)

# place image right of text
rat_image2_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    remote_access2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    remote_access2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_access2_page = tk.Label(
    
    remote_access2_page, 
    text="75% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_remote_access2_page.place(relx=0.5, rely=0.9, anchor="center")

# rat page
remote_access3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
remote_access3_page.place(relwidth=1, relheight=1)

# header
remote_access_header = "Remote Access Tools"
remote_access_header_label = tk.Label(
    
    remote_access3_page, 
    text=remote_access_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
remote_access_header_label.place(relx=0.5, rely=0.1, anchor="center") 

# header
section_title = tk.Label(
    
    remote_access3_page, 
    text="Prevention Tips", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Only install remote access software from official websites or trusted sources.",
    "Use strong, unique passwords and enable two-factor authentication for remote access tools.",
    "Remove unknown or unused remote access programs on your system.",
    "Be cautious of pop-ups or emails asking to grant remote control of your device."
]


# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(remote_access3_page, point, 50, y_start)

# load and resize image
rat_image3 = Image.open("images/safe.png")
rat_image3 = rat_image3.resize((300, 300), Image.LANCZOS)
rat_image3 = ImageTk.PhotoImage(rat_image3)
rat_image3_label = tk.Label(remote_access3_page, image=rat_image3)

# place image right of text
rat_image3_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    remote_access3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(remote_access2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    remote_access3_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_rats)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_access3_page = tk.Label(
    
    remote_access3_page, 
    text="100% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_remote_access3_page.place(relx=0.5, rely=0.9, anchor="center")

# viruses page
viruses_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
viruses_page.place(relwidth=1, relheight=1)

# header
viruses_header = "Viruses"
viruses_header_label = tk.Label(
    
    viruses_page, 
    text=viruses_header, 
    font=("Helvetica", 40, "bold"), 
    bg="white", 
    fg="black"
)
viruses_header_label.place(relx=0.5, rely=0.1, anchor="center") 

# header
section_title = tk.Label(
    
    viruses_page, 
    text="What are Viruses", 
    font=("Helvetica", 20, "bold"), 
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_are_viruses = [
    
    "Viruses are malicious software programs designed to infect a computer system.",
    "Some viruses are designed to replicate themselves, while others spread to more devices on the network.",
    "Viruses attach themselves to legitimate files or programs and execute malicious actions when the legitimate file is run."
]

# loop through each list text
for point in what_are_viruses:
    
    # create bullet point
    y_start = create_bullet_point_edu(viruses_page, point, 50, y_start)

# load and resize image
virus_image = Image.open("images/virus1.png")
virus_image = virus_image.resize((400, 300), Image.LANCZOS)
virus_image = ImageTk.PhotoImage(virus_image)
virus_image_label = tk.Label(viruses_page, image=virus_image)

# place image right of text
virus_image_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    viruses_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    viruses_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page1)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_viruses_page = tk.Label(
    
    viruses_page, 
    text="25% Complete", 
    font=("Helvetica", 18, "bold"), 
    bg="white", 
    fg="gray"
)
progress_label_remote_viruses_page.place(relx=0.5, rely=0.9, anchor="center")

# viruses page
viruses_page1 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
viruses_page1.place(relwidth=1, relheight=1)

# header
viruses_header = "Viruses"
viruses_header_label = tk.Label(
    
    viruses_page1,
    text=viruses_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
viruses_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    viruses_page1,
    text="Why are Viruses Dangerous",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_dangerous_virus = [
    
    "Viruses can lead to data loss and corruption. They can delete important files or programs.",
    "They slow down the operating system and can make the computer crash frequently.",
    "Viruses can spread to devices connected to the network, quickly affecting multiple systems.",
    "Some viruses are designed to create backdoors so that attackers can have unauthorized access to the victim's computer at any time."
]

# loop through each list text
for point in why_dangerous_virus:
    
    # create bullet point
    y_start = create_bullet_point_edu(viruses_page1, point, 50, y_start)

# load and resize image
virus_image1 = Image.open("images/stealing.png")
virus_image1 = virus_image1.resize((300, 300), Image.LANCZOS)
virus_image1 = ImageTk.PhotoImage(virus_image1)
virus_image1_label = tk.Label(viruses_page1, image=virus_image1)

# place image right of text
virus_image1_label.place(relx=0.6, rely=0.3)

# next button to go to next page
next_button = tk.Button(
    
    viruses_page1,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page2)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# back button to return to the previous page
back_button = tk.Button(
    
    viruses_page1,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_viruses1_page = tk.Label(
    
    viruses_page1,
    text="50% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_viruses1_page.place(relx=0.5, rely=0.9, anchor="center")

# viruses page
viruses_page2 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
viruses_page2.place(relwidth=1, relheight=1)

# header
viruses_header = "Viruses"
viruses_header_label = tk.Label(
    
    viruses_page2,
    text=viruses_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
viruses_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    viruses_page2,
    text="How are Viruses Obtained",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_virus_obtained = [
    
    "Viruses are commonly obtained through email attachments. They are malicious files disguised as legitimate documents.",
    "Software from untrusted sources may be infected with hidden viruses.",
    "USB drives or external drives can contain viruses that will automatically spread to a connected computer.",
    "Accessing or downloading content from malicious websites can expose the system to viruses."
]

# loop through each list text
for point in how_virus_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(viruses_page2, point, 50, y_start)

# load and resize image
virus_image2 = Image.open("images/danger.png")
virus_image2 = virus_image2.resize((300, 300), Image.LANCZOS)
virus_image2 = ImageTk.PhotoImage(virus_image2)
virus_image2_label = tk.Label(viruses_page2, image=virus_image2)

# place image right of text
virus_image2_label.place(relx=0.6, rely=0.3)

# next button to go to next page
next_button = tk.Button(
    
    viruses_page2,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page3)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# back button to return to the previous page
back_button = tk.Button(
    
    viruses_page2,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page1)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_viruses2_page = tk.Label(
    viruses_page2,
    text="75% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_viruses2_page.place(relx=0.5, rely=0.9, anchor="center")

# viruses page
viruses_page3 = tk.Frame(root, bg="white")

# takes up entire screen dynamically
viruses_page3.place(relwidth=1, relheight=1)

# header
viruses_header = "Viruses"
viruses_header_label = tk.Label(
    
    viruses_page3,
    text=viruses_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
viruses_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    viruses_page3,
    text="Prevention Tips",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Do not download software or content from untrusted sources.",
    "Always scan email attachments before opening them, even if they seem legitimate.",
    "Avoid inserting unknown USB drives into your computer.",
    "Download programs only from trusted, official sources."
    
]

# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(viruses_page3, point, 50, y_start)

# load and resize image
virus_image3 = Image.open("images/safe6.png")
virus_image3 = virus_image3.resize((300, 300), Image.LANCZOS)
virus_image3 = ImageTk.PhotoImage(virus_image3)
virus_image3_label = tk.Label(viruses_page3, image=virus_image3)

# place image right of text
virus_image3_label.place(relx=0.6, rely=0.3)

# next button to go to next page
next_button = tk.Button(
    
    viruses_page3,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_viruses)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# back button to return to the previous page
back_button = tk.Button(
    
    viruses_page3,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(viruses_page2)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_viruses3_page = tk.Label(
    
    viruses_page3,
    text="100% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_viruses3_page.place(relx=0.5, rely=0.9, anchor="center")

# credential stealers page
credential_stealers_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
credential_stealers_page.place(relwidth=1, relheight=1)

# header
credential_stealers_header = "Credential Stealers"
credential_stealers_header_label = tk.Label(
    credential_stealers_page,
    
    text=credential_stealers_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
credential_stealers_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    credential_stealers_page,
    text="What are Credential Stealers",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_are_credential_stealers = [
    
    "Credential stealers are malicious tools or programs that extract sensitive information such as usernames and passwords from a victim's computer.",
    "These tools target web browsers, password managers, and system memory to collect any authentication credentials."
]

# loop through each list text
for point in what_are_credential_stealers:
    
    # create bullet point
    y_start = create_bullet_point_edu(credential_stealers_page, point, 50, y_start)

# load and resize image
credential_stealers_image = Image.open("images/credential_steal.png")
credential_stealers_image = credential_stealers_image.resize((300, 300), Image.LANCZOS)
credential_stealers_image = ImageTk.PhotoImage(credential_stealers_image)
credential_stealers_image_label = tk.Label(credential_stealers_page, image=credential_stealers_image)

# place image right of text
credential_stealers_image_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    credential_stealers_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    credential_stealers_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_credential_stealers_page = tk.Label(
    
    credential_stealers_page,
    text="25% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_credential_stealers_page.place(relx=0.5, rely=0.9, anchor="center")

# credential stealers page
credential_stealers1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
credential_stealers1_page.place(relwidth=1, relheight=1)

# header
credential_stealers_header = "Credential Stealers"
credential_stealers_header_label = tk.Label(
    
    credential_stealers1_page,
    text=credential_stealers_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
credential_stealers_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    credential_stealers1_page,
    text="Why are Credential Stealers Dangerous",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_credential_stealers_dangerous = [
    
    "If credential information is collected, attackers can gain unauthorized access to email accounts, financial systems like banks, or other personal systems.",
    "Attackers can carry out identity theft, allowing them to use the information of the victim to impersonate and commit fraud.",
    "Credential stealers could lead to large-scale data leaks and security breaches if a large organization or company is the target victim."
]

# loop through each list text
for point in why_credential_stealers_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(credential_stealers1_page, point, 50, y_start)

# load and resize image
credential_stealers_image1 = Image.open("images/website.png")
credential_stealers_image1 = credential_stealers_image1.resize((400, 300), Image.LANCZOS)
credential_stealers_image1 = ImageTk.PhotoImage(credential_stealers_image1)
credential_stealers_image1_label = tk.Label(credential_stealers1_page, image=credential_stealers_image1)

# place image right of text
credential_stealers_image1_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    credential_stealers1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    credential_stealers1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_credential_stealers1_page = tk.Label(
    
    credential_stealers1_page,
    text="50% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_credential_stealers1_page.place(relx=0.5, rely=0.9, anchor="center")

# credential stealers page
credential_stealers2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
credential_stealers2_page.place(relwidth=1, relheight=1)

# header
credential_stealers_header = "Credential Stealers"
credential_stealers_header_label = tk.Label(
    
    credential_stealers2_page,
    text=credential_stealers_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
credential_stealers_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    credential_stealers2_page,
    text="How are Credential Stealers Obtained",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_credential_stealers_obtained = [
    
    "Credential stealers are obtained through phishing emails using links or attachments.",
    "Credential stealers can be automatically downloaded when visiting malicious websites.",
    "Seemingly safe software may be infected with credential stealers that install quietly in the background when executed."
]

# loop through each list text
for point in how_credential_stealers_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(credential_stealers2_page, point, 50, y_start)

# load and resize image
credential_stealers_image2 = Image.open("images/malicious_website.png")
credential_stealers_image2 = credential_stealers_image2.resize((300, 300), Image.LANCZOS)
credential_stealers_image2 = ImageTk.PhotoImage(credential_stealers_image2)
credential_stealers_image2_label = tk.Label(credential_stealers2_page, image=credential_stealers_image2)

# place image right of text
credential_stealers_image2_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    credential_stealers2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    credential_stealers2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_credential_stealers2_page = tk.Label(
    credential_stealers2_page,
    text="75% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_credential_stealers2_page.place(relx=0.5, rely=0.9, anchor="center")

# credential stealers page
credential_stealers3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
credential_stealers3_page.place(relwidth=1, relheight=1)

# header
credential_stealers_header = "Credential Stealers"
credential_stealers_header_label = tk.Label(
    
    credential_stealers3_page,
    text=credential_stealers_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
credential_stealers_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    credential_stealers3_page,
    text="Prevention Tips",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Use multi-factor authentication wherever possible to add more security to your accounts.",
    "Avoid entering sensitive credentials on unfamiliar websites or unsecure networks.",
    "Regularly update passwords on web browsers."
]

# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(credential_stealers3_page, point, 50, y_start)

# load and resize image
credential_stealers_image3 = Image.open("images/safe.png")
credential_stealers_image3 = credential_stealers_image3.resize((300, 300), Image.LANCZOS)
credential_stealers_image3 = ImageTk.PhotoImage(credential_stealers_image3)
credential_stealers_image3_label = tk.Label(credential_stealers3_page, image=credential_stealers_image3)

# place image right of text
credential_stealers_image3_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    credential_stealers3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(credential_stealers2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    credential_stealers3_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_credential_stealers)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_remote_credential_stealers3_page = tk.Label(
    
    credential_stealers3_page,
    text="100% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_remote_credential_stealers3_page.place(relx=0.5, rely=0.9, anchor="center")

# compressed files page
compressed_files_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
compressed_files_page.place(relwidth=1, relheight=1)

# header
compressed_files_header = "Compressed Files"
compressed_files_header_label = tk.Label(
    
    compressed_files_page,
    text=compressed_files_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
compressed_files_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    compressed_files_page,
    text="What are Compressed Files",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points position
y_start = 150

# info
what_are_compressed = [
    
    "Compressed files are collections of multiple files bundled together into a single package.",
    "This is done to reduce the file size for easier sharing methods or to save storage on the local machine.",
    "Common compressed file formats include: '.zip', '.rar', '.7z', '.tar'."
]

# loop through each list text
for point in what_are_compressed:
    
    # create bullet point
    y_start = create_bullet_point_edu(compressed_files_page, point, 50, y_start)

# load and resize image
compressed_files_image = Image.open("images/folder2.png")
compressed_files_image = compressed_files_image.resize((300, 300), Image.LANCZOS)
compressed_files_image = ImageTk.PhotoImage(compressed_files_image)
compressed_files_image_label = tk.Label(compressed_files_page, image=compressed_files_image)

# place image right of text
compressed_files_image_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    compressed_files_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    compressed_files_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_compressed_files_page = tk.Label(
    
    compressed_files_page,
    text="25% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_compressed_files_page.place(relx=0.5, rely=0.9, anchor="center")

# compressed files page
compressed_files1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
compressed_files1_page.place(relwidth=1, relheight=1)

# header
compressed_files_header = "Compressed Files"
compressed_files_header_label = tk.Label(
    
    compressed_files1_page,
    text=compressed_files_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
compressed_files_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    compressed_files1_page,
    text="Why are Compressed Files Dangerous",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points position
y_start = 150

# info
why_are_compressed_dangerous = [
    
    "Malicious files can be hidden within compressed files and not be detected by antivirus scanners.",
    "When compressed files are unzipped, malicious content can automatically begin executing without any control over it."
]

# loop through each list text
for point in why_are_compressed_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(compressed_files1_page, point, 50, y_start)

# load and resize image
compressed_files_image1 = Image.open("images/compressed.png")
compressed_files_image1 = compressed_files_image1.resize((300, 300), Image.LANCZOS)
compressed_files_image1 = ImageTk.PhotoImage(compressed_files_image1)
compressed_files_image1_label = tk.Label(compressed_files1_page, image=compressed_files_image1)

# place image right of text
compressed_files_image1_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    compressed_files1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    compressed_files1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_compressed_files1_page = tk.Label(
    
    compressed_files1_page,
    text="50% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_compressed_files1_page.place(relx=0.5, rely=0.9, anchor="center")

# compressed files page
compressed_files2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
compressed_files2_page.place(relwidth=1, relheight=1)

# header
compressed_files_header = "Compressed Files"
compressed_files_header_label = tk.Label(
    
    compressed_files2_page,
    text=compressed_files_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
compressed_files_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    compressed_files2_page,
    text="How are Compressed Files Obtained",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points position
y_start = 150

# info
how_compressed_obtained = [
    
    "Compressed files may be advertised as legitimate safe software when it is actually malicious.",
    "File sharing platforms can allow users to send each other compressed files.",
    "Phishing emails may contain attachments of compressed files."
]

# loop through each list text
for point in how_compressed_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(compressed_files2_page, point, 50, y_start)

# load and resize image
compressed_files_image2 = Image.open("images/data_steal.png")
compressed_files_image2 = compressed_files_image2.resize((400, 300), Image.LANCZOS)
compressed_files_image2 = ImageTk.PhotoImage(compressed_files_image2)
compressed_files_image2_label = tk.Label(compressed_files2_page, image=compressed_files_image2)

# place image right of text
compressed_files_image2_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    compressed_files2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    compressed_files2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_compressed_files2_page = tk.Label(
    
    compressed_files2_page,
    text="75% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_compressed_files2_page.place(relx=0.5, rely=0.9, anchor="center")

# compressed files page
compressed_files3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
compressed_files3_page.place(relwidth=1, relheight=1)

# header
compressed_files_header = "Compressed Files"
compressed_files_header_label = tk.Label(
    
    compressed_files3_page,
    text=compressed_files_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
compressed_files_header_label.place(relx=0.5, rely=0.1, anchor="center")

# header
section_title = tk.Label(
    
    compressed_files3_page,
    text="Prevention Tips",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points position
y_start = 150

# info
prevention_tips = [
    
    "Avoid opening compressed files from unknown or untrusted sources.",
    "Download compressed files only from official and secure websites.",
    "Be cautious of compressed files that require a password. Password-protected files may be skipped by antivirus software, and attackers may add passwords to malicious files to make them seem safe."
]

# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(compressed_files3_page, point, 50, y_start)

# load and resize image
compressed_files_image3 = Image.open("images/safe7.png")
compressed_files_image3 = compressed_files_image3.resize((300, 300), Image.LANCZOS)
compressed_files_image3 = ImageTk.PhotoImage(compressed_files_image3)
compressed_files_image3_label = tk.Label(compressed_files3_page, image=compressed_files_image3)

# place image right of text
compressed_files_image3_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    compressed_files3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(compressed_files2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    compressed_files3_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_compressed_files)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_compressed_files3_page = tk.Label(
    
    compressed_files3_page,
    text="100% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_compressed_files3_page.place(relx=0.5, rely=0.9, anchor="center")

# macros page
macros_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
macros_page.place(relwidth=1, relheight=1)

# header
macros_header = "Macros"
macros_header_label = tk.Label(
    
    macros_page,
    text=macros_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
macros_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    macros_page,
    text="What are Macros",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
what_are_macros = [
    
    "Macros are scripts, or a set of instructions, which are designed to automate tasks within applications, specifically Microsoft Office programs.",
    "They are used to simplify repetitive tasks such as formatting data or generating reports.",
    "Common Office file formats include: '.docm', '.xlsm', '.pptm'. The 'm' in the file extension indicates the presence of a macro."
]

# loop through each list text
for point in what_are_macros:
    
    # create bullet point
    y_start = create_bullet_point_edu(macros_page, point, 50, y_start)

# load and resize image
macros_image = Image.open("images/documents.png")
macros_image = macros_image.resize((300, 300), Image.LANCZOS)
macros_image = ImageTk.PhotoImage(macros_image)
macros_image_label = tk.Label(macros_page, image=macros_image)

# place image right of text
macros_image_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    macros_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(malware_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    macros_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros1_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_macros_page = tk.Label(
    
    macros_page,
    text="25% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_macros_page.place(relx=0.5, rely=0.9, anchor="center")

# macros page
macros1_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
macros1_page.place(relwidth=1, relheight=1)

# header
macros_header = "Macros"
macros_header_label = tk.Label(
    
    macros1_page,
    text=macros_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
macros_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    macros1_page,
    text="Why are Macros Dangerous",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
why_macros_dangerous = [
    
    "Attackers embed harmful scripts in macros to execute malware when the file is opened.",
    "Macros can be programmed to download malicious files, steal data, or alter the computer's system settings.",
    "Since macros are automated tasks, they will execute the moment the file is opened, making it difficult to stop their actions."
]

# loop through each list text
for point in why_macros_dangerous:
    
    # create bullet point
    y_start = create_bullet_point_edu(macros1_page, point, 50, y_start)

# load and resize image
macros_image1 = Image.open("images/hacker5.png")
macros_image1 = macros_image1.resize((300, 300), Image.LANCZOS)
macros_image1 = ImageTk.PhotoImage(macros_image1)
macros_image1_label = tk.Label(macros1_page, image=macros_image1)

# place image right of text
macros_image1_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    macros1_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    macros1_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros2_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_macros1_page = tk.Label(
    
    macros1_page,
    text="50% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_macros1_page.place(relx=0.5, rely=0.9, anchor="center")

# macros page
macros2_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
macros2_page.place(relwidth=1, relheight=1)

# header
macros_header = "Macros"
macros_header_label = tk.Label(
    
    macros2_page,
    text=macros_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
macros_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    macros2_page,
    text="How are Macros Obtained",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
how_macros_obtained = [
    
    "Phishing emails contain files with embedded macros as attachments.",
    "Fake reports or documents are created by attackers with macros enabled to exploit the victim's system.",
    "Macro-enabled files may be automatically downloaded from malicious websites."
]

# loop through each list text
for point in how_macros_obtained:
    
    # create bullet point
    y_start = create_bullet_point_edu(macros2_page, point, 50, y_start)

# load and resize image
macros_image2 = Image.open("images/stealing1.png")
macros_image2 = macros_image2.resize((300, 300), Image.LANCZOS)
macros_image2 = ImageTk.PhotoImage(macros_image2)
macros_image2_label = tk.Label(macros2_page, image=macros_image2)

# place image right of text
macros_image2_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    macros2_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros1_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    macros2_page,
    text="Next",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros3_page)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_macros2_page = tk.Label(
    
    macros2_page,
    text="75% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_macros2_page.place(relx=0.5, rely=0.9, anchor="center")

# macros page
macros3_page = tk.Frame(root, bg="white")

# takes up entire screen dynamically
macros3_page.place(relwidth=1, relheight=1)

# header
macros_header = "Macros"
macros_header_label = tk.Label(
    
    macros3_page,
    text=macros_header,
    font=("Helvetica", 40, "bold"),
    bg="white",
    fg="black"
)
macros_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# header
section_title = tk.Label(
    
    macros3_page,
    text="Prevention Tips",
    font=("Helvetica", 20, "bold"),
    bg="white"
)
section_title.place(relx=0.05, rely=0.15)

# starting position for bullet points
y_start = 150

# info
prevention_tips = [
    
    "Disable macros when handling Microsoft Office files.",
    "Avoid opening documents with macros from unknown or untrusted sources.",
    "View Microsoft Office files in 'Protected View' to open files in a restricted mode that disables macros by default."
]

# loop through each list text
for point in prevention_tips:
    
    # create bullet point
    y_start = create_bullet_point_edu(macros3_page, point, 50, y_start)

# load and resize image
macros_image3 = Image.open("images/safe8.png")
macros_image3 = macros_image3.resize((300, 300), Image.LANCZOS)
macros_image3 = ImageTk.PhotoImage(macros_image3)
macros_image3_label = tk.Label(macros3_page, image=macros_image3)

# place image right of text
macros_image3_label.place(relx=0.6, rely=0.3)

# back button to return to the previous page
back_button = tk.Button(
    
    macros3_page,
    text="Back",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(macros2_page)
)
back_button.place(relx=0.45, rely=0.8, anchor="center")

# next button to go to next page
next_button = tk.Button(
    
    macros3_page,
    text="Quiz me!",
    font=("Helvetica", 18, "bold"),
    command=lambda: show_page(quiz_macros)
)
next_button.place(relx=0.55, rely=0.8, anchor="center")

# progress label of current page
progress_label_macros3_page = tk.Label(
    
    macros3_page,
    text="100% Complete",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="gray"
)
progress_label_macros3_page.place(relx=0.5, rely=0.9, anchor="center")

# global var to store previous quiz results
previous_results_page = None

# class to manage quiz functionality
# question display, user selection, scoring, navigation
# each quiz page is dynamic
class QuizModule:
    
    def __init__(self, root, controller, title, questions, start_page, revise_page, topic_name):
        
        self.root = root 
        self.controller = controller
        self.title = title
        self.questions = questions
        self.start_page = start_page
        self.revise_page = revise_page
        self.topic_name = topic_name
        
        # track current question
        self.current_question = 0
        
        # track score
        self.score = 0
        
        # track user answers
        self.user_answers = []

        # main page for quiz
        self.quiz_frame = tk.Frame(root, bg="white")
        
        # takes up entire screen dynamically
        self.quiz_frame.place(relwidth=1, relheight=1)

        # header
        self.header_label = tk.Label(
            
            self.quiz_frame, 
            text=self.title, 
            font=("Helvetica", 40, "bold"),
            fg="black", 
            bg="white"
        )
        self.header_label.place(relx=0.5, rely=0.1, anchor="center")

        # label to display current question
        self.question_label = tk.Label(
            
            self.quiz_frame, 
            text="", 
            font=("Helvetica", 20, "bold"), 
            wraplength=1000, 
            justify="left", 
            bg="white"
        )
        self.question_label.place(x=120, y=160)

        # var to track which radio button is selected
        self.selected_option = tk.IntVar(value=-1)

        # list to store radio button widgets
        self.options = []

        # style for radio buttons
        style = ttkb.Style()
        style.configure('Custom_radio.TRadiobutton', 
                        font=('Helvetica', 20), 
                        background='white', 
                        padding=10)
        
        # radio button multiple choice options
        for i in range(5):
            
            rb = ttkb.Radiobutton(
                
                self.quiz_frame,
                text="",
                variable=self.selected_option,
                value=i,
                style='Custom_radio.TRadiobutton',
                padding=(10, 5)
            )
            rb.place(x=160, y=230 + i * 50)
            
            # add radio button to options list
            self.options.append(rb)

        # label to show question number
        self.question_number_label = tk.Label(
            
            self.quiz_frame, 
            text="", 
            font=("Helvetica", 20, "bold"),
            bg="white"
        )
        self.question_number_label.place(relx=0.5, rely=0.85, anchor="center")

        # next button to go to next question
        self.next_button = tk.Button(
            
            self.quiz_frame,
            text="Next",
            font=("Helvetica", 20, "bold"),
            command=self.validate_and_next
        )
        self.next_button.place(relx=0.5, rely=0.73, anchor="center")

        # display first question on initialisation
        self.display_question()

    # function to display current quiz question and options
    def display_question(self):
        
        global hamburger_button, home_button
        
        # get current question data
        q = self.questions[self.current_question]
        
        # set question text in label
        self.question_label.config(text=q["question"])
        
        # reset selected option
        self.selected_option.set(-1)

        # loop through available options
        # update corresponding radio buttons
        for i, opt in enumerate(q["options"]):
            
            # set text and value for current radio button
            self.options[i].config(text=opt, value=i)
            
            # position radio button
            self.options[i].place(x=140, y=230 + i * 50)
            
            # bring radio button to front
            self.options[i].tkraise()

        # hide any unused radio buttons
        for i in range(len(q["options"]), len(self.options)):
            
            # hide radio button
            self.options[i].place_forget()

        # update question number label
        self.question_number_label.config(
            
            text=f"Question {self.current_question + 1} / {len(self.questions)}"
        )
        
        # show hamburger button
        hamburger_button.tkraise()
        
        # show home button
        home_button.tkraise()

    # function to validate selected answer and go to next question
    def validate_and_next(self):
        
        # get selected answer
        selected = self.selected_option.get()
        
        # save answer
        self.user_answers.append(selected)

        # check if answer is correct
        if selected == self.questions[self.current_question]["answer"]:
            
            # increment score
            self.score += 1

        # move to next question
        self.current_question += 1

        # if there are more questions
        if self.current_question < len(self.questions):
            
            # display next question
            self.display_question()
            
        # if quiz is done
        else:
            
            # show results
            self.show_results()

    # function to display results page
    def show_results(self):
        
        global hamburger_button, previous_results_page, home_button
        
        # clear previous page if it exists
        if previous_results_page:
            
            # logging
            print("Destroying previous results page")
            
            # destroy page
            previous_results_page.destroy()
            
        else:
            # logging
            print("No previous results page to destroy")

        # get score and list of incorrect questions
        score, incorrect_questions = self.controller.get_quiz_results(self.questions, self.user_answers)
        
        # results page
        results_page = tk.Frame(self.root, bg="white")
        
        # takes up entire screen dynamically
        results_page.pack(fill=tk.BOTH, expand=True)

        # keep reference to new results page
        previous_results_page = results_page

        # canvas to allow scrolling vertically
        canvas = tk.Canvas(results_page, bg="white", highlightthickness=0)
        
        # vertical scrollbar
        # link it to canvas
        scrollbar = tk.Scrollbar(results_page, orient="vertical", command=canvas.yview, width=20)
        
        # place canvas on left side allow it to expand with window
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # place scrollbar on right side and stretch it vertically
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # frame that will sit inside canvas and hold all the scrollable widgets
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        # bind configuration changes so canvas updates scroll region when content changes
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # add scrollable frame into canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        
        # connect scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # show result text with user score
        result_text = f"You scored {self.score} out of {len(self.questions)}!"
        tk.Label(
            
            scrollable_frame, 
            text=result_text, 
            font=("Helvetica", 40, "bold"), 
            bg="white"
        ).pack(pady=(40, 20), anchor="center")

        # flag to track if any incorrect answers were found
        incorrect_found = False
        
        # loop through each recorded user answer and index
        for i, user_answer in enumerate(self.user_answers):
            
            # get correct answer index from current question
            correct = self.questions[i]["answer"]
            
            # check if user answer is incorrect
            if user_answer != correct:
                
                # set flag indicating at least 1 incorrect answer was found
                incorrect_found = True
                
                # get question text for display
                q_text = self.questions[i]["question"]
                
                # get correct answer using correct index
                correct_text = self.questions[i]["options"][correct]
                
                # get user selected answer text if selected
                # otherwise show default message
                user_text = self.questions[i]["options"][user_answer] if user_answer != -1 else "No answer selected"

                # lbael for question text in bold
                tk.Label(scrollable_frame, text=f"Q: {q_text}", font=("Helvetica", 20, "bold"), wraplength=1500, justify="left", bg="white").pack(anchor="w", padx=100, pady=(10, 0))
                
                # style for incorrect answer in red
                style.configure("Red.TLabel", foreground="red", background="white", font=("Helvetica", 18))
                
                # style for correct answer in green
                style.configure("Green.TLabel", foreground="green", background="white", font=("Helvetica", 18))

                # display user answer using red style
                ttkb.Label(
                    
                    scrollable_frame, 
                    text=f"Your Answer: {user_text}", 
                    style="Red.TLabel"
                ).pack(anchor="w", padx=120, pady=(5, 0))

                # display correct answer using green style
                ttkb.Label(
                    
                    scrollable_frame, 
                    text=f"Correct Answer: {correct_text}", 
                    style="Green.TLabel"
                ).pack(anchor="w", padx=120, pady=(0, 10))

        # if no incorrect answers found
        if not incorrect_found:
            
            # style for congratulations message
            style.configure("GreenBold.TLabel", foreground="green", background="white", font=("Helvetica", 30))
            
            # label for congratulations message using green style
            ttkb.Label(
                
                scrollable_frame, 
                text="Congratulations! You got everything correct!", 
                style="GreenBold.TLabel"
            ).pack(pady=40, anchor="center")

            # refresh layout to get latest size of scrollable frame
            scrollable_frame.update_idletasks()
            
            # recreate scrollable frame inside canvas with updated width
            canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=canvas.winfo_width())

        # if quiz score is 6 or higher
        if self.score >= 6:
            
            # mark quiz topic as passed using controller
            self.controller.mark_quiz_as_passed(self.topic_name)

        # button to restart quiz from beginning
        tk.Button(
            
            scrollable_frame, 
            text="Restart Quiz", 
            font=("Helvetica", 20, "bold"), 
            command=lambda: show_page(self.start_page)
        ).pack(pady=(20, 10), anchor="center")

        # button to navigate to revision page for current topic
        tk.Button(
            
            scrollable_frame, 
            text=f"Revise {self.topic_name}", 
            font=("Helvetica", 20, "bold"), 
            command=lambda: show_page(self.revise_page)
        ).pack(pady=(10, 40), anchor="center")

        # show hamburger button
        hamburger_button.tkraise()
        
        # show home button
        home_button.tkraise()
        
        # function to enable scroll behaviour when mouse wheel is used
        def on_mousewheel(event):
        
            # scrolling
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # bind mouse wheel scrolling when cursor enters canvas area
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        
        # unbind mouse wheel scrooling when cursor leaves canvas area
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

# quiz pages
# executables
quiz_executables = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_executables.place(relwidth=1, relheight=1)

# header
quiz_header = "Quiz Executables"
quiz_header_label = tk.Label(
    
    quiz_executables, 
    text=quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# info
quiz_info = [
    
    "This quiz will cover the theory from the educational section.",
    "There will be 10 questions.",
    "You cannot go back and revisit questions.",
    "Get 60% to pass the quiz",
    "Click the button below to start the quiz!"
]

# function to create bullet point for quiz info
def create_bullet_point_quiz(parent, text, x, y, font=("Helvetica", 20)):
    
    # label to create bullet symbol
    bullet_label = tk.Label(parent, text="•", font=font, bg="white", anchor="w")
    
    # place bullet point
    bullet_label.place(x=x, y=y)
    
    # label for text beside bullet point
    text_label = tk.Label(parent, text=text, font=font, bg="white", anchor="w", justify="left")
    
    # place text beside bullet point
    text_label.place(x=x + 20, y=y)
    
    # padding
    spacing = 15 
    
    # return updated y position for next bullet point
    return text_label.winfo_reqheight() + y + spacing 

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height() 

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_executables, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for executables
start_button_executables = tk.Button(
    
    quiz_executables,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Executables",
        questions=executables_questions,
        start_page=quiz_executables,
        revise_page=executables_page,
        topic_name="Executables"
    )
)
start_button_executables.place(relx=0.5, rely=0.8, anchor="center")


# questions data
executables_questions = [
    {
        "question": "What are executables?",
        "options": [
            
            "Files that store personal data for users",
            "Files that contain instructions for a computer to perform specific tasks or run programs",
            "Files used only for temporary storage on a computer"
        ],
        "answer": 1
    },
    {
        "question": "Which of the following is a common executable file extension?",
        "options": [
            
            ".txt",
            ".exe",
            ".jpeg"
        ],
        "answer": 1
    },
    {
        "question": "Why are executables considered dangerous?",
        "options": [
            
            "They interact with the computer system and give attackers direct access",
            "They are always scanned and approved by antivirus software",
            "They do not require any permissions to execute"
        ],
        "answer": 0
    },
    {
        "question": "How do attackers disguise malicious executables?",
        "options": [
            
            "By embedding them in image files",
            "By packaging them as seemingly safe executables",
            "By naming them after popular music files"
        ],
        "answer": 1
    },
    {
        "question": "Which of the following is NOT a way executables can be obtained?",
        "options": [
            
            "Through a phishing email attachment",
            "From auto-run executables on USB drives",
            "By downloading from official websites",
        ],
        "answer": 2
    },
    {
        "question": "What happens when executables are executed?",
        "options": [
            
            "They remain dormant in the system memory",
            "They interact with the computer's operating system to launch applications",
            "They create encrypted backups of system files"
        ],
        "answer": 1
    },
    {
        "question": "How can executables be delivered through phishing?",
        "options": [
            
            "By sending them as email attachments",
            "By embedding them in social media posts",
            "By linking them to legitimate software updates"
        ],
        "answer": 0
    },
    {
        "question": "What is a prevention tip for dealing with executables?",
        "options": [
            
            "Always download files from unverified websites",
            "Ensure real-time scanning is enabled",
            "Allow unrestricted permissions on all accounts"
        ],
        "answer": 1
    },
    {
        "question": "Which of these formats indicates an executable file?",
        "options": [
            
            ".mp3",
            ".doc",
            ".msi",
        ],
        "answer": 2
    },
    {
        "question": "Why is it important to restrict user permissions?",
        "options": [
            
            "To allow full access to all executables",
            "To prevent unauthorized access to the system",
            "To disable the use of real-time scanning"
        ],
        "answer": 1
    }
]

# file spoofing
quiz_file_spoofing = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_file_spoofing.place(relwidth=1, relheight=1)


# header
quiz_header = "Quiz File Spoofing"
quiz_header_label = tk.Label(
    
    quiz_file_spoofing, 
    text=quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  


# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_file_spoofing, point, x_center, y_start)
    
# begin quiz button
# creates new quizmodule instance for file spoofing
start_button_spoofing = tk.Button(
    
    quiz_file_spoofing,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz File Spoofing",
        questions=file_spoofing_questions,
        start_page=quiz_file_spoofing,
        revise_page=file_spoofing_page,
        topic_name="File Spoofing"
    )
)
start_button_spoofing.place(relx=0.5, rely=0.8, anchor="center") 

# questions data
file_spoofing_questions = [
    {
        "question": "What is file spoofing?",
        "options": [
            
            "A technique where attackers disguise a malicious file as a safe one",
            "A process of encrypting files to protect them from malware",
            "A method to backup files on secure servers"
        ],
        "answer": 0
    },
    {
        "question": "How do attackers disguise spoofed files?",
        "options": [
            
            "By changing their color schemes",
            "By altering the file extension",
            "By making them read-only"
        ],
        "answer": 1
    },
    {
        "question": "Which of these is an example of a file spoofing technique?",
        "options": [
            
            "Icon spoofing, where a trusted application icon is applied to a malicious file",
            "Compressing files into ZIP folders",
            "Sharing files over secure cloud storage"
        ],
        "answer": 0
    },
    {
        "question": "Why is file spoofing dangerous?",
        "options": [
            
            "Users might unknowingly open malicious files thinking they are harmless",
            "It always causes immediate system crashes",
            "It permanently deletes the original file"
        ],
        "answer": 0
    },
    {
        "question": "Which of these extensions is likely an example of a spoofed file?",
        "options": [
            
             "document.pdf",
            "image.jpg",
            "image.jpg.exe"
        ],
        "answer": 2
    },
    {
        "question": "How are spoofed files often delivered?",
        "options": [
            
            "Hidden downloaded files when visiting malicious websites",
            "By syncing files with a trusted cloud provider",
            "Via encrypted and secure email links"
        ],
        "answer": 0
    },
    {
        "question": "Why might security software fail to detect spoofed files?",
        "options": [
            
            "Because they are encrypted with a user's password",
            "Because they have manipulated extensions",
            "Because they are always shared over USB drives"
        ],
        "answer": 1
    },
    {
        "question": "What can spoofed files do to a computer system?",
        "options": [
            
            "Install malware, steal information, or compromise the operating system",
            "Enhance the system's security features",
            "Automatically quarantine malicious files"
        ],
        "answer": 0
    },
    {
        "question": "What is a prevention tip for dealing with file spoofing?",
        "options": [
            
            "Disable the viewing of full file extensions in your operating system",
            "Enable the viewing of full file extensions in your operating system",
            "Always hide system files for better organization"
        ],
        "answer": 1
    },
    {
        "question": "Which source is the safest to download files from?",
        "options": [
            
            "Attachments from unknown email senders",
            "Random file-sharing platforms",
            "Trusted official websites"
        ],
        "answer": 2
    }
]

# obfuscation
quiz_obfuscation = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_obfuscation.place(relwidth=1, relheight=1)  

# header
obfuscation_quiz_header = "Quiz Obfuscation & High Entropy"
obfuscation_quiz_header_label = tk.Label(
    
    quiz_obfuscation, 
    text=obfuscation_quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
obfuscation_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_obfuscation, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for obfuscation
start_button_obfuscation = tk.Button(
    
    quiz_obfuscation,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Obfuscation",
        questions=obfuscation_questions,
        start_page=quiz_obfuscation,
        revise_page=obfuscation_page,
        topic_name="Obfuscation"
    )
)
start_button_obfuscation.place(relx=0.5, rely=0.8, anchor="center") 

# questions data
obfuscation_questions = [
    {
        "question": "What is obfuscation?",
        "options": [
            
            "A technique used to simplify file code for faster processing",
            "A method to make a file difficult to understand or analyze",
            "A process to increase file readability for security experts"
        ],
        "answer": 1
    },
    {
        "question": "Why do attackers use obfuscation?",
        "options": [
            
            "To hide the true nature of their malicious files",
            "To compress files for easy sharing",
            "To remove any harmful payloads from the file"
        ],
        "answer": 0
    },
    {
        "question": "What is an example of an obfuscation technique?",
        "options": [
            
            "Using encoding methods to hide malicious scripts",
            "Compressing files into ZIP folders",
            "Backing up files to cloud storage"
        ],
        "answer": 0
    },
    {
        "question": "What does high entropy refer to?",
        "options": [
            
            "Data that appears random and lacks recognizable patterns",
            "Data that has been stored in an organized sequence",
            "A method for improving system speed"
        ],
        "answer": 0
    },
    {
        "question": "Why is high entropy used in malicious files?",
        "options": [
            
            "To make the malware easier to detect by security software",
            "To make malware detection more difficult",
            "To delete all evidence of the malware"
        ],
        "answer": 1
    },
    {
        "question": "Which of these is NOT a reason why obfuscation and high entropy are dangerous?",
        "options": [
            
            "Security software struggles to detect obfuscated patterns",
            "High entropy files are harder for experts to reverse engineer",
            "High entropy files improve antivirus scanning accuracy"
        ],
        "answer": 2
    },
    {
        "question": "How do attackers often deliver obfuscated or high entropy files?",
        "options": [
            
            "Received via email as strange-looking attachments with random names.",
            "Through verified official websites",
            "Installed automatically during regular system updates."
        ],
        "answer": 0
    },
    {
        "question": "What makes obfuscated code particularly dangerous?",
        "options": [
            
            "It conceals malicious payloads until execution",
            "It crashes immediately upon download",
            "It removes all harmful patterns from the file"
        ],
        "answer": 0
    },
    {
        "question": "What is a sign of a potentially obfuscated or high entropy file?",
        "options": [
            
            "A file size that matches industry standards",
            "A file name containing user-friendly characters"
            "A file name like 'a9x$gh29.exe'"
        ],
        "answer": 2
    },
    {
        "question": "What is a good prevention tip for avoiding obfuscated and high entropy files?",
        "options": [
            
            "Look for abnormally small or large file sizes",
            "Avoid downloading any files from the internet",
            "Trust all files from friends or colleagues"
        ],
        "answer": 0
    }
]

# rats
quiz_rats = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_rats.place(relwidth=1, relheight=1)

# header
rats_quiz_header = "Quiz Remote Access Tools"
rats_quiz_header_label = tk.Label(
    
    quiz_rats, 
    text=rats_quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
rats_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_rats, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for rats
start_button_rats = tk.Button(
    
    quiz_rats,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Remote Access Tools",
        questions=rats_questions,
        start_page=quiz_rats,
        revise_page=remote_access_page,
        topic_name="Remote Access Control"
    )
)
start_button_rats.place(relx=0.5, rely=0.8, anchor="center") 

# question data
rats_questions = [
    {
        "question": "What are Remote Access Tools (RATs)?",
        "options": [
            
            "Software applications that allow users to access and control a computer remotely",
            "Tools used only for backing up files on a local network",
            "Applications designed for encrypting sensitive data"
        ],
        "answer": 0
    },
    {
        "question": "How are Remote Access Tools typically used in a legitimate context?",
        "options": [
            
            "For playing online games with friends",
            "For IT support or remote work",
            "For creating secure local backups"
        ],
        "answer": 1
    },
    {
        "question": "Which of these is an example of a safe remote access tool?",
        "options": [
            
            "AccessBridge Utility",
            "NetControl Pro",
            "TeamViewer"
        ],
        "answer": 2
    },
    {
        "question": "Why are malicious Remote Access Tools dangerous?",
        "options": [
            
            "They monitor activity, steal data, and allow attackers to control a victim's computer",
            "They are designed only to slow down the victim's computer system",
            "They work openly and alert the victim to their presence"
        ],
        "answer": 0
    },
    {
        "question": "What does it mean when a RAT serves as a backdoor?",
        "options": [
            
            "It allows the victim to easily uninstall the tool",
            "It provides attackers unauthorized access to the victim's system anytime",
            "It prevents attackers from accessing the system remotely"
        ],
        "answer": 1
    },
    {
        "question": "How can attackers deliver malicious Remote Access Tools?",
        "options": [
            
            "Through phishing emails with attachments or links",
            "By automatic updates from trusted software.",
            "Through only well-known software download platforms"
        ],
        "answer": 0
    },
    {
        "question": "What is one way attackers trick users into installing remote access tools?",
        "options": [
            
            "By pretending to be tech support and asking for access",
            "By sending random software updates from trusted companies",
            "By recommending strong password managers"
        ],
        "answer": 0
    },
    {
        "question": "Why might malicious RATs remain unnoticed by victims?",
        "options": [
            
            "They do not interact with the victim's computer system",
            "They work quietly in the background",
            "They notify users about every action they take"
        ],
        "answer": 1
    },
    {
        "question": "Which of these is a good prevention tip for avoiding RATs?",
        "options": [
            
            "Avoid downloading software from untrusted sources",
            "Share your login credentials with IT support immediately",
            "Disable all email notifications to prevent phishing attempts"
        ],
        "answer": 0
    },
    {
        "question": "What might indicate a suspicious remote access tool running on your system?",
        "options": [
            
            "An occasional system update notification",
            "A new desktop wallpaper from the operating system",
            "Unfamiliar programs launching at startup"
        ],
        "answer": 2
    }
]

# viruses
quiz_viruses = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_viruses.place(relwidth=1, relheight=1)

# header
viruses_quiz_header = "Quiz Viruses"
viruses_quiz_header_label = tk.Label(
    
    quiz_viruses, 
    text=viruses_quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
viruses_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_viruses, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for viruses
start_button_viruses = tk.Button(
    
    quiz_viruses,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Viruses",
        questions=viruses_questions,
        start_page=quiz_viruses,
        revise_page=viruses_page,
        topic_name="Viruses"
    )
)
start_button_viruses.place(relx=0.5, rely=0.8, anchor="center") 

# question data
viruses_questions = [
    {
        "question": "What are computer viruses?",
        "options": [
            
            "Malicious software programs designed to infect a computer system",
            "Programs created to optimize computer performance",
            "Harmless files that mimic legitimate applications"
        ],
        "answer": 0
    },
    {
        "question": "What is a common characteristic of some computer viruses?",
        "options": [
            
            "They replicate themselves or spread to other devices",
            "They disable all software on the system permanently",
            "They remove other malicious programs from the computer"
        ],
        "answer": 0
    },
    {
        "question": "How do viruses execute malicious actions?",
        "options": [
            
            "By operating directly from the system's BIOS",
            "By attaching themselves to legitimate files or programs",
            "By only infecting the hardware of a computer"
        ],
        "answer": 1
    },
    {
        "question": "Which of the following is NOT a danger of computer viruses?",
        "options": [
            
            "Data loss and corruption",
            "Increasing the computer's speed significantly",
            "Slowing down the operating system"
        ],
        "answer": 1
    },
    {
        "question": "What is one way viruses can spread?",
        "options": [
            
            "By remaining dormant indefinitely without action",
            "By requiring user interaction every time they execute",
            "By replicating themselves to devices on the same network"
        ],
        "answer": 2
    },
    {
        "question": "Why might a virus create a backdoor on a victim's computer?",
        "options": [
            
            "To allow attackers unauthorized access anytime",
            "To make the computer immune to further malware infections",
            "To improve the victim's system security"
        ],
        "answer": 0
    },
    {
        "question": "Which is a common method attackers use to deliver viruses?",
        "options": [
            
            "Pop-up ads offering antivirus software",
            "Sharing files via secure cloud storage",
            "Email attachments disguised as legitimate documents"
        ],
        "answer": 2
    },
    {
        "question": "How might external drives contribute to virus infections?",
        "options": [
            
            "By transferring files more quickly",
            "By automatically spreading viruses to connected computers",
            "By encrypting all files on the computer"
        ],
        "answer": 1
    },
    {
        "question": "Which of these is a good prevention tip for avoiding viruses?",
        "options": [
            
            "Always scan email attachments before opening them",
            "Allow automatic downloads from any website",
            "Click on every email link to ensure they are safe"
        ],
        "answer": 0
    },
    {
        "question": "What should you avoid to reduce the risk of virus infections?",
        "options": [
            
            "Using antivirus software on your computer",
            "Backing up your files regularly",
            "Downloading software or content from untrusted sources"
        ],
        "answer": 2
    }
]

# credential stealers
quiz_credential_stealers = tk.Frame(root, bg="white")  

# takes up entire screen dynamically
quiz_credential_stealers.place(relwidth=1, relheight=1)  

# header
credential_stealers_quiz_header = "Quiz Credential Stealers"
credential_stealers_quiz_header_label = tk.Label(
    
    quiz_credential_stealers, 
    text=credential_stealers_quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
credential_stealers_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_credential_stealers, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for credential stealers
start_button_cred_steal = tk.Button(
    
    quiz_credential_stealers,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Credential Stealers",
        questions=credential_stealers_questions,
        start_page=quiz_credential_stealers,
        revise_page=credential_stealers_page,
        topic_name="Credential Stealers"
    )
)
start_button_cred_steal.place(relx=0.5, rely=0.8, anchor="center") 

# question data
credential_stealers_questions = [
    {
        "question": "What are credential stealers?",
        "options": [
            
            "Tools designed to extract sensitive information such as usernames and passwords",
            "Programs created to securely store authentication details",
            "Software used for encrypting files on a computer"
        ],
        "answer": 0
    },
    {
        "question": "Which systems are commonly targeted by credential stealers?",
        "options": [
            
            "Media players and gaming applications",
            "Web browsers, password managers, and system memory",
            "File-sharing platforms and music libraries"
        ],
        "answer": 1
    },
    {
        "question": "Why are credential stealers dangerous?",
        "options": [
            
            "They provide attackers unauthorized access to email accounts and financial systems",
            "They only delete saved passwords from browsers",
            "They cause the computer to crash without stealing data"
        ],
        "answer": 0
    },
    {
        "question": "What crime can attackers carry out using credential stealers?",
        "options": [
            
            "Installing legitimate software on the victim's device",
            "Improving the victim's password strength",
            "Impersonation to commit fraud through identity theft"
        ],
        "answer": 2
    },
    {
        "question": "How can credential stealers affect large organizations?",
        "options": [
            
            "They allow employees to work remotely more securely",
            "They eliminate the need for regular system updates",
            "They can lead to large-scale data leaks and security breaches"
        ],
        "answer": 2
    },
    {
        "question": "How are credential stealers commonly delivered?",
        "options": [
            
            "Through phishing emails using links or attachments",
            "By inserting encrypted text files into password managers",
            "By updating keyboard drivers through official settings"
        ],
        "answer": 0
    },
    {
        "question": "What might happen when visiting a malicious website?",
        "options": [
            
            "Credential stealers can be automatically downloaded",
            "The website improves browser speed",
            "The website restricts the ability to save passwords"
        ],
        "answer": 0
    },
    {
        "question": "How can seemingly safe software spread credential stealers?",
        "options": [
            
            "By preventing access to online banking services",
            "By executing malicious programs quietly in the background",
            "By making antivirus programs more effective"
        ],
        "answer": 1
    },
    {
        "question": "Which is a good prevention tip for protecting against credential stealers?",
        "options": [
            
            "Use multi-factor authentication wherever possible",
            "Save all passwords in an unsecured text file",
            "Avoid changing browser passwords regularly"
        ],
        "answer": 0
    },
    {
        "question": "What should you avoid to protect against credential stealers?",
        "options": [
            
            "Using multi-factor authentication on your accounts",
            "Visiting websites with valid SSL certificates",
            "Entering sensitive credentials on unfamiliar websites or unsecure networks",
        ],
        "answer": 2
    }
]

# compressed files
quiz_compressed_files = tk.Frame(root, bg="white")

# takes up entire screen dynamically
quiz_compressed_files.place(relwidth=1, relheight=1)

# header
compressed_quiz_header = "Quiz Compressed Files"
compressed_quiz_header_label = tk.Label(
    
    quiz_compressed_files, 
    text=compressed_quiz_header,
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
compressed_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_compressed_files, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for compressed file
start_button_compressed = tk.Button(
    
    quiz_compressed_files,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Compressed Files",
        questions=compressed_files_questions,
        start_page=quiz_compressed_files,
        revise_page=compressed_files_page,
        topic_name="Compressed Files"
    )
)
start_button_compressed.place(relx=0.5, rely=0.8, anchor="center") 

# question data
compressed_files_questions = [
    {
        "question": "What are compressed files?",
        "options": [
            
            "Files that are automatically deleted after being downloaded",
            "Collections of multiple files bundled into a single package",
            "Files that are permanently locked to prevent editing"
        ],
        "answer": 1
    },
    {
        "question": "Why are files compressed?",
        "options": [
            
            "To reduce file size for easier sharing or to save storage",
            "To make the files appear hidden from antivirus software",
            "To ensure they cannot be downloaded by unauthorized users"
        ],
        "answer": 0
    },
    {
        "question": "Which of the following is a common compressed file format?",
        "options": [
            
            ".doc",
            ".7z",
            ".exe"
        ],
        "answer": 1
    },
    {
        "question": "Why are compressed files dangerous?",
        "options": [
            
            "They cannot be opened on most operating systems",
            "They automatically delete other files in the folder",
            "Malicious files within compressed files may not be detected by antivirus scanners",
        ],
        "answer": 2
    },
    {
        "question": "What can happen when a malicious compressed file is unzipped?",
        "options": [
            
            "Malicious content can automatically execute without the user's control",
            "The computer's internet speed increases",
            "The file is deleted before it can be accessed"
        ],
        "answer": 0
    },
    {
        "question": "How might compressed files be disguised as safe?",
        "options": [
            
            "By being labeled as password-protected to avoid antivirus scans",
            "By appearing as audio files in the system's library",
            "By being named with random numbers"
        ],
        "answer": 0
    },
    {
        "question": "Where can malicious compressed files often be obtained?",
        "options": [
            
            "From a trusted company's official website",
            "Through phishing emails",
            "Through verified application updates"
        ],
        "answer": 1
    },
    {
        "question": "What is a good way to prevent issues with compressed files?",
        "options": [
            
            "Avoid opening compressed files from unknown or untrusted sources",
            "Always run compressed files with administrator privileges",
            "Store all compressed files on the desktop for easier access"
        ],
        "answer": 0
    },
    {
        "question": "Why should you be cautious of password-protected compressed files?",
        "options": [
            
            "They are difficult to share over email due to their size",
            "They can only be opened on specific operating systems",
            "They may contain malicious files that are skipped by antivirus software",
        ],
        "answer": 2
    },
    {
        "question": "Where should you download compressed files from?",
        "options": [
            
            "Only from official and secure websites",
            "Any website offering free software bundles",
            "Links sent via email from unknown senders"
        ],
        "answer": 0
    }
]

# macros
quiz_macros = tk.Frame(root, bg="white")  

# takes up entire screen dynamically
quiz_macros.place(relwidth=1, relheight=1)  

# header
macros_quiz_header = "Quiz Macros"
macros_quiz_header_label = tk.Label(
    
    quiz_macros, 
    text=macros_quiz_header, 
    font=("Helvetica", 40, "bold"),  
    fg="black", 
    bg="white"
)
macros_quiz_header_label.place(relx=0.5, rely=0.1, anchor="center")  

# fixed width for bullet points
content_width = 800

# calculate x position to center the content horizontally
x_center = (root.winfo_width() - content_width) // 2

# y starting position relative to window height
y_start = 0.25 * root.winfo_height()

# loop through each line of quiz info
for point in quiz_info:
    
    # add bullet point
    y_start = create_bullet_point_quiz(quiz_macros, point, x_center, y_start)

# begin quiz button
# creates new quizmodule instance for macros
start_button_macros = tk.Button(
    
    quiz_macros,
    text="Begin Quiz",
    font=("Helvetica", 20, "bold"),
    
    command=lambda: QuizModule(
        root=root,
        controller=controller,
        title="Quiz Macros",
        questions=macros_questions,
        start_page=quiz_macros,
        revise_page=macros_page,
        topic_name="Macros"
    )
)
start_button_macros.place(relx=0.5, rely=0.8, anchor="center") 

# question data
macros_questions = [
    {
        "question": "What are macros?",
        "options": [
            
            "Tools used to manage a computer's hardware components",
            "Scripts designed to automate tasks within applications",
            "Encrypted files that store passwords"
        ],
        "answer": 1
    },
    {
        "question": "In which applications are macros commonly used?",
        "options": [
            
            "Microsoft Office programs",
            "Web browsers like Chrome or Firefox",
            "Media players like VLC"
        ],
        "answer": 0
    },
    {
        "question": "What does the 'm' in file extensions like '.docm' or '.xlsm' signify?",
        "options": [
            
            "The file is modified",
            "The presence of a macro",
            "The file is manually saved"
        ],
        "answer": 1
    },
    {
        "question": "Why are macros considered dangerous?",
        "options": [
            
            "They require high system resources to execute",
            "They make files impossible to delete",
            "They can embed harmful scripts to execute malware"
        ],
        "answer": 2
    },
    {
        "question": "What can attackers do with malicious macros?",
        "options": [
            
            "Only read data from a file",
            "Program them to download malicious files, steal data, or alter system settings",
            "Disable the internet connection temporarily"
        ],
        "answer": 1
    },
    {
        "question": "How are malicious macros usually obtained?",
        "options": [
            
            "Through phishing emails with files containing embedded macros",
            "Only through physical storage devices like USB drives",
            "By installing verified updates from official software providers"
        ],
        "answer": 0
    },
    {
        "question": "What might a fake document with malicious macros do?",
        "options": [
            
            "Automatically reformat the victim's hard drive",
            "Block access to the internet",
            "Exploit the system to install malware or steal information"
        ],
        "answer": 2
    },
    {
        "question": "What is a safe way to view Microsoft Office files with macros?",
        "options": [
            
            "Open them in 'Protected View'",
            "Always enable macros to ensure functionality",
            "Open them on a public computer"
        ],
        "answer": 0
    },
    {
        "question": "What should you do when handling files with macros?",
        "options": [
            
            "Disable macros when working with Microsoft Office files",
            "Enable macros for quicker file access",
            "Use macros to scan the file for viruses"
        ],
        "answer": 0
    },
    {
        "question": "Where should you avoid opening documents with macros?",
        "options": [
            
            "On computers with antivirus software installed",
            "From unknown or untrusted sources",
            "While connected to secure Wi-Fi"
        ],
        "answer": 1
    }
]

# show welcome page when application first opens
welcome_page.tkraise()

# show hamburger button
hamburger_button.tkraise() 

# home button
home_button.tkraise()

# main loop
root.mainloop()