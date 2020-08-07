import sys
from enum import IntEnum

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from .SurveyTableView import SurveyTableView
from ..AppResources import SurveyTableResources as R

# TODO maybe move to AppEnums
class Column(IntEnum):
    SURVEY_DATETIME = 0
    RECORDER_ID = 1
    RECORDER_DURATION = 2
    RECORDING_LOCATION = 3
    FILE = 4
    URL = 5
    NOTE = 6

class SurveyTableWidget(SurveyTableView):

    combineSignal = pyqtSignal()
    addSurveySignal = pyqtSignal()
    editSurveySignal = pyqtSignal()
    loadSurveyAudioSignal = pyqtSignal()
    selectionChangeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # init table model TODO: make vars private
        self.surveyTableModel = QSqlRelationalTableModel()
        self.surveyTableModel.setTable(R.tableName)
        self.surveyTableModel.setEditStrategy(QSqlTableModel.OnRowChange)
        self.surveyTableModel.select()
        self.surveyTableView.setModel(self.surveyTableModel)
        self.surveyTableSelectionModel = self.surveyTableView.selectionModel()
        self.surveyTableSelectionModel.selectionChanged.connect(self.onSurveySelectionChange)

        self.surveyTableView.horizontalHeader().sortIndicatorChanged.connect(self.onSurveySelectionChange) # TODO

        # connect buttons
        self.addSurveyButton.clicked.connect(self.addSurveySignal.emit)
        self.editSurveyButton.clicked.connect(self.editSurveySignal.emit)
        self.deleteSurveyButton.clicked.connect(self.deleteSurveyButtonAction)
        self.loadAudioButton.clicked.connect(self.loadSurveyAudioSignal.emit)
        self.combineButton.clicked.connect(self.combineSignal.emit)

    # info to populate AddSurveyDialog
    def getDialogArgs(self):
        recorderIds = []
        query = QSqlQuery("SELECT DISTINCT recorder_id FROM survey")

        while query.next():
            print(query.value(0))

        kwargs = {"recorderIds" : recorderIds}
        return kwargs

    def select(self, index):
        self.surveyTableView.selectRow(index)

    def sortByKey(self):
        self.surveyTableView.sortByColumn(0, Qt.DescendingOrder)

    # TODO: keep selection after sort
    def onSort(self):
        pass

    def getSelectedRows(self):
        return self.surveyTableSelectionModel.selectedRows()

    def onPlaylistMediaChange(self, hasMedia):
        self.addSurveyButton.setEnabled(hasMedia)
        self.selectionChangeSignal.emit()

    def getSelectedData(self, row=0, column=Column.SURVEY_DATETIME):
        key = self.getSelectedRows()[row]
        return self.surveyTableModel.data(key.sibling(key.row(), column.value))

    def getDataFromKey(self, keyIndex, column=Column.SURVEY_DATETIME):
        return self.surveyTableModel.data(keyIndex.sibling(keyIndex.row(), column.value))

    def getSelectedKeys(self):
        list = []
        for row in self.getSelectedRows():
            list.append(str(self.surveyTableModel.data(row)))
        return list

    def singlePathSelected(self):
        if len(self.getSelectedRows()) > 0:
            firstPath = self.getDataFromKey(self.getSelectedRows()[0], Column.FILE)
            for row in self.getSelectedRows(): # self.getSelectedRows():
                if self.getDataFromKey(row, Column.FILE) != firstPath:
                    return None
            return firstPath
        return None

    def addRecord(self, record):
        sqlRecord = record.getQSQLRecord(self.surveyTableModel.record())
        self.surveyTableModel.insertRecord(0, sqlRecord)
        self.sortByKey()
        self.select(0)
        QApplication.processEvents()  # allow for selection highlight

    def editRecord(self, record):
        index = self.getSelectedRows()[0]
        record.editData(model=self.surveyTableModel, index=index)
        QApplication.processEvents()  # TODO maybe remove

    @pyqtSlot()
    def deleteSurveyButtonAction(self):
        for row in self.getSelectedRows():
            self.surveyTableModel.removeRow(row.row())
        self.surveyTableSelectionModel.clearSelection()
        self.surveyTableModel.select()
        QApplication.processEvents()

    @pyqtSlot()
    def onSurveySelectionChange(self):
        # enable/disable buttons then signal MainWindow
        selectionCount = len(self.getSelectedRows())
        self.deleteSurveyButton.setEnabled(selectionCount > 0)
        self.loadAudioButton.setEnabled(selectionCount > 0)
        self.editSurveyButton.setEnabled(selectionCount == 1)
        self.combineButton.setEnabled(selectionCount > 1 and self.singlePathSelected() is not None)
        self.selectionChangeSignal.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SurveyTableWidget()
    widget.show()
    sys.exit(app.exec_())