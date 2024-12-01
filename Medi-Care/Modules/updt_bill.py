import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='root',
    port=3306,
    database='hbill'
)

cursor = mydb.cursor()


# Fetch Patient IDs and Names from MySQL
def get_patient_ids_and_names():
    cursor.execute("SELECT patientid, firstname FROM patient")
    return cursor.fetchall()


# Fetch Bill Details by Patient ID
def get_existing_bill(patient_id):
    cursor.execute(
        "SELECT doctorfee, nursingfee, roomfee, ambufee, medfee, total, status FROM bill WHERE patientid = %s",
        (patient_id,))
    return cursor.fetchone()


# Function to update the bill with status check
def update_bill_with_status(patient_id_combobox, doctor_fee_entry, nursing_fee_entry, room_fee_entry, ambu_fee_entry,
                            med_fee_entry, existing_total_entry):
    try:
        patient_id = patient_id_combobox.get().split(' ')[0]  # Extract patient ID from combobox

        # Get fee values, defaulting to 0 if entry is empty
        doctor_fee = float(doctor_fee_entry.get() or 0)
        nursing_fee = float(nursing_fee_entry.get() or 0)
        room_fee = float(room_fee_entry.get() or 0)
        ambu_fee = float(ambu_fee_entry.get() or 0)
        med_fee = float(med_fee_entry.get() or 0)

        total = doctor_fee + nursing_fee + room_fee + ambu_fee + med_fee

        # Check if the bill exists and fetch current bill status
        existing_bill = get_existing_bill(patient_id)
        if not existing_bill:
            messagebox.showerror("Error", "No bill found for the selected patient.")
            return

        existing_status = existing_bill[6]

        # Update the bill and change the status to 'unpaid' if the bill was previously paid
        new_status = 'unpaid' if existing_status == 'paid' else existing_status

        cursor.execute('''UPDATE bill 
                          SET doctorfee = %s, nursingfee = %s, roomfee = %s, ambufee = %s, medfee = %s, total = %s, status = %s
                          WHERE patientid = %s''',
                       (doctor_fee, nursing_fee, room_fee, ambu_fee, med_fee, total, new_status, patient_id))
        mydb.commit()

        messagebox.showinfo("Success", "Bill Updated Successfully!")
        existing_total_entry.config(state='normal')  # Update the existing total field with new value
        existing_total_entry.delete(0, END)
        existing_total_entry.insert(0, total)
        existing_total_entry.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to open the update bill window
def open_update_bill_window():
    update_bill_window = Toplevel()
    update_bill_window.title("Update Bill")

    frame = Frame(update_bill_window, padx=20, pady=20)
    frame.grid(row=0, column=0)

    # Patient ID dropdown
    patient_id_label = Label(frame, text="Select Patient")
    patient_id_label.grid(row=0, column=0, sticky=W)
    patient_ids = get_patient_ids_and_names()
    patient_id_combobox = ttk.Combobox(frame, values=[f"{p[0]} - {p[1]}" for p in patient_ids])
    patient_id_combobox.grid(row=0, column=1)
    patient_id_combobox.current(0)

    # Display existing total in read-only field
    existing_total_label = Label(frame, text="Existing Total")
    existing_total_label.grid(row=1, column=0, sticky=W)
    existing_total_entry = Entry(frame, state='readonly')
    existing_total_entry.grid(row=1, column=1)

    def fetch_existing_bill():
        patient_id = patient_id_combobox.get().split(' ')[0]
        existing_bill = get_existing_bill(patient_id)
        if existing_bill:
            existing_total_entry.config(state='normal')
            existing_total_entry.delete(0, END)
            existing_total_entry.insert(0, existing_bill[5])  # Show the current total in read-only mode
            existing_total_entry.config(state='readonly')
        else:
            messagebox.showerror("Error", "No bill found for the selected patient.")

    # Button to fetch existing bill
    fetch_existing_bill_button = Button(frame, text="Fetch Existing Bill", command=fetch_existing_bill)
    fetch_existing_bill_button.grid(row=2, columnspan=2, pady=10)

    # New fees input fields
    doctor_fee_label = Label(frame, text="Doctor Fee")
    doctor_fee_label.grid(row=3, column=0, sticky=W)
    doctor_fee_entry = Entry(frame)
    doctor_fee_entry.grid(row=3, column=1)

    nursing_fee_label = Label(frame, text="Nursing Fee")
    nursing_fee_label.grid(row=4, column=0, sticky=W)
    nursing_fee_entry = Entry(frame)
    nursing_fee_entry.grid(row=4, column=1)

    room_fee_label = Label(frame, text="Room Fee")
    room_fee_label.grid(row=5, column=0, sticky=W)
    room_fee_entry = Entry(frame)
    room_fee_entry.grid(row=5, column=1)

    ambu_fee_label = Label(frame, text="Ambulance Fee")
    ambu_fee_label.grid(row=6, column=0, sticky=W)
    ambu_fee_entry = Entry(frame)
    ambu_fee_entry.grid(row=6, column=1)

    med_fee_label = Label(frame, text="Medicine Fee")
    med_fee_label.grid(row=7, column=0, sticky=W)
    med_fee_entry = Entry(frame)
    med_fee_entry.grid(row=7, column=1)

    # Update Bill Button
    update_bill_button = Button(frame, text="Update Bill",
                                command=lambda: update_bill_with_status(patient_id_combobox, doctor_fee_entry,
                                                                        nursing_fee_entry, room_fee_entry,
                                                                        ambu_fee_entry, med_fee_entry,
                                                                        existing_total_entry))
    update_bill_button.grid(row=8, columnspan=2, pady=10)


# Main Application
'''
root = Tk()
root.title("Update Bill System")
root.geometry("400x300")

# Button to open the update bill window
update_bill_button = Button(root, text="Update Bill", command=open_update_bill_window)
update_bill_button.pack(pady=20)

root.mainloop()

# Close the database connection when the application closes
mydb.close()
'''
