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
        page_title="タスクマネージャー",
        page_icon="✅",
        layout="wide"
    )
    
    st.title("タスクマネージャー")
    st.write("効率的にタスクを管理しましょう")
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Sidebar for navigation
    st.sidebar.title("ナビゲーション")
    page = st.sidebar.radio("ページを選択", ["タスク一覧", "タスク追加", "タスク検索"])
    
    if page == "タスク一覧":
        display_tasks_page(task_service)
    elif page == "タスク追加":
        add_task_page(task_service)
    elif page == "タスク検索":
        search_tasks_page(task_service)


def display_tasks_page(task_service):
    """Display the tasks page."""
    st.header("タスク一覧")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("完了済みタスクを表示", value=False)
    with col2:
        filter_priority = st.selectbox(
            "優先度でフィルター",
            ["すべて", "低", "中", "高"]
        )
    
    # Get tasks
    tasks = task_service.get_all_tasks(show_completed=True)
    
    # Apply filters
    if not show_completed:
        tasks = [task for task in tasks if not task.completed]
    
    # Map Japanese filter to English priority
    priority_map = {"すべて": "All", "低": "Low", "中": "Medium", "高": "High"}
    english_priority = priority_map.get(filter_priority, "All")
    
    if english_priority != "All":
        tasks = [task for task in tasks if task.priority.lower() == english_priority.lower()]
    
    if not tasks:
        st.info("条件に一致するタスクが見つかりません。")
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
                
                with st.expander("詳細"):
                    st.write(f"**説明:** {task.description}")
                    st.write(f"**作成日時:** {task.created_at}")
            
            with col2:
                priority_color = {
                    "low": "blue",
                    "medium": "orange",
                    "high": "red"
                }.get(task.priority.lower(), "gray")
                
                priority_japanese = {
                    "low": "低",
                    "medium": "中",
                    "high": "高"
                }.get(task.priority.lower(), task.priority)
                
                st.markdown(
                    f"<span style='color:{priority_color};font-weight:bold;'>{priority_japanese}</span>",
                    unsafe_allow_html=True
                )
            
            with col3:
                if not task.completed and st.button("✓", key=f"complete_{task.id}", help="完了にする"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col4:
                if st.button("🗑️", key=f"delete_{task.id}", help="削除"):
                    # Store the task ID to delete in session state for confirmation
                    st.session_state.task_to_delete = task.id
                    st.experimental_rerun()
            
            st.divider()
    
    # Handle delete confirmation
    if hasattr(st.session_state, 'task_to_delete'):
        task_to_delete = st.session_state.task_to_delete
        try:
            task = task_service.get_task_by_id(task_to_delete)
            
            st.warning(f"⚠️ タスク「{task.title}」を削除しますか？")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("削除する", key="confirm_delete", type="primary"):
                    try:
                        task_service.delete_task(task_to_delete)
                        st.success(f"タスク「{task.title}」を削除しました。")
                        del st.session_state.task_to_delete
                        st.experimental_rerun()
                    except TaskNotFoundException:
                        st.error("タスクが見つかりません。")
                        del st.session_state.task_to_delete
                        st.experimental_rerun()
            
            with col2:
                if st.button("キャンセル", key="cancel_delete"):
                    del st.session_state.task_to_delete
                    st.experimental_rerun()
                    
        except TaskNotFoundException:
            st.error("削除対象のタスクが見つかりません。")
            del st.session_state.task_to_delete
            st.experimental_rerun()


def add_task_page(task_service):
    """Display the add task page."""
    st.header("新しいタスクを追加")
    
    with st.form("add_task_form"):
        title = st.text_input("タイトル", max_chars=50)
        description = st.text_area("説明", max_chars=200)
        priority = st.select_slider(
            "優先度",
            options=["低", "中", "高"],
            value="中"
        )
        
        submitted = st.form_submit_button("タスクを追加")
        
        if submitted:
            if not title:
                st.error("タイトルは必須です")
            else:
                # Map Japanese priority to English
                priority_map = {"低": "low", "中": "medium", "高": "high"}
                english_priority = priority_map.get(priority, "medium")
                
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=english_priority
                )
                st.success(f"タスク「{title}」を追加しました（ID: {task.id}）")


def search_tasks_page(task_service):
    """Display the search tasks page."""
    st.header("タスク検索")
    
    keyword = st.text_input("タスクを検索", placeholder="キーワードを入力...")
    
    if keyword:
        results = task_service.search_tasks(keyword)
        
        if not results:
            st.info(f"「{keyword}」に一致するタスクが見つかりません")
        else:
            st.write(f"「{keyword}」に一致するタスクが{len(results)}件見つかりました:")
            
            for task in results:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        status = "完了済み" if task.completed else "進行中"
                        priority_japanese = {
                            "low": "低",
                            "medium": "中", 
                            "high": "高"
                        }.get(task.priority.lower(), task.priority)
                        
                        st.markdown(f"**{task.title}** ({status})")
                        st.write(f"優先度: {priority_japanese}")
                        
                        with st.expander("詳細"):
                            st.write(f"**説明:** {task.description}")
                            st.write(f"**作成日時:** {task.created_at}")
                    
                    with col2:
                        if st.button("詳細表示", key=f"view_{task.id}"):
                            st.session_state.task_to_view = task.id
                            st.experimental_rerun()
                    
                    st.divider()
    
    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            
            st.subheader(f"タスク詳細: {task.title}")
            st.write(f"**ID:** {task.id}")
            st.write(f"**説明:** {task.description}")
            
            priority_japanese = {
                "low": "低",
                "medium": "中",
                "high": "高"
            }.get(task.priority.lower(), task.priority)
            st.write(f"**優先度:** {priority_japanese}")
            
            st.write(f"**ステータス:** {'完了済み' if task.completed else '進行中'}")
            st.write(f"**作成日時:** {task.created_at}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not task.completed and st.button("完了にする"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col2:
                if st.button("削除", type="secondary"):
                    st.session_state.task_to_delete_from_detail = task.id
                    st.experimental_rerun()
            
            with col3:
                if st.button("閉じる"):
                    del st.session_state.task_to_view
                    st.experimental_rerun()
                
        except TaskNotFoundException:
            st.error("タスクが見つかりません")
            del st.session_state.task_to_view
    
    # Handle delete confirmation from task detail view
    if hasattr(st.session_state, 'task_to_delete_from_detail'):
        task_to_delete = st.session_state.task_to_delete_from_detail
        try:
            task = task_service.get_task_by_id(task_to_delete)
            
            st.warning(f"⚠️ タスク「{task.title}」を削除しますか？")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("削除する", key="confirm_delete_detail", type="primary"):
                    try:
                        task_service.delete_task(task_to_delete)
                        st.success(f"タスク「{task.title}」を削除しました。")
                        # Clean up session state
                        if hasattr(st.session_state, 'task_to_view'):
                            del st.session_state.task_to_view
                        del st.session_state.task_to_delete_from_detail
                        st.experimental_rerun()
                    except TaskNotFoundException:
                        st.error("タスクが見つかりません。")
                        del st.session_state.task_to_delete_from_detail
                        st.experimental_rerun()
            
            with col2:
                if st.button("キャンセル", key="cancel_delete_detail"):
                    del st.session_state.task_to_delete_from_detail
                    st.experimental_rerun()
                    
        except TaskNotFoundException:
            st.error("削除対象のタスクが見つかりません。")
            del st.session_state.task_to_delete_from_detail
            st.experimental_rerun()


if __name__ == "__main__":
    main()
