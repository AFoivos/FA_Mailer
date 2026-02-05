# -*- coding: utf-8 -*-

"""
AF Mailer
Copyright (c) 2026 Φοίβος Γεώργιος Αμπατζής

All rights reserved.
Unauthorized copying, modification or distribution is prohibited.
"""

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(986, 791)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lblBody = QTextEdit(self.centralwidget)
        self.lblBody.setObjectName(u"lblBody")
        self.lblBody.setGeometry(QRect(32, 60, 721, 311))
        self.txtSubject = QLineEdit(self.centralwidget)
        self.txtSubject.setObjectName(u"txtSubject")
        self.txtSubject.setGeometry(QRect(30, 20, 721, 20))
        self.txtSubject.setClearButtonEnabled(True)
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(760, 270, 211, 25))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lblExcel = QLabel(self.horizontalLayoutWidget)
        self.lblExcel.setObjectName(u"lblExcel")

        self.horizontalLayout.addWidget(self.lblExcel)

        self.txtExcel = QLineEdit(self.horizontalLayoutWidget)
        self.txtExcel.setObjectName(u"txtExcel")

        self.horizontalLayout.addWidget(self.txtExcel)

        self.btnBrowseExcel = QPushButton(self.horizontalLayoutWidget)
        self.btnBrowseExcel.setObjectName(u"btnBrowseExcel")

        self.horizontalLayout.addWidget(self.btnBrowseExcel)

        self.grpPlaceholders = QGroupBox(self.centralwidget)
        self.grpPlaceholders.setObjectName(u"grpPlaceholders")
        self.grpPlaceholders.setGeometry(QRect(760, 20, 211, 251))
        self.layoutWidget = QWidget(self.grpPlaceholders)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 191, 221))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lblPhHint = QLabel(self.layoutWidget)
        self.lblPhHint.setObjectName(u"lblPhHint")

        self.verticalLayout_2.addWidget(self.lblPhHint)

        self.listPlaceholders = QListWidget(self.layoutWidget)
        self.listPlaceholders.setObjectName(u"listPlaceholders")
        self.listPlaceholders.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_2.addWidget(self.listPlaceholders)

        self.grpPersonalPdf = QGroupBox(self.centralwidget)
        self.grpPersonalPdf.setObjectName(u"grpPersonalPdf")
        self.grpPersonalPdf.setGeometry(QRect(30, 380, 261, 271))
        self.layoutWidget1 = QWidget(self.grpPersonalPdf)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 20, 251, 251))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lblPdfFolder = QLabel(self.layoutWidget1)
        self.lblPdfFolder.setObjectName(u"lblPdfFolder")

        self.horizontalLayout_4.addWidget(self.lblPdfFolder)

        self.txtPdfFolderName = QLineEdit(self.layoutWidget1)
        self.txtPdfFolderName.setObjectName(u"txtPdfFolderName")
        self.txtPdfFolderName.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.txtPdfFolderName)

        self.btnBrowsePdfFolder = QPushButton(self.layoutWidget1)
        self.btnBrowsePdfFolder.setObjectName(u"btnBrowsePdfFolder")

        self.horizontalLayout_4.addWidget(self.btnBrowsePdfFolder)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.lblPdfPatterns = QLabel(self.layoutWidget1)
        self.lblPdfPatterns.setObjectName(u"lblPdfPatterns")

        self.verticalLayout_3.addWidget(self.lblPdfPatterns)

        self.listPdfPatterns = QListWidget(self.layoutWidget1)
        self.listPdfPatterns.setObjectName(u"listPdfPatterns")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listPdfPatterns.sizePolicy().hasHeightForWidth())
        self.listPdfPatterns.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.listPdfPatterns)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnAddPdfPattern = QPushButton(self.layoutWidget1)
        self.btnAddPdfPattern.setObjectName(u"btnAddPdfPattern")

        self.horizontalLayout_5.addWidget(self.btnAddPdfPattern)

        self.btnRemovePdfPattern = QPushButton(self.layoutWidget1)
        self.btnRemovePdfPattern.setObjectName(u"btnRemovePdfPattern")

        self.horizontalLayout_5.addWidget(self.btnRemovePdfPattern)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.grpRun = QGroupBox(self.centralwidget)
        self.grpRun.setObjectName(u"grpRun")
        self.grpRun.setGeometry(QRect(300, 380, 331, 271))
        self.layoutWidget2 = QWidget(self.grpRun)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 322, 252))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioDraft = QRadioButton(self.layoutWidget2)
        self.radioDraft.setObjectName(u"radioDraft")

        self.horizontalLayout_7.addWidget(self.radioDraft)

        self.radioSend = QRadioButton(self.layoutWidget2)
        self.radioSend.setObjectName(u"radioSend")
        self.radioSend.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radioSend)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btnValidate = QPushButton(self.layoutWidget2)
        self.btnValidate.setObjectName(u"btnValidate")

        self.horizontalLayout_6.addWidget(self.btnValidate)

        self.btnPreview = QPushButton(self.layoutWidget2)
        self.btnPreview.setObjectName(u"btnPreview")

        self.horizontalLayout_6.addWidget(self.btnPreview)

        self.btnCheck = QPushButton(self.layoutWidget2)
        self.btnCheck.setObjectName(u"btnCheck")

        self.horizontalLayout_6.addWidget(self.btnCheck)

        self.btnRun = QPushButton(self.layoutWidget2)
        self.btnRun.setObjectName(u"btnRun")

        self.horizontalLayout_6.addWidget(self.btnRun)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.txtLog = QTextEdit(self.layoutWidget2)
        self.txtLog.setObjectName(u"txtLog")
        self.txtLog.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.txtLog)

        self.progressBar = QProgressBar(self.layoutWidget2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.verticalLayout_4.addWidget(self.progressBar)

        self.layoutWidget3 = QWidget(self.centralwidget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(640, 380, 239, 241))
        self.verticalLayout = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lblAttachments = QLabel(self.layoutWidget3)
        self.lblAttachments.setObjectName(u"lblAttachments")

        self.verticalLayout.addWidget(self.lblAttachments)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnAddAttachments = QPushButton(self.layoutWidget3)
        self.btnAddAttachments.setObjectName(u"btnAddAttachments")

        self.horizontalLayout_2.addWidget(self.btnAddAttachments)

        self.btnClearAttachments = QPushButton(self.layoutWidget3)
        self.btnClearAttachments.setObjectName(u"btnClearAttachments")

        self.horizontalLayout_2.addWidget(self.btnClearAttachments)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listAttachments = QListWidget(self.layoutWidget3)
        self.listAttachments.setObjectName(u"listAttachments")
        sizePolicy.setHeightForWidth(self.listAttachments.sizePolicy().hasHeightForWidth())
        self.listAttachments.setSizePolicy(sizePolicy)
        self.listAttachments.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.listAttachments)

        self.layoutWidget4 = QWidget(self.centralwidget)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(760, 300, 211, 22))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lblEmailCol = QLabel(self.layoutWidget4)
        self.lblEmailCol.setObjectName(u"lblEmailCol")

        self.horizontalLayout_3.addWidget(self.lblEmailCol)

        self.comboEmailCol = QComboBox(self.layoutWidget4)
        self.comboEmailCol.setObjectName(u"comboEmailCol")

        self.horizontalLayout_3.addWidget(self.comboEmailCol)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 60, 21, 83))
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btnBold = QPushButton(self.widget)
        self.btnBold.setObjectName(u"btnBold")
        self.btnBold.setCheckable(True)

        self.verticalLayout_5.addWidget(self.btnBold)

        self.btnItalic = QPushButton(self.widget)
        self.btnItalic.setObjectName(u"btnItalic")
        self.btnItalic.setCheckable(True)

        self.verticalLayout_5.addWidget(self.btnItalic)

        self.btnUnderline = QPushButton(self.widget)
        self.btnUnderline.setObjectName(u"btnUnderline")
        self.btnUnderline.setCheckable(True)

        self.verticalLayout_5.addWidget(self.btnUnderline)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 986, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lblBody.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.lblBody.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u039a\u03b5\u03af\u03bc\u03b5\u03bd\u03bf", None))
        self.txtSubject.setText("")
        self.txtSubject.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0398\u03ad\u03bc\u03b1", None))
        self.lblExcel.setText(QCoreApplication.translate("MainWindow", u"Excel :", None))
        self.btnBrowseExcel.setText(QCoreApplication.translate("MainWindow", u"Browse Excel\u2026", None))
        self.grpPlaceholders.setTitle(QCoreApplication.translate("MainWindow", u"\u0394\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03b1 placeholders (\u03b1\u03c0\u03cc Excel)", None))
        self.lblPhHint.setText(QCoreApplication.translate("MainWindow", u"\u0394\u03b9\u03c0\u03bb\u03cc \u03ba\u03bb\u03b9\u03ba \u03b3\u03b9\u03b1 \u03b1\u03bd\u03c4\u03b9\u03b3\u03c1\u03b1\u03c6\u03ae \u03c3\u03c4\u03bf clipboard", None))
        self.grpPersonalPdf.setTitle(QCoreApplication.translate("MainWindow", u"\u03a0\u03c1\u03bf\u03c3\u03c9\u03c0\u03b9\u03ba\u03ac PDF (\u03b1\u03bd\u03ac \u03ac\u03c4\u03bf\u03bc\u03bf)", None))
        self.lblPdfFolder.setText(QCoreApplication.translate("MainWindow", u"\u03a6\u03ac\u03ba\u03b5\u03bb\u03bf\u03c2 PDF:", None))
        self.txtPdfFolderName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0394\u03b5\u03bd \u03ad\u03c7\u03b5\u03b9 \u03b5\u03c0\u03b9\u03bb\u03b5\u03b3\u03b5\u03af \u03c6\u03ac\u03ba\u03b5\u03bb\u03bf\u03c2", None))
        self.btnBrowsePdfFolder.setText(QCoreApplication.translate("MainWindow", u"Browse\u2026", None))
        self.lblPdfPatterns.setText(QCoreApplication.translate("MainWindow", u"Patterns \u03b1\u03c1\u03c7\u03b5\u03af\u03c9\u03bd:", None))
        self.btnAddPdfPattern.setText(QCoreApplication.translate("MainWindow", u"\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7", None))
        self.btnRemovePdfPattern.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03c6\u03b1\u03af\u03c1\u03b5\u03c3\u03b7", None))
        self.grpRun.setTitle(QCoreApplication.translate("MainWindow", u"\u0395\u03ba\u03c4\u03ad\u03bb\u03b5\u03c3\u03b7", None))
        self.radioDraft.setText(QCoreApplication.translate("MainWindow", u"Save (Draft)", None))
        self.radioSend.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.btnValidate.setText(QCoreApplication.translate("MainWindow", u"Validate", None))
        self.btnPreview.setText(QCoreApplication.translate("MainWindow", u"Preview ", None))
        self.btnCheck.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.btnRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.txtLog.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0395\u03b4\u03ce \u03b8\u03b1 \u03b5\u03bc\u03c6\u03b1\u03bd\u03af\u03b6\u03bf\u03bd\u03c4\u03b1\u03b9 \u03c4\u03b1 \u03bc\u03b7\u03bd\u03cd\u03bc\u03b1\u03c4\u03b1...", None))
        self.lblAttachments.setText(QCoreApplication.translate("MainWindow", u"\u03a3\u03c5\u03bd\u03b7\u03bc\u03bc\u03ad\u03bd\u03b1:", None))
        self.btnAddAttachments.setText(QCoreApplication.translate("MainWindow", u"\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7", None))
        self.btnClearAttachments.setText(QCoreApplication.translate("MainWindow", u"\u039a\u03b1\u03b8\u03b1\u03c1\u03b9\u03c3\u03bc\u03cc\u03c2", None))
        self.lblEmailCol.setText(QCoreApplication.translate("MainWindow", u"\u03a3\u03c4\u03ae\u03bb\u03b7 Email:", None))
        self.btnBold.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.btnItalic.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.btnUnderline.setText(QCoreApplication.translate("MainWindow", u"U", None))
    # retranslateUi

