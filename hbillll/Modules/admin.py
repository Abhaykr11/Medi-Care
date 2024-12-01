import tkinter as tk
from tkinter import Menu
from PIL import ImageTk, Image
import os
from add_emp import open_add_emp_page
from updt_emp import open_updt_emp_page
from dlt_emp import open_dlt_emp_page
from add_patient import open_add_patient_page
from updt_patient import open_updt_patient_page
from dlt_patient import open_dlt_patient_page
from view_patients import view_patients
from view_employees import view_employees


# Function to open the admin page
def open_admin_page():
    admin_window = tk.Toplevel()
    admin_window.title('Admin')
    admin_window.geometry('998x660+50+50')
    admin_window.resizable(0, 0)

    # Set background image
    path_to_image = '../image/admin1.jpeg'
    try:
        bgImage = ImageTk.PhotoImage(Image.open(path_to_image))
    except FileNotFoundError:
        print(f"Image file not found at: {os.path.abspath(path_to_image)}")
        bgImage = None

    if bgImage:
        bgLabel = tk.Label(admin_window, image=bgImage)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

    # Create and configure menu
    add_employee_menu_option(admin_window)

    # Keep a reference to the image to prevent garbage collection
    admin_window.images = {'bgImage': bgImage}


# Function to add employee and patient menu options to the menu bar
def add_employee_menu_option(admin_window):
    menu_bar = Menu(admin_window)

    # Manage Employee Menu
    manage_employee_menu = Menu(menu_bar, tearoff=0)
    manage_employee_menu.add_command(label="Add Employee", command=open_add_emp_page)
    manage_employee_menu.add_command(label="Edit Employee", command=open_updt_emp_page)
    manage_employee_menu.add_command(label="Delete Employee", command=open_dlt_emp_page)
    manage_employee_menu.add_command(label="View Employees", command=view_employees)  # Added view employees
    menu_bar.add_cascade(label="Manage Employee", menu=manage_employee_menu)

    # Manage Patient Menu
    manage_patient_menu = Menu(menu_bar, tearoff=0)
    manage_patient_menu.add_command(label="Add Patient", command=open_add_patient_page)
    manage_patient_menu.add_command(label="Update Patient", command=open_updt_patient_page)
    manage_patient_menu.add_command(label="Delete Patient", command=open_dlt_patient_page)
    manage_patient_menu.add_command(label="View Patients", command=view_patients)  # Added view patients
    menu_bar.add_cascade(label="Manage Patient", menu=manage_patient_menu)

    # Add other menus similarly
    admin_window.config(menu=menu_bar)


# Assuming other necessary functions like open_add_emp_page(), view_employees(), view_patients() are already implemented

# To open the admin page, call open_admin_page() when needed.
# Example: open_admin_page()
