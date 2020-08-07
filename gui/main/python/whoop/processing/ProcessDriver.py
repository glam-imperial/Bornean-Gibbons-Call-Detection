'''
Manages multi-threaded execution of audio processing.

Author: Alexander Shiarella
'''

import os
import shutil
import datetime

from .AudioSplitter import AudioSplitter
from .AudioConverter import AudioConverter
from .AudioPredictor import AudioPredictor
from .CsvSorter import CsvSorter


class ProcessDriver():
    
    def __init__(self, setting, tempDirecs, model, statusSignal, killEvent, full="", clips=[], label=None):
        print("driver init")

        self.setting = setting
        self.tempDirecs = tempDirecs
        self.full = full
        self.clips = clips
        self.model = model
        self.statusSignal = statusSignal
        self.killEvent = killEvent

        if label == None:
            label = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        self.label = label

        self.csvPath = self.tempDirecs.createCsvPath(self.label)

        self.statusSignal.emit("Process driver initialized.")


    def go(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        return self.runAll() # TODO look at the settings and only run what is desired

    def runAll(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return
        print("run all")
        results = []

        print("________PROCESS DRIVER TEST SPLIT__________")
        print(self.setting == None)
        print(str(self.setting.toSplit()))
        print("________PROCESS DRIVER AFTER TEST SPLIT__________")

        if not self.setting.toSplit():
            self.statusSignal.emit("Skip splitting - using clips as input.")

        if self.setting.toSplit():
            self.split()

        print(self.setting.toConvert())
        if self.setting.toConvert():
            labels, partition = self.convert()

            if self.setting.toPredict():
                results = self.predict(labels, partition)

                if self.setting.toSavePos() or self.setting.toSaveNeg():
                    self.copyFromClips(results)

            if self.setting.toSaveNpy():
                self.moveNpy(partition["raw"])

        print(self.setting.toSaveClip())
        if self.setting.toSaveClip():
            self.copyUnprocessedClips()

        if self.killEvent.is_set():
            self.__cleanKill()
            return

        # self.sort() # todo only if saving csv individually
        return results
        
    def split(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        self.statusSignal.emit("Splitting audio from: " + self.full)
        self.splitter = AudioSplitter(clip_len = self.setting.audio["length"],
                                      shift_len = self.setting.audio["shift"])

        self.clips = self.splitter.returnSplit(input_file=self.full,
                                               output_folder=self.tempDirecs.clipDirec,
                                               aud_start=self.setting.getAudioStart(),
                                               aud_end=self.setting.getAudioEnd(),
                                               statusSignal=self.statusSignal)
    
    def convert(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        print(self.clips)
        self.statusSignal.emit("Converting audio clips to spectrograms.")
        self.converter = AudioConverter(sample_rate=self.setting.spectrogram["rate"],
                                        f_min=self.setting.getMinFreq(),
                                        f_max=self.setting.getMaxFreq(),
                                        mean_sub=self.setting.spectrogram["sub"],
                                        n_fft=self.setting.spectrogram["nfft"],
                                        power=self.setting.spectrogram["power"],
                                        hop_length=self.setting.spectrogram["hop"])

        return self.converter.processListReturn(clipList=self.clips, npy_folder=self.tempDirecs.npyDirec)
    
    def predict(self, labels, partition):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        self.predictor = AudioPredictor(model_file=self.setting.model["path"],
                                        npy_folder=self.tempDirecs.npyDirec, # TODO fix naming need to create temp maybe remove option
                                        model_params=self.setting.getModelParams(),
                                        model=self.model)
        # return self.predictor.predictReturnDict(labels, partition, csv_file=self.csvPath, saveCsv=True, threshold=self.setting.model["threshold"])
        return self.predictor.stoppablePredictReturnDict(labels, partition, self.killEvent, csv_file=self.csvPath, saveCsv=True,
                                                threshold=self.setting.model["threshold"])

    def moveNpy(self, idList):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        for id in idList:
            npyPath = os.path.join(self.tempDirecs.npyDirec, id + '.npy')
            shutil.move(npyPath, os.path.join(self.setting.getNpyDirec(), id + '.npy'))

    def moveUnprocessedClips(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        for clip in self.clips:
            clipFile = os.path.basename(clip)
            shutil.move(clip, os.path.join(self.setting.getClipDirec(), clipFile))

    def copyUnprocessedClips(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        for clip in self.clips:
            clipFile = os.path.basename(clip)
            shutil.copy(clip, os.path.join(self.setting.getClipDirec(), clipFile))

    def copyFromClips(self, results):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        for clip in self.clips:
            id = os.path.splitext(os.path.basename(clip))[0]
            result = int(results[id][2])
            if (self.setting.toSavePos() and result == 1):
                shutil.copy(clip, os.path.join(self.setting.getPosDirec(), id + '.wav'))
            elif (self.setting.toSaveNeg() and result == 0):
                  shutil.copy(clip, os.path.join(self.setting.getNegDirec(), id + '.wav'))
    
    def saveFromResults(self, results):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        for id, result in results.items():
            clipPath = os.path.join(self.tempDirecs.clipDirec, id + '.wav')
            if (self.setting.toSavePos() and int(result[2]) == 1):
                shutil.copy(clipPath, os.path.join(self.setting.getPosDirec(), id + '.wav'))
            if (self.setting.toSaveNeg() and int(result[2]) == 0):
                shutil.copy(clipPath, os.path.join(self.setting.getNegDirec(), id + '.wav'))
    
    def sort(self):
        if self.killEvent.is_set():
            self.__cleanKill()
            return

        self.sorter = CsvSorter(csv=self.csvPath) # TODO fix naming
        self.sorter.sort()

    # TODO
    def __cleanKill(self):
        print("TODO clean pool driver thread")


    def clean(self):
        pass