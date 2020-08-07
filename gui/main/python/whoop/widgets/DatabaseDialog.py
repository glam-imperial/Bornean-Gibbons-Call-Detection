"""
Initial dialog to select an exiting database or create a new one using SQL in AppResources.SQLResources.

Author: Alexander Shiarella
"""

import sqlite3
import os

from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QDialogButtonBox, QLineEdit, QFileDialog, QStyle

from ..AppResources import SQLResources

class DatabaseDialog(QDialog):

    def __init__(self, logWidget, parent=None):
        super().__init__(parent)

        self.logWidget = logWidget

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.fileChooserDialog = QFileDialog(self)
        self.fileChooserDialog.setFileMode(QFileDialog.ExistingFile)
        self.fileChooserDialog.setNameFilter(("*.db"))

        self.selectButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.selectButton.setToolTip("Select existing database")
        self.addButton = QPushButton("Create")
        self.addButton.setToolTip("Create new empty database")
        self.databaseField = QLineEdit()
        self.databaseField.setEnabled(False)

        self.mainLayout.addWidget(QLabel("Select or create a database."))
        self.__createForm()
        self.__connectFileChooser()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(("buttonBox"))
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setEnabled(False)
        self.__initButtons()

        self.infoLabel = QLabel()
        self.mainLayout.addWidget(self.infoLabel)


    def getDatabasePath(self):
        """return the chosen or created database path shown in the text field"""
        return self.databaseField.text()

    def __initButtons(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout.addWidget(self.buttonBox)

    def __createForm(self):
        formLayout = QFormLayout()
        formLayout.addRow("File Path", self.databaseField)

        buttonLayout = QFormLayout()
        buttonLayout.addRow(self.selectButton)
        buttonLayout.addRow(self.addButton)

        box = QHBoxLayout()
        box.addLayout(formLayout)
        box.addLayout(buttonLayout)

        self.mainLayout.addLayout(box)

    def __connectFileChooser(self):
        self.selectButton.clicked.connect(self.__showDatabaseSelector)
        self.addButton.clicked.connect(self.__showDatabaseCreator)

    # TODO use utility method
    def __showDatabaseSelector(self):
        self.fileChooserDialog.setAcceptMode(QFileDialog.AcceptOpen)
        if self.fileChooserDialog.exec_():
            dir = self.fileChooserDialog.selectedFiles()[0]
            self.databaseField.setText(dir)
            self.okButton.setEnabled(True)

    def __showDatabaseCreator(self):
        self.fileChooserDialog.setAcceptMode(QFileDialog.AcceptSave)
        if self.fileChooserDialog.exec_():
            dir = self.fileChooserDialog.selectedFiles()[0]
            self.databaseField.setText(dir)
            if self.__createDatabase():
                self.databaseField.setText(dir)
                self.okButton.setEnabled(True)
            else:
                self.databaseField.clear()

    def __createDatabase(self):
        filePath = self.getDatabasePath()

        # TODO have warning dialog to confirm deletion, based on user setting
        # if os.path.exists(filePath):
        #     print("removing file", filePath)
        #     os.remove(filePath)

        if not os.path.exists(filePath):
            connection = sqlite3.connect(filePath)
            if self.__initDatabase(connection):
                print("Creating database: ", filePath) # TODO remove
                self.logWidget.logItem("Created new database " + filePath)
                self.infoLabel.setText("Created new database: " + filePath)
                return True

        else:
            print("Using existing database - use a unique name to create an empty database.") # TODO dialog stuff, db overwrite option
            # self.logWidget.logItem("Created new database " + filePath)
            self.infoLabel.setText("Database overwrite not allowed with current user settings. Use a unique name or select an existing database.")
            return False

    def __initDatabase(self, connection):
        try:
            connection.execute(SQLResources.createAnnotationTable)
            connection.execute(SQLResources.createSurveyTable)
            return True
        except sqlite3.Error as e:
            self.infoLabel.setText("Error creating new database: " + e)
            return False