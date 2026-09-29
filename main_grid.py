import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from tkcalendar import DateEntry
from datetime import datetime

def check_all_deadlines():
    reminders = []

    for task in tasks:
        if task["completed"]:
            continue
        reminder = check_deadline(task["task"], task["subject"], task["deadline"])

        if reminder:
            reminders.append(reminder)

    if reminders:
        messagebox.showinfo(
            "Upcoming Deadlines",
            "\n".join(reminders)
        )

def check_deadline(task_name, subject, deadline):
    deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
    today = datetime.today().date()

    days_left = (deadline_date - today).days

    if days_left == 2:
        return f"{subject} — {task_name} — 2 days left"
    elif days_left == 1:
        return f"{subject} — {task_name} — due tomorrow"
    elif days_left == 0:
        return f"{subject} — {task_name} — due today"
    elif days_left < 0:
        return f"{subject} — {task_name} — overdue by {-days_left} days"
    
BG_COLOR = "#BEECC2"
LABEL_COLOR = "#1B4332"
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT = "white"

subjects = []
tasks = []

root = tk.Tk()
root.title("Study Planner")
root.geometry("1100x1000")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

def add_task():
    if task_entry.get().strip() == "":
        messagebox.showerror("Error", "Please enter a task")
        return
    if deadline_entry.get().strip() == "":
        messagebox.showerror("Error", "Please enter a deadline")
        return
    if subject_dropdown.get() == "":
        messagebox.showerror("Error", "Please select a subject")
        return
    if priority_dropdown.get() == "":
        messagebox.showerror("Error", "Please select the priority level")
        return

    new_task = {"task": task_entry.get(), "subject": subject_dropdown.get(), "deadline": deadline_entry.get(), "priority": priority_dropdown.get(),
    "completed": False}
    tasks.append(new_task)

    task_info = f"{task_entry.get()} | {subject_dropdown.get()} | {deadline_entry.get()} | {priority_dropdown.get()}"
    tasks_listbox.insert(tk.END, task_info)
    
    save_tasks()

    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    subject_dropdown.set("")
    priority_dropdown.set("")
    update_summary()

def delete_task():
    selected = tasks_listbox.curselection()

    if len(selected) == 0:
        messagebox.showerror("Error", "Please select a task to delete.")
        return

    selected_index = selected[0]

    tasks.pop(selected_index)
    tasks_listbox.delete(selected_index)
    save_tasks()
    update_summary()

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
    
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            saved_tasks = json.load(file)

        tasks.extend(saved_tasks)

        for task in tasks:
            task_info = f"{task['task']} | {task['subject']} | {task['deadline']} | {task['priority']}"
            if task["completed"]:
                task_info = "✔ " + task_info
            tasks_listbox.insert(tk.END, task_info)

    except (FileNotFoundError, json.JSONDecodeError):
        pass

def complete_task():
    selected = tasks_listbox.curselection()

    if len(selected) == 0:
        messagebox.showerror("Error", "Please select a task to complete.")
        return

    selected_index = selected[0]

    if tasks[selected_index]["completed"]:
        messagebox.showinfo(
            "Already Completed",
            "This task has already been marked as completed."
        )
        return

    tasks[selected_index]["completed"] = True

    selected_task = tasks[selected_index]

    completed_task = (
        "✔ " +
        f"{selected_task['task']} | "
        f"{selected_task['subject']} | "
        f"{selected_task['deadline']} | "
        f"{selected_task['priority']}"
    )

    tasks_listbox.delete(selected_index)
    tasks_listbox.insert(selected_index, completed_task)

    save_tasks()
    update_summary()

def clear_completed():
    for i in range(len(tasks) - 1, -1, -1):
        if tasks[i]["completed"]:
            tasks.pop(i)
            tasks_listbox.delete(i)
    save_tasks()
    update_summary()

def update_summary():
    total_tasks = len(tasks)
    completed_tasks = 0
    high_priority_tasks = 0

    for task in tasks:
        if task["completed"]:
            completed_tasks += 1

        if task["priority"] == "High" and not task["completed"]:
            high_priority_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    total_label.config(text = f"Total Tasks: {total_tasks}")
    pending_label.config(text = f"Pending: {pending_tasks}")
    completed_label.config(text = f"Completed: {completed_tasks}")
    high_priority_label.config(text = f"High Priority: {high_priority_tasks}")

def add_subject():
    new_subject = subject_entry.get().strip()
    if new_subject == "":
        messagebox.showerror("Error", "Please enter a subject")
        return
    subjects.append(new_subject)
    save_subjects()
    subject_dropdown["values"] = subjects
    subject_entry.delete(0, tk.END)

def remove_subject():
    selected_subject = subject_dropdown.get()

    if selected_subject == "":
        messagebox.showerror("Error", "Please select a subject to remove")
        return

    confirm = messagebox.askyesno("Remove Subject", f"Are you sure you want to remove '{selected_subject}'?")
    if not confirm:
        return
    subjects.remove(selected_subject)
    save_subjects()
    subject_dropdown["values"] = subjects
    subject_dropdown.set("")

def save_subjects():
    with open("subjects.json", "w") as file:
        json.dump(subjects, file)

def load_subjects():
    try:
        with open("subjects.json", "r") as file:
            saved_subjects = json.load(file)
        subjects.extend(saved_subjects)
        subject_dropdown["values"] = subjects
    except (FileNotFoundError, json.JSONDecodeError):
        pass


heading = tk.Label(root, text = "Study Planner", font = ("Arial", 20, "bold"), bg=BG_COLOR,
fg=LABEL_COLOR)
heading.grid(row = 0, column = 0, columnspan = 2, pady = 10)

task_label = tk.Label(root, text="Task", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
task_label.grid(row = 1, column = 0, pady = 10, padx = 20)

task_entry = tk.Entry(root, width = 40, font = ("Arial", 14))
task_entry.grid(row = 1, column = 1, pady = 10, padx = 10)

subject_label = tk.Label(root, text = "Subject", font = ("Arial", 20, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
subject_label.grid(row = 2, column = 0, pady = 10, padx = 10)

subject_dropdown = ttk.Combobox(root, values = subjects, width = 25, font = ("Arial", 14), state = "readonly")
subject_dropdown.grid(row = 2, column = 1, pady = 10, padx = 10)

subject_frame = tk.Frame(root, bg = BG_COLOR)
subject_frame.grid(row = 2, column = 2, padx = 0, pady = 20)

subject_entry = tk.Entry(subject_frame, width = 10, font = ("Arial", 14))
subject_entry.pack(side = "left", padx = 5)

add_subject_button = tk.Button(subject_frame, text="Add Subject", font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg=BUTTON_TEXT, command = add_subject)
add_subject_button.pack(pady = 5)

remove_subject_button = tk.Button(subject_frame, text="Remove Subject", font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg=BUTTON_TEXT,command=remove_subject)
remove_subject_button.pack(pady = 5)

deadline_label = tk.Label(root, text = "Deadline", font = ("Arial", 20, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
deadline_label.grid(row = 3, column = 0, pady = 10, padx = 20)

deadline_entry = DateEntry(root, width = 30, font=("Arial", 20), date_pattern="dd/mm/yyyy", bg=BG_COLOR, fg=LABEL_COLOR)
deadline_entry.grid(row = 3, column = 1, pady = 10, padx = 20)

priority_label = tk.Label(root, text = "Priority", font = ("Arial", 20, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
priority_label.grid(row = 4, column = 0, pady = 10, padx = 20)

priority_dropdown = ttk.Combobox(root, width = 40, values = ["High", "Medium", "Low"], font = ("Arial", 14), state = "readonly")
priority_dropdown.grid(row = 4, column = 1, pady = 10, padx = 20)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.grid(row=5, column=0, columnspan=3, pady = 10)

add_button = tk.Button(button_frame, text = "Add Task", font = ("Arial", 14, "bold"), command = add_task, bg=BUTTON_COLOR,
fg=BUTTON_TEXT)
add_button.pack(side = "left", padx = 5)

delete_button = tk.Button(button_frame, text = "Delete Task", font = ("Arial", 14, "bold"), command = delete_task,  bg=BUTTON_COLOR, fg=BUTTON_TEXT)
delete_button.pack(side = "left", padx = 5)

complete_button = tk.Button(button_frame, text = "Complete Task", font = ("Arial", 14, "bold"), command = complete_task, bg=BUTTON_COLOR,
fg=BUTTON_TEXT)
complete_button.pack(side = "left", padx = 5)

clear_button = tk.Button(button_frame, text = "Clear Completed Tasks", font = ("Arial", 14, "bold"), command = clear_completed, bg = BUTTON_COLOR, fg = BUTTON_TEXT)
clear_button.pack(side = "left", padx = 5)

tasks_label = tk.Label(root, text = "To-do List", font = ("Arial", 20, "bold"))
tasks_label.grid(row = 6, column = 0, pady = 10, padx = 20)

tasks_frame = tk.Frame(root, bg = BG_COLOR)
tasks_frame.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 20)

tasks_scrollbar = tk.Scrollbar(tasks_frame, orient="vertical")
tasks_scrollbar.pack(side = "right", fill = "y")

tasks_listbox = tk.Listbox(tasks_frame, width = 70, height = 6, font = ("Arial", 14), yscrollcommand = tasks_scrollbar.set)
tasks_listbox.pack(side = "left")

tasks_scrollbar.config(command = tasks_listbox.yview)

summary_frame = tk.Frame(root, bg = BG_COLOR)
summary_frame.grid(row = 7, column = 2, pady = 0, padx = 20,sticky = "n")

summary_label = tk.Label(summary_frame, text = "Task Summary", font = ("Arial", 16, "bold"), bg = BUTTON_COLOR, fg = BUTTON_TEXT)
summary_label.grid(row = 0, column = 0, pady = 2)

total_label = tk.Label(summary_frame, text = "Total Tasks: 0", font = ("Arial", 14, "bold"), bg = BG_COLOR, fg = LABEL_COLOR)
total_label.grid(row = 1, column = 0, pady = 0)

pending_label = tk.Label(summary_frame, text = "Pending: 0", font = ("Arial", 14, "bold"), bg = BG_COLOR, fg = LABEL_COLOR)
pending_label.grid(row = 2, column = 0, pady = 0)

completed_label = tk.Label(summary_frame, text = "Completed: 0", font = ("Arial", 14, "bold"), bg = BG_COLOR, fg = LABEL_COLOR) 
completed_label.grid(row = 3, column = 0, pady = 0)

high_priority_label = tk.Label(summary_frame, text = "High Priority: 0", font = ("Arial", 14, "bold"), bg = BG_COLOR, fg = LABEL_COLOR)
high_priority_label.grid(row = 4, column = 0, pady =0)

load_tasks()
load_subjects()

check_all_deadlines()
print("Reached the bottom")
update_summary()
root.mainloop()