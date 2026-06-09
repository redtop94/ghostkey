import tkinter as tk
from tkinter import font, messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("700x600")
        self.root.config(bg="#1a1a1a")
        
        # Storage file
        self.storage_file = "todos.json"
        self.todos = self.load_todos()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(
            self.root,
            text="Todo List",
            font=title_font,
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#1a1a1a")
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.todo_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        self.todo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.todo_entry.bind("<Return>", lambda e: self.add_todo())
        
        add_btn = tk.Button(
            input_frame,
            text="Add",
            font=("Helvetica", 12),
            bg="#00ff00",
            fg="#000000",
            command=self.add_todo,
            width=8
        )
        add_btn.pack(side=tk.LEFT)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=10, padx=20, fill=tk.X)
        
        clear_completed_btn = tk.Button(
            btn_frame,
            text="Clear Completed",
            font=("Helvetica", 10),
            bg="#ff6600",
            fg="#ffffff",
            command=self.clear_completed
        )
        clear_completed_btn.pack(side=tk.LEFT, padx=5)
        
        delete_all_btn = tk.Button(
            btn_frame,
            text="Delete All",
            font=("Helvetica", 10),
            bg="#ff3333",
            fg="#ffffff",
            command=self.delete_all
        )
        delete_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Listbox frame
        list_frame = tk.Frame(self.root, bg="#1a1a1a")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 11),
            bg="#2a2a2a",
            fg="#ffffff",
            yscrollcommand=scrollbar.set,
            activestyle="none",
            selectmode=tk.SINGLE
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind right-click and double-click
        self.listbox.bind("<Button-3>", self.show_context_menu)
        self.listbox.bind("<Double-1>", self.toggle_todo)
        
        # Stats label
        self.stats_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 10),
            bg="#1a1a1a",
            fg="#00ccff"
        )
        self.stats_label.pack(pady=10)
        
        # Load and display todos
        self.refresh_list()
    
    def add_todo(self):
        task = self.todo_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        todo = {
            "task": task,
            "completed": False,
            "created": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self.save_todos()
        self.todo_entry.delete(0, tk.END)
        self.refresh_list()
    
    def toggle_todo(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        self.todos[index]["completed"] = not self.todos[index]["completed"]
        self.save_todos()
        self.refresh_list()
    
    def delete_todo(self, index):
        del self.todos[index]
        self.save_todos()
        self.refresh_list()
    
    def clear_completed(self):
        self.todos = [t for t in self.todos if not t["completed"]]
        self.save_todos()
        self.refresh_list()
    
    def delete_all(self):
        if messagebox.askyesno("Confirm", "Delete all todos?"):
            self.todos = []
            self.save_todos()
            self.refresh_list()
    
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        
        for i, todo in enumerate(self.todos):
            task = todo["task"]
            completed = todo["completed"]
            
            # Format: [X] Task or [ ] Task
            prefix = "[✓]" if completed else "[ ]"
            display = f"{prefix} {task}"
            
            self.listbox.insert(tk.END, display)
            
            # Color completed tasks
            if completed:
                self.listbox.itemconfig(i, fg="#666666")
            else:
                self.listbox.itemconfig(i, fg="#ffffff")
        
        # Update stats
        completed_count = sum(1 for t in self.todos if t["completed"])
        total_count = len(self.todos)
        self.stats_label.config(
            text=f"Total: {total_count} | Completed: {completed_count} | Pending: {total_count - completed_count}"
        )
    
    def show_context_menu(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=False, bg="#2a2a2a", fg="#ffffff")
        context_menu.add_command(
            label="Toggle Complete",
            command=lambda: self.toggle_and_refresh(index)
        )
        context_menu.add_command(
            label="Delete",
            command=lambda: self.delete_and_refresh(index)
        )
        
        context_menu.post(event.x_root, event.y_root)
    
    def toggle_and_refresh(self, index):
        self.toggle_todo()
    
    def delete_and_refresh(self, index):
        self.delete_todo(index)
    
    def save_todos(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.todos, f, indent=2)
    
    def load_todos(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
