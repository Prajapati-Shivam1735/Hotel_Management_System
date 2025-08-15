from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime

class Room_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1300x565+230+220")

        # Variables
        self.var_contact = StringVar()
        self.var_check_in = StringVar()
        self.var_check_out = StringVar()
        self.var_roomtype = StringVar()
        self.var_roomavailable = StringVar()
        self.var_meal = StringVar()
        self.var_no_of_days = StringVar()
        self.var_paidtax = StringVar()
        self.var_sobtotal = StringVar()
        self.var_total = StringVar()

        self.entries = []

        self.setup_ui()

    def connect(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="server", database="hotel_management"
        )

    def setup_ui(self):
        Label(self.root, text="ROOM BOOKING DETAILS", font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE).place(x=0, y=0, width=1300, height=55)

        self.labelframeleft = LabelFrame(self.root, text="Room Booking Details", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, padx=2)
        self.labelframeleft.place(x=0, y=55, width=420, height=505)

        Label(self.labelframeleft, text="Customer Contact", font=("arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=4, sticky=W)

        contact_frame = Frame(self.labelframeleft)
        contact_frame.grid(row=0, column=1, columnspan=2, padx=0, pady=4, sticky=W)
        ttk.Entry(contact_frame, textvariable=self.var_contact, font=("arial", 12), width=18).pack(side=LEFT, padx=(0, 5))
        Button(contact_frame, text="Fetch", command=self.fetch_contact_data, font=("arial", 10, "bold"), bg="black", fg="gold", width=8).pack(side=LEFT)

        #available Room
        # lblroomavailable=Lable(labelframeleft,font=("arial",12,"bold"),text="Available Room")
        # lblroomavailable.grid(row=4,column=0,sticky=W)

        # combo


        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT roomNo FROM details")
            rooms = [row[0] for row in cur.fetchall()]
            cur.execute("SELECT DISTINCT roomType FROM details")
            room_types = [row[0] for row in cur.fetchall()]
            conn.close()
        except:
            rooms = []
            room_types = ["Single", "Double", "Luxury"]

        fields = [
            ("Check-in Date", self.var_check_in),
            ("Check-out Date", self.var_check_out),
            ("Room Type", self.var_roomtype, room_types),
            ("Available Room", self.var_roomavailable, rooms),
            ("Meal", self.var_meal, ["Breakfast", "Lunch", "Dinner", "None"]),
            ("No. of Days", self.var_no_of_days),
            ("Paid Tax", self.var_paidtax),
            ("Sub Total", self.var_sobtotal),
            ("Total Cost", self.var_total)
        ]

        for i, (label, var, *options) in enumerate(fields, 1):
            Label(self.labelframeleft, text=label, font=("arial", 12, "bold")).grid(row=i, column=0, padx=10, pady=4, sticky=W)
            if options:
                widget = ttk.Combobox(self.labelframeleft, textvariable=var, values=options[0], state="readonly", font=("arial", 12), width=22)
            else:
                widget = ttk.Entry(self.labelframeleft, textvariable=var, font=("arial", 12), width=24)
            widget.grid(row=i, column=1, padx=10, pady=4, sticky=W)
            self.entries.append(widget)

        Button(self.labelframeleft, text="Bill", command=self.calculate_bill, font=("arial", 11, "bold"), bg="black", fg="gold").grid(row=10, column=0, padx=10, pady=5, sticky=W)

        btn_frame = Frame(self.labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=380, width=410, height=93)

        buttons = [("Add", self.add_data), ("Update", self.update_data), ("Delete", self.delete_data), ("Reset", self.reset_fields)]
        for i, (label, cmd) in enumerate(buttons):
            Button(btn_frame, text=label, command=cmd, font=("arial", 11, "bold"), bg="black", fg="gold", width=21).grid(row=i // 2, column=i % 2, padx=5, pady=5)
            # Right Image
        try:
            bed_img = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\bed.jpg")
            bed_img = bed_img.resize((470, 195), Image.Resampling.LANCZOS)
            self.photo_bed = ImageTk.PhotoImage(bed_img)
            Label(self.root, image=self.photo_bed, relief=RIDGE).place(x=820, y=60, width=470, height=195)
        except:
            pass

        tableframe = LabelFrame(self.root, text="View Details", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE)
        tableframe.place(x=430, y=250, width=860, height=310)

        Label(tableframe, text="Search By:", font=("arial", 12, "bold")).grid(row=0, column=0, padx=3, pady=5, sticky=W)
        self.combo_searchby = ttk.Combobox(tableframe, font=("arial", 12), state="readonly", width=21)
        self.combo_searchby["values"] = ("contact", "roomavailable")
        self.combo_searchby.grid(row=0, column=1, padx=3, pady=5)
        self.txt_search = ttk.Entry(tableframe, font=("arial", 12), width=21)
        self.txt_search.grid(row=0, column=2, padx=3)

        Button(tableframe, text="Search", command=self.search_data, font=("arial", 11, "bold"), bg="black", fg="gold").grid(row=0, column=3, padx=20)
        Button(tableframe, text="Show All", command=self.fetch_data, font=("arial", 11, "bold"), bg="black", fg="gold").grid(row=0, column=4)

        data_frame = Frame(tableframe, bd=2, relief=RIDGE)
        data_frame.place(x=0, y=40, width=850, height=245)

        scroll_x = Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(data_frame, orient=VERTICAL)

        self.room_details = ttk.Treeview(data_frame, columns=("contact", "check_in", "check_out", "roomtype", "roomavailable", "meal", "noOfdays", "paidtax", "subtotal", "total"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.room_details.xview)
        scroll_y.config(command=self.room_details.yview)

        for col in self.room_details["columns"]:
            self.room_details.heading(col, text=col.title())
            self.room_details.column(col, width=100)

        self.room_details.bind("<ButtonRelease-1>", self.get_cursor)
        self.room_details["show"] = "headings"
        self.room_details.pack(fill=BOTH, expand=1)
        self.fetch_data()

    def calculate_bill(self):
        try:
            in_date = datetime.strptime(self.var_check_in.get(), "%Y-%m-%d")
            out_date = datetime.strptime(self.var_check_out.get(), "%Y-%m-%d")
            days = (out_date - in_date).days or 1
            self.var_no_of_days.set(days)

            room_prices = {"single": 1000, "Double": 1500, "luxury": 2500}
            meal_prices = {"Breakfast": 200, "Lunch": 400, "Dinner": 500, "None": 0}

            room_price = room_prices.get(self.var_roomtype.get(), 1000)
            meal_price = meal_prices.get(self.var_meal.get(), 0)

            subtotal = (room_price + meal_price) * days
            tax = subtotal * 0.1
            total = subtotal + tax

            self.var_paidtax.set(f"{tax:.2f}")
            self.var_sobtotal.set(f"{subtotal:.2f}")
            self.var_total.set(f"{total:.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid date format or data: {e}")

    def add_data(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO room (contact, check_in, check_out, roomtype, roomavailable, meal, noOfdays, paidtax, subtotal, total)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.var_contact.get(), self.var_check_in.get(), self.var_check_out.get(),
                self.var_roomtype.get(), self.var_roomavailable.get(), self.var_meal.get(),
                self.var_no_of_days.get(), self.var_paidtax.get(), self.var_sobtotal.get(), self.var_total.get()
            ))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Room booked successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def get_cursor(self, event=""):
        selected_row = self.room_details.focus()
        content = self.room_details.item(selected_row)
        row = content["values"]
        if row:
            self.var_contact.set(row[0])
            for entry, val in zip(self.entries, row[1:]):
                if isinstance(entry, ttk.Combobox):
                    entry.set(val)
                else:
                    entry.delete(0, END)
                    entry.insert(0, val)

    def fetch_data(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM room")
            rows = cur.fetchall()
            self.room_details.delete(*self.room_details.get_children())
            for row in rows:
                self.room_details.insert("", END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def search_data(self):
        search_by = self.combo_searchby.get()
        search_text = self.txt_search.get()

        if not search_by or not search_text:
            messagebox.showerror("Error", "Please select a search field and enter a value.")
            return

        try:
            conn = self.connect()
            cur = conn.cursor()
            query = f"SELECT * FROM room WHERE {search_by} LIKE %s"
            cur.execute(query, (f"%{search_text}%",))
            rows = cur.fetchall()
            conn.close()

            self.room_details.delete(*self.room_details.get_children())
            for row in rows:
                self.room_details.insert("", END, values=row)

            if not rows:
                messagebox.showinfo("No Results", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def update_data(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("""
                UPDATE room SET check_in=%s, check_out=%s, roomtype=%s, roomavailable=%s,
                meal=%s, noOfdays=%s, paidtax=%s, subtotal=%s, total=%s WHERE contact=%s
            """, (
                self.var_check_in.get(), self.var_check_out.get(), self.var_roomtype.get(),
                self.var_roomavailable.get(), self.var_meal.get(), self.var_no_of_days.get(),
                self.var_paidtax.get(), self.var_sobtotal.get(), self.var_total.get(), self.var_contact.get()
            ))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Record updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def delete_data(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM room WHERE contact=%s", (self.var_contact.get(),))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Deleted", "Record deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def reset_fields(self):
        for var in [self.var_contact, self.var_check_in, self.var_check_out, self.var_roomtype,
                    self.var_roomavailable, self.var_meal, self.var_no_of_days,
                    self.var_paidtax, self.var_sobtotal, self.var_total]:
            var.set("")

    def fetch_contact_data(self):
        contact = self.var_contact.get()
        if not contact:
            messagebox.showerror("Error", "Enter a contact number")
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT name, gender, email, nationality, address FROM customers WHERE mobile=%s", (contact,))
            data = cur.fetchone()
            conn.close()

            if data:
                show_frame = Frame(self.root, bd=4, relief=RIDGE, padx=2)
                show_frame.place(x=455, y=60, width=320, height=180)
                labels = ['Name', 'Gender', 'Email', 'Nationality', 'Address']
                for i, value in enumerate(data):
                    Label(show_frame, text=f"{labels[i]}:", font=("arial", 12, "bold")).place(x=0, y=i * 30)
                    Label(show_frame, text=value, font=("arial", 12)).place(x=100, y=i * 30)
            else:
                messagebox.showinfo("No Data", "No customer found with that contact.")
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")


if __name__ == "__main__":
    root = Tk()
    app = Room_Win(root)
    root.mainloop()
