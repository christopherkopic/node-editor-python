from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import QCKGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

class QCKGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)

        self.grScene = grScene
        self.initUI()
        self.setScene(grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.1
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [-20,20]

        self.edgeDragStartThreshhold = 10

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altKeyPress()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altKeyRelease()
        else:
            super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def altKeyPress(self):
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def altKeyRelease(self):
        self.setDragMode(QGraphicsView.NoDrag)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if type(item) is QCKGraphicsSocket:
            if self.mode is MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode is MODE_EDGE_DRAG:
            success = self.edgeDragEnd(item)
            if success: return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)

        if self.mode is MODE_EDGE_DRAG:
            new_lmb_release_scene_pos = self.mapToScene(event.pos())
            dist = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos

            if (dist.x()*dist.x() + dist.y()*dist.y()) > self.edgeDragStartThreshhold*self.edgeDragStartThreshhold:
                success = self.edgeDragEnd(item)
                if success: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        print("start dragging edge")
        print(" Assign start socket")

    def edgeDragEnd(self, item):
        """returns True to skip rest of code"""
        self.mode = MODE_NOOP
        print("End dragging Edge")

        if type(item) is QCKGraphicsSocket:
            print(" Assign end socket")
            return True

        return False

    def wheelEvent(self, event):
        #calculate zoom factor
        zoomOutFactor = 1 / self.zoomInFactor
        #calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
        #set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
