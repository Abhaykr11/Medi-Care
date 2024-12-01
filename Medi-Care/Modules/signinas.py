import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the necessary modules for image handling
from signin import create_login_window


def open_login_page(page_type):
    create_login_window(page_type)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        signinas.destroy()  # Close the application


# Setup main window
signinas = tk.Tk()
signinas.title('Signinas')
signinas.geometry('998x660+50+50')
signinas.resizable(0, 0)

# Load the background image (admin.jpg)
bgImage = ImageTk.PhotoImage(Image.open('../image/admin.jpg'))  # Adjust the path as needed

# Add the background image as a label
bgLabel = tk.Label(signinas, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)  # Place the image to cover the window

# Title Label
title_label = tk.Label(signinas, text='MEDI-CARE', font=('Arial', 32, 'bold'), fg='white', bg='green')
title_label.place(relx=0.5, y=25, anchor='center')

# Buttons with updated font and centered alignment
button_font = ('Arial', 18, 'bold')  # Changed font to Arial with size 18

logasadmin = tk.Button(signinas, text='Admin', font=button_font, fg='white',
                       bg='firebrick1', activebackground='firebrick1', activeforeground='white', cursor='hand2', bd=0,
                       width=10, height=2, command=lambda: open_login_page('admin'))
logasadmin.place(relx=0.5, rely=0.2, anchor='center')

logasemp = tk.Button(signinas, text='Employee', font=button_font, fg='white',
                     bg='firebrick1', activebackground='firebrick1', activeforeground='white', cursor='hand2', bd=0,
                     width=10, height=2, command=lambda: open_login_page('employee'))
logasemp.place(relx=0.5, rely=0.4, anchor='center')

logaspatient = tk.Button(signinas, text='Patient', font=button_font, fg='white',
                         bg='firebrick1', activebackground='firebrick1', activeforeground='white', cursor='hand2', bd=0,
                         width=10, height=2, command=lambda: open_login_page('patient'))
logaspatient.place(relx=0.5, rely=0.6, anchor='center')

# Bind the close event to the on_closing function
signinas.protocol("WM_DELETE_WINDOW", on_closing)

signinas.mainloop()
