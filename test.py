import pymongo as mongo
import pandas as pd 

client = mongo.MongoClient("mongodb://localhost:27017")
database = client["Planes_Crash_data"]
print("Database is created")
collection = database["Planes_Data"]
# record = {"Record_number":1,"Value":"Test"}
# insert = collection.insert_one(record)
data = collection.find()
for i in data :
     print(i)
