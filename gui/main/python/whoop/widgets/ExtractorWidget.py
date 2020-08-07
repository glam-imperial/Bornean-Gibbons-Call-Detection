import os
from enum import Enum, unique

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from .ExtractorView import ExtractorView

# TODO maybe move to AppEnums
@unique
class Type(Enum):
    CONT = (True, False, False)
    POS = (False, True, False)
    NEG = (False, False, True)
    BOTH = (False, True, True)
    INVALID = (False, False, False)

class ExtractorWidget(ExtractorView):

    runSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.direcDialog = QFileDialog(self)
        self.direcDialog.setFileMode(QFileDialog.Directory)
        self.connectDialog()
        self.runButton.clicked.connect(self.runAction)

    def showDialog(self, field):
        if self.direcDialog.exec_():
            dir = self.direcDialog.selectedFiles()[0]
            field.setText(dir)

    def connectDialog(self):
        self.addPosButton.clicked.connect(lambda ignore, field=self.posField : self.showDialog(field))
        self.addNegButton.clicked.connect(lambda ignore, field=self.negField : self.showDialog(field))
        self.addValButton.clicked.connect(lambda ignore, field=self.valField : self.showDialog(field))

    def runAction(self):
        if self.getType() == Type.INVALID:
            self.showTypeError()
            return

        isValid, errorDirec = self.validOutputDirec()
        if isValid:
            self.runSignal.emit()
        else:
            self.showDirecError(errorDirec)

    def showTypeError(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText("Invalid Extraction Type")
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def showDirecError(self, errorDirec):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText("Output Directory Not Found")
        message.setInformativeText("Directory: " + errorDirec)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def getStartEnd(self):
        if self.fullLengthCheck.isChecked():
            return 0, None
        return self.startBox.value(), self.endBox.value()

    def getSplitterArgs(self):
        clip_len = self.lengthBox.value()
        shift_len = self.shiftBox.value()
        alpha = self.alphaBox.value()
        beta = self.betaBox.value()
        gamma = self.gammaBox.value()
        delta = self.deltaBox.value()
        return (clip_len, shift_len, alpha, beta, gamma, delta)
    
    def getType(self):
        if self.continuousCheck.isChecked():
            return Type.CONT
        return Type((False, self.posCheck.isChecked(), self.negCheck.isChecked()))

    def validOutputDirec(self):
        extractionType = self.getType().value
        outputDirec = self.getOutputDirec()
        for index in range (0, 2):
            if extractionType[index]:
                if os.path.isdir(outputDirec[index]) == False:
                    return False, outputDirec[index]
        return True, None

    def getOutputDirec(self):
        type = self.getType()
        if type == Type.INVALID:
            return (None, None, None)
        if type == Type.CONT:
            return (self.valField.text(), None, None)
        if type == Type.BOTH:
            return (None, self.posField.text(), self.negField.text())
        if type == Type.POS:
            return (None, self.posField.text(), None)
        if type == Type.NEG:
            return (None, None, self.negField.text())

    def toFilter(self):
        return not self.extractAllCheck.isChecked()

    def hasLabelsSelected(self):
        return len(self.labelList.selectedItems()) > 0

    def getLabelFilter(self):
        if not self.hasLabelsSelected():
            return "label = 999" # TODO backup only - have error dialog

        filter = "label = \"" + self.labelList.selectedItems()[0].text() + "\""

        for i in range (1, len(self.labelList.selectedItems())):
            label = self.labelList.selectedItems()[i].text()
            filter = filter + " OR label = \"" + label + "\""

        print(filter) # TODO remove testing only
        return filter

    def runMode(self, isRunning):
        self.runButton.setDisabled(isRunning)