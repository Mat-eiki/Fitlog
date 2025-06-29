from bottle import route, template, static_file, redirect, request, response

# A linha mais importante a verificar: garante que AMBAS as classes são importadas
from models.treino import Treino, Exercicio
from models.usuario import Usuario


# Rota para servir ficheiros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Rota da página de apresentação
@route('/')
def index():
    s = request.environ.get('beaker.session')
    if 'user_id' in s:
        return redirect('/home')
    return template('views/apresentacao.html')

# Rota de Cadastro
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

# Rota de Login
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

# Rota Home (página principal logada)
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
    return template('views/home.tpl', nome=usuario.nome, treinos=treinos_do_usuario)

# Rota para CRIAR TREINOS
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

# Rota para CRIAR EXERCÍCIOS
@route('/exercicios/criar/<treino_id:int>', method='POST')
def criar_exercicio(treino_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    nome_exercicio = request.forms.get('nome_exercicio')
    carga_exercicio = request.forms.get('carga_exercicio')

    if nome_exercicio and carga_exercicio:
        novo_exercicio = Exercicio(
            nome=nome_exercicio, 
            carga=carga_exercicio, 
            treino_id=treino_id
        )
        novo_exercicio.save()

    return redirect('/home')

# Rota para EDITAR EXERCÍCIOS
@route('/exercicios/editar/<exercicio_id:int>', method='POST')
def editar_exercicio(exercicio_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    novo_nome = request.forms.get('novo_nome_exercicio')
    nova_carga = request.forms.get('nova_carga_exercicio')

    if novo_nome and nova_carga:
        # Idealmente, aqui também haveria uma verificação de segurança
        Exercicio.update(exercicio_id, novo_nome, nova_carga)

    return redirect('/home')

# Rota para DELETAR EXERCÍCIOS
@route('/exercicios/deletar/<exercicio_id:int>', method='POST')
def deletar_exercicio(exercicio_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    # Adicionar verificação de segurança aqui seria ideal
    Exercicio.delete(exercicio_id)
    return redirect('/home')

# Rota para EDITAR TREINOS
@route('/treinos/editar/<treino_id:int>', method='POST')
def editar_treino(treino_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    novo_nome = request.forms.get('novo_nome_treino')
    if novo_nome:
        Treino.update_nome(treino_id, novo_nome)
    
    return redirect('/home')

# Rota para DELETAR TREINOS
@route('/treinos/deletar/<treino_id:int>', method='POST')
def deletar_treino(treino_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    Treino.delete(treino_id)
    return redirect('/home')

# Rota de Logout
@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    return redirect('/login')

# Rota de Informações (placebo)
@route('/informacoes')
def informacoes_page():
    return "<h1>Página de Informações do Utilizador</h1><p>Em construção...</p>"