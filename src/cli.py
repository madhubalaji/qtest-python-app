#!/usr/bin/env python3
"""
Command-line interface for the task manager application.
"""

import argparse
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Task Manager - A CLI task management app")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description", default="")
    add_parser.add_argument(
        "-s", "--severity", 
        help="Task severity", 
        choices=["low", "medium", "high"], 
        default="medium"
    )

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "-a", "--all", 
        help="Show completed tasks as well", 
        action="store_true"
    )

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID to mark as complete")

    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Search tasks command
    search_parser = subparsers.add_parser("search", help="Search for tasks")
    search_parser.add_argument("keyword", help="Keyword to search for")

    # View task command
    view_parser = subparsers.add_parser("view", help="View task details")
    view_parser.add_argument("id", type=int, help="Task ID to view")

    args = parser.parse_args()
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)

    try:
        if args.command == "add":
            task = task_service.add_task(args.title, args.description, args.severity)
            print(f"Task '{task.title}' added successfully with ID {task.id}.")
            
        elif args.command == "list":
            tasks = task_service.get_all_tasks(show_completed=args.all)
            if not tasks:
                print("No tasks found.")
                return
                
            print("\n" + "=" * 60)
            print(f"{'ID':^5}|{'Title':^20}|{'Severity':^10}|{'Status':^10}|{'Created At':^20}")
            print("=" * 60)
            
            for task in tasks:
                status = "Completed" if task.completed else "Active"
                print(f"{task.id:^5}|{task.title[:18]:^20}|{task.severity:^10}|{status:^10}|{task.created_at:^20}")
            
            print("=" * 60 + "\n")
            
        elif args.command == "complete":
            task = task_service.complete_task(args.id)
            print(f"Task {task.id} marked as complete.")
            
        elif args.command == "delete":
            task = task_service.delete_task(args.id)
            print(f"Task '{task.title}' deleted successfully.")
            
        elif args.command == "search":
            results = task_service.search_tasks(args.keyword)
            
            if not results:
                print(f"No tasks found matching '{args.keyword}'.")
                return
                
            print(f"\nFound {len(results)} tasks matching '{args.keyword}':")
            print("=" * 60)
            print(f"{'ID':^5}|{'Title':^20}|{'Severity':^10}|{'Status':^10}")
            print("=" * 60)
            
            for task in results:
                status = "Completed" if task.completed else "Active"
                print(f"{task.id:^5}|{task.title[:18]:^20}|{task.severity:^10}|{status:^10}")
            
            print("=" * 60 + "\n")
            
        elif args.command == "view":
            task = task_service.get_task_by_id(args.id)
            print("\n" + "=" * 60)
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Severity: {task.severity}")
            print(f"Status: {'Completed' if task.completed else 'Active'}")
            print(f"Created at: {task.created_at}")
            print("=" * 60 + "\n")
            
        else:
            parser.print_help()
            
    except TaskNotFoundException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
