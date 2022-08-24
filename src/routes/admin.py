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


@user_admin.route('/getDocente',methods=["GET"])
def getDocente():
    return {"Ok":True}

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




#Materia
@user_admin.route('/createMateria',methods=['POST'])
def CreateMateria():
    print(request.json)
    descripcion = request.json['descripcion']
    horaInicio = request.json['hora_inicial']
    horaFinal = request.json['hora_final']
  
    aula = request.json['aula']
    lunes = request.json['Lunes']
    martes = request.json['Martes']
    miercoles = request.json['Miercoles']
    jueves = request.json['Jueves']
    viernes = request.json['Viernes']
    datos = []

    if lunes:
        datos.append('Lunes')
    if martes:
        datos.append('Martes')
    if miercoles:
        datos.append('Miercoles')
    if jueves:
        datos.append('Jueves')
    if viernes:
        datos.append('Viernes')
    
    mydb.materia.insert_one({"descripcion":descripcion,"hora_inicio":horaInicio,"hora_final":horaFinal,"dias":datos})

    response = jsonify({
        "ok":"ok",
    })
    return response;

@user_admin.route('/getMaterias',methods=['GET'])
def getMaterias():
    datos = mydb.materia.find()
    materias = [ dict(row) for row in datos ]
    return json.dumps(materias, default=json_util.default)

@user_admin.route('/deleteMateria',methods=['DELETE'])
def deleteMateria():
    args = request.args
    id_materia = args.get('id_materia')
    mydb.materia.delete_one({'_id': ObjectId(id_materia)})
    return {
        "ok":"ok"
    }

@user_admin.route('/updateMateria/<id>',methods=["PUT"])
def updateMateria(id):

    _id = id
    print(request.json)
    descripcion = request.json['descripcion']
    horaInicio = request.json['hora_inicial']
    horaFinal = request.json['hora_final']
    aula = request.json['aula']
  
    lunes = request.json['Lunes']
    martes = request.json['Martes']
    miercoles = request.json['Miercoles']
    jueves = request.json['Jueves']
    viernes = request.json['Viernes']
    datos = []

    # aulaExist = mydb.materia.find_one({"aula":aula})
    
  


    if lunes:
        datos.append('Lunes')
    if martes:
        datos.append('Martes')
    if miercoles:
        datos.append('Miercoles')
    if jueves:
        datos.append('Jueves')
    if viernes:
        datos.append('Viernes')
    
    mydb.materia.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)},{"$set":{"descripcion":descripcion,"hora_inicio":horaInicio,"hora_final":horaFinal,"dias":datos,"aula":aula}})

    return {
        "ok":True
    }


# Ciclo Academico 
@user_admin.route('/createCicloAcademico',methods=["POST"])
def createCicloAcademico():
    json = request.json
    descripcion = json['descripcion']
    orden = json['orden']
 

    mydb.ciclo_academico.insert_one({"descripcion":descripcion,"orden":orden,"estado":False})

    return {
        "ok":True
    }
@user_admin.route('/getCicloAcademico',methods=["GET"])
def getCicloAcademico():
    ciclo_academico = mydb.ciclo_academico.find()
    ciclos = [ dict(row) for row in ciclo_academico ]
    return json.dumps(ciclos,default=json.util.default)

@user_admin.route('/updateCicloAcademico/<id>',methods=["PUT"])
def updateCicloAcademico(id):
    _id = id
    json = request.json
    descripcion = json['descripcion']
    orden = json['orden']

    mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)},{"$set":{"descripcion":descripcion,"orden":orden}})

    return {
        "message":"update successfully"
    }
@user_admin.route('/updateEstadoClicloAcademico/<id>',methods=["PUT"])
def updateStateCicloAcademico(id):

    _id  = id
    mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)}, {"$set":{"estado":True}})

    return {
        "message":"Activate successfully"
    }


#
@user_admin.route('/createNota',methods=["POST"])
def CreateNota():
    json = request.json
    ciclo_academica = json['id_ciclo']

    mydb.nota.inser_one({"ciclo_academico":ciclo_academica})

    return {"Ok":True}

@user_admin.route('/getNotas',methods=['GET'])
def GetNotas():
    notas_get = mydb.nota.find()
    notas = [ dict(row) for row in notas_get ]
    return json.dumps(notas,default=json.util.default)


#  

@user_admin.route('/assignParalelo',methods=['POST'])
def AssignParalelo():
    json = request.json
    id_ciclo = json['id_ciclo']
    docente = json['id_docente']
    materia = json['id_materia']
    paralelo = json['paralelo']
    
    # mydb.AssingParalelo.insert_one({})
