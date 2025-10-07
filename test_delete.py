#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de eliminar tareas.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Prueba la funcionalidad de eliminar tareas."""
    print("🧪 Probando funcionalidad de eliminar tareas...")
    
    # Initialize task service
    config_dir = os.path.join(".", "config")
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Show current tasks
    print("\n📋 Tareas actuales:")
    tasks = task_service.get_all_tasks()
    for task in tasks:
        status = "✅ Completada" if task.completed else "⏳ Pendiente"
        print(f"  ID: {task.id} | {task.title} | {status} | Prioridad: {task.priority}")
    
    if not tasks:
        print("  No hay tareas en el sistema.")
        # Create a test task
        print("\n➕ Creando tarea de prueba...")
        test_task = task_service.add_task(
            title="Tarea de Prueba para Eliminar",
            description="Esta es una tarea creada para probar la funcionalidad de eliminar",
            priority="high"
        )
        print(f"  ✅ Tarea creada con ID: {test_task.id}")
        
        # Show tasks again
        print("\n📋 Tareas después de crear:")
        tasks = task_service.get_all_tasks()
        for task in tasks:
            status = "✅ Completada" if task.completed else "⏳ Pendiente"
            print(f"  ID: {task.id} | {task.title} | {status} | Prioridad: {task.priority}")
    
    # Test delete functionality
    if tasks:
        task_to_delete = tasks[0]
        print(f"\n🗑️ Intentando eliminar tarea ID {task_to_delete.id}: '{task_to_delete.title}'")
        
        try:
            deleted_task = task_service.delete_task(task_to_delete.id)
            print(f"  ✅ Tarea eliminada exitosamente: '{deleted_task.title}'")
            
            # Verify deletion
            print("\n📋 Tareas después de eliminar:")
            remaining_tasks = task_service.get_all_tasks()
            if remaining_tasks:
                for task in remaining_tasks:
                    status = "✅ Completada" if task.completed else "⏳ Pendiente"
                    print(f"  ID: {task.id} | {task.title} | {status} | Prioridad: {task.priority}")
            else:
                print("  No quedan tareas en el sistema.")
                
        except TaskNotFoundException as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Prueba de funcionalidad de eliminar completada!")

if __name__ == "__main__":
    test_delete_functionality()