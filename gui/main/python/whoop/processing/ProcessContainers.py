'''
Container classes for audio processing.

Author: Alexander Shiarella
'''

import datetime
import os
import shutil

from whoop.AppResources import baseDirec


# TODO maybe remove
class AudioContainer():

    def __init__(self, paths=(), split=False):

        self.paths = paths
        self.split = split

# container for directories of single thread in ThreadPoolExecutor
class DirectoryContainer():

    def __init__(self):
        self.datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        self.dataDirec = self.__createDataDirec()
        self.csvDirec = self.__createCsvDirec()
        self.clipDirec = self.__createClipDirec()
        self.npyDirec = self.__createNpyDirec()

    def createCsvPath(self, label=None):
        if label == None:
            label = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        csvPath = os.path.join(self.csvDirec, label + ".csv")
        print("returning: " + csvPath)
        return csvPath

    def remove(self):
        print("removing: " + self.dataDirec)
        shutil.rmtree(self.dataDirec)

    def __createDataDirec(self):
        dataDirec = os.path.join(baseDirec, self.datetime)
        if not os.path.exists(dataDirec):
            print("creating: " + dataDirec)
            os.mkdir(dataDirec)
        return dataDirec

    def __createCsvDirec(self):
        csvDirec = os.path.join(self.dataDirec, "csv/")
        if not os.path.exists(csvDirec):
            print("creating: " + csvDirec)
            os.mkdir(csvDirec)
        return csvDirec

    def __createClipDirec(self):
        clipDirec = os.path.join(self.dataDirec, "clip/")
        if not os.path.exists(clipDirec):
            print("creating: " + clipDirec)
            os.mkdir(clipDirec)
        return clipDirec

    def __createNpyDirec(self):
        npyDirec = os.path.join(self.dataDirec, "npy/")
        if not os.path.exists(npyDirec):
            print("creating: " + npyDirec)
            os.mkdir(npyDirec)
        return npyDirec