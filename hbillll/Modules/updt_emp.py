import tkinter as tk
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


# Function to search for employee details based on empid
def search_employee(empid_entry, password_entry, empname_entry, address_entry, postalpin_entry, phoneno_entry,
                    email_entry, position_entry, dept_entry, error_label):
    empid = empid_entry.get()

    if not empid:
        error_label.config(text="Please enter an Employee ID", fg="red")
        return

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM employee WHERE empid = %s"
        cursor.execute(sql, (empid,))
        result = cursor.fetchone()

        if result:
            # Populate the fields with the current employee details
            password_entry.delete(0, tk.END)
            password_entry.insert(0, result[1])
            password_entry.config(show='')  # Show the password

            empname_entry.delete(0, tk.END)
            empname_entry.insert(0, result[2])

            address_entry.delete(0, tk.END)
            address_entry.insert(0, result[3])

            postalpin_entry.delete(0, tk.END)
            postalpin_entry.insert(0, result[4])

            phoneno_entry.delete(0, tk.END)
            phoneno_entry.insert(0, result[5])

            email_entry.delete(0, tk.END)
            email_entry.insert(0, result[6])

            position_entry.delete(0, tk.END)
            position_entry.insert(0, result[7])

            dept_entry.delete(0, tk.END)
            dept_entry.insert(0, result[8])

            error_label.config(text="Employee found", fg="green")  # Success message

            # Disable the Employee ID entry field
            empid_entry.config(state=tk.DISABLED)

        else:
            error_label.config(text="No employee found with the given ID", fg="red")

    except mysql.connector.Error as err:
        error_label.config(text=f"Error: {err}", fg="red")
    finally:
        cursor.close()
        db.close()


# Function to update employee details
def update_employee(empid_entry, password_entry, empname_entry, address_entry, postalpin_entry, phoneno_entry,
                    email_entry, position_entry, dept_entry, error_label):
    empid = empid_entry.get()
    password = password_entry.get()
    empname = empname_entry.get()
    address = address_entry.get()
    postalpin = postalpin_entry.get()
    phoneno = phoneno_entry.get()
    email = email_entry.get()
    position = position_entry.get()
    dept = dept_entry.get()

    if not empid:
        error_label.config(text="Please enter an Employee ID to update", fg="red")
        return

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = """UPDATE employee
                 SET password = %s, empname = %s, address = %s, postalpin = %s, phoneno = %s, email = %s, position = %s, dept = %s
                 WHERE empid = %s"""
        values = (password, empname, address, postalpin, phoneno, email, position, dept, empid)
        cursor.execute(sql, values)
        db.commit()

        error_label.config(text="Employee details updated successfully", fg="green")  # Success message

        # Clear the text areas after successful update
        empid_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        empname_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        postalpin_entry.delete(0, tk.END)
        phoneno_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        position_entry.delete(0, tk.END)
        dept_entry.delete(0, tk.END)

    except mysql.connector.Error as err:
        error_label.config(text=f"Error: {err}", fg="red")
    finally:
        cursor.close()
        db.close()


# Function to open the update employee page
def open_updt_emp_page():
    updt_emp_window = tk.Toplevel()
    updt_emp_window.title('Update Employee')
    updt_emp_window.geometry('998x660+50+50')
    updt_emp_window.resizable(0, 0)

    # Labels and entries
    tk.Label(updt_emp_window, text="Employee ID").grid(row=0, column=0, padx=10, pady=5)
    empid_entry = tk.Entry(updt_emp_window)
    empid_entry.grid(row=0, column=1, padx=10, pady=5)

    # Error label
    error_label = tk.Label(updt_emp_window, text="", fg="red")
    error_label.grid(row=0, column=3, padx=10, pady=5)

    # Search button
    tk.Button(updt_emp_window, text="Search Employee",
              command=lambda: search_employee(empid_entry, password_entry, empname_entry, address_entry,
                                              postalpin_entry, phoneno_entry, email_entry, position_entry, dept_entry,
                                              error_label)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Password").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(updt_emp_window, show='*')  # Mask the password input
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Employee Name").grid(row=2, column=0, padx=10, pady=5)
    empname_entry = tk.Entry(updt_emp_window)
    empname_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Address").grid(row=3, column=0, padx=10, pady=5)
    address_entry = tk.Entry(updt_emp_window)
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Postal Pin").grid(row=4, column=0, padx=10, pady=5)
    postalpin_entry = tk.Entry(updt_emp_window)
    postalpin_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Phone No").grid(row=5, column=0, padx=10, pady=5)
    phoneno_entry = tk.Entry(updt_emp_window)
    phoneno_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Email").grid(row=6, column=0, padx=10, pady=5)
    email_entry = tk.Entry(updt_emp_window)
    email_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Position").grid(row=7, column=0, padx=10, pady=5)
    position_entry = tk.Entry(updt_emp_window)
    position_entry.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(updt_emp_window, text="Department").grid(row=8, column=0, padx=10, pady=5)
    dept_entry = tk.Entry(updt_emp_window)
    dept_entry.grid(row=8, column=1, padx=10, pady=5)

    # Update Employee Button
    tk.Button(updt_emp_window, text="Update Employee",
              command=lambda: update_employee(empid_entry, password_entry, empname_entry, address_entry,
                                              postalpin_entry, phoneno_entry, email_entry, position_entry, dept_entry,
                                              error_label)).grid(row=9, column=0, columnspan=2, padx=10, pady=10)


# Main window setup (for demonstration purposes)
'''root = tk.Tk()
root.title('Employee Management')
tk.Button(root, text="Open Update Employee Page", command=open_updt_emp_page).pack(pady=20)
root.mainloop()'''
