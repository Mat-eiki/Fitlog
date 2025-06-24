from bottle import route, template, static_file, redirect

# Rota para servir arquivos estáticos (CSS, JS, Imagens)
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def apresentacao():
    return template('views/apresentacao.html', nome="Visitante")

# Rota para a página de login
@route('/login')
def login_page():
    return template('views/login.html')

# Rota para a página de cadastro
@route('/cadastro')
def cadastro_page():
    return template('views/cadastro.html')