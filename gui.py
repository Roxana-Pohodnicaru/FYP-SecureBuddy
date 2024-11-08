# imports
import tkinter as tk


# tkinter object
root = tk.Tk()

# title of program
root.title("SecureBuddy")

# screen size
root.geometry("1980x1200")

# welcome page
welcome_page = tk.Frame(root, width=1980, height=1200)
welcome_page.place(x=0, y=0, relwidth=1, relheight=1)

# text to show
text = """Welcome to SecureBuddy"""
# label for text
label = tk.Label(welcome_page, text=text)
label.pack()


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


# function to display different page based on buttons clicked in hamburger menu
def show_page(page):
    
    # raise the page on the top
    page.tkraise()
    
    # hide the menu frame
    hide_menu()
    
    # need to show hamburger button
    hamburger_button.tkraise()



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
scan_history_button = tk.Button(menu_frame, text="Scan History", font=("Arial", 16), command=print("placeholder"))
education_button = tk.Button(menu_frame, text="Education", font=("Arial", 16), command=print("placeholder"))

# manual button height
# TODO need to make this automatic
button_height = 225

# placing location for buttons
scan_files_button.place(x=0, y=0, width=800, height=button_height)
scan_history_button.place(x=0, y=button_height, width=800, height=button_height)
education_button.place(x=0, y=button_height * 2, width=800, height=button_height)


# scan files page - testing with green background
scan_files_page = tk.Frame(root, bg="green", width=1980, height=1200)
scan_files_page.place(x=0, y=0)


# need to show at start
welcome_page.tkraise()

# need to show hamburger button
# TODO include for hamburger menu frame 'x' / 'esc' functionality
hamburger_button.tkraise()

# main loop
root.mainloop()