import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),                  # MySQL 서버 호스트
        user=os.getenv("MYSQL_USER"),                  # MySQL 사용자 이름
        password=os.getenv("MYSQL_PASSWORD"),          # MySQL 비밀번호
        database=os.getenv("MYSQL_DATABASE"),          # 사용할 데이터베이스
        charset="utf8"                                 # 문자 인코딩 설정
    )

def get_portfolio_image():
    try:
        # 데이터베이스 커넥션 생성 및 커서 객체 생성
        db = get_db_connection()
        cursor = db.cursor()

        # SQL 쿼리 실행
        cursor.execute("SELECT portfolio_image_id,access_url, portfolio_id FROM portfolio_image")

        # 쿼리 결과 가져오기
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # 커서 및 연결 닫기
        if cursor:
            cursor.close()
        if db:
            db.close()