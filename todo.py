import streamlit as st
import json
import os
from datetime import date

FILE_NAME = "tasks.json"

# Load tasks
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        tasks = json.load(file)
else:
    tasks = []

# Session state
if "tasks" not in st.session_state:
    st.session_state.tasks = tasks

if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1

# Save function
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(st.session_state.tasks, file)

# Background styling
st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5d0fe;
    }

    .stButton>button {
        border-radius: 10px;
        background-color: #9333ea;
        color: white;
        border: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("📝 Smart Task Manager")

# -------- Add Task --------
every_day=st.checkbox("Every Day Task")
with st.form("add_form", clear_on_submit=True):

    new_task = st.text_input("Enter a task")
    priority = st.selectbox("Select Priority", ["Low", "Medium", "High"])

    if every_day:
        due_date = "Every Day"
    else:
        due_date = st.date_input(
            "Select Due Date",
             min_value=date.today()
    )

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if new_task:

            task_data = {
                "task": new_task,
                "due_date": str(due_date),
                "every_day": every_day,
                "priority":priority,
                "completed": False
            }

            st.session_state.tasks.append(task_data)

            save_tasks()

            st.success("Task added!")

            st.rerun()

st.subheader("Tasks")

# -------- Display Tasks --------
i = 0

for t in st.session_state.tasks:

    col1, col2, col3, col4,col5 = st.columns([4,2,1,1,1])

    # Edit mode
    if st.session_state.edit_index == i:

        with col1:

            with st.form(f"edit_form_{i}"):

                updated_task = st.text_input(
                    "Edit Task",
                    value=t["task"]
                )

                updated_date = st.date_input(
                    "Update Due Date"
                )

                updated = st.form_submit_button("Save")

                if updated:

                    st.session_state.tasks[i]["task"] = updated_task
                    st.session_state.tasks[i]["due_date"] = str(updated_date)

                    st.session_state.edit_index = -1

                    save_tasks()

                    st.rerun()

    else:

        with col1:

            completed = st.checkbox(
                t["task"],
                value=t["completed"],
                key=f"check_{i}"
            )

            st.session_state.tasks[i]["completed"] = completed
        with col2:

            if t["priority"] == "High":
                st.error("🔴 High")

            elif t["priority"] == "Medium":
                st.warning("🟡 Medium")

            else:
                st.success("🟢 Low")

        with col3:
            if t["every_day"]:
                    st.write("🔁 Every Day")
            else:
                    st.write(f"📅 {t['due_date']}")

        with col4:
            if st.button("Edit", key=f"edit_{i}"):

                st.session_state.edit_index = i

                st.rerun()

    # Delete button
    with col5:
        if st.button("Delete", key=f"delete_{i}"):

            st.session_state.tasks.pop(i)

            save_tasks()

            st.rerun()

    i += 1

# Save checkbox updates
save_tasks()