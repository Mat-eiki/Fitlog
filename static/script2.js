document.addEventListener('DOMContentLoaded', () => {

    // LÓGICA DO ACORDEÃO (ABRIR/FECHAR TREINOS)
    const workoutItems = document.querySelectorAll('.workout-item');
    workoutItems.forEach(item => {
        const header = item.querySelector('.workout-header');
        if (header) {
            header.addEventListener('click', (e) => {
                if (!e.target.closest('.workout-controls') && !e.target.closest('.inline-edit-form')) {
                    item.classList.toggle('active');
                }
            });
        }
    });

    // LÓGICA DO MODAL (ADICIONAR TREINO)
    const addWorkoutModal = document.getElementById('addWorkoutModal');
    const addWorkoutBtn = document.getElementById('addWorkoutBtn');
    const closeAddBtn = addWorkoutModal ? addWorkoutModal.querySelector('.close-btn') : null;
    if (addWorkoutBtn) {
        addWorkoutBtn.onclick = () => { if (addWorkoutModal) addWorkoutModal.style.display = "block"; };
    }
    if (closeAddBtn) {
        closeAddBtn.onclick = () => { if (addWorkoutModal) addWorkoutModal.style.display = "none"; };
    }

    // LÓGICA DO MODAL DE DELEÇÃO (GENÉRICO)
    const deleteModal = document.getElementById('deleteWorkoutModal');
    const confirmDeleteForm = document.getElementById('confirmDeleteForm');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    
    // Para deletar TREINOS
    document.querySelectorAll('.delete-workout-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const treinoId = btn.dataset.id;
            if (confirmDeleteForm) confirmDeleteForm.action = `/treinos/deletar/${treinoId}`;
            if (deleteModal) deleteModal.style.display = 'block';
        });
    });

    // Para deletar EXERCÍCIOS
    document.querySelectorAll('.delete-exercise-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const exercicioId = btn.dataset.id;
            if (confirmDeleteForm) confirmDeleteForm.action = `/exercicios/deletar/${exercicioId}`;
            if (deleteModal) deleteModal.style.display = 'block';
        });
    });

    if (cancelDeleteBtn) {
        cancelDeleteBtn.onclick = () => { if (deleteModal) deleteModal.style.display = 'none'; };
    }

    // LÓGICA PARA EDITAR NOME DO TREINO
    document.querySelectorAll('.edit-workout-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const header = btn.closest('.workout-header');
            const title = header.querySelector('.workout-title');
            const form = header.querySelector('.inline-edit-form');
            if(title) title.style.display = 'none';
            if(form) form.style.display = 'flex';
        });
    });

    // LÓGICA PARA EDITAR EXERCÍCIO
    document.querySelectorAll('.edit-exercise-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const item = btn.closest('.exercise-item');
            const displayDiv = item.querySelector('.exercise-display');
            const editForm = item.querySelector('.inline-exercise-edit-form');
            if (displayDiv) displayDiv.style.display = 'none';
            if (editForm) editForm.style.display = 'flex';
        });
    });

    // LÓGICA PARA FECHAR MODAIS CLICANDO FORA
    window.onclick = function(event) {
        if (event.target == addWorkoutModal) addWorkoutModal.style.display = "none";
        if (event.target == deleteModal) deleteModal.style.display = "none";
    }
});