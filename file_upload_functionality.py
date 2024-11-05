# imports
import tkinter as tk
from tkinter import filedialog


# function to handle file upload
def upload_file():
    
    # open file dialog
    file_path = filedialog.askopenfilename()
    
    if file_path:
        
        # update label with file path
        label.config(text=f"Selected file: {file_path}")


# tkinter object
root = tk.Tk()

# title of program
root.title("SecureBuddy")

# screen size
root.geometry("500x500")

# text to show
text = """Testing Tkinter :)"""
# label for text
label = tk.Label(root, text=text)
# display label
label.pack()

# button for file upload
upload_button = tk.Button(root, text="Upload file", command=upload_file)
# display
upload_button.pack()

# main
root.mainloop()