import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QCKGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        #settings
        self.grid_size = 20

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")

        self.penLight = QPen(self._color_light)
        self.penLight.setWidth(1)

        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height) # // equals divide and round to int

        self.setBackgroundBrush(self._color_background)

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
        lines_light = []
        for x in range(first_left, right, self.grid_size):
            lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            lines_light.append(QLine(left, y, right, y))


        # draw lines
        painter.setPen(self.penLight)
        painter.drawLines(*lines_light)  # * equals pass array as individual elements
