import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import DB_NAME
from models.treino import Treino # Certifique-se que esta linha está presente

class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def save(self):
        """Salva um novo usuário no banco de dados."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        senha_hash = generate_password_hash(self.senha)
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (self.nome, self.email, senha_hash)
        )
        conn.commit()
        conn.close()

    def check_password(self, senha_plana):
        """Verifica se a senha fornecida (plana) corresponde ao hash salvo."""
        return check_password_hash(self.senha, senha_plana)

    @staticmethod
    def find_by_email(email):
        """
        Busca um usuário pelo email. Este é o método que estava faltando.
        """
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return Usuario(id=user_data[0], nome=user_data[1], email=user_data[2], senha=user_data[3])
        return None

    @staticmethod
    def find_by_id(user_id):
        """Busca um usuário pelo seu ID."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return Usuario(id=user_data[0], nome=user_data[1], email=user_data[2], senha=user_data[3])
        return None

    def get_treinos(self):
        """Busca todos os treinos associados a este usuário."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM treinos WHERE usuario_id = ?", (self.id,))
        treinos_data = cursor.fetchall()
        conn.close()
        
        lista_de_treinos = []
        for treino_data in treinos_data:
            treino = Treino(id=treino_data[0], nome=treino_data[1], usuario_id=self.id)
            treino.exercicios = Treino.get_exercicios_by_treino_id(treino.id)
            lista_de_treinos.append(treino)
        
        return lista_de_treinos