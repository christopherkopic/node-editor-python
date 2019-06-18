from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QCKGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00FF00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen.setWidth(2.0)
        self._pen_selected.setWidth(3.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.posSource = [0,0]
        self.posDestination = [100,200]


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        raise NotImplemented("This method has to be overriden in a child class")

class QCKGraphicsEdgeDirect(QCKGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class QCKGraphicsEdgeBezier(QCKGraphicsEdge):
    def updatePath(self):
        pass
