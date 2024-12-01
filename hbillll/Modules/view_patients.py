import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


def view_patients():
    try:
        # Establish connection to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="hbill",  # Your database name
            port=3306  # Your port number
        )
        cursor = conn.cursor()

        # Query to fetch all patient details
        query = "SELECT patientid, firstname, lastname, dob, gender, address, city, state, postalpin, phoneno, email, contactname, contactno, doreg, dodis FROM patient"
        cursor.execute(query)
        records = cursor.fetchall()

        # Create the main window
        root = tk.Tk()
        root.title("View All Patients")
        root.geometry("998x660+50+50")  # Set window size

        # Function to search patients based on input
        def search():
            search_query = search_entry.get().strip()

            try:
                # Re-establish the connection inside the search function
                conn_search = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="hbill",
                    port=3306
                )
                cursor_search = conn_search.cursor()

                for item in tree.get_children():
                    tree.delete(item)

                # Query to search for patients based on patientid, firstname, lastname, or email
                search_sql = """
                    SELECT patientid, firstname, lastname, dob, gender, address, city, state, postalpin, phoneno, email, contactname, contactno, doreg, dodis 
                    FROM patient 
                    WHERE patientid LIKE %s OR firstname LIKE %s OR lastname LIKE %s OR email LIKE %s
                """
                search_values = ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
                cursor_search.execute(search_sql, search_values)
                search_results = cursor_search.fetchall()

                for row in search_results:
                    tree.insert("", "end", values=row)

                # Close the cursor and connection used for searching
                cursor_search.close()
                conn_search.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        # Create a frame for the search bar
        search_frame = tk.Frame(root)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        search_label = tk.Label(search_frame, text="Search Patient:")
        search_label.pack(side=tk.LEFT, padx=5)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(search_frame, text="Search", command=search)
        search_button.pack(side=tk.LEFT, padx=5)

        # Create a frame for the table and scrollbars
        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Treeview for displaying the data
        tree = ttk.Treeview(table_frame, columns=(
            "ID", "First Name", "Last Name", "DOB", "Gender", "Address", "City", "State", "Postal Pin", "Phone No", "Email",
            "Contact Name", "Contact No", "Date of Reg", "Date of Discharge"), show="headings")

        # Define headings and columns
        tree.heading("ID", text="Patient ID")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("DOB", text="Date of Birth")
        tree.heading("Gender", text="Gender")
        tree.heading("Address", text="Address")
        tree.heading("City", text="City")
        tree.heading("State", text="State")
        tree.heading("Postal Pin", text="Postal Pin")
        tree.heading("Phone No", text="Phone No")
        tree.heading("Email", text="Email")
        tree.heading("Contact Name", text="Contact Name")
        tree.heading("Contact No", text="Contact No")
        tree.heading("Date of Reg", text="Date of Registration")
        tree.heading("Date of Discharge", text="Date of Discharge")

        # Define column width
        for col in tree["columns"]:
            tree.column(col, width=120)

        # Add scrollbars
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add data to Treeview
        for row in records:
            tree.insert("", "end", values=row)

        tree.pack(fill=tk.BOTH, expand=True)

        # Add color styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', 'blue')])

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Run the window
        root.mainloop()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


'''# Call the function to view patient details
view_patients()
'''