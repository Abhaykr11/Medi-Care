import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re  # For email and phone validation


# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password='root',
        port=3306,
        database='hbill'
    )


# Function to validate patient data
def validate_patient_data(entries, error_labels):
    is_valid = True

    # Clear previous error messages
    for label in error_labels.values():
        label.config(text="")

    # Validate each field
    if not entries['patient_id'].get():
        error_labels['patient_id'].config(text="Required")
        is_valid = False

    if not entries['password'].get() or len(entries['password'].get()) < 6:
        error_labels['password'].config(text="At least 6 characters")
        is_valid = False

    if not entries['email'].get() or not re.match(r"[^@]+@[^@]+\.[^@]+", entries['email'].get()):
        error_labels['email'].config(text="Invalid email")
        is_valid = False

    # Phone number validation: allow digits, starting with an optional '+', followed by up to 10 digits
    phone_pattern = r"^\+?\d{1,10}$"

    if not re.match(phone_pattern, entries['phone'].get()):
        error_labels['phone'].config(text="Invalid phone number")
        is_valid = False

    if not re.match(phone_pattern, entries['contact_no'].get()):
        error_labels['contact_no'].config(text="Invalid contact number")
        is_valid = False

    if not entries['date_of_birth'].get():
        error_labels['date_of_birth'].config(text="Required")
        is_valid = False

    if not entries['date_of_registration'].get():
        error_labels['date_of_registration'].config(text="Required")
        is_valid = False

    return is_valid


# Function to check if patient ID exists
def check_patient_id(patient_id_entry, patient_id_error_label):
    patient_id = patient_id_entry.get()

    if not patient_id:
        patient_id_error_label.config(text="Patient ID is required")
        return

    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Check if the patient ID already exists in the database
        cursor.execute("SELECT patientid FROM patient WHERE patientid = %s", (patient_id,))
        result = cursor.fetchone()

        if result:
            patient_id_error_label.config(text="Patient ID exists, please try another ID", fg="red")
        else:
            patient_id_error_label.config(text="Patient ID available, you can proceed", fg="green")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


# Function to add a new patient
def add_patient(entries, error_labels):
    if validate_patient_data(entries, error_labels):
        try:
            patient_data = (
                entries['patient_id'].get(),
                entries['password'].get(),
                entries['first_name'].get(),
                entries['last_name'].get(),
                entries['date_of_birth'].get(),
                entries['gender'].get(),
                entries['address'].get(),
                entries['city'].get(),
                entries['state'].get(),
                entries['postal_pin'].get(),
                entries['phone'].get(),
                entries['email'].get(),
                entries['contact_name'].get(),
                entries['contact_no'].get(),
                entries['date_of_registration'].get(),
            )

            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO patient (patientid, password, firstname, lastname, dob, gender, address, city, state, postalpin, phoneno, email, contactname, contactno, doreg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, patient_data)
            db.commit()
            messagebox.showinfo("Success", "Patient added successfully")

            # Clear all entry fields after successful addition
            for entry in entries.values():
                entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()


# Function to add placeholders and bind events
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# Function to open the add patient page
def open_add_patient_page():
    add_patient_window = tk.Toplevel()
    add_patient_window.title('Add Patient')
    add_patient_window.geometry('600x700+50+50')
    add_patient_window.resizable(0, 0)

    # Create a dictionary to hold entry widgets
    entries = {}
    error_labels = {}

    # Labels and entries
    labels = [
        "Patient ID", "Password", "First Name", "Last Name", "Date of Birth", "Gender", "Address", "City", "State",
        "Postal PIN", "Phone", "Email", "Contact Name", "Contact No", "Date of Registration"
    ]

    placeholders = {
        "patient_id": "Start with letter P and number",
        "date_of_registration": "dd-mm-yyyy format"
    }

    for i, label in enumerate(labels):
        tk.Label(add_patient_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(add_patient_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label.replace(" ", "_").lower()] = entry

        # Add placeholders for Patient ID and Date of Registration
        if label.replace(" ", "_").lower() in placeholders:
            add_placeholder(entry, placeholders[label.replace(" ", "_").lower()])

        # Add a label to show errors next to each field
        error_label = tk.Label(add_patient_window, text="", fg="red")
        error_label.grid(row=i, column=2, padx=10, pady=5)
        error_labels[label.replace(" ", "_").lower()] = error_label

    # "Check Patient ID" Button next to "Patient ID" entry
    check_button = tk.Button(add_patient_window, text="Check Patient ID",
                             command=lambda: check_patient_id(entries['patient_id'], error_labels['patient_id']))
    check_button.grid(row=0, column=3, padx=10, pady=5)

    # Add Patient Button
    tk.Button(add_patient_window, text="Add Patient", command=lambda: add_patient(entries, error_labels)).grid(
        row=len(labels),
        column=0, columnspan=2,
        padx=10, pady=10)


# Main window setup (for demonstration purposes)
'''root = tk.Tk()
root.title('Patient Management')
tk.Button(root, text="Open Add Patient Page", command=open_add_patient_page).pack(pady=20)
root.mainloop()'''
