from flask_mongoengine import BaseQuerySet
import mongoengine as engine 


class Materia(engine.Document):
    id = engine.ObjectIdField()
    description = engine.StringField(required= True,max_length = 255)
    hora_inicio = engine.StringField(required= True)
    