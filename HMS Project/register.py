import os
import re
import bcrypt
import hashlib
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")

        # Background
        bg_img = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\back.jpg")
        bg_img = bg_img.resize((1550, 800), Image.Resampling.LANCZOS)  # Resize to window dimensions
        self.bg = ImageTk.PhotoImage(bg_img)

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, width=1550, height=800)

        # Left Image
        left_img = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\thought-good-morning-messages-LoveSove.jpg")
        left_img = left_img.resize((470, 550), Image.Resampling.LANCZOS)  # high-quality resize
        self.bg1 = ImageTk.PhotoImage(left_img)

        lbl_bg1 = Label(self.root, image=self.bg1)
        lbl_bg1.place(x=100, y=100, width=470, height=550)

        # Frame
        frame = Frame(self.root, bg="white")
        frame.place(x=570, y=100, width=800, height=550)

        register_lbl = Label(frame, text="Register Here", font=("times new roman", 20, "bold"), fg="darkgreen", bg="white")
        register_lbl.place(x=20, y=20)

        # Row 1
        Label(frame, text="First Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=100)
        self.fname_entry = ttk.Entry(frame, font=("times new roman", 15))
        self.fname_entry.place(x=50, y=135, width=250)

        Label(frame, text="Last Name", font=("times new roman", 15, "bold"), bg="white").place(x=390, y=100)
        self.lname_entry = ttk.Entry(frame, font=("times new roman", 15))
        self.lname_entry.place(x=390, y=135, width=250)

        # Row 2
        Label(frame, text="Contact No.", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=180)
        self.contact_entry = ttk.Entry(frame, font=("times new roman", 15))
        self.contact_entry.place(x=50, y=210, width=250)

        Label(frame, text="Email", font=("times new roman", 15, "bold"), bg="white").place(x=390, y=180)
        self.email_entry = ttk.Entry(frame, font=("times new roman", 15))
        self.email_entry.place(x=390, y=210, width=250)

        # Row 3
        Label(frame, text="Security Question", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=260)
        self.combo_security_Q = ttk.Combobox(frame, font=("times new roman", 15), state="readonly")
        self.combo_security_Q["values"] = ("Select", "Your Pet Name", "Your Birth Place", "Your Best Friend")
        self.combo_security_Q.place(x=50, y=290, width=250)
        self.combo_security_Q.current(0)

        Label(frame, text="Security Answer", font=("times new roman", 15, "bold"), bg="white").place(x=390, y=260)
        self.security_A_entry = ttk.Entry(frame, font=("times new roman", 15))
        self.security_A_entry.place(x=390, y=290, width=250)

        # Password Row
        Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=340)
        self.pswd_entry = ttk.Entry(frame, font=("times new roman", 15), show="*")
        self.pswd_entry.place(x=50, y=370, width=250)

        Label(frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white").place(x=390, y=340)
        self.confirm_pswd_entry = ttk.Entry(frame, font=("times new roman", 15), show="*")
        self.confirm_pswd_entry.place(x=390, y=370, width=250)

        # Eye Button Images
        eye_open = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\Icon\eye_open.jpg").resize((20, 20))
        eye_closed = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\Icon\eye_closed.png").resize((20, 20))
        self.eye_open_img = ImageTk.PhotoImage(eye_open)
        self.eye_closed_img = ImageTk.PhotoImage(eye_closed)

        # Eye Buttons
        self.show_password = False
        self.show_confirm_password = False

        self.eye_btn1 = Button(self.pswd_entry, cursor="hand2",image=self.eye_closed_img, command=self.toggle_password, bg="white", bd=0)
        self.eye_btn1.place(x=225, y=3)

        self.eye_btn2 = Button(self.confirm_pswd_entry,cursor="hand2", image=self.eye_closed_img, command=self.toggle_confirm_password, bg="white", bd=0)
        self.eye_btn2.place(x=225, y=3)

        # Check Button
        self.var_check = IntVar()
        checkbtn = Checkbutton(frame, variable=self.var_check, text="I Agree to the Terms & Conditions", font=("times new roman", 10, "bold"), bg="white", onvalue=1, offvalue=0)
        checkbtn.place(x=50, y=420)

        # Register Button
        img = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\register-now-button1.jpg")
        img = img.resize((150, 50))
        self.register_btn_img = ImageTk.PhotoImage(img)
        Button(frame, image=self.register_btn_img, command=self.register_data, borderwidth=0, cursor="hand2").place(x=50, y=460)

        # Login Button
        img1 = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\loginpng.png")
        img1 = img1.resize((130, 40))
        self.login_btn_img = ImageTk.PhotoImage(img1)
        Button(frame, image=self.login_btn_img, command=self.open_login,borderwidth=0, cursor="hand2").place(x=340, y=470)

    def toggle_password(self):
        if self.show_password:
            self.pswd_entry.config(show="*")
            self.eye_btn1.config(image=self.eye_closed_img)
        else:
            self.pswd_entry.config(show="")
            self.eye_btn1.config(image=self.eye_open_img)
        self.show_password = not self.show_password

    def toggle_confirm_password(self):
        if self.show_confirm_password:
            self.confirm_pswd_entry.config(show="*")
            self.eye_btn2.config(image=self.eye_closed_img)
        else:
            self.confirm_pswd_entry.config(show="")
            self.eye_btn2.config(image=self.eye_open_img)
        self.show_confirm_password = not self.show_confirm_password

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_data(self):
        if (self.fname_entry.get() == "" or
            self.email_entry.get() == "" or
            self.pswd_entry.get() == "" or
            self.combo_security_Q.get() == "Select"):
            messagebox.showerror("Error", "All fields are required")
        elif self.pswd_entry.get() != self.confirm_pswd_entry.get():
            messagebox.showerror("Error", "Passwords do not match")
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to the Terms & Conditions")
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="server",
                    database="hotel_management"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM register WHERE email=%s", (self.email_entry.get(),))
                row = my_cursor.fetchone()
                if row:
                    messagebox.showerror("Error", "User already exists with this email")
                else:
                    my_cursor.execute("INSERT INTO register (fname, lname, contact, email, securityQ, securityA, password) VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                        self.fname_entry.get(),
                        self.lname_entry.get(),
                        self.contact_entry.get(),
                        self.email_entry.get(),
                        self.combo_security_Q.get(),
                        self.security_A_entry.get(),
                        self.hash_password(self.pswd_entry.get())
                    ))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Registered Successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}")


    def open_login(self):
        self.root.destroy()
        os.system("python login.py")  # Adjust if your login file has a different name


if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
