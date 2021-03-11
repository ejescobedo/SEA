import pymongo
from bson import ObjectId


def remove_data(document_id):
    document = collection.delete_one({'_id': ObjectId(document_id)})
    return document.acknowledged


#All the information from all elements
#List of all objects
def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)

#all the information of one element
def get_single_data(document_id):
    """
    get document data by document ID
    :param document_id:
    :return:
    """
    data = collection.find_one({'_id': ObjectId(document_id)})
    return data



#update data
def update_or_create(document_id, data):
    """
    This will create new document in collection
    IF same document ID exist then update the data
    :param document_id:
    :param data:
    :return:
    """
    # TO AVOID DUPLICATES - THIS WILL CREATE NEW DOCUMENT IF SAME ID NOT EXIST
    document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data}, upsert=True)
    return document.acknowledged



#Returning the ID of the created data
def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    document = collection.insert_one(data)
    return document.inserted_id



#myclient = pymongo.MongoClient("cluster0-shard-00-00.mtrde.mongodb.net:27017")
#connection = pymongo.MongoClient('cluster0-shard-00-02.mtrde.mongodb.net', 27017)
#mydb = connection["myDB_01"]  #If it doesn't exist, it will create it
                              #not created if empty database
#collection = mydb['my_collection-01']  #Collection, but need to add data into collection

#data = {'Name': "Edgar"}

#collection.insert_one(data)

''''
connection = pymongo.MongoClient('cluster0-shard-00-02.mtrde.mongodb.net')
mydb = connection["myDB_01"]
collection = mydb['my_collection-01']
data = {'Name': "Edgar"}
collection.insert_one(data)
'''''

#Creating connection
connection = pymongo.MongoClient('localhost', 27017)
######connection = pymongo.MongoClient('cluster0-shard-00-00.bjij3.mongodb.net, 27017')
#####connection = pymongo.MongoClient("mongodb+srv://ejescobedo:maps1010@cluster0.bjij3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#####db = client.test


#creating new database -- will look for database, if not exist, will create one, if exist, just establish connection
#if empty database, it will not be created, not allowed, need to add info to database
database = connection['mydb_01']

#create collection, but still no info, need to add something to the collection
collection = database['mycol_01']

#Creating actual data
data = {"Scan": "1____", "Name of Scan": "number _____", "Execution Number": "3142____________", "Start Time": "10:20_____", "End Time": "11:40___",
        "Scanned IPs": "20_________", "Successful Execution/Failure": "25__________________________"}

#adding data to collection
#Every time you run it it will create the data, even if it is the same information
collection.insert_one(data)

#adding data and defining the ID, it cannot be repeated
#data = {"_id": "user1", "Name": "El sebas"}
#collection.insert_one(data)

data = {"Scan": "11111", "Name of Scan": "number 11111", "Execution Number": "3142111111111111", "Start Time": "10:2011111", "End Time": "11:40111",
        "Scanned IPs": "20111111111", "Successful Execution/Failure": "2511111111111111111111111111"}
#update_or_create("user1", data)

#x = get_single_data('604433e255aa2a7f763d933f')
#print(x)
y = get_multiple_data()
y = list(y)
print(type(y))
for element in y:
    print(element.get("Scan"))
def get_info_from_database(connection, database, collection):
    data = collection.find()
    return list(data)
    y = get_multiple_data()
    y = list(y)
    print(type(y))
    for element in y:
        print(element.get("Scan"))

connection.close()