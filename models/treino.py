import sqlite3
from database import DB_NAME

class Exercicio:
    def __init__(self, nome, carga, id=None, treino_id=None):
        self.id = id
        self.nome = nome
        self.carga = carga
        self.treino_id = treino_id

    def save(self):
        """Salva um novo exercício na base de dados, associado a um treino."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exercicios (nome, carga, treino_id) VALUES (?, ?, ?)",
            (self.nome, self.carga, self.treino_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update(exercicio_id, novo_nome, nova_carga):
        """Atualiza o nome e a carga de um exercício específico."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE exercicios SET nome = ?, carga = ? WHERE id = ?",
            (novo_nome, nova_carga, exercicio_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(exercicio_id):
        """Deleta um exercício específico do banco de dados."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exercicios WHERE id = ?", (exercicio_id,))
        conn.commit()
        conn.close()

class Treino:
    def __init__(self, nome, usuario_id, id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id
        self.exercicios = []

    def save(self):
        """Salva um novo treino na base de dados."""
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
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE treinos SET nome = ? WHERE id = ?", (novo_nome, treino_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(treino_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exercicios WHERE treino_id = ?", (treino_id,))
        cursor.execute("DELETE FROM treinos WHERE id = ?", (treino_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_exercicios_by_treino_id(treino_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, carga FROM exercicios WHERE treino_id = ?", (treino_id,))
        exercicios_data = cursor.fetchall()
        conn.close()
        
        exercicios = []
        for ex_data in exercicios_data:
            exercicios.append(Exercicio(id=ex_data[0], nome=ex_data[1], carga=ex_data[2]))
        return exercicios