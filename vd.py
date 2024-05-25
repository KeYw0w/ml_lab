import sys

import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QLineEdit, QFileDialog, QLabel, QMainWindow, QDateEdit, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate

from fd.ml_lab.mc import plot_data_with_date_range, predict_with_date_range


class ResultWindow(QWidget):
    def __init__(self, result):
        super().__init__()
        self.initUI(result)

    def initUI(self, result):
        self.setWindowTitle('Результат')
        self.setGeometry(100, 100, 200, 200)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)

        if result == 1:
            pixmap = QPixmap("happy.png")  # Укажите путь к изображению с улыбкой
        else:
            pixmap = QPixmap("sad.png")  # Укажите путь к изображению с грустью

        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(100, 100)

        layout.addWidget(self.image_label)
        self.setLayout(layout)


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Статистика')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.date_edit1 = QDateEdit(self)
        self.date_edit1.setCalendarPopup(True)
        self.date_edit1.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit1)

        self.date_edit2 = QDateEdit(self)
        self.date_edit2.setCalendarPopup(True)
        self.date_edit2.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit2)

        self.btn_show = QPushButton('Вывести', self)
        self.btn_show.clicked.connect(self.show_image)
        layout.addWidget(self.btn_show)

        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def show_image(self):
        try:
            # Сохраняем информацию из полей ввода в переменные
            date1 = self.date_edit1.date().toString("yyyy-MM-dd")
            date2 = self.date_edit2.date().toString("yyyy-MM-dd")
            df = pd.read_csv('data.csv', sep=';')
            # Преобразование столбца 'Дата' в тип данных datetime
            df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
            # Выводим даты в консоль
            # dat{date1}")
            # print(f"Дата 2: {date2}")
            # date1 = '2022-12-05'
            # end_date = '2022-12-07'

            plot_data_with_date_range(df, date1, date2)

            # Замените путь на путь к вашему изображению
            pixmap = QPixmap("image.png")
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setFixedSize(1000, 600)
        except ValueError as e:
            # Отображаем сообщение об ошибке
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка ввода даты")
            # msg.setWindowTitle("Ошибка ввода даты")
            msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное окно')
        self.setGeometry(100, 100, 400, 200)

        widget = QWidget()
        layout = QVBoxLayout()

        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        self.btn_import = QPushButton('Импорт файла', self)
        self.btn_import.clicked.connect(self.import_file)
        layout.addWidget(self.btn_import)

        self.btn_calculate = QPushButton('Рассчитать', self)
        self.btn_calculate.clicked.connect(self.calculate)
        layout.addWidget(self.btn_calculate)

        self.btn_statistics = QPushButton('Статистика', self)
        self.btn_statistics.clicked.connect(self.open_statistics)
        layout.addWidget(self.btn_statistics)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.input_text = ""

    def import_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.text_input.setText(content)

    def calculate(self):
        # Сохраняем текст из поля ввода в переменную
        self.input_text = self.text_input.text()
        print(f"Введенный текст: {self.input_text}")

    # Вызываем функцию predict и открываем окно с результатом
        result = self.predict(self.input_text)
        self.result_window = ResultWindow(result)
        self.result_window.show()


    def predict(self, text):
        predict = predict_with_date_range(text)
    # Простейший пример функции predict
    # На практике здесь будет сложный алгоритм предсказания
        return predict


    def open_statistics(self):
        self.second_window = SecondWindow()
        self.second_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
