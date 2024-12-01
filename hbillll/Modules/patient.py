from tkinter import Toplevel, Label, Menu
from PIL import ImageTk, Image
import os
from view_bill import open_view_bill_and_payment_window


def open_patient_page():
    patient_window = Toplevel()
    patient_window.title('Patient')
    patient_window.geometry('998x660+50+50')
    patient_window.resizable(0, 0)

    path_to_image = '../image/patient.jpg'
    try:
        bgImage = ImageTk.PhotoImage(Image.open(path_to_image))
    except FileNotFoundError:
        print(f"Image file not found at: {os.path.abspath(path_to_image)}")
        bgImage = None

    if bgImage:
        bgLabel = Label(patient_window, image=bgImage)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

    menu_bar = Menu(patient_window)

    patient_bill_menu = Menu(menu_bar, tearoff=0)
    patient_bill_menu.add_command(label="View Bill",command=open_view_bill_and_payment_window)
    menu_bar.add_cascade(label="Patient Bill", menu=patient_bill_menu)

    about_hospital_menu = Menu(menu_bar, tearoff=0)
    about_hospital_menu.add_command(label="About Hospital")
    menu_bar.add_cascade(label="About Hospital", menu=about_hospital_menu)

    patient_window.config(menu=menu_bar)

    patient_window.images = {'bgImage': bgImage}
