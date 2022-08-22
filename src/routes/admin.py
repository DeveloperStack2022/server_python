from flask import Blueprint, request,jsonify
import bcrypt
from functions_jwt import validate_token
from database import mydb
user_admin = Blueprint('admin',__name__)
import json
from bson import json_util
import base64
from bson.objectid import ObjectId

print(__name__)

# @user_admin.before_request
# def verify_token_middleware():
#     token = request.headers['Authorization'].split(" ")[1]
#     return validate_token(token,output=False)

@user_admin.route('/createUser',methods=['POST'])
def createUser():
    #reciving datap
    username = request.json['username']
    nombre =  request.json['nombre']
    apellido =  request.json['apellido']
    password = request.json['password']
    dni =  request.json['numCedula']
    # rol = request.json['rol_id']
    rol = request.json['rol']
    
    # -------- END DATA ------------- # 
    if username and nombre and password and apellido and dni and rol :
        idRol = mydb.db.role.find_one({"name_role":rol})
        hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'),bcrypt.gensalt(10))
        id = mydb.users.insert_one({'username':username,'_id':str(dni),'password':hashed_password,'apellido':apellido,'nombre':nombre,'rol_id':idRol["_id"]}).inserted_id
        
        response = jsonify({
            '_id': str(id),
            'nombre': nombre,
            'apellido':apellido,
            'username':username,
            'numCedula':dni,
            'rol':idRol['name_role']
        })
        response.status_code = 201
        return response
    else:
        return not_found()

""" GET Users """
@user_admin.route('/getUsers', methods=["GET"])
def getUsers():
   
    datos = mydb.users.find()
    users = [ dict(row) for row in datos ]
    # print(users)
    # docs_list  = list(datos)
    return json.dumps(users, default=json_util.default)
    # return {"Datos":users}


@user_admin.route('/deleteUser',methods=["DELETE"])
def deleteUser():
    username = request.json['username']
    datos = mydb.users.find_one({"username": username})
    if datos: 
        mydb.users.delete_one({"username": username})
        response = jsonify({
            "ok":"ok",
            "username":datos['username']
        })
        response.status_code = 200
        return  response


@user_admin.route('/createMateria',methods=['POST'])
def CreateMateria():
    descripcion = request.json['descripcion']
    horaInicio = request.json['hora_inicio']
    horaFinal = request.json['hora_final']
    dias = request.json['dias']
    aula = request.json['aula']
    
     
    return {
        "Status":"Ok"
    }

@user_admin.route('/getMaterias',methods=['GET'])
def getMaterias():

    return {
        "Status":"Ok"
    }