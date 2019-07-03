import pymongo 
import pandas as pd

def get_from_db(collection, query_dict, fields_return_dict, db_name='MLB'):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name] #select database
    db_collection = db[collection] #select the collection within the databse
    df = pd.DataFrame(list(db_collection.find(query_dict,fields_return_dict))) #convert entire collection to pandas DataFrame
    return df
