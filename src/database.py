import pymongo

myClient = pymongo.MongoClient('mongodb://localhost:27017/');
mydb = myClient['projectSGA']

