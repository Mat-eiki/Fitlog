from bottle import route, template, static_file, redirect, request, response, TEMPLATE_PATH
TEMPLATE_PATH.insert(0, './views/')
from models.treino import Treino, Exercicio
from models.usuario import Usuario


# --- ROTA ESTÁTICA SIMPLIFICADA ---
@route('/static/<filepath:path>')
def server_static(filepath):
    """Serve arquivos estáticos (CSS, JS, imagens) da pasta ./static/"""
    return static_file(filepath, root='./static/')

# Rota da página de apresentação
@route('/')
def index():
    return template('apresentacao.html')

# Rota para a página de acesso negado
@route('/acesso_negado')
def acesso_negado_page():
    return template('acesso_negado.html')

# Rota de Cadastro
@route('/cadastro', method=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('senha')

        if Usuario.find_by_email(email):
            return template('cadastro.html', error="Este e-mail já está em uso.")

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        novo_usuario.save()
        return redirect('/login')
    
    return template('cadastro.html', error=None)

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
        return template('login.html', error=error_msg)

    return template('login.html', error=None)

# Rota Home (página principal logada)
@route('/home')
def home_page():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/acesso_negado') # Redirecionamento correto

    usuario = Usuario.find_by_id(s['user_id'])
    if not usuario:
        s.delete()
        return redirect('/acesso_negado')

    treinos_do_usuario = usuario.get_treinos()
    # Lembre-se que o arquivo é 'home.tpl'
    return template('home.tpl', nome=usuario.nome, treinos=treinos_do_usuario)

# --- ROTAS DE TREINOS E EXERCÍCIOS (sem alterações na lógica) ---

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

@route('/exercicios/editar/<exercicio_id:int>', method='POST')
def editar_exercicio(exercicio_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    novo_nome = request.forms.get('novo_nome_exercicio')
    nova_carga = request.forms.get('nova_carga_exercicio')

    if novo_nome and nova_carga:
        Exercicio.update(exercicio_id, novo_nome, nova_carga)

    return redirect('/home')

@route('/exercicios/deletar/<exercicio_id:int>', method='POST')
def deletar_exercicio(exercicio_id):
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    Exercicio.delete(exercicio_id)
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

# Rota de Logout
@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    return redirect('/login')

# Rota de Informações
@route('/informacoes')
def informacoes_page():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    usuario = Usuario.find_by_id(s['user_id'])
    
    # Se o usuário não for encontrado (pode ter sido deletado), redireciona para o login
    if not usuario:
        s.delete()
        return redirect('/login')

    success_msg = request.query.get('success')
    error_msg = request.query.get('error')

    # A linha mais importante: Garante que 'usuario', 'success' e 'error' 
    # são sempre enviados para o template.
    return template('informacoes.html', 
                    usuario=usuario, 
                    success=success_msg, 
                    error=error_msg)

@route('/usuario/atualizar/nome', method='POST')
def atualizar_nome():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')
    
    novo_nome = request.forms.get('novo_nome')
    if novo_nome:
        Usuario.update_nome(s['user_id'], novo_nome)
        return redirect('/informacoes?success=Nome alterado com sucesso!')
    
    return redirect('/informacoes?error=Ocorreu um erro ao alterar o nome.')

@route('/usuario/atualizar/senha', method='POST')
def atualizar_senha():
    s = request.environ.get('beaker.session')
    if 'user_id' not in s:
        return redirect('/login')

    senha_antiga = request.forms.get('senha_antiga')
    nova_senha = request.forms.get('nova_senha')
    
    usuario = Usuario.find_by_id(s['user_id'])

    # Verifica se a senha antiga fornecida está correta
    if not usuario or not usuario.check_password(senha_antiga):
        return redirect('/informacoes?error=A senha atual está incorreta.')

    # Atualiza para a nova senha
    usuario.update_senha(nova_senha)
    return redirect('/informacoes?success=Senha alterada com sucesso!')

@route('/usuario/deletar', method='POST')
def deletar_conta():
    s = request.environ.get('beaker.session')
    user_id = s.get('user_id')

    if not user_id:
        return redirect('/login')

    # Deleta o usuário e todos os seus dados associados
    Usuario.delete(user_id)

    # Destrói a sessão para fazer o logout
    s.delete()

    # Redireciona para a página de apresentação inicial
    return redirect('/')