# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plumbingdiagramZxAcBb.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QWidget)
import diagram_rc

class Ui_plumbingdiagram(object):
    def setupUi(self, plumbingdiagram):
        if not plumbingdiagram.objectName():
            plumbingdiagram.setObjectName(u"plumbingdiagram")
        plumbingdiagram.resize(1329, 738)
        self.diagram = QLabel(plumbingdiagram)
        self.diagram.setObjectName(u"diagram")
        self.diagram.setGeometry(QRect(0, 0, 1331, 741))

        self.retranslateUi(plumbingdiagram)

        QMetaObject.connectSlotsByName(plumbingdiagram)
    # setupUi

    def retranslateUi(self, plumbingdiagram):
        plumbingdiagram.setWindowTitle(QCoreApplication.translate("plumbingdiagram", u"Dialog", None))
        self.diagram.setText(QCoreApplication.translate("plumbingdiagram", u"<html><head/><body><p><img src=\":/newPrefix/plumbing.png\"/></p></body></html>", None))
    # retranslateUi



class StatusIndicator(QWidget):
    def __init__(self, color='gray', diameter=20, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._diameter = diameter
        self.setFixedSize(QSize(diameter, diameter))
 
    def setColor(self, color):
        self._color = QColor(color)
        self.update()  # Trigger repaint
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self._color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self._diameter, self._diameter)
    # retranslateUi