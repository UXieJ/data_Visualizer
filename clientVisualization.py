# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clientVisualization.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt,
                            QSize)
from PySide6.QtWidgets import (QGraphicsView, QHBoxLayout, QPushButton, QWidget)


class Ui_gui(object):
    def setupUi(self, gui):
        if not gui.objectName():
            gui.setObjectName(u"gui")
        gui.resize(960, 640) #width and height ratio 3:2
        gui.setMinimumSize(QSize(120, 80))
        gui.setMaximumSize(QSize(1950, 1300))
        # self.graphicsView = QGraphicsView(gui)
        self.graphicsView = mouseGraphicsView(gui)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(6, 6, 680, 500))
        # set the position and size of the QGraphicsView widget within its parent(gui)
        # View starts at 6 pixels from the left and 6 pixels from the top of its parent widget
        self.widget = QWidget(gui) #create an instance of QWidget
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(130, 540, 158, 26))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.connectButton = QPushButton(self.widget)
        self.connectButton.setObjectName(u"connectButton")

        self.horizontalLayout.addWidget(self.connectButton)

        self.cancelButton = QPushButton(self.widget)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.retranslateUi(gui)

        QMetaObject.connectSlotsByName(gui)
    # setupUi

    def retranslateUi(self, gui):
        gui.setWindowTitle(QCoreApplication.translate("gui", u"clientVisualization", None))
        self.connectButton.setText(QCoreApplication.translate("gui", u"connect", None))
        self.cancelButton.setText(QCoreApplication.translate("gui", u"disconnect", None))
    # retranslateUi


class mouseGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(mouseGraphicsView, self).__init__(parent)
        # self.setDragMode(QGraphicsView.RubberBandDrag)
        self.rubberBandOrigin = None
        self.panning = False
        self.currentZoom = 1.0

    # def wheelEvent(self, event):
    #     zoom_factor = 1.2
    #     if event.angleDelta().y() > 0:  # Zoom in
    #         self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    #         self.scale(zoom_factor, zoom_factor)
    #     else:  # Zoom out
    #         self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    #         self.scale(1 / zoom_factor, 1 / zoom_factor)
    def wheelEvent(self, event):
        zoomInFactor = 1.2
        zoomOutFactor = 1/ zoomInFactor
        oldPos = self.mapToScene(event.position().toPoint())
        if event.angleDelta().y() > 0:
            proposeZoom = self.currentZoom * zoomInFactor
            if proposeZoom < 20:
                self.currentZoom = proposeZoom
                zoomFactor = zoomInFactor
            else:
                zoomFactor = 1.0
        else:
            proposeZoom = self.currentZoom * zoomOutFactor
            if proposeZoom > 0.5:
                self.currentZoom = proposeZoom
                zoomFactor = zoomOutFactor
            else:
                zoomFactor = 1.0
        self.scale(zoomFactor, zoomFactor)

        newPos = self.mapToScene(event.position().toPoint())
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:  # Use right mouse button to drag
            self.panning = True
            self.panning_start = event.pos()
        elif event.button() == Qt.LeftButton:  # Use left mouse button for rubber-band selection
            self.rubberBandOrigin = event.pos()
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super(mouseGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - (event.x() - self.panning_start.x()))
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - (event.y() - self.panning_start.y()))
            self.panning_start = event.pos()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.panning = False
        elif event.button() == Qt.LeftButton and self.rubberBandOrigin:
            rect = QRect(self.rubberBandOrigin, event.pos()).normalized()
            selected_items = self.items(rect)
            # Now, selected_items contains all the points within the rubber-band rectangle
            # You can process them as needed
            self.rubberBandOrigin = None
        super(mouseGraphicsView, self).mouseReleaseEvent(event)




