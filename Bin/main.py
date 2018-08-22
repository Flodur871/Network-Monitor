# -*- coding: utf8 -*-
from cPickle import loads  # faster than the regular pickle
from screen import Screen
from PySide import QtGui, QtCore
from scapy.all import *
from scanner import Scan
from time import strftime
import win32gui
import win32clipboard
import win32con
import design  # This file holds our MainWindow and all design related things
import sys  # We need sys so that we can pass argv to QApplication

conf.verb = 0  # stops scapy from printing commands (similar to @echo off)


class UI(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically

        self.control = False  # if control button was pressed
        self.log = ''
        self.logged = ''
        self.screen = None

        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setTextVisible(True)
        self.fred = Scan()

        self.iface = IFACES.values()[0]

        self.Table.viewport().installEventFilter(self)
        self.run()
        self.canceled = False

    def eventFilter(self, obj, event):
        """
        decide what to do when an event happens
        :param obj: object the event happened on
        :param event: the event that just occurred
        :return: QWidget event filter result
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.Table.clearSelection()
            self.Table.mousePressEvent(event)

        elif event.type() == QtCore.QEvent.ContextMenu:
            self.contextmenu(event.pos())

        return QtGui.QWidget.eventFilter(self, obj, event)

    def change_iface(self, i):
        """
        change current iface
        :param i: index of the selected iface
        """
        if not self.canceled:
            if self.Table.itemAt(0, 0):

                if self.warning_msg():
                    self.start()
                    self.set_iface(i)
                    self.Table.clear()

                else:
                    self.canceled = True
                    self.Ifaces.setCurrentIndex(self.Ifaces.findText(str(self.iface)[1:-40]))

            else:
                self.set_iface(i)

        else:
            self.canceled = False

    def error_msg(self):
        """
        show a critical error message when an interface isn't connected
        Change the stop button text back to start
        """
        QtGui.QMessageBox.critical(None, 'Error!', 'The interface selected doesn\'t seem to be connected to a network',
                                   QtGui.QMessageBox.Ok)

        self.statusbar.showMessage('Offline')
        self.start()

    def change_status(self, ip, status):
        """
        finds and change status (offline/online)
        :param ip: target ip address
        :param status: new status
        :return: the requested ip object in the table
        """
        it = QtGui.QTreeWidgetItemIterator(self.Table)

        while it.value():
            if it.value().text(1) == ip:
                it.value().setText(0, status)
                return it.value()

            it += 1

    def new(self, ip, status):
        """
        create a new status based on the change
        :param ip: requested ip
        :param status: new status
        """
        QtGui.QMessageBox.information(None, 'Network Monitor', '{} has {} the network'.format(ip, status),
                                      QtGui.QMessageBox.Ok)
        if status == 'left':
            self.change_status(ip, 'Offline')

    @staticmethod
    def warning_msg():
        """
        shows a warning when content may not be saved
        :return: True if Ok was pressed and False otherwise
        True if ok was pressed
        False if cancel was pressed
        """
        msg = QtGui.QMessageBox.warning(None, 'Network Montior', 'All changes made will not be saved',
                                        QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)

        if msg == QtGui.QMessageBox.Ok:  # ok button was pressed
            return True

        return False

    def set_iface(self, i):
        """
        finds and sets the interface to the requested one
        :param i: index of the selected interface
        """
        self.statusbar.showMessage('Ready')
        ifa = self.Ifaces.itemText(i)
        for x in IFACES.values():
            if ifa in str(x):
                self.iface = x
                break

    def contextmenu(self, pos):
        """
        opens a context menu
        :param pos: mouse position when clicked
        """
        menu = QtGui.QMenu()
        copyaction = menu.addAction('Copy')
        scan = menu.addAction('Scan Host')
        action = menu.exec_(self.Table.viewport().mapToGlobal(pos))

        if action == copyaction:
            self.copy()

        elif action == scan:
            selected = self.Table.selectedItems()
            if selected:
                self.screen = Screen(selected[0].text(1))
                self.screen.start()

    def keyPressEvent(self, k):
        """
        closes the program if esc was pressed
        :param k: key that was pressed
        """
        if k.key() == QtCore.Qt.Key_Escape:
            self.close()

        if k.key() == 16777249:
            self.control = True

        if self.control and k.key() == 67:
            self.copy()
            self.control = False

    def check_status(self, new):
        it = QtGui.QTreeWidgetItemIterator(self.Table)

        while it.value():
            val = it.value()
            if val.text(1) == new[1]:
                for x in xrange(len(new)):
                    if val.text(x) != new[x]:
                        val.setText(x, new[x])
            it += 1

        return False

    def add_device(self, st):
        """
        appends a new item to the tree widget
        :param st: pickle object of list of items to add
        """
        x = loads(str(st))
        item = self.change_status(x, 'Online')

        if not item:
            self.fred.ips.append(x[1])
            ips = sorted(self.fred.ips, key=lambda z: map(int, z.split('.')))
            i = ips.index(x[1])

            item = QtGui.QTreeWidgetItem(x)

            for y in xrange(len(x)):
                if x[y] == 'n\\a':
                    item.setBackground(y, QtGui.QBrush(QtGui.QColor(215, 0, 0)))

            if x[-1][:-2].isdigit():
                cr = int(x[-1][:-2])

                if cr < 100:
                    col = QtGui.QColor(0, 255 - cr, 0)

                elif cr < 200:
                    col = QtGui.QColor(255 - cr, 0, 0)

                else:
                    col = QtGui.QColor(55, 0, 0)

                item.setBackground(x.index(x[-1]), QtGui.QBrush(col))

            self.Table.insertTopLevelItem(i, item)

            self.log += '{}({}) is online ({})\n'.format(x[1], x[3], strftime('%X'))

    def loading(self, val):
        """
        sets the progress bar as needed`
        :param val: value needed
        """
        if val == 0:
            self.progressBar.setRange(0, 0)  # sets the progress bar to busy mode

        elif val == 1:
            self.progressBar.setValue(self.progressBar.value() + 1)  # increase current value by one

        else:
            self.progressBar.setMaximum(val)
            self.progressBar.setValue(0)

            self.log += 'Initial scan has been activated on {}({})\n'.format(self.Ifaces.currentText(),
                                                                             time.strftime('%X'))

    def copy(self):
        """
        copies the selected text over to the clipboard
        """
        selected = self.Table.selectedItems()
        if selected:
            txt = selected[0].text(1)
            win32clipboard.OpenClipboard()

            win32clipboard.SetClipboardData(1, txt)
            win32clipboard.SetClipboardData(7, txt)
            win32clipboard.SetClipboardData(13, txt.decode('utf-8'))

            win32clipboard.CloseClipboard()
            self.Table.clearSelection()
            self.Table.clearFocus()

    def done(self):
        """
        called when the scan is done
        sets the text on the button to start
        sets the progress back to normal mode
        """
        self.Start.setText(QtGui.QApplication.translate("MainWindow", u"Start".encode('utf-8'), None,
                                                        QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setRange(0, 1)

        self.log += 'The scan was canceled by the user({})\n'.format(time.strftime('%X'))

    def save(self):
        """
        saves scan results
        """
        filter = 'Log files (*.log)\0*.log\0All files (*.*)\0*.*\0'
        customfilter = 'Other file types\0*.*\0'
        fname = None

        try:
            fname, customfilter, flags = win32gui.GetSaveFileNameW(
                InitialDir='C:\\',
                Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER,
                File='', DefExt='log',
                Title='Save File',
                Filter=filter,
                CustomFilter=customfilter,
                FilterIndex=1)

        except:
            pass

        if fname:
            with open(fname, 'w') as f:
                f.write(self.log)

            self.logged = self.log

    def connection(self):
        """
        connect our fred to all the different functions
        """
        self.connect(self.fred, QtCore.SIGNAL('status(QString)'), lambda x: self.statusbar.showMessage(x))
        self.connect(self.fred, QtCore.SIGNAL('finished()'), self.done)
        self.connect(self.fred, QtCore.SIGNAL('prog(int)'), self.loading)
        self.connect(self.fred, QtCore.SIGNAL('error()'), self.error_msg)
        self.connect(self.fred, QtCore.SIGNAL('device(QString)'), self.add_device)
        self.connect(self.fred, QtCore.SIGNAL('neo(QString, QString)'), self.new)

    def start(self):
        """
        starts/stops the scan thread
        """
        if self.Start.text() == 'Start':

            if self.statusbar.currentMessage() == 'Offline Interface':
                self.statusbar.showMessage('Ready')
                return

            self.Start.setText(QtGui.QApplication.translate("MainWindow", u"Stop".encode('utf-8'), None,
                                                            QtGui.QApplication.UnicodeUTF8))

            conf.iface = self.iface
            self.fred = Scan()
            self.connection()

            self.fred.start()

        else:

            if self.Table.itemAt(0, 0):

                if self.warning_msg():
                    self.Table.clear()

                else:
                    return

            if self.fred.isRunning():
                self.fred.terminate()

            self.Start.setText(QtGui.QApplication.translate('MainWindow', u'Start'.encode('utf-8'), None,
                                                            QtGui.QApplication.UnicodeUTF8))

            self.statusbar.showMessage('Offline Interface')

    def run(self):
        """
        sets all the necessary adjustments to start the program
        """
        ifaces = IFACES.values()
        for x in ifaces:
            self.Ifaces.addItem(str(x)[1:-40])

        self.Table.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Start.clicked.connect(self.start)
        self.Ifaces.currentIndexChanged.connect(self.set_iface)
        self.actionExit.triggered.connect(lambda: self.close())
        self.actionSave.triggered.connect(self.save)
        self.actionSave.setShortcut(QtGui.QKeySequence.Save)

        header = self.Table.header()
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        self.statusbar.insertPermanentWidget(0, self.progressBar)
        self.statusbar.showMessage('Ready')

    def closeEvent(self, event):
        """
        triggered when user tries to close the program
        if a scan is running shows an warning message
        :param event: close event
        """
        if self.Table.itemAt(0, 0):
            if self.logged != self.log:
                if not self.warning_msg():  # if cancel was pressed abort the exiting
                    event.ignore()
                    return

        if self.fred.isRunning():
            self.fred.terminate()

        sys.exit(0)


def main():
    """
    main function
    """
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = UI()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    sys.exit(app.exec_())  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
