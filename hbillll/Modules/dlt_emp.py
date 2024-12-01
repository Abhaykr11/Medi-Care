import tkinter as tk
from tkinter import messagebox
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


# Function to delete employee based on empid
def delete_employee(empid_entry):
    empid = empid_entry.get()

    if not empid:
        messagebox.showwarning("Input Error", "Please enter an Employee ID")
        return

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM employee WHERE empid = %s"
        cursor.execute(sql, (empid,))
        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Employee deleted successfully")
        else:
            messagebox.showwarning("Not Found", "No employee found with the given ID")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


# Function to open the delete employee page
def open_dlt_emp_page():
    dlt_emp_window = tk.Toplevel()
    dlt_emp_window.title('Delete Employee')
    dlt_emp_window.geometry('400x200+50+50')
    dlt_emp_window.resizable(0, 0)

    # Labels and entry
    tk.Label(dlt_emp_window, text="Employee ID").grid(row=0, column=0, padx=10, pady=20)
    empid_entry = tk.Entry(dlt_emp_window)
    empid_entry.grid(row=0, column=1, padx=10, pady=20)

    # Delete Employee Button
    tk.Button(dlt_emp_window, text="Delete Employee", command=lambda: delete_employee(empid_entry)).grid(row=1,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         padx=10,
                                                                                                         pady=10)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x300+50+50')  # Set size and position of the window
    root.title("Admin Menu")

    # Button to open delete employee page
    tk.Button(root, text="Open Delete Employee Page", command=open_dlt_emp_page).pack(pady=20)

    root.mainloop()
