import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QSlider, QListView, QAbstractItemView, QSizePolicy, QStyle
from PyQt5.QtCore import Qt, QSize

from .AppWidget import AppWidget
from ..AppResources import MediaPlayerResources as R

class MediaPlayerView(AppWidget):

    def __init__(self):
        super().__init__()

        # controls
        self.previousButton = QPushButton(self.style().standardIcon(QStyle.SP_MediaSeekBackward), "") # TODO change to icons
        self.playButton = QPushButton(self.style().standardIcon(QStyle.SP_MediaPlay), "")
        self.pauseButton = QPushButton(self.style().standardIcon(QStyle.SP_MediaPause), "")
        self.nextButton = QPushButton(self.style().standardIcon(QStyle.SP_MediaSeekForward), "")
        self.stopButton = QPushButton(self.style().standardIcon(QStyle.SP_MediaStop), "")
        self.removeButton = QPushButton(self.style().standardIcon(QStyle.SP_DialogCancelButton), "")
        self.volumeSlider = QSlider()
        self.initControls()

        # seek bar
        self.timeSlider = QSlider()
        self.currentTimeLabel = QLabel()
        self.totalTimeLabel = QLabel()
        self.initSeekBar()

        # playlist
        self.playlistView = QListView()
        self.initPlaylistView()

        self.assemble()

    def initControls(self):
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", R.initVolume)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.playButton.setDisabled(True)
        self.pauseButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.previousButton.setDisabled(True)
        self.nextButton.setDisabled(True)
        self.removeButton.setDisabled(True)

    def initSeekBar(self):
        self.timeSlider.setOrientation(Qt.Horizontal)
        self.currentTimeLabel.setMinimumSize(QSize(R.timeLabelWidth, 0))
        self.currentTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.totalTimeLabel.setMinimumSize(QSize(R.timeLabelWidth, 0))
        self.totalTimeLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.currentTimeLabel.setText(R.initTimeLabel)
        self.totalTimeLabel.setText(R.initTotalTimeLabel)

    def initPlaylistView(self):
        self.playlistView.setAcceptDrops(True)
        self.playlistView.setProperty("showDropIndicator", True)
        self.playlistView.setDragDropMode(QAbstractItemView.DropOnly)
        self.playlistView.setAlternatingRowColors(True)
        self.playlistView.setUniformItemSizes(True)

    def assemble(self):
        # controls
        buttonGroup = QHBoxLayout()
        buttonGroup.addWidget(self.previousButton)
        buttonGroup.addWidget(self.playButton)
        buttonGroup.addWidget(self.pauseButton)
        buttonGroup.addWidget(self.stopButton)
        buttonGroup.addWidget(self.nextButton)
        buttonGroup.addWidget(self.volumeSlider)
        buttonGroup.addWidget(self.removeButton)

        # seek bar
        timerLayout = QHBoxLayout()
        timerLayout.addWidget(self.currentTimeLabel)
        timerLayout.addWidget(self.timeSlider)
        timerLayout.addWidget(self.totalTimeLabel)

        # main layout
        self.mainLayout.addWidget(self.playlistView)
        self.mainLayout.addLayout(timerLayout)
        self.mainLayout.addLayout(buttonGroup)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MediaPlayerView()
    widget.show()
    sys.exit(app.exec_())