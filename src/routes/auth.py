from flask import Blueprint, request, jsonify
from functions_jwt import write_token, validate_token
from database import mydb
import bcrypt
from functions_jwt import write_token


auth = Blueprint('auth',__name__);

@auth.route('/login',methods=['POST'])
def login():
    data = request.get_json()
   
    username = data['username']
    password = data['password']
    result = mydb.users.find_one({"username":username})
    
    if not result:
        return "User not exist"
    #
    passwordhash = result['password']
    if bcrypt.hashpw(data['password'].encode('utf-8'),result['password'])  == result['password']:
        token = write_token({'username':result['username'],'rol_id':result['rol_id']})
        
        return "existe"
    else:
        return "password incorrect"

    
    