// Garante que o código só rode depois que a página carregar completamente
document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA DO ACORDEÃO (ABRIR/FECHAR TREINOS) ---
    const workoutItems = document.querySelectorAll('.workout-item');

    workoutItems.forEach(item => {
        const header = item.querySelector('.workout-header');
        header.addEventListener('click', () => {
            // Alterna a classe 'active' no item de treino clicado
            item.classList.toggle('active');
        });
    });


    // --- LÓGICA DO MODAL (JANELA PARA ADICIONAR TREINO) ---
    const modal = document.getElementById('addWorkoutModal');
    const addBtn = document.getElementById('addWorkoutBtn');
    const closeBtn = document.querySelector('.close-btn');

    // Abre o modal quando o botão '+' é clicado
    if (addBtn) {
        addBtn.onclick = function() {
            modal.style.display = "block";
        }
    }

    // Fecha o modal quando o 'x' é clicado
    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Fecha o modal se o usuário clicar fora da caixa do modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

});

// Função antiga para o botão 'Saiba Mais' da página de apresentação
function rolarParaConteudo() {
  const secao = document.getElementById('conteudo');
  if(secao) { // Verifica se o elemento existe antes de rolar
    secao.scrollIntoView({ behavior: 'smooth' });
  }
}

document.addEventListener('DOMContentLoaded', () => {

    // ... (código do acordeão e do modal de adicionar treino sem alterações) ...


    // --- LÓGICA PARA DELETAR TREINO (ABRIR MODAL DE CONFIRMAÇÃO) ---
    const deleteModal = document.getElementById('deleteWorkoutModal');
    const deleteBtns = document.querySelectorAll('.delete-workout-btn');
    const confirmDeleteForm = document.getElementById('confirmDeleteForm');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

    deleteBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Impede que o acordeão abra/feche ao clicar no X
            const treinoId = btn.dataset.id; // Pega o ID do data-id
            // Define a ação do formulário do modal para a URL correta
            confirmDeleteForm.action = `/treinos/deletar/${treinoId}`;
            deleteModal.style.display = 'block'; // Mostra o modal
        });
    });

    // Fecha o modal de deleção se clicar em "Cancelar"
    if(cancelDeleteBtn) {
        cancelDeleteBtn.onclick = function() {
            deleteModal.style.display = 'none';
        }
    }
    
    const editBtns = document.querySelectorAll('.edit-workout-btn');

    editBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Impede que o acordeão abra/feche
            const header = btn.closest('.workout-header');
            const title = header.querySelector('.workout-title');
            const form = header.querySelector('.inline-edit-form');
            
            // Alterna a visibilidade: esconde o título e mostra o formulário
            title.style.display = 'none';
            form.style.display = 'flex';
        });
    });

});