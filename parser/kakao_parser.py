# parser/kakao_parser.py

import sqlite3

def load_all_chat_partners(db_path):
    """
    대화 상대 리스트(room_name 또는 friend_name)를 불러옴
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT DISTINCT room_name FROM messages")
        result = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print("대화 상대 목록 불러오기 실패:", e)
        result = []

    conn.close()
    return result


def load_chat_data(db_path, room_name):
    """
    특정 대화방(room_name)의 전체 메시지를 로드하여 리스트로 반환
    - 반환 형식: [{date, time, sender, text}]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT date, time, sender, message FROM messages WHERE room_name = ? ORDER BY date ASC, time ASC",
            (room_name,)
        )
        raw = cursor.fetchall()
    except Exception as e:
        print("대화 내용 불러오기 실패:", e)
        raw = []

    chat_data = []
    for row in raw:
        try:
            date_str, time_str, sender, message = row
            chat_data.append({
                "date": date_str,
                "time": time_str,
                "sender": sender,
                "text": message
            })
        except Exception:
            continue

    conn.close()
    return chat_data
