from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.metrics.pairwise import cosine_similarity
import requests
from io import BytesIO
from PIL import Image
import numpy as np

model = VGG16(weights="imagenet", include_top=False, pooling="avg")


def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = img.resize((224, 224))  # VGG16 모델에 맞게 크기 조정
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


# 이미지 특징 추출 함수
def extract_features(url):
    img_array = load_image_from_url(url)
    features = model.predict(img_array)
    return features.flatten()


def find_most_similar_image_with_vector(query_image_url, query_results, top_n=5):

    query_features = extract_features(query_image_url)
    feature_list = [doc['vector'] for doc in query_results]
    similarities = cosine_similarity([query_features], feature_list).flatten()
    sorted_indices = np.argsort(similarities)[::-1]  # 내림차순 정렬
    top_indices = sorted_indices[:top_n]  # 상위 N개 인덱스 추출

    # 상위 N개의 유사 이미지 ID와 유사도 점수 추출
    similar_images = [
        (query_results[i]['_id'], similarities[i]) for i in top_indices
    ]

    return similar_images
