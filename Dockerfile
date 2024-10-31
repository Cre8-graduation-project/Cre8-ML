# 베이스 이미지 설정
FROM python:3.9

# 작업 디렉토리 생성
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Flask 앱과 모델 파일 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "main.py"]