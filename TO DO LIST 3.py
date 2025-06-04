import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.load_data()
        self.create_widgets()
        self.display_todos()

    def setup_main_window(self):
        self.root.title("Colorful To-Do List")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f4ff")

    def load_data(self):
        self.data_file = "todos.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
        try:
            with open(self.data_file, 'r') as f:
                self.todos = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.todos = []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def create_widgets(self):
        self.create_header()
        self.create_left_panel()
        self.create_right_panel()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#f0f4ff")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Rainbow color strip
        colors = ["#ff6b6b", "#ff8e6b", "#ffb16b", "#ffd46b", "#f9f871",
                  "#c7f971", "#97f971", "#6bf98e", "#6bf9c7", "#6bf0f9", "#6bc7f9"]
        for i, color in enumerate(colors):
            tk.Label(header_frame, text=" " * 3, bg=color, font=("Arial", 1)).grid(row=0, column=i, sticky="ew")

        # Main header
        tk.Label(
            header_frame,
            text="🌈 Rainbow To-Do List 🌈",
            font=("Comic Sans MS", 24, "bold"),
            bg="#f0f4ff",
            fg="#5d5dff"
        ).grid(row=1, column=0, columnspan=len(colors), pady=10)

        # Date display
        tk.Label(
            header_frame,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=("Arial", 12, "italic"),
            bg="#f0f4ff",
            fg="#666666"
        ).grid(row=2, column=0, columnspan=len(colors), pady=(0, 10))

    def create_left_panel(self):
        left_frame = tk.Frame(self.root, bg="#f0f4ff")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=10)

        self.create_task_entry(left_frame)
        self.create_filters(left_frame)

    def create_task_entry(self, parent):
        entry_frame = tk.LabelFrame(
            parent,
            text=" Add New Task ",
            font=("Arial", 12, "bold"),
            bg="#f0f4ff",
            fg="#5d5dff",
            bd=2,
            relief=tk.GROOVE
        )
        entry_frame.pack(fill=tk.X, pady=(0, 15))

        # Task description
        tk.Label(entry_frame, text="Task:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.task_entry = tk.Entry(entry_frame, font=("Arial", 12), bg="#ffffff", fg="#333333")
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Priority
        tk.Label(entry_frame, text="Priority:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(
            entry_frame,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Due date
        tk.Label(entry_frame, text="Due Date:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.due_date_entry = tk.Entry(entry_frame, font=("Arial", 12), bg="#ffffff", fg="#333333")
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Category
        tk.Label(entry_frame, text="Category:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.category_var = tk.StringVar(value="Personal")
        ttk.Combobox(
            entry_frame,
            textvariable=self.category_var,
            values=["Personal", "Work", "Study", "Health", "Finance", "Other"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Add button
        tk.Button(
            entry_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg="#6bd9a7",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=3
        ).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    def create_filters(self, parent):
        filter_frame = tk.LabelFrame(
            parent,
            text=" Filter Tasks ",
            font=("Arial", 12, "bold"),
            bg="#f0f4ff",
            fg="#5d5dff",
            bd=2,
            relief=tk.GROOVE
        )
        filter_frame.pack(fill=tk.X, pady=(15, 0))

        # Priority filter
        tk.Label(filter_frame, text="Priority:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.filter_priority_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_priority_var,
            values=["All", "High", "Medium", "Low"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Category filter
        tk.Label(filter_frame, text="Category:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.filter_category_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_category_var,
            values=["All", "Personal", "Work", "Study", "Health", "Finance", "Other"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Status filter
        tk.Label(filter_frame, text="Status:", bg="#f0f4ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.filter_status_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_status_var,
            values=["All", "Completed", "Pending"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Bind filter changes
        for var in [self.filter_priority_var, self.filter_category_var, self.filter_status_var]:
            var.trace_add("write", lambda *args: self.filter_tasks())

    def create_right_panel(self):
        right_frame = tk.Frame(self.root, bg="#f0f4ff")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=10)

        self.create_search_bar(right_frame)
        self.create_task_list(right_frame)
        self.create_action_buttons(right_frame)
        self.create_statistics(right_frame)

    def create_search_bar(self, parent):
        search_frame = tk.Frame(parent, bg="#f0f4ff")
        search_frame.pack(fill=tk.X, pady=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#333333"
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        search_entry.bind("<KeyRelease>", lambda e: self.filter_tasks())

        tk.Button(
            search_frame,
            text="🔍 Search",
            command=self.filter_tasks,
            bg="#5d5dff",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bg="#ff9e7d",
            fg="white",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(5, 0))

    def create_task_list(self, parent):
        list_frame = tk.Frame(parent, bg="#f0f4ff")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview with scrollbar
        self.tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Task", "Priority", "Category", "Due Date", "Status"),
            show="headings",
            selectmode="extended"
        )

        # Configure columns
        columns = {
            "ID": {"width": 40, "anchor": "center"},
            "Task": {"width": 200},
            "Priority": {"width": 80, "anchor": "center"},
            "Category": {"width": 100, "anchor": "center"},
            "Due Date": {"width": 100, "anchor": "center"},
            "Status": {"width": 100, "anchor": "center"}
        }

        for col, settings in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **settings)

        # Style the Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#ffffff",
                        fieldbackground="#ffffff",
                        foreground="#333333",
                        rowheight=30,
                        font=("Arial", 11))
        style.configure("Treeview.Heading",
                        background="#5d5dff",
                        foreground="white",
                        font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", "#a8d8ea")])

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#f0f4ff")
        button_frame.pack(fill=tk.X, pady=(10, 0))

        buttons = [
            ("✓ Complete", "#6bd9a7", self.mark_complete),
            ("✏️ Edit", "#ffd166", self.edit_task),
            ("🗑️ Delete", "#ff6b6b", self.delete_task)
        ]

        for text, color, command in buttons:
            tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 12, "bold"),
                relief=tk.RAISED,
                bd=3
            ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def create_statistics(self, parent):
        stats_frame = tk.LabelFrame(
            parent,
            text=" Task Statistics ",
            font=("Arial", 12, "bold"),
            bg="#f0f4ff",
            fg="#5d5dff",
            bd=2,
            relief=tk.GROOVE
        )
        stats_frame.pack(fill=tk.X, pady=(15, 0))

        self.total_label = tk.Label(
            stats_frame,
            text="Total: 0",
            bg="#f0f4ff",
            fg="#333333",
            font=("Arial", 11)
        )
        self.total_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.completed_label = tk.Label(
            stats_frame,
            text="Completed: 0",
            bg="#f0f4ff",
            fg="#6bd9a7",
            font=("Arial", 11, "bold")
        )
        self.completed_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.pending_label = tk.Label(
            stats_frame,
            text="Pending: 0",
            bg="#f0f4ff",
            fg="#ff6b6b",
            font=("Arial", 11, "bold")
        )
        self.pending_label.pack(side=tk.LEFT, padx=10, pady=5)

    def display_todos(self, todos=None):
        self.tree.delete(*self.tree.get_children())
        todos_to_display = todos if todos is not None else self.todos

        for idx, todo in enumerate(todos_to_display, 1):
            status = "Completed" if todo.get("completed", False) else "Pending"
            priority = todo.get("priority", "Medium")

            self.tree.insert("", tk.END, values=(
                idx,
                todo["task"],
                priority,
                todo.get("category", "Personal"),
                todo.get("due_date", ""),
                status
            ), tags=(priority, status))

        # Configure tag colors
        self.tree.tag_configure("High", background="#ffeeee")
        self.tree.tag_configure("Medium", background="#fff9ee")
        self.tree.tag_configure("Low", background="#eeffee")
        self.tree.tag_configure("Completed", foreground="#6bd9a7")
        self.tree.tag_configure("Pending", foreground="#ff6b6b")

        self.update_statistics(todos_to_display)

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task description.")
            return

        new_task = {
            "task": task,
            "priority": self.priority_var.get(),
            "category": self.category_var.get(),
            "due_date": self.due_date_entry.get(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.todos.append(new_task)
        self.save_data()
        self.display_todos()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Task added successfully!")

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select task(s) to mark as complete.")
            return

        for item in selected:
            task_idx = self.tree.item(item)["values"][0] - 1
            if 0 <= task_idx < len(self.todos):
                self.todos[task_idx]["completed"] = True

        self.save_data()
        self.display_todos()
        messagebox.showinfo("Success", f"Marked {len(selected)} task(s) as complete!")

    def edit_task(self):
        selected = self.tree.selection()
        if not selected or len(selected) > 1:
            messagebox.showwarning("Warning", "Please select a single task to edit.")
            return

        task_idx = self.tree.item(selected[0])["values"][0] - 1
        if 0 <= task_idx < len(self.todos):
            self.show_edit_window(task_idx)

    def show_edit_window(self, task_idx):
        task = self.todos[task_idx]
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x400")
        edit_window.configure(bg="#e6f3ff")
        edit_window.grab_set()

        # Form fields
        tk.Label(edit_window, text="Edit Task", font=("Arial", 16, "bold"), bg="#e6f3ff", fg="#5d5dff"
                 ).pack(pady=10)

        fields_frame = tk.Frame(edit_window, bg="#e6f3ff")
        fields_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Task description
        tk.Label(fields_frame, text="Task:", bg="#e6f3ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        task_entry = tk.Entry(fields_frame, font=("Arial", 12), bg="#ffffff", fg="#333333")
        task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        task_entry.insert(0, task["task"])

        # Priority
        tk.Label(fields_frame, text="Priority:", bg="#e6f3ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        priority_var = tk.StringVar(value=task.get("priority", "Medium"))
        ttk.Combobox(
            fields_frame,
            textvariable=priority_var,
            values=["High", "Medium", "Low"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Due date
        tk.Label(fields_frame, text="Due Date:", bg="#e6f3ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        due_date_entry = tk.Entry(fields_frame, font=("Arial", 12), bg="#ffffff", fg="#333333")
        due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        due_date_entry.insert(0, task.get("due_date", ""))

        # Category
        tk.Label(fields_frame, text="Category:", bg="#e6f3ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        category_var = tk.StringVar(value=task.get("category", "Personal"))
        ttk.Combobox(
            fields_frame,
            textvariable=category_var,
            values=["Personal", "Work", "Study", "Health", "Finance", "Other"],
            font=("Arial", 11),
            state="readonly"
        ).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Status
        tk.Label(fields_frame, text="Status:", bg="#e6f3ff", fg="#333333", font=("Arial", 11)
                 ).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        status_var = tk.BooleanVar(value=task.get("completed", False))
        tk.Checkbutton(
            fields_frame,
            text="Completed",
            variable=status_var,
            bg="#e6f3ff",
            font=("Arial", 11)
        ).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Buttons
        button_frame = tk.Frame(edit_window, bg="#e6f3ff")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Save Changes",
            command=lambda: self.save_edited_task(
                task_idx,
                task_entry.get(),
                priority_var.get(),
                due_date_entry.get(),
                category_var.get(),
                status_var.get(),
                edit_window
            ),
            bg="#5d5dff",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Cancel",
            command=edit_window.destroy,
            bg="#ff6b6b",
            fg="white",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=10)

    def save_edited_task(self, task_idx, task, priority, due_date, category, completed, window):
        if not task:
            messagebox.showwarning("Warning", "Task description cannot be empty.")
            return

        self.todos[task_idx] = {
            "task": task,
            "priority": priority,
            "due_date": due_date,
            "category": category,
            "completed": completed,
            "created_at": self.todos[task_idx]["created_at"]
        }

        self.save_data()
        self.display_todos()
        window.destroy()
        messagebox.showinfo("Success", "Task updated successfully!")

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select task(s) to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} task(s)?"):
            indices = sorted([self.tree.item(item)["values"][0] - 1 for item in selected], reverse=True)
            for idx in indices:
                if 0 <= idx < len(self.todos):
                    self.todos.pop(idx)

            self.save_data()
            self.display_todos()
            messagebox.showinfo("Success", f"Deleted {len(selected)} task(s)!")

    def filter_tasks(self):
        search_text = self.search_var.get().lower()
        priority_filter = self.filter_priority_var.get()
        category_filter = self.filter_category_var.get()
        status_filter = self.filter_status_var.get()

        filtered_tasks = []

        for task in self.todos:
            matches = True

            if search_text and search_text not in task["task"].lower():
                matches = False

            if priority_filter != "All" and task.get("priority", "Medium") != priority_filter:
                matches = False

            if category_filter != "All" and task.get("category", "Personal") != category_filter:
                matches = False

            if status_filter != "All":
                task_status = "Completed" if task.get("completed", False) else "Pending"
                if status_filter != task_status:
                    matches = False

            if matches:
                filtered_tasks.append(task)

        self.display_todos(filtered_tasks)

    def clear_search(self):
        self.search_var.set("")
        self.filter_priority_var.set("All")
        self.filter_category_var.set("All")
        self.filter_status_var.set("All")
        self.display_todos()

    def update_statistics(self, tasks):
        total = len(tasks)
        completed = sum(1 for task in tasks if task.get("completed", False))
        pending = total - completed

        self.total_label.config(text=f"Total: {total}")
        self.completed_label.config(text=f"Completed: {completed}")
        self.pending_label.config(text=f"Pending: {pending}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()