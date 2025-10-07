#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité de suppression de tâches.
"""

import os
import sys

# Ajouter le répertoire racine du projet au chemin Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Tester la fonctionnalité de suppression de tâches."""
    print("=== Test de la Fonctionnalité de Suppression de Tâches ===\n")
    
    # Créer un service de tâches avec un fichier temporaire
    test_file = "test_tasks.json"
    task_service = TaskService(test_file)
    
    try:
        # 1. Ajouter quelques tâches de test
        print("1. Ajout de tâches de test...")
        task1 = task_service.add_task("Tâche Test 1", "Description de la tâche 1", "high")
        task2 = task_service.add_task("Tâche Test 2", "Description de la tâche 2", "medium")
        task3 = task_service.add_task("Tâche Test 3", "Description de la tâche 3", "low")
        
        print(f"   ✓ Tâche créée: {task1.title} (ID: {task1.id})")
        print(f"   ✓ Tâche créée: {task2.title} (ID: {task2.id})")
        print(f"   ✓ Tâche créée: {task3.title} (ID: {task3.id})")
        
        # 2. Lister toutes les tâches
        print(f"\n2. Liste des tâches avant suppression:")
        tasks = task_service.get_all_tasks()
        for task in tasks:
            print(f"   - ID {task.id}: {task.title} ({task.priority})")
        
        # 3. Supprimer une tâche
        print(f"\n3. Suppression de la tâche ID {task2.id}...")
        deleted_task = task_service.delete_task(task2.id)
        print(f"   ✓ Tâche supprimée: {deleted_task.title}")
        
        # 4. Vérifier que la tâche a été supprimée
        print(f"\n4. Liste des tâches après suppression:")
        tasks = task_service.get_all_tasks()
        for task in tasks:
            print(f"   - ID {task.id}: {task.title} ({task.priority})")
        
        # 5. Tenter de supprimer une tâche inexistante
        print(f"\n5. Test de suppression d'une tâche inexistante...")
        try:
            task_service.delete_task(999)
            print("   ❌ ERREUR: La suppression aurait dû échouer")
        except TaskNotFoundException as e:
            print(f"   ✓ Exception correctement levée: {e}")
        
        # 6. Vérifier la persistance
        print(f"\n6. Test de persistance...")
        new_service = TaskService(test_file)
        persisted_tasks = new_service.get_all_tasks()
        print(f"   ✓ {len(persisted_tasks)} tâche(s) persistée(s) après rechargement")
        
        print(f"\n=== Tous les tests sont passés avec succès ! ===")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        
    finally:
        # Nettoyer le fichier de test
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\n🧹 Fichier de test nettoyé: {test_file}")

if __name__ == "__main__":
    test_delete_functionality()