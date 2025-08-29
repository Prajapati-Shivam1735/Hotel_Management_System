import tkinter as tk
from tkinter import ttk, messagebox
import db

def fetch_customers():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        tree.insert("", "end", values=(row[1], row[2], row[3]))

def add_customer():
    if entry_name.get() == "":
        messagebox.showerror("Error", "Name required")
        return
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
        (entry_name.get(), entry_phone.get(), entry_email.get())
    )
    conn.commit()
    fetch_customers()
    clear_entries()

def update_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a customer")
        return
    name, phone, email = entry_name.get(), entry_phone.get(), entry_email.get()
    cid = get_customer_id(selected[0])
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name=%s, phone=%s, email=%s WHERE id=%s",
        (name, phone, email, cid)
    )
    conn.commit()
    fetch_customers()

def delete_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a customer")
        return
    cid = get_customer_id(selected[0])
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=%s", (cid,))
    conn.commit()
    fetch_customers()

def get_customer_id(item):
    """Retrieve customer ID based on name/phone/email triple."""
    values = tree.item(item, "values")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE name=%s AND phone=%s AND email=%s",(values[0], values[1], values[2]))
    result = cursor.fetchone()
    return result[0] if result else None

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def on_tree_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[0])
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, values[1])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, values[2])

conn = db.get_connection()

root = tk.Tk()
root.title("Customers Management")
root.geometry("600x400")

# Input fields
tk.Label(root, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(root); entry_name.grid(row=0, column=1)
tk.Label(root, text="Phone").grid(row=1, column=0)
entry_phone = tk.Entry(root); entry_phone.grid(row=1, column=1)
tk.Label(root, text="Email").grid(row=2, column=0)
entry_email = tk.Entry(root); entry_email.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add", command=add_customer).grid(row=3, column=0)
tk.Button(root, text="Update", command=update_customer).grid(row=3, column=1)
tk.Button(root, text="Delete", command=delete_customer).grid(row=3, column=2)
tk.Button(root, text="Clear", command=clear_entries).grid(row=3, column=3)

# Table for customers
columns = ("Name", "Phone", "Email")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=4, column=0, columnspan=3, pady=10)

tree.bind("<<TreeviewSelect>>", on_tree_select)

fetch_customers()
root.mainloop()
conn.close()
