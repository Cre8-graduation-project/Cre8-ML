from dotenv import load_dotenv
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests.auth import HTTPBasicAuth
import os

load_dotenv()


host = os.getenv('ELASTIC_HOST')
region = os.getenv('ELASTIC_REGION')
service = os.getenv('ELASTIC_SERVICE')
user = os.getenv('ELASTIC_USER')
password = os.getenv('ELASTIC_PASSWORD')

auth = HTTPBasicAuth(user, password)

es = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20
)

index_name = "portfolio"


def insert_portfolio_image_with_vector_elastic(data):
    document = {
        "vector": data['vector'],
        "portfolioId": data['portfolio_id'],
        "accessUrl": data['access_url'],
        "portfolioImageId": data['portfolio_image_id']
    }

    result = es.index(index=index_name, body=document)
    print("Inserted document ID:", result['_id'])


def find_vector_with_id():
    query = {
        "_source": ["vector"],
        "query": {"match_all": {}}
    }
    response = es.search(index=index_name, body=query)
    return [(hit['_id'], hit['_source']['vector']) for hit in response['hits']['hits']]


def find_by_id(document_id):
    try:
        result = es.get(index=index_name, id=document_id)
        return result['_source']
    except Exception as e:
        print("Error:", e)
        return None


def find_by_portfolio_image_id(portfolio_image_id):
    query = {
        "query": {
            "term": {"portfolioImageId": portfolio_image_id}
        }
    }
    response = es.search(index=index_name, body=query)
    return response['hits']['hits'][0]['_source'] if response['hits']['hits'] else None


def find_by_access_url(access_url):
    query = {
        "query": {
            "term": {"access_url": access_url}
        }
    }
    response = es.search(index=index_name, body=query)
    return response['hits']['hits'][0]['_source'] if response['hits']['hits'] else None


def find_similar_image(query_vector):
    cosine_query = {
        "size": 5,
        "query": {
            "knn": {
                "vector": {
                    "vector": query_vector,
                    "k": 5
                }
            }
        }
    }

    response = es.search(index=index_name, body=cosine_query)

    similar_images = []

    # 결과 처리
    for hit in response['hits']['hits']:
        most_similar_mongo_id = hit['_source']['portfolioImageId']
        similarity_score = hit['_score']

        similar_images.append((most_similar_mongo_id, similarity_score))

    return similar_images
