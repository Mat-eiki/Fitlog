import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Importa o nome do banco de dados do nosso script de setup
from database import DB_NAME

class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def save(self):
        """
        Salva um novo usuário no banco de dados.
        O método lida com o hashing da senha.
        """
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Gera um hash seguro da senha antes de salvar
        senha_hash = generate_password_hash(self.senha)

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (self.nome, self.email, senha_hash)
        )
        
        conn.commit()
        conn.close()

    def check_password(self, senha_plana):
        """
        Verifica se a senha fornecida (plana) corresponde ao hash salvo.
        """
        return check_password_hash(self.senha, senha_plana)

    @staticmethod
    def find_by_email(email):
        """
        Busca um usuário pelo email. Útil para verificar se um email já existe.
        """
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Retorna um objeto Usuario se encontrar
            return Usuario(id=user_data[0], nome=user_data[1], email=user_data[2], senha=user_data[3])
        return None

    # Futuramente, você adicionaria os outros métodos do CRUD aqui:
    # def update(self): ...
    # def delete(self): ...
    # @staticmethod
    # def find_by_id(id): ...