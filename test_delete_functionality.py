#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de eliminar tareas.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Prueba la funcionalidad de eliminar tareas."""
    print("🧪 Iniciando pruebas de funcionalidad de eliminar tareas...")
    
    # Crear un archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_storage = temp_file.name
    
    try:
        # Inicializar el servicio de tareas
        task_service = TaskService(temp_storage)
        
        # Agregar algunas tareas de prueba
        print("\n📝 Agregando tareas de prueba...")
        task1 = task_service.add_task("Tarea de prueba 1", "Descripción 1", "high")
        task2 = task_service.add_task("Tarea de prueba 2", "Descripción 2", "medium")
        task3 = task_service.add_task("Tarea de prueba 3", "Descripción 3", "low")
        
        print(f"✅ Agregadas 3 tareas: IDs {task1.id}, {task2.id}, {task3.id}")
        
        # Verificar que las tareas existen
        all_tasks = task_service.get_all_tasks()
        print(f"📊 Total de tareas antes de eliminar: {len(all_tasks)}")
        
        # Eliminar una tarea
        print(f"\n🗑️ Eliminando tarea con ID {task2.id}...")
        deleted_task = task_service.delete_task(task2.id)
        print(f"✅ Tarea eliminada: '{deleted_task.title}'")
        
        # Verificar que la tarea fue eliminada
        remaining_tasks = task_service.get_all_tasks()
        print(f"📊 Total de tareas después de eliminar: {len(remaining_tasks)}")
        
        # Verificar que no podemos obtener la tarea eliminada
        print(f"\n🔍 Intentando obtener la tarea eliminada (ID {task2.id})...")
        try:
            task_service.get_task_by_id(task2.id)
            print("❌ ERROR: La tarea eliminada aún existe!")
            return False
        except TaskNotFoundException:
            print("✅ Correcto: La tarea eliminada no se puede encontrar")
        
        # Verificar que las otras tareas siguen existiendo
        print(f"\n🔍 Verificando que las otras tareas siguen existiendo...")
        try:
            remaining_task1 = task_service.get_task_by_id(task1.id)
            remaining_task3 = task_service.get_task_by_id(task3.id)
            print(f"✅ Tarea {task1.id} existe: '{remaining_task1.title}'")
            print(f"✅ Tarea {task3.id} existe: '{remaining_task3.title}'")
        except TaskNotFoundException as e:
            print(f"❌ ERROR: Una tarea que debería existir no se encontró: {e}")
            return False
        
        # Intentar eliminar una tarea que no existe
        print(f"\n🔍 Intentando eliminar una tarea inexistente (ID 999)...")
        try:
            task_service.delete_task(999)
            print("❌ ERROR: Se pudo eliminar una tarea inexistente!")
            return False
        except TaskNotFoundException:
            print("✅ Correcto: No se puede eliminar una tarea inexistente")
        
        print("\n🎉 ¡Todas las pruebas de funcionalidad de eliminar tareas pasaron exitosamente!")
        return True
        
    finally:
        # Limpiar el archivo temporal
        if os.path.exists(temp_storage):
            os.unlink(temp_storage)
            print(f"🧹 Archivo temporal limpiado: {temp_storage}")

if __name__ == "__main__":
    success = test_delete_functionality()
    sys.exit(0 if success else 1)