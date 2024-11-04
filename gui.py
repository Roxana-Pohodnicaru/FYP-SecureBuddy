# imports
import tkinter as tk

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


# main
root.mainloop()