import os

from PyQt5.QtWidgets import QFileDialog, QLineEdit, QShortcut
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence

from .ValidateView import ValidateView

class ValidateWidget(ValidateView):

    moveSignal = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        for field, button in self.formDict.items():
            self.__connectDialog(field, button)

        for field, button in self.moveDict.items():
            self.__connectMove(field, button)

        self.hotkeys = self.__initHotkeys()
        self.hotkeyButton.clicked.connect(self.enableHotkeys)

    # TODO move into utility method
    def __connectDialog(self, field, button):
        button.clicked.connect(lambda ignore,
                                      field=field,
                                      fileMode=QFileDialog.Directory,
                                      acceptMode=QFileDialog.AcceptOpen : self.__showDialog(field, fileMode, acceptMode))

    def __connectMove(self, field, button):
        button.clicked.connect(lambda ignore,
                                      field=field : self.__movePreCheck(field))

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

    @pyqtSlot(QLineEdit)
    def __movePreCheck(self, field):
        direc = field.text()
        if not os.path.exists(direc):
            print("new direc: ", direc) # TODO remove
            try:
                os.mkdir(direc)
            except Exception as e:
                print("directory could not be created") # TODO notfication
                print(e)

        self.moveSignal.emit(direc, self.removeCheck.isChecked())

    def __initHotkeys(self):
        keyList = []
        shortcutP = QShortcut(QKeySequence("p", QKeySequence.NativeText), self);
        shortcutP.activated.connect(self.move1.click)
        shortcutN = QShortcut(QKeySequence("n", QKeySequence.NativeText), self);
        shortcutN.activated.connect(self.move2.click)
        shortcutN = QShortcut(QKeySequence("o", QKeySequence.NativeText), self);
        shortcutN.activated.connect(self.move3.click)
        # for i in range (, 'e'):
        #     shortcut = QShortcut(QKeySequence(str(i), QKeySequence.NativeText), self);
        #     keyList.append(shortcut)
        #     print(i)
        #     shortcut.activated.connect(self.moveByKey)
        return keyList

    # def moveByKey(self):
    #     key = 0
    #     print("clicked")
    #     self.buttonList[key].click()
    #     print(key)

    def enableHotkeys(self, isClicked):
        print(isClicked)
        for shortcut in self.hotkeys:
            shortcut.setEnabled(isClicked)

    def onDeselection(self):
        self.enableHotkeys(False)
        self.hotkeyButton.setChecked(False)
