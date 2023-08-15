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

        self.paintPoint = MyItem([])
        self.scene.addItem(self.paintPoint)
        # self.centerItemInScene(self.paintPoint)


        # Optionally, set render hints for the view
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.points_buffer = {}
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
        all_points = []

        for circleNumber, points in grouped_points.items():
            for point in points:
                # act_angular, first_return_dist, first_return_amp, x, y = point
                _, _, _, x, y = point
                all_points.append((x, y))
                #用链表list1能接x,y 然后就不需要additem
        # self.paintPoint = MyItem(all_points)
        # self.paintPoint.setPos(0, 0)
        # self.scene.addItem(self.paintPoint)
        self.paintPoint.setPointList(all_points)

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
