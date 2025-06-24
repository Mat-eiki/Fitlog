import sqlite3

# Define o nome do arquivo do banco de dados
DB_NAME = 'fitlog.db'

def create_tables():
    """
    Cria as tabelas necessárias no banco de dados se elas não existirem.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Cria a tabela de usuários
    # A estrutura já prevê futuras implementações (peso, altura, etc)
    # A senha será armazenada como um "hash" seguro, nunca como texto puro.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            peso REAL,
            altura REAL
        )
    ''')

    print("Tabela 'usuarios' criada com sucesso.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()