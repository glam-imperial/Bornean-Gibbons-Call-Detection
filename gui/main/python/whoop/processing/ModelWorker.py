'''
Worker thread for making predictions on audio using a trained model.

Author: Alexander Shiarella
'''

from PyQt5.QtCore import QObject, pyqtSignal
from keras.models import load_model
from keras import backend as K
from threading import Thread
from keras import Sequential


class ModelWorker(Thread, QObject):

    modelSignal = pyqtSignal(Sequential, str)
    errorSignal = pyqtSignal(str)

    def __init__(self, modelFile):
        Thread.__init__(self)
        QObject.__init__(self)
        self.modelFile = modelFile


    @staticmethod
    def null():
        """Dummy factory for thread initialization"""
        return ModelWorker(None)


    def run(self):
        self.__initModel()


    def __initModel(self):
        K.clear_session()
        try:
            self.model = load_model(self.modelFile)
            self.model._make_predict_function()
        except Exception as e:
            self.errorSignal.emit(str(e))
            return
        print(type(self.model))
        self.modelSignal.emit(self.model, self.modelFile)
