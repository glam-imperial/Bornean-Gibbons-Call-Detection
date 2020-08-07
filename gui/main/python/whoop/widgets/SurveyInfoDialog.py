import re
import abc

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QDateTimeEdit, QDialogButtonBox, QComboBox
from PyQt5.QtCore import QDateTime, pyqtSignal, pyqtSlot

from ..Records import SurveyRecord
from ..AppResources import SurveyTableResources as R

from .SurveyTableWidget import Column

# todo switch to kwargs
class SurveyInfoDialog(QDialog):

    audioIndexSignal = pyqtSignal(str)

    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.surveyTableModel = parent.surveyTableModel

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.kwargs = kwargs

        # form
        self.surveyDatetimeField = QDateTimeEdit()
        self.recorderIDField = QComboBox()
        self.recordingDatetimeField = QDateTimeEdit()
        self.recordingDurationField = QLabel()
        self.audioField = QComboBox()
        self.urlField = QLineEdit()
        self.noteField = QLineEdit()
        self.initForm()

        # buttons
        self.initButtons()

    # TODO make a property?
    @pyqtSlot(int)
    def setDuration(self, duration):
        # self.audioDuration = int
        self.recordingDurationField.setText(str(duration))

    def initForm(self):
        # labels
        formLayout = QFormLayout()
        surveyDatetimeLabel = QLabel("Survey Datetime")
        recorderIDLabel = QLabel("Recorder ID")
        recordingDatetimeLabel = QLabel("Recording Datetime")
        recordingDurationLabel = QLabel("Recording Duration")
        audioLabel = QLabel("Audio File Path")
        urlLabel = QLabel("Audio URL")
        noteLabel = QLabel("Notes")

        # datetime format
        self.surveyDatetimeField.setDisplayFormat(R.datetimeFormat)
        self.recordingDatetimeField.setDisplayFormat(R.datetimeFormat)
        self.surveyDatetimeField.setEnabled(False)  # primary key should not be edited

        # combo boxes
        self.recorderIDField.setEditable(True)
        self.audioField.setEditable(False)
        self.recorderIDField.addItems(self.kwargs["recorderIds"])
        self.audioField.addItems(self.kwargs["audioFiles"])
        self.audioField.currentTextChanged.connect(self.onFileIndexChange)

        # populate fields
        self.setInitialValues(**self.kwargs)

        # assemble form
        formLayout.addRow(surveyDatetimeLabel, self.surveyDatetimeField)
        formLayout.addRow(recorderIDLabel, self.recorderIDField)
        formLayout.addRow(recordingDatetimeLabel, self.recordingDatetimeField)
        formLayout.addRow(recordingDurationLabel, self.recordingDurationField)
        formLayout.addRow(audioLabel, self.audioField)
        formLayout.addRow(urlLabel, self.urlField)
        formLayout.addRow(noteLabel, self.noteField)
        self.mainLayout.addLayout(formLayout)

    @pyqtSlot(str)
    def onFileIndexChange(self, file):
        print(file)
        # newDuration = self.updateDuration(file)
        # self.recordingDurationField.setText(str(newDuration))
        self.audioIndexSignal.emit(file)
        # self.updateDuration(file)
        QApplication.processEvents()
        self.repaint()

    @abc.abstractmethod
    def setInitialValues(self, **kwargs):
        pass

    def initButtons(self):
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.mainLayout.addWidget(buttonBox)

    # helper for loadForm()
    def getQDateTime(self, string):
        idStr = re.split("[:\s.\-]", string)
        idStr = list(map(int, idStr))
        if len(idStr) == 6:
            id = QDateTime(int(idStr[0]), idStr[1], idStr[2], idStr[3], idStr[4], idStr[5])
        elif len(idStr) == 7:
            id = QDateTime(int(idStr[0]), idStr[1], idStr[2], idStr[3], idStr[4], idStr[5], idStr[6])
        return id

    def getDateTime(self):
        return self.surveyDatetimeField.dateTime()

    def createRecord(self):
        return SurveyRecord(surveyDatetime=self.surveyDatetimeField.dateTime(),
                            recorderID=self.recorderIDField.currentText(),
                            recordingDatetime=self.recordingDatetimeField.dateTime(),
                            recordingDuration=self.recordingDurationField.text(),
                            audioFilePath=self.audioField.currentText(),
                            audioURL=self.urlField.text(),
                            note=self.noteField.text())

class EditSurveyDialog(SurveyInfoDialog):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def setInitialValues(self, **kwargs):
        # firstRow = self.parent().getSelectedRows()[0]

        field0 = self.getQDateTime(self.parent().getSelectedData(0, Column(0)))
        field1 = self.parent().getSelectedData(0, Column(1))
        field2 = self.getQDateTime(self.parent().getSelectedData(0, Column(2)))
        field3 = self.parent().getSelectedData(0, Column(3))
        field4 = self.parent().getSelectedData(0, Column(4))
        field5 = self.parent().getSelectedData(0, Column(5))
        field6 = self.parent().getSelectedData(0, Column(6))

        # field0 = self.getQDateTime(self.parent().getSelectedData(0, 0))
        # field1 = self.parent().getSelectedData(0, 1)
        # field2 = self.getQDateTime(self.parent().getSelectedData(0, 2))
        # field3 = self.parent().getSelectedData(0, 3)
        # field4 = self.parent().getSelectedData(0, 4)
        # field5 = self.parent().getSelectedData(0, 5)
        # field6 = self.parent().getSelectedData(0, 6)

        self.surveyDatetimeField.setDateTime(field0)
        self.recorderIDField.setCurrentIndex(self.recorderIDField.findText(field1))
        self.recordingDatetimeField.setDateTime(field2)
        self.recordingDurationField.setText(field3)

        if self.audioField.findText(field4) > -1: # TODO magic number
            print(self.audioField.findText(field4))
            self.audioField.setCurrentIndex(self.audioField.findText(field4))
        else:
            print(self.audioField.findText(field4))
            self.audioField.addItem(field4)
            self.audioField.setCurrentIndex(self.audioField.findText(field4))

        self.urlField.setText(field5)
        self.noteField.setText(field6)

class CombineSurveyDialog(SurveyInfoDialog):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def setInitialValues(self, **kwargs):
        self.surveyDatetimeField.setDateTime(QDateTime.currentDateTime())

        field1 = self.parent().getSelectedData(0, Column(1))
        field2 = self.getQDateTime(self.parent().getSelectedData(0, Column(2)))
        field3 = self.parent().getSelectedData(0, Column(3))
        field4 = self.parent().getSelectedData(0, Column(4))
        field5 = self.parent().getSelectedData(0, Column(5))

        self.recorderIDField.setCurrentIndex(self.recorderIDField.findText(field1))
        self.recordingDatetimeField.setDateTime(field2)
        self.recordingDurationField.setText(field3)

        if self.audioField.findText(field4) > -1: # TODO magic number
            print(self.audioField.findText(field4))
            self.audioField.setCurrentIndex(self.audioField.findText(field4))
        else:
            print(self.audioField.findText(field4))
            self.audioField.addItem(field4)
            self.audioField.setCurrentIndex(self.audioField.findText(field4))

        self.urlField.setText(field5)

        if kwargs["audioSelected"]:
            self.recordingDurationField.setText(kwargs["audioDuration"])
            self.audioField.setCurrentIndex(self.audioField.findText(kwargs["audioFile"]))

class AddSurveyDialog(SurveyInfoDialog):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def setInitialValues(self, **kwargs):
        self.surveyDatetimeField.setDateTime(QDateTime.currentDateTime())
        if kwargs["audioSelected"]:
            self.recordingDurationField.setText(kwargs["audioDuration"])
            self.audioField.setCurrentIndex(self.audioField.findText(kwargs["audioFile"]))
        # TODO: add drop down etc