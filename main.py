# main.py

import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.window import MainWindow

def main():
    app = QApplication(sys.argv)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)

        # GUI 팝업으로 오류 표시
        QMessageBox.critical(None, "애플리케이션 오류", f"예기치 못한 오류 발생:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
