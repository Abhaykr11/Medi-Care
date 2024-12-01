import tkinter as tk
import re
import mysql.connector


# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password='root',
        port=3306,
        database='hbill'
    )


# Validation function for employee fields
def validate_employee_fields(entries, error_label):
    empid = entries['empid'].get().strip()
    password = entries['password'].get().strip()
    empname = entries['empname'].get().strip()
    phoneno = entries['phoneno'].get().strip()
    email = entries['email'].get().strip()

    if not empid:
        error_label.config(text="Employee ID should not be null")
        return False

    if not password or len(password) < 6 or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        error_label.config(text="Password must be at least 6 characters long and contain a special character")
        return False

    if not empname:
        error_label.config(text="Employee name should not be null")
        return False

    if not phoneno or not re.match(r'^\+?\d+$', phoneno):
        error_label.config(text="Phone number should contain only numbers and optionally a plus sign (+)")
        return False

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        error_label.config(text="Email should be in a valid email format")
        return False

    error_label.config(text="")  # Clear the error message if all validations pass
    return True


# Function to add employee
def add_employee(entries, error_label):
    if not validate_employee_fields(entries, error_label):
        return

    empid = entries['empid'].get()
    password = entries['password'].get()
    empname = entries['empname'].get()
    address = entries['address'].get()
    phoneno = entries['phoneno'].get()
    email = entries['email'].get()
    position = entries['position'].get()
    dept = entries['dept'].get()

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = """INSERT INTO employee (empid, password, empname, address, phoneno, email, position, dept)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (empid, password, empname, address, phoneno, email, position, dept)
        cursor.execute(sql, values)
        db.commit()

        # Success message (No messagebox used as requested)
        error_label.config(text="Employee added successfully", fg="green")

        # Clear all entry fields after successful addition
        for entry in entries.values():
            entry.delete(0, tk.END)

    except mysql.connector.Error as err:
        error_label.config(text=f"Error: {err}", fg="red")
    finally:
        cursor.close()
        db.close()


# Function to open the add employee page
def open_add_emp_page():
    add_emp_window = tk.Toplevel()
    add_emp_window.title('Add Employee')
    add_emp_window.geometry('998x660+50+50')
    add_emp_window.resizable(0, 0)

    # Create a dictionary to hold entry widgets
    entries = {}

    # Labels and entries
    tk.Label(add_emp_window, text="Employee ID").grid(row=0, column=0, padx=10, pady=5)
    entries['empid'] = tk.Entry(add_emp_window)
    entries['empid'].grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Password").grid(row=1, column=0, padx=10, pady=5)
    entries['password'] = tk.Entry(add_emp_window, show='*')  # Mask the password input
    entries['password'].grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Employee Name").grid(row=2, column=0, padx=10, pady=5)
    entries['empname'] = tk.Entry(add_emp_window)
    entries['empname'].grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Address").grid(row=3, column=0, padx=10, pady=5)
    entries['address'] = tk.Entry(add_emp_window)
    entries['address'].grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Phone No").grid(row=4, column=0, padx=10, pady=5)
    entries['phoneno'] = tk.Entry(add_emp_window)
    entries['phoneno'].grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Email").grid(row=5, column=0, padx=10, pady=5)
    entries['email'] = tk.Entry(add_emp_window)
    entries['email'].grid(row=5, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Position").grid(row=6, column=0, padx=10, pady=5)
    entries['position'] = tk.Entry(add_emp_window)
    entries['position'].grid(row=6, column=1, padx=10, pady=5)

    tk.Label(add_emp_window, text="Department").grid(row=7, column=0, padx=10, pady=5)
    entries['dept'] = tk.Entry(add_emp_window)
    entries['dept'].grid(row=7, column=1, padx=10, pady=5)

    # Label to display validation and success/error messages
    error_label = tk.Label(add_emp_window, text="", fg="red")
    error_label.grid(row=8, column=0, columnspan=2)

    # Add Employee Button
    tk.Button(add_emp_window, text="Add Employee", command=lambda: add_employee(entries, error_label)).grid(row=9, column=0, columnspan=2, padx=10, pady=10)



