from PyQt5.QtWidgets import QActionGroup, QAction
from PyQt5.QtCore import pyqtSignal

from ..AppEnums import ScreenMode

class AbstractActionGroup(QActionGroup):
    switchSignal = pyqtSignal(QAction)

    def __init__(self, parent=None):
        super().__init__(parent)

    def initAction(self):
        pass

    def switchAction(self):
        pass

# TODO defunct
class ViewActionGroup(QActionGroup):

    switchSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.generateAction = QAction("Prepare", self)
        self.processAction = QAction("Process", self)
        self.trainAction = QAction("Train", self)

        self.initActions()

    def initActions(self):
        # set checkable
        self.generateAction.setCheckable(True)
        self.processAction.setCheckable(False)
        self.trainAction.setCheckable(False)

        # disable
        self.processAction.setDisabled(False)
        self.trainAction.setDisabled(False)

        # set clicked
        self.generateAction.setChecked(True)

        # remove for now
        self.generateAction.setVisible(True)
        self.processAction.setVisible(False)
        self.trainAction.setVisible(True)

        # connect to signals
        self.generateAction.triggered.connect(lambda ignore : self.switchSignal.emit(0)) # TODO enum
        self.processAction.triggered.connect(lambda ignore : self.switchSignal.emit(1))
        self.trainAction.triggered.connect(lambda ignore : self.switchSignal.emit(2))

    def switchAction(self, option):
        print("Switch View Test")

class SettingsActionGroup(QActionGroup):

    settingsSignal = pyqtSignal()
    helpSignal = pyqtSignal()
    exportSignal = pyqtSignal()
    dockSignal = pyqtSignal()
    licenseSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.settingsAction = QAction("Settings", self)
        self.exportAction = QAction("Export", self)
        self.dockAction = QAction("Dock", self)
        self.licenseAction = QAction("License", self)
        self.helpAction = QAction("Help", self)
        self.initActions()

    def initActions(self):
        # set checkable
        self.settingsAction.setCheckable(False)
        self.helpAction.setCheckable(False)
        self.exportAction.setCheckable(False)
        self.dockAction.setCheckable(False)
        self.licenseAction.setCheckable(False)

        # connect to signals
        self.settingsAction.triggered.connect(self.settingsSignal.emit)
        self.helpAction.triggered.connect(self.helpSignal.emit)
        self.exportAction.triggered.connect(self.exportSignal.emit)
        self.dockAction.triggered.connect(self.dockSignal.emit)
        self.licenseAction.triggered.connect(self.licenseSignal.emit)


class GenerateModeActionGroup(QActionGroup):

    switchSignal = pyqtSignal(ScreenMode)

    def __init__(self, parent):
        super().__init__(parent)

        self.allAction = QAction("All", self)
        self.prepareAction = QAction("Prepare", self)
        self.editAction = QAction("Edit", self)
        self.surveyAction = QAction("Survey", self)
        self.extractAction = QAction("Extract", self)
        self.processAction = QAction("Process", self)
        self.trainAction = QAction("Train", self)

        self.initActions()

    def initActions(self):
        # set checkable
        self.allAction.setCheckable(True)
        self.editAction.setCheckable(True)
        self.surveyAction.setCheckable(True)
        self.extractAction.setCheckable(True)
        self.processAction.setCheckable(True)
        self.prepareAction.setCheckable(True)
        self.trainAction.setCheckable(True)

        # disable
        self.allAction.setDisabled(False)
        self.surveyAction.setDisabled(True)
        self.extractAction.setDisabled(False)
        self.trainAction.setDisabled(True)

        # set clicked
        self.prepareAction.setChecked(True)

        # remove unncessary TODO actually delete
        self.allAction.setCheckable(True)
        self.editAction.setVisible(False)
        self.surveyAction.setVisible(False)
        self.extractAction.setVisible(False)

        # connect to signals
        self.allAction.triggered.connect(lambda ignore : self.switchSignal.emit(ScreenMode.ALL))
        self.editAction.triggered.connect(lambda ignore : self.switchSignal.emit(ScreenMode.EDIT))
        self.surveyAction.triggered.connect(lambda ignore : self.switchSignal.emit(ScreenMode.SURVEY))
        self.extractAction.triggered.connect(lambda ignore : self.switchSignal.emit(ScreenMode.EXTRACT))
        self.processAction.triggered.connect(lambda ignore: self.switchSignal.emit(ScreenMode.PROCESS))
        self.trainAction.triggered.connect(lambda ignore: self.switchSignal.emit(ScreenMode.TRAIN))
        self.prepareAction.triggered.connect(lambda ignore: self.switchSignal.emit(ScreenMode.PREPARE))

    def switchAction(self, option):
        print("Switch Mode Test")
        self.switchSignal.emit(option)


