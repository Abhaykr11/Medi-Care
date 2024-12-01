import tkinter as tk
from tkinter import messagebox
import mysql.connector


class DeletePatientPage:
    def __init__(self, root):
        self.entry_patientid = None
        self.root = root
        self.db = self.get_db_connection()

        # Initialize UI components
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
        self.root.title('Delete Patient')
        self.root.geometry('300x150+50+50')
        self.root.resizable(0, 0)

        # Labels and Entry fields
        tk.Label(self.root, text="Patient ID").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_patientid = tk.Entry(self.root)
        self.entry_patientid.grid(row=0, column=1, padx=10, pady=10)

        # Delete Patient Button
        tk.Button(self.root, text="Delete Patient", command=self.delete_patient).grid(row=1, column=0, columnspan=2,
                                                                                      pady=10)

    def delete_patient(self):
        patientid = self.entry_patientid.get()

        if not patientid:
            messagebox.showwarning("Input Error", "Patient ID is required")
            return

        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM patient WHERE patientid=%s", (patientid,))

            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "No patient found with this ID")
            else:
                self.db.commit()
                messagebox.showinfo("Success", "Patient deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            self.entry_patientid.delete(0, tk.END)


# Function to open the delete patient page
def open_dlt_patient_page():
    dlt_patient_window = tk.Toplevel()
    DeletePatientPage(dlt_patient_window)
