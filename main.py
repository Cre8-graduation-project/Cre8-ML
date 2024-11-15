import json

from flask import Flask, request, jsonify, Response

import MongoVectorRepository
import PortFolioImageRepository
import VGGVector
import requests

import VectorElasticSearch

app = Flask(__name__)


@app.route('/today/vector', methods=['POST'])
def save_today_vector():
    portfolio_image = PortFolioImageRepository.get_portfolio_image()

    for portfolio_image_id, access_url, portfolio_id in portfolio_image:
        if not VectorElasticSearch.find_by_portfolio_image_id(portfolio_image_id):
            try:
                vector = VGGVector.extract_features(access_url)
                document = {
                    "portfolio_image_id": portfolio_image_id,
                    "access_url": access_url,
                    "portfolio_id": portfolio_id,
                    "vector": vector.tolist()  # numpy 배열을 리스트로 변환
                }

                VectorElasticSearch.insert_portfolio_image_with_vector_elastic(document)
            except Exception as e:
                print("저장시 오류 발생 URL {access_url}: {e}")

    return Response(status=200)


@app.route('/portfolio/vector', methods=['POST'])
def save_vector():

    portfolio_image_id = request.args.get('portfolioImageId')

    if portfolio_image_id:

        portfolio_image = PortFolioImageRepository.get_portfolio_image_one(portfolio_image_id)
        try:

            vector = VGGVector.extract_features(portfolio_image[1])
            document = {
                "portfolio_image_id": portfolio_image[0],
                "access_url": portfolio_image[1],
                "portfolio_id": portfolio_image[2],
                "vector": vector.tolist()
            }

            VectorElasticSearch.insert_portfolio_image_with_vector_elastic(document)
        except Exception as e:
            print("저장시 오류 발생 URL {access_url}: {e}")

        return jsonify({"message": "Received", "portfolioImageId": portfolio_image_id}), 200
    else:
        # 파라미터가 없을 경우 에러 응답
        return jsonify({"error": "portfolioImageId is required"}), 400


@app.route('/find_similar_image', methods=['POST'])
def find_similar_image():
    if 'query_image_file' in request.files:
        query_image = request.files['query_image_file']  # multipart file
    elif 'query_image_url' in request.form:
        query_image = request.form['query_image_url']  # URL (텍스트 데이터)

    similar_images = VectorElasticSearch.find_similar_image(VGGVector.extract_features(query_image))

    response_list = []

    for most_similar_mongo_id, similarity_score in similar_images:
        query_result = VectorElasticSearch.find_by_portfolio_image_id(most_similar_mongo_id)

        response_list.append({
            "most_similar_portfolio_id": query_result['portfolioId'],
            "most_similar_portfolio_image_id": query_result['portfolioImageId'],
            'most_similar_access_url': query_result['accessUrl'],
            "similarity_score": json.dumps(str(round(similarity_score, 4)))
        })

    # 최종 결과 반환
    return jsonify(response_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
