
from sre_constants import SUCCESS
from unicodedata import category
from flask import Blueprint, request,jsonify
import bcrypt
from functions_jwt import validate_token
from database import mydb
user_admin = Blueprint('admin',__name__)
import json
from bson import json_util
import base64
from bson.objectid import ObjectId
import urllib.request
from app import cloudinary
# from ConfiCloud import Cloud

print(__name__)








# @user_admin.before_request
# def verify_token_middleware():
#     token = request.headers['Authorization'].split(" ")[1]
#     return validate_token(token,output=False)

@user_admin.route('/createUser',methods=['POST'])
def createUser():
    #reciving datap
    username = request.form['username']
    nombre =  request.form['nombre']
    apellido =  request.form['apellido']
    password = request.form['password']
    dni =  request.form['numCedula']
    # rol = request.form['rol_id']
    rol = request.form['rol']

    # image = request.form.get('image_perfil')

    if 'image_perfil' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    image = request.files['image_perfil']
    print(image)
    response = cloudinary.uploader.upload(image)
    print(response['secure_url'])
    img_url = response['secure_url']
    # print(request.form.get('numCedula'))
    # -------- END DATA ------------- # 
    if username and nombre and password and apellido and dni and rol :
        idRol = mydb.db.role.find_one({"name_role":rol})
        hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt(10))
        id = mydb.users.insert_one({'username':username,'_id':str(dni),'password':hashed_password,'apellido':apellido,'nombre':nombre,'rol_id':idRol["_id"],'img_url':img_url}).inserted_id
        
        response = jsonify({
            '_id': str(id),
            'nombre': nombre,
            'apellido':apellido,
            'username':username,
            'numCedula':dni,
            'rol':idRol['name_role'],
        })
        response.status_code = 201
        return response
        return {
            "ok":"ok"
        }
    else:
        return not_found()
    return {"ok":"ok"}

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
    # {'_id'}
    # nono
    if datos:
        user = mydb.users.delete_one({"username": username})
       
        response = jsonify({
            "ok":"ok",
            "username":datos['username']
        })
        response.status_code = 200
        return  response

    result =  jsonify({
        "message":"not found document by username"
    })
    result.status = 400 #Cliente esta haciendo incorreacta 
    
    return result



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

    # http://localhost:5000/api/deleteMateria?id_materia=123&name=luis
    # name = request.args.get('name') # "luis"
    id_materia = args.get('id_materia') # "mi trabajo"

    mydb.materia.delete_one({'_id': ObjectId(id_materia)})
    return {
        "ok":"ok"
    }

@user_admin.route('/updateMateria/<id>',methods=["PUT"])
def updateMateria(id):
    # http://localhost:5000/updateMateria/21546546478
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
    # [{"_id":"adsasd"},{{"_id":"asdasdasd"}}]
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
    if idQuery['estado']:  # False | True 
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
    print(users)
    queryCiclo = mydb.AssingParalelo.find_one({"id_ciclo":str(id_ciclo),"paralelo":str(paralelo)})
    if queryCiclo:
        if str(queryCiclo['paralelo']) == str(paralelo):
            mydb.AssingParalelo.update_one({"id_ciclo":str(id_ciclo)},{"$push":{"students":{"$each":users}}})
            response = jsonify({
                "ok":"ok",
            })
            response.status = 201;
            return response;

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

# Notes 

@user_admin.route('/createNotaStudent',methods=["POST"])
def createNoteStudent():
    json = request.json
    id = json['id_student']
    fallos = json['fallos']
    nota = 0;
    if(fallos == 0):
        nota = 100;
    if(fallos == 1 ):
        nota = 80;
    if(fallos == 2):
        nota = 60;
    if(fallos == 3):
        nota = 40;
    if(fallos == 4):
        nota = 20;
    if(fallos == 5):
        nota = 0;
    mydb.notas.insert_one({"id_student":id,"calificacion":nota,"fallos": fallos})

    return {
        "ok":"ok"
    }



@user_admin.route('/createScore',methods=["POST"])
def createScore():

    json = request.json
    id = json['id_student']
    score = json['score']

    mydb.scores.insert_one({"id_student":id,"score":score})

    return {
        "ok":"success"
    }

# 
@user_admin.route('/createNoteAdmin',methods=["POST"])
def createNoteAdmin():
    json = request.json

    id_ciclo = json['id_ciclo']
    nota_inicial = json['nota_inicial']
    nota_final = json['nota_final']
    paralelo = json['paralelo']
    estado = json['estado']

    doc = mydb.notasAdmin.find({"id_ciclo":id_ciclo})
    # 0 , 1 , 2
    # ['adsa','asdasd']
    # [{"_id":"asdasda","paralelo":"A","estado":True},{"_id:":"adsasda",parasdas}]
    for row in doc:
        # verdadero and  falso => falso
        # verdadero and verdadero and verdadero  => verdadero

        # 
        # A == A and true === false 
        if row['paralelo'] == paralelo and row['estado'] == estado:
            res = jsonify({
                "message":"nota ya existe"
            })
            res.status = 400;
            return res;
        #   A                   A  true      and True !=  False
        if row['paralelo'] == paralelo and row['estado'] != estado:
            if estado:
                mydb.notasAdmin.update_one({"id_ciclo":id_ciclo,"paralelo":paralelo},{"$set":{"estado":True}})
                res = jsonify({
                    "message":"nota modificada a true"
                })
                res.status = 200;
                return res;
            else:    
                mydb.notasAdmin.update_one({"id_ciclo":id_ciclo,"paralelo":paralelo},{"$set":{"estado":False}})
                res = jsonify({
                    "message":"nota modificada a false"
                })
                res.status = 200;
                return res;
    mydb.notasAdmin.insert_one({"id_ciclo":id_ciclo,"nota_inicial":nota_inicial,"nota_final":nota_final,"paralelo":paralelo,"estado":estado})
    return {"ok":"ok"}


@user_admin.route('/getNotesAdmin')
def getNotesAdmin():
    notas = [dict(row ) for row in mydb.notasAdmin.find()]
    return json.dumps(notas,default=json_util.default)


@user_admin.route('/deleteNotes/<id>',methods=["DELETE"])
def deleteNotes(id):
    _id = id
    mydb.notasAdmin.delete_one({"_id",ObjectId(_id)})
    return {
        "ok":"ok"
    }

# http://localhost:5000/deleteNotes/121321212312

#Get Users Paralelos

@user_admin.route('/getUsersParalelos')
def userGetParalelos(): 
    args = request.args
    paralelo = args.get('paralelo')
    
    if not paralelo:
        response = jsonify(message="paralelo no encontrado",category="error",status=400)
        response.status = 400;
        return response;
    
    ciclo = mydb.ciclo_academico.find_one({"estado":True})
    paraleloQuery = mydb.AssingParalelo.find_one({"id_ciclo":str(ciclo["_id"])});
 
    

    if not paraleloQuery:
        response = jsonify(message="paralelo asignado al ciclo no se encuentra",category="error",status=400)
        response.status = 400;
        return response;

  

    datos = []
    # print(paraleloQuery["id_ciclo"])
    # print(ciclo["_id"])
    if str(paraleloQuery["id_ciclo"])  == str(ciclo["_id"]):
       
        for user in paraleloQuery['students']:
            userFound = mydb.users.find_one({"_id":user})
            datos.append(userFound)
            print(userFound)
        
        response =  json.dumps(datos,default=json_util.default)
        return response
        

     # paraleloArray = [dict(row) for row in paralelo]

    

    
    
    
    

   
   

    # for rowArray in paraleloArray:
        # print("\n",rowArray)
        # print([dict(roww) for roww in user])
        # for rowArr in rowArray['students']:

    # response =  json.dumps(datos,default=json_util.default)
    # return response;
    return {"ok":True}
       

