from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class DetailsRoom:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1300x565+230+220")

        # Variables
        self.var_floor = StringVar()
        self.var_roomNo = StringVar()
        self.var_roomType = StringVar()

        # Database connection
        self.conn = mysql.connector.connect(host="localhost", user="root", password="server", database="hotel_management")
        self.cursor = self.conn.cursor()

        # Title
        Label(self.root, text="Room Adding", font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE).place(x=0, y=0, width=1300, height=55)

        # Logo
        img = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\logohotel.png")
        img = img.resize((100, 53), Image.Resampling.LANCZOS)
        self.photo_logo = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photo_logo, relief=RIDGE).place(x=0, y=0, width=100, height=55)

        # Form Frame
        self.labelframeleft = LabelFrame(self.root, text="New Rooms Add", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, padx=2)
        self.labelframeleft.place(x=5, y=55, width=600, height=305)

        # Floor
        Label(self.labelframeleft, text="Floor", font=("arial", 12, "bold")).grid(row=0, column=0, padx=2, pady=6)
        ttk.Entry(self.labelframeleft, textvariable=self.var_floor, width=20, font=("arial", 12, "bold")).grid(row=0, column=1, sticky=W)

        # Room No
        Label(self.labelframeleft, text="Room No.", font=("arial", 12, "bold")).grid(row=1, column=0, padx=2, pady=6)
        ttk.Entry(self.labelframeleft, textvariable=self.var_roomNo, width=20, font=("arial", 12, "bold")).grid(row=1, column=1, sticky=W)

        # Room Type
        Label(self.labelframeleft, text="Room Type", font=("arial", 12, "bold")).grid(row=2, column=0, padx=2, pady=6)
        ttk.Entry(self.labelframeleft, textvariable=self.var_roomType, width=20, font=("arial", 12, "bold")).grid(row=2, column=1, sticky=W)

        # Button Frame
        btn_frame = Frame(self.labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=360, y=120, width=205, height=150)

        Button(btn_frame, text="Add", command=self.add_room, font=("arial", 11, "bold"), bg="black", fg="gold", width=21).grid(row=0, column=0, padx=2, pady=2)
        Button(btn_frame, text="Update", command=self.update_room, font=("arial", 11, "bold"), bg="black", fg="gold", width=21).grid(row=1, column=0, padx=2, pady=2)
        Button(btn_frame, text="Delete", command=self.delete_room, font=("arial", 11, "bold"), bg="black", fg="gold", width=21).grid(row=2, column=0, padx=2, pady=2)
        Button(btn_frame, text="Reset", command=self.reset_form, font=("arial", 11, "bold"), bg="black", fg="gold", width=21).grid(row=3, column=0, padx=2, pady=2)

        # Table Frame
        tableframe = LabelFrame(self.root, text="View Details", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE)
        tableframe.place(x=670, y=55, width=600, height=305)

        data_frame = Frame(tableframe, bd=2, relief=RIDGE)
        data_frame.place(x=2, y=5, width=590, height=275)

        scroll_x = Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(data_frame, orient=VERTICAL)

        self.room_details = ttk.Treeview(data_frame, columns=("Floor", "Room No.", "Room Type"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.room_details.xview)
        scroll_y.config(command=self.room_details.yview)

        for col in self.room_details["columns"]:
            self.room_details.heading(col, text=col)
            self.room_details.column(col, width=100)

        self.room_details["show"] = "headings"
        self.room_details.pack(fill=BOTH, expand=1)
        self.room_details.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def add_room(self):
        if self.var_floor.get() == "" or self.var_roomNo.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            self.cursor.execute("INSERT INTO details (floor, roomNo, roomtype) VALUES (%s, %s, %s)", (
                self.var_floor.get(),
                self.var_roomNo.get(),
                self.var_roomType.get()
            ))
            self.conn.commit()
            self.fetch_data()
            self.reset_form()
            messagebox.showinfo("Success", "Room added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding room:\n{e}")

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM details")
        rows = self.cursor.fetchall()
        self.room_details.delete(*self.room_details.get_children())
        for row in rows:
            self.room_details.insert("", END, values=row)

    def get_cursor(self, event):
        selected = self.room_details.focus()
        data = self.room_details.item(selected)["values"]
        if data:
            self.var_floor.set(data[0])
            self.var_roomNo.set(data[1])
            self.var_roomType.set(data[2])

    def update_room(self):
        try:
            self.cursor.execute("UPDATE details SET floor=%s, roomType=%s WHERE roomNo=%s", (
                self.var_floor.get(),
                self.var_roomType.get(),
                self.var_roomNo.get()
            ))
            self.conn.commit()
            self.fetch_data()
            self.reset_form()
            messagebox.showinfo("Success", "Room updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating room:\n{e}")

    def delete_room(self):
        try:
            self.cursor.execute("DELETE FROM details WHERE roomNo=%s", (self.var_roomNo.get(),))
            self.conn.commit()
            self.fetch_data()
            self.reset_form()
            messagebox.showinfo("Deleted", "Room deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting room:\n{e}")

    def reset_form(self):
        self.var_floor.set("")
        self.var_roomNo.set("")
        self.var_roomType.set("")

if __name__ == "__main__":
    root = Tk()
    app = DetailsRoom(root)
    root.mainloop()
