'''
Data generator for model.py. Returns shuffled training data in batches.
Allows for multiprocessing and prevents potential memory error from loading data in full.

Adapted code from Shervine Amidi's Stanford tutorial. I used a different version
than here for the multi-channel model.
'''

import numpy as np
import keras


class DataGenerator(keras.utils.Sequence):

    def __init__(self, list_IDs, labels, npy_folder, batch_size=32, dim=(128, 431), n_channels=1, n_classes=2, shuffle=True):
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.npy_folder = npy_folder
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()


    def __len__(self):
        return int(np.floor(len(self.list_IDs) / self.batch_size))


    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        X, y = self.__data_generation(list_IDs_temp)
        return X, y


    def on_epoch_end(self):
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)


    def __data_generation(self, list_IDs_temp):
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)
        for i, ID in enumerate(list_IDs_temp):
            X_temp = np.load(self.npy_folder + ID + '.npy')
            print("getting prediction for: " + self.npy_folder + ID + '.npy')
            X_temp = np.expand_dims(X_temp, axis=2)
            X[i,] = X_temp
            y[i] = self.labels[ID]

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

