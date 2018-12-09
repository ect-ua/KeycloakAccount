from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import json
import sys
import re

import config
import keycloakrest as cloak


app = Flask(__name__, static_url_path='/static')
api = Api(app)

nameRegex = re.compile('^[a-zA-Z\sÀ-ú]*$')
nmecRegex = re.compile('^([1-9]{1}[0-9]+)$')
emailRegex = re.compile('^[a-z0-9._%+-]+@ua\.pt$')
usernameRegex = re.compile('^[a-zA-Z0-9._-]{3,50}$')

@app.route("/")
def index():
    return open('index.html').read()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Página não encontrada'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='Erro interno do servidor'), 500

@app.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', error='Não tens permissões para aceder a esta página'), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error='Não tens permissões para aceder a esta página'), 403

@app.errorhandler(400)
def invalid_request(e):
    return render_template('error.html', error='Pedido inválido'), 400


@app.route("/register", methods=['POST', 'GET'])
def password():
    if request.method == 'GET':  #Se eles quiserem registar
        mytoken = request.args.get('token', default=None, type = str)
        student = cloak.get_user_by_token(mytoken)
        if student == None:
            return render_template('error.html', error='O registo no ECT-UA requer um token de registo válido.')
        else:
            if student.username != '':
                return render_template('migrate.html', token=mytoken, username=student.username) #old user
            else:
                return render_template('new.html', token=mytoken, username='Username') #new user

    elif request.method == 'POST': #depois de preencherem os campos e carregarem em registar
        result = register()
        if result == 0:
            return render_template('success.html')
        elif result == 1:
            return render_template('error.html', error='Nome de utilizador inválido')
        elif result == 2:
            return render_template('error.html', error='Nome inválido')
        elif result == 3:
            return render_template('error.html', error='Número mecanográfico inválido')
        elif result == 4:
            return render_template('error.html', error='E-mail inválido')
        elif result == 5:
            return render_template('error.html', error='As palavras-passe não coincidem')
        elif result == 6:
            return render_template('error.html', error='Não foi possível concluir o registo da conta de utilizador')


def register():
    data = request.get_json()

    username = data['username'] or ''
    firstName = data['firstname'] or ''
    lastName = data['lastname'] or ''
    nmec = data['nmec'] or 0
    email = data['email'] or ''
    password = data['password'] or 'a'
    password_confirm = data['confirm_password'] or 'b'

    if username.lower().endswith('bot') or usernameRegex.match(username) == None:
        return 1

    if nameRegex.match(firstName) == None or nameRegex.match(lastName) == None:
        return 2

    if nmecRegex.match(nmec) == None:
        return 3

    if emailRegex.match(email) == None:
        return 4

    if password != password_confirm:
        return 5

    if cloak.register(data):
        return 0
    else:
        return 6



if __name__ == '__main__':
    app.run(debug=True)