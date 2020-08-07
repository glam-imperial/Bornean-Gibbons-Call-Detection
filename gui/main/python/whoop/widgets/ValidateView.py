from PyQt5.QtWidgets import QApplication, QPushButton, QCheckBox, QLabel, QRadioButton, QSpinBox, QLineEdit
from PyQt5.QtWidgets import QFormLayout, QButtonGroup, QGroupBox, QHBoxLayout, QGridLayout, QVBoxLayout, QStyle

from .ShrinkableButton import ShrinkableButton
from .AppWidget import AppWidget

class ValidateView(AppWidget):

    def __init__(self):
        super().__init__()

        # text fields
        self.field1 = QLineEdit()
        self.field2 = QLineEdit()
        self.field3 = QLineEdit()
        self.field4 = QLineEdit()
        self.field5 = QLineEdit()

        # check box
        self.removeCheck = QCheckBox("remove original")

        # push buttons
        self.add1 = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.add2 = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.add3 = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.add4 = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.add5 = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.move1 = QPushButton(self.style().standardIcon(QStyle.SP_DialogApplyButton), "  (p)")
        self.move2 = QPushButton(self.style().standardIcon(QStyle.SP_DialogApplyButton), "  (n)")
        self.move3 = QPushButton(self.style().standardIcon(QStyle.SP_DialogApplyButton), "  (o)")
        self.move4 = QPushButton(self.style().standardIcon(QStyle.SP_DialogApplyButton), "")
        self.move5 = QPushButton(self.style().standardIcon(QStyle.SP_DialogApplyButton), "")
        self.hotkeyButton = ShrinkableButton("Hotkeys")

        self.formDict = {self.field1 : self.add1,
                         self.field2 : self.add2,
                         self.field3 : self.add3,
                         self.field4 : self.add4,
                         self.field5 : self.add5}

        self.moveDict = {self.field1: self.move1,
                         self.field2: self.move2,
                         self.field3: self.move3,
                         self.field4: self.move4,
                         self.field5: self.move5}

        self.buttonList = [self.move1, self.move2, self.move3, self.move4, self.move5]

        self.assemble()

    def createForm(self):
        grid = QGridLayout()
        grid.addWidget(self.removeCheck, 0, 1)
        grid.addWidget(self.hotkeyButton, 0, 0)

        grid.addWidget(self.move1, 1, 0)
        grid.addWidget(self.move2, 2, 0)
        grid.addWidget(self.move3, 3, 0)
        grid.addWidget(self.move4, 4, 0)
        grid.addWidget(self.move5, 5, 0)
        grid.addWidget(self.field1, 1, 1)
        grid.addWidget(self.field2, 2, 1)
        grid.addWidget(self.field3, 3, 1)
        grid.addWidget(self.field4, 4, 1)
        grid.addWidget(self.field5, 5, 1)
        grid.addWidget(self.add1, 1, 2)
        grid.addWidget(self.add2, 2, 2)
        grid.addWidget(self.add3, 3, 2)
        grid.addWidget(self.add4, 4, 2)
        grid.addWidget(self.add5, 5, 2)
        return grid

    def assemble(self):
        self.hotkeyButton.setCheckable(True)
        self.hotkeyButton.setChecked(False)
        self.mainLayout.addLayout(self.createForm())


