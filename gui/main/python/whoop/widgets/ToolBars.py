"""
Application toolbars.

Author: Alexander Shiarella
"""

from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from .ActionGroups import ViewActionGroup, GenerateModeActionGroup, SettingsActionGroup
from ..AppEnums import ScreenMode

class ViewToolBar(QToolBar):
    """No longer used. Leaving as reminder for adding multiple screens later."""

    generateSignal = pyqtSignal(bool)
    processSignal = pyqtSignal(bool)
    trainSignal = pyqtSignal(bool)
    switchSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.actionGroup = ViewActionGroup(self)
        self.addActions(self.actionGroup.actions())
        self.actionGroup.switchSignal.connect(self.switchSignal)

    def onSwitch(self, option):
        if option == 0:
            self.generateSignal.emit(True)
        if option == 1:
            self.processSignal.emit(True)
        if option == 2:
            self.processSignal.emit(True)


class ModeToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)


class SettingsToolBar(QToolBar):

    settingsSignal = pyqtSignal()
    helpSignal = pyqtSignal()
    exportSignal = pyqtSignal()
    dockSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionGroup = SettingsActionGroup(self)
        self.addActions(self.actionGroup.actions())

        self.actionGroup.settingsSignal.connect(self.settingsSignal)
        self.actionGroup.helpSignal.connect(self.helpSignal)
        self.actionGroup.exportSignal.connect(self.exportSignal)
        self.actionGroup.dockSignal.connect(self.dockSignal)


class GenerationToolBar(QToolBar):

    switchSignal = pyqtSignal(ScreenMode)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionGroup = GenerateModeActionGroup(self)
        self.addActions(self.actionGroup.actions())
        self.actionGroup.switchSignal.connect(self.switchSignal)

    @pyqtSlot(bool)
    def enableSurvey(self, enable):
        self.actionGroup.surveyAction.setEnabled(enable)
