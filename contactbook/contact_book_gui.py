import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILENAME = "contacts.json"
contacts = []

def load_contacts():
    global contacts
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            try:
                contacts = json.load(f)
            except json.JSONDecodeError:
                contacts = []

def save_contacts():
    with open(FILENAME, "w") as f:
        json.dump(contacts, f, indent=2)

def refresh_listbox():
    listbox.delete(0, tk.END)
    for contact in contacts:
        listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showerror("Missing Info", "Name and phone are required.")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })
    save_contacts()
    refresh_listbox()
    clear_fields()

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def on_select(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        contact = contacts[index]
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        name_entry.insert(0, contact["name"])
        phone_entry.insert(0, contact["phone"])
        email_entry.insert(0, contact["email"])
        address_entry.insert(0, contact["address"])

def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("No Selection", "Select a contact to update.")
        return
    index = selected[0]
    contacts[index] = {
        "name": name_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "address": address_entry.get()
    }
    save_contacts()
    refresh_listbox()
    clear_fields()

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("No Selection", "Select a contact to delete.")
        return
    index = selected[0]
    if messagebox.askyesno("Delete", f"Delete contact {contacts[index]['name']}?"):
        contacts.pop(index)
        save_contacts()
        refresh_listbox()
        clear_fields()

def search_contact():
    query = search_entry.get().lower()
    listbox.delete(0, tk.END)
    for contact in contacts:
        if query in contact["name"].lower() or query in contact["phone"]:
            listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

# GUI Setup
root = tk.Tk()
root.title("Contact Book")

# Form
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Phone").grid(row=1, column=0)
tk.Label(root, text="Email").grid(row=2, column=0)
tk.Label(root, text="Address").grid(row=3, column=0)

name_entry = tk.Entry(root, width=30)
phone_entry = tk.Entry(root, width=30)
email_entry = tk.Entry(root, width=30)
address_entry = tk.Entry(root, width=30)

name_entry.grid(row=0, column=1, padx=10, pady=5)
phone_entry.grid(row=1, column=1, padx=10, pady=5)
email_entry.grid(row=2, column=1, padx=10, pady=5)
address_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Contact", command=add_contact).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update Contact", command=update_contact).grid(row=4, column=1)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=5, column=0)
tk.Button(root, text="Clear Fields", command=clear_fields).grid(row=5, column=1)

# Search
tk.Label(root, text="Search:").grid(row=6, column=0)
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1, pady=5)
tk.Button(root, text="Search", command=search_contact).grid(row=6, column=2, padx=5)

# Contact List
listbox = tk.Listbox(root, width=60, height=10)
listbox.grid(row=7, column=0, columnspan=3, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

# Load existing contacts
load_contacts()
refresh_listbox()

root.mainloop()
