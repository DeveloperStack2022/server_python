from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with


 class MateriaApi(Resource):
    def get(self):
        # materias =