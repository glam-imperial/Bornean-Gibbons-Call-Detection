from PyQt5.QtWidgets import QApplication, QPushButton, QCheckBox, QLabel, QRadioButton, QSpinBox, QLineEdit, QListWidget, QStyle
from PyQt5.QtWidgets import QFormLayout, QButtonGroup, QGroupBox, QHBoxLayout, QGridLayout, QVBoxLayout, QWidget, QAbstractItemView

from .AppWidget import AppWidget

class ExtractorView(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # labels
        self.startLabel = QLabel("Audio Start")
        self.endLabel = QLabel("Audio End")
        self.alphaLabel = QLabel("Alpha")
        self.betaLabel = QLabel("Beta")
        self.gammaLabel = QLabel("Gamma")
        self.deltaLabel = QLabel("Delta")
        self.posLabel = QLabel("Positive")
        self.negLabel = QLabel("Negative")
        self.valLabel = QLabel("Validation")

        # radio buttons
        self.pointCheck = QRadioButton("Point Count")
        self.continuousCheck = QRadioButton("Continuous")

        # check boxes
        self.fullLengthCheck = QCheckBox("Full Length")
        self.posCheck = QCheckBox("Pos")
        self.negCheck = QCheckBox("Neg")
        self.extractAllCheck = QCheckBox("Extract All")

        # spin boxes
        self.startBox = QSpinBox()
        self.endBox = QSpinBox()
        self.alphaBox = QSpinBox()
        self.betaBox = QSpinBox()
        self.gammaBox = QSpinBox()
        self.deltaBox = QSpinBox()
        self.lengthBox = QSpinBox()
        self.shiftBox = QSpinBox()
        # TODO set max and min

        # text fields
        self.posField = QLineEdit()
        self.negField = QLineEdit()
        self.valField = QLineEdit()

        # buttons
        self.addPosButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.addNegButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.addValButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.defaultButton = QPushButton("Defaults")
        self.runButton = QPushButton("Run")

        # list
        self.labelList = QListWidget()

        # group
        self.labelListGroup = self.createLabelList()

        self.enable()
        self.connect()

        self.assemble()
        self.defaultAction()

    def createLabelList(self):
        box = QVBoxLayout()
        self.labelList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.labelList.addItem("-")
        for i in range (0, 10):
            self.labelList.addItem(str(i))

        groupBox = QGroupBox("Filter By Label")
        box.addWidget(self.extractAllCheck)
        box.addWidget(self.labelList)
        groupBox.setLayout(box)
        return groupBox

    def createControlBox(self):
        box = QHBoxLayout()
        box.addWidget(self.defaultButton)
        box.addWidget(self.runButton)
        return box

    def createOutputForm(self):
        clipNameLabel = QLabel("Include in clip filename:")

        formLayout = QFormLayout()
        formLayout.addRow(self.posLabel, self.posField)
        formLayout.addRow(self.negLabel, self.negField)
        formLayout.addRow(self.valLabel, self.valField)
        # formLayout.addRow(clipLabel, self.clipField)
        # formLayout.addRow(npyLabel, self.npyField)
        # formLayout.addRow(dictLabel, self.dictField)

        buttonLayout = QFormLayout()
        buttonLayout.addRow(self.addPosButton)
        buttonLayout.addRow(self.addNegButton)
        buttonLayout.addRow(self.addValButton)

        box = QHBoxLayout()
        box.addLayout(formLayout)
        box.addLayout(buttonLayout)

        groupBox = QGroupBox("Output Clip Directories")
        groupBox.setLayout(box)


        return groupBox

    def enable(self):
        # check boxes
        self.lengthBox.setDisabled(False)
        self.shiftBox.setDisabled(False)
        # # TODO set max and min

        # text fields
        # self.valField.setDisabled(True)
        # self.valLabel.setDisabled(True)

        # buttons
        self.addValButton.setDisabled(True) # TODO

        # list
        self.labelListGroup.setEnabled(False)
        self.labelList.setEnabled(False)

        self.posCheckAction(False)
        self.negCheckAction(False)

    def connect(self):
        # radio buttons
        self.pointCheck.clicked.connect(self.pointCheckAction)
        self.continuousCheck.clicked.connect(self.continuousCheckAction)
        # check boxes
        self.posCheck.clicked.connect(self.posCheckAction)
        self.negCheck.clicked.connect(self.negCheckAction)
        self.extractAllCheck.clicked.connect(self.extractAllCheckAction)
        # buttons
        self.defaultButton.clicked.connect(self.defaultAction)

    def pointCheckAction(self, isChecked):
        self.posCheck.setEnabled(isChecked)
        self.negCheck.setEnabled(isChecked)
        self.valField.setDisabled(isChecked)
        self.addValButton.setDisabled(isChecked) # TODO
        self.valLabel.setDisabled(isChecked)
        self.labelListGroup.setEnabled(isChecked)

        if isChecked:
            self.posCheckAction(self.posCheck.isChecked())
            self.negCheckAction(self.negCheck.isChecked())
        else:
            self.posCheckAction(False)
            self.negCheckAction(False)

        QApplication.processEvents()
        self.repaint()

    def continuousCheckAction(self, isChecked):
        if isChecked:
            self.pointCheckAction(False)

    def posCheckAction(self, isChecked):
        self.alphaBox.setEnabled(isChecked)
        self.alphaLabel.setEnabled(isChecked)
        self.betaBox.setEnabled(isChecked)
        self.betaLabel.setEnabled(isChecked)
        self.addPosButton.setEnabled(isChecked) # TODO
        self.posField.setEnabled(isChecked)
        self.posLabel.setEnabled(isChecked)

    def negCheckAction(self, isChecked):
        self.gammaBox.setEnabled(isChecked)
        self.gammaLabel.setEnabled(isChecked)
        self.deltaBox.setEnabled(isChecked)
        self.deltaLabel.setEnabled(isChecked)
        self.addNegButton.setEnabled(isChecked) # TODO
        self.negField.setEnabled(isChecked)
        self.negLabel.setEnabled(isChecked)

    def extractAllCheckAction(self, isChecked):
        self.labelList.setDisabled(isChecked)

    def defaultAction(self):
        # radio buttons
        self.pointCheck.setChecked(False)
        self.continuousCheck.setChecked(True)

        # check boxes
        self.posCheck.setChecked(False)
        self.negCheck.setChecked(False)
        self.extractAllCheck.setChecked(True)

        # spin boxes
        self.alphaBox.setValue(2000)
        self.betaBox.setValue(0)
        self.gammaBox.setValue(4000)
        self.deltaBox.setValue(6000)
        self.lengthBox.setValue(5000)
        self.shiftBox.setValue(2500)
        # TODO set max and min

        # text fields TODO defaults
        self.posField.clear()
        self.negField.clear()
        self.valField.clear()

        # buttons
        self.addPosButton.setDisabled(True)
        self.addNegButton.setDisabled(True)
        self.addValButton.setDisabled(False)
        self.runButton.setDisabled(False) # TODO

    # TODO
    def fileNameSelector(self):
        pass

    def createAlgorithmForm(self):
        self.fullLengthCheck.setChecked(True)

        # spin box settings
        self.startBox.setRange(0, 999999999)
        self.endBox.setRange(0, 999999999)
        self.alphaBox.setRange(0, 999999)
        self.betaBox.setRange(0, 999999)
        self.gammaBox.setRange(0, 999999)
        self.deltaBox.setRange(0, 999999)
        self.lengthBox.setRange(0, 999999)
        self.shiftBox.setRange(0, 999999)

        # form
        formLayout = QFormLayout()
        formLayout.addRow(self.startLabel, self.startBox)
        formLayout.addRow(self.endLabel, self.endBox)
        formLayout.addRow("Clip Length", self.lengthBox)
        formLayout.addRow("Shift Length", self.shiftBox)
        formLayout.addRow(self.alphaLabel, self.alphaBox)
        formLayout.addRow(self.betaLabel, self.betaBox)
        formLayout.addRow(self.gammaLabel, self.gammaBox)
        formLayout.addRow(self.deltaLabel, self.deltaBox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.fullLengthCheck)
        vbox.addLayout(formLayout)
        groupBox = QGroupBox("Algorithm Settings (ms)")
        groupBox.setLayout(vbox)
        self.onFullLengthCheck(True)
        self.fullLengthCheck.clicked.connect(self.onFullLengthCheck)
        return groupBox

    def onFullLengthCheck(self, isChecked):
        self.startBox.setDisabled(isChecked)
        self.endBox.setDisabled(isChecked)
        self.startLabel.setDisabled(isChecked)
        self.endLabel.setDisabled(isChecked)

    def createRadioGroup(self):
        radioGroup = QButtonGroup()
        radioBox = QGridLayout()
        self.posCheck.setDisabled(True)
        self.negCheck.setDisabled(True)
        radioGroupBox = QGroupBox("Extraction Type")
        radioGroup.addButton(self.pointCheck)
        radioGroup.addButton(self.continuousCheck)
        radioBox.addWidget(self.pointCheck, 0, 0)
        radioBox.addWidget(self.posCheck, 0, 1)
        radioBox.addWidget(self.negCheck, 1, 1)
        radioBox.addWidget(self.continuousCheck, 2, 0)
        radioGroupBox.setLayout(radioBox)
        return radioGroupBox

    def assemble(self):
        # self.mainLayout.addWidget(self.createRadioGroup(), 0, 0)
        # self.mainLayout.addWidget(self.createOutputForm(), 1, 0)
        # self.mainLayout.addWidget(self.createAlgorithmForm(), 2, 0)
        # self.mainLayout.addLayout(self.createControlBox(), 3, 0)
        self.mainLayout.addWidget(self.createRadioGroup(), 0, 0)
        self.mainLayout.addWidget(self.createOutputForm(), 3, 0, 1, 2)
        self.mainLayout.addWidget(self.labelListGroup, 1, 0)
        self.mainLayout.addWidget(self.createAlgorithmForm(), 0, 1, 2, 1)
        self.mainLayout.addLayout(self.createControlBox(), 4, 1)


'''
Extraction:

pre-req: needs a survey with a valid file path
--> require audio to be loaded into media player

extraction mode button:
	enable extraction widget
	disable audio widget's remove button
	disable survey widget, except table, but make table not editable or selectable
		maybe filter selected surveys
	populate extraction widget
		Number of selected surveys
		Extraction mode (check boxes):
			positive: --> enable Positive Directory and alpha beta?
			negative: --> enable Negative Directory and gamma delta?
			validation: --> diable Positive
		Extraction labels:
			[a, b, c, d, 45, 0]
			or check list?
		Positive directory: --> file explorer
		Negative directory: --> file explorer
		Validation directory: --> file explorer
		file name:
			survey_datetime
			recorder_id
			recording_datetime
			audio filename (no path)
		Algorithm (help -> launch graph):
			variables:
				alpha, beta, gamma, delta
				clip length
				shift length?

'''