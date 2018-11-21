import json
import secrets
import requests
import psycopg2
import sqlite3
from config import *
from student import Student

def getToken():
    url = "https://idp.ect-ua.com/auth/realms/master/protocol/openid-connect/token"
    data = {'username': KEYCLOAK_USERNAME,
            'password': KEYCLOAK_PASSWORD,
            'client_id': 'admin-cli',
            'grant_type': 'password'}

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, data=data, headers=headers)
    data = json.loads(response.text)
    token = data['access_token']

    return token

def addaccount(data):
    token = getToken()

    url = "https://idp.ect-ua.com/auth/admin/realms/master/users"

    payload = json.dumps({'enabled': 'true',
               'username': data['username'],
               'email': data['email'],
               'firstName': data['firstname'],
               'lastName': data['lastname']})

    print(payload)


    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response)
    addPassword(getUserKeycloakId(data['username']), data['password'])


def addPassword(id, password):
    token = getToken()

    url = "https://idp.ect-ua.com/auth/admin/realms/master/users/"+id+"/reset-password"

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'cache-control': "no-cache"
    }

    payload = json.dumps({'type': 'password',
                          'value': password,
                          'temporary': 'false'})

    response = requests.request("PUT", url, data=payload, headers=headers)


def getUserKeycloakId(username):
    url = "http://idp.ect-ua.com/auth/admin/realms/master/users"
    querystring = {"username": username}

    headers = {
        'Authorization': 'Bearer ' + getToken()
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    print(response.url)
    return response.json()[0]['id']


def addAtributes(id, attributes):
    token = getToken()
    url = "https://idp.ect-ua.com/auth/admin/realms/master/users/" + id

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'cache-control': "no-cache"
    }

    payload = json.dumps({"attributes":attributes})
    response = requests.request("PUT", url, data=payload, headers=headers)

def connect_db():
    conn_string = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    #conn = sqlite3.connect('testDB')
    #cur = conn.cursor()

    return conn, cur

def closedb(cur, conn):
    cur.close()
    conn.close()

def get_user_by_token(token):
    conn, cur = connect_db()
    query = 'SELECT * from ectua_newusers WHERE register_token = ?'
    cur.execute(query, (token,))
    result = cur.fetchall()
    closedb(cur, conn)

    if not result:
        return None
    else:
        result = result[0]

    return Student(result)

def deleteRegister(token):
    print('Deleting token: ' + token)
    conn, cur = connect_db()

    query = "DELETE FROM ectua_newusers WHERE register_token = ?"

    cur.execute(query, (token,))
    conn.commit()

    print('Finished')

    closedb(cur, conn)


def register(data):

    #db scheme: username, full name, email, token, nmec, ano de entrada

    user = get_user_by_token(data['token'])
    #_id, full_name, username, , email, token, nmec, ano_entrada = get_user_by_token()[0]
    print(user)
    username = user.username
    firstName = user.name.split(' ')[0]
    lastName = user.name.split(' ')[1]

    if username is None:
        username = data['username']  #só vou buscar o username ao post se for um new user
    password = data['password']

    new_data = {'username': username,
                'password': password,
                'firstname': firstName,
                'lastname': lastName,
                'email':    user.email}


    attributes = {'nmec':     username.nmec,
                  'ano_matricula':      username.ano}

    addaccount(new_data)
    addAtributes(getUserKeycloakId(new_data['username']), attributes)
    deleteRegister(token)




if __name__ == '__main__':
    get_user_by_token('123456')