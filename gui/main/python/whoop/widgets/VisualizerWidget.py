import sys

# ugh hacky work around to fix pyplot import
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import librosa
import librosa.display
import librosa.core
import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog

from whoop.widgets.VisualizerView import VisualizerView

class VisualizerWidget(VisualizerView):

    def __init__(self):
        super().__init__()
        self.__connect()

    def __connect(self):
        self.addPath.clicked.connect(lambda ignore,
                                            field=self.npyField,
                                            fileMode=QFileDialog.AnyFile,
                                            filter=("*.npy"),
                                            acceptMode=QFileDialog.AcceptOpen: self.__showFileDialog(field, fileMode,
                                                                                                 acceptMode, filter))

        self.showButton.clicked.connect(self.__showSpectrogram)

    def __showSpectrogram(self):
        maxFreq = None if self.fullFreqCheck.isChecked() else self.maxFreqBox.value()
        minFreq = None if self.fullFreqCheck.isChecked() else self.minFreqBox.value()
        dialog = VisualizerDialog(self.npyField.text(),
                                  cmap=self.cmapCombo.currentText(),
                                  y_axis=self.yAxisCombo.currentText(),
                                  fmax=maxFreq,
                                  fmin=minFreq,
                                  x_axis='time',
                                  hop_length=self.hopBox.value(),
                                  sr=self.sampleRateBox.value(),
                                  parent=self)
        dialog.exec_()

    def __showFileDialog(self, field, fileMode, acceptMode, filter=None):
        dialog = QFileDialog(self)
        if filter != None:
            dialog.setNameFilter(filter)
        dialog.setFileMode(fileMode)  # QFileDialog.Directory
        dialog.setAcceptMode(acceptMode)
        if dialog.exec_():
            out = dialog.selectedFiles()[0]
            print(out)
            field.setText(out)

class VisualizerDialog(QDialog):

    def __init__(self, npyPath, cmap='viridis', y_axis='mel', fmax=200, fmin=2000, x_axis='time',
                                        hop_length=512, sr=41000, parent=None):
        super().__init__(parent)
        plt.close()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        canvas = FigureCanvas(self.displaySpec(npyPath, cmap, y_axis, fmax, fmin, x_axis, hop_length, sr))
        toolbar = NavigationToolbar(canvas, self)
        self.mainLayout.addWidget(toolbar)
        self.mainLayout.addWidget(canvas)

    def displaySpec(self, npyPath, cmap, y_axis, fmax, fmin, x_axis, hop_length, sr):
        # TODO catch file not found
        spec = np.load(npyPath)
        axes = librosa.display.specshow(spec, cmap=cmap, y_axis=y_axis, fmax=fmax, fmin=fmin, x_axis=x_axis, hop_length=hop_length, sr=sr)
        figure = axes.figure
        figure.colorbar(axes.collections[0], format='%+2.0f dB')
        return figure

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = VisualizerWidget()
    widget.show()
    sys.exit(app.exec_())
