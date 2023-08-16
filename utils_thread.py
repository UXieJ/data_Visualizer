from PySide6.QtCore import QThread, Signal, Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QPainter, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView


class parseNetThread(QThread):
    fin = Signal(object)

    def __init__(self, uParser):
        super().__init__()
        self.parser = uParser

    def run(self):
        pointCloud = self.parser.parse_data
        self.fin.emit(pointCloud)


class MyItem(QGraphicsItem):
    #QGraphicScene is a container for QGrpahicsItem objects and it manages their layout and rendering
    def __init__(self, x, y, data):
        super(MyItem, self).__init__()
        self.x = x
        self.y = y
        self.data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    # boundingRect函数返回item的边界矩形
    def boundingRect(self):
        return QRectF(self.x - 1, self.y - 1, 1.1, 1.1)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.blue, 1))
        painter.setBrush(Qt.blue)
        #painter.drawPoint(self.x, self.y)
        painter.drawRect(self.x - 1, self.y - 1, 1, 1)

    def mousePressEvent(self, event):
        print(self.data)  # Display data of the selected point
        super(MyItem, self).mousePressEvent(event)

    def center(self):
        rect = self.boundingRect()
        return QPointF(rect.x() + rect.width() / 2, rect.y() + rect.height() / 2)

    def setPointList(self, points):
        self.points = points
        self.update()

    def getData(self):
        return self.x, self.y


class GridGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
     #QGraphicView is a widget that provides a viewport onto a QGraphicScene
        super(GridGraphicsScene, self).__init__(parent)
        self.grid_interval = 50
        self.grid_lines = []
        self.drawGrid()

#background grid is automatically drawn when the scene is rendered ,when call the update method of the QGraphicsView that display the scene
    def drawBackground(self, painter: QPainter, rect: QRectF):
        grid_pen = QPen(QColor(220, 220, 220))  # light gray color
        grid_pen.setWidthF(0.5)
        grid_pen.setCosmetic(True)  # Ensure the pen width remains consistent regardless of transformations
        painter.setPen(grid_pen)  # Set the pen for the painter
        # print("draw background witdh ", rect.width())
        # print("draw background height ", rect.height())

        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        # transform = self.views()[0].transform()
        # scale_factor = transform.m11()  # Horizontal scaling factor
        # adjusted_grid_interval = self.grid_interval / scale_factor

        adjusted_grid_interval = 50

        x = left - left % adjusted_grid_interval
        while x < right:
            painter.drawLine(x, top, x, bottom)
            x += adjusted_grid_interval

        y = top - top % adjusted_grid_interval
        while y < bottom:
            painter.drawLine(left, y, right, y)
            y += adjusted_grid_interval

    def drawGrid(self):
        w, h = int(self.width()), int(self.height())
        for x in range(0, w, self.grid_interval):
            self.grid_lines.append(self.addLine(x, 0, x, h, self.grid_pen))
        for y in range(0, h, self.grid_interval):
            self.grid_lines.append(self.addLine(0, y, w, y, self.grid_pen))

#this method removes the existing grid lines from the scene, clear the self.grid_lines list then redraws teh grid using the drawGrid method
    def updateGrid(self):
        for line in self.grid_lines:
            self.removeItem(line)
        self.grid_lines.clear()
        self.drawGrid()

    def mouseReleaseEvent(self, event):
        print("222222")
        items = self.selectedItems()
        for item in items:
            x,y = item.getData()
            print("item x:", x, "y:", y)
        super().mouseReleaseEvent(event)




