import pandas as pd
import numpy as np 
import pymongo as mongo
import os
import datetime as dt  


def insert_data(data):
    
    import pandas as pd 
    try: 
        client = mongo.MongoClient("mongodb://localhost:27017")
        database = client["Planes_Crash_data"]
        collection = database["Planes_Data"]
        data_dict = data.to_dict("records")
        collection.insert_many(data_dict)
    except Exception as e:
        print(e)


def time_format(x):
    try:
        time = str(x).strip(" ")
        if len(time)==4:
            return str(dt.datetime.strptime(f"{time[:2]}:{time[-2:]}","%H:%M").time())
        elif("c" in time):
            if ("c:" in time):
                time = time.split("c:")[1]
                return str(dt.datetime.strptime(time.strip(" "),"%H:%M").time())
            else:
                time = time.split("c")[1]
                return str(dt.datetime.strptime(time.strip(" "),"%H:%M").time())
        elif("z" in time):
            time = time.split("Z")[0]
            return str(dt.datetime.strptime(time.strip(" "),"%H:%M").time()) 
        elif len(time)==3:
            return str(dt.datetime.strptime(f"{time[:1]}:{time[-2:]}","%H:%M").time())
        else:
            return x
    except:
        return dt.datetime.strptime("00:00","%H:%M").time()          
def validate_num(aboard):
    aboard = aboard.split("(")[0].strip(" ")
    try:
        return int(aboard)
    except:
        return 0      

def passenger_num(passenger):
    passenger = passenger.split("passengers:")[1].split(" ")[0]
    try:
        return int(passenger)
    except:
        return 0

def crew_num(crew):
    crew = crew.split("crew:")[1].split(")")[0].strip(" ")
    try:
        return int(crew)
    except:
        return 0

files_names = os.listdir("Planes_Db_files")
for name in files_names:

    files_table = pd.read_csv(f"Planes_db_files\{name}",index_col="Unnamed: 0")
    files_table = files_table.replace("?",0)
    files_table["Date"] = pd.to_datetime(files_table["Date"])
    files_table["Time"] = files_table["Time"].apply(time_format)
    files_table["Aboard_Passengers"] = files_table["Aboard"].apply(passenger_num)
    files_table["Aboard_Crew"] = files_table["Aboard"].apply(crew_num)
    files_table["Aboard"] = files_table["Aboard"].apply(validate_num)
    files_table["Fatalities_Passengers"] = files_table["Fatalities"].apply(passenger_num)
    files_table["Fatalities_Crew"] = files_table["Fatalities"].apply(crew_num)
    files_table["Fatalities"] = files_table["Fatalities"].apply(validate_num)
    files_table["Summary"] = files_table["Summary"].apply(lambda x : (str(x)[:50]+".....").lstrip(" "))
    insert_data(files_table)
    


    
    