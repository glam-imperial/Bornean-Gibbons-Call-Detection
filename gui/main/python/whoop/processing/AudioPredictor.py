'''
Class for making predictions from spectrograms using given model.

TODO: fix sorting

Author: Alexander Shiarella
'''

import os
import numpy as np
import pandas as pd
import pickle
from .Generator import DataGenerator
from whoop.processing.StoppableGenerator import StoppableDataGenerator


class AudioPredictor:

    def __init__(self, model_file, model_params, npy_folder, model):
        self.model = model
        self.model_params = model_params
        self.npy_folder = npy_folder


    def predictSaved(self, dict_folder, csv_file="", saveCsv=True):
        # load dictionary with test/validation/raw partition
        with open(os.path.join(dict_folder, 'partition_dict.pkl'), 'rb') as input_file:
            partition = pickle.load(input_file)

        # load dictionary with labels
        with open(os.path.join(dict_folder, 'labels_dict.pkl'), 'rb') as input_file:
            labels = pickle.load(input_file)

        # use the raw partition
        ID_list = partition['raw']

        # create custom data generator object for model - see generator.py
        validation_generator = DataGenerator(partition['raw'], labels, self.npy_folder, **self.model_params)

        # get predictions using generator
        predictions = self.model.predict_generator(validation_generator)

        # match predictions with IDs and save CSV with results
        results = {}
        for i, id in enumerate(ID_list):
            results[id] = np.append(predictions[i], int(np.argmax(predictions[i])))

        data_frame = pd.DataFrame.from_dict(results, orient='index', columns=['X', 'Y', 'Label'])


    def predict(self, labels, partition, csv_file="", saveCsv=True):
        # use the raw partition
        ID_list = partition['raw']

        # create custom data generator object for model - see generator.py
        validation_generator = DataGenerator(partition['raw'], labels, self.npy_folder, **self.model_params)

        # get predictions using generator
        predictions = self.model.predict_generator(validation_generator)

        # match predicitions with IDs and save CSV with results
        results = {}
        for i, id in enumerate(ID_list):
            results[id] = np.append(predictions[i], int(np.argmax(predictions[i])))

        data_frame = pd.DataFrame.from_dict(results, orient='index', columns=['X', 'Y', 'Label'])

        if saveCsv:
            # TODO check valid file path?
            print("saving: " + csv_file)
            data_frame.to_csv(csv_file)


    def predictReturnDict(self, labels, partition, csv_file="", saveCsv=True, threshold=0.5):
        print(partition)
        # use the raw partition
        ID_list = partition['raw']

        # create custom data generator object for model - see generator.py
        validation_generator = DataGenerator(partition['raw'], labels, self.npy_folder, **self.model_params)

        # get predictions using generator
        predictions = self.model.predict_generator(validation_generator)

        # match predicitions with IDs and save CSV with results
        results = {}
        for i, id in enumerate(ID_list):
            # results[id] = np.append(predictions[i], int(np.argmax(predictions[i])))
            results[id] = np.append(predictions[i], int(predictions[i][1] > threshold))

        if saveCsv:
            print('to dataframe...')
            data_frame = pd.DataFrame.from_dict(results, orient='index', columns=['X', 'Y', 'Label'])

            # TODO check valid file path?
            print("saving: " + csv_file)
            data_frame.to_csv(csv_file)

        return results


    def stoppablePredictReturnDict(self, labels, partition, killEvent, csv_file="", saveCsv=True, threshold=0.5):
        print(partition)
        # use the raw partition
        ID_list = partition['raw']

        # create custom data generator object for model - see generator.py
        validation_generator = StoppableDataGenerator(partition['raw'], labels, self.npy_folder, killEvent, **self.model_params)

        # get predictions using generator
        predictions = self.model.predict_generator(validation_generator)

        # match predicitions with IDs and save CSV with results
        results = {}
        for i, id in enumerate(ID_list):
            if killEvent.is_set():
                print("Kill event - returning halting prediction")
                return
            # results[id] = np.append(predictions[i], int(np.argmax(predictions[i])))
            results[id] = np.append(predictions[i], int(predictions[i][1] > threshold))

        if saveCsv:
            print('to dataframe...')

            if killEvent.is_set():
                print("Kill event - returning halting prediction")
                return

            data_frame = pd.DataFrame.from_dict(results, orient='index', columns=['X', 'Y', 'Label'])

            # TODO check valid file path?
            print("saving: " + csv_file)
            data_frame.to_csv(csv_file)

        return results
