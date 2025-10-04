
print("Program started")
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# Add contact
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if not name or not phone or not email:
        messagebox.showwarning("Missing Fields", "Please fill out all fields.")
        return

    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts()
    refresh_list()
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Refresh listbox
def refresh_list():
    listbox.delete(0, tk.END)
    for idx, contact in enumerate(contacts):
        listbox.insert(tk.END, f"{idx+1}. {contact['name']} - {contact['phone']} - {contact['email']}")

# Delete contact
def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to delete.")
        return

    index = selected[0]
    del contacts[index]
    save_contacts()
    refresh_list()

# Edit contact
def edit_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to edit.")
        return

    index = selected[0]
    contact = contacts[index]

    new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact["name"])
    new_phone = simpledialog.askstring("Edit Phone", "Enter new phone:", initialvalue=contact["phone"])
    new_email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact["email"])

    if new_name and new_phone and new_email:
        contacts[index] = {"name": new_name.strip(), "phone": new_phone.strip(), "email": new_email.strip()}
        save_contacts()
        refresh_list()

# ---------------- GUI ----------------

contacts = load_contacts()

root = tk.Tk()
root.title("📇 Contact Manager")
root.geometry("600x400")
root.resizable(False, False)

# Entry fields
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame_form, width=25)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Phone").grid(row=1, column=0)
entry_phone = tk.Entry(frame_form, width=25)
entry_phone.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Email").grid(row=2, column=0)
entry_email = tk.Entry(frame_form, width=25)
entry_email.grid(row=2, column=1, padx=5)

tk.Button(frame_form, text="Add Contact", command=add_contact, width=20).grid(row=3, column=0, columnspan=2, pady=10)

# Contact list
listbox = tk.Listbox(root, width=80, height=10)
listbox.pack()

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Edit Contact", command=edit_contact, width=20).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Delete Contact", command=delete_contact, width=20).grid(row=0, column=1, padx=10)

refresh_list()

root.mainloop()