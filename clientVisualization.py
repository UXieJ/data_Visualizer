# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clientVisualization.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QPushButton, QGraphicsScene,
    QSizePolicy, QWidget)


class Ui_gui(object):
    def setupUi(self, gui):
        if not gui.objectName():
            gui.setObjectName(u"gui")
        gui.resize(800, 600)
        gui.setMinimumSize(QSize(100, 80))
        gui.setMaximumSize(QSize(2048, 1080))
        self.graphicsView = QGraphicsView(gui)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(6, 6, 680, 500))
        self.widget = QWidget(gui)
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




