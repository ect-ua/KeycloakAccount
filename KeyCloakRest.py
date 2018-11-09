import json
import secrets
import requests
import psycopg2
import sqlite3
from Student import Student
def getToken():

    url = "https://idp.ect-ua.com/auth/realms/master/protocol/openid-connect/token"


    data = {'username': username,
            'password': password,
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
               'firstName': data['Firstname'],
               'lastName': data['Lastname']})

    print(payload)


    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + token,
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response)
    addPassword(getID(data['username']), data['password'])


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


def getID(username):


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
    # conn_string = "host=%s dbname=%s user=%s password=%s" % ("localhost", "testdb", "toms", "password")
    # conn = psycopg2.connect(conn_string)
    # cur = conn.cursor()
    conn = sqlite3.connect('testDB')
    cur = conn.cursor()

    return conn, cur

def closedb(cur, conn):
    cur.close()
    conn.close()

def verify_token(token):

    user = get_user_by_token(token)
    if not user:
        return None
    else:
        user = user[0]

    return Student(user)

    # elif username is None:
    #     return 2, ''  # new user
    # elif user[0][0] is not None: #assumindo que o username é o primeiro campo na tabela
    #     return 1, user[0][0]



def get_user_by_token(token):
    conn, cur = connect_db()

    query = 'SELECT * from Users WHERE token = ?'

    cur.execute(query, (token,))

    result = cur.fetchall()

    closedb(cur, conn)

    return result

def deleteRegister(token):
    print(token)
    conn, cur = connect_db()

    query = "DELETE FROM Users WHERE token = ?"

    cur.execute(query, (token,))
    conn.commit()

    closedb(cur, conn)


def register(data):

    #db scheme: username, full name, email, token, nmec, ano de entrada

    username, full_name, email, token, nmec, ano_entrada = get_user_by_token(data['token'])[0]
    print(get_user_by_token(data['token']))

    if username is None:
        username = data['username']  #só vou buscar o username ao post se for um new user
    password = data['password']

    new_data = {'username': username,
                'password': password,
                'Firstname': full_name.split(' ')[0],
                'Lastname': full_name.split(' ')[1],
                'email':    email}


    attributes = {'nmec':     nmec,
                  'ano':      ano_entrada}

    addaccount(new_data)
    addAtributes(getID(new_data['username']), attributes)
    deleteRegister(token)




if __name__ == '__main__':
    verify_token('123456')