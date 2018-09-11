#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, qApp, QLabel


class EndGameWindow(QWidget):

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
        self.setGeometry(300, 300, 500, 200)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setWindowIcon(QIcon('resources/checker.png'))
        self.setWindowTitle('Result')
        self.setFixedSize(self.size())

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0, 255, 0))
        qp.setFont(QFont('Decorative', 20))
        qp.drawText(QPaintEvent.rect(), Qt.AlignCenter, self.result_text)
        qp.end()

    def play_again(self):
        from startMenu import StartMenu
        self.start_window = StartMenu()
        self.start_window.show()
        self.close()
