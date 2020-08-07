import sys
import datetime

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QListView, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QAbstractListModel, QItemSelection

from PyQt5.QtCore import pyqtSlot, pyqtSignal

class LogWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # list
        self.listView = QListView()
        self.logList = []
        self.listModel = LogListModel(self.logList)
        self.listView.setModel(self.listModel)
        self.logItem("Log initialized.")

        # buttons
        self.clearButton = QPushButton("Clear")

        self.__connect()
        self.__assemble()

    # TODO fix unpredictable behavior
    @pyqtSlot(str)
    def logItem(self, logText):
        self.logList.append(str(datetime.datetime.now()) + ": " + logText)
        self.listModel.layoutChanged.emit()

    def __connect(self):
        self.clearButton.clicked.connect(self.__clearList)

    def __clearList(self):
        self.logList.clear()
        self.listModel.layoutChanged.emit()

    def __assemble(self):
        self.mainLayout.addWidget(self.listView, 0, 0, 2, 2)
        self.mainLayout.addWidget(self.clearButton, 2, 1, 1, 1)

class LogListModel(QAbstractListModel):

    def __init__(self, logList, *args, **kwargs):
        super(LogListModel, self).__init__(*args, **kwargs)
        self.logList = logList

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.logList[index.row()]

    def rowCount(self, index):
        return len(self.logList)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LogWidget()
    widget.show()
    sys.exit(app.exec_())