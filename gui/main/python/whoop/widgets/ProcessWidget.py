import os

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal

from .ProcessView import ProcessView

class ProcessWidget(ProcessView):
    
    runSignal = pyqtSignal()
    loadSignal = pyqtSignal(str)
    cancelSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.__enableRun()
        self.runMode(False)
        
        self.runButton.clicked.connect(self.runSignal.emit)
        self.loadButton.clicked.connect(self.__loadButtonAction)
        self.cancelButton.clicked.connect(self.cancelSignal.emit)
        self.__connectDialog()
        self.__connectOutputOptions()

    def setModelLabel(self, modelFile):
        self.modelLoaded.setText(os.path.basename(modelFile))
        self.__enableRun()

    def runMode(self, isRunning):
        self.loadButton.setDisabled(isRunning)
        self.cancelButton.setEnabled(isRunning)

    # TODO move into utility method
    def __connectDialog(self):
        self.addInputButton.clicked.connect(lambda ignore,
                                                   field=self.inputField,
                                                   fileMode=QFileDialog.Directory,
                                                   acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))
        self.addCsvFileButton.clicked.connect(lambda ignore,
                                                     field=self.csvField,
                                                     fileMode=QFileDialog.AnyFile,
                                                     acceptMode=QFileDialog.AcceptSave,
                                                     filter=("*.csv") : self.__showDialog(field, fileMode, acceptMode, filter))
        self.addClipDirecButton.clicked.connect(lambda ignore,
                                                       field=self.clipField,
                                                       fileMode=QFileDialog.Directory,
                                                       acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))
        self.addPosDirecButton.clicked.connect(lambda ignore,
                                                      field=self.posField,
                                                      fileMode=QFileDialog.Directory,
                                                      acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))
        self.addNegDirecButton.clicked.connect(lambda ignore,
                                                      field=self.negField,
                                                      fileMode=QFileDialog.Directory,
                                                      acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))
        self.addNpyDirecButton.clicked.connect(lambda ignore,
                                                      field=self.npyField,
                                                      fileMode=QFileDialog.Directory,
                                                      acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))
        self.chooseModelButton.clicked.connect(lambda ignore,
                                                      field=self.modelFileField,
                                                      fileMode=QFileDialog.AnyFile,
                                                      acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))

    # TODO move into utility method
    def __showDialog(self, field, fileMode, acceptMode, filter=None):
        dialog = QFileDialog(self)
        if filter != None:
            dialog.setNameFilter(filter)
        dialog.setFileMode(fileMode) # QFileDialog.Directory
        dialog.setAcceptMode(acceptMode)
        if dialog.exec_():
            out = dialog.selectedFiles()[0]
            print(out)
            field.setText(out)

    def __enableRun(self):
        canRun = self.modelLoaded.text() != "None" or not self.__needsModel()
        self.runButton.setEnabled(canRun)

    def __enableModelGroup(self):
        self.modelGroup.setEnabled(self.__needsModel())

    def __needsModel(self):
        return self.csvCheck.isChecked() or self.posCheck.isChecked() or self.negCheck.isChecked()

    def __connectOutputOptions(self):
        self.csvCheck.clicked.connect(self.__enableRun)
        self.posCheck.clicked.connect(self.__enableRun)
        self.negCheck.clicked.connect(self.__enableRun)
        self.csvCheck.clicked.connect(self.__enableModelGroup)
        self.posCheck.clicked.connect(self.__enableModelGroup)
        self.negCheck.clicked.connect(self.__enableModelGroup)

    def __loadButtonAction(self):
        self.setDisabled(True)
        modelFile = self.getSetting().model["path"]
        self.loadSignal.emit(modelFile)