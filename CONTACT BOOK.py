import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Contact Book")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")

        # Create data file if it doesn't exist
        self.data_file = "contacts.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

        # Load contacts
        self.contacts = self.load_contacts()

        # Create GUI elements
        self.create_widgets()

        # Display contacts
        self.display_contacts()

    def load_contacts(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_contacts(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = tk.Label(
            main_frame,
            text="My Colorful Contact Book",
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
            fg="#ff6b6b"
        )
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Search frame
        search_frame = tk.Frame(main_frame, bg="#f0f8ff")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333",
            relief=tk.GROOVE,
            bd=2
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            command=self.search_contact,
            bg="#4ecdc4",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        search_btn.pack(side=tk.LEFT)

        clear_search_btn = tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bg="#ff9e7d",
            fg="white",
            font=("Arial", 12),
            relief=tk.RAISED,
            bd=2
        )
        clear_search_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Contacts list
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Name", "Phone"),
            show="headings",
            selectmode="browse"
        )
        self.tree.grid(row=2, column=0, sticky="nsew", pady=(0, 10))

        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#ffffff",
                        fieldbackground="#ffffff",
                        foreground="#333333",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#ff6b6b",
                        foreground="white",
                        font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", "#4ecdc4")])

        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.column("Name", width=200)
        self.tree.column("Phone", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f8ff")
        button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # Buttons
        add_btn = tk.Button(
            button_frame,
            text="➕ Add Contact",
            command=self.add_contact_window,
            bg="#6aecd2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        add_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        view_btn = tk.Button(
            button_frame,
            text="👁️ View Details",
            command=self.view_contact,
            bg="#ffb347",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        view_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        update_btn = tk.Button(
            button_frame,
            text="✏️ Update",
            command=self.update_contact_window,
            bg="#ffcc5c",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        update_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete",
            command=self.delete_contact,
            bg="#ff6f69",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        delete_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Configure grid weights
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def display_contacts(self, contacts=None):
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display all contacts or filtered contacts
        contacts_to_display = contacts if contacts is not None else self.contacts

        for contact in contacts_to_display:
            self.tree.insert("", tk.END, values=(contact["name"], contact["phone"]))

    def search_contact(self):
        query = self.search_var.get().lower()
        if not query:
            self.display_contacts()
            return

        results = [
            contact for contact in self.contacts
            if query in contact["name"].lower() or query in contact["phone"]
        ]

        self.display_contacts(results)

    def clear_search(self):
        self.search_var.set("")
        self.display_contacts()

    def add_contact_window(self):
        self.contact_form("Add New Contact", self.save_new_contact)

    def update_contact_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to update.")
            return

        # Get the selected contact details
        item = self.tree.item(selected[0])
        name = item["values"][0]

        # Find the full contact details
        contact = next((c for c in self.contacts if c["name"] == name), None)
        if contact:
            self.contact_form("Update Contact", self.save_updated_contact, contact)

    def contact_form(self, title, save_command, contact=None):
        # Create a new window
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x400")
        form_window.configure(bg="#e6f3ff")
        form_window.grab_set()  # Make it modal

        # Form fields
        tk.Label(
            form_window,
            text=title,
            font=("Arial", 16, "bold"),
            bg="#e6f3ff",
            fg="#2d5985"
        ).pack(pady=10)

        fields_frame = tk.Frame(form_window, bg="#e6f3ff")
        fields_frame.pack(pady=10)

        # Name
        tk.Label(
            fields_frame,
            text="Name:",
            bg="#e6f3ff",
            fg="#333333",
            font=("Arial", 12)
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry = tk.Entry(
            fields_frame,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333"
        )
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Phone
        tk.Label(
            fields_frame,
            text="Phone:",
            bg="#e6f3ff",
            fg="#333333",
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        phone_entry = tk.Entry(
            fields_frame,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333"
        )
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        # Email
        tk.Label(
            fields_frame,
            text="Email:",
            bg="#e6f3ff",
            fg="#333333",
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        email_entry = tk.Entry(
            fields_frame,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333"
        )
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Address
        tk.Label(
            fields_frame,
            text="Address:",
            bg="#e6f3ff",
            fg="#333333",
            font=("Arial", 12)
        ).grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        address_text = tk.Text(
            fields_frame,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333",
            height=4,
            width=25
        )
        address_text.grid(row=3, column=1, padx=5, pady=5)

        # If updating, populate fields
        if contact:
            name_entry.insert(0, contact["name"])
            phone_entry.insert(0, contact["phone"])
            email_entry.insert(0, contact.get("email", ""))
            address_text.insert("1.0", contact.get("address", ""))

        # Button frame
        button_frame = tk.Frame(form_window, bg="#e6f3ff")
        button_frame.pack(pady=10)

        # Save button
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=lambda: save_command(
                name_entry.get(),
                phone_entry.get(),
                email_entry.get(),
                address_text.get("1.0", tk.END).strip(),
                form_window
            ),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        save_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=form_window.destroy,
            bg="#f44336",
            fg="white",
            font=("Arial", 12),
            relief=tk.RAISED,
            bd=2
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def save_new_contact(self, name, phone, email, address, window):
        if not name or not phone:
            messagebox.showerror("Error", "Name and phone are required fields.")
            return

        new_contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        self.contacts.append(new_contact)
        self.save_contacts()
        self.display_contacts()
        window.destroy()
        messagebox.showinfo("Success", "Contact added successfully!")

    def save_updated_contact(self, name, phone, email, address, window):
        if not name or not phone:
            messagebox.showerror("Error", "Name and phone are required fields.")
            return

        # Find the contact to update
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No contact selected.")
            return

        item = self.tree.item(selected[0])
        old_name = item["values"][0]

        # Find the contact in the list
        for contact in self.contacts:
            if contact["name"] == old_name:
                contact["name"] = name
                contact["phone"] = phone
                contact["email"] = email
                contact["address"] = address
                break

        self.save_contacts()
        self.display_contacts()
        window.destroy()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def view_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view.")
            return

        # Get the selected contact details
        item = self.tree.item(selected[0])
        name = item["values"][0]

        # Find the full contact details
        contact = next((c for c in self.contacts if c["name"] == name), None)
        if contact:
            # Create a details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Contact Details - {name}")
            details_window.geometry("400x300")
            details_window.configure(bg="#e6f3ff")

            # Header
            tk.Label(
                details_window,
                text=f"Contact Details",
                font=("Arial", 16, "bold"),
                bg="#e6f3ff",
                fg="#2d5985"
            ).pack(pady=10)

            # Details frame
            details_frame = tk.Frame(details_window, bg="#e6f3ff")
            details_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

            # Name
            tk.Label(
                details_frame,
                text=f"Name: {contact['name']}",
                bg="#e6f3ff",
                fg="#333333",
                font=("Arial", 12),
                anchor="w"
            ).pack(fill=tk.X, pady=5)

            # Phone
            tk.Label(
                details_frame,
                text=f"Phone: {contact['phone']}",
                bg="#e6f3ff",
                fg="#333333",
                font=("Arial", 12),
                anchor="w"
            ).pack(fill=tk.X, pady=5)

            # Email
            tk.Label(
                details_frame,
                text=f"Email: {contact.get('email', 'N/A')}",
                bg="#e6f3ff",
                fg="#333333",
                font=("Arial", 12),
                anchor="w"
            ).pack(fill=tk.X, pady=5)

            # Address
            address_label = tk.Label(
                details_frame,
                text=f"Address:\n{contact.get('address', 'N/A')}",
                bg="#e6f3ff",
                fg="#333333",
                font=("Arial", 12),
                justify=tk.LEFT,
                anchor="nw",
                wraplength=350
            )
            address_label.pack(fill=tk.BOTH, expand=True, pady=5)

            # Close button
            close_btn = tk.Button(
                details_window,
                text="Close",
                command=details_window.destroy,
                bg="#2d5985",
                fg="white",
                font=("Arial", 12),
                relief=tk.RAISED,
                bd=2
            )
            close_btn.pack(pady=10)

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        # Get the selected contact name
        item = self.tree.item(selected[0])
        name = item["values"][0]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            # Remove from contacts list
            self.contacts = [c for c in self.contacts if c["name"] != name]

            # Save and refresh
            self.save_contacts()
            self.display_contacts()
            messagebox.showinfo("Success", "Contact deleted successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()