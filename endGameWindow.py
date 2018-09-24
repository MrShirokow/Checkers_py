#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, qApp, QLabel
from constants import SCRIPT_DIR
from os import path


class EndGameWindow(QWidget):
    """
    Класс окошка результата игры.
    """
    def __init__(self, result_text):
        super().__init__()
        self.result_text = result_text
        self.initUI()

    def initUI(self):
        play_again_btn = QPushButton('Play again', self)
        play_again_btn.clicked.connect(self.play_again)
        play_again_btn.move(100, 150)
        exit_btn = QPushButton('Exit', self)
        exit_btn.clicked.connect(qApp.quit)
        exit_btn.move(300, 150)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setGeometry(300, 300, 500, 200)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        resource_path = path.join(SCRIPT_DIR, 'resources', 'checker.png')
        self.setWindowIcon(QIcon(resource_path))
        self.setWindowTitle('Result')
        self.setFixedSize(self.size())

    def paintEvent(self, q_paint_event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Decorative', 20))
        qp.drawText(q_paint_event.rect(), Qt.AlignCenter, self.result_text)
        qp.end()

    def play_again(self, run_in_test=False):
        """
        Метод, на который опирается кнопка 'Начать заново'.
        При нажатии - игры инициализируется заново.
        Параметр - флаг, который по умолчанию false, за исключением случаев тестирования.
        (Сделано, чтобы при тестировании не открывались всплывающие окна).
        """
        from startMenu import StartMenu
        self.start_window = StartMenu()
        if not run_in_test:
            self.start_window.show()
        self.close()
