from node_graphics_node import QCKGraphicsNode

class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene
        self.title = title

        self.grNode = QCKGraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
