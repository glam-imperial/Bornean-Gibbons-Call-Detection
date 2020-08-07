import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableView, QAbstractItemView, QHeaderView, QPushButton
from PyQt5.QtCore import pyqtSlot

from .ShrinkableButton import ShrinkableButton
from .AppWidget import AppWidget
from ..AppResources import SurveyTableResources as R

class SurveyTableView(AppWidget):

    def __init__(self):
        super().__init__()

        # table
        self.surveyTableView = QTableView()
        self.initTableView()

        # buttons
        self.addSurveyButton = ShrinkableButton(R.addSurveyButtonText)
        self.editSurveyButton = ShrinkableButton(R.editSurveyButtonText)
        self.deleteSurveyButton = ShrinkableButton(R.deleteSurveyButtonText)
        self.loadAudioButton = ShrinkableButton(R.loadAudioButtonText)
        self.combineButton = ShrinkableButton(R.combineButtonText)

        self.assemble(self.initButtons())

    def initTableView(self):
        self.surveyTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.surveyTableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.surveyTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.surveyTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.surveyTableView.setSortingEnabled(True)

    def initButtons(self):
        self.addSurveyButton.setDisabled(False) # TODO
        self.editSurveyButton.setDisabled(True)
        self.deleteSurveyButton.setDisabled(True)
        self.loadAudioButton.setDisabled(True)
        self.combineButton.setDisabled(True)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addSurveyButton)
        buttonLayout.addWidget(self.editSurveyButton)
        buttonLayout.addWidget(self.deleteSurveyButton)
        buttonLayout.addWidget(self.loadAudioButton)
        buttonLayout.addWidget(self.combineButton)
        return buttonLayout

    def assemble(self, buttonLayout):
        self.mainLayout.addWidget(self.surveyTableView)
        self.mainLayout.addLayout(buttonLayout)

    @pyqtSlot(bool)
    def surveyMode(self, modeOn):
        self.surveyTableView.setDisabled(modeOn)
        self.addSurveyButton.setDisabled(modeOn)
        self.editSurveyButton.setDisabled(modeOn)
        self.deleteSurveyButton.setDisabled(modeOn)
        self.loadAudioButton.setDisabled(modeOn)
        self.combineButton.setDisabled(modeOn)

    @pyqtSlot(bool)
    def editMode(self, modeOn):
        self.surveyTableView.setEnabled(modeOn)
        self.addSurveyButton.setEnabled(modeOn)
        self.editSurveyButton.setEnabled(modeOn)
        self.deleteSurveyButton.setEnabled(modeOn)
        self.loadAudioButton.setEnabled(modeOn)
        self.combineButton.setEnabled(modeOn)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SurveyTableView()
    widget.show()
    sys.exit(app.exec_())