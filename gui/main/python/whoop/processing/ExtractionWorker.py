'''
Worker thread for extracting clips from audio either continuously or using timestamp survey data.

Author: Alexander Shiarella
'''

from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

from PyQt5.QtCore import QObject, pyqtSignal

from ..widgets.ExtractorWidget import Type as ExtractionType
from whoop.processing.AudioSplitter import AudioSplitter


# todo run io tasks multithreaded then pool lists and run predictions in parallel (maybe processes)
class ExtractionWorker(Thread, QObject):

    testSignal = pyqtSignal()
    runModeSignal = pyqtSignal(bool)
    statusSignal = pyqtSignal(str)

    def __init__(self, parent, splitterArgs, audioInfo, type, audioStart, audioEnd, outputDirec): # setting, audioTup, model):
        Thread.__init__(self)
        QObject.__init__(self)

        self.parent = parent # TODO maybe remove
        # self.splitter = splitter
        self.splitterArgs = splitterArgs
        self.audioInfo = audioInfo
        self.type = type
        self.audioStart = audioStart
        self.audioEnd = audioEnd
        self.outputDirec = outputDirec

        self.splitter = AudioSplitter(*splitterArgs)


    @staticmethod
    def null():
        """Dummy factory for thread initialization"""
        return ExtractionWorker(None, (0, 0, 0, 0, 0), None, None, None, None, None)


    def run(self):
        if self.type == ExtractionType.CONT:
            self.runContinuousExtraction()
        else:
            self.runPointExtraction()


    def runContinuousExtraction(self):
        print("Running continuous extraction thread pool executor with default max workers.")
        self.statusSignal.emit("Running continuous extraction thread pool executor with default max workers.")

        with ThreadPoolExecutor() as executor:
            for audioFile in self.audioInfo:
                executor.submit(self.continuousExtractionTask, audioFile)

        self.runModeSignal.emit(False)


    def runPointExtraction(self):
        print("Running point count extraction thread pool executor with default max workers.")
        self.statusSignal.emit("Running point count extraction thread pool executor with default max workers.")

        with ThreadPoolExecutor() as executor:
            for audioFile, stampList in self.audioInfo.items():
                executor.submit(self.pointExtractionTask, audioFile, stampList)

        self.runModeSignal.emit(False)


    def continuousExtractionTask(self, audioFile):
        self.splitter.split(audioFile, self.outputDirec, self.audioStart, self.audioEnd)


    def pointExtractionTask(self, audioFile, stampList):
        print(audioFile)
        print(stampList)
        print(self.type == ExtractionType.BOTH)
        if self.type == ExtractionType.POS or self.type == ExtractionType.BOTH:
            print("extract pos")
            self.splitter.extract(stampList, ExtractionType.POS, audioFile,
                                  self.outputDirec[0], self.audioStart, self.audioEnd)
        if self.type == ExtractionType.NEG or self.type == ExtractionType.BOTH:
            print("extract neg")
            self.splitter.extract(stampList, ExtractionType.NEG, audioFile,
                                  self.outputDirec[1], self.audioStart, self.audioEnd)