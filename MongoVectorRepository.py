from pymongo import MongoClient
from bson.objectid import ObjectId

from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB 클라이언트 생성
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
database_name = os.getenv("MONGO_DATABASE")

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


def find_by_access_url(access_url):
    return collection.find_one({"access_url": access_url})
