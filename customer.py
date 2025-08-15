from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector


class Cust_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1300x565+230+220")

        # MySQL Connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",          # <-- Replace with your MySQL username
                password="server",  # <-- Replace with your MySQL password
                database="hotel_management"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Connection failed:\n{e}")
            return

        # Title
        lbl_title = Label(self.root, text="ADD CUSTOMER DETAILS", font=("times new roman", 20, "bold"),bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1300, height=55)

        # Logo
        try:
            img2 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\logohotel.png")
            img2 = img2.resize((100, 53), Image.Resampling.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img2)
            lblimg = Label(self.root, image=self.photoimg2, relief=RIDGE)
            lblimg.place(x=0, y=0, width=100, height=55)
        except Exception as e:
            print("Logo image failed to load:", e)

        # Customer Details Frame
        labelframeleft = LabelFrame(self.root, text="Customer Details", font=("times new roman", 12, "bold"),
                                    bd=2, relief=RIDGE, padx=2)
        labelframeleft.place(x=0, y=55, width=400, height=505)

        # Fields
        self.labels = [
            "Customer Ref.", "Customer Name", "Father Name", "Gender", "Pin Code",
            "Mobile No.", "Email", "Nationality", "Id Proof", "Id No.", "Address"
        ]
        self.entries = []

        for i, text in enumerate(self.labels):
            lbl = Label(labelframeleft, text=text, font=("arial", 12, "bold"), padx=2, pady=6)
            lbl.grid(row=i, column=0, sticky=W)

            if text in ["Gender", "Nationality", "Id Proof"]:
                combo = ttk.Combobox(labelframeleft, font=("arial", 12, "bold"), width=21, state="readonly")
                combo_values = {
                    "Gender": ("Male", "Female", "Other"),
                    "Nationality": ("Indian", "Foreign"),
                    "Id Proof": ("Aadhar Card", "PAN Card", "Driving License")
                }
                combo["values"] = combo_values[text]
                combo.grid(row=i, column=1)
                self.entries.append(combo)
            else:
                entry = ttk.Entry(labelframeleft, width=23, font=("arial", 12, "bold"))
                entry.grid(row=i, column=1)
                self.entries.append(entry)

        # Button Frame
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=410, width=390, height=70)

        Button(btn_frame, text="Add", font=("arial", 11, "bold"), bg="black", fg="gold", width=20,
               command=self.add_customer).grid(row=0, column=0, padx=2, pady=2)
        Button(btn_frame, text="Update", font=("arial", 11, "bold"), bg="black", fg="gold", width=20,
               command=self.update_customer).grid(row=0, column=1, padx=2, pady=2)
        Button(btn_frame, text="Delete", font=("arial", 11, "bold"), bg="black", fg="gold", width=20,
               command=self.delete_customer).grid(row=1, column=0, padx=2, pady=2)
        Button(btn_frame, text="Reset", font=("arial", 11, "bold"), bg="black", fg="gold", width=20,
               command=self.reset_fields).grid(row=1, column=1, padx=2, pady=2)

        # Table Frame
        tableframe = LabelFrame(self.root, text="View Details", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, padx=2)
        tableframe.place(x=430, y=55, width=860, height=505)

        lblSearchby = Label(tableframe, text="Search By", font=("arial", 12, "bold"), bg="red", fg="white", padx=2)
        lblSearchby.grid(row=0, column=0, sticky=W, padx=3)

        self.combo_Searchby = ttk.Combobox(tableframe, font=("arial", 12, "bold"), width=21, state="readonly")
        self.combo_Searchby["values"] = ("name", "id_proof", "ref")
        self.combo_Searchby.grid(row=0, column=1, padx=3)

        self.txtsearch = ttk.Entry(tableframe, width=21, font=("arial", 12, "bold"))
        self.txtsearch.grid(row=0, column=2, padx=3)

        Button(tableframe, text="Search", font=("arial", 11, "bold"), bg="black", fg="gold", width=8,command=self.search_customer).grid(row=0, column=3, padx=6)

        Button(tableframe, text="Show All", font=("arial", 11, "bold"), bg="black", fg="gold", width=8,command=self.fetch_data).grid(row=0, column=4, padx=6)

        # Data Table
        data_frame = Frame(tableframe, bd=2, relief=RIDGE)
        data_frame.place(x=0, y=40, width=850, height=440)

        scroll_x = ttk.Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(data_frame, orient=VERTICAL)

        self.cust_details = ttk.Treeview(
            data_frame,
            columns=("ref", "name", "fname", "gender", "pincode", "mobile", "email", "nationality", "id_proof", "id_number", "address"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.cust_details.xview)
        scroll_y.config(command=self.cust_details.yview)

        for col in self.cust_details["columns"]:
            self.cust_details.heading(col, text=col.replace("_", " ").title())
            self.cust_details.column(col, width=100)

        self.cust_details["show"] = "headings"
        self.cust_details.pack(fill=BOTH, expand=1)
        self.cust_details.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def add_customer(self):
        if not self.entries[0].get():
            messagebox.showerror("Error", "Customer Ref. is required")
            return

        data = [entry.get() for entry in self.entries]
        try:
            self.cursor.execute("INSERT INTO customers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
            self.conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Customer added successfully")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Customer Ref. already exists")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add customer:\n{e}")

    def fetch_data(self):
        try:
            self.cursor.execute("SELECT * FROM customers")
            rows = self.cursor.fetchall()
            self.cust_details.delete(*self.cust_details.get_children())
            for row in rows:
                self.cust_details.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{e}")

    def get_cursor(self, event=""):
        selected_row = self.cust_details.focus()
        content = self.cust_details.item(selected_row)
        row = content["values"]
        if row:
            for entry, val in zip(self.entries, row):
                if isinstance(entry, ttk.Combobox):
                    entry.set(val)
                else:
                    entry.delete(0, END)
                    entry.insert(0, val)

    def update_customer(self):
        ref = self.entries[0].get()
        if not ref:
            messagebox.showerror("Error", "Customer Ref. required for update")
            return

        data = [entry.get() for entry in self.entries[1:]] + [ref]
        try:
            self.cursor.execute("""
                UPDATE customers SET 
                    name=%s, fname=%s, gender=%s, pincode=%s, mobile=%s, email=%s, 
                    nationality=%s, id_proof=%s, id_number=%s, address=%s 
                WHERE ref=%s
            """, data)
            self.conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Customer updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update:\n{e}")

    def delete_customer(self):
        ref = self.entries[0].get()
        if not ref:
            messagebox.showerror("Error", "Customer Ref. required for deletion")
            return

        try:
            self.cursor.execute("DELETE FROM customers WHERE ref=%s", (ref,))
            self.conn.commit()
            self.fetch_data()
            self.reset_fields()
            messagebox.showinfo("Success", "Customer deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")

    def reset_fields(self):
        for entry in self.entries:
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, END)

    def search_customer(self):
        by = self.combo_Searchby.get()
        val = self.txtsearch.get()
        if not by or not val:
            messagebox.showwarning("Input Error", "Select search criteria and enter search text")
            return

        try:
            query = f"SELECT * FROM customers WHERE {by} LIKE %s"
            self.cursor.execute(query, (f"%{val}%",))
            rows = self.cursor.fetchall()
            self.cust_details.delete(*self.cust_details.get_children())
            for row in rows:
                self.cust_details.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search:\n{e}")


if __name__ == "__main__":
    root = Tk()
    app = Cust_Win(root)
    root.mainloop()
