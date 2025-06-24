from bottle import route, template, static_file, redirect, request

from models.usuario import Usuario

@route('/static/<filepath:path>')
def server_static(filepath):
    # Quando alguém pedir um arquivo começando com /static/, procure-o dentro da pasta './static' no disco rígido.
    return static_file(filepath, root='./static')


@route('/')
def apresentacao():
    return template('views/apresentacao.html', nome="Visitante")

@route('/login', method=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.forms.get('email')
        senha = request.forms.get('senha')

        # 1. Tenta encontrar o usuário pelo email
        usuario = Usuario.find_by_email(email)

        # 2. Verifica se o usuário existe E se a senha está correta
        if usuario and usuario.check_password(senha):
            # Login bem-sucedido!
            # Renderiza a página home, passando o nome do usuário.
            return template('views/home.html', nome=usuario.nome)
        
        # 3. Se o usuário não existe ou a senha está errada, mostra erro.
        error_msg = "E-mail ou senha inválidos."
        return template('views/login.html', error=error_msg)

    # Se o método for GET, apenas mostra a página de login
    return template('views/login.html', error=None)


@route('/cadastro', method=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        # --- LÓGICA DE CRIAÇÃO DO USUÁRIO ---
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('senha')

        # 1. Verifica se o email já existe no banco de dados
        if Usuario.find_by_email(email):
            return template('views/cadastro.html', error="Este e-mail já está em uso.")

        # 2. Cria a instância do novo usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        
        # 3. Salva no banco de dados (o método .save() já faz o hash da senha)
        novo_usuario.save()

        # 4. Redireciona para a página de login após o sucesso
        return redirect('/login')
    
    # Se o método for GET, apenas mostra a página de cadastro normal
    return template('views/cadastro.html', error=None)