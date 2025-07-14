# gui/window.py

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit,
    QLabel, QPushButton, QCheckBox, QDateEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("카톡 정리 귀찮아")
        self.setFixedSize(900, 600)
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.current_chat_data = []  # 대화 데이터 전체 저장
        self.init_ui()

    def init_ui(self):
        # 전체 수평 레이아웃
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 좌측: 대화 상대 리스트
        self.friend_list = QListWidget()
        self.friend_list.setFixedWidth(200)
        self.friend_list.addItem("홍길동")
        self.friend_list.addItem("김철수")
        self.friend_list.itemClicked.connect(self.on_friend_selected)

        # 우측: 대화 미리보기 + 필터 + 버튼
        right_layout = QVBoxLayout()

        self.chat_preview = QTextEdit()
        self.chat_preview.setReadOnly(True)
        self.chat_preview.setPlaceholderText("대화 내용을 선택하세요")

        # 필터 옵션: 날짜 선택 + 체크박스 + 저장 버튼
        filter_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())

        self.checkbox_mine = QCheckBox("내 메시지도 포함")
        self.checkbox_mine.setChecked(False)
        self.checkbox_mine.stateChanged.connect(self.update_preview_based_on_checkbox)

        self.btn_export = QPushButton("💾 엑셀로 저장")

        # 필터 레이아웃 구성
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(self.checkbox_mine)
        filter_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        filter_layout.addWidget(self.btn_export)

        # 우측 레이아웃 구성
        right_layout.addWidget(self.chat_preview)
        right_layout.addLayout(filter_layout)

        # 전체 배치
        main_layout.addWidget(self.friend_list)
        main_layout.addLayout(right_layout)

    def on_friend_selected(self, item):
        # 대화 상대 선택 시 실행되는 함수 (여기선 샘플 메시지로 가상 구현)
        name = item.text()

        # 샘플 대화 데이터 (추후 kakao_parser로 대체)
        self.current_chat_data = [
            {"date": "2025.07.14", "time": "15:21", "sender": "나", "text": "안녕?"},
            {"date": "2025.07.14", "time": "15:22", "sender": name, "text": "잘 지냈어?"},
            {"date": "2025.07.15", "time": "09:02", "sender": "나", "text": "오늘 뭐해?"},
            {"date": "2025.07.15", "time": "09:04", "sender": name, "text": "출근 중이야!"}
        ]

        self.update_preview_based_on_checkbox()

    def update_preview_based_on_checkbox(self):
        # 체크박스 상태에 따라 미리보기 내용 필터링
        include_mine = self.checkbox_mine.isChecked()
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()

        self.chat_preview.clear()

        for msg in self.current_chat_data:
            msg_date = QDate.fromString(msg["date"], "yyyy.MM.dd").toPyDate()
            if msg["sender"] == "나" and not include_mine:
                continue
            if not (date_from <= msg_date <= date_to):
                continue
            line = f'{msg["date"]} {msg["time"]}, {msg["sender"]}: {msg["text"]}'
            self.chat_preview.append(line)
