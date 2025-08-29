# main.py
import tkinter as tk
import subprocess
import sys
import os

# Adjust these to match file names in same folder
CUSTOMERS_SCRIPT = "customers_window.py"
ROOMS_SCRIPT = "rooms_window.py"
BOOKINGS_SCRIPT = "bookings_window.py"

def run_script(script_name):
    # Launch a separate process for the selected module
    # Uses the same Python interpreter as running this script
    cwd = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable, os.path.join(cwd, script_name)], cwd=cwd)

def open_customers():
    run_script(CUSTOMERS_SCRIPT)

def open_rooms():
    run_script(ROOMS_SCRIPT)

def open_bookings():
    run_script(BOOKINGS_SCRIPT)

root = tk.Tk()
root.title("Hotel Management - Main Menu")
root.geometry("320x200")

tk.Label(root, text="Hotel Management System", font=("Arial", 14)).pack(pady=12)
tk.Button(root, text="Customers", width=22, command=open_customers).pack(pady=6)
tk.Button(root, text="Rooms", width=22, command=open_rooms).pack(pady=6)
tk.Button(root, text="Bookings", width=22, command=open_bookings).pack(pady=6)

root.mainloop()
