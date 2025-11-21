import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os 

DATA_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        root.title("To Do List")
        root.geometry("420x460")
        root.minsize(360, 360)

        # Top label
        ttk.Label(root, text="To Do List", font=("Segoe UI", 16, "bold")).pack(pady=8)

        # Input frame
        input_frame = ttk.Frame(root, padding=8)
        input_frame.pack(fill='x')
        self.new_text_var = tk.StringVar()
        self.entry = ttk.Entry(input_frame, textvariable=self.new_text_var)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.add_task())

        ttk.Button(input_frame, text="Add", command=self.add_task).pack(side="left", padx=6)

        # Middle: listbox with scrollbar
        box_frame = ttk.Frame(root, padding=(8, 0, 8, 8))
        box_frame.pack(fill="both", expand=True)

        self.tasks_listbox = tk.Listbox(box_frame, selectmode="extended", activestyle="none")
        self.tasks_listbox.pack(side="left", fill="both", expand=True)
        self.tasks_listbox.bind("<Double-1>", lambda e: self.toggle_done())

        scrollbar = ttk.Scrollbar(box_frame, orient="vertical", command=self.tasks_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)

        # Bottom buttons
        btn_frame = ttk.Frame(root, padding=8)
        btn_frame.pack(fill='x')

        ttk.Button(btn_frame, text="Mark Done/Undone", command=self.toggle_done).grid(row=0, column=0, padx=4, pady=4)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).grid(row=0, column=1, padx=4, pady=4)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=4, pady=4)

        ttk.Separator(root).pack(fill="x", pady=(6, 6))

        # Save/Load area
        save_frame = ttk.Frame(root, padding=8)
        save_frame.pack(fill="x")

        ttk.Button(save_frame, text="Save", command=self.save_tasks).pack(side="left")
        ttk.Button(save_frame, text="Load", command=self.load_tasks).pack(side="left", padx=6)
        ttk.Button(save_frame, text="Save As...", command=self.save_as).pack(side="left", padx=6)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(root, textvariable=self.status_var, anchor="w").pack(fill="x", padx=8, pady=(6, 6))

        # Task storage
        self.tasks = []
        self.load_tasks()

        # Shortcuts
        root.bind("<Control-s>", lambda e: self.save_tasks())
        root.bind("<Control-o>", lambda e: self.load_tasks())
        root.bind("<Control-n>", lambda e: self.clear_all())
        root.bind("<Delete>", lambda e: self.delete_selected())
