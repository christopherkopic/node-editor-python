from node_graphics_node import QCKGraphicsNode
from node_content_widget import QCKNodeContentWidget

class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene
        self.title = title

        self.content = QCKNodeContentWidget()
        self.grNode = QCKGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
