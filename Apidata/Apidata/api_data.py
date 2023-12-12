""" ================================================================================================
Institucion..: Universidad Tecnica Nacional
Sede.........: Del Pacifico
Carrera......: Tecnologias de Informacion
Periodo......: 3-2020
Charla.......: Uso de Python para demostracion de servicio en Droplet - Digital Ocean
Documento....: api_data.py
Objetivos....: Demostracion de un micro servicio web con api-REST.
Profesor.....: Jorge Ruiz (york)
Estudiante...:
================================================================================================"""
# -------------------------------------------------------
# Import libraries API service support
# -------------------------------------------------------
from datetime import datetime
import random
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

# Create flask app
app = Flask(__name__)
CORS(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Create connection with MongoDB
from pymongo import MongoClient

def contextDB():
    conex = MongoClient(host=['127.0.0.1:27017'], username='admin', password='parda99*')
    #conexDB = conex.apiData_01
    return conex


# -------------------------------------------------------
# Create data objets, only memory
# -------------------------------------------------------
users = []
ldata = []

conta = 0

# -------------------------------------------------------
# Create local API functions
# -------------------------------------------------------
def token():
    ahora = datetime.now()
    antes = datetime.strptime("1970-01-01", "%Y-%m-%d")
    return str(hex(abs((ahora - antes).seconds) * random.randrange(10000000)).split('x')[-1]).upper()

def tokTask():
    ahora = datetime.now()
    antes = datetime.strptime("1970-01-01", "%Y-%m-%d")
    return str(hex(abs((ahora - antes).seconds) * random.randrange(1000000000)).split('x')[-1]).upper()


# -------------------------------------------------------
# Error control, httpRequest rules
# -------------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request....!'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized....!'}), 401)

@app.errorhandler(403)
def forbiden(error):
    return make_response(jsonify({'error': 'Forbidden....!'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found....!'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Inernal Server Error....!'}), 500)

# --------------------------------------------------
# Create routes and user control functions
# --------------------------------------------------
# User signup, register new user
@app.route('/signup', methods=['POST'])
def create_user():
    if not request.json or \
            not 'name' in request.json or \
            not 'email' in request.json or \
            not 'passwd' in request.json:
        abort(400)

    tkn1 = token()
    user = {
        "_id" : tkn1,
        'name': request.json['name'],
        'email': request.json['email'],
        'passwd': request.json['passwd'],
    }
    try:
        conexDB= contextDB()
        conexDB.apiData_01.user.insert_one(user)
        user2 = {
            'token':tkn1,
            'name': request.json['name'],
            'email': request.json['email'],
            'passwd': request.json['passwd'],
        }
        data = {
            "status_code": 201,
            "status_message": "Data was created",
            "data": {'user': user2}
        }
        conexDB.close()
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 201

# Retrieve data user from token
@app.route('/<string:token>/me', methods=['GET'])
def get_user(token):
    try:
        conexDB = contextDB()
        user = conexDB.apiData_01.user.find_one({"_id":{"$eq":token}})

        if user == None:
            abort(404)

        data = {
            "status_code": 200,
            "status_message": "Ok",
            "data": {'user': {"name": user['name'],
                              "email": user['email']
                              }
                    }
        }
        conexDB.close()
    except Exception as expc:
        abort(404)
    return jsonify(data)


# Retrieve token field from login data
@app.route('/login/<string:email>/<string:passwd>', methods=['GET'])
def get_login(email, passwd):
    try:
        conexDB = contextDB()
        user = conexDB.apiData_01.user.find_one({"email":{"$eq":email},"passwd":{"$eq":passwd}})
        if user == None:
            abort(404)
        data = {
            "status_code": 200,
            "status_message": "Ok",
            "data": {'user': {"name": user['name'],
                              "token": user['_id']
                              }
                    }
        }
        conexDB.close()
    except Exception as expc:
        abort(404)
    return jsonify(data)

# --------------------------------------------------
# Task methods
# --------------------------------------------------
@app.route('/<string:token>/task', methods=['POST'])
def create_task(token):
    if not (request.json and 'task' in request.json):
        abort(400)

    conexDB = contextDB()
    conta = tokTask()
    data = {
        '_id': conta,
        'task': request.json['task'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'token': token
    }
    try:
        conexDB.apiData_01.task.insert_one(data)
        salida = {
            "status_code": 201,
            "status_message": "Data was created",
            "data": data
        }
    except Exception as expc:
        abort(500)
    conexDB.close()
    return jsonify({'customer': salida}), 201


# Retrieve user task list
@app.route('/<string:token>/task', methods=['GET'])
def get_task(token):
    try:
        conexDB = contextDB()
        datos = conexDB.apiData_01.task.find({"token":{"$eq":token}}).sort('date')

        if datos is None:
            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": "Empty task list"
            }
        else:
            lista = []
            for collect in datos:
                lista.append({"id": collect['_id'],
                      "task": collect['task'],
                      "date": collect['date']})

            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": lista
            }
        conexDB.close()
    except:
        abort(500)
    return jsonify(data)


# Retrieve a specific task
@app.route('/<string:token>/task/<string:task_id>', methods=['GET'])
def get_task_id(token, task_id):
    try:
        conexDB = contextDB()
        datos = conexDB.apiData_01.task.find_one({"token":{"$eq":token},"_id":{"$eq":task_id}})

        if datos is None:
            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": "Task data not found"
            }
        else:
            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": {"id": datos['_id'],
                         "task": datos['task'],
                         "date": datos['date']}
            }
        conexDB.close()
    except Exception as expc:
        abort(404)
    return jsonify(data)


# Delete a specific user task
@app.route('/<string:token>/task/<string:task_id>', methods=['DELETE'])
def delete_task(token, task_id):
    try:
        conexDB = contextDB()
        datos = conexDB.apiData_01.task.find_one({"token":{"$eq":token},"_id":{"$eq":task_id}})
        if datos == None:
            abort(404)
        conexDB.apiData_01.task.delete_one({'_id':datos['_id']})

    except Exception as expc:
        abort(404)
    return jsonify({"status_code": 200,
                    "status_message": "Ok",
                    "result": True})


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 5000
    app.run(HOST, PORT)
