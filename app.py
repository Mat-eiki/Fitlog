from bottle import run

# 1. Importa as rotas do seu arquivo de controller.
import controllers.rotas

# 2. Inicia o servidor.
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)