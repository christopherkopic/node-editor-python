from node_graphics_node import QCKGraphicsNode
from node_content_widget import QCKNodeContentWidget
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM

class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene
        self.title = title

        self.content = QCKNodeContentWidget()
        self.grNode = QCKGraphicsNode(self)

        self.socket_spacing = 20;

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()
    def setPoa(self, x, y):
        self.grNode.setPos(x,y)

    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode._padding - self.grNode.edge_size - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()
