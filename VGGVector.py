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

