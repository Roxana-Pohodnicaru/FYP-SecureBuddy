# imports
import tkinter as tk


# tkinter object
root = tk.Tk()

# title of program
root.title("SecureBuddy")

# screen size
root.geometry("1980x1200")


# text to show
text = """Welcome to SecureBuddy"""
# label for text
label = tk.Label(root, text=text)
# display label
label.pack()


# function that handles functionality when hamburger button is clicked
# displays message when clicked
def hamburger_menu():
    clicked_message.config(text="Button was clicked")


# hamburger menu icon
hamburger_button = tk.Button(root, text="☰", font=("Arial", 20), command=hamburger_menu)
# top left corner
hamburger_button.place(x=10, y=10)

# show if hamburger button is clicked
clicked_message = tk.Label(root, text="", font=("Arial", 14))
clicked_message.pack()



# main
root.mainloop()