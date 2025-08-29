# rooms_window.py
import tkinter as tk
from tkinter import messagebox, END
import db

def fetch_rooms():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, room_number, room_type, price, status FROM rooms ORDER BY id")
        rows = cursor.fetchall()
        listbox.delete(0, END)
        for r in rows:
            listbox.insert(END, r)
        cursor.close()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def add_room():
    number = entry_number.get().strip()
    rtype = entry_type.get().strip()
    price = entry_price.get().strip() or "0.00"
    if not number:
        messagebox.showerror("Validation", "Room number is required")
        return
    try:
        p = float(price)
    except ValueError:
        messagebox.showerror("Validation", "Price must be a number")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rooms (room_number, room_type, price) VALUES (%s, %s, %s)",
                       (number, rtype, p))
        conn.commit()
        cursor.close()
        fetch_rooms()
        clear_entries()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def update_room():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Please select a room to update")
        return
    rid = listbox.get(sel[0])[0]
    number = entry_number.get().strip()
    rtype = entry_type.get().strip()
    price = entry_price.get().strip() or "0.00"
    try:
        p = float(price)
    except ValueError:
        messagebox.showerror("Validation", "Price must be a number")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET room_number=%s, room_type=%s, price=%s WHERE id=%s",
                       (number, rtype, p, rid))
        conn.commit()
        cursor.close()
        fetch_rooms()
        clear_entries()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def delete_room():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Please select a room to delete")
        return
    rid = listbox.get(sel[0])[0]
    if not messagebox.askyesno("Confirm", "Delete selected room? This will remove related bookings."):
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rooms WHERE id=%s", (rid,))
        conn.commit()
        cursor.close()
        fetch_rooms()
        clear_entries()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def on_select(evt):
    sel = listbox.curselection()
    if not sel:
        return
    row = listbox.get(sel[0])
    entry_number.delete(0, END); entry_number.insert(0, row[1])
    entry_type.delete(0, END); entry_type.insert(0, row[2] or "")
    entry_price.delete(0, END); entry_price.insert(0, str(row[3] or 0.0))

def clear_entries():
    entry_number.delete(0, END)
    entry_type.delete(0, END)
    entry_price.delete(0, END)

try:
    conn = db.get_connection()
except Exception as e:
    tk.messagebox.showerror("DB Error", f"Unable to connect to DB: {e}")
    raise SystemExit(1)

root = tk.Tk()
root.title("Rooms Management - Separate Window")
root.geometry("640x420")

frm = tk.Frame(root, padx=8, pady=8)
frm.pack(fill="both", expand=True)

tk.Label(frm, text="Rooms", font=("Arial", 14)).grid(row=0, column=0, columnspan=4, pady=(0,8))

tk.Label(frm, text="Room Number").grid(row=1, column=0, sticky="e")
entry_number = tk.Entry(frm, width=25); entry_number.grid(row=1, column=1, padx=4, pady=2)

tk.Label(frm, text="Type").grid(row=2, column=0, sticky="e")
entry_type = tk.Entry(frm, width=25); entry_type.grid(row=2, column=1, padx=4, pady=2)

tk.Label(frm, text="Price").grid(row=3, column=0, sticky="e")
entry_price = tk.Entry(frm, width=25); entry_price.grid(row=3, column=1, padx=4, pady=2)

tk.Button(frm, text="Add", width=12, command=add_room).grid(row=4, column=0, pady=8)
tk.Button(frm, text="Update", width=12, command=update_room).grid(row=4, column=1)
tk.Button(frm, text="Delete", width=12, command=delete_room).grid(row=4, column=2)
tk.Button(frm, text="Clear", width=12, command=clear_entries).grid(row=4, column=3)

listbox = tk.Listbox(frm, width=90, height=15)
listbox.grid(row=5, column=0, columnspan=4, pady=(6,0))
listbox.bind("<<ListboxSelect>>", on_select)

fetch_rooms()
root.mainloop()

conn.close()
