# bookings_window.py
import tkinter as tk
from tkinter import messagebox, END
import db
from datetime import datetime

def fetch_bookings():
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, c.name, r.room_number, b.check_in, b.check_out
            FROM bookings b
            JOIN customers c ON b.customer_id = c.id
            JOIN rooms r ON b.room_id = r.id
            ORDER BY b.id
        """)
        rows = cursor.fetchall()
        listbox.delete(0, END)
        for r in rows:
            listbox.insert(END, r)
        cursor.close()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def add_booking():
    cust_id = entry_customer.get().strip()
    room_id = entry_room.get().strip()
    checkin = entry_checkin.get().strip()
    checkout = entry_checkout.get().strip()

    # Basic validation
    if not (cust_id and room_id and checkin and checkout):
        messagebox.showerror("Validation", "All fields are required")
        return
    try:
        # Validate date format
        ci = datetime.strptime(checkin, "%Y-%m-%d").date()
        co = datetime.strptime(checkout, "%Y-%m-%d").date()
        if co <= ci:
            messagebox.showerror("Validation", "Check-out must be after check-in")
            return
    except ValueError:
        messagebox.showerror("Validation", "Dates must be in YYYY-MM-DD format")
        return

    try:
        # Use a transaction to insert booking and mark room as Booked atomically
        cursor = conn.cursor()
        conn.start_transaction()
        # Check that room exists and is Available
        cursor.execute("SELECT status FROM rooms WHERE id=%s FOR UPDATE", (room_id,))
        row = cursor.fetchone()
        if row is None:
            conn.rollback()
            messagebox.showerror("Error", "Room not found")
            return
        if row[0] == "Booked":
            conn.rollback()
            messagebox.showerror("Error", "Room is already booked")
            return

        # Insert booking
        cursor.execute("INSERT INTO bookings (customer_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)",
                       (cust_id, room_id, checkin, checkout))
        # Mark room booked
        cursor.execute("UPDATE rooms SET status='Booked' WHERE id=%s", (room_id,))
        conn.commit()
        cursor.close()
        fetch_bookings()
        clear_entries()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        messagebox.showerror("DB Error", str(e))

def delete_booking():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Please select a booking to delete")
        return
    bid = listbox.get(sel[0])[0]
    if not messagebox.askyesno("Confirm", "Delete selected booking (this will free the room)?"):
        return
    try:
        cursor = conn.cursor()
        # Find room_id for booking
        cursor.execute("SELECT room_id FROM bookings WHERE id=%s", (bid,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Error", "Booking not found")
            return
        room_id = row[0]
        conn.start_transaction()
        cursor.execute("DELETE FROM bookings WHERE id=%s", (bid,))
        cursor.execute("UPDATE rooms SET status='Available' WHERE id=%s", (room_id,))
        conn.commit()
        cursor.close()
        fetch_bookings()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        messagebox.showerror("DB Error", str(e))

def on_select(evt):
    sel = listbox.curselection()
    if not sel:
        return
    row = listbox.get(sel[0])
    # row is (id, customer_name, room_number, check_in, check_out)
    # we only display selection info, but editing uses IDs entered manually
    # (we recommend enhancing to select from dropdowns)
    entry_customer.delete(0, END)
    entry_room.delete(0, END)
    entry_checkin.delete(0, END)
    entry_checkout.delete(0, END)
    # Can't map back IDs from displayed row; this UI uses manual entry of IDs
    # Consider enhancing: load customers/rooms into comboboxes.

def clear_entries():
    entry_customer.delete(0, END)
    entry_room.delete(0, END)
    entry_checkin.delete(0, END)
    entry_checkout.delete(0, END)

# DB connect
try:
    conn = db.get_connection()
except Exception as e:
    tk.messagebox.showerror("DB Error", f"Unable to connect to DB: {e}")
    raise SystemExit(1)

root = tk.Tk()
root.title("Bookings Management - Separate Window")
root.geometry("700x460")

frm = tk.Frame(root, padx=8, pady=8)
frm.pack(fill="both", expand=True)

tk.Label(frm, text="Bookings", font=("Arial", 14)).grid(row=0, column=0, columnspan=4, pady=(0,8))

tk.Label(frm, text="Customer ID").grid(row=1, column=0, sticky="e")
entry_customer = tk.Entry(frm, width=20); entry_customer.grid(row=1, column=1, padx=4, pady=2)

tk.Label(frm, text="Room ID").grid(row=2, column=0, sticky="e")
entry_room = tk.Entry(frm, width=20); entry_room.grid(row=2, column=1, padx=4, pady=2)

tk.Label(frm, text="Check-in (YYYY-MM-DD)").grid(row=3, column=0, sticky="e")
entry_checkin = tk.Entry(frm, width=20); entry_checkin.grid(row=3, column=1, padx=4, pady=2)

tk.Label(frm, text="Check-out (YYYY-MM-DD)").grid(row=4, column=0, sticky="e")
entry_checkout = tk.Entry(frm, width=20); entry_checkout.grid(row=4, column=1, padx=4, pady=2)

tk.Button(frm, text="Add Booking", width=14, command=add_booking).grid(row=5, column=0, pady=8)
tk.Button(frm, text="Delete Booking", width=14, command=delete_booking).grid(row=5, column=1)
tk.Button(frm, text="Clear", width=14, command=clear_entries).grid(row=5, column=2)

listbox = tk.Listbox(frm, width=100, height=16)
listbox.grid(row=6, column=0, columnspan=4, pady=(6,0))
listbox.bind("<<ListboxSelect>>", on_select)

fetch_bookings()
root.mainloop()

conn.close()
