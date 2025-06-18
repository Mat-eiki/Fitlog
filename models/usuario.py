class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def get_primeiro_nome(self):
        return self.nome.split(' ')[0]