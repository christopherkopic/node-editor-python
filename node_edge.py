from node_graphics_edge import *

class Edge():
    def __init__(self, scene, start_socket, end_socket):
        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.grEdge = QCKGraphicsEdgeDirect(self)
        self.scene.grScene.addItem(self.grEdge)
