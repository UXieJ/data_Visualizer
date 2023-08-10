from PySide6.QtCore import QThread, Signal, QTimer, Qt, QRectF
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QGraphicsItem


class parseNetThread(QThread):
    fin = Signal(object)

    def __init__(self, uParser):
        super().__init__()
        self.parser = uParser

    def run(self):
        pointCloud = self.parser.parse_data
        self.fin.emit(pointCloud)


class MyItem(QGraphicsItem):
    def __init__(self, points):
        super(MyItem, self).__init__()
        self.points = points

    def boundingRect(self):
        if not self.points:
            return QRectF(-10, -10, 20, 20)
        min_x = min([x for x, _ in self.points])
        max_x = max([x for x, _ in self.points])
        min_y = min([y for _, y in self.points])
        max_y = max([y for _, y in self.points])
        return QRectF(min_x, min_y, max_x - min_x, max_y - min_y)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.blue))
        for x, y in self.points:
            painter.drawPoint(x, y)

    def mousePressEvent(self, event):
        self.update()

    def setPointList(self, points):
        self.update()
        self.points = points
