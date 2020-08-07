
# ugh hacky work around to fix pyplot import
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QPushButton, QCheckBox, QLabel, QRadioButton, QSpinBox, QLineEdit, QWidget, QDialog, QComboBox
from PyQt5.QtWidgets import QFormLayout, QButtonGroup, QGroupBox, QHBoxLayout, QGridLayout, QVBoxLayout, QStyle, QFileDialog
from PyQt5 import QtGui

PATH = '/Users/ajkshiarella/Desktop/thesis/mp3_player/example_songs/pyqt/test_temp/1-01 Mokshamu galada – Saramati – Adi_chunk_377500.npy'

class VisualizerView(QWidget):
    def __init__(self):

        super().__init__()

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # labels
        self.minFreqLabel = QLabel("Min Frequency")
        self.maxFreqLabel = QLabel("Max Frequency")

        # spin boxes
        self.minFreqBox = QSpinBox()
        self.maxFreqBox = QSpinBox()
        self.hopBox = QSpinBox()
        self.sampleRateBox = QSpinBox()

        # check boxes
        self.fullFreqCheck = QCheckBox("Full Frequency")

        # combo boxes
        self.cmapCombo = QComboBox()
        self.yAxisCombo = QComboBox()

        # text box
        self.npyField = QLineEdit()
        self.npyField.setText(PATH)

        # buttons
        self.addPath = QPushButton(self.style().standardIcon(QStyle.SP_FileLinkIcon), "")
        self.showButton = QPushButton("Show")

        self.__assemble()

    def __initBoxes(self):
        self.maxFreqBox.setRange(0, 999999)
        self.minFreqBox.setRange(0, 999999)
        self.hopBox.setRange(0, 999999)
        self.sampleRateBox.setRange(0, 999999)
        self.minFreqBox.setValue(200)
        self.maxFreqBox.setValue(2000)
        self.hopBox.setValue(512)
        self.sampleRateBox.setValue(44100)
        self.cmapCombo.addItems(plt.colormaps())
        self.cmapCombo.setCurrentIndex(plt.colormaps().index("viridis"))
        self.yAxisCombo.addItems(["mel", "linear", "log", "cqt_hz"])
        self.yAxisCombo.setCurrentIndex(0)

    def __createSettingsGroup(self):
        self.__initBoxes()
        group = QGroupBox("Settings")
        layout = QGridLayout()
        form = QFormLayout()
        layout.addWidget(self.fullFreqCheck, 0, 0, 1, 2)
        form.addRow(self.minFreqLabel, self.minFreqBox)
        form.addRow(self.maxFreqLabel, self.maxFreqBox)
        form.addRow(QLabel("Hop Length"), self.hopBox)
        form.addRow(QLabel("Sample Rate"), self.sampleRateBox)
        form.addRow(QLabel("Color Map"), self.cmapCombo)
        form.addRow(QLabel("y-Axis"), self.yAxisCombo)
        layout.addItem(form, 1, 0, 1, 2)
        group.setLayout(layout)
        self.fullFreqCheck.clicked.connect(self.__onFullFreqCheck)
        return group

    def __onFullFreqCheck(self, isChecked):
        self.minFreqLabel.setDisabled(isChecked)
        self.maxFreqLabel.setDisabled(isChecked)
        self.minFreqBox.setDisabled(isChecked)
        self.maxFreqBox.setDisabled(isChecked)

    def __assemble(self):
        self.mainLayout.addWidget(QLabel("File"), 0, 0, 1, 1)
        self.mainLayout.addWidget(self.npyField, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.addPath, 0, 3, 1, 1)
        self.mainLayout.addWidget(self.showButton, 1, 3, 1, 1)
        self.mainLayout.addWidget(self.__createSettingsGroup(), 4, 0, 5, 4)


'''
spec = convert_wav_to_melspec(wav_file=Config.WAV_EX4)
# spec = convert_wav_to_mfcc(wav_file=WAV_EX)
# spec = np.load(Config.NPY_EX)
print(spec.shape)
print(spec)

# Plot for testing
plt.figure(figsize=(431/30, 128/30))
# TODO: make sure that the parameters match your spectrogram, otherwise axes will be wrong!
librosa.display.specshow(spec, cmap='viridis', y_axis='mel', fmax=200, fmin=2000, x_axis='time', hop_length=512, sr=SAMPLE_RATE)
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
'''

