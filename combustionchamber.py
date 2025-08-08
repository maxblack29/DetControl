# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'combustionchamberTuFpaF.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QLCDNumber, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

import os
os.environ["PYQTGRAPH_QT_LIB"] = "PySide6" #ensures that PyQtGraph uses PySide6 for rendering

from pyqtgraph import PlotWidget
import diagram_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1229, 553)
        Dialog.setStyleSheet(u"/*Copyright (c) DevSec Studio. All rights reserved.\n"
"\n"
"MIT License\n"
"\n"
"Permission is hereby granted, free of charge, to any person obtaining a copy\n"
"of this software and associated documentation files (the \"Software\"), to deal\n"
"in the Software without restriction, including without limitation the rights\n"
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
"copies of the Software, and to permit persons to whom the Software is\n"
"furnished to do so, subject to the following conditions:\n"
"\n"
"The above copyright notice and this permission notice shall be included in all\n"
"copies or substantial portions of the Software.\n"
"\n"
"THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
"LIABILITY, WHETHER IN AN ACT"
                        "ION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
"*/\n"
"\n"
"/*-----QWidget-----*/\n"
"QWidget\n"
"{\n"
"	background-color: #3a3a3a;\n"
"	color: #fff;\n"
"	selection-background-color: #b78620;\n"
"	selection-color: #000;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLabel-----*/\n"
"QLabel\n"
"{\n"
"	background-color: transparent;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QMenuBar-----*/\n"
"QMenuBar \n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item \n"
"{\n"
"	background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item:selected \n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item:pressed \n"
"{\n"
"	background-color: rgb(183, 134, 32);\n"
""
                        "	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QMenu-----*/\n"
"QMenu\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    border: 1px solid #222;\n"
"    padding: 4px;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item\n"
"{\n"
"    background-color: transparent;\n"
"    padding: 2px 20px 2px 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::separator\n"
"{\n"
"   	background-color: rgb(183, 134, 32);\n"
"	height: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item:disabled\n"
"{\n"
"    color: #555;\n"
"    background-color: transparent;\n"
"    padding: 2px 20px 2px 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QToolBar-----*/\n"
"QToolBar\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(69, 69, 69, 255),stop"
                        ":1 rgba(58, 58, 58, 255));\n"
"	border-top: none;\n"
"	border-bottom: 1px solid #4f4f4f;\n"
"	border-left: 1px solid #4f4f4f;\n"
"	border-right: 1px solid #4f4f4f;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolBar::separator\n"
"{\n"
"	background-color: #2e2e2e;\n"
"	width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QToolButton-----*/\n"
"QToolButton \n"
"{\n"
"	background-color: transparent;\n"
"	color: #fff;\n"
"	padding: 5px;\n"
"	padding-left: 8px;\n"
"	padding-right: 8px;\n"
"	margin-left: 1px;\n"
"}\n"
"\n"
"\n"
"QToolButton:hover\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"	\n"
"}\n"
"\n"
"\n"
"QToolButton:pressed\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolButton:checked\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, "
                        "50, 255));\n"
"	border: 1px solid #222;\n"
"}\n"
"\n"
"\n"
"/*-----QPushButton-----*/\n"
"QPushButton\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"	color: #ffffff;\n"
"	min-width: 80px;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-radius: 3px;\n"
"	border-color: #051a39;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::flat\n"
"{\n"
"	background-color: transparent;\n"
"	border: none;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::disabled\n"
"{\n"
"	background-color: #404040;\n"
"	color: #656565;\n"
"	border-color: #051a39;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));\n"
"	border: 1px solid #b78620;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QPushButton::checked\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));\n"
"	border: 1px solid #222;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLineEdit-----*/\n"
"QLineEdit\n"
"{\n"
"	background-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	border-radius: 2px;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QPlainTExtEdit-----*/\n"
"QPlainTextEdit\n"
"{\n"
"	background-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	border-radius: 2px;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTabBar-----*/\n"
"QTabBar::tab\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"	color: #ffffff;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-color: #666;\n"
"	border-bottom: none;\n"
"	padding: 5px;\n"
"	padding-lef"
                        "t: 15px;\n"
"	padding-right: 15px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabWidget::pane \n"
"{\n"
"	background-color: red;\n"
"	border: 1px solid #666;\n"
"	top: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"	margin-right: 0; \n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
"	background-color: #0c0c0d;\n"
"	margin-left: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"	color: #b1b1b1;\n"
"	border-bottom-style: solid;\n"
"	background-color: #0c0c0d;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"	margin-bottom: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"	border-top-color: #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QComboBox-----*/\n"
"QComboBox\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"    border: 1px solid #000;\n"
"    padding-left: 6px;\n"
"    color: #ffffff;\n"
"    height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::disabled\n"
"{\n"
"	b"
                        "ackground-color: #404040;\n"
"	color: #656565;\n"
"	border-color: #051a39;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    background-color: #b78620;\n"
"	color: #000;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    background-color: #383838;\n"
"    color: #ffffff;\n"
"    border: 1px solid black;\n"
"    selection-background-color: #b78620;\n"
"    outline: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: black;\n"
"    border-left-style: solid; \n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 8px;\n"
"    height: 8px;\n"
"}\n"
"\n"
"\n"
"/*-----QSpinBox & QDateTimeEdit-----*/\n"
"QSpinBox,\n"
"QDateTimeEdit \n"
"{\n"
"    background"
                        "-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"    border-radius : 2px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button, \n"
"QDateTimeEdit::up-button\n"
"{\n"
"	border-top-right-radius:2px;\n"
"	background-color: #777777;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button:hover, \n"
"QDateTimeEdit::up-button:hover\n"
"{\n"
"	background-color: #585858;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button:pressed, \n"
"QDateTimeEdit::up-button:pressed\n"
"{\n"
"	background-color: #252525;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-arrow,\n"
"QDateTimeEdit::up-arrow\n"
"{\n"
"    image: url(://arrow-up.png);\n"
"    width: 7px;\n"
"    height: 7px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-button, \n"
"QDateTimeEdit::down-button\n"
"{\n"
"	border-bottom-right-radius:2px;\n"
"	background-color: #777777;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
""
                        "QSpinBox::down-button:hover, \n"
"QDateTimeEdit::down-button:hover\n"
"{\n"
"	background-color: #585858;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-button:pressed, \n"
"QDateTimeEdit::down-button:pressed\n"
"{\n"
"	background-color: #252525;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-arrow,\n"
"QDateTimeEdit::down-arrow\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 7px;\n"
"    height: 7px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QGroupBox-----*/\n"
"QGroupBox \n"
"{\n"
"    border: 1px solid;\n"
"    border-color: #666666;\n"
"	border-radius: 5px;\n"
"    margin-top: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QGroupBox::title  \n"
"{\n"
"    background-color: transparent;\n"
"    color: #eee;\n"
"    subcontrol-origin: margin;\n"
"    padding: 5px;\n"
"	border-top-left-radius: 3px;\n"
"	border-top-right-radius: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QHeaderView-----*/\n"
"QHeaderView::section\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2"
                        ":1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"    color: #fff;\n"
"    text-align: left;\n"
"	padding: 4px;\n"
"	\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:disabled\n"
"{\n"
"    background-color: #525251;\n"
"    color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:checked\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical::first,\n"
"QHeaderView::section::vertical::only-one\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal::first,\n"
"QHeaderView::section::horizontal::only-one\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QTableCornerButton::section\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTreeWidget-----*/\n"
"QTreeView\n"
"{\n"
"	show-decoration-selected: 1;\n"
"	alternate-background-color: #3a3a3a;\n"
"	selection-color: #fff;\n"
"	background-color: #2d2d2d;\n"
"	border: 1px solid gray;\n"
"	padding-top : 5px;\n"
"	color: #fff;\n"
"	font: 8pt;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:selected\n"
"{\n"
"	color:#fff;\n"
"	background-color: #b78620;\n"
"	border-radius: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:!selected:hover\n"
"{\n"
"    background-color: #262626;\n"
"    border: none;\n"
"    color: white;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings \n"
"{\n"
"	image: url(://tree-closed.png);\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::branc"
                        "h:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  \n"
"{\n"
"	image: url(://tree-open.png);\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QListView-----*/\n"
"QListView \n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(83, 83, 83, 255),stop:0.293269 rgba(81, 81, 81, 255),stop:0.634615 rgba(79, 79, 79, 255),stop:1 rgba(83, 83, 83, 255));\n"
"    border : none;\n"
"    color: white;\n"
"    show-decoration-selected: 1; \n"
"    outline: 0;\n"
"	border: 1px solid gray;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::disabled \n"
"{\n"
"	background-color: #656565;\n"
"	color: #1b1b1b;\n"
"    border: 1px solid #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item \n"
"{\n"
"	background-color: #2d2d2d;\n"
"    padding: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:alternate \n"
"{\n"
"    background-color: #3a3a3a;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:selected \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QListView::item:selected:!active \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:selected:active \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:hover {\n"
"    background-color: #262626;\n"
"    border: none;\n"
"    color: white;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QCheckBox-----*/\n"
"QCheckBox\n"
"{\n"
"	background-color: transparent;\n"
"    color: lightgray;\n"
"	border: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator\n"
"{\n"
"    background-color: #323232;\n"
"    border: 1px solid darkgray;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(\"./ressources/check.png\");\n"
"	background-color: #b78620;\n"
"    border: 1px solid #3a546e;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:unchecked:hover\n"
"{\n"
"	border: 1px solid #b78620; \n"
"\n"
"}\n"
"\n"
"\n"
""
                        "QCheckBox::disabled\n"
"{\n"
"	color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:disabled\n"
"{\n"
"	background-color: #656565;\n"
"	color: #656565;\n"
"    border: 1px solid #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QRadioButton-----*/\n"
"QRadioButton \n"
"{\n"
"	color: lightgray;\n"
"	background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator::unchecked:hover \n"
"{\n"
"	background-color: lightgray;\n"
"	border: 2px solid #b78620;\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator::checked \n"
"{\n"
"	border: 2px solid #b78620;\n"
"	border-radius: 6px;\n"
"	background-color: rgba(183,134,32,20%);  \n"
"	width: 9px; \n"
"	height: 9px; \n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QSlider-----*/\n"
"QSlider::groove:horizontal \n"
"{\n"
"	background-color: transparent;\n"
"	height: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal \n"
"{\n"
"	background-color: #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal \n"
"{\n"
"	background-color: #131313;\n"
""
                        "\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal \n"
"{\n"
"	background-color: #b78620;\n"
"	width: 14px;\n"
"	margin-top: -6px;\n"
"	margin-bottom: -6px;\n"
"	border-radius: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:hover \n"
"{\n"
"	background-color: #d89e25;\n"
"	border-radius: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal:disabled \n"
"{\n"
"	background-color: #bbb;\n"
"	border-color: #999;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal:disabled \n"
"{\n"
"	background-color: #eee;\n"
"	border-color: #999;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:disabled \n"
"{\n"
"	background-color: #eee;\n"
"	border: 1px solid #aaa;\n"
"	border-radius: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QScrollBar-----*/\n"
"QScrollBar:horizontal\n"
"{\n"
"    border: 1px solid #222222;\n"
"    background-color: #3d3d3d;\n"
"    height: 15px;\n"
"    margin: 0px 16px 0 16px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:"
                        "1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    min-height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    width: 15px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::sub-line:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    width: 15px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::right-arrow:horizontal\n"
"{\n"
"    image: url(://arrow-right.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::left-arrow:horizontal\n"
"{\n"
"    image: url(://arr"
                        "ow-left.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"    background: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"    background-color: #3d3d3d;\n"
"    width: 16px;\n"
"	border: 1px solid #2d2d2d;\n"
"    margin: 16px 0px 16px 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    min-height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    height: 15px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"	background-color: qlinear"
                        "gradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    height: 15px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::up-arrow:vertical\n"
"{\n"
"    image: url(://arrow-up.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::down-arrow:vertical\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"    background: none;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QProgressBar-----*/\n"
"QProgressBar\n"
"{\n"
"    border: 1px solid #666666;\n"
"    text-align: center;\n"
"	color: #000;\n"
"	font-weight: bold;\n"
"\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #b78620;\n"
"    width: 30px;\n"
"    margin: 0.5px;\n"
"\n"
"}\n"
"\n"
"")
        self.mfcAgas = QComboBox(Dialog)
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.addItem("")
        self.mfcAgas.setObjectName(u"mfcAgas")
        self.mfcAgas.setGeometry(QRect(70, 60, 81, 21))
        self.mfccontrollerlabel = QLabel(Dialog)
        self.mfccontrollerlabel.setObjectName(u"mfccontrollerlabel")
        self.mfccontrollerlabel.setGeometry(QRect(140, 10, 91, 31))
        self.mfcAlabel = QLabel(Dialog)
        self.mfcAlabel.setObjectName(u"mfcAlabel")
        self.mfcAlabel.setGeometry(QRect(20, 60, 49, 16))
        self.mfcBlabel = QLabel(Dialog)
        self.mfcBlabel.setObjectName(u"mfcBlabel")
        self.mfcBlabel.setGeometry(QRect(20, 100, 49, 16))
        self.mfcClabel = QLabel(Dialog)
        self.mfcClabel.setObjectName(u"mfcClabel")
        self.mfcClabel.setGeometry(QRect(20, 140, 49, 16))
        self.mfcBgas = QComboBox(Dialog)
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.addItem("")
        self.mfcBgas.setObjectName(u"mfcBgas")
        self.mfcBgas.setGeometry(QRect(70, 100, 81, 21))
        self.mfcCgas = QComboBox(Dialog)
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.addItem("")
        self.mfcCgas.setObjectName(u"mfcCgas")
        self.mfcCgas.setGeometry(QRect(70, 140, 81, 21))
        self.mfcCgas.setStyleSheet(u"/*Copyright (c) DevSec Studio. All rights reserved.\n"
"\n"
"MIT License\n"
"\n"
"Permission is hereby granted, free of charge, to any person obtaining a copy\n"
"of this software and associated documentation files (the \"Software\"), to deal\n"
"in the Software without restriction, including without limitation the rights\n"
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
"copies of the Software, and to permit persons to whom the Software is\n"
"furnished to do so, subject to the following conditions:\n"
"\n"
"The above copyright notice and this permission notice shall be included in all\n"
"copies or substantial portions of the Software.\n"
"\n"
"THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
"LIABILITY, WHETHER IN AN ACT"
                        "ION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
"*/\n"
"\n"
"/*-----QWidget-----*/\n"
"QWidget\n"
"{\n"
"	background-color: #3a3a3a;\n"
"	color: #fff;\n"
"	selection-background-color: #b78620;\n"
"	selection-color: #000;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLabel-----*/\n"
"QLabel\n"
"{\n"
"	background-color: transparent;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QMenuBar-----*/\n"
"QMenuBar \n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item \n"
"{\n"
"	background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item:selected \n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenuBar::item:pressed \n"
"{\n"
"	background-color: rgb(183, 134, 32);\n"
""
                        "	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QMenu-----*/\n"
"QMenu\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    border: 1px solid #222;\n"
"    padding: 4px;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item\n"
"{\n"
"    background-color: transparent;\n"
"    padding: 2px 20px 2px 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::separator\n"
"{\n"
"   	background-color: rgb(183, 134, 32);\n"
"	height: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item:disabled\n"
"{\n"
"    color: #555;\n"
"    background-color: transparent;\n"
"    padding: 2px 20px 2px 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QToolBar-----*/\n"
"QToolBar\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(69, 69, 69, 255),stop"
                        ":1 rgba(58, 58, 58, 255));\n"
"	border-top: none;\n"
"	border-bottom: 1px solid #4f4f4f;\n"
"	border-left: 1px solid #4f4f4f;\n"
"	border-right: 1px solid #4f4f4f;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolBar::separator\n"
"{\n"
"	background-color: #2e2e2e;\n"
"	width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QToolButton-----*/\n"
"QToolButton \n"
"{\n"
"	background-color: transparent;\n"
"	color: #fff;\n"
"	padding: 5px;\n"
"	padding-left: 8px;\n"
"	padding-right: 8px;\n"
"	margin-left: 1px;\n"
"}\n"
"\n"
"\n"
"QToolButton:hover\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"	\n"
"}\n"
"\n"
"\n"
"QToolButton:pressed\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolButton:checked\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, "
                        "50, 255));\n"
"	border: 1px solid #222;\n"
"}\n"
"\n"
"\n"
"/*-----QPushButton-----*/\n"
"QPushButton\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"	color: #ffffff;\n"
"	min-width: 80px;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-radius: 3px;\n"
"	border-color: #051a39;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::flat\n"
"{\n"
"	background-color: transparent;\n"
"	border: none;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::disabled\n"
"{\n"
"	background-color: #404040;\n"
"	color: #656565;\n"
"	border-color: #051a39;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgba(183, 134, 32, 20%);\n"
"	border: 1px solid #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));\n"
"	border: 1px solid #b78620;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QPushButton::checked\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));\n"
"	border: 1px solid #222;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLineEdit-----*/\n"
"QLineEdit\n"
"{\n"
"	background-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	border-radius: 2px;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QPlainTExtEdit-----*/\n"
"QPlainTextEdit\n"
"{\n"
"	background-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	border-radius: 2px;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTabBar-----*/\n"
"QTabBar::tab\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"	color: #ffffff;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-color: #666;\n"
"	border-bottom: none;\n"
"	padding: 5px;\n"
"	padding-lef"
                        "t: 15px;\n"
"	padding-right: 15px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabWidget::pane \n"
"{\n"
"	background-color: red;\n"
"	border: 1px solid #666;\n"
"	top: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"	margin-right: 0; \n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
"	background-color: #0c0c0d;\n"
"	margin-left: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"	color: #b1b1b1;\n"
"	border-bottom-style: solid;\n"
"	background-color: #0c0c0d;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"	margin-bottom: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"	border-top-color: #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QComboBox-----*/\n"
"QComboBox\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));\n"
"    border: 1px solid #000;\n"
"    padding-left: 6px;\n"
"    color: #ffffff;\n"
"    height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::disabled\n"
"{\n"
"	b"
                        "ackground-color: #404040;\n"
"	color: #656565;\n"
"	border-color: #051a39;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    background-color: #b78620;\n"
"	color: #000;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    background-color: #383838;\n"
"    color: #ffffff;\n"
"    border: 1px solid black;\n"
"    selection-background-color: #b78620;\n"
"    outline: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: black;\n"
"    border-left-style: solid; \n"
"\n"
"}\n"
"\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 8px;\n"
"    height: 8px;\n"
"}\n"
"\n"
"\n"
"/*-----QSpinBox & QDateTimeEdit-----*/\n"
"QSpinBox,\n"
"QDateTimeEdit \n"
"{\n"
"    background"
                        "-color: #131313;\n"
"	color : #eee;\n"
"	border: 1px solid #343434;\n"
"	padding: 3px;\n"
"	padding-left: 5px;\n"
"    border-radius : 2px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button, \n"
"QDateTimeEdit::up-button\n"
"{\n"
"	border-top-right-radius:2px;\n"
"	background-color: #777777;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button:hover, \n"
"QDateTimeEdit::up-button:hover\n"
"{\n"
"	background-color: #585858;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button:pressed, \n"
"QDateTimeEdit::up-button:pressed\n"
"{\n"
"	background-color: #252525;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-arrow,\n"
"QDateTimeEdit::up-arrow\n"
"{\n"
"    image: url(://arrow-up.png);\n"
"    width: 7px;\n"
"    height: 7px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-button, \n"
"QDateTimeEdit::down-button\n"
"{\n"
"	border-bottom-right-radius:2px;\n"
"	background-color: #777777;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
""
                        "QSpinBox::down-button:hover, \n"
"QDateTimeEdit::down-button:hover\n"
"{\n"
"	background-color: #585858;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-button:pressed, \n"
"QDateTimeEdit::down-button:pressed\n"
"{\n"
"	background-color: #252525;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-arrow,\n"
"QDateTimeEdit::down-arrow\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 7px;\n"
"    height: 7px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QGroupBox-----*/\n"
"QGroupBox \n"
"{\n"
"    border: 1px solid;\n"
"    border-color: #666666;\n"
"	border-radius: 5px;\n"
"    margin-top: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QGroupBox::title  \n"
"{\n"
"    background-color: transparent;\n"
"    color: #eee;\n"
"    subcontrol-origin: margin;\n"
"    padding: 5px;\n"
"	border-top-left-radius: 3px;\n"
"	border-top-right-radius: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QHeaderView-----*/\n"
"QHeaderView::section\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2"
                        ":1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"    color: #fff;\n"
"    text-align: left;\n"
"	padding: 4px;\n"
"	\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:disabled\n"
"{\n"
"    background-color: #525251;\n"
"    color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:checked\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical::first,\n"
"QHeaderView::section::vertical::only-one\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal::first,\n"
"QHeaderView::section::horizontal::only-one\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QTableCornerButton::section\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));\n"
"	border: 1px solid #000;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTreeWidget-----*/\n"
"QTreeView\n"
"{\n"
"	show-decoration-selected: 1;\n"
"	alternate-background-color: #3a3a3a;\n"
"	selection-color: #fff;\n"
"	background-color: #2d2d2d;\n"
"	border: 1px solid gray;\n"
"	padding-top : 5px;\n"
"	color: #fff;\n"
"	font: 8pt;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:selected\n"
"{\n"
"	color:#fff;\n"
"	background-color: #b78620;\n"
"	border-radius: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:!selected:hover\n"
"{\n"
"    background-color: #262626;\n"
"    border: none;\n"
"    color: white;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings \n"
"{\n"
"	image: url(://tree-closed.png);\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::branc"
                        "h:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  \n"
"{\n"
"	image: url(://tree-open.png);\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QListView-----*/\n"
"QListView \n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(83, 83, 83, 255),stop:0.293269 rgba(81, 81, 81, 255),stop:0.634615 rgba(79, 79, 79, 255),stop:1 rgba(83, 83, 83, 255));\n"
"    border : none;\n"
"    color: white;\n"
"    show-decoration-selected: 1; \n"
"    outline: 0;\n"
"	border: 1px solid gray;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::disabled \n"
"{\n"
"	background-color: #656565;\n"
"	color: #1b1b1b;\n"
"    border: 1px solid #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item \n"
"{\n"
"	background-color: #2d2d2d;\n"
"    padding: 1px;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:alternate \n"
"{\n"
"    background-color: #3a3a3a;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:selected \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
""
                        "}\n"
"\n"
"\n"
"QListView::item:selected:!active \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:selected:active \n"
"{\n"
"	background-color: #b78620;\n"
"	border: 1px solid #b78620;\n"
"	color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:hover {\n"
"    background-color: #262626;\n"
"    border: none;\n"
"    color: white;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QCheckBox-----*/\n"
"QCheckBox\n"
"{\n"
"	background-color: transparent;\n"
"    color: lightgray;\n"
"	border: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator\n"
"{\n"
"    background-color: #323232;\n"
"    border: 1px solid darkgray;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(\"./ressources/check.png\");\n"
"	background-color: #b78620;\n"
"    border: 1px solid #3a546e;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:unchecked:hover\n"
"{\n"
"	border: 1px solid #b78620; \n"
"\n"
"}\n"
"\n"
"\n"
""
                        "QCheckBox::disabled\n"
"{\n"
"	color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:disabled\n"
"{\n"
"	background-color: #656565;\n"
"	color: #656565;\n"
"    border: 1px solid #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QRadioButton-----*/\n"
"QRadioButton \n"
"{\n"
"	color: lightgray;\n"
"	background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator::unchecked:hover \n"
"{\n"
"	background-color: lightgray;\n"
"	border: 2px solid #b78620;\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator::checked \n"
"{\n"
"	border: 2px solid #b78620;\n"
"	border-radius: 6px;\n"
"	background-color: rgba(183,134,32,20%);  \n"
"	width: 9px; \n"
"	height: 9px; \n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QSlider-----*/\n"
"QSlider::groove:horizontal \n"
"{\n"
"	background-color: transparent;\n"
"	height: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal \n"
"{\n"
"	background-color: #b78620;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal \n"
"{\n"
"	background-color: #131313;\n"
""
                        "\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal \n"
"{\n"
"	background-color: #b78620;\n"
"	width: 14px;\n"
"	margin-top: -6px;\n"
"	margin-bottom: -6px;\n"
"	border-radius: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:hover \n"
"{\n"
"	background-color: #d89e25;\n"
"	border-radius: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal:disabled \n"
"{\n"
"	background-color: #bbb;\n"
"	border-color: #999;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal:disabled \n"
"{\n"
"	background-color: #eee;\n"
"	border-color: #999;\n"
"\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:disabled \n"
"{\n"
"	background-color: #eee;\n"
"	border: 1px solid #aaa;\n"
"	border-radius: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QScrollBar-----*/\n"
"QScrollBar:horizontal\n"
"{\n"
"    border: 1px solid #222222;\n"
"    background-color: #3d3d3d;\n"
"    height: 15px;\n"
"    margin: 0px 16px 0 16px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:"
                        "1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    min-height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    width: 15px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::sub-line:horizontal\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    width: 15px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::right-arrow:horizontal\n"
"{\n"
"    image: url(://arrow-right.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::left-arrow:horizontal\n"
"{\n"
"    image: url(://arr"
                        "ow-left.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"    background: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"    background-color: #3d3d3d;\n"
"    width: 16px;\n"
"	border: 1px solid #2d2d2d;\n"
"    margin: 16px 0px 16px 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    min-height: 20px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    height: 15px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"	background-color: qlinear"
                        "gradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));\n"
"	border: 1px solid #2d2d2d;\n"
"    height: 15px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::up-arrow:vertical\n"
"{\n"
"    image: url(://arrow-up.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::down-arrow:vertical\n"
"{\n"
"    image: url(://arrow-down.png);\n"
"    width: 6px;\n"
"    height: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"    background: none;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QProgressBar-----*/\n"
"QProgressBar\n"
"{\n"
"    border: 1px solid #666666;\n"
"    text-align: center;\n"
"	color: #000;\n"
"	font-weight: bold;\n"
"\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #b78620;\n"
"    width: 30px;\n"
"    margin: 0.5px;\n"
"\n"
"}\n"
"\n"
"")
        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(-10, 300, 1261, 16))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.mfcDgas = QComboBox(Dialog)
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.addItem("")
        self.mfcDgas.setObjectName(u"mfcDgas")
        self.mfcDgas.setGeometry(QRect(70, 180, 81, 21))
        self.mfcDlabel = QLabel(Dialog)
        self.mfcDlabel.setObjectName(u"mfcDlabel")
        self.mfcDlabel.setGeometry(QRect(20, 180, 49, 16))
        self.drivergaslabel = QLabel(Dialog)
        self.drivergaslabel.setObjectName(u"drivergaslabel")
        self.drivergaslabel.setGeometry(QRect(440, 60, 121, 16))
        self.openS1 = QPushButton(Dialog)
        self.openS1.setObjectName(u"openS1")
        self.openS1.setGeometry(QRect(590, 60, 92, 24))
        self.closeS1 = QPushButton(Dialog)
        self.closeS1.setObjectName(u"closeS1")
        self.closeS1.setGeometry(QRect(690, 60, 92, 24))
        self.fuellabel = QLabel(Dialog)
        self.fuellabel.setObjectName(u"fuellabel")
        self.fuellabel.setGeometry(QRect(470, 110, 91, 16))
        self.closeS2 = QPushButton(Dialog)
        self.closeS2.setObjectName(u"closeS2")
        self.closeS2.setGeometry(QRect(690, 110, 92, 24))
        self.openS2 = QPushButton(Dialog)
        self.openS2.setObjectName(u"openS2")
        self.openS2.setGeometry(QRect(590, 110, 92, 24))
        self.oxidizerlabel = QLabel(Dialog)
        self.oxidizerlabel.setObjectName(u"oxidizerlabel")
        self.oxidizerlabel.setGeometry(QRect(380, 160, 181, 16))
        self.closeS3 = QPushButton(Dialog)
        self.closeS3.setObjectName(u"closeS3")
        self.closeS3.setGeometry(QRect(690, 160, 92, 24))
        self.openS3 = QPushButton(Dialog)
        self.openS3.setObjectName(u"openS3")
        self.openS3.setGeometry(QRect(590, 160, 92, 24))
        self.purgelabel = QLabel(Dialog)
        self.purgelabel.setObjectName(u"purgelabel")
        self.purgelabel.setGeometry(QRect(430, 210, 131, 16))
        self.openS4 = QPushButton(Dialog)
        self.openS4.setObjectName(u"openS4")
        self.openS4.setGeometry(QRect(590, 210, 92, 24))
        self.closeS4 = QPushButton(Dialog)
        self.closeS4.setObjectName(u"closeS4")
        self.closeS4.setGeometry(QRect(690, 210, 92, 24))
        self.closeS5 = QPushButton(Dialog)
        self.closeS5.setObjectName(u"closeS5")
        self.closeS5.setGeometry(QRect(1110, 60, 92, 24))
        self.staticpressurelabel = QLabel(Dialog)
        self.staticpressurelabel.setObjectName(u"staticpressurelabel")
        self.staticpressurelabel.setGeometry(QRect(810, 60, 191, 16))
        self.openS5 = QPushButton(Dialog)
        self.openS5.setObjectName(u"openS5")
        self.openS5.setGeometry(QRect(1010, 60, 92, 24))
        self.closeS6 = QPushButton(Dialog)
        self.closeS6.setObjectName(u"closeS6")
        self.closeS6.setGeometry(QRect(1110, 110, 92, 24))
        self.exhaustlabel = QLabel(Dialog)
        self.exhaustlabel.setObjectName(u"exhaustlabel")
        self.exhaustlabel.setGeometry(QRect(850, 110, 141, 16))
        self.openS6 = QPushButton(Dialog)
        self.openS6.setObjectName(u"openS6")
        self.openS6.setGeometry(QRect(1010, 110, 92, 24))
        self.closeS7 = QPushButton(Dialog)
        self.closeS7.setObjectName(u"closeS7")
        self.closeS7.setGeometry(QRect(1110, 160, 92, 24))
        self.vacuumlabel = QLabel(Dialog)
        self.vacuumlabel.setObjectName(u"vacuumlabel")
        self.vacuumlabel.setGeometry(QRect(890, 160, 101, 16))
        self.openS7 = QPushButton(Dialog)
        self.openS7.setObjectName(u"openS7")
        self.openS7.setGeometry(QRect(1010, 160, 92, 24))
        self.setpointlabel1 = QLabel(Dialog)
        self.setpointlabel1.setObjectName(u"setpointlabel1")
        self.setpointlabel1.setGeometry(QRect(170, 60, 49, 16))
        self.setpointlabel2 = QLabel(Dialog)
        self.setpointlabel2.setObjectName(u"setpointlabel2")
        self.setpointlabel2.setGeometry(QRect(170, 100, 49, 16))
        self.setpointlabel3 = QLabel(Dialog)
        self.setpointlabel3.setObjectName(u"setpointlabel3")
        self.setpointlabel3.setGeometry(QRect(170, 140, 49, 16))
        self.setpointlabel4 = QLabel(Dialog)
        self.setpointlabel4.setObjectName(u"setpointlabel4")
        self.setpointlabel4.setGeometry(QRect(170, 180, 49, 16))
        self.SLPMlabel1 = QLabel(Dialog)
        self.SLPMlabel1.setObjectName(u"SLPMlabel1")
        self.SLPMlabel1.setGeometry(QRect(310, 60, 49, 16))
        self.SLPMlabel2 = QLabel(Dialog)
        self.SLPMlabel2.setObjectName(u"SLPMlabel2")
        self.SLPMlabel2.setGeometry(QRect(310, 100, 49, 16))
        self.SLPMlabel3 = QLabel(Dialog)
        self.SLPMlabel3.setObjectName(u"SLPMlabel3")
        self.SLPMlabel3.setGeometry(QRect(310, 140, 49, 16))
        self.SLPMlabel4 = QLabel(Dialog)
        self.SLPMlabel4.setObjectName(u"SLPMlabel4")
        self.SLPMlabel4.setGeometry(QRect(310, 180, 49, 16))
        self.updatesetpoints = QPushButton(Dialog)
        self.updatesetpoints.setObjectName(u"updatesetpoints")
        self.updatesetpoints.setGeometry(QRect(130, 230, 111, 24))
        self.updatesetpoints.setCheckable(False)
        self.resetmfc = QPushButton(Dialog)
        self.resetmfc.setObjectName(u"resetmfc")
        self.resetmfc.setGeometry(QRect(130, 270, 111, 24))
        self.solenoidstatelabel = QLabel(Dialog)
        self.solenoidstatelabel.setObjectName(u"solenoidstatelabel")
        self.solenoidstatelabel.setGeometry(QRect(740, 10, 91, 31))
        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(340, -10, 61, 561))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.Lowfreqpressure = QLCDNumber(Dialog)
        self.Lowfreqpressure.setObjectName(u"Lowfreqpressure")
        self.Lowfreqpressure.setGeometry(QRect(180, 410, 81, 31))
        self.staticpressurelabel_2 = QLabel(Dialog)
        self.staticpressurelabel_2.setObjectName(u"staticpressurelabel_2")
        self.staticpressurelabel_2.setGeometry(QRect(90, 400, 81, 41))
        self.pressuremonitorlabel = QLabel(Dialog)
        self.pressuremonitorlabel.setObjectName(u"pressuremonitorlabel")
        self.pressuremonitorlabel.setGeometry(QRect(140, 350, 101, 16))
        self.line_3 = QFrame(Dialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(910, 310, 61, 241))
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.testautomation = QPushButton(Dialog)
        self.testautomation.setObjectName(u"testautomation")
        self.testautomation.setGeometry(QRect(1020, 320, 151, 61))
        self.emergencypurge = QPushButton(Dialog)
        self.emergencypurge.setObjectName(u"emergencypurge")
        self.emergencypurge.setGeometry(QRect(1020, 400, 151, 61))
        self.mfcAsetpoint = QLineEdit(Dialog)
        self.mfcAsetpoint.setObjectName(u"mfcAsetpoint")
        self.mfcAsetpoint.setGeometry(QRect(230, 60, 61, 22))
        self.mfcBsetpoint = QLineEdit(Dialog)
        self.mfcBsetpoint.setObjectName(u"mfcBsetpoint")
        self.mfcBsetpoint.setGeometry(QRect(230, 100, 61, 22))
        self.mfcCsetpoint = QLineEdit(Dialog)
        self.mfcCsetpoint.setObjectName(u"mfcCsetpoint")
        self.mfcCsetpoint.setGeometry(QRect(230, 140, 61, 22))
        self.mfcDsetpoint = QLineEdit(Dialog)
        self.mfcDsetpoint.setObjectName(u"mfcDsetpoint")
        self.mfcDsetpoint.setGeometry(QRect(230, 180, 61, 22))
        self.standardpurge = QPushButton(Dialog)
        self.standardpurge.setObjectName(u"standardpurge")
        self.standardpurge.setGeometry(QRect(1020, 480, 151, 61))
        self.line_4 = QFrame(Dialog)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(0, 550, 1261, 16))
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.test_plot = PlotWidget(Dialog)
        self.test_plot.setObjectName(u"test_plot")
        self.test_plot.setGeometry(QRect(430, 320, 441, 191))
        self.line.raise_()
        self.mfcAgas.raise_()
        self.mfccontrollerlabel.raise_()
        self.mfcAlabel.raise_()
        self.mfcBlabel.raise_()
        self.mfcClabel.raise_()
        self.mfcBgas.raise_()
        self.mfcCgas.raise_()
        self.line_2.raise_()
        self.mfcDgas.raise_()
        self.mfcDlabel.raise_()
        self.drivergaslabel.raise_()
        self.openS1.raise_()
        self.closeS1.raise_()
        self.fuellabel.raise_()
        self.closeS2.raise_()
        self.openS2.raise_()
        self.oxidizerlabel.raise_()
        self.closeS3.raise_()
        self.openS3.raise_()
        self.purgelabel.raise_()
        self.openS4.raise_()
        self.closeS4.raise_()
        self.closeS5.raise_()
        self.staticpressurelabel.raise_()
        self.openS5.raise_()
        self.closeS6.raise_()
        self.exhaustlabel.raise_()
        self.openS6.raise_()
        self.closeS7.raise_()
        self.vacuumlabel.raise_()
        self.openS7.raise_()
        self.setpointlabel1.raise_()
        self.setpointlabel2.raise_()
        self.setpointlabel3.raise_()
        self.setpointlabel4.raise_()
        self.SLPMlabel1.raise_()
        self.SLPMlabel2.raise_()
        self.SLPMlabel3.raise_()
        self.SLPMlabel4.raise_()
        self.updatesetpoints.raise_()
        self.resetmfc.raise_()
        self.solenoidstatelabel.raise_()
        self.Lowfreqpressure.raise_()
        self.staticpressurelabel_2.raise_()
        self.pressuremonitorlabel.raise_()
        self.line_3.raise_()
        self.testautomation.raise_()
        self.emergencypurge.raise_()
        self.mfcAsetpoint.raise_()
        self.mfcBsetpoint.raise_()
        self.mfcCsetpoint.raise_()
        self.mfcDsetpoint.raise_()
        self.standardpurge.raise_()
        self.line_4.raise_()
        self.test_plot.raise_()

        self.retranslateUi(Dialog)

        self.openS1.setDefault(False)
        self.closeS1.setDefault(True)
        self.closeS2.setDefault(True)
        self.closeS3.setDefault(True)
        self.openS4.setDefault(True)
        self.closeS5.setDefault(True)
        self.openS6.setDefault(True)
        self.closeS7.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.mfcAgas.setItemText(0, QCoreApplication.translate("Dialog", u"Air", None))
        self.mfcAgas.setItemText(1, QCoreApplication.translate("Dialog", u"Ar", None))
        self.mfcAgas.setItemText(2, QCoreApplication.translate("Dialog", u"CH4", None))
        self.mfcAgas.setItemText(3, QCoreApplication.translate("Dialog", u"CO", None))
        self.mfcAgas.setItemText(4, QCoreApplication.translate("Dialog", u"CO2", None))
        self.mfcAgas.setItemText(5, QCoreApplication.translate("Dialog", u"C2H6", None))
        self.mfcAgas.setItemText(6, QCoreApplication.translate("Dialog", u"H2", None))
        self.mfcAgas.setItemText(7, QCoreApplication.translate("Dialog", u"He", None))
        self.mfcAgas.setItemText(8, QCoreApplication.translate("Dialog", u"N2", None))
        self.mfcAgas.setItemText(9, QCoreApplication.translate("Dialog", u"N2O", None))
        self.mfcAgas.setItemText(10, QCoreApplication.translate("Dialog", u"Ne", None))
        self.mfcAgas.setItemText(11, QCoreApplication.translate("Dialog", u"O2", None))
        self.mfcAgas.setItemText(12, QCoreApplication.translate("Dialog", u"C3H8", None))
        self.mfcAgas.setItemText(13, QCoreApplication.translate("Dialog", u"n-C4H10", None))
        self.mfcAgas.setItemText(14, QCoreApplication.translate("Dialog", u"C2H2", None))
        self.mfcAgas.setItemText(15, QCoreApplication.translate("Dialog", u"C2H4", None))
        self.mfcAgas.setItemText(16, QCoreApplication.translate("Dialog", u"i-C2H10", None))
        self.mfcAgas.setItemText(17, QCoreApplication.translate("Dialog", u"Kr", None))
        self.mfcAgas.setItemText(18, QCoreApplication.translate("Dialog", u"Xe", None))
        self.mfcAgas.setItemText(19, QCoreApplication.translate("Dialog", u"SF6", None))
        self.mfcAgas.setItemText(20, QCoreApplication.translate("Dialog", u"C-25", None))
        self.mfcAgas.setItemText(21, QCoreApplication.translate("Dialog", u"C-10", None))
        self.mfcAgas.setItemText(22, QCoreApplication.translate("Dialog", u"C-8", None))
        self.mfcAgas.setItemText(23, QCoreApplication.translate("Dialog", u"C-2", None))
        self.mfcAgas.setItemText(24, QCoreApplication.translate("Dialog", u"C-75", None))
        self.mfcAgas.setItemText(25, QCoreApplication.translate("Dialog", u"A-75", None))
        self.mfcAgas.setItemText(26, QCoreApplication.translate("Dialog", u"A-25", None))
        self.mfcAgas.setItemText(27, QCoreApplication.translate("Dialog", u"A1025", None))
        self.mfcAgas.setItemText(28, QCoreApplication.translate("Dialog", u"Star29", None))
        self.mfcAgas.setItemText(29, QCoreApplication.translate("Dialog", u"P-5", None))

        self.mfccontrollerlabel.setText(QCoreApplication.translate("Dialog", u"MFC Controllers:", None))
        self.mfcAlabel.setText(QCoreApplication.translate("Dialog", u"MFC A:", None))
        self.mfcBlabel.setText(QCoreApplication.translate("Dialog", u"MFC B:", None))
        self.mfcClabel.setText(QCoreApplication.translate("Dialog", u"MFC C:", None))
        self.mfcBgas.setItemText(0, QCoreApplication.translate("Dialog", u"Air", None))
        self.mfcBgas.setItemText(1, QCoreApplication.translate("Dialog", u"Ar", None))
        self.mfcBgas.setItemText(2, QCoreApplication.translate("Dialog", u"CH4", None))
        self.mfcBgas.setItemText(3, QCoreApplication.translate("Dialog", u"CO", None))
        self.mfcBgas.setItemText(4, QCoreApplication.translate("Dialog", u"CO2", None))
        self.mfcBgas.setItemText(5, QCoreApplication.translate("Dialog", u"C2H6", None))
        self.mfcBgas.setItemText(6, QCoreApplication.translate("Dialog", u"H2", None))
        self.mfcBgas.setItemText(7, QCoreApplication.translate("Dialog", u"He", None))
        self.mfcBgas.setItemText(8, QCoreApplication.translate("Dialog", u"N2", None))
        self.mfcBgas.setItemText(9, QCoreApplication.translate("Dialog", u"N2O", None))
        self.mfcBgas.setItemText(10, QCoreApplication.translate("Dialog", u"Ne", None))
        self.mfcBgas.setItemText(11, QCoreApplication.translate("Dialog", u"O2", None))
        self.mfcBgas.setItemText(12, QCoreApplication.translate("Dialog", u"C3H8", None))
        self.mfcBgas.setItemText(13, QCoreApplication.translate("Dialog", u"n-C4H10", None))
        self.mfcBgas.setItemText(14, QCoreApplication.translate("Dialog", u"C2H2", None))
        self.mfcBgas.setItemText(15, QCoreApplication.translate("Dialog", u"C2H4", None))
        self.mfcBgas.setItemText(16, QCoreApplication.translate("Dialog", u"i-C2H10", None))
        self.mfcBgas.setItemText(17, QCoreApplication.translate("Dialog", u"Kr", None))
        self.mfcBgas.setItemText(18, QCoreApplication.translate("Dialog", u"Xe", None))
        self.mfcBgas.setItemText(19, QCoreApplication.translate("Dialog", u"SF6", None))
        self.mfcBgas.setItemText(20, QCoreApplication.translate("Dialog", u"C-25", None))
        self.mfcBgas.setItemText(21, QCoreApplication.translate("Dialog", u"C-10", None))
        self.mfcBgas.setItemText(22, QCoreApplication.translate("Dialog", u"C-8", None))
        self.mfcBgas.setItemText(23, QCoreApplication.translate("Dialog", u"C-2", None))
        self.mfcBgas.setItemText(24, QCoreApplication.translate("Dialog", u"C-75", None))
        self.mfcBgas.setItemText(25, QCoreApplication.translate("Dialog", u"A-75", None))
        self.mfcBgas.setItemText(26, QCoreApplication.translate("Dialog", u"A-25", None))
        self.mfcBgas.setItemText(27, QCoreApplication.translate("Dialog", u"A1025", None))
        self.mfcBgas.setItemText(28, QCoreApplication.translate("Dialog", u"Star29", None))
        self.mfcBgas.setItemText(29, QCoreApplication.translate("Dialog", u"P-5", None))

        self.mfcCgas.setItemText(0, QCoreApplication.translate("Dialog", u"Air", None))
        self.mfcCgas.setItemText(1, QCoreApplication.translate("Dialog", u"Ar", None))
        self.mfcCgas.setItemText(2, QCoreApplication.translate("Dialog", u"CH4", None))
        self.mfcCgas.setItemText(3, QCoreApplication.translate("Dialog", u"CO", None))
        self.mfcCgas.setItemText(4, QCoreApplication.translate("Dialog", u"CO2", None))
        self.mfcCgas.setItemText(5, QCoreApplication.translate("Dialog", u"C2H6", None))
        self.mfcCgas.setItemText(6, QCoreApplication.translate("Dialog", u"H2", None))
        self.mfcCgas.setItemText(7, QCoreApplication.translate("Dialog", u"He", None))
        self.mfcCgas.setItemText(8, QCoreApplication.translate("Dialog", u"N2", None))
        self.mfcCgas.setItemText(9, QCoreApplication.translate("Dialog", u"N2O", None))
        self.mfcCgas.setItemText(10, QCoreApplication.translate("Dialog", u"Ne", None))
        self.mfcCgas.setItemText(11, QCoreApplication.translate("Dialog", u"O2", None))
        self.mfcCgas.setItemText(12, QCoreApplication.translate("Dialog", u"C3H8", None))
        self.mfcCgas.setItemText(13, QCoreApplication.translate("Dialog", u"n-C4H10", None))
        self.mfcCgas.setItemText(14, QCoreApplication.translate("Dialog", u"C2H2", None))
        self.mfcCgas.setItemText(15, QCoreApplication.translate("Dialog", u"C2H4", None))
        self.mfcCgas.setItemText(16, QCoreApplication.translate("Dialog", u"i-C2H10", None))
        self.mfcCgas.setItemText(17, QCoreApplication.translate("Dialog", u"Kr", None))
        self.mfcCgas.setItemText(18, QCoreApplication.translate("Dialog", u"Xe", None))
        self.mfcCgas.setItemText(19, QCoreApplication.translate("Dialog", u"SF6", None))
        self.mfcCgas.setItemText(20, QCoreApplication.translate("Dialog", u"C-25", None))
        self.mfcCgas.setItemText(21, QCoreApplication.translate("Dialog", u"C-10", None))
        self.mfcCgas.setItemText(22, QCoreApplication.translate("Dialog", u"C-8", None))
        self.mfcCgas.setItemText(23, QCoreApplication.translate("Dialog", u"C-2", None))
        self.mfcCgas.setItemText(24, QCoreApplication.translate("Dialog", u"C-75", None))
        self.mfcCgas.setItemText(25, QCoreApplication.translate("Dialog", u"A-75", None))
        self.mfcCgas.setItemText(26, QCoreApplication.translate("Dialog", u"A-25", None))
        self.mfcCgas.setItemText(27, QCoreApplication.translate("Dialog", u"A1025", None))
        self.mfcCgas.setItemText(28, QCoreApplication.translate("Dialog", u"Star29", None))
        self.mfcCgas.setItemText(29, QCoreApplication.translate("Dialog", u"P-5", None))

        self.mfcDgas.setItemText(0, QCoreApplication.translate("Dialog", u"Air", None))
        self.mfcDgas.setItemText(1, QCoreApplication.translate("Dialog", u"Ar", None))
        self.mfcDgas.setItemText(2, QCoreApplication.translate("Dialog", u"CH4", None))
        self.mfcDgas.setItemText(3, QCoreApplication.translate("Dialog", u"CO", None))
        self.mfcDgas.setItemText(4, QCoreApplication.translate("Dialog", u"CO2", None))
        self.mfcDgas.setItemText(5, QCoreApplication.translate("Dialog", u"C2H6", None))
        self.mfcDgas.setItemText(6, QCoreApplication.translate("Dialog", u"H2", None))
        self.mfcDgas.setItemText(7, QCoreApplication.translate("Dialog", u"He", None))
        self.mfcDgas.setItemText(8, QCoreApplication.translate("Dialog", u"N2", None))
        self.mfcDgas.setItemText(9, QCoreApplication.translate("Dialog", u"N2O", None))
        self.mfcDgas.setItemText(10, QCoreApplication.translate("Dialog", u"Ne", None))
        self.mfcDgas.setItemText(11, QCoreApplication.translate("Dialog", u"O2", None))
        self.mfcDgas.setItemText(12, QCoreApplication.translate("Dialog", u"C3H8", None))
        self.mfcDgas.setItemText(13, QCoreApplication.translate("Dialog", u"n-C4H10", None))
        self.mfcDgas.setItemText(14, QCoreApplication.translate("Dialog", u"C2H2", None))
        self.mfcDgas.setItemText(15, QCoreApplication.translate("Dialog", u"C2H4", None))
        self.mfcDgas.setItemText(16, QCoreApplication.translate("Dialog", u"i-C2H10", None))
        self.mfcDgas.setItemText(17, QCoreApplication.translate("Dialog", u"Kr", None))
        self.mfcDgas.setItemText(18, QCoreApplication.translate("Dialog", u"Xe", None))
        self.mfcDgas.setItemText(19, QCoreApplication.translate("Dialog", u"SF6", None))
        self.mfcDgas.setItemText(20, QCoreApplication.translate("Dialog", u"C-25", None))
        self.mfcDgas.setItemText(21, QCoreApplication.translate("Dialog", u"C-10", None))
        self.mfcDgas.setItemText(22, QCoreApplication.translate("Dialog", u"C-8", None))
        self.mfcDgas.setItemText(23, QCoreApplication.translate("Dialog", u"C-2", None))
        self.mfcDgas.setItemText(24, QCoreApplication.translate("Dialog", u"C-75", None))
        self.mfcDgas.setItemText(25, QCoreApplication.translate("Dialog", u"A-75", None))
        self.mfcDgas.setItemText(26, QCoreApplication.translate("Dialog", u"A-25", None))
        self.mfcDgas.setItemText(27, QCoreApplication.translate("Dialog", u"A1025", None))
        self.mfcDgas.setItemText(28, QCoreApplication.translate("Dialog", u"Star29", None))
        self.mfcDgas.setItemText(29, QCoreApplication.translate("Dialog", u"P-5", None))

        self.mfcDlabel.setText(QCoreApplication.translate("Dialog", u"MFC D:", None))
        self.drivergaslabel.setText(QCoreApplication.translate("Dialog", u"S1: Driver gas injection", None))
        self.openS1.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.closeS1.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.fuellabel.setText(QCoreApplication.translate("Dialog", u"S2: Fuel injection", None))
        self.closeS2.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.openS2.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.oxidizerlabel.setText(QCoreApplication.translate("Dialog", u"S3: Oxidizer and Dilutent Inection", None))
        self.closeS3.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.openS3.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.purgelabel.setText(QCoreApplication.translate("Dialog", u"S4: Purge *default open*", None))
        self.openS4.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.closeS4.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.closeS5.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.staticpressurelabel.setText(QCoreApplication.translate("Dialog", u"S5: Static pressure sensor protection", None))
        self.openS5.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.closeS6.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.exhaustlabel.setText(QCoreApplication.translate("Dialog", u"S6: Exhaust *default open*", None))
        self.openS6.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.closeS7.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.vacuumlabel.setText(QCoreApplication.translate("Dialog", u"S7: Vaccuum valve", None))
        self.openS7.setText(QCoreApplication.translate("Dialog", u"Open", None))
        self.setpointlabel1.setText(QCoreApplication.translate("Dialog", u"Setpoint:", None))
        self.setpointlabel2.setText(QCoreApplication.translate("Dialog", u"Setpoint:", None))
        self.setpointlabel3.setText(QCoreApplication.translate("Dialog", u"Setpoint:", None))
        self.setpointlabel4.setText(QCoreApplication.translate("Dialog", u"Setpoint:", None))
        self.SLPMlabel1.setText(QCoreApplication.translate("Dialog", u"SLPM", None))
        self.SLPMlabel2.setText(QCoreApplication.translate("Dialog", u"SLPM", None))
        self.SLPMlabel3.setText(QCoreApplication.translate("Dialog", u"SLPM", None))
        self.SLPMlabel4.setText(QCoreApplication.translate("Dialog", u"SLPM", None))
        self.updatesetpoints.setText(QCoreApplication.translate("Dialog", u"Update Setpoints", None))
        self.resetmfc.setText(QCoreApplication.translate("Dialog", u"Reset flow", None))
        self.solenoidstatelabel.setText(QCoreApplication.translate("Dialog", u"Solenoid States:", None))
        self.staticpressurelabel_2.setText(QCoreApplication.translate("Dialog", u"Static Pressure", None))
        self.pressuremonitorlabel.setText(QCoreApplication.translate("Dialog", u"Pressure Monitors:", None))
        self.testautomation.setText(QCoreApplication.translate("Dialog", u"Begin Testing", None))
        self.emergencypurge.setText(QCoreApplication.translate("Dialog", u"Emergency Purge", None))
        self.mfcAsetpoint.setText(QCoreApplication.translate("Dialog", u"0.0", None))
        self.mfcBsetpoint.setText(QCoreApplication.translate("Dialog", u"0.0", None))
        self.mfcCsetpoint.setText(QCoreApplication.translate("Dialog", u"0.0", None))
        self.mfcDsetpoint.setText(QCoreApplication.translate("Dialog", u"0.0", None))
        self.standardpurge.setText(QCoreApplication.translate("Dialog", u"Standard Purge", None))
    # retranslateUi

