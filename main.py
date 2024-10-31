from flask import Flask, Response

import MongoVectorRepository
import PortFolioRepository
import VGGVector

app = Flask(__name__)


@app.route('/today/vector', methods=['POST'])
def save_today_vector():
    portfolio = PortFolioRepository.get_portfolio()

    for portfolio_id, access_url in portfolio:
        if not MongoVectorRepository.find_by_access_url(access_url):
            try:
                vector = VGGVector.extract_features(access_url)

                print(vector.tolist())

                document = {
                    "portfolio_id": portfolio_id,
                    "access_url": access_url,
                    "vector": vector.tolist()  # numpy 배열을 리스트로 변환
                }

                MongoVectorRepository.insert_portfolio_with_vector(document)

            except Exception as e:
                print(f"Error processing URL {access_url}: {e}")

    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
