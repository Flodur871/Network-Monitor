# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Network Monito.ui'
#
# Created: Wed Feb 07 10:58:56 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(850, 546)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Ifaces = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Ifaces.sizePolicy().hasHeightForWidth())
        self.Ifaces.setSizePolicy(sizePolicy)
        self.Ifaces.setMinimumSize(QtCore.QSize(225, 0))
        self.Ifaces.setObjectName("Ifaces")
        self.gridLayout.addWidget(self.Ifaces, 0, 1, 1, 1)
        self.Iface = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Iface.sizePolicy().hasHeightForWidth())
        self.Iface.setSizePolicy(sizePolicy)
        self.Iface.setObjectName("Iface")
        self.gridLayout.addWidget(self.Iface, 0, 0, 1, 1)
        self.Start = QtGui.QPushButton(self.centralwidget)
        self.Start.setObjectName("Start")
        self.gridLayout.addWidget(self.Start, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        self.Table = QtGui.QTreeWidget(self.centralwidget)
        self.Table.setIndentation(0)
        self.Table.setObjectName("Table")
        self.Table.header().setDefaultSectionSize(135)
        self.Table.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.Table, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 833, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.menuStyle = QtGui.QMenu(self.menubar)
        self.menuStyle.setObjectName("menuStyle")

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()

        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Ifaces, self.Start)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "Network Monitor", None, QtGui.QApplication.UnicodeUTF8))
        self.Iface.setText(QtGui.QApplication.translate("MainWindow", "Iface", None, QtGui.QApplication.UnicodeUTF8))
        self.Start.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Status", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "IP", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Name", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Mac Address", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Manufacturer", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.Table.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "OS", None,
                                                                        QtGui.QApplication.UnicodeUTF8))

        self.Table.headerItem().setText(6, QtGui.QApplication.translate("MainWindow", "Ping", None,
                                                                        QtGui.QApplication.UnicodeUTF8))

        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuStyle.setTitle(
            QtGui.QApplication.translate("MainWindow", "Themes", None, QtGui.QApplication.UnicodeUTF8))

        self.actionExit.setText(
            QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(
            QtGui.QApplication.translate("MainWindow", "About...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(
            QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
