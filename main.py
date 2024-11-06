import json

from flask import Flask, request, jsonify, Response

import MongoVectorRepository
import PortFolioImageRepository
import VGGVector
import requests

app = Flask(__name__)


@app.route('/today/vector', methods=['POST'])
def save_today_vector():
    portfolio_image = PortFolioImageRepository.get_portfolio_image()

    for portfolio_image_id, access_url, portfolio_id in portfolio_image:
        if not MongoVectorRepository.find_by_portfolio_image_id(portfolio_image_id):
            try:

                vector = VGGVector.extract_features(access_url)
                document = {
                    "portfolio_image_id": portfolio_image_id,
                    "access_url": access_url,
                    "portfolio_id": portfolio_id,
                    "vector": vector.tolist()  # numpy 배열을 리스트로 변환
                }

                MongoVectorRepository.insert_portfolio_image_with_vector(document)

            except Exception as e:
                print(f"Error processing URL {access_url}: {e}")

    return Response(status=200)


@app.route('/find_similar_image', methods=['POST'])
def find_similar_image():
    if 'query_image_file' in request.files:
        query_image = request.files['query_image_file']  # multipart file
    elif 'query_image_url' in request.form:
        query_image = request.form['query_image_url']  # URL (텍스트 데이터)

    result = MongoVectorRepository.find_vector_with_id()
    result_list = list(result)

    similar_images = VGGVector.find_most_similar_image_with_vector(query_image, result_list)

    # 결과를 담을 리스트 초기화
    response_list = []

    # 각 유사 이미지에 대해 MongoDB에서 정보 조회
    for most_similar_mongo_id, similarity_score in similar_images:
        query_result = MongoVectorRepository.find_by_id(most_similar_mongo_id)

        # 결과를 리스트에 추가
        response_list.append({
            "most_similar_portfolio_id": query_result['portfolio_id'],
            "most_similar_portfolio_image_id": query_result['portfolio_image_id'],
            'most_similar_access_url': query_result['access_url'],
            "similarity_score": json.dumps(str(round(similarity_score, 4)))
        })

    # 최종 결과 반환
    return jsonify(response_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
