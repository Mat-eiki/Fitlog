import sqlite3
from database import DB_NAME

class Exercicio:
    def __init__(self, nome, carga, id=None, treino_id=None):
        self.id = id
        self.nome = nome
        self.carga = carga
        self.treino_id = treino_id

class Treino:
    # Este é o método que precisa ser corrigido.
    # Garanta que ele aceite 'id=None' e tenha a linha 'self.id = id'.
    def __init__(self, nome, usuario_id, id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id
        # Esta lista guardará os objetos de exercício do treino
        self.exercicios = []

    def save(self):
        """Salva um novo treino no banco de dados."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO treinos (nome, usuario_id) VALUES (?, ?)",
            (self.nome, self.usuario_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_nome(treino_id, novo_nome):
        """Atualiza o nome de um treino específico."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE treinos SET nome = ? WHERE id = ?", (novo_nome, treino_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(treino_id):
        """Deleta um treino e todos os seus exercícios associados."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exercicios WHERE treino_id = ?", (treino_id,))
        cursor.execute("DELETE FROM treinos WHERE id = ?", (treino_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_exercicios_by_treino_id(treino_id):
        """Busca todos os exercícios de um treino específico."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, carga FROM exercicios WHERE treino_id = ?", (treino_id,))
        exercicios_data = cursor.fetchall()
        conn.close()
        
        exercicios = []
        for ex_data in exercicios_data:
            exercicios.append(Exercicio(id=ex_data[0], nome=ex_data[1], carga=ex_data[2]))
        return exercicios