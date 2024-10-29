# db_connection.py
from sqlalchemy import create_engine, text, exc

# 데이터베이스 엔진 생성
engine = create_engine("mysql+pymysql://test:test@localhost/test4movies", pool_pre_ping=True)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(result.scalar())
    except exc.DBAPIError as e:
        if e.connection_invalidated:
            print("연결이 무효화되었습니다.")