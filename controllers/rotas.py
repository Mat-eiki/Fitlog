from bottle import route, template, static_file, redirect, request, response

from models.usuario import Usuario
from models.treino import Treino

# Rota para servir arquivos estáticos (CSS, JS, Imagens)
@route('/static/<filepath:path>')
def server_static(filepath):
    """
    Esta rota é responsável por servir todos os arquivos estáticos
    (CSS, JavaScript, Imagens) da pasta /static.
    """
    return static_file(filepath, root='./static')

@route('/cadastro', method=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('senha')

        if Usuario.find_by_email(email):
            return template('views/cadastro.html', error="Este e-mail já está em uso.")

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        novo_usuario.save()
        return redirect('/login')
    
    return template('views/cadastro.html', error=None)


@route('/login', method=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.forms.get('email')
        senha = request.forms.get('senha')
        
        usuario = Usuario.find_by_email(email)

        if usuario and usuario.check_password(senha):
            s = request.environ.get('beaker.session')
            s['user_id'] = usuario.id
            s.save()
            return redirect('/home')
        
        error_msg = "E-mail ou senha inválidos."
        return template('views/login.html', error=error_msg)

    return template('views/login.html', error=None)

# ROTA HOME
@route('/home')
def home_page():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    usuario = Usuario.find_by_id(s['user_id'])
    if not usuario:
        s.delete()
        return redirect('/login')

    treinos_do_usuario = usuario.get_treinos()
    return template('views/home.html', nome=usuario.nome, treinos=treinos_do_usuario)

# ROTA PARA CRIAR TREINOS
@route('/treinos/criar', method='POST')
def criar_treino():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    nome_treino = request.forms.get('nome_treino')
    if nome_treino:
        novo_treino = Treino(nome=nome_treino, usuario_id=s['user_id'])
        novo_treino.save()

    return redirect('/home')

@route('/treinos/editar/<treino_id:int>', method='POST')
def editar_treino(treino_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    novo_nome = request.forms.get('novo_nome_treino')
    if novo_nome:
        Treino.update_nome(treino_id, novo_nome)
    
    return redirect('/home')

@route('/treinos/deletar/<treino_id:int>', method='POST')
def deletar_treino(treino_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    Treino.delete(treino_id)
    return redirect('/home')

# Rota de logout
@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    return redirect('/login')

# Rota de informações (placebo)
@route('/informacoes')
def informacoes_page():
    return "<h1>Página de Informações do Usuário</h1><p>Em construção...</p>"


@route('/')
def index():
    return template('views/apresentacao.html')