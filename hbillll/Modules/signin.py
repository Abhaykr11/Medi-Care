import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import re  # For validation using regular expressions

from Modules import admin, employee, patient


def create_login_window(page_type):
    def user_enter(event):
        if usernameEntry.get() == 'Username':
            usernameEntry.delete(0, END)

    def password_enter(event):
        if passwordEntry.get() == 'Password':
            passwordEntry.delete(0, END)

    def hide():
        openeye.config(file='../image/closeye.png')
        passwordEntry.config(show='*')
        eyeButton.config(command=show)

    def show():
        openeye.config(file='../image/openeye.png')
        passwordEntry.config(show='')
        eyeButton.config(command=hide)

    def validate_username(username):
        """Validate username: only letters and digits allowed."""
        return re.match(r'^[A-Za-z0-9]+$', username) is not None

    def validate_password(password):
        """Validate password:
        - Maximum 10 characters.
        - Must contain at least one uppercase, one lowercase, one digit, and one special character.
        """
        if len(password) > 10:
            return False
        return (
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        )

    def login():
        user_id = usernameEntry.get()
        password = passwordEntry.get()

        # Validate username and password
        if not validate_username(user_id):
            messagebox.showerror("Invalid Username", "Username should only contain letters and digits.")
            return
        if not validate_password(password):
            messagebox.showerror(
                "Invalid Password",
                "Password must:\n"
                "- Be at most 10 characters long.\n"
                "- Contain at least one uppercase, one lowercase, one digit, and one special character."
            )
            return

        table = ""
        id_field = ""

        if page_type == 'admin':
            table = "admin"
            id_field = "adminid"
        elif page_type == 'employee':
            table = "employee"
            id_field = "empid"
        elif page_type == 'patient':
            table = "patient"
            id_field = "patientid"

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="hbill"
            )
            cursor = conn.cursor()
            query = f'SELECT * FROM {table} WHERE {id_field}=%s AND password=%s'
            cursor.execute(query, (user_id, password))
            user = cursor.fetchone()

            if user:
                print("Login successful")
                if page_type == 'admin':
                    admin.open_admin_page()
                elif page_type == 'employee':
                    employee.open_employee_page()
                elif page_type == 'patient':
                    patient.open_patient_page()
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            messagebox.showerror("Database Error", "An error occurred while connecting to the database.")
        finally:
            if conn:
                conn.close()

    login_window = Toplevel()
    login_window.title('Login')
    login_window.geometry('998x660+50+50')
    login_window.resizable(0, 0)

    bgImage = ImageTk.PhotoImage(file='../image/bg.jpg')
    openeye = PhotoImage(file='../image/openeye.png')
    closeye = PhotoImage(file='../image/closeye.png')

    bgLabel = Label(login_window, image=bgImage)
    bgLabel.grid(row=0, column=0)
    bgLabel.place(x=0, y=0)

    heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yauheni UI Light', 23, 'bold'),
                    bg='white', fg='firebrick1')
    heading.place(x=605, y=120)

    usernameEntry = Entry(login_window, width=25, font=('Microsoft Yauheni UI Light', 11, 'bold'), bd=0,
                          fg='firebrick1')
    usernameEntry.place(x=580, y=200)
    usernameEntry.insert(0, 'Username')
    usernameEntry.bind('<FocusIn>', user_enter)
    Frame(login_window, width=250, height=2, bg='firebrick1').place(x=580, y=222)

    passwordEntry = Entry(login_window, width=25, font=('Microsoft Yauheni UI Light', 11, 'bold'), bd=0,
                          fg='firebrick1', show='*')
    passwordEntry.place(x=580, y=260)
    passwordEntry.insert(0, 'Password')
    passwordEntry.bind('<FocusIn>', password_enter)
    Frame(login_window, width=250, height=2, bg='firebrick1').place(x=580, y=282)

    eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white',
                       cursor='hand2', command=show)
    eyeButton.place(x=800, y=255)

    loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white',
                         bg='firebrick1', activebackground='firebrick1', activeforeground='white', cursor='hand2', bd=0,
                         width=19, command=login)
    loginButton.place(x=578, y=350)

    login_window.images = {'bgImage': bgImage, 'openeye': openeye, 'closeye': closeye}
