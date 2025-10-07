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
        page_title="Gestionnaire de Tâches",
        page_icon="✅",
        layout="wide"
    )
    
    st.title("Gestionnaire de Tâches")
    st.write("Gérez vos tâches efficacement")
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller à", ["Voir les Tâches", "Ajouter une Tâche", "Rechercher des Tâches"])
    
    if page == "Voir les Tâches":
        display_tasks_page(task_service)
    elif page == "Ajouter une Tâche":
        add_task_page(task_service)
    elif page == "Rechercher des Tâches":
        search_tasks_page(task_service)


def display_tasks_page(task_service):
    """Display the tasks page."""
    st.header("Vos Tâches")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("Afficher les tâches terminées", value=False)
    with col2:
        filter_priority = st.selectbox(
            "Filtrer par priorité",
            ["Toutes", "Faible", "Moyenne", "Élevée"]
        )
    
    # Get tasks
    tasks = task_service.get_all_tasks(show_completed=True)
    
    # Apply filters
    if not show_completed:
        tasks = [task for task in tasks if not task.completed]
    
    if filter_priority != "Toutes":
        priority_mapping = {"Faible": "low", "Moyenne": "medium", "Élevée": "high"}
        tasks = [task for task in tasks if task.priority.lower() == priority_mapping.get(filter_priority, "").lower()]
    
    if not tasks:
        st.info("Aucune tâche trouvée correspondant à vos critères.")
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
                
                with st.expander("Détails"):
                    st.write(f"**Description:** {task.description}")
                    st.write(f"**Créé le:** {task.created_at}")
            
            with col2:
                priority_color = {
                    "low": "blue",
                    "medium": "orange", 
                    "high": "red"
                }.get(task.priority.lower(), "gray")
                
                priority_text = {
                    "low": "FAIBLE",
                    "medium": "MOYENNE",
                    "high": "ÉLEVÉE"
                }.get(task.priority.lower(), task.priority.upper())
                
                st.markdown(
                    f"<span style='color:{priority_color};font-weight:bold;'>{priority_text}</span>",
                    unsafe_allow_html=True
                )
            
            with col3:
                if not task.completed and st.button("✓", key=f"complete_{task.id}", help="Marquer comme terminé"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col4:
                # Gestion de la confirmation de suppression
                confirm_key = f"confirm_delete_{task.id}"
                if confirm_key in st.session_state and st.session_state[confirm_key]:
                    # Afficher les boutons de confirmation
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Oui", key=f"yes_delete_{task.id}", type="primary"):
                            try:
                                task_service.delete_task(task.id)
                                st.success(f"Tâche '{task.title}' supprimée avec succès")
                                # Nettoyer l'état de confirmation
                                if confirm_key in st.session_state:
                                    del st.session_state[confirm_key]
                                st.experimental_rerun()
                            except TaskNotFoundException:
                                st.error("Tâche introuvable")
                                if confirm_key in st.session_state:
                                    del st.session_state[confirm_key]
                    with col_no:
                        if st.button("Non", key=f"no_delete_{task.id}"):
                            # Annuler la confirmation
                            if confirm_key in st.session_state:
                                del st.session_state[confirm_key]
                            st.experimental_rerun()
                else:
                    # Bouton de suppression initial
                    if st.button("🗑️", key=f"delete_{task.id}", help="Supprimer la tâche"):
                        st.session_state[confirm_key] = True
                        st.experimental_rerun()
            
            st.divider()


def add_task_page(task_service):
    """Display the add task page."""
    st.header("Ajouter une Nouvelle Tâche")
    
    with st.form("add_task_form"):
        title = st.text_input("Titre", max_chars=50)
        description = st.text_area("Description", max_chars=200)
        priority = st.select_slider(
            "Priorité",
            options=["Faible", "Moyenne", "Élevée"],
            value="Moyenne"
        )
        
        submitted = st.form_submit_button("Ajouter la Tâche")
        
        if submitted:
            if not title:
                st.error("Le titre est obligatoire")
            else:
                priority_mapping = {"Faible": "low", "Moyenne": "medium", "Élevée": "high"}
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=priority_mapping[priority]
                )
                st.success(f"Tâche '{title}' ajoutée avec succès avec l'ID {task.id}")


def search_tasks_page(task_service):
    """Display the search tasks page."""
    st.header("Rechercher des Tâches")
    
    keyword = st.text_input("Rechercher des tâches", placeholder="Entrez un mot-clé...")
    
    if keyword:
        results = task_service.search_tasks(keyword)
        
        if not results:
            st.info(f"Aucune tâche trouvée correspondant à '{keyword}'")
        else:
            st.write(f"Trouvé {len(results)} tâche(s) correspondant à '{keyword}':")
            
            for task in results:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        status = "Terminée" if task.completed else "Active"
                        priority_text = {
                            "low": "Faible",
                            "medium": "Moyenne", 
                            "high": "Élevée"
                        }.get(task.priority.lower(), task.priority)
                        
                        st.markdown(f"**{task.title}** ({status})")
                        st.write(f"Priorité: {priority_text}")
                        
                        with st.expander("Détails"):
                            st.write(f"**Description:** {task.description}")
                            st.write(f"**Créé le:** {task.created_at}")
                    
                    with col2:
                        if st.button("Voir", key=f"view_{task.id}"):
                            st.session_state.task_to_view = task.id
                            st.experimental_rerun()
                    
                    st.divider()
    
    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            
            st.subheader(f"Détails de la Tâche: {task.title}")
            st.write(f"**ID:** {task.id}")
            st.write(f"**Description:** {task.description}")
            
            priority_text = {
                "low": "Faible",
                "medium": "Moyenne",
                "high": "Élevée"
            }.get(task.priority.lower(), task.priority)
            st.write(f"**Priorité:** {priority_text}")
            
            st.write(f"**Statut:** {'Terminée' if task.completed else 'Active'}")
            st.write(f"**Créé le:** {task.created_at}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not task.completed and st.button("Marquer comme Terminée"):
                    task_service.complete_task(task.id)
                    st.experimental_rerun()
            
            with col2:
                # Gestion de la suppression avec confirmation
                confirm_key = f"confirm_delete_detail_{task.id}"
                if confirm_key in st.session_state and st.session_state[confirm_key]:
                    # Mode confirmation
                    st.write("**Êtes-vous sûr de vouloir supprimer cette tâche ?**")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Oui, Supprimer", key=f"yes_delete_detail_{task.id}", type="primary"):
                            try:
                                task_title = task.title
                                task_service.delete_task(task.id)
                                st.success(f"Tâche '{task_title}' supprimée avec succès")
                                # Nettoyer les états de session
                                if confirm_key in st.session_state:
                                    del st.session_state[confirm_key]
                                if hasattr(st.session_state, 'task_to_view'):
                                    del st.session_state.task_to_view
                                st.experimental_rerun()
                            except TaskNotFoundException:
                                st.error("Tâche introuvable")
                                if confirm_key in st.session_state:
                                    del st.session_state[confirm_key]
                    with col_no:
                        if st.button("Annuler", key=f"no_delete_detail_{task.id}"):
                            if confirm_key in st.session_state:
                                del st.session_state[confirm_key]
                            st.experimental_rerun()
                else:
                    # Bouton de suppression initial
                    if st.button("Supprimer la Tâche", key=f"delete_detail_{task.id}"):
                        st.session_state[confirm_key] = True
                        st.experimental_rerun()
            
            with col3:
                if st.button("Fermer"):
                    del st.session_state.task_to_view
                    st.experimental_rerun()
                
        except TaskNotFoundException:
            st.error("Tâche introuvable")
            del st.session_state.task_to_view


if __name__ == "__main__":
    main()
