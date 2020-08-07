import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableView, QAbstractItemView, QHeaderView, QLabel, QPushButton
from PyQt5.QtCore import pyqtSlot

from .AppWidget import AppWidget

class StampTableView(AppWidget):

    def __init__(self):
        super().__init__()

        # table
        self.stampTableView = QTableView()
        self.initTableView()

        # buttons
        self.addStampButton = QPushButton("Add")
        self.deleteStampButton = QPushButton("Delete")
        self.hotkeyButton = QPushButton("Hotkeys")

        self.assemble(self.initButtons())

    def initTableView(self):
        self.stampTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stampTableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.stampTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.stampTableView.setSortingEnabled(True) # need to ensure PK

    def initButtons(self):
        self.addStampButton.setDisabled(True)
        self.deleteStampButton.setDisabled(True)
        self.hotkeyButton.setDisabled(True)
        self.hotkeyButton.setCheckable(True)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addStampButton)
        buttonLayout.addWidget(self.deleteStampButton)
        buttonLayout.addWidget(self.hotkeyButton)
        return buttonLayout

    def assemble(self, buttonLayout):
        self.mainLayout.addWidget(self.stampTableView)
        self.mainLayout.addLayout(buttonLayout)

    @pyqtSlot(bool)
    def editMode(self, modeOn):
        self.addStampButton.setDisabled(modeOn)
        self.hotkeyButton.setDisabled(modeOn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StampTableView()
    widget.show()
    sys.exit(app.exec_())