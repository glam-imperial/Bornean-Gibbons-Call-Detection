'''
Worker thread for audio processing.

Author: Alexander Shiarella
'''

import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from PyQt5.QtCore import QObject, pyqtSignal

from .ProcessDriver import ProcessDriver
from whoop.processing.ProcessContainers import DirectoryContainer
from ..AppEnums import AudioInputType


# todo run io tasks multithreaded then pool lists and run predictions in parallel (maybe processes)
class ProcessWorker(Thread, QObject):

    testSignal = pyqtSignal()
    runModeSignal = pyqtSignal(bool)
    statusSignal = pyqtSignal(str)

    def __init__(self, parent, setting, audioTup, model, killEvent):
        Thread.__init__(self)
        QObject.__init__(self)

        self.parent = parent # TODO maybe remove
        self.setting = setting
        self.audioTup = audioTup
        self.directories = DirectoryContainer()
        self.model = model
        self.killEvent = killEvent

    @staticmethod
    def null():
        """Dummy factory for thread initialization"""
        return ProcessWorker(None, None, None, None, None)

    def run(self):
        if self.setting.getAudioInputType() == AudioInputType.FULL:
            self.runFullPool()
        elif self.setting.getAudioInputType() == AudioInputType.CLIP:
            self.runClipPool()
        else:
            print("ERROR")
            pass # TODO error?
        # self.directories.remove()

    def runFullPool(self):
        print("running full pool")
        numWorkers = len(self.audioTup) if len(self.audioTup) < 12 else 12
        self.statusSignal.emit("Running thread pool executor with " + str(numWorkers) + " max workers.")
        with ThreadPoolExecutor(max_workers=numWorkers) as executor:
            futures = []
            for file in self.audioTup:
                if self.killEvent.is_set():
                    self.__cleanKill()
                    return

                label = os.path.splitext(os.path.basename(file))[0]
                futures.append(executor.submit(self.task, ProcessDriver(self.setting,
                                                                        self.directories,
                                                                        self.model,
                                                                        killEvent=self.killEvent,
                                                                        full=file,
                                                                        label=label,
                                                                        statusSignal = self.statusSignal)))
        if self.setting.toSaveCsv():
            if self.killEvent.is_set():
                self.__cleanKill()
                return

            fullData = {}
            for x in as_completed(futures):
                print(x.result())
                if self.killEvent.is_set():
                    self.__cleanKill()
                    return
                fullData.update(x.result())
            self.__saveCsv(fullData, self.setting.getCsvDirec())
        self.runModeSignal.emit(False)
        self.directories.remove()

    def runClipPool(self):
        futures = []
        self.statusSignal.emit("Running thread pool executor with default max workers.")
        with ThreadPoolExecutor() as executor: # TODO maybe use a process pool executor
            if self.killEvent.is_set():
                self.__cleanKill()
                return

            futures.append(executor.submit(self.task, ProcessDriver(self.setting,
                                                                    self.directories,
                                                                    killEvent=self.killEvent,
                                                                    clips=self.audioTup,
                                                                    model=self.model,
                                                                    statusSignal=self.statusSignal)))
        if self.setting.toSaveCsv():
            if self.killEvent.is_set():
                self.__cleanKill()
                return

            fullData = {}
            for x in as_completed(futures):
                print(x.result())
                fullData.update(x.result())
            self.__saveCsv(fullData, self.setting.getCsvDirec())
        self.runModeSignal.emit(False)
        self.directories.remove()

    # TODO
    def __cleanKill(self):
        print("TODO clean main worker thread")
        self.directories.remove()
        self.runModeSignal.emit(False)

    def __saveCsv(self, data, csvFile):
        data_frame = pd.DataFrame.from_dict(data, orient='index', columns=['X', 'Y', 'Label'])
        print("saving: " + csvFile)
        self.statusSignal.emit("Saving CSV: " + csvFile)
        data_frame.to_csv(csvFile)

    def task(self, driver):
        return driver.go()
