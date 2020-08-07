import sys
import os
import re

from PyQt5.QtWidgets import QRadioButton, QPushButton, QComboBox, QHBoxLayout, QSpinBox, QCheckBox, QLineEdit, QGroupBox, QStyle
from PyQt5.QtWidgets import QFormLayout, QButtonGroup, QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QSizePolicy, QDoubleSpinBox

from .ShrinkableButton import ShrinkableButton
from ..processing.ProcessSetting import ProcessSetting
from ..AppEnums import AudioSource, AudioInputType

# TODO maybe inherit AppWidget
class ProcessView(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QGridLayout()
        self.initLayout()

        # labels
        self.modelLoaded = QLabel("None")
        self.startLabel = QLabel("audio start")
        self.endLabel = QLabel("audio end")
        self.minFreqLabel = QLabel("min frequency")
        self.maxFreqLabel = QLabel("max frequency")

        # radio buttons
        self.fullRadio = QRadioButton("full")
        self.clipRadio = QRadioButton("clip")
        self.selectedRadio = QRadioButton("audio player (selected)")
        self.allRadio = QRadioButton("audio player (all)")
        self.direcRadio = QRadioButton("file directory")

        # push buttons
        self.addInputButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        # self.addInputButton.setMinimumWidth(20)
        # self.addInputButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.addCsvFileButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.addClipDirecButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.addPosDirecButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.addNegDirecButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.addNpyDirecButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.addPklDirecButton = QPushButton(self.style().standardIcon(QStyle.SP_DirLinkIcon), "")
        self.chooseModelButton = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.defaultsButton = ShrinkableButton("Defaults")
        self.defaultsButton.clicked.connect(self.setTestingDefaults) # TODO change
        self.loadButton = ShrinkableButton("Load Model")
        self.runButton = ShrinkableButton("Run")
        self.cancelButton = ShrinkableButton("Cancel")

        # check boxes
        self.clipCheck = QCheckBox("unsorted clips")
        self.csvCheck = QCheckBox("csv with predictions")
        self.posCheck = QCheckBox("pos predicted clips")
        self.negCheck = QCheckBox("neg predicted clips")
        self.npyCheck = QCheckBox(".npy files")
        self.fullLengthCheck = QCheckBox("process full length")
        self.meanSubCheck = QCheckBox("mean subtraction")
        self.fullFreqCheck = QCheckBox("full frequency")

        # text fields
        self.inputField = QLineEdit()
        self.csvField = QLineEdit()
        self.csvField.setMinimumWidth(30)
        self.clipField = QLineEdit()
        self.posField = QLineEdit()
        self.negField = QLineEdit()
        self.npyField = QLineEdit()
        self.modelFileField = QLineEdit()

        # spin boxes
        self.firstDimField = QSpinBox()
        self.secondDimField = QSpinBox()
        self.numClassField = QSpinBox()
        self.numChannelField = QSpinBox()
        self.lengthBox = QSpinBox()
        self.shiftBox = QSpinBox()
        self.startBox = QSpinBox()
        self.endBox = QSpinBox()
        self.nfftBox = QSpinBox()
        self.maxFreqBox = QSpinBox()
        self.minFreqBox = QSpinBox()
        self.hopBox = QSpinBox()
        self.sampleRateBox = QSpinBox()
        self.powerBox = QSpinBox()
        self.thresholdBox = QDoubleSpinBox()

        # combo boxes
        self.spectrogramType = QComboBox()

        # groups
        self.audioSettingsGroup = QGroupBox("Audio Settings")
        self.modelGroup = QGroupBox("Model")

        self.assemble()

    def getSetting(self):

        input = AudioInputType.FULL if self.fullRadio.isChecked() else AudioInputType.CLIP

        if self.selectedRadio.isChecked():
            source = AudioSource.SELECTED
        elif self.allRadio.isChecked():
             source = AudioSource.ALL
        elif self.direcRadio.isChecked():
             source = AudioSource.DIREC
        else:
            source = AudioSource.NONE

        output = {"csv": (self.csvCheck.isChecked(), self.csvField.text()),
                  "clip": (self.clipCheck.isChecked(), self.clipField.text()),
                  "pos": (self.posCheck.isChecked(), self.posField.text()),
                  "neg": (self.negCheck.isChecked(), self.negField.text()),
                  "npy": (self.npyCheck.isChecked(), self.npyField.text())}
        
        model = {"path": self.modelFileField.text(),
                 "first": self.firstDimField.value(),
                 "second": self.secondDimField.value(),
                 "classes": self.numClassField.value(),
                 "channels": self.numChannelField.value(),
                 "threshold": self.thresholdBox.value()}

        audio = {"length": self.lengthBox.value(),
                 "shift": self.shiftBox.value(),
                 "start": self.startBox.value(),
                 "end": self.endBox.value(),
                 "full": self.fullLengthCheck.isChecked()}

        spectrogram = {"type": self.spectrogramType.currentText(),
                       "full": self.fullFreqCheck.isChecked(),
                       "sub": self.meanSubCheck.isChecked(),
                       "rate": self.sampleRateBox.value(),
                       "min": self.minFreqBox.value(),
                       "max": self.maxFreqBox.value(),
                       "nfft": self.nfftBox.value(),
                       "power": self.powerBox.value(),
                       "hop": self.hopBox.value()}
        
        kwargs = {"input": input,
                  "source": source,
                  "direc": self.inputField.text(),
                  "spectrogram": spectrogram,
                  "audio": audio,
                  "output": output,
                  "model": model }
        
        return ProcessSetting(**kwargs)

    def setTestingDefaults(self):
        self.clear('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/pos_clip')
        self.clear('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/neg_clip')
        self.clear('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/clip_unsorted')
        self.clear('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/npy')
        self.direcRadio.setChecked(True)
        self.clipCheck.setChecked(True)
        self.csvCheck.setChecked(True)
        self.posCheck.setChecked(True)
        self.negCheck.setChecked(True)
        self.npyCheck.setChecked(True)
        self.inputField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/clip_orig')
        self.modelFileField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/model/model_g_5s_1.h5')
        self.posField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/pos_clip')
        self.negField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/neg_clip')
        self.clipField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/clip_unsorted')
        self.csvField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/csv/testFull.csv')
        self.npyField.setText('/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/default_test/npy')

    @staticmethod
    def clear(aud_folder):
        for filename in os.listdir(aud_folder):
            os.remove(os.path.join(aud_folder, filename))

    def initLayout(self):
        self.setLayout(self.mainLayout)

    def getLayout(self):
        return self.mainLayout

    def initModelValues(self):
        # self.modelDefaultButton.setCheckable(True)
        # self.modelDefaultButton.setDown(True)
        self.firstDimField.setRange(0, 9999)
        self.secondDimField.setRange(0, 9999)
        self.thresholdBox.setRange(0.000000001, 0.99999)
        self.thresholdBox.setDecimals(5)
        self.firstDimField.setValue(128)
        self.secondDimField.setValue(431)
        self.numClassField.setValue(2)
        self.numChannelField.setValue(1)
        self.thresholdBox.setValue(0.9)

    def createSettingsGroup(self):
        self.lengthBox.setRange(0, 999999)
        self.shiftBox.setRange(0, 999999)
        self.startBox.setRange(0, 999999999)
        self.endBox.setRange(0, 999999999)
        self.lengthBox.setValue(5000)
        self.shiftBox.setValue(2500)
        self.fullLengthCheck.setChecked(True)
        # self.startBox.setDisabled(True)
        # self.endBox.setDisabled(True)
        # self.audioSettingsGroup = QGroupBox("Audio Settings")
        # labels
        # lengthLabel = QLabel("clip length")
        # shiftLabel = QLabel("shift length")
        # form
        topForm = QFormLayout()
        bottomForm = QFormLayout()
        box = QVBoxLayout()
        topForm.addRow(QLabel("clip length"), self.lengthBox)
        topForm.addRow(QLabel("shift length"), self.shiftBox)
        bottomForm.addRow(self.startLabel, self.startBox)
        bottomForm.addRow(self.endLabel, self.endBox)
        box.addLayout(topForm)
        box.addWidget(self.fullLengthCheck)
        box.addLayout(bottomForm)
        self.audioSettingsGroup.setLayout(box)
        self.onFullLengthCheck(True)
        self.fullLengthCheck.clicked.connect(self.onFullLengthCheck)
        return self.audioSettingsGroup

    def onFullLengthCheck(self, isChecked):
        self.startBox.setDisabled(isChecked)
        self.endBox.setDisabled(isChecked)
        self.startLabel.setDisabled(isChecked)
        self.endLabel.setDisabled(isChecked)
        self.repaint()

    '''
    sample_rate=44100,
                 f_min=200,
                 f_max=2000,
                 mean_sub=True,
                 n_fft=2048,
                 power=2.0,
                 hop_length=512
                 
        self.nfftBox = QSpinBox()
        self.maxFreqBox = QSpinBox()
        self.minFreqBox = QSpinBox()
        self.hopBox = QSpinBox()
        self.sampleRateBox = QSpinBox()
        self.powerBox = QSpinBox()
    '''
    def createSpectrogramGroup(self):
        group = QGroupBox("Spectrogram Settings")
        form = QFormLayout()
        form.addRow(QLabel("type"), self.spectrogramType)
        form.addRow(QLabel("sample rate"), self.sampleRateBox)
        form.addRow(self.minFreqLabel, self.minFreqBox)
        form.addRow(self.maxFreqLabel, self.maxFreqBox)
        form.addRow(QLabel("nfft"), self.nfftBox)
        form.addRow(QLabel("power"), self.powerBox)
        form.addRow(QLabel("hop length"), self.hopBox)
        box = QVBoxLayout()
        box.addWidget(self.fullFreqCheck)
        box.addWidget(self.meanSubCheck)
        box.addLayout(form)
        group.setLayout(box)
        self.initSpectrogramValues()
        return group

    def onFullFreqChecked(self, isChecked):
        self.minFreqLabel.setDisabled(isChecked)
        self.maxFreqLabel.setDisabled(isChecked)
        self.minFreqBox.setDisabled(isChecked)
        self.maxFreqBox.setDisabled(isChecked)

    def initSpectrogramValues(self):
        self.spectrogramType.addItems(["powmel", "melspec", "stft", "powsq"])
        self.spectrogramType.setCurrentIndex(0)
        self.spectrogramType.setEditable(False)
        self.nfftBox.setRange(0, 999999)
        self.maxFreqBox.setRange(0, 999999)
        self.minFreqBox.setRange(0, 999999)
        self.hopBox.setRange(0, 999999)
        self.sampleRateBox.setRange(0, 999999)
        self.powerBox.setRange(0, 999999)
        self.nfftBox.setValue(2048)
        self.maxFreqBox.setValue(2000)
        self.minFreqBox.setValue(200)
        self.hopBox.setValue(512)
        self.sampleRateBox.setValue(44100)
        self.powerBox.setValue(2.0)
        self.meanSubCheck.setChecked(True)
        self.fullFreqCheck.setChecked(False)
        self.fullFreqCheck.clicked.connect(self.onFullFreqChecked)

    def createModelGroup(self):
        self.initModelValues()
        modelForm = QFormLayout()
        modelForm.addRow(QLabel("Model Loaded"), self.modelLoaded)
        modelForm.addRow(QLabel("Model File Path"), self.modelFileField)
        modelForm.addRow(QLabel("Decision Threshold"), self.thresholdBox)
        modelForm.addRow(QLabel("1st Dimension"), self.firstDimField)
        modelForm.addRow(QLabel("2nd Dimension"), self.secondDimField)
        modelForm.addRow(QLabel("# Classes"), self.numClassField)
        modelForm.addRow(QLabel("# Channels"), self.numChannelField)
        modelButtonLayout = QFormLayout()
        modelButtonLayout.addRow(QLabel(""))
        modelButtonLayout.addRow(self.chooseModelButton)
        modelBox = QGridLayout()
        modelBox.addLayout(modelForm, 1, 0)
        modelBox.addLayout(modelButtonLayout, 1, 1)
        self.modelGroup.setLayout(modelBox)
        self.modelGroup.setDisabled(True)
        return self.modelGroup

    def createInputGroup(self):
        radioGroup = QButtonGroup()
        radioBox = QGridLayout()
        radioGroupBox = QGroupBox("Input Type")
        radioGroup.addButton(self.fullRadio)
        radioGroup.addButton(self.clipRadio)
        radioBox.addWidget(self.fullRadio, 0, 0)
        radioBox.addWidget(self.clipRadio, 1, 0)
        self.fullRadio.setChecked(True)
        self.fullRadio.clicked.connect(self.onInputFullChecked)
        self.clipRadio.clicked.connect(self.onInputClipChecked)
        radioGroupBox.setLayout(radioBox)
        return radioGroupBox

    def onInputFullChecked(self, isChecked):
        self.audioSettingsGroup.setEnabled(isChecked)
        self.clipCheck.setEnabled(isChecked)
        self.clipField.setEnabled(isChecked)
        self.addClipDirecButton.setEnabled(isChecked)

    def onInputClipChecked(self, isChecked):
        if isChecked:
            self.onInputFullChecked(False)

    def createSourceGroup(self):
        radioGroup = QButtonGroup()
        radioBox = QGridLayout()
        radioGroupBox = QGroupBox("Audio Source")
        radioGroup.addButton(self.selectedRadio)
        radioGroup.addButton(self.allRadio)
        radioGroup.addButton(self.direcRadio)
        radioBox.addWidget(self.selectedRadio, 0, 0)
        radioBox.addWidget(self.allRadio, 1, 0)
        radioBox.addWidget(self.direcRadio, 2, 0)
        radioBox.addWidget(self.inputField, 3, 0)
        radioBox.addWidget(self.addInputButton, 3, 1)
        self.selectedRadio.setChecked(True)
        radioGroupBox.setLayout(radioBox)
        return radioGroupBox

    def createOutputGroup(self):
        grid = QGridLayout()
        grid.addWidget(self.csvCheck, 0, 0)
        grid.addWidget(self.posCheck, 1, 0)
        grid.addWidget(self.negCheck, 2, 0)
        grid.addWidget(self.npyCheck, 3, 0)
        grid.addWidget(self.clipCheck, 5, 0)
        grid.addWidget(self.csvField, 0, 1)
        grid.addWidget(self.posField, 1, 1)
        grid.addWidget(self.negField, 2, 1)
        grid.addWidget(self.npyField, 3, 1)
        grid.addWidget(self.clipField, 5, 1)
        grid.addWidget(self.addCsvFileButton, 0, 2)
        grid.addWidget(self.addPosDirecButton, 1, 2)
        grid.addWidget(self.addNegDirecButton, 2, 2)
        grid.addWidget(self.addNpyDirecButton, 3, 2)
        grid.addWidget(self.addClipDirecButton, 5, 2)
        outputGroupBox = QGroupBox("Output")
        outputGroupBox.setLayout(grid)
        return outputGroupBox

    def assemble(self):
        # hBox = QHBoxLayout()
        # hBox.addWidget(self.createInputGroup())
        # hBox.addWidget(self.createSourceGroup())
        # hBox.addWidget(self.createSettingsGroup())
        # self.mainLayout.addLayout(hBox, 0, 0, 1, 3)
        vBox = QVBoxLayout()
        vBox.addWidget(self.createInputGroup())
        vBox.addWidget(self.createSpectrogramGroup())
        self.mainLayout.addLayout(vBox, 0, 0, 2, 1)
        self.mainLayout.addWidget(self.createSourceGroup(), 0, 1, 1, 1)
        self.mainLayout.addWidget(self.createSettingsGroup(), 1, 1, 1, 1)
        # self.mainLayout.addWidget(self.createSpectrogramGroup(), 0, 2, 2, 1)
        self.mainLayout.addWidget(self.createOutputGroup(), 0, 3, 1, 1)
        # self.mainLayout.addWidget(self.createSpectrogramGroup(), 2, 0, 1, 1)
        self.mainLayout.addWidget(self.createModelGroup(), 1, 3, 1, 1)
        buttonBox = QHBoxLayout()
        buttonBox.addWidget(self.defaultsButton)
        buttonBox.addWidget(self.loadButton)
        buttonBox.addWidget(self.runButton)
        buttonBox.addWidget(self.cancelButton)
        self.mainLayout.addLayout(buttonBox, 3, 0, 1, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ProcessView()
    widget.show()
    sys.exit(app.exec_())



