import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QCKGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        #settings
        self.grid_size = 30
        self.grid_squares = 4

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self.penLight = QPen(self._color_light)
        self.penLight.setWidth(2)
        self.penDark = QPen(self._color_dark)
        self.penDark.setWidth(3)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height) # // equals divide and round to int


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # we'll create our grid here
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # compute all lines to be draw
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if (x % (self.grid_size * self.grid_squares) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if (y % (self.grid_size * self.grid_squares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))

        # draw lines
        painter.setPen(self.penLight)
        painter.drawLines(*lines_light)  # * equals pass array as individual elements

        painter.setPen(self.penDark)
        painter.drawLines(*lines_dark)
