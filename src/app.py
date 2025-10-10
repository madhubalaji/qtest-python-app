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
        page_title="कार्य प्रबंधक",  # Task Manager in Hindi
        page_icon="✅",
        layout="wide"
    )
    
    st.title("कार्य प्रबंधक")  # Task Manager in Hindi
    st.write("अपने कार्यों को कुशलतापूर्वक प्रबंधित करें")  # Manage your tasks efficiently in Hindi
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Sidebar for navigation
    st.sidebar.title("नेवीगेशन")  # Navigation in Hindi
    page = st.sidebar.radio("जाएं", ["कार्य देखें", "कार्य जोड़ें", "कार्य खोजें"])  # Go to, View Tasks, Add Task, Search Tasks in Hindi
    
    if page == "कार्य देखें":  # View Tasks in Hindi
        display_tasks_page(task_service)
    elif page == "कार्य जोड़ें":  # Add Task in Hindi
        add_task_page(task_service)
    elif page == "कार्य खोजें":  # Search Tasks in Hindi
        search_tasks_page(task_service)


def display_tasks_page(task_service):
    """Display the tasks page."""
    st.header("आपके कार्य")  # Your Tasks in Hindi
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("पूर्ण कार्य दिखाएं", value=False)  # Show completed tasks in Hindi
    with col2:
        filter_priority = st.selectbox(
            "प्राथमिकता के अनुसार फ़िल्टर करें",  # Filter by priority in Hindi
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
        st.info("आपके मानदंडों से मेल खाने वाले कोई कार्य नहीं मिले।")  # No tasks found matching your criteria in Hindi
        return
    
    # Display tasks
    for task in tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                if task.completed:
                    st.markdown(f"~~**{task.title}**~~")
                else:
                    st.markdown(f"**{task.title}**")
                
                with st.expander("विवरण"):  # Details in Hindi
                    st.write(f"**विवरण:** {task.description}")  # Description in Hindi
                    st.write(f"**बनाया गया:** {task.created_at}")  # Created at in Hindi
            
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
                if not task.completed and st.button("✓", key=f"complete_{task.id}"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col4:
                # Delete confirmation logic
                if f"confirm_delete_{task.id}" in st.session_state:
                    # Show confirmation buttons
                    col4a, col4b = st.columns(2)
                    with col4a:
                        if st.button("हाँ", key=f"yes_delete_{task.id}"):  # Yes in Hindi
                            try:
                                task_service.delete_task(task.id)
                                st.success(f"कार्य '{task.title}' सफलतापूर्वक हटा दिया गया")  # Task deleted successfully in Hindi
                                if f"confirm_delete_{task.id}" in st.session_state:
                                    del st.session_state[f"confirm_delete_{task.id}"]
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"कार्य हटाने में त्रुटि: {str(e)}")  # Error deleting task in Hindi
                    with col4b:
                        if st.button("नहीं", key=f"no_delete_{task.id}"):  # No in Hindi
                            del st.session_state[f"confirm_delete_{task.id}"]
                            st.experimental_rerun()
                else:
                    # Show delete button
                    if st.button("🗑️", key=f"delete_{task.id}", help="कार्य हटाएं"):  # Delete task in Hindi
                        st.session_state[f"confirm_delete_{task.id}"] = True
                        st.experimental_rerun()
            
            st.divider()


def add_task_page(task_service):
    """Display the add task page."""
    st.header("नया कार्य जोड़ें")  # Add New Task in Hindi
    
    with st.form("add_task_form"):
        title = st.text_input("शीर्षक", max_chars=50)  # Title in Hindi
        description = st.text_area("विवरण", max_chars=200)  # Description in Hindi
        priority = st.select_slider(
            "प्राथमिकता",  # Priority in Hindi
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        submitted = st.form_submit_button("कार्य जोड़ें")  # Add Task in Hindi
        
        if submitted:
            if not title:
                st.error("शीर्षक आवश्यक है")  # Title is required in Hindi
            else:
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=priority.lower()
                )
                st.success(f"कार्य '{title}' सफलतापूर्वक जोड़ा गया, आईडी {task.id}")  # Task added successfully in Hindi


def search_tasks_page(task_service):
    """Display the search tasks page."""
    st.header("कार्य खोजें")  # Search Tasks in Hindi
    
    keyword = st.text_input("कार्यों की खोज करें", placeholder="कीवर्ड दर्ज करें...")  # Search for tasks, Enter keyword in Hindi
    
    if keyword:
        results = task_service.search_tasks(keyword)
        
        if not results:
            st.info(f"'{keyword}' से मेल खाने वाले कोई कार्य नहीं मिले")  # No tasks found matching in Hindi
        else:
            st.write(f"'{keyword}' से मेल खाने वाले {len(results)} कार्य मिले:")  # Found X tasks matching in Hindi
            
            for task in results:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        status = "पूर्ण" if task.completed else "सक्रिय"  # Completed/Active in Hindi
                        st.markdown(f"**{task.title}** ({status})")
                        st.write(f"प्राथमिकता: {task.priority}")  # Priority in Hindi
                        
                        with st.expander("विवरण"):  # Details in Hindi
                            st.write(f"**विवरण:** {task.description}")  # Description in Hindi
                            st.write(f"**बनाया गया:** {task.created_at}")  # Created at in Hindi
                    
                    with col2:
                        if st.button("देखें", key=f"view_{task.id}"):  # View in Hindi
                            st.session_state.task_to_view = task.id
                            st.experimental_rerun()
                    
                    with col3:
                        # Delete confirmation logic for search results
                        if f"confirm_delete_search_{task.id}" in st.session_state:
                            # Show confirmation buttons
                            col3a, col3b = st.columns(2)
                            with col3a:
                                if st.button("हाँ", key=f"yes_delete_search_{task.id}"):  # Yes in Hindi
                                    try:
                                        task_service.delete_task(task.id)
                                        st.success(f"कार्य '{task.title}' सफलतापूर्वक हटा दिया गया")  # Task deleted successfully in Hindi
                                        if f"confirm_delete_search_{task.id}" in st.session_state:
                                            del st.session_state[f"confirm_delete_search_{task.id}"]
                                        st.experimental_rerun()
                                    except Exception as e:
                                        st.error(f"कार्य हटाने में त्रुटि: {str(e)}")  # Error deleting task in Hindi
                            with col3b:
                                if st.button("नहीं", key=f"no_delete_search_{task.id}"):  # No in Hindi
                                    del st.session_state[f"confirm_delete_search_{task.id}"]
                                    st.experimental_rerun()
                        else:
                            # Show delete button
                            if st.button("🗑️", key=f"delete_search_{task.id}", help="कार्य हटाएं"):  # Delete task in Hindi
                                st.session_state[f"confirm_delete_search_{task.id}"] = True
                                st.experimental_rerun()
                    
                    st.divider()
    
    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            
            st.subheader(f"कार्य विवरण: {task.title}")  # Task Details in Hindi
            st.write(f"**आईडी:** {task.id}")  # ID in Hindi
            st.write(f"**विवरण:** {task.description}")  # Description in Hindi
            st.write(f"**प्राथमिकता:** {task.priority}")  # Priority in Hindi
            st.write(f"**स्थिति:** {'पूर्ण' if task.completed else 'सक्रिय'}")  # Status in Hindi
            st.write(f"**बनाया गया:** {task.created_at}")  # Created at in Hindi
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not task.completed and st.button("पूर्ण के रूप में चिह्नित करें"):  # Mark as Complete in Hindi
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col2:
                # Delete confirmation logic for task details
                if f"confirm_delete_detail_{task.id}" in st.session_state:
                    # Show confirmation message and buttons
                    st.warning("क्या आप वाकई इस कार्य को हटाना चाहते हैं?")  # Are you sure you want to delete this task? in Hindi
                    col2a, col2b = st.columns(2)
                    with col2a:
                        if st.button("हाँ, हटाएं", key=f"yes_delete_detail_{task.id}"):  # Yes, Delete in Hindi
                            try:
                                task_service.delete_task(task.id)
                                st.success(f"कार्य '{task.title}' सफलतापूर्वक हटा दिया गया")  # Task deleted successfully in Hindi
                                if f"confirm_delete_detail_{task.id}" in st.session_state:
                                    del st.session_state[f"confirm_delete_detail_{task.id}"]
                                if hasattr(st.session_state, 'task_to_view'):
                                    del st.session_state.task_to_view
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"कार्य हटाने में त्रुटि: {str(e)}")  # Error deleting task in Hindi
                    with col2b:
                        if st.button("रद्द करें", key=f"cancel_delete_detail_{task.id}"):  # Cancel in Hindi
                            del st.session_state[f"confirm_delete_detail_{task.id}"]
                            st.experimental_rerun()
                else:
                    if st.button("कार्य हटाएं"):  # Delete Task in Hindi
                        st.session_state[f"confirm_delete_detail_{task.id}"] = True
                        st.experimental_rerun()
            
            with col3:
                if st.button("बंद करें"):  # Close in Hindi
                    del st.session_state.task_to_view
                    st.experimental_rerun()
                
        except TaskNotFoundException:
            st.error("कार्य नहीं मिला")  # Task not found in Hindi
            del st.session_state.task_to_view


if __name__ == "__main__":
    main()
