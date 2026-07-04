import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def refresh_listbox():
    task_listbox.delete(0, tk.END)

    for task in tasks:
        status = "✅" if task["completed"] else "❌"

        display_text = (
            f"{status} {task['title']} | "
            f"{task['priority']} | "
            f"{task['due_date']}"
        )

        task_listbox.insert(tk.END, display_text)


def add_task():
    title = title_entry.get().strip()
    priority = priority_var.get()
    due_date = due_entry.get().strip()

    if not title:
        messagebox.showerror("Error", "Task name cannot be empty!")
        return

    task = {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)

    save_tasks()
    refresh_listbox()

    title_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Task Added Successfully!")



def complete_task():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first!")
        return

    index = selected[0]

    tasks[index]["completed"] = True

    save_tasks()
    refresh_listbox()

    messagebox.showinfo("Done", "Task Completed!")


def delete_task():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first!")
        return

    index = selected[0]

    tasks.pop(index)

    save_tasks()
    refresh_listbox()

    messagebox.showinfo("Deleted", "Task Deleted!")


def show_statistics():
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed

    messagebox.showinfo(
        "Statistics",
        f"📌 Total Tasks: {total}\n\n"
        f"✅ Completed: {completed}\n\n"
        f"❌ Pending: {pending}"
    )

tasks = load_tasks()

root = tk.Tk()
root.title("Smart To-Do Manager")
root.geometry("850x600")
root.configure(bg="#1E1E2E")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="📝 SMART TO-DO MANAGER",
    font=("Segoe UI", 22, "bold"),
    bg="#1E1E2E",
    fg="#00FFCC"
)
title_label.pack(pady=15)

tk.Label(
    root,
    text="Task Name",
    bg="#1E1E2E",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack()

title_entry = tk.Entry(
    root,
    width=40,
    font=("Segoe UI", 11),
    bg="#2A2A3C",
    fg="white",
    insertbackground="white"
)
title_entry.pack(pady=5)


tk.Label(
    root,
    text="Priority",
    bg="#1E1E2E",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack()

priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(
    root,
    priority_var,
    "High",
    "Medium",
    "Low"
)

priority_menu.config(
    bg="#2A2A3C",
    fg="white",
    font=("Segoe UI", 10)
)

priority_menu.pack(pady=5)


tk.Label(
    root,
    text="Due Date",
    bg="#1E1E2E",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack()

due_entry = tk.Entry(
    root,
    width=30,
    font=("Segoe UI", 11),
    bg="#2A2A3C",
    fg="white",
    insertbackground="white"
)
due_entry.pack(pady=5)


button_frame = tk.Frame(root, bg="#1E1E2E")
button_frame.pack(pady=15)

# Add Button
tk.Button(
    button_frame,
    text="➕ Add",
    width=12,
    bg="#00C853",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=add_task
).grid(row=0, column=0, padx=5)


tk.Button(
    button_frame,
    text="✅ Complete",
    width=12,
    bg="#2962FF",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=complete_task
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="🗑 Delete",
    width=12,
    bg="#D50000",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=delete_task
).grid(row=0, column=2, padx=5)


tk.Button(
    button_frame,
    text="📊 Stats",
    width=12,
    bg="#FF6D00",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=show_statistics
).grid(row=0, column=3, padx=5)


task_listbox = tk.Listbox(
    root,
    width=90,
    height=15,
    font=("Consolas", 11),
    bg="#2A2A3C",
    fg="white",
    selectbackground="#00C853",
    selectforeground="white",
    bd=0
)

task_listbox.pack(pady=20)

refresh_listbox()

footer = tk.Label(
    root,
    text="🚀 Smart To-Do Manager | Python Tkinter Project",
    bg="#1E1E2E",
    fg="gray",
    font=("Segoe UI", 9)
)

footer.pack(side="bottom", pady=10)

root.mainloop()
