from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

# TODO make abstract

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.initLayout()

    def initLayout(self):
        self.setLayout(self.mainLayout)

    def getLayout(self):
        return self.mainLayout

    @pyqtSlot(bool)
    def surveyMode(self, modeOn):
        pass

    @pyqtSlot(bool)
    def extractMode(self, modeOn):
        pass