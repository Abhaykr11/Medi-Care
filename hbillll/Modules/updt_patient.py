import tkinter as tk
import mysql.connector
from tkinter import messagebox, simpledialog


class UpdatePatientPage:
    def __init__(self, root):
        self.btn_update = None
        self.patient_id_entry = None  # Add patient_id_entry
        self.root = root
        self.db = self.get_db_connection()
        self.entries = {}  # Initialize entries here
        self.create_widgets()

    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password='root',
            port=3306,
            database='hbill'
        )

    def create_widgets(self):
        self.root.title('Update Patient')
        self.root.geometry('600x700+50+50')
        self.root.resizable(0, 0)

        # Labels and Entry fields
        labels = [
            "Patient ID", "Password", "First Name", "Last Name", "Date of Birth", "Gender", "Address", "City", "State",
            "Postal PIN", "Phone", "Email", "Contact Name", "Contact No", "Date of Registration", "Date of Discharge"
        ]

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            key = label.replace(" ", "_").lower()
            self.entries[key] = entry

        # Save the patient_id_entry separately
        self.patient_id_entry = self.entries['patient_id']

        # Select Patient Button
        tk.Button(self.root, text="Select Patient", command=self.select_patient).grid(row=len(labels), column=0,
                                                                                      padx=10, pady=10)

        # Update Patient Button (initially disabled)
        self.btn_update = tk.Button(self.root, text="Update Patient", command=self.update_patient, state=tk.DISABLED)
        self.btn_update.grid(row=len(labels), column=1, padx=10, pady=10)

    def fetch_patient_details(self, patientid):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patient WHERE patientid=%s", (patientid,))
            patient = cursor.fetchone()
            cursor.close()

            if patient:
                # Populate entries with fetched patient details
                for db_column, entry in self.entries.items():
                    # Ensure the key matches the column name from the database
                    if db_column in patient:
                        entry.delete(0, tk.END)
                        entry.insert(0, patient[db_column])
                # Show the update button after fetching patient details
                self.btn_update.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("Not Found", "No patient found with this ID.")
                self.clear_entries()  # Clear entries if not found
                self.btn_update.config(state=tk.DISABLED)  # Disable update button if no patient found
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def update_patient(self):
        try:
            patient_data = (
                self.entries['password'].get(),
                self.entries['first_name'].get(),
                self.entries['last_name'].get(),
                self.entries['date_of_birth'].get(),
                self.entries['gender'].get(),
                self.entries['address'].get(),
                self.entries['city'].get(),
                self.entries['state'].get(),
                self.entries['postal_pin'].get(),
                self.entries['phone'].get(),
                self.entries['email'].get(),
                self.entries['contact_name'].get(),
                self.entries['contact_no'].get(),
                self.entries['date_of_registration'].get(),
                self.entries['date_of_discharge'].get(),
                self.patient_id_entry.get()  # Get the patient ID from the entry field
            )

            cursor = self.db.cursor()
            cursor.execute(""" 
                UPDATE patient
                SET password=%s, firstname=%s, lastname=%s, dob=%s, gender=%s, address=%s, city=%s, state=%s, postalpin=%s, phoneno=%s, email=%s, contactname=%s, contactno=%s, doreg=%s, dodis=%s
                WHERE patientid=%s
            """, patient_data)
            self.db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Patient details updated successfully")
            else:
                messagebox.showwarning("Not Found", "No patient found with this ID")

            # Clear the text areas after successful update
            self.clear_entries()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def clear_entries(self):
        """Clear all entry fields."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def select_patient(self):
        patientid = simpledialog.askstring("Select Patient", "Enter Patient ID:")
        if patientid:
            self.fetch_patient_details(patientid)


# Function to open the update patient page
def open_updt_patient_page():
    updt_patient_window = tk.Toplevel()
    UpdatePatientPage(updt_patient_window)


# Main application window
def main():
    root = tk.Tk()
    root.title('Patient Management System')
    root.geometry('400x200+50+50')

    # Button to open the update patient page
    tk.Button(root, text="Update Patient", command=open_updt_patient_page).pack(pady=50)

    root.mainloop()

'''if __name__ == "__main__":
    main()'''
