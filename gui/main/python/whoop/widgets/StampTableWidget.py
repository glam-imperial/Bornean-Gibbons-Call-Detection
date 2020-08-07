import sys
import io
import csv

from PyQt5.QtWidgets import QApplication, QShortcut
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlTableModel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QItemSelection, Qt, QEvent
from PyQt5.QtGui import QKeySequence

from .StampTableView import StampTableView
from ..AppResources import StampTableResources as R
from ..Records import StampRecord

class StampTableWidget(StampTableView):

    addStampSignal = pyqtSignal(str)
    # deleteStampSignal = pyqtSignal()
    surveyModeSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.hasSelection = False # todo
        self.surveyDatetime = None

        # init table model
        self.stampTableModel = QSqlRelationalTableModel()
        self.stampTableModel.setTable(R.tableName)
        self.stampTableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.stampTableModel.setFilter("survey_datetime = None")
        self.stampTableModel.select()
        self.stampTableView.setModel(self.stampTableModel)
        self.stampTableSelectionModel = self.stampTableView.selectionModel()
        self.stampTableSelectionModel.selectionChanged.connect(self.onStampSelectionChange)

        # connect buttons
        self.addStampButton.clicked.connect(lambda ignore, key="-" : self.addStampSignal.emit(key))
        self.deleteStampButton.clicked.connect(self.deleteButtonAction)
        self.hotkeyButton.clicked.connect(self.enableHotkeys)
        # self.recordButton.clicked.connect(self.surveyMode)

        # hotkeys
        self.hotkeys = self.initHotkeys()

        # copy selection to clipboard
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
                event.matches(QKeySequence.Copy)):
            self.copySelection()
            return True
        return super().eventFilter(source, event)

    def copySelection(self):
        selection = self.stampTableView.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

    def initHotkeys(self):
        keyList = []

        shortcut = QShortcut(QKeySequence(Qt.Key_Space, QKeySequence.NativeText), self);
        keyList.append(shortcut)
        shortcut.activated.connect(lambda key="-": self.addStampSignal.emit(key))

        for i in range (0, 10):
            print(i)
            shortcut = QShortcut(QKeySequence(str(i), QKeySequence.NativeText), self);
            keyList.append(shortcut)
            shortcut.activated.connect(lambda key=str(i): self.addStampSignal.emit(key))
        return keyList

    def enableHotkeys(self, isClicked):
        for shortcut in self.hotkeys:
            shortcut.setEnabled(isClicked)

    def onDeselection(self):
        self.enableHotkeys(False)
        self.hotkeyButton.setChecked(False)

    # TODO delete
    def testHotKey(self, key):
        print("test")
        print(key)

    # TODO maybe repaint
    def loadSurveyStamps(self, keys):
        print("LSS")
        self.surveyDatetime = keys[0]
        filter = self.createFilter(keys)
        self.stampTableModel.setFilter(filter)
        self.stampTableModel.select()
        print("survey_datetime = " + self.surveyDatetime)
        QApplication.processEvents()
        self.repaint()

    def createFilter(self, keys):
        filter = "survey_datetime = \"" + self.surveyDatetime + "\""
        for i in range(1, len(keys)):
            filter = filter + " OR survey_datetime = \"" + keys[i] + "\""
        print(filter)
        return filter

    @pyqtSlot()
    def deleteButtonAction(self):
        for row in self.stampTableSelectionModel.selectedRows():
            self.stampTableModel.removeRow(row.row())
        self.stampTableSelectionModel.clearSelection()
        self.stampTableModel.select()
        QApplication.processEvents()

    def clearSurveyStamps(self):
        self.surveyDatetime = None
        # self.stampTableModel.setFilter("") # TODO will this work?
        self.stampTableModel.setFilter("survey_datetime = None")
        print("survey_datetime = None")

    def addStamp(self, stamp, key="-"):
        stampRecord = StampRecord(miliseconds=stamp, surveyDatetime=self.surveyDatetime, label=key, note="")
        sqlRecord = stampRecord.getQSQLRecord(self.stampTableModel.record())
        self.stampTableModel.insertRecord(0, sqlRecord)
        # self.surveyWidget.sortByKey()
        # self.surveyWidget.select(0)
        QApplication.processEvents()  # allow for selection highlight

    def addRecord(self, stampRecord):
        sqlRecord = stampRecord.getQSQLRecord(self.stampTableModel.record())
        print(self.stampTableModel.insertRowIntoTable(sqlRecord))


        # self.repaint() # TODO
        # self.surveyModeSignal.emit(modeOn)

    # @pyqtSlot(bool)
    # def enableSurvey(self, canSurvey):
    #     print(canSurvey)
    #     self.recordButton.setEnabled(canSurvey)

    @pyqtSlot()
    def testButtonAction(self):
        print("Test")

    @pyqtSlot(bool)
    def surveyMode(self, modeOn):
        self.addStampButton.setEnabled(modeOn)
        self.hotkeyButton.setEnabled(modeOn)
        self.enableHotkeys(self.hotkeyButton.isChecked())

    @pyqtSlot(QItemSelection)
    def onStampSelectionChange(self, selection):
        self.hasSelection = selection.count() > 0
        self.deleteStampButton.setEnabled(self.hasSelection)

    @pyqtSlot(bool)
    def enableStamps(self, modeOn):
        self.addStampButton.setEnabled(modeOn)
        self.hotkeyButton.setEnabled(modeOn)
        if not modeOn and self.hotkeyButton.isChecked():
            self.hotkeyButton.setChecked(False)
            self.enableHotkeys(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StampTableWidget()
    widget.show()
    sys.exit(app.exec_())