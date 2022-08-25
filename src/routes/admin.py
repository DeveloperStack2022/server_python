
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

@user_admin.route('/getUsersEstudiantes')
def getUserStudent():
    rol = mydb.db.role.find_one({"name_role":"estudiante"})
    print(rol)
    estudiantes = mydb.users.find({'rol_id':rol['_id']})
    students = [ dict(row) for row in estudiantes ]
    return json.dumps(students, default=json_util.default)
  

#Docente 
@user_admin.route('/getUsersDocentes')
def getDocentes():
    docente = mydb.db.role.find_one({"name_role":"docente"})
    docentes = mydb.users.find({"rol_id":docente['_id']})
    docenteList = [ dict(row) for row in docentes ]
    return json.dumps(docenteList, default=json_util.default)

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
    
    mydb.materia.insert_one({"descripcion":descripcion,"hora_inicio":horaInicio,"hora_final":horaFinal,"dias":datos,"aula":aula})

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
    cicloAcademico = mydb.ciclo_academico.find();
    cicloAca = [dict(row) for row in cicloAcademico]
    print(cicloAca)
    if not cicloAca: 
        mydb.ciclo_academico.insert_one({"descripcion":descripcion,"orden":orden,"estado":True})
    else:
        mydb.ciclo_academico.insert_one({"descripcion":descripcion,"orden":orden,"estado":False})

    return {
        "ok":True
    }

@user_admin.route('/getCicloAcademicos',methods=["GET"])
def getCicloAcademico():
    ciclo_academico = mydb.ciclo_academico.find()
    ciclos = [ dict(row) for row in ciclo_academico ]
    return json.dumps(ciclos,default=json_util.default)

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
    idQuery = mydb.ciclo_academico.find_one({"_id":ObjectId(_id)})
    if idQuery['estado']: 
        mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)}, {"$set":{"estado":False}})
        # querySizes = mydb.ciclo_academico.find({"estado":True})
    else:
        mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)}, {"$set":{"estado":True}})

        # --------------------------- Reutilizar -------------------------------- # 

        # if len(list(querySizes)) > 0 : 
        #     # update many
        #     # updateM = mydb.ciclo_academico.update_many({},{})
        #     print(dict(querySizes))
        #     for row in list(querySizes) : 
        #         print('Row' + row["_id"])
            # mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)}, {"$set":{"estado":True}})
            
        # mydb.ciclo_academico.update_one({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)}, {"$set":{"estado":True}})
    # else:



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
    users = json['user']
    
    mydb.AssingParalelo.insert_one({"id_ciclo":id_ciclo,"id_docente":docente,"id_materia":materia,"paralelo":paralelo,"students":users})

    response = jsonify({
        "ok":"ok",
    })
    response.status = 201;
    return response;


@user_admin.route('/getParalelos')
def getParalelos():

    paralelos = mydb.AssingParalelo.find()

    # paralelosDic = [ dict(row) for row in paralelos ]
    datosArray = []
    datosUser = []
    for row in paralelos :
        # print("\n",dict(row))
        valores  = dict(row)
        _id = valores['_id']
        id_ciclo = valores['id_ciclo']
        id_materia = valores['id_materia']
        id_docente = valores['id_docente']
        studentsId = valores['students']

        # Obtenemos el Documente del  ciclo Academico  (Query for Id )
        cicloAcademico = mydb.ciclo_academico.find_one({"_id":ObjectId(id_ciclo)})
        # print(dict(cicloAcademico))
        descripcionDelCiclo  = cicloAcademico['descripcion']
      
        
        #Obtenemos el Documente de la Materia  (Query for Id )
        materia = mydb.materia.find_one({"_id":ObjectId(id_materia)})
        # print(materia)
        
    
        #Obtenemos el Documente de la Materia  (Query for Id )
        docenteDocument = mydb.users.find_one({"_id":id_docente})
        # print(docenteDocument)
        
        # print(studentsId)
        count = 0;
        for userRow in studentsId:
            user = mydb.users.find_one({"_id":userRow})
            # print("\n",dict(user))
            count += 1
            datosUser.append({"usuario":user['nombre']})
            # datosArray.append({"usuario":user['nombre']})


        datosArray.append({"_id":_id,"descripcion_ciclo":descripcionDelCiclo,"descripcion_materia":materia['descripcion'],"nombre_docente":docenteDocument['nombre']})
        print(count)
        
        
    # print(datosArray)
 
    # return json.dumps(paralelosDic,default=json_util.default)
    return json.dumps(datosArray,default=json_util.default)


@user_admin.route('/deleteParalelo/<id>',methods=["DELETE"])
def deleteParalelo(id):
    _id = id
    mydb.AssingParalelo.delete_one({"_id":ObjectId(_id)})

    return {
        "ok":"ok"
    }