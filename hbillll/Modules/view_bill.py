from tkinter import *
from tkinter import messagebox
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port=3306,
    database="hbill"
)

cursor = mydb.cursor()


# Fetch Bill Details by Patient ID
def get_bill_details_by_patient_id(patient_id):
    cursor.execute("SELECT * FROM bill WHERE patientid = %s", (patient_id,))
    return cursor.fetchone()


# Function to update the bill status and set the total amount to zero
def update_bill_as_paid(bill_id):
    cursor.execute("UPDATE bill SET status = 'Paid', total = 0 WHERE billid = %s", (bill_id,))
    mydb.commit()


# Process card payment
def process_card_payment(bill_id, patient_id, card_window, frame):
    # Update the database
    update_bill_as_paid(bill_id)
    messagebox.showinfo("Payment Success", "Your payment was successful! The bill is now marked as Paid.")
    card_window.destroy()

    # Refresh the frame to display updated bill details
    refresh_bill_details(frame, patient_id)


# Open the card payment window
def open_card_payment_window(bill_id, frame, patient_id):
    card_window = Toplevel()
    card_window.title("Card Payment")
    card_window.geometry("400x300")

    Label(card_window, text="Enter Card Details", font=("Arial", 14, "bold")).pack(pady=10)

    Label(card_window, text="Card Number:", font=("Arial", 10)).pack(anchor=W, padx=20)
    card_number_entry = Entry(card_window, width=30)
    card_number_entry.pack(padx=20, pady=5)

    Label(card_window, text="CVV:", font=("Arial", 10)).pack(anchor=W, padx=20)
    cvv_entry = Entry(card_window, width=10, show="*")
    cvv_entry.pack(padx=20, pady=5)

    def validate_and_pay():
        card_number = card_number_entry.get().strip()
        cvv = cvv_entry.get().strip()

        if len(card_number) != 16 or not card_number.isdigit():
            messagebox.showerror("Validation Error", "Please enter a valid 16-digit card number.")
            return

        if len(cvv) != 3 or not cvv.isdigit():
            messagebox.showerror("Validation Error", "Please enter a valid 3-digit CVV.")
            return

        # Simulate successful card payment
        process_card_payment(bill_id, patient_id, card_window, frame)

    Button(card_window, text="Pay Now", width=20, command=validate_and_pay).pack(pady=20)


# Handle payment
def make_payment(bill_id, patient_id, frame):
    # Fetch the bill details
    bill_details = get_bill_details_by_patient_id(patient_id)

    if bill_details:
        _, _, _, _, _, _, _, total, status = bill_details

        if status == 'Paid':
            messagebox.showinfo("Already Paid", f"The bill for Patient ID {patient_id} is already paid.")
        else:
            # Open the payment window
            open_card_payment_window(bill_id, frame, patient_id)
    else:
        messagebox.showerror("Error", "No bill found for this patient ID.")


# Refresh bill details
def refresh_bill_details(frame, patient_id):
    for widget in frame.winfo_children():
        widget.destroy()
    view_bill(frame, patient_id=patient_id)


# View bill
def view_bill(frame, patient_id_entry=None, patient_id=None):
    if not patient_id:
        patient_id = patient_id_entry.get().strip()

    if patient_id == "":
        messagebox.showerror("Input Error", "Please enter a valid Patient ID.")
        return

    # Fetch bill details
    bill_details = get_bill_details_by_patient_id(patient_id)

    if bill_details:
        billid, _, doctor_fee, nursing_fee, room_fee, ambu_fee, med_fee, total, status = bill_details

        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Display bill details
        Label(frame, text=f"Patient ID: {patient_id}", font=("Arial", 10)).grid(row=0, column=0, sticky=W)
        Label(frame, text=f"Bill ID: {billid}", font=("Arial", 10)).grid(row=1, column=0, sticky=W)
        Label(frame, text=f"Doctor Fee: ₹{doctor_fee}", font=("Arial", 10)).grid(row=2, column=0, sticky=W)
        Label(frame, text=f"Nursing Fee: ₹{nursing_fee}", font=("Arial", 10)).grid(row=3, column=0, sticky=W)
        Label(frame, text=f"Room Fee: ₹{room_fee}", font=("Arial", 10)).grid(row=4, column=0, sticky=W)
        Label(frame, text=f"Ambulance Fee: ₹{ambu_fee}", font=("Arial", 10)).grid(row=5, column=0, sticky=W)
        Label(frame, text=f"Medicine Fee: ₹{med_fee}", font=("Arial", 10)).grid(row=6, column=0, sticky=W)
        Label(frame, text=f"Total Amount: ₹{total}", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky=W)
        Label(frame, text=f"Status: {status}", font=("Arial", 10)).grid(row=8, column=0, sticky=W)

        # Payment button
        if status == "Unpaid":
            Button(frame, text="Pay Bill", command=lambda: make_payment(billid, patient_id, frame)).grid(row=9, column=0, pady=10)
        else:
            Label(frame, text="Bill is already paid.", font=("Arial", 10, "bold"), fg="green").grid(row=9, column=0, pady=10)
    else:
        messagebox.showerror("No Bill Found", f"No bill found for Patient ID: {patient_id}")


# Open bill viewing and payment window
def open_view_bill_and_payment_window():
    view_bill_window = Toplevel()
    view_bill_window.title("View Bill and Payment")
    view_bill_window.geometry("600x400")

    frame = Frame(view_bill_window, padx=20, pady=20)
    frame.grid(row=0, column=0)

    Label(frame, text="Enter Patient ID:", font=("Arial", 10)).grid(row=0, column=0, sticky=W)
    patient_id_entry = Entry(frame, width=20)
    patient_id_entry.grid(row=0, column=1)

    Button(frame, text="View Bill", command=lambda: view_bill(frame, patient_id_entry)).grid(row=0, column=2, padx=10)


# Main Window
'''
root = Tk()
root.title("Hospital Billing System")
root.geometry("400x200")

Button(root, text="View Bill and Make Payment", command=open_view_bill_and_payment_window).pack(pady=50)

root.mainloop()
'''