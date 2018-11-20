from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import keycloakrest as cloak
import json


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
        mytoken = request.args.get('token', default='', type = str)
        student = cloak.get_user_by_token(mytoken)
        if student is None:
            return 'Error reading token'
        else:
            if student.userName is not None:
                return render_template('register-token.html', token=mytoken, username=student.userName) #old user
            else:
                return render_template('register-token.html', token=mytoken, username='Username') #new user

    elif request.method == 'POST': #depois de preencherem os campos e carregarem em registar
        register()
        return "<html><body>Success</body></html>"



def register():
    data = request.get_json()
    if data['username'].lower().endswith('bot'):
        #inserir mais verificações já feitas em javascript
        return None,412
    #UserName, Password, Token já verificado
    cloak.register(data)



if __name__ == '__main__':
    app.run(debug=True)