from PyQt5.QtWidgets import QWidget

class StatusBarWidget(QWidget):

    def __init__(self, mainWindow):
        super().__init__(parent=mainWindow)
        self.text = ""
        self.mainWindow = mainWindow
        self.addWidget()

    def showTextMessage(self, text):
        self.text = text
        self.mainWindow.statusBar().showMessage(text)

    def removeWidget(self):
        self.mainWindow.statusBar().removeWidget(self)

    def addWidget(self):
        self.mainWindow.statusBar().addWidget(self)
