import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# Connect to the MySQL database with a buffered cursor
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='root',
    port=3306,
    database='hbill'
)

cursor = mydb.cursor(buffered=True)  # Use buffered cursor to handle unread results

# Create Bill Table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS bill (
    billid INT AUTO_INCREMENT PRIMARY KEY,
    patientid INT,
    doctorfee DECIMAL(10, 2),
    nursingfee DECIMAL(10, 2),
    roomfee DECIMAL(10, 2),
    ambufee DECIMAL(10, 2),
    medfee DECIMAL(10, 2),
    total DECIMAL(10, 2),
    status VARCHAR(10),
    FOREIGN KEY (patientid) REFERENCES patient(patientid)
)''')


# Function to fetch patients based on search criteria (name or patient ID)
def search_patient(search_term):
    try:
        cursor.execute("SELECT patientid, firstname FROM patient WHERE patientid LIKE %s OR firstname LIKE %s",
                       (f"%{search_term}%", f"%{search_term}%"))
        return cursor.fetchall()  # Ensure all results are fetched
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching patients: {err}")
        return []


# Function to check if a bill has already been generated for the patient
def is_bill_generated(patient_id):
    try:
        cursor.execute("SELECT * FROM bill WHERE patientid = %s", (patient_id,))
        return cursor.fetchone() is not None  # Fetch the result to prevent unread result errors
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error checking bill: {err}")
        return False


# Function to reset the form and clear the inputs
def reset_form(search_entry, results_frame, fee_entries, generate_bill_button):
    search_entry.delete(0, END)
    results_frame.delete(*results_frame.get_children())
    for entry in fee_entries:
        entry.delete(0, END)
        entry.config(state=DISABLED)
    generate_bill_button.config(state=DISABLED)


# Function to generate the bill
def generate_bill(patient_id, doctor_fee_entry, nursing_fee_entry, room_fee_entry, ambu_fee_entry, med_fee_entry,
                  search_entry, results_frame, fee_entries, generate_bill_button):
    try:
        # Fetch fee values and calculate the total
        doctor_fee = float(doctor_fee_entry.get())
        nursing_fee = float(nursing_fee_entry.get())
        room_fee = float(room_fee_entry.get())
        ambu_fee = float(ambu_fee_entry.get())
        med_fee = float(med_fee_entry.get())
        total = doctor_fee + nursing_fee + room_fee + ambu_fee + med_fee

        # Check if a bill is already generated
        if is_bill_generated(patient_id):
            messagebox.showinfo("Info", "Bill is already generated, please update the bill.")
            reset_form(search_entry, results_frame, fee_entries, generate_bill_button)
        else:
            # Insert new bill record into the database with status 'Unpaid'
            cursor.execute('''INSERT INTO bill (patientid, doctorfee, nursingfee, roomfee, ambufee, medfee, total, status) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                           (patient_id, doctor_fee, nursing_fee, room_fee, ambu_fee, med_fee, total, 'Unpaid'))
            mydb.commit()
            messagebox.showinfo("Success", f"Bill Generated! Total Amount: {total}")
            reset_form(search_entry, results_frame, fee_entries, generate_bill_button)  # Reset after success
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for fees.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error generating bill: {err}")


# Function to handle patient selection from the search result
def on_patient_select(results_frame, fee_entries, generate_bill_button, search_entry):
    selected_item = results_frame.item(results_frame.selection())['values']
    if not selected_item:
        return  # No selection made

    patient_id = selected_item[0]

    # Check if the bill is already generated for the selected patient
    if is_bill_generated(patient_id):
        messagebox.showinfo("Info", "Bill is already generated for this patient. Please update the bill.")
        # Ensure fee entries and button remain disabled
        for entry in fee_entries:
            entry.config(state=DISABLED)
        generate_bill_button.config(state=DISABLED)
        reset_form(search_entry, results_frame, fee_entries, generate_bill_button)
    else:
        # Enable all fee entry fields and the "Generate Bill" button
        for entry in fee_entries:
            entry.config(state=NORMAL)
            entry.delete(0, END)  # Clear previous entries
        generate_bill_button.config(state=NORMAL)


# Function to search for patients and populate search results
def search_and_display_results(search_entry, results_frame):
    search_term = search_entry.get().strip()

    if not search_term:
        messagebox.showerror("Error", "Please enter a valid patient ID or name.")
        return

    results_frame.delete(*results_frame.get_children())  # Clear previous search results

    patient_list = search_patient(search_term)
    if patient_list:
        for patient in patient_list:
            results_frame.insert("", "end", values=(patient[0], patient[1]))
    else:
        messagebox.showinfo("No Results", "No patients found matching the search term.")


# Function to open the bill generation window
def open_add_bill_page():
    bill_window = Tk()  # Create the main window directly
    bill_window.title("Hospital Bill Generation")
    bill_window.geometry('700x500')  # Set a larger window size

    # Frame for search bar and patient search result list
    search_frame = Frame(bill_window)
    search_frame.grid(row=0, column=0, padx=20, pady=10, sticky=W)

    search_label = Label(search_frame, text="Search Patient (ID or Name):")
    search_label.grid(row=0, column=0, sticky=W)

    search_entry = Entry(search_frame)
    search_entry.grid(row=0, column=1, padx=5)

    search_button = Button(search_frame, text="Search",
                           command=lambda: search_and_display_results(search_entry, results_frame))
    search_button.grid(row=0, column=2, padx=5)

    # Treeview for displaying search results
    columns = ("Patient ID", "Name")
    results_frame = ttk.Treeview(bill_window, columns=columns, show="headings")
    results_frame.heading("Patient ID", text="Patient ID")
    results_frame.heading("Name", text="Name")
    results_frame.grid(row=1, column=0, padx=20, pady=10, sticky=W + E)

    # List to hold references to fee entry fields
    fee_entries = []

    # Frame for entering bill details
    bill_details_frame = Frame(bill_window, padx=20, pady=20)
    bill_details_frame.grid(row=2, column=0, sticky=W + E)

    # Doctor Fee input
    doctor_fee_label = Label(bill_details_frame, text="Doctor Fee")
    doctor_fee_label.grid(row=0, column=0, sticky=W)
    doctor_fee_entry = Entry(bill_details_frame, state=DISABLED)
    doctor_fee_entry.grid(row=0, column=1, padx=5)
    fee_entries.append(doctor_fee_entry)

    # Nursing Fee input
    nursing_fee_label = Label(bill_details_frame, text="Nursing Fee")
    nursing_fee_label.grid(row=1, column=0, sticky=W)
    nursing_fee_entry = Entry(bill_details_frame, state=DISABLED)
    nursing_fee_entry.grid(row=1, column=1, padx=5)
    fee_entries.append(nursing_fee_entry)

    # Room Fee input
    room_fee_label = Label(bill_details_frame, text="Room Fee")
    room_fee_label.grid(row=2, column=0, sticky=W)
    room_fee_entry = Entry(bill_details_frame, state=DISABLED)
    room_fee_entry.grid(row=2, column=1, padx=5)
    fee_entries.append(room_fee_entry)

    # Ambulance Fee input
    ambu_fee_label = Label(bill_details_frame, text="Ambulance Fee")
    ambu_fee_label.grid(row=3, column=0, sticky=W)
    ambu_fee_entry = Entry(bill_details_frame, state=DISABLED)
    ambu_fee_entry.grid(row=3, column=1, padx=5)
    fee_entries.append(ambu_fee_entry)

    # Medicine Fee input
    med_fee_label = Label(bill_details_frame, text="Medicine Fee")
    med_fee_label.grid(row=4, column=0, sticky=W)
    med_fee_entry = Entry(bill_details_frame, state=DISABLED)
    med_fee_entry.grid(row=4, column=1, padx=5)
    fee_entries.append(med_fee_entry)

    # Generate Bill Button (disabled initially)
    generate_bill_button = Button(bill_details_frame, text="Generate Bill", state=DISABLED,
                                  command=lambda: generate_bill(
                                      results_frame.item(results_frame.selection())['values'][0],
                                      doctor_fee_entry, nursing_fee_entry, room_fee_entry, ambu_fee_entry,
                                      med_fee_entry, search_entry, results_frame, fee_entries, generate_bill_button))
    generate_bill_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Attach patient selection handler to the treeview
    results_frame.bind("<<TreeviewSelect>>",
                       lambda _: on_patient_select(results_frame, fee_entries, generate_bill_button, search_entry))

    bill_window.mainloop()

'''
# Open the bill generation page
open_add_bill_page()'''
