from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import hashlib
import os

class login:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\SDT_Zoom-Backgrounds_April-8_Windansea-1-logo-1.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)

        img1 = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\LoginIconAppl.png")
        img1 = img1.resize((100, 100), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimg1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=175, width=100, height=100)

        get_str = Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=95, y=105)

        # Username
        username = Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black")
        username.place(x=70, y=155)
        self.txtuser = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=40, y=185, width=270)

        # Password
        password = Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        password.place(x=70, y=225)
        self.txtpass = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.txtpass.place(x=40, y=250, width=270)

        #eye button image
        eye_open = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\Icon\eye_open.jpg").resize((20, 20))
        eye_closed = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\Icon\eye_closed.png").resize((20, 20))
        self.eye_open_img = ImageTk.PhotoImage(eye_open)
        self.eye_closed_img = ImageTk.PhotoImage(eye_closed)

        # Eye Buttons
        self.show_password = False

        self.eye_btn1 = Button(self.txtpass, cursor="hand2",image=self.eye_closed_img, command=self.toggle_password, bg="white", bd=0)
        self.eye_btn1.place(x=245, y=3)

        # Icons
        img2 = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\LoginIconAppl.png").resize((25, 25))
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(image=self.photoimg2, bg="black", borderwidth=0).place(x=655, y=325, width=25, height=25)

        img3 = Image.open(r"C:\Users\shiva\Desktop\HMS Project\images\hotel images\34971dc4-ae18-412d-9c04-d38db704ef2c.jpeg").resize((25, 25))
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(image=self.photoimg3, bg="black", borderwidth=0).place(x=655, y=393, width=25, height=25)

        # Login Button
        loginbtn = Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=110, y=300, width=120, height=35)

        # Register Button
        registerbtn = Button(frame, text="New User Register", command=self.open_register,font=("times new roman", 12, "bold"), borderwidth=0, fg="white", bg="black")
        registerbtn.place(x=15, y=355, width=160)

        # Forgot Password Button
        forgotbtn = Button(frame, text="Forgot Password?", command=self.forgot_password_window,font=("times new roman", 12, "bold"), borderwidth=0,fg="white", bg="black", activeforeground="white", activebackground="black")
        forgotbtn.place(x=10, y=380, width=150)

    def toggle_password(self):
        if self.show_password:
            self.txtpass.config(show="*")
            self.eye_btn1.config(image=self.eye_closed_img)
        else:
            self.txtpass.config(show="")
            self.eye_btn1.config(image=self.eye_open_img)
        self.show_password = not self.show_password

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",                   
                password="server",       
                database="hotel_management"    
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT password FROM register WHERE email=%s", (self.txtuser.get(),))
            row = my_cursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Invalid username")
            else:
                hashed_input = hashlib.sha256(self.txtpass.get().encode()).hexdigest()
                if hashed_input == row[0]:
                    # messagebox.showinfo("Success", "Login Successful")
                    self.root.destroy()
                    os.system("python home.py")
                else:
                    messagebox.showerror("Error", "Invalid password")
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {str(e)}")

    def open_register(self):
        try:
            os.system("python register.py")
        except:
            messagebox.showerror("Error", "register.py not found")

    def forgot_password_window(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please enter your email to reset password")
            return

        self.top = Toplevel()
        self.top.title("Forgot Password")
        self.top.geometry("400x350+600+200")
        self.top.config(bg="white")

        Label(self.top, text="Forgot Password", font=("times new roman", 18, "bold"), bg="white", fg="red").place(x=100, y=20)

        Label(self.top, text="Security Question", font=("times new roman", 15), bg="white").place(x=50, y=70)
        self.combo_security_Q = ttk.Combobox(self.top, font=("times new roman", 13), state="readonly")
        self.combo_security_Q["values"] = ("Select", "Your Birth Place", "Your Pet Name", "Your Best Friend")
        self.combo_security_Q.place(x=50, y=100, width=300)
        self.combo_security_Q.current(0)

        Label(self.top, text="Answer", font=("times new roman", 15), bg="white").place(x=50, y=140)
        self.txt_answer = ttk.Entry(self.top, font=("times new roman", 13))
        self.txt_answer.place(x=50, y=170, width=300)

        Label(self.top, text="New Password", font=("times new roman", 15), bg="white").place(x=50, y=210)
        self.txt_new_pass = ttk.Entry(self.top, font=("times new roman", 13), show="*")
        self.txt_new_pass.place(x=50, y=240, width=300)

        Button(self.top, text="Reset", font=("times new roman", 13, "bold"),bg="green", fg="white", command=self.reset_password).place(x=150, y=280, width=100)

    def reset_password(self):
        if (self.combo_security_Q.get() == "Select" or
            self.txt_answer.get() == "" or
            self.txt_new_pass.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=self.top)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="server",
                database="hotel_management"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM register WHERE email=%s AND securityQ=%s AND securityA=%s",
                        (self.txtuser.get(), self.combo_security_Q.get(), self.txt_answer.get()))
            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", "Incorrect security answer", parent=self.top)
            else:
                new_hashed = hashlib.sha256(self.txt_new_pass.get().encode()).hexdigest()
                cur.execute("UPDATE register SET password=%s WHERE email=%s", (new_hashed, self.txtuser.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password reset successful", parent=self.top)
                self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.top)


if __name__ == "__main__":
    root = Tk()
    app = login(root)
    root.mainloop()
