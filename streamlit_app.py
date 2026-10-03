import streamlit as st
from streamlit_local_storage import LocalStorage
import time
from datetime import date, datetime

local_storage = LocalStorage()

def get_deadline_reminders(tasks):
    reminders = []
    today = date.today()
    for task_item in tasks:
        if task_item.get("completed", False):
            continue
        deadline = datetime.strptime(
            task_item["deadline"],
            "%Y-%m-%d"
        ).date()
        days_left = (deadline - today).days
        if days_left == 0:
            reminders.append(
                f"🔴 {task_item['subject']} — "
                f"{task_item['task']} — due today"
            )
        elif days_left == 1:
            reminders.append(
                f"🟠 {task_item['subject']} — "
                f"{task_item['task']} — due tomorrow"
            )
        elif days_left == 2:
            reminders.append(
                f"🟡 {task_item['subject']} — "
                f"{task_item['task']} — 2 days left"
            )
        elif days_left < 0:
            reminders.append(
                f"🔴 {task_item['subject']} — "
                f"{task_item['task']} — "
                f"overdue by {abs(days_left)} days"
            )
    return reminders

if "tasks" not in st.session_state:
    saved_tasks = local_storage.getItem("tasks")
    if saved_tasks is not None:
        st.session_state.tasks = saved_tasks
    else:
        st.session_state.tasks = []

if "subjects" not in st.session_state:
    saved_subjects = local_storage.getItem("subjects")
    if saved_subjects is None:
        st.session_state.subjects = []
    else:
        st.session_state.subjects = saved_subjects

st.title("📚 Study Planner")
st.write("Welcome to your personal academic planner!")

reminders = get_deadline_reminders(st.session_state.tasks)

if reminders:
    st.warning("⏰ Upcoming Deadlines")
    for reminder in reminders:
        st.write(reminder)

st.header("➕ Add a Task")

task = st.text_input("Task")
if len(st.session_state.subjects) == 0:
    st.info("📚 No subjects added yet. Add your subjects below to get started!")
    subject = None
else:
    subject = st.selectbox("Subject", st.session_state.subjects)

deadline = st.date_input("Deadline")
priority = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add Task"):
    if subject is None:
        st.warning("Please add a subject before creating a task.")
    else:
        new_task = {"task": task, "subject": subject, "deadline": str(deadline), "priority": priority, "completed": False}

        st.session_state.tasks.append(new_task)
        local_storage.setItem("tasks", st.session_state.tasks)
        time.sleep(1.5)
        st.success("Task added successfully! 🎉")

st.header("📋 To-Do List")

if len(st.session_state.tasks) == 0:
    st.write("No tasks added yet.")
else:
    for index, task_item in enumerate(st.session_state.tasks):

        if task_item.get("completed", False):
            st.write(
                f"~~{task_item['task']} | "
                f"{task_item['subject']} | "
                f"{task_item['deadline']} | "
                f"{task_item['priority']}~~"
            )
            st.success("✅ Completed")

        else:
            st.write(
                f"**{task_item['task']}** | "
                f"{task_item['subject']} | "
                f"{task_item['deadline']} | "
                f"{task_item['priority']}"
            )

            if st.button("✅ Complete", key=f"complete_{index}"):
                task_item["completed"] = True
                local_storage.setItem("tasks", st.session_state.tasks)
                time.sleep(1)
                st.rerun()

            if st.button("🗑️ Delete", key=f"delete_{index}"):
                st.session_state.tasks.pop(index)
                local_storage.setItem("tasks", st.session_state.tasks)
                time.sleep(2)
                st.rerun()

if st.button("🧹 Clear Completed Tasks"):
    st.session_state.tasks = [
        task_item
        for task_item in st.session_state.tasks
        if not task_item.get("completed", False)
    ]

    local_storage.setItem("tasks", st.session_state.tasks)
    time.sleep(2)
    st.rerun()

st.header("📚 Manage Subjects")

new_subject = st.text_input("New Subject")

if st.button("➕ Add Subject"):
    if new_subject.strip() == "":
        st.warning("Please enter a subject name.")
    elif new_subject in st.session_state.subjects:
        st.warning("Subject already exists.")
    else:
        st.session_state.subjects.append(new_subject)

        local_storage.setItem(
            "subjects",
            st.session_state.subjects
        )

        time.sleep(1.5)

        st.success("Subject added successfully! 🎉")
        st.rerun()

if len(st.session_state.subjects) == 0:
    st.info("No subjects available to remove.")
else:
    remove_subject = st.selectbox(
        "Select Subject to Remove",
        st.session_state.subjects
    )
    if st.button("➖ Remove Subject"):
        if len(st.session_state.subjects) == 1:
            st.warning("At least one subject must remain.")
        else:
            st.session_state.subjects.remove(remove_subject)
            local_storage.setItem(
                "subjects",
                st.session_state.subjects
            )
            time.sleep(2)
            st.success("Subject removed successfully! 🗑️")
            st.rerun()

st.header("📊 Task Summary")
total_tasks = len(st.session_state.tasks)

completed_tasks = 0
high_priority_tasks = 0

for task_item in st.session_state.tasks:
    if task_item.get("completed", False):
        completed_tasks += 1

    if task_item["priority"] == "High" and not task_item.get("completed", False):
        high_priority_tasks += 1

pending_tasks = total_tasks - completed_tasks
st.write(f"**Total Tasks:** {total_tasks}")
st.write(f"**Pending:** {pending_tasks}")
st.write(f"**Completed:** {completed_tasks}")
st.write(f"**High Priority:** {high_priority_tasks}")