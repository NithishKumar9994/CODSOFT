import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip  # For copy to clipboard functionality

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🌈 Ultra Password Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.config(bg="#2b2b2b")
        
        # Custom font
        self.title_font = ("Segoe UI", 24, "bold")
        self.label_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 12, "bold")
        
        # Color scheme
        self.colors = {
            "background": "#2b2b2b",
            "primary": "#6b8cff",
            "secondary": "#4e5254",
            "accent": "#ff6b6b",
            "text": "#ffffff",
            "entry_bg": "#3c3f41",
            "checkbox_active": "#a5d6a7"
        }
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["background"])
        header_frame.pack(pady=(20, 10))
        
        tk.Label(
            header_frame,
            text="🔒 Password Generator",
            font=self.title_font,
            bg=self.colors["background"],
            fg=self.colors["primary"]
        ).pack()
        
        # Length selection
        length_frame = tk.Frame(self.root, bg=self.colors["background"])
        length_frame.pack(pady=10)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(
            length_frame,
            from_=4,
            to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=self.update_length_label,
            length=200
        )
        self.length_slider.pack(side=tk.LEFT)
        
        self.length_label = tk.Label(
            length_frame,
            textvariable=self.length_var,
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["primary"],
            width=3
        )
        self.length_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Complexity options
        options_frame = tk.Frame(self.root, bg=self.colors["background"])
        options_frame.pack(pady=20)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Uppercase Letters (A-Z)",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"],
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["checkbox_active"],
            variable=self.uppercase_var,
            onvalue=True,
            offvalue=False
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.lowercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Lowercase Letters (a-z)",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"],
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["checkbox_active"],
            variable=self.lowercase_var,
            onvalue=True,
            offvalue=False
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Digits (0-9)",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"],
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["checkbox_active"],
            variable=self.digits_var,
            onvalue=True,
            offvalue=False
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        self.symbols_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Symbols (!@#$%^&*)",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"],
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["checkbox_active"],
            variable=self.symbols_var,
            onvalue=True,
            offvalue=False
        ).grid(row=3, column=0, sticky="w", pady=5)
        
        # Generate button
        generate_button = tk.Button(
            self.root,
            text="✨ Generate Password",
            font=self.button_font,
            bg=self.colors["primary"],
            fg=self.colors["text"],
            activebackground=self.colors["primary"],
            activeforeground=self.colors["text"],
            bd=0,
            padx=20,
            pady=10,
            command=self.generate_password
        )
        generate_button.pack(pady=20)
        
        # Password display
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            self.root,
            textvariable=self.password_var,
            font=("Consolas", 14),
            bg=self.colors["entry_bg"],
            fg=self.colors["text"],
            bd=0,
            relief=tk.FLAT,
            justify=tk.CENTER,
            state='readonly',
            readonlybackground=self.colors["entry_bg"]
        )
        password_entry.pack(fill=tk.X, padx=50, pady=(0, 20))
        
        # Copy button
        copy_button = tk.Button(
            self.root,
            text="📋 Copy to Clipboard",
            font=self.button_font,
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            activebackground=self.colors["secondary"],
            activeforeground=self.colors["text"],
            bd=0,
            padx=20,
            pady=10,
            command=self.copy_to_clipboard
        )
        copy_button.pack()
        
        # Strength indicator
        self.strength_label = tk.Label(
            self.root,
            text="",
            font=self.label_font,
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.strength_label.pack(pady=(20, 0))
        
    def update_length_label(self, value):
        self.length_var.set(int(float(value)))
        
    def generate_password(self):
        # Check if at least one option is selected
        if not any([self.uppercase_var.get(), self.lowercase_var.get(), 
                   self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return
            
        length = self.length_var.get()
        characters = ""
        
        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.lowercase_var.get():
            characters += string.ascii_lowercase
        if self.digits_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        # Ensure we have enough characters to choose from
        if len(characters) < 1:
            self.password_var.set("")
            return
            
        # Generate password
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        
        # Update strength indicator
        self.update_strength_indicator(password)
        
    def update_strength_indicator(self, password):
        strength = 0
        length = len(password)
        
        # Length contributes to strength
        if length >= 12:
            strength += 2
        elif length >= 8:
            strength += 1
            
        # Character diversity
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        strength += sum([has_upper, has_lower, has_digit, has_symbol])
        
        # Set strength text and color
        if strength >= 5:
            text = "🔒 Very Strong"
            color = "#4CAF50"  # Green
        elif strength >= 3:
            text = "🔑 Strong"
            color = "#8BC34A"  # Light green
        elif strength >= 2:
            text = "⚠️ Medium"
            color = "#FFC107"  # Yellow
        else:
            text = "❌ Weak"
            color = "#F44336"  # Red
            
        self.strength_label.config(text=f"Password Strength: {text}", fg=color)
        
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()