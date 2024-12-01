from tkinter import Toplevel, Label, Menu
from PIL import ImageTk, Image
import os
from add_patient import open_add_patient_page
from updt_patient import open_updt_patient_page
from dlt_patient import open_dlt_patient_page
from add_bill import open_add_bill_page  # Replace with the actual import if different
from updt_bill import open_update_bill_window
from view_patients import view_patients

# from update_bill import open_update_bill_page  # Replace with the actual import if different

def open_employee_page():
    employee_window = Toplevel()
    employee_window.title('Employee')
    employee_window.geometry('998x660+50+50')
    employee_window.resizable(0, 0)

    # Use a relative path for the image
    path_to_image = '../image/emp.jpg'
    try:
        bgImage = ImageTk.PhotoImage(Image.open(path_to_image))
    except FileNotFoundError:
        print(f"Image file not found at: {os.path.abspath(path_to_image)}")
        bgImage = None  # Provide a fallback or handle the error

    # Create a label to display the image if it was loaded successfully
    if bgImage:
        bgLabel = Label(employee_window, image=bgImage)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a menu bar
    menu_bar = Menu(employee_window)

    # Create the 'Manage Patient' menu
    manage_patient_menu = Menu(menu_bar, tearoff=0)
    manage_patient_menu.add_command(label="Add Patient", command=open_add_patient_page)
    manage_patient_menu.add_command(label="Edit Patient", command=open_updt_patient_page)
    manage_patient_menu.add_command(label="Delete Patient", command=open_dlt_patient_page)
    manage_patient_menu.add_command(label="View Patients", command=view_patients)  # Added option to view all patients
    menu_bar.add_cascade(label="Manage Patient", menu=manage_patient_menu)

    # Create the 'Manage Bill' menu
    manage_bill_menu = Menu(menu_bar, tearoff=0)
    manage_bill_menu.add_command(label="Add Bill", command=open_add_bill_page)  # Function to open the Add Bill page
    manage_bill_menu.add_command(label="Update Bill", command=open_update_bill_window)  # Function to open the Update Bill page
    menu_bar.add_cascade(label="Manage Bill", menu=manage_bill_menu)

    # Add the menu bar to the window
    employee_window.config(menu=menu_bar)

    employee_window.images = {'bgImage': bgImage}


# Assuming you have a main window, call open_employee_page() when needed
# open_employee_page()
