import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')

mydb = None


def get_db():
    global mydb
    if mydb is None:
        try:
            conn_str = f"mongodb+srv://{username}:{password}@cluster0.zv44hy3.mongodb.net/?retryWrites=true&w=majority"
            client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
            mydb = client["database"]
        except:
            print("Unable to connect to the server.")
            pass
    return mydb