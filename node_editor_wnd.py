from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import Node
from node_edge import *
from node_graphics_view import QCKGraphicsView

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        #create graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene

        self.addNodes()

        #create graphics view
        self.view = QCKGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

        # self.addDebugContent()

    def addNodes(self):
        self.node1 = Node(self.scene, "General Kenodi", inputs=[1,2,3], outputs=[2])
        self.node2 = Node(self.scene, "General Kenodi", inputs=[1], outputs=[3,2,1])
        self.node3 = Node(self.scene, "General Kenodi", inputs=[1,2], outputs=[3,2])
        self.node1.setPoa(-350, -250)
        self.node3.setPoa(350, -250)

        edge1 = Edge(self.scene, self.node1.outputs[0], self.node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, self.node2.outputs[2], self.node3.inputs[1], edge_type=EDGE_TYPE_BEZIER)

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(3)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)

        text = self.grScene.addText("Hello There!\nGeneral Kenobi!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0,1.0,1.0))

        widget1 = QPushButton("Hello There")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setPos(0, 60)

        # Somewhat broken
        # widget2 = QTextEdit()
        # proxy2 = self.grScene.addWidget(widget2)
        # proxy2.setFlag(QGraphicsItem.ItemIsMovable)

        line = self.grScene.addLine(-200,-200,400,-100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print("Loading ", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
