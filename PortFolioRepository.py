import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("MYSQL_host"),                  # MySQL 서버 호스트 (Spring 설정의 'localhost')
    user=os.getenv("MYSQL_USER"),                         # MySQL 사용자 이름 (Spring 설정의 'root')
    password=os.getenv("MYSQL_PASSWORD"),                      # MySQL 비밀번호 (Spring 설정의 'root')
    database=os.getenv("MYSQL_DATABASE"),           # 사용할 데이터베이스 (Spring 설정의 'cre8_local')
    charset="utf8"                        # 문자 인코딩 설정
)

def get_portfolio():
    # 커서 객체 생성

    cursor = db.cursor()

    # SQL 쿼리 실행
    cursor.execute("SELECT portfolio_id, access_url FROM portfolio_image")

    # 쿼리 결과 가져오기
    results = cursor.fetchall()

    print(results)

    # 커서 및 연결 닫기
    cursor.close()


    return results