import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#2C3E50")
        
        # Variables
        self.current_input = ""
        self.total = 0
        self.operation = ""
        self.reset_input = False
        self.memory = 0
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#34495E", bd=5)
        display_frame.pack(pady=(20, 10), padx=20, fill=tk.BOTH, expand=True)
        
        # Display label
        self.display = tk.Label(
            display_frame, 
            text="0", 
            font=("Arial", 36), 
            bg="#34495E", 
            fg="#ECF0F1", 
            anchor=tk.E,
            padx=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("7", "8", "9", "/", "√"),
            ("4", "5", "6", "*", "x²"),
            ("1", "2", "3", "-", "1/x"),
            ("0", ".", "±", "+", "=")
        ]
        
        # Button colors
        button_colors = {
            "MC": "#3498DB", "MR": "#3498DB", "M+": "#3498DB", "M-": "#3498DB", "C": "#E74C3C",
            "7": "#95A5A6", "8": "#95A5A6", "9": "#95A5A6", "/": "#F39C12", "√": "#F39C12",
            "4": "#95A5A6", "5": "#95A5A6", "6": "#95A5A6", "*": "#F39C12", "x²": "#F39C12",
            "1": "#95A5A6", "2": "#95A5A6", "3": "#95A5A6", "-": "#F39C12", "1/x": "#F39C12",
            "0": "#95A5A6", ".": "#95A5A6", "±": "#95A5A6", "+": "#F39C12", "=": "#2ECC71"
        }
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    button_frame,
                    text=button_text,
                    font=("Arial", 18, "bold"),
                    bg=button_colors[button_text],
                    fg="#2C3E50" if button_text in "0123456789." else "#ECF0F1",
                    bd=0,
                    highlightthickness=0,
                    command=lambda text=button_text: self.on_button_click(text)
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky=tk.NSEW)
                button_frame.grid_columnconfigure(j, weight=1)
                button_frame.grid_rowconfigure(i, weight=1)
                
    def on_button_click(self, button_text):
        if button_text in "0123456789":
            self.handle_number(button_text)
        elif button_text == ".":
            self.handle_decimal()
        elif button_text == "±":
            self.handle_negate()
        elif button_text in "+-*/":
            self.handle_operation(button_text)
        elif button_text == "=":
            self.handle_equals()
        elif button_text == "C":
            self.handle_clear()
        elif button_text == "√":
            self.handle_square_root()
        elif button_text == "x²":
            self.handle_square()
        elif button_text == "1/x":
            self.handle_reciprocal()
        elif button_text in ["MC", "MR", "M+", "M-"]:
            self.handle_memory(button_text)
            
    def handle_number(self, number):
        if self.reset_input:
            self.current_input = ""
            self.reset_input = False
        if self.current_input == "0":
            self.current_input = number
        else:
            self.current_input += number
        self.update_display()
        
    def handle_decimal(self):
        if self.reset_input:
            self.current_input = "0"
            self.reset_input = False
        if "." not in self.current_input:
            self.current_input += "."
            self.update_display()
            
    def handle_negate(self):
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display()
            
    def handle_operation(self, op):
        if self.current_input:
            self.perform_calculation()
            self.operation = op
            self.reset_input = True
            
    def handle_equals(self):
        if self.current_input and self.operation:
            self.perform_calculation()
            self.operation = ""
            
    def handle_clear(self):
        self.current_input = ""
        self.total = 0
        self.operation = ""
        self.reset_input = False
        self.update_display("0")
        
    def handle_square_root(self):
        try:
            value = float(self.current_input if self.current_input else "0")
            if value < 0:
                messagebox.showerror("Error", "Cannot calculate square root of negative number")
                return
            self.current_input = str(math.sqrt(value))
            self.reset_input = True
            self.update_display()
        except:
            messagebox.showerror("Error", "Invalid input")
            
    def handle_square(self):
        try:
            value = float(self.current_input if self.current_input else "0")
            self.current_input = str(value ** 2)
            self.reset_input = True
            self.update_display()
        except:
            messagebox.showerror("Error", "Invalid input")
            
    def handle_reciprocal(self):
        try:
            value = float(self.current_input if self.current_input else "0")
            if value == 0:
                messagebox.showerror("Error", "Cannot divide by zero")
                return
            self.current_input = str(1 / value)
            self.reset_input = True
            self.update_display()
        except:
            messagebox.showerror("Error", "Invalid input")
            
    def handle_memory(self, mem_op):
        try:
            current_value = float(self.current_input if self.current_input else "0")
            
            if mem_op == "MC":
                self.memory = 0
            elif mem_op == "MR":
                self.current_input = str(self.memory)
                self.reset_input = True
                self.update_display()
            elif mem_op == "M+":
                self.memory += current_value
            elif mem_op == "M-":
                self.memory -= current_value
        except:
            messagebox.showerror("Error", "Invalid memory operation")
            
    def perform_calculation(self):
        try:
            input_value = float(self.current_input if self.current_input else "0")
            
            if self.operation == "+":
                self.total += input_value
            elif self.operation == "-":
                self.total -= input_value
            elif self.operation == "*":
                self.total *= input_value
            elif self.operation == "/":
                if input_value == 0:
                    messagebox.showerror("Error", "Cannot divide by zero")
                    return
                self.total /= input_value
            else:
                self.total = input_value
                
            self.current_input = str(self.total)
            self.reset_input = True
            self.update_display()
        except:
            messagebox.showerror("Error", "Calculation error")
            
    def update_display(self, text=None):
        if text is None:
            text = self.current_input if self.current_input else "0"
        
        # Limit decimal places for cleaner display
        try:
            num = float(text)
            if num.is_integer():
                text = str(int(num))
            else:
                # Limit to 10 decimal places
                text = "{:.10f}".format(num).rstrip("0").rstrip(".")
        except ValueError:
            pass
            
        self.display.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()