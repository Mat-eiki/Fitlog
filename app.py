from bottle import route, run, template
from bottle import static_file

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@route('/home')
def home():
    return template('views/home.html', nome="Visitante")

run(host='localhost', port=8080, debug=True)
