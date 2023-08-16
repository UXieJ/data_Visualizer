from PySide6.QtCore import (QThread)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QWidget)

import clientVisualization
from dataParse import *
from utils_thread import *


class MainBoss(QWidget, clientVisualization.Ui_gui):

    def __init__(self):
        QWidget.__init__(self)
        clientVisualization.Ui_gui.__init__(self)
        self.setupUi(self)

        # Initialize the custom QGraphicsScene
        self.scene = GridGraphicsScene(self)

        self.graphicsView.setMouseTracking(True)

        # Set the custom scene to the QGraphicsView
        self.graphicsView.setScene(self.scene)
        width = 600
        height = 490
        #未设置场景边界矩形，QGraphicsScene将使用itemsBoundingRect()返回的所有项目的边界区域作为场景边界矩形。但是，itemsBoundingRect()是一个相对耗时的函数，
        self.scene.setSceneRect(-width / 2, -height / 2, width, height)
        # Set the scene for the graphics

        # Optionally, set render hints for the view
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.currentItems = []
        self.connectButton.clicked.connect(self.udp_connect_click)
        self.cancelButton.clicked.connect(self.udp_disconnect_click)

        self.graphicsView.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

    def udp_connect_click(self):
        if self.connectButton.text() == 'connect':
            self.parse_udp = UdpReceiver()
            self.udp_thread = parseNetThread(self.parse_udp)
            self.udp_thread.fin.connect(self.parseData)
            # process_data = UdpReceiver(self.parse_udp.results)
            self.parse_udp.dataProcessed.connect(self.drawOnGraphicsScene)
            # print("process data length: ", len(process_data.cal_xy))


    def drawOnGraphicsScene(self):
        grouped_points = self.parse_udp.grouped_data

        # Remove previous items from the scene
        for item in self.currentItems:
            self.scene.removeItem(item)
        self.currentItems.clear()

        for circleNumber, points in grouped_points.items():
            x_values = points["x"]
            y_values = points["y"]
            amp_values = points["first_return_amp"]
            angular_values = points["angular"]
            for x, y, amp, angular in zip(x_values, y_values, amp_values, angular_values):
                data = {
                    "x": x,
                    "y": y,
                    "amp": amp,
                    "angular": angular
                }
                pointItem = MyItem(x, y, data)
                self.scene.addItem(pointItem)
                self.currentItems.append(pointItem)
                #Clear the list after adding the points to the scene
        # all_points.clear()

    def centerItemInScene(self, item):
        item_center = item.center()
        scene_rect = self.scene.sceneRect()
        scene_center = QPointF(scene_rect.width() / 2, scene_rect.height() / 2)
        offset = scene_center - item_center
        item.setPos(item.pos() + offset)

    def parseData(self):
        self.udp_thread.start(priority=QThread.HighestPriority)

    def udp_disconnect_click(self):
        if hasattr(self, 'parse_udp') and hasattr(self.parse_udp, 'udpSocket'):
            self.parse_udp.udpSocket.close()
            self.udp_thread.quit()
            self.udp_thread.wait()
            print("Connection closed")


if __name__ == '__main__':
    app = QApplication([])
    visMain = MainBoss()
    visMain.show()
    app.exec()
