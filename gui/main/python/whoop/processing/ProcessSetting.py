'''
Stores UI settings for audio processing and translates them to backend logic.

Author: Alexander Shiarella
'''

from ..AppEnums import AudioSource, AudioInputType


# todo switch to private assignment in init with properties
class ProcessSetting():
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.input = kwargs["input"] # see AppEnums.AudioInputType
        self.source = kwargs["source"] # see AppEnums.AudioSource
        self.direc = kwargs["direc"] # ignored if source not AudioSource.DIREC
        self.audio = kwargs["audio"]
        self.spectrogram = kwargs["spectrogram"]
        self.output = kwargs["output"]
        self.model = kwargs["model"]

    def toPredict(self):
        return self.toSaveNeg() or self.toSavePos() or self.toSaveCsv()

    def toConvert(self):
        return self.toPredict() or self.toSaveNpy()

    def toSplit(self):
        print("____TO SPLIT (input values in setting____")
        print(self.input)
        return self.input == AudioInputType.FULL and (self.toConvert() or self.toSaveClip())

    def getAudioInputType(self):
        return self.input

    def getAudioSource(self):
        return self.source

    def getAudioDirec(self):
        return self.direc if self.getAudioSource() == AudioSource.DIREC else None

    def getAudioStart(self):
        return 0 if self.audio["full"] else self.audio["start"]

    def getAudioEnd(self):
        return None if self.audio["full"] else self.audio["end"]

    def getMaxFreq(self):
        return None if self.spectrogram["full"] else self.spectrogram["max"]

    def getMinFreq(self):
        return None if self.spectrogram["full"] else self.spectrogram["min"]

    def toSaveClip(self):
        return self.output["clip"][0] == True
    
    def toSavePos(self):
        return self.output["pos"][0] == True

    def toSaveNeg(self):
        return self.output["neg"][0] == True
    
    def toSaveNpy(self):
        return self.output["npy"][0] == True

    def toSaveCsv(self):
        return self.output["csv"][0] == True

    def getInputDirec(self):
        return self.direc

    def getCsvDirec(self):
        return self.output["csv"][1]
    
    def getClipDirec(self):
        return self.output["clip"][1] if self.toSaveClip() else None
    
    def getPosDirec(self):
        return self.output["pos"][1] if self.toSavePos() else None
    
    def getNegDirec(self):
        return self.output["neg"][1] if self.toSaveNeg() else None
    
    def getNpyDirec(self):
        return self.output["npy"][1] if self.toSaveNpy() else None

    def getModelParams(self):
        return {'dim': (self.model["first"], self.model["second"]), # default: (128, 431)
                'batch_size': 1,
                'n_classes': self.model["classes"], # default: 2
                'n_channels': self.model["channels"], # default: 1
                'shuffle': False}

        