"""
Streamlit web application for the task manager.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
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
    page = st.sidebar.radio("移動先", ["タスク表示", "タスク追加", "タスク検索", "タスク削除"])

    if page == "タスク表示":
        display_tasks_page(task_service)
    elif page == "タスク追加":
        add_task_page(task_service)
    elif page == "タスク検索":
        search_tasks_page(task_service)
    elif page == "タスク削除":
        delete_tasks_page(task_service)


def _get_filtered_tasks(task_service, show_completed, filter_priority):
    """Get tasks with applied filters."""
    tasks = task_service.get_all_tasks(show_completed=True)

    if not show_completed:
        tasks = [task for task in tasks if not task.completed]

    if filter_priority != "全て":
        priority_map = {"低": "low", "中": "medium", "高": "high"}
        tasks = [task for task in tasks if task.priority.lower() == priority_map[filter_priority]]

    return tasks


def _render_task_filters():
    """Render task filter controls."""
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("完了したタスクを表示", value=False)
    with col2:
        filter_priority = st.selectbox(
            "優先度でフィルター",
            ["全て", "低", "中", "高"]
        )
    return show_completed, filter_priority


def _handle_task_deletion(task, task_service):
    """Handle task deletion with confirmation."""
    if st.button("🗑️", key=f"delete_{task.id}", help="タスクを削除"):
        st.session_state[f"confirm_delete_{task.id}"] = True
        st.experimental_rerun()

    if st.session_state.get(f"confirm_delete_{task.id}", False):
        st.warning(f"タスク '{task.title}' を削除しますか？")
        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("はい", key=f"confirm_yes_{task.id}"):
                task_service.delete_task(task.id)
                if f"confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"confirm_delete_{task.id}"]
                st.success(f"タスク '{task.title}' を削除しました")
                st.experimental_rerun()

        with col_no:
            if st.button("いいえ", key=f"confirm_no_{task.id}"):
                if f"confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"confirm_delete_{task.id}"]
                st.experimental_rerun()


def _render_single_task(task, task_service):
    """Render a single task with all its controls."""
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

        st.markdown(
            f"<span style='color:{priority_color};font-weight:bold;'>{task.priority.upper()}</span>",
            unsafe_allow_html=True
        )

    with col3:
        if not task.completed and st.button("✓", key=f"complete_{task.id}"):
            task_service.complete_task(task.id)
            st.experimental_rerun()

    with col4:
        _handle_task_deletion(task, task_service)


def display_tasks_page(task_service):
    """タスク表示ページを表示します。"""
    st.header("あなたのタスク")

    # フィルターオプション
    show_completed, filter_priority = _render_task_filters()

    # タスクを取得
    tasks = _get_filtered_tasks(task_service, show_completed, filter_priority)

    if not tasks:
        st.info("条件に一致するタスクが見つかりません。")
        return

    # Display tasks
    for task in tasks:
        with st.container():
            _render_single_task(task, task_service)
            st.divider()


def add_task_page(task_service):
    """タスク追加ページを表示します。"""
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
                priority_map = {"低": "low", "中": "medium", "高": "high"}
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=priority_map[priority]
                )
                st.success(f"タスク '{title}' をID {task.id}で正常に追加しました")


def _handle_search_task_deletion(task, task_service):
    """Handle task deletion in search results."""
    if st.button("🗑️", key=f"search_delete_{task.id}", help="タスクを削除"):
        st.session_state[f"search_confirm_delete_{task.id}"] = True
        st.experimental_rerun()

    if st.session_state.get(f"search_confirm_delete_{task.id}", False):
        st.warning(f"タスク '{task.title}' を削除しますか？")
        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("はい", key=f"search_confirm_yes_{task.id}"):
                task_service.delete_task(task.id)
                if f"search_confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"search_confirm_delete_{task.id}"]
                st.success(f"タスク '{task.title}' を削除しました")
                st.experimental_rerun()

        with col_no:
            if st.button("いいえ", key=f"search_confirm_no_{task.id}"):
                if f"search_confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"search_confirm_delete_{task.id}"]
                st.experimental_rerun()


def _render_search_result(task, task_service):
    """Render a single search result."""
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        status = "完了" if task.completed else "アクティブ"
        st.markdown(f"**{task.title}** ({status})")
        st.write(f"優先度: {task.priority}")

        with st.expander("詳細"):
            st.write(f"**説明:** {task.description}")
            st.write(f"**作成日時:** {task.created_at}")

    with col2:
        if st.button("表示", key=f"view_{task.id}"):
            st.session_state.task_to_view = task.id
            st.experimental_rerun()

    with col3:
        _handle_search_task_deletion(task, task_service)


def _handle_task_detail_deletion(task, task_service):
    """Handle task deletion from detail view."""
    if st.button("削除", key=f"detail_delete_{task.id}"):
        st.session_state[f"detail_confirm_delete_{task.id}"] = True
        st.experimental_rerun()

    if st.session_state.get(f"detail_confirm_delete_{task.id}", False):
        st.warning(f"タスク '{task.title}' を削除しますか？")
        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("はい", key=f"detail_confirm_yes_{task.id}"):
                task_service.delete_task(task.id)
                if f"detail_confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"detail_confirm_delete_{task.id}"]
                if hasattr(st.session_state, 'task_to_view'):
                    del st.session_state.task_to_view
                st.success(f"タスク '{task.title}' を削除しました")
                st.experimental_rerun()

        with col_no:
            if st.button("いいえ", key=f"detail_confirm_no_{task.id}"):
                if f"detail_confirm_delete_{task.id}" in st.session_state:
                    del st.session_state[f"detail_confirm_delete_{task.id}"]
                st.experimental_rerun()


def _render_task_details(task, task_service):
    """Render detailed task view."""
    st.subheader(f"タスク詳細: {task.title}")
    st.write(f"**ID:** {task.id}")
    st.write(f"**説明:** {task.description}")
    st.write(f"**優先度:** {task.priority}")
    st.write(f"**ステータス:** {'完了' if task.completed else 'アクティブ'}")
    st.write(f"**作成日時:** {task.created_at}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if not task.completed and st.button("完了にする"):
            task_service.complete_task(task.id)
            st.experimental_rerun()

    with col2:
        _handle_task_detail_deletion(task, task_service)

    with col3:
        if st.button("閉じる"):
            del st.session_state.task_to_view
            st.experimental_rerun()


def search_tasks_page(task_service):
    """タスク検索ページを表示します。"""
    st.header("タスク検索")

    keyword = st.text_input("タスクを検索", placeholder="キーワードを入力...")

    if keyword:
        results = task_service.search_tasks(keyword)

        if not results:
            st.info(f"'{keyword}' に一致するタスクが見つかりません")
        else:
            st.write(f"'{keyword}' に一致する {len(results)} 個のタスクが見つかりました：")

            for task in results:
                with st.container():
                    _render_search_result(task, task_service)
                    st.divider()

    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            _render_task_details(task, task_service)

        except TaskNotFoundException:
            st.error("タスクが見つかりません")
            del st.session_state.task_to_view


def _handle_bulk_delete_confirmation(selected_tasks, task_service):
    """Handle bulk delete confirmation dialog."""
    if st.button("選択したタスクを削除", type="primary"):
        st.session_state.confirm_bulk_delete = True
        st.experimental_rerun()

    if st.session_state.get("confirm_bulk_delete", False):
        st.warning(f"{len(selected_tasks)}個のタスクを削除しますか？この操作は取り消せません。")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("はい、削除します", key="bulk_delete_confirm"):
                deleted_count = 0
                deleted_titles = []

                for task in selected_tasks:
                    try:
                        task_service.delete_task(task.id)
                        deleted_count += 1
                        deleted_titles.append(task.title)
                    except TaskNotFoundException:
                        st.warning(f"タスク '{task.title}' は既に削除されています。")

                if "confirm_bulk_delete" in st.session_state:
                    del st.session_state.confirm_bulk_delete

                if deleted_count > 0:
                    st.success(f"{deleted_count}個のタスクを削除しました。")
                    with st.expander("削除されたタスク"):
                        for title in deleted_titles:
                            st.write(f"- {title}")

                st.experimental_rerun()

        with col2:
            if st.button("キャンセル", key="bulk_delete_cancel"):
                if "confirm_bulk_delete" in st.session_state:
                    del st.session_state.confirm_bulk_delete
                st.experimental_rerun()


def _handle_delete_all_confirmation(all_tasks, task_service):
    """Handle delete all confirmation dialog."""
    if st.button("全てのタスクを削除", type="secondary"):
        st.session_state.confirm_delete_all = True
        st.experimental_rerun()

    if st.session_state.get("confirm_delete_all", False):
        st.error("本当に全てのタスクを削除しますか？この操作は取り消せません。")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("はい、全て削除します", key="delete_all_confirm"):
                deleted_count = len(all_tasks)
                for task in all_tasks:
                    try:
                        task_service.delete_task(task.id)
                    except TaskNotFoundException:
                        pass

                if "confirm_delete_all" in st.session_state:
                    del st.session_state.confirm_delete_all

                st.success(f"全ての{deleted_count}個のタスクを削除しました。")
                st.experimental_rerun()

        with col2:
            if st.button("キャンセル", key="delete_all_cancel"):
                if "confirm_delete_all" in st.session_state:
                    del st.session_state.confirm_delete_all
                st.experimental_rerun()


def delete_tasks_page(task_service):
    """タスク削除ページを表示します。"""
    st.header("タスク削除")

    # 全タスクを取得
    all_tasks = task_service.get_all_tasks(show_completed=True)

    if not all_tasks:
        st.info("削除可能なタスクがありません。")
        return

    st.write("削除したいタスクを選択してください：")

    # タスク選択用のチェックボックス
    selected_tasks = []

    for task in all_tasks:
        status = "完了" if task.completed else "アクティブ"
        task_label = f"{task.title} ({status}) - 優先度: {task.priority}"

        if st.checkbox(task_label, key=f"select_delete_{task.id}"):
            selected_tasks.append(task)

    if selected_tasks:
        st.write(f"選択されたタスク数: {len(selected_tasks)}")
        _handle_bulk_delete_confirmation(selected_tasks, task_service)

    # 全タスク削除オプション
    st.divider()
    st.subheader("全タスク削除")
    st.warning("⚠️ 危険: この操作は全てのタスクを削除します")
    _handle_delete_all_confirmation(all_tasks, task_service)


if __name__ == "__main__":
    main()
