from flask import Blueprint, request, jsonify,Response
from functions_jwt import write_token, validate_token
from database import mydb
import bcrypt
from functions_jwt import write_token
from bson.objectid  import ObjectId


auth = Blueprint('auth',__name__);

@auth.route('/login',methods=['POST'])
def login():
    data = request.get_json()
   
    username = data['username']
    password = data['password']
    result = mydb.users.find_one({"username":username})
    if not result:
        response = jsonify({
            "error":True,
            "message":"Usuario no existe",
            "token":"null"
        })      
        response.status_code = 200
        return response
    #
    rolId = result['rol_id']
    rolData = mydb.db.role.find_one({"_id":rolId})
    passwordhash = result['password']
    if bcrypt.hashpw(data['password'].encode('utf-8'),result['password'])  == result['password']:
        token = write_token({'username':result['username'],'name_rol':rolData['name_role']})
        response = jsonify({
            "token":str(token),
            "error":False,
            "message":""
        })
        response.status_code = 200
        return response
    else:
        return "password incorrect"

    
    