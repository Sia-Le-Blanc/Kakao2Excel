import sqlite3
import shutil

# 원본 복사 (이미 했다면 생략)
shutil.copyfile("KakaoCopy.sqlite", "KakaoFinal.sqlite")

# 연결 시 WAL 파일 포함하도록 옵션 추가
conn = sqlite3.connect("KakaoFinal.sqlite", isolation_level=None)
cursor = conn.cursor()

# 테이블 목록 확인
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print(table[0])
