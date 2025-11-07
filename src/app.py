"""
Streamlit web application for the task manager.
"""

import os
import sys
import streamlit as st

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def main():
    """Main function for the Streamlit application."""
    st.set_page_config(
        page_title="Task Manager",
        page_icon="✅",
        layout="wide"
    )
    
    st.title("Task Manager")
    st.write("Manage your tasks efficiently")
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["View Tasks", "Add Task", "Search Tasks"])
    
    if page == "View Tasks":
        display_tasks_page(task_service)
    elif page == "Add Task":
        add_task_page(task_service)
    elif page == "Search Tasks":
        search_tasks_page(task_service)


def display_tasks_page(task_service):
    """Display the tasks page."""
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("Show completed tasks", value=False)
    with col2:
        filter_priority = st.selectbox(
            "Filter by priority",
            ["All", "Low", "Medium", "High"]
        )
    
    # Get tasks
    tasks = task_service.get_all_tasks(show_completed=True)
    
    # Apply filters
    if not show_completed:
        tasks = [task for task in tasks if not task.completed]
    
    if filter_priority != "All":
        tasks = [task for task in tasks if task.priority.lower() == filter_priority.lower()]
    
    if not tasks:
        st.info("No tasks found matching your criteria.")
        return
    
    # Display tasks
    for task in tasks:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if task.completed:
                    st.markdown(f"~~**{task.title}**~~")
                else:
                    st.markdown(f"**{task.title}**")
                
                with st.expander("Details"):
                    st.write(f"**Description:** {task.description}")
                    st.write(f"**Created at:** {task.created_at}")
            
            with col2:
                priority_color = {
                    "low": "blue",
                    "medium": "orange",
                    "high": "red"
                }.get(task.priority.lower(), "gray")
                
                st.markdown(
                    f"<span style='color:{priority_color};font-weight:bold;'>{task.priority.upper()}</span>",
                    unsafe_allow_html=True
                )
            
            with col3:
                # BOUTONS D'ACTION POUR CHAQUE TÂCHE
                action_col1, action_col2 = st.columns(2)
                
                with action_col1:
                    if not task.completed and st.button("✓", key=f"complete_{task.id}"):
                        task_service.complete_task(task.id)
                        st.experimental_rerun()
                
                with action_col2:
                    # BOUTON DE SUPPRESSION AVEC ICÔNE POUBELLE
                    if st.button("🗑️", key=f"delete_{task.id}", help="Delete task"):
                        st.session_state[f"confirm_delete_{task.id}"] = True
                        st.experimental_rerun()
            
            st.divider()
    
    # GESTION DES CONFIRMATIONS DE SUPPRESSION
    # PARCOURIR TOUTES LES TÂCHES POUR VÉRIFIER LES DEMANDES DE SUPPRESSION
    for task in tasks:
        if st.session_state.get(f"confirm_delete_{task.id}", False):
            st.warning(f"⚠️ Are you sure you want to delete the task: **{task.title}**?")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("Yes, Delete", key=f"confirm_yes_{task.id}", type="primary"):
                    try:
                        task_service.delete_task(task.id)
                        st.success(f"Task '{task.title}' deleted successfully!")
                        # NETTOYER L'ÉTAT DE SESSION APRÈS SUPPRESSION
                        del st.session_state[f"confirm_delete_{task.id}"]
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error deleting task: {str(e)}")
            
            with col2:
                if st.button("Cancel", key=f"confirm_no_{task.id}"):
                    # ANNULER LA SUPPRESSION ET NETTOYER L'ÉTAT
                    del st.session_state[f"confirm_delete_{task.id}"]
                    st.experimental_rerun()
            
            # ARRÊTER APRÈS LA PREMIÈRE CONFIRMATION TROUVÉE POUR ÉVITER LES CONFLITS
            break


def add_task_page(task_service):
    """Display the add task page."""
    st.header("Add New Task")
    
    with st.form("add_task_form"):
        title = st.text_input("Title", max_chars=50)
        description = st.text_area("Description", max_chars=200)
        priority = st.select_slider(
            "Priority",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        submitted = st.form_submit_button("Add Task")
        
        if submitted:
            if not title:
                st.error("Title is required")
            else:
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=priority.lower()
                )
                st.success(f"Task '{title}' added successfully with ID {task.id}")


def search_tasks_page(task_service):
    """Display the search tasks page."""
    st.header("Search Tasks")
    
    keyword = st.text_input("Search for tasks", placeholder="Enter keyword...")
    
    if keyword:
        results = task_service.search_tasks(keyword)
        
        if not results:
            st.info(f"No tasks found matching '{keyword}'")
        else:
            st.write(f"Found {len(results)} tasks matching '{keyword}':")
            
            for task in results:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        status = "Completed" if task.completed else "Active"
                        st.markdown(f"**{task.title}** ({status})")
                        st.write(f"Priority: {task.priority}")
                        
                        with st.expander("Details"):
                            st.write(f"**Description:** {task.description}")
                            st.write(f"**Created at:** {task.created_at}")
                    
                    with col2:
                        if st.button("View", key=f"view_{task.id}"):
                            st.session_state.task_to_view = task.id
                            st.experimental_rerun()
                    
                    st.divider()
    
    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            
            st.subheader(f"Task Details: {task.title}")
            st.write(f"**ID:** {task.id}")
            st.write(f"**Description:** {task.description}")
            st.write(f"**Priority:** {task.priority}")
            st.write(f"**Status:** {'Completed' if task.completed else 'Active'}")
            st.write(f"**Created at:** {task.created_at}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not task.completed and st.button("Mark as Complete"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col2:
                # BOUTON DE SUPPRESSION DANS LA VUE DÉTAILLÉE
                if st.button("🗑️", key=f"delete_detail_{task.id}"):
                    st.session_state[f"confirm_delete_detail_{task.id}"] = True
                    st.experimental_rerun()
            
            with col3:
                if st.button("Close"):
                    del st.session_state.task_to_view
                    st.experimental_rerun()
            
            # GESTION DE LA CONFIRMATION DE SUPPRESSION DANS LA VUE DÉTAILLÉE
            if st.session_state.get(f"confirm_delete_detail_{task.id}", False):
                st.warning(f"⚠️ Are you sure you want to delete the task: **{task.title}**?")
                
                confirm_col1, confirm_col2, confirm_col3 = st.columns([1, 1, 2])
                
                with confirm_col1:
                    if st.button("Yes, Delete", key=f"confirm_detail_yes_{task.id}", type="primary"):
                        try:
                            task_service.delete_task(task.id)
                            st.success(f"Task '{task.title}' deleted successfully!")
                            # NETTOYER L'ÉTAT APRÈS SUPPRESSION ET FERMER LA VUE DÉTAILLÉE
                            if f"confirm_delete_detail_{task.id}" in st.session_state:
                                del st.session_state[f"confirm_delete_detail_{task.id}"]
                            if hasattr(st.session_state, 'task_to_view'):
                                del st.session_state.task_to_view
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Error deleting task: {str(e)}")
                
                with confirm_col2:
                    if st.button("Cancel", key=f"confirm_detail_no_{task.id}"):
                        # ANNULER LA SUPPRESSION
                        del st.session_state[f"confirm_delete_detail_{task.id}"]
                        st.experimental_rerun()
                
        except TaskNotFoundException:
            st.error("Task not found")
            del st.session_state.task_to_view


if __name__ == "__main__":
    main()
