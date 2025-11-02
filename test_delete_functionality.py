#!/usr/bin/env python3
"""
MBSOURCE: 削除機能のテストスクリプト
Test script to verify the delete functionality works correctly.
"""

import os
import sys
import tempfile
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def test_delete_functionality():
    """Test the delete functionality of TaskService."""
    print("MBSOURCE: 削除機能のテストを開始します...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        # Create some test data
        test_data = [
            {
                "id": 1,
                "title": "Test Task 1",
                "description": "First test task",
                "priority": "high",
                "completed": False,
                "created_at": "2025-01-01 10:00:00"
            },
            {
                "id": 2,
                "title": "Test Task 2", 
                "description": "Second test task",
                "priority": "medium",
                "completed": True,
                "created_at": "2025-01-01 11:00:00"
            }
        ]
        
        json.dump(test_data, temp_file, indent=2)
        temp_file_path = temp_file.name
    
    try:
        # Initialize TaskService with the temporary file
        task_service = TaskService(temp_file_path)
        
        # Test 1: Verify initial tasks
        print("テスト 1: 初期タスクの確認")
        all_tasks = task_service.get_all_tasks()
        print(f"初期タスク数: {len(all_tasks)}")
        assert len(all_tasks) == 2, f"Expected 2 tasks, got {len(all_tasks)}"
        print("✓ 初期タスクの確認が成功しました")
        
        # Test 2: Delete an existing task
        print("\nテスト 2: 既存タスクの削除")
        deleted_task = task_service.delete_task(1)
        print(f"削除されたタスク: {deleted_task.title}")
        assert deleted_task.id == 1, f"Expected task ID 1, got {deleted_task.id}"
        
        # Verify task was deleted
        remaining_tasks = task_service.get_all_tasks()
        print(f"削除後のタスク数: {len(remaining_tasks)}")
        assert len(remaining_tasks) == 1, f"Expected 1 task remaining, got {len(remaining_tasks)}"
        assert remaining_tasks[0].id == 2, f"Expected remaining task ID 2, got {remaining_tasks[0].id}"
        print("✓ タスクの削除が成功しました")
        
        # Test 3: Try to delete non-existent task
        print("\nテスト 3: 存在しないタスクの削除")
        try:
            task_service.delete_task(999)
            assert False, "Expected TaskNotFoundException"
        except TaskNotFoundException as e:
            print(f"期待通りの例外が発生しました: {e}")
            print("✓ 存在しないタスクの削除テストが成功しました")
        
        # Test 4: Delete the last remaining task
        print("\nテスト 4: 最後のタスクの削除")
        task_service.delete_task(2)
        final_tasks = task_service.get_all_tasks()
        print(f"最終タスク数: {len(final_tasks)}")
        assert len(final_tasks) == 0, f"Expected 0 tasks, got {len(final_tasks)}"
        print("✓ 最後のタスクの削除が成功しました")
        
        print("\n🎉 すべてのテストが成功しました！削除機能は正常に動作しています。")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            print(f"テンポラリファイルを削除しました: {temp_file_path}")


if __name__ == "__main__":
    test_delete_functionality()