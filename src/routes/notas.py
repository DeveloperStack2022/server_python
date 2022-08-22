from flask import Blueprint, request, jsonify
from functions_jwt import write_token, validate_token
from database import mydb


notas = Blueprint('notas',__name__)

@notas.route('/createNota',methods=['POST'])
def createNota():
    data = request.get_json()

    
