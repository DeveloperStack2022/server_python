from jwt import encode,decode
from jwt import exceptions
from datetime import datetime,timedelta
from flask import jsonify


def expires_date(days:int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

# Create Token
def write_token(data:dict):
    token = encode(payload={**data,'exp':expires_date(2)},key='secret',algorithm="HS256")
    return token;

# Valid / Verifytoken
def validate_token(token,output=False):
    try:
        if output:
            return decode(token,key='secret',algorithms=["HS256"])
        decode(token,key='secret',algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
