from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import json

import config
import keycloakrest as cloak
import sys

app = Flask(__name__, static_url_path='/static')
api = Api(app)

#
# class REST(Resource):
#     # def post(self):
#     #     data = request.get_json()
#     #     print(data)
#     #     if data['username'].lower().endswith('bot'):
#     #         return None,412
#     #     cloak.addaccount(data)
#
#
#
#
# api.add_resource(REST, '/')

@app.route("/")

def index():
    return open('index.html').read()

@app.route("/register", methods=['POST', 'GET'])
def password():
    if request.method == 'GET':  #Se eles quiserem registar
        mytoken = request.args.get('token', default=None, type = str)
        student = cloak.get_user_by_token(mytoken)
        if student is None:
            return 'Error reading token'
        else:
            if student.username != '':
                return render_template('migrate.html', token=mytoken, username=student.username) #old user
            else:
                return render_template('new.html', token=mytoken, username='Username') #new user

    elif request.method == 'POST': #depois de preencherem os campos e carregarem em registar
        register()
        return "<html><body>Success</body></html>"



def register():
    print('entrei aqui')
    data = request.get_json()
    print('#################', file=sys.stderr)
    print('data is:', file=sys.stderr)
    print(data, file=sys.stderr)
    if data['username'].lower().endswith('bot'):
        #inserir mais verificações já feitas em javascript
        return None,412
    #UserName, Password, Token já verificado
    cloak.register(data)



if __name__ == '__main__':
    app.run(debug=True)