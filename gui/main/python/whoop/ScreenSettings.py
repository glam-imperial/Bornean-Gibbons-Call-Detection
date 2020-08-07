"""
Main application window, displays set of dock widgets, manages inter-widget processes and data sharing.

Author: Alexander Shiarella
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSlot

from .widgets.ToolBars import GenerationToolBar, ModeToolBar
from .AppEnums import ScreenMode


class ScreenSetting:

    def __init__(self, mainWindow):
        self.mode = 0
        self.mainWindow = mainWindow
        self.modeToolBar = ModeToolBar()

        self.dockList = (self.mainWindow.playerDock,
                         self.mainWindow.surveyDock,
                         self.mainWindow.stampDock,
                         self.mainWindow.extractorDock,
                         self.mainWindow.processDock,
                         self.mainWindow.validateDock,
                         self.mainWindow.visualizerDock,
                         self.mainWindow.logDock)

    def clearWidgets(self):
        for dock in self.dockList:
            dock.setFloating(False)
            self.mainWindow.removeDockWidget(dock)

    def setModeToolBar(self):
        pass

    def showScreen(self):
        self.clearWidgets()
        # self.addPlayerWidget()
        self.setModeToolBar() # TODO not used right now - moved to top toolbar only
        self.showDockWidgets()
        self.enable()
        QApplication.processEvents()
        self.mainWindow.repaint()

    def addPlayerWidget(self):
        pass

    def showDockWidgets(self):
        pass

    def connectSignals(self):
        pass

    def setMode(self, option):
        self.mode = option
        self.enable()

    def enable(self):
        pass

class MainScreenSetting(ScreenSetting):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        # self.modeToolBar = GenerationToolBar()

    def setModeToolBar(self):
        self.mainWindow.removeToolBar(self.mainWindow.modeToolBar)
        self.mainWindow.addToolBar(Qt.TopToolBarArea, self.mainWindow.generationToolBar)
        self.mainWindow.generationToolBar.show()

    def addPlayerWidget(self, area=Qt.TopDockWidgetArea):
        self.mainWindow.addDockWidget(area, self.mainWindow.playerDock)
        # self.mainWindow.playerDock.widget().resize(self.mainWindow.playerDock.widget().minimumSizeHint())
        # self.mainWindow.playerDock.widget().setPreferredSize(self.mainWindow.playerDock.widget().minimumSizeHint())  #self.mainWindow.playerDock.widget().minimumSize(
        # self.mainWindow.playerDock.widget().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def showPlayerWidget(self):
        self.mainWindow.playerDock.show()

    def adjustSize(self):
        self.mainWindow.playerDock.widget().resize(self.mainWindow.playerDock.widget().minimumSizeHint())
        self.mainWindow.surveyDock.adjustSize()
        self.mainWindow.stampDock.adjustSize()
        self.mainWindow.extractorDock.adjustSize()
        self.mainWindow.processDock.adjustSize()

    def enable(self):
        if self.mode == ScreenMode.ALL:
            self.toggleAllMode(True)
        if self.mode == ScreenMode.EDIT:
            self.toggleEditMode(True)
        if self.mode == ScreenMode.SURVEY:
            self.toggleSurveyMode(True)
        if self.mode == ScreenMode.EXTRACT:
            self.toggleExtractionMode(True)
        if self.mode == ScreenMode.PROCESS:
            self.toggleProcessMode(True)
        if self.mode == ScreenMode.TRAIN:
            self.toggleTrainMode(True)
        if self.mode == ScreenMode.PREPARE:
            self.togglePrepareMode(True)

    @pyqtSlot(bool)
    def toggleTrainMode(self, toggleOn):
        pass

    @pyqtSlot(bool)
    def togglePrepareMode(self, toggleOn):
        self.mainWindow.validateWidget.onDeselection()

        self.clearWidgets()

        self.mainWindow.setCentralWidget(self.mainWindow.surveyDock)
        # self.mainWindow.surveyDock.setFixedHeight(self.mainWindow.surveyDock.maximumSize())

        # self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.surveyDock)
        self.mainWindow.addDockWidget(Qt.RightDockWidgetArea, self.mainWindow.extractorDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.stampDock)
        self.addPlayerWidget()
        self.mainWindow.removeDockWidget(self.mainWindow.processDock)
        # self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.validateDock)

        self.showPlayerWidget()
        self.mainWindow.extractorDock.show()
        self.mainWindow.surveyDock.show()
        self.mainWindow.stampDock.show()
        # self.mainWindow.processDock.show()
        # self.mainWindow.validateDock.show()
        # self.adjustSize()
        if not self.mainWindow.isFullScreen():
            self.mainWindow.resize(self.mainWindow.minimumWidth() + 300, self.mainWindow.minimumHeight())
            self.mainWindow.playerDock.resize(self.mainWindow.playerDock.minimumWidth(),
                                              self.mainWindow.playerDock.minimumHeight())
            self.mainWindow.stampWidget.resize(5000,
                                             self.mainWindow.stampWidget.maximumHeight())
            self.mainWindow.stampDock.resize(self.mainWindow.stampDock.maximumWidth(),
                                              self.mainWindow.stampDock.maximumHeight())
            # self.mainWindow.resizeDockWidget(waitForObject(self.mainWindow.stampDock), 500, 600)
            #self.mainWindow.resizeDockWidget(self.mainWindow.stampDock, 500, 600)
        self.mainWindow.repaint()

    @pyqtSlot(bool)
    def toggleAllMode(self, toggleOn):
        self.mainWindow.stampWidget.onDeselection()
        self.mainWindow.validateWidget.onDeselection()

        self.clearWidgets()

        # self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.surveyDock)
        self.mainWindow.setCentralWidget(self.mainWindow.surveyDock)
        self.mainWindow.addDockWidget(Qt.RightDockWidgetArea, self.mainWindow.extractorDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.stampDock)
        self.mainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.mainWindow.processDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.validateDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.visualizerDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.logDock)
        self.addPlayerWidget()

        self.showPlayerWidget()
        self.mainWindow.extractorDock.show()
        self.mainWindow.surveyDock.show()
        self.mainWindow.stampDock.show()
        self.mainWindow.processDock.show()
        self.mainWindow.validateDock.show()
        self.mainWindow.visualizerDock.show()
        self.mainWindow.logDock.show()
        # self.adjustSize()
        self.mainWindow.repaint()

    @pyqtSlot(bool)
    def toggleProcessMode(self, toggleOn):
        self.mainWindow.stampWidget.onDeselection()

        self.clearWidgets()

        self.mainWindow.setCentralWidget(self.mainWindow.logDock)
        # self.mainWindow.logDock.setFixedHeight(self.mainWindow.logDock.maximumSize())
        self.mainWindow.addDockWidget(Qt.RightDockWidgetArea, self.mainWindow.processDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.validateDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.visualizerDock)
        self.addPlayerWidget()

        self.mainWindow.processDock.show()
        self.mainWindow.validateDock.show()
        self.mainWindow.visualizerDock.show()
        self.mainWindow.logDock.show()
        self.showPlayerWidget()

        if not self.mainWindow.isFullScreen():
            self.mainWindow.resize(self.mainWindow.minimumWidth() + 300, self.mainWindow.minimumHeight())
        self.mainWindow.repaint()

    @pyqtSlot(bool)
    def toggleSurveyMode(self, toggleOn):
        self.mainWindow.stampWidget.surveyMode(toggleOn)
        # self.mainWindow.surveyWidget.surveyMode(toggleOn)
        # self.mainWindow.playerWidget.surveyMode(toggleOn)

        # self.mainWindow.removeDockWidget(self.mainWindow.processDock)
        # self.mainWindow.removeDockWidget(self.mainWindow.extractorDock)
        # self.mainWindow.removeDockWidget(self.mainWindow.surveyDock)
        self.clearWidgets()
        self.addPlayerWidget()

        self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.stampDock)
        # self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.surveyDock)

        self.showPlayerWidget()
        self.mainWindow.stampDock.show()
        self.mainWindow.repaint()

    @pyqtSlot(bool)
    def toggleEditMode(self, toggleOn):
        self.mainWindow.stampWidget.editMode(toggleOn)
        self.mainWindow.surveyWidget.editMode(toggleOn)
        self.mainWindow.playerWidget.editMode(toggleOn)

        # self.mainWindow.removeDockWidget(self.mainWindow.extractorDock)
        # self.mainWindow.removeDockWidget(self.mainWindow.processDock)
        self.clearWidgets()
        self.addPlayerWidget()

        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.stampDock)
        self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.surveyDock)

        self.showPlayerWidget()
        self.mainWindow.stampDock.show()
        self.mainWindow.surveyDock.show()
        self.mainWindow.repaint()

    @pyqtSlot(bool)
    def toggleExtractionMode(self, toggleOn):
        self.mainWindow.stampWidget.editMode(toggleOn)
        self.mainWindow.surveyWidget.editMode(toggleOn)
        self.mainWindow.playerWidget.editMode(toggleOn)

        # self.mainWindow.removeDockWidget(self.mainWindow.processDock)
        self.clearWidgets()
        self.addPlayerWidget()

        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.stampDock)
        self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.surveyDock)
        self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.mainWindow.extractorDock)

        self.showPlayerWidget()
        self.mainWindow.stampDock.show()
        self.mainWindow.extractorDock.show()
        self.mainWindow.surveyDock.show()
        self.mainWindow.repaint()

class SeparateScreenSetting(ScreenSetting):
    """No longer used - replaced by Widget mode. Left as reminder for training screen."""

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.modeToolBar = GenerationToolBar()

    def setModeToolBar(self):
        self.mainWindow.removeToolBar(self.mainWindow.generationToolBar)

    def addDockWidgets(self):
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.playerDock)
        self.mainWindow.addDockWidget(Qt.TopDockWidgetArea, self.mainWindow.processDock)

    def showDockWidgets(self):
        self.mainWindow.playerDock.show()
        self.mainWindow.processDock.show()

    def connectSignals(self):
        pass