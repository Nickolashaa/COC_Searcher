from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import sys
from app.parsing import parsing, ScreenReader, resource_path
import threading
import json


class Searcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('app\\ui\\searcher.ui'), self)
        self.btn.clicked.connect(self.parse)
        self.activated = False
        self.gold_input.setText('0')
        self.elixir_input.setText('0')
        self.dark_elixir_input.setText('0')
        self.stop_event = None
        self.thread = None
        self.reader = ScreenReader()
        with open('saved_data.json', 'r') as f:
            data = json.load(f)
        self.gold_input.setText(str(data["gold"]))
        self.elixir_input.setText(str(data["elixir"]))
        self.dark_elixir_input.setText(str(data["dark_elixir"]))

    def parse(self):
        if self.activated:
            self.activated = False
            self.btn.setText('Старт')
            if self.stop_event:
                self.stop_event.set()
            if self.thread and self.thread.is_alive():
                self.thread.join()
        else:
            try:
                gold = int(self.gold_input.text().replace(' ', ''))
                elixir = int(self.elixir_input.text().replace(' ', ''))
                dark_elixir = int(self.dark_elixir_input.text().replace(' ', ''))
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Вводите только цифры")
                msg.exec()
                return

            self.btn.setText('Стоп')
            self.update()
            self.activated = True

            if self.thread and self.thread.is_alive():
                self.thread.join()  # Дождемся завершения старого потока

            self.stop_event = threading.Event()  # Создаем новый флаг
            self.thread = threading.Thread(
                target=parsing, args=(gold, elixir, dark_elixir, self))
            self.thread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('app\\ui\\pic\\favicon.ico')))
    searcher = Searcher()
    searcher.show()
    sys.exit(app.exec())
