from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB 클라이언트 생성
username = ""
password = ""
host = ""
port = ""
database_name = "test"

client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
db = client[database_name]  # 사용할 데이터베이스
collection = db["vector"]  # 사용할 컬렉션


def insert_portfolio_with_vector(data):
    document = {"vector": data['vector'], "portfolio_id": data['portfolio_id'],
                "access_url": data['access_url']}
    result = collection.insert_one(document)
    print("Inserted document ID:", result.inserted_id)


def find_vector_with_id():
    return collection.find({}, {"vector": 1, "_id": 1})


def find_by_id(document_id):
    return collection.find_one({"_id": ObjectId(document_id)})
