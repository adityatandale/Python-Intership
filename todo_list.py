"""
To-Do List Application - Streamlit App
Task 1

Tasks are represented as objects (a Task class) with a description and a
completion status. Users can add, complete/reopen, delete, and filter tasks.

Run with:
    pip install streamlit
    streamlit run todo_list.py
"""

import streamlit as st
from dataclasses import dataclass, field
from datetime import datetime
import uuid

st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")


# ---------------------------------------------------------------------------
# Data structure: Task represented as a class, not a bare dict
# ---------------------------------------------------------------------------

@dataclass
class Task:
    description: str
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = []  # list[Task]

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("✅ To-Do List")
st.write("Add tasks, mark them complete, and keep track of what's left.")

# ---------------------------------------------------------------------------
# Add task
# ---------------------------------------------------------------------------

with st.form("add_task_form", clear_on_submit=True):
    new_task_text = st.text_input("New task", placeholder="e.g. Finish Task 3 README")
    add_clicked = st.form_submit_button("➕ Add Task")

if add_clicked:
    stripped = new_task_text.strip()
    if not stripped:
        st.warning("Task description can't be empty.")
    elif any(t.description.lower() == stripped.lower() and not t.completed for t in st.session_state.tasks):
        st.warning("That task is already on your active list.")
    else:
        st.session_state.tasks.append(Task(description=stripped))
        st.success(f"Added: {stripped}")

# ---------------------------------------------------------------------------
# Filter + stats
# ---------------------------------------------------------------------------

total = len(st.session_state.tasks)
completed_count = sum(1 for t in st.session_state.tasks if t.completed)
active_count = total - completed_count

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Active", active_count)
col3.metric("Completed", completed_count)

filter_choice = st.radio("Show", ["All", "Active", "Completed"], horizontal=True)

if filter_choice == "Active":
    visible_tasks = [t for t in st.session_state.tasks if not t.completed]
elif filter_choice == "Completed":
    visible_tasks = [t for t in st.session_state.tasks if t.completed]
else:
    visible_tasks = st.session_state.tasks

# ---------------------------------------------------------------------------
# Task list
# ---------------------------------------------------------------------------

st.markdown("---")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above to get started.")
elif not visible_tasks:
    st.info(f"No {filter_choice.lower()} tasks.")
else:
    for task in visible_tasks:
        c1, c2, c3 = st.columns([0.08, 0.72, 0.2])

        with c1:
            checked = st.checkbox(
                "done", value=task.completed, key=f"chk_{task.id}", label_visibility="collapsed"
            )
            if checked != task.completed:
                task.completed = checked
                st.rerun()

        with c2:
            if task.completed:
                st.markdown(f"~~{task.description}~~")
            else:
                st.markdown(task.description)
            st.caption(f"Added {task.created_at}")

        with c3:
            if st.button("🗑️ Delete", key=f"del_{task.id}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t.id != task.id]
                st.rerun()

# ---------------------------------------------------------------------------
# Bulk actions
# ---------------------------------------------------------------------------

if st.session_state.tasks:
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if completed_count > 0 and st.button("🧹 Clear completed tasks"):
            st.session_state.tasks = [t for t in st.session_state.tasks if not t.completed]
            st.rerun()
    with b2:
        if st.button("♻️ Delete all tasks"):
            st.session_state.tasks = []
            st.rerun()
