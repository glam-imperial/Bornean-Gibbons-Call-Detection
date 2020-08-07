import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QAbstractListModel, QItemSelection
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

from .MediaPlayerView import MediaPlayerView
from ..AppUtils import hhmmss

# mapping of QMediaPlaylist data to QAbstractListModel
class PlaylistModel(QAbstractListModel):

    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().toLocalFile() #.fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()

class MediaPlayerWidget(MediaPlayerView):

    playlistSelectionChangedSignal = pyqtSignal()
    durationChangeSignal = pyqtSignal(int)
    mediaChangedSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.selected = False

        # set up player and playlist
        self.player = QMediaPlayer()
        self.player.error.connect(self.erroralert)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.playlistModel = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.playlistModel)
        self.playlist.currentIndexChanged.connect(self.onPlaylistIndexChange)
        self.selectionModel = self.playlistView.selectionModel()
        self.selectionModel.selectionChanged.connect(self.onPlaylistSelectionChange)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

        self.playlist.mediaChanged.connect(self.onMediaChange)
        self.playlist.mediaRemoved.connect(self.onMediaChange)
        self.playlist.mediaInserted.connect(self.onMediaChange)

        # connect controls
        self.player.mediaStatusChanged.connect(self.endOfMediaCheck) # stay on same audio file until user clicks otherwise
        self.playButton.pressed.connect(self.player.play)
        self.pauseButton.pressed.connect(self.player.pause)
        self.stopButton.pressed.connect(self.player.stop)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)
        self.previousButton.pressed.connect(self.playlist.previous)
        self.nextButton.pressed.connect(self.playlist.next)
        self.removeButton.pressed.connect(self.removeButtonAction)

        # connect seek bar
        self.timeSlider.valueChanged.connect(self.player.setPosition)

    # do not automatically proceed to next at end of audio
    @pyqtSlot(QMediaPlayer.MediaStatus)
    def endOfMediaCheck(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.stop()

    # info to populate AddSurveyDialog
    def getDialogArgs(self):
        audioFiles = set()
        if self.playlist.mediaCount() > 0:
            for row in range (0, self.playlist.mediaCount()):
                media = self.playlist.media(row)
                audioFiles.add(media.canonicalUrl().toLocalFile())

        kwargs = {"audioSelected" : self.hasSelection(),
                  "audioDuration" : str(self.player.duration()),
                  "audioFiles": audioFiles,
                  "audioFile" : str(self.player.currentMedia().canonicalUrl().toLocalFile())}
        return kwargs

    # TODO maybe remove
    # for the survey info dialog
    @pyqtSlot(str)
    def changeSelection(self, path):
        self.select(path)
        QApplication.processEvents()

    def getCurrentMediaUrl(self):
        return self.player.currentMedia().canonicalUrl().toLocalFile()

    def fileIndex(self, filePath):
        for index in range(0, self.playlist.mediaCount()):
            media = self.playlist.media(index)
            compURL = media.canonicalUrl().toLocalFile()
            if filePath == compURL:
                return index
        return -1 # TODO magic number

    def getAllMedia(self):
        mediaList = []
        for index in range(0, self.playlist.mediaCount()):
            media = self.playlist.media(index)
            url = media.canonicalUrl().toLocalFile()
            mediaList.append(url)
        return mediaList

    def select(self, url):
        # case 1: no single url
        if url is None:
            self.deSelect()
            return

        # case 2: url in playlist
        index = self.fileIndex(url)
        if index > -1: # TODO magic number
            self.playlist.setCurrentIndex(index)
            self.playlist.currentIndexChanged.emit(index)
            self.playlistModel.layoutChanged.emit()
            return

        # case 3: url not in playlist
        self.deSelect()

    def deSelect(self):
        self.selectionModel.clearSelection()
        self.playlistModel.layoutChanged.emit()

    def isLoaded(self, url):
        for index in range(0, self.playlist.mediaCount()):
            media = self.playlist.media(index)
            compURL = media.canonicalUrl().toLocalFile()
            if url == compURL:
                return True
        return False

    # TODO maybe swich attribute to self.hasSelection() accessing component class
    def hasSelection(self):
        return self.selected

    @pyqtSlot()
    def onMediaChange(self):
        print("Media Changed")
        self.mediaChangedSignal.emit(self.playlist.mediaCount() > 0)

    # triggered from self.selection_model.selectionChanged
    @pyqtSlot(QItemSelection)
    def onPlaylistSelectionChange(self, selection):
        self.selected = selection.count() > 0 # TODO maybe swich attribute to self.hasSelection() accessing component class
        if self.hasSelection():
            i = selection.indexes()[0].row() # get int index of selected row
            self.playlist.setCurrentIndex(i)

        else:
            self.player.stop()

        self.playButton.setEnabled(self.hasSelection())
        self.pauseButton.setEnabled(self.hasSelection())
        self.nextButton.setEnabled(self.hasSelection())
        self.previousButton.setEnabled(self.hasSelection())
        self.stopButton.setEnabled(self.hasSelection())
        self.removeButton.setEnabled(self.hasSelection())

        QApplication.processEvents() # DO NOT REMOVE!
        self.playlistSelectionChangedSignal.emit()


    @pyqtSlot()
    def removeButtonAction(self):
        if self.hasSelection():
            self.player.stop()
            index = self.playlist.currentIndex()
            self.playlist.mediaAboutToBeRemoved.emit(index, index)
            self.playlist.removeMedia(self.playlist.currentIndex())
            self.playlist.mediaChanged.emit(index, index)
            self.playlistModel.layoutChanged.emit()

    def getMiliseconds(self):
        return self.player.position()

    # triggered from self.playlist.currentIndexChanged
    @pyqtSlot(int)
    def onPlaylistIndexChange(self, position):
        if position > -1:
            modelIndex = self.playlistModel.index(position) # QModelIndex
            self.playlistView.setCurrentIndex(modelIndex)
            self.repaint() # needed for selection highlight

    def update_duration(self, mc):
        self.timeSlider.setMaximum(self.player.duration())
        duration = self.player.duration()

        if duration >= 0:
            self.totalTimeLabel.setText(hhmmss(duration))
            self.durationChangeSignal.emit(duration) # kinda hacky but mitigates race condition on dialog update

    def update_position(self, *args):
        position = self.player.position()
        if position >= 0:
            self.currentTimeLabel.setText(hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(
                QMediaContent(url)
            )

        self.playlistModel.layoutChanged.emit()

    def erroralert(self, *args):
        print("Error: ", args)

    @pyqtSlot(bool)
    def surveyMode(self, modeOn):
        self.playlistView.setDisabled(modeOn)
        self.nextButton.setDisabled(modeOn)
        self.previousButton.setDisabled(modeOn)
        self.removeButton.setDisabled(modeOn)
        self.playButton.setEnabled(modeOn and self.hasSelection())
        self.pauseButton.setEnabled(modeOn and self.hasSelection())
        self.stopButton.setEnabled(modeOn and self.hasSelection())

    @pyqtSlot(bool)
    def editMode(self, modeOn):
        self.playlistView.setEnabled(modeOn)
        self.nextButton.setEnabled(modeOn and self.hasSelection())
        self.previousButton.setEnabled(modeOn and self.hasSelection())
        self.removeButton.setEnabled(modeOn and self.hasSelection())
        self.playButton.setEnabled(modeOn and self.hasSelection())
        self.pauseButton.setEnabled(modeOn and self.hasSelection())
        self.stopButton.setEnabled(modeOn and self.hasSelection())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = MediaPlayerWidget()
    widget.show()
    sys.exit(app.exec_())