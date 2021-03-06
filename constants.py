#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
from os import path
from sys import argv
from PyQt5.QtGui import QColor

USER32 = ctypes.windll.user32
CELL_BLACK_COLOR = QColor(150, 50, 0)
CELL_WHITE_COLOR = QColor("White")
CHECKER_WHITE_COLOR = QColor(255, 219, 88)
CHECKER_BLACK_COLOR = QColor(0, 0, 0, 255)
KING_COLOR = QColor("Gold")
FRAME_COLOR = QColor(255, 0, 0)
WALKING_COLOR = QColor(100, 200, 40)
DIRECTION_COEFFICIENTS = {CHECKER_WHITE_COLOR.getRgb(): 1,
                          CHECKER_BLACK_COLOR.getRgb(): -1}
SCRIPT_DIR = path.dirname(argv[0])
