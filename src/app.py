
from flask import Flask,request,Response,jsonify
from flask_pymongo  import PyMongo
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_uuid import FlaskUUID
from flask_cors   import CORS
import uuid
#
from database import mydb 
#
from routes.admin import user_admin
from routes.auth import auth

app  = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost/projectSGA'
# mongo  = PyMongo(app) 
api = Api(app)

FlaskUUID(app)

#settings 
CORS(app)

app.register_blueprint(user_admin,url_prefix="/api")
app.register_blueprint(auth,url_prefix="/api")
# Create Role POST 
@app.route('/createRole',methods=['POST'])
def createRole():
    name_role = request.json['name_role']

    if name_role : 
        # roleCollection = mydb['role']
        id_role = mydb.db.role.insert_one({"_id":str(uuid.uuid4()),"name_role":name_role}).inserted_id
        print(id_role)
        return id_role
    else:
        return {"message":"Icomplete Data"}

@app.route('/',methods=['GET'])
def home():

    return {'message':"Welcome"}

if __name__ == '__main__':
    app.run(debug=True)