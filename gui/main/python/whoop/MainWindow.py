"""
Main application window, displays set of dock widgets, manages inter-widget processes and data sharing.

Author: Alexander Shiarella
"""

import os
import sys
import shutil
import sqlite3
from pathlib import Path
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

from .AppEnums import AudioSource, ScreenMode
from .AppResources import StampTableResources, GlobalResources, AudioResources, SQLResources
from .AppUtils import ErrorUtils
from .Records import StampRecord

from .widgets.MediaPlayerWidget import MediaPlayerWidget
from .widgets.SurveyTableWidget import SurveyTableWidget
from .widgets.SurveyTableWidget import Column as SurveyTableColumn
from .widgets.StampTableWidget import StampTableWidget
from .widgets.ExtractorWidget import ExtractorWidget
from .widgets.ProcessWidget import ProcessWidget
from .widgets.ValidateWidget import ValidateWidget
from .widgets.ExtractorWidget import Type as ExtractionType
from .widgets.SurveyInfoDialog import AddSurveyDialog, EditSurveyDialog, CombineSurveyDialog
from .widgets.ToolBars import ViewToolBar, ModeToolBar, GenerationToolBar, SettingsToolBar
from .widgets.VisualizerWidget import VisualizerWidget
from whoop.widgets.StatusBar import StatusBarWidget

from .processing.AudioSplitter import AudioSplitter
from .processing.ProcessWorker import ProcessWorker
from .processing.ModelWorker import ModelWorker
from .processing.ExtractionWorker import ExtractionWorker

from .ScreenSettings import MainScreenSetting, SeparateScreenSetting

from keras import Sequential


class MainWindow(QMainWindow):

    enableSurveyStart = pyqtSignal(bool)

    def __init__(self, databasePath, logWidget):
        super().__init__()

        # Log
        self.logWidget = logWidget

        # Style
        # self.setStyleSheet(open('Styles.css').read()) # Comment out if not using custom CSS.

        # Database
        self.qDatabaseConnection = None # To allow checking for existing connection to close.
        self.qDatabaseConnection = self.__openDatabase(databasePath)
        print(QSqlDatabase.database().connectionName())

        # General
        self.setWindowTitle("whoop")
        self.errorLabel = QLabel()  # TODO remove
        self.statusBarWidget = StatusBarWidget(self)
        self.statusBarWidget.showTextMessage("Status: Connected to " + databasePath)

        # Toolbars
        self.viewToolBar = ViewToolBar(self)
        self.modeToolBar = ModeToolBar(self) # TODO abstract?
        self.generationToolBar = GenerationToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.viewToolBar)
        self.viewToolBar.setVisible(False) # TODO depricated for now - add for training screen maybe
        self.settingsToolBar = SettingsToolBar()
        self.addToolBar(Qt.RightToolBarArea, self.settingsToolBar)

        # Widgets
        self.playerWidget = MediaPlayerWidget()
        self.surveyWidget = SurveyTableWidget()
        self.stampWidget = StampTableWidget()
        self.extractorWidget = ExtractorWidget()
        self.processWidget = ProcessWidget()
        self.validateWidget = ValidateWidget()
        self.visualizerWidget = VisualizerWidget()
        # self.logWidget = logWidget

        # Docks
        self.playerDock = QDockWidget("Audio", self)
        self.surveyDock = QDockWidget("Surveys", self)
        self.stampDock = QDockWidget("Annotation", self)
        self.extractorDock = QDockWidget("Extraction", self)
        self.processDock = QDockWidget("Processing", self)
        self.validateDock = QDockWidget("Validation", self)
        self.visualizerDock = QDockWidget("Visualization", self)
        self.logDock = QDockWidget("Log", self)
        self.playerDock.setWidget(self.playerWidget)
        self.surveyDock.setWidget(self.surveyWidget)
        self.stampDock.setWidget(self.stampWidget)
        self.extractorDock.setWidget(self.extractorWidget)
        self.processDock.setWidget(self.processWidget)
        self.validateDock.setWidget(self.validateWidget)
        self.visualizerDock.setWidget(self.visualizerWidget)
        self.logDock.setWidget(self.logWidget)

        # Screens
        self.generationScreen = MainScreenSetting(self)
        # TODO depricated - not using separate screens anymore (just showing docks) since side toolbar can be shared
        self.processScreen = SeparateScreenSetting(self)

        # Model/Processing
        self.kerasModel = None
        self.worker = ProcessWorker.null()
        self.modelWorker = ModelWorker.null()
        self.killProcessingEvent = threading.Event()

        # extraction
        self.extractionWorker = ExtractionWorker.null()

        self.__createInitialView()

        # signals
        self.__connectSignals()

    # TODO user confirmation? Save session?
    def closeEvent(self, event):
        self.__setKillFlag(True)

        try:
            # TODO something less hacky
            self.worker.join()
            self.extractionWorker.join()
            self.modelWorker.join()
        except RuntimeError:
            pass # The thread has not been started.

        self.__closeDatabase()
        super().closeEvent(event)

    # TODO Possible improvement: Reset table models so that DB can be switched from within app.
    def __openDatabase(self, path):
        self.logWidget.logItem("Opening database connection to " + path)
        try:
            if self.qDatabaseConnection:
                self.__closeDatabase()
            qDatabaseConnection = QSqlDatabase.addDatabase(SQLResources.dbType)
            qDatabaseConnection.setDatabaseName(path)
            if not qDatabaseConnection.open():
                ErrorUtils.showErrorDialog(text="Could not create database connection.",
                                           info="Application exiting.")
                sys.exit(1)  # TODO log error

        except sqlite3.Error as e:
            ErrorUtils.showErrorDialog(text="sqlite3 error when connecting to database. Exiting.", info=str(e))
            sys.exit(1)  # TODO log error

        except Exception as e:
            ErrorUtils.showErrorDialog(text="Uncaught exception when connecting to database. Exiting.", info=str(e))
            sys.exit(1)  # TODO log error

        self.logWidget.logItem("Opened database connection to " + path)
        return qDatabaseConnection

    # TODO reset table models so that DB can be switched from within app
    def __closeDatabase(self):
        self.logWidget.logItem("Closing database connection")
        QSqlDatabase.database().connectionName()
        self.qDatabaseConnection.close()
        del self.qDatabaseConnection
        QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

    def __connectSignals(self):
        # survey widget
        self.surveyWidget.addSurveySignal.connect(self.showAddSurveyDialog)
        self.surveyWidget.editSurveySignal.connect(self.showEditSurveyDialog)
        self.surveyWidget.loadSurveyAudioSignal.connect(self.loadSurveyAudio)
        self.surveyWidget.selectionChangeSignal.connect(self.onSurveySelectionChange)
        self.surveyWidget.combineSignal.connect(self.showCombineSurveyDialog)

        # player widget
        # self.playerWidget.mediaChangedSignal.connect(self.surveyWidget.onPlaylistMediaChange) # TODO removed for performance
        self.playerWidget.playlistSelectionChangedSignal.connect(self.onPlaylistSelectionChange)

        # stamp widget
        self.stampWidget.addStampSignal.connect(lambda key : self.supplyStamp(key))

        # extraction widget
        self.extractorWidget.runSignal.connect(self.__runExtraction)

        # process widget
        self.processWidget.runSignal.connect(self.__runProcessing)
        self.processWidget.loadSignal.connect(self.__loadModel)
        self.processWidget.cancelSignal.connect(lambda ignore, flagUp=True : self.__setKillFlag(flagUp=flagUp))

        # validate widget
        self.validateWidget.moveSignal.connect(self.__moveFile)

        # generation toolbar
        self.enableSurveyStart.connect(self.generationToolBar.enableSurvey)
        self.enableSurveyStart.connect(self.stampWidget.enableStamps)
        self.generationToolBar.switchSignal.connect(self.generationScreen.setMode)

        # view toolbar
        # TODO depricated - not using separate screens anymore (just showing docks) since side toolbar can be shared
        # self.viewToolBar.switchSignal.connect(self.onViewSwitch)

    @pyqtSlot(bool)
    def __setKillFlag(self, flagUp):
        if flagUp:
            self.killProcessingEvent.set()
        else:
            self.worker.join()
            self.killProcessingEvent.clear()

    @pyqtSlot(str, bool)
    def __moveFile(self, direc, toRemove):
        audioFile = self.playerWidget.getCurrentMediaUrl()
        if os.path.exists(audioFile):
            newPath = os.path.join(direc, os.path.basename(audioFile))
            try:
                if toRemove:
                    shutil.move(audioFile, newPath)
                    self.playerWidget.removeButtonAction()
                    self.logWidget.logItem("Moved " + audioFile + " to " + newPath)
                else:
                    shutil.copy(audioFile, newPath)
                    self.logWidget.logItem("Copied " + audioFile + " to " + newPath)
            except shutil.SameFileError:
                # TODO show notification maybe option to overwrite
                self.logWidget.logItem(" ERROR - destination " + newPath + " already exists")
                ErrorUtils.showErrorDialog(text=("Did not move " + audioFile), info=(newPath + " already exists."))
        else:
            self.logWidget.logItem("ERROR - Could not find " + audioFile)
            ErrorUtils.showErrorDialog(text="File not found", info=audioFile)

    @pyqtSlot(str)
    def __loadModel(self, modelFile):
        self.modelWorker = ModelWorker(modelFile) # TODO move delclaration to constructor?
        self.modelWorker.modelSignal.connect(self.__modelLoaded)
        self.modelWorker.errorSignal.connect(self.__modelLoadError)
        self.modelWorker.start()

    @pyqtSlot(Sequential, str)
    def __modelLoaded(self, model, modelFile):
        self.kerasModel = model
        self.processWidget.setModelLabel(modelFile)
        self.processWidget.setDisabled(False)

    @pyqtSlot(str)
    def __modelLoadError(self, error):
        ErrorUtils.showErrorDialog(text="Could not load model.", info=error)
        self.processWidget.setDisabled(False)

    def __runProcessing(self):
        self.logWidget.logItem("Running processing")

        # temp disable changes
        self.processWidget.setDisabled(True)
        self.playerWidget.setDisabled(True)

        # get settings from ProcessWidget
        setting = self.processWidget.getSetting()

        # create tuple of audio file paths
        audioTup, errorMessage = self.__getAudioForProcessing(setting)
        if len(audioTup) < 1:
            self.logWidget.logItem("ERROR - no audio for processing.")
            ErrorUtils.showErrorDialog(text="No audio selected for processing", info=errorMessage)

        else:
            self.processWidget.runMode(True)
            self.worker = ProcessWorker(self, setting, audioTup, self.kerasModel, self.killProcessingEvent)
            self.worker.runModeSignal.connect(self.processWidget.runMode)
            self.worker.statusSignal.connect(self.logWidget.logItem)
            self.worker.runModeSignal.connect(self.__setKillFlag) # False if not running

            # p = multiprocessing.Process(target=self.__runProcess, args=(self.worker,))
            self.worker.start()

        self.processWidget.setDisabled(False)
        self.playerWidget.setDisabled(False)

    def __getAudioForProcessing(self, setting):
        audioList = []
        errorMessage = ""
        
        if setting.getAudioSource() == AudioSource.SELECTED:
            audioList.append(self.playerWidget.getCurrentMediaUrl())
            self.logWidget.logItem("Loading selected audio: " + str(self.playerWidget.getCurrentMediaUrl()))
            
        elif setting.getAudioSource() == AudioSource.ALL:
            audioList = self.playerWidget.getAllMedia()
            self.logWidget.logItem("Loading all audio in Audio widget")

        elif setting.getAudioSource() == AudioSource.DIREC:
            direc = setting.getInputDirec()
            if os.path.isdir(direc):
                self.logWidget.logItem("Loading audio from " + direc)
                # get all allowed files in directory
                for filename in os.listdir(direc):
                    if filename.endswith(AudioResources.allowedExt):
                        audioList.append(os.path.join(direc, filename))
            else:
                self.logWidget.logItem("ERROR - not a valid directory " + direc)
                errorMessage = "Not a valid directory: " + direc
                # TODO launch error dialog and return (not a valid directory)

        else:
            print("Error: no source selected") # TODO error dialog and enablement
            self.logWidget.logItem("ERROR - no audio source selected.")
            errorMessage = "No audio source selected."

        return tuple(audioList), errorMessage

    # TODO depricated - not using separate screens anymore (just showing docks) since side toolbar can be shared
    # def __onViewSwitch(self, option):
    #     if option == 0:
    #         print("option 0")
    #         self.__loadGenerateView()
    #     if option == 1:
    #         print("option 1")
    #         self.loadProcessView()
    #     if option == 2:
    #         print("option 2")

    def __loadGenerateView(self):
        self.generationScreen.showScreen()

    def loadProcessView(self):
        self.processScreen.showScreen()

    def __createInitialView(self):
        self.__loadGenerateView()
        self.generationScreen.setMode(ScreenMode.PREPARE)

    def __runExtraction(self):
        print("run extraction")
        if self.checkSurveySelection():

            self.extractorWidget.runMode(True)
            # create a splitter object with values from forms
            args = self.extractorWidget.getSplitterArgs()
            splitter = AudioSplitter(*args)
            type = self.extractorWidget.getType()

            # get audio start and end
            audioStart, audioEnd = self.extractorWidget.getStartEnd()

            # for each survey selected, get all of timestamps
            # rows = self.surveyWidget.getSelectedRows()
            #
            # for row in rows:
            #     audioFile = self.surveyWidget.getDataFromKey(row, SurveyTableColumn.FILE)
            #
            #     if type == ExtractionType.CONT:
            #         splitter.split(audioFile, self.extractorWidget.getOutputDirec()[0], start, end)
            #
            #     else:
            #         stampList = self.queryStamps(row)
            #         if type == ExtractionType.POS or type == ExtractionType.BOTH:
            #             splitter.extract(stampList, ExtractionType.POS, audioFile, self.extractorWidget.getOutputDirec()[1], start, end)
            #         if type == ExtractionType.NEG or type == ExtractionType.BOTH:
            #             splitter.extract(stampList, ExtractionType.NEG, audioFile, self.extractorWidget.getOutputDirec()[2], start, end)
            rows = self.surveyWidget.getSelectedRows()

            if type == ExtractionType.CONT:
                audioList = []
                for row in rows:
                    audioFile = self.surveyWidget.getDataFromKey(row, SurveyTableColumn.FILE)
                    audioList.append(audioFile)

                self.extractionWorker = ExtractionWorker(self,
                                                         # splitter=splitter,
                                                         splitterArgs = args,
                                                         audioInfo=audioList,
                                                         type=type,
                                                         audioStart=audioStart,
                                                         audioEnd=audioEnd,
                                                         outputDirec=self.extractorWidget.getOutputDirec()[0])
                # todo disable button

            else:
                audioDict = {}
                for row in rows:
                    audioFile = self.surveyWidget.getDataFromKey(row, SurveyTableColumn.FILE)
                    audioDict[audioFile] = self.queryStamps(row)

                self.extractionWorker = ExtractionWorker(self,
                                                         splitterArgs=args,
                                                         # splitter=splitter,
                                                         audioInfo=audioDict,
                                                         type=type,
                                                         audioStart=audioStart,
                                                         audioEnd=audioEnd,
                                                         outputDirec=[self.extractorWidget.getOutputDirec()[1], self.extractorWidget.getOutputDirec()[2]])

            self.worker.runModeSignal.connect(self.extractorWidget.runMode)
            self.extractionWorker.statusSignal.connect(self.logWidget.logItem)
            self.extractionWorker.start()
                # todo disable button

            # audioList = []
            # audioDict = {}
            # for row in rows:
            #     audioFile = self.surveyWidget.getDataFromKey(row, SurveyTableColumn.FILE)
            #
            #     if type == ExtractionType.CONT:
            #         audio
            #         splitter.split(audioFile, self.extractorWidget.getOutputDirec()[0], start, end)
            #
            #     else:
            #         stampList = self.queryStamps(row)
            #         if type == ExtractionType.POS or type == ExtractionType.BOTH:
            #             splitter.extract(stampList, ExtractionType.POS, audioFile,
            #                              self.extractorWidget.getOutputDirec()[1], start, end)
            #         if type == ExtractionType.NEG or type == ExtractionType.BOTH:
            #             splitter.extract(stampList, ExtractionType.NEG, audioFile,
            #                              self.extractorWidget.getOutputDirec()[2], start, end)


    def runQuery(self, queryStr, lastField, firstField = 0):
        query = QSqlQuery(queryStr)
        if query.exec_() == False:
            print(query.lastError().text()) # TODO
        result = []
        while query.next():
            rowResult = []
            for col in range(firstField, lastField):
                print(query.value(col)) # TODO remove
                rowResult.append(query.value(col))
            result.append(rowResult)
        return result

    def queryColumn(self, queryStr, col=0):
        query = QSqlQuery(queryStr)
        if query.exec_() == False:
            print(query.lastError().text()) # TODO
        result = []
        while query.next():
            result.append(query.value(col))
        return result

    def queryStamps(self, surveyRow):
        surveyID = self.surveyWidget.getDataFromKey(surveyRow, SurveyTableColumn.SURVEY_DATETIME)
        if self.extractorWidget.toFilter():
            queryStr = "SELECT miliseconds FROM " \
                       + StampTableResources.tableName \
                       + " WHERE survey_datetime = \"" \
                       + surveyID + "\"" \
                       + " AND (" + self.extractorWidget.getLabelFilter() + ")" \
                       + " ORDER BY miliseconds ASC"
        else:
            queryStr = "SELECT miliseconds FROM " \
                       + StampTableResources.tableName \
                       + " WHERE survey_datetime = \"" \
                       + surveyID \
                       + "\" ORDER BY miliseconds ASC"
        stamps = self.queryColumn(queryStr)
        return stamps

    def checkSurveySelection(self):
        # TODO maybe remove (redundant)
        rows = self.surveyWidget.getSelectedRows()
        if len(rows) < 1:
            print("Error: No survey selected.")  # TODO
            self.errorMessage("No Survey Selected")
            return False

        for row in rows:
            file = self.surveyWidget.getDataFromKey(row, SurveyTableColumn.FILE)
            if self.playerWidget.fileIndex(file) < 0:
                print("Error: Audio file is not loaded for all selected surveys.") # TODO
                self.showNotLoadedError(file)
                return False
        return True

    def showNotLoadedError(self, errorFile):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText("Load Audio Into Player")
        message.setInformativeText("File: " + errorFile)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def errorMessage(self, text):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(text)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    # todo maybe local
    @pyqtSlot()
    def combineSurveys(self):
        rows = self.surveyWidget.getSelectedRows()
        print(len(rows))
        print(rows)



    @pyqtSlot()
    def supplyStamp(self, key):
        stamp = self.playerWidget.getMiliseconds()
        self.stampWidget.addStamp(stamp, key)

    def showCombineSurveyDialog(self):
        print(self.playerWidget.getDialogArgs())
        dialog = CombineSurveyDialog(self.surveyWidget, **self.playerWidget.getDialogArgs(),
                                 **self.surveyWidget.getDialogArgs())
        dialog.audioIndexSignal.connect(self.playerWidget.changeSelection)
        self.playerWidget.durationChangeSignal.connect(dialog.setDuration)
        if dialog.exec_():
            filter = self.stampWidget.createFilter(self.surveyWidget.getSelectedKeys())
            queryStr = "SELECT * FROM ANNOTATION WHERE " + filter
            result = self.runQuery(queryStr, 5)
            print(result)

            self.surveyWidget.addRecord(dialog.createRecord())
            for row in result:
                print(row[0])
                print(dialog.getDateTime())
                newRecord = StampRecord(miliseconds=row[0],
                                        surveyDatetime=dialog.getDateTime().toString(GlobalResources.datetimeFormat),
                                        label=row[3],
                                        note=row[4],
                                        creationDatetime=row[2])

                self.stampWidget.addRecord(newRecord)

            self.stampWidget.loadSurveyStamps(self.surveyWidget.getSelectedKeys())

    @pyqtSlot()
    def showAddSurveyDialog(self):
        print(self.playerWidget.getDialogArgs())
        dialog = AddSurveyDialog(self.surveyWidget, **self.playerWidget.getDialogArgs(),
                                 **self.surveyWidget.getDialogArgs())
        dialog.audioIndexSignal.connect(self.playerWidget.changeSelection)
        self.playerWidget.durationChangeSignal.connect(dialog.setDuration)
        if dialog.exec_():
            self.surveyWidget.addRecord(dialog.createRecord())

    @pyqtSlot()
    def showEditSurveyDialog(self):
        dialog = EditSurveyDialog(self.surveyWidget, **self.playerWidget.getDialogArgs(),
                                  **self.surveyWidget.getDialogArgs())
        dialog.audioIndexSignal.connect(self.playerWidget.changeSelection)
        self.playerWidget.durationChangeSignal.connect(dialog.setDuration)
        if dialog.exec_():
            self.surveyWidget.editRecord(dialog.createRecord())
            self.enableSurveyStart.emit(self.canStartSurvey())

    @pyqtSlot()
    def loadSurveyAudio(self):
        # load all not already in playlist
        rows = self.surveyWidget.getSelectedRows()
        for index in rows:
            path = self.surveyWidget.getDataFromKey(index, SurveyTableColumn.FILE)
            if not self.playerWidget.isLoaded(path):
                if self.isValidAudioFile(path):
                    self.playerWidget.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))

        self.onSurveySelectionChange()
        QApplication.processEvents()
        self.repaint()

    @pyqtSlot()
    def onSurveySelectionChange(self):
        print(self.surveyWidget.singlePathSelected())
        self.playerWidget.select(self.surveyWidget.singlePathSelected())

        self.enableSurveyStart.emit(self.canStartSurvey())

        if len(self.surveyWidget.getSelectedRows()) > 0:
            self.stampWidget.loadSurveyStamps(self.surveyWidget.getSelectedKeys())
        else:
            self.stampWidget.clearSurveyStamps()

        QApplication.processEvents()  # TODO maybe remove
        self.repaint()  # need for button

    @pyqtSlot()
    def onPlaylistSelectionChange(self):
        self.enableSurveyStart.emit(self.canStartSurvey())
        QApplication.processEvents()  # TODO maybe remove
        self.repaint()  # need for button


    def canStartSurvey(self):
        if len(self.surveyWidget.getSelectedRows()) == 1:
            if self.playerWidget.hasSelection():
                if self.surveyWidget.singlePathSelected() == self.playerWidget.getCurrentMediaUrl():
                    return True
        return False

    def isValidAudioFile(self, path):
        try:
            file = open(path, 'r')
        except FileNotFoundError:
            print("FILE NOT FOUND")
            self.displayError("FILE NOT FOUND")
            return False
        except IOError:
            self.displayError("FILE NOT READABLE")
            return False

        extension = Path(path).suffix
        if extension not in [".m4a", ".mp3", ".aac", ".wav"]:
            self.displayError(extension + " FILE TYPE NOT ACCEPTED")
            return False
        return True

    # TODO change
    def displayError(self, errorString):
        self.errorLabel.setText("ERROR: " + errorString)
