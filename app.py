from bottle import run, app # Importe 'app' do bottle
import beaker.middleware
import controllers.rotas

# Configurações da sessão
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600, # Expira em 1 hora
    'session.data_dir': './session_data', # Pasta para guardar os dados da sessão
    'session.auto': True
}

# Cria a aplicação com o middleware de sessão
# A variável 'app' é a nossa aplicação Bottle com superpoderes de sessão
application = beaker.middleware.SessionMiddleware(app(), session_opts)

# Inicia o servidor usando a nova 'application'
if __name__ == '__main__':
    run(app=application, host='localhost', port=8080, debug=True, reloader=True)