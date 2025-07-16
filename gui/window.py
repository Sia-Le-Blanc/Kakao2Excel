# gui/window.py

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit,
    QLabel, QPushButton, QCheckBox, QDateEdit, QSpacerItem,
    QSizePolicy, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon

from parser.kakao_parser import load_all_chat_partners, load_chat_data

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("카톡 정리 귀찮아")
        self.setFixedSize(900, 600)
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.db_path = None
        self.current_chat_data = []
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 좌측: 대화 상대 리스트
        self.friend_list = QListWidget()
        self.friend_list.setFixedWidth(200)
        self.friend_list.itemClicked.connect(self.on_friend_selected)

        # 우측: 전체 구성
        right_layout = QVBoxLayout()

        # 📂 DB 열기 버튼
        self.btn_open_db = QPushButton("📂 대화 DB 열기")
        self.btn_open_db.clicked.connect(self.on_open_db_clicked)

        # 대화 미리보기
        self.chat_preview = QTextEdit()
        self.chat_preview.setReadOnly(True)
        self.chat_preview.setPlaceholderText("대화 내용을 선택하세요")

        # 날짜, 체크박스, 저장 버튼
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

        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(self.checkbox_mine)
        filter_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        filter_layout.addWidget(self.btn_export)

        # 우측에 위젯 배치
        right_layout.addWidget(self.btn_open_db)
        right_layout.addWidget(self.chat_preview)
        right_layout.addLayout(filter_layout)

        main_layout.addWidget(self.friend_list)
        main_layout.addLayout(right_layout)

    def on_open_db_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "카카오톡 대화 DB 선택", "", "SQLite DB 파일 (*.db *.sqlite);;모든 파일 (*)"
        )
        if file_path:
            try:
                self.db_path = file_path
                partners = load_all_chat_partners(self.db_path)
                self.friend_list.clear()
                for name in partners:
                    self.friend_list.addItem(name)
            except Exception as e:
                QMessageBox.critical(self, "불러오기 실패", f"대화 DB를 불러오는 데 실패했습니다:\n{e}")

    def on_friend_selected(self, item):
        if not self.db_path:
            return

        name = item.text()
        try:
            self.current_chat_data = load_chat_data(self.db_path, name)
        except Exception as e:
            QMessageBox.critical(self, "대화 불러오기 실패", f"{name} 대화를 불러오지 못했습니다:\n{e}")
            self.current_chat_data = []

        self.update_preview_based_on_checkbox()

    def update_preview_based_on_checkbox(self):
        include_mine = self.checkbox_mine.isChecked()
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()

        self.chat_preview.clear()

        for msg in self.current_chat_data:
            try:
                msg_date = QDate.fromString(msg["date"], "yyyy.MM.dd").toPyDate()
            except Exception:
                continue

            if msg["sender"] == "나" and not include_mine:
                continue
            if not (date_from <= msg_date <= date_to):
                continue

            line = f'{msg["date"]} {msg["time"]}, {msg["sender"]}: {msg["text"]}'
            self.chat_preview.append(line)
