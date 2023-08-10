from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QObject, QPoint, QRect, QThread, Signal, QPointF, QTimer, Qt)
from utils_thread import parseNetThread
from utils_thread import MyItem

from dataParse import *
import clientVisualization
import queue

from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QPushButton, QGraphicsScene,
     QWidget)
from PySide6.QtGui import QPainter, QPen, QColor


class MainBoss(QWidget, clientVisualization.Ui_gui):

    def __init__(self):
        QWidget.__init__(self)
        clientVisualization.Ui_gui.__init__(self)
        self.setupUi(self)
        # Initialize the QGraphicsScene
        self.scene = QGraphicsScene()

        # Set the scene for the graphics vie
        self.graphicsView.setScene(self.scene)

        # Optionally, set render hints for the view
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.points_buffer = {}
        self.connectButton.clicked.connect(self.udp_connect_click)
        self.cancelButton.clicked.connect(self.udp_disconnect_click)
        # self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
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
                #self.scene.addEllipse(x - point_radius, y - point_radius, 2 * point_radius, 2 * point_radius, QPen(Qt.blue), QColor(Qt.blue))
                # QTimer.singleShot(100, lambda: self.removeEllipse(ellipse_item))
        self.paintPoint = MyItem(all_points)
        self.paintPoint.setPos(0, 0)
        self.scene.addItem(self.paintPoint)

    def removeEllipse(self, ellipse_item):
        """Remove the specified ellipse from the scene."""
        self.scene.removeItem(ellipse_item)

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
