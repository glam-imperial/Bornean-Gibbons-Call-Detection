'''
Converts audio to spectrograms.

Author: Alexander Shiarella
'''

import librosa
import os
import numpy as np
import pickle


class AudioConverter:

    NO_VAL = 1

    def __init__(self,
                 sample_rate=44100,
                 f_min=200,
                 f_max=2000,
                 mean_sub=True,
                 n_fft=2048,
                 power=2.0,
                 hop_length=512):
        self.sample_rate = sample_rate
        self.f_min = f_min
        self.f_max = f_max
        self.mean_sub = mean_sub
        self.n_fft = n_fft
        self.power = power
        self.hop_length = hop_length


    '''
    Convert wav clip to spectrogram
    '''
    def convert_wav_to_melspec(self, wav_file, type='powmel'):

        wav, sr = librosa.load(wav_file, mono=True, sr=self.sample_rate)

        if type is 'stft':
            stft = librosa.core.stft(y=wav,
                                     n_fft=self.n_fft,
                                     hop_length=self.hop_length)
            stft = librosa.amplitude_to_db(stft, ref=np.max)
            return stft

        try:
            mel_spec = librosa.feature.melspectrogram(y=wav,
                                                      sr=self.sample_rate,
                                                      fmin=self.f_min,
                                                      fmax=self.f_max,
                                                      power=self.power,
                                                      n_fft=self.n_fft,
                                                      hop_length=self.hop_length)
        except Exception as e:
            print("error: " + e)

        if type is 'melspec':
            spectrogram = mel_spec

        elif type is 'powsq':
            spectrogram = librosa.amplitude_to_db(mel_spec, ref=np.max)

        else:  # type is 'powmel':
            spectrogram = librosa.power_to_db(mel_spec, ref=np.max)

        if self.mean_sub is True:
            spectrogram -= (np.mean(spectrogram, axis=0) + 1e-8)

        return spectrogram


    '''
    Convert wav to MFCC with specified parameters
    '''
    def convert_wav_to_mfcc(self, wav_file):

        wav, sr = librosa.load(wav_file, mono=True, sr=self.sample_rate)

        mfcc = librosa.feature.mfcc(y=wav,
                                    sr=self.sample_rate,
                                    fmin=self.f_min,
                                    fmax=self.f_max,
                                    power=self.power,
                                    n_fft=self.n_fft,
                                    hop_length=self.hop_length)

        if self.mean_sub is True:
            mfcc -= (np.mean(mfcc, axis=0) + 1e-8)

        return mfcc


    '''
    Save all .wav files in aud_folder as .npy spectrograms
    Returns: list of names (should be unique if filenames unique)
             labels dictionary with {name: value}
    '''
    def save_npy(self, aud_folder, npy_folder, value):
        labels = {}
        name_list = []
        for filename in os.listdir(aud_folder):
            if filename.endswith(".wav"):
                full_path_wav = os.path.join(aud_folder, filename)
                print('filename: ', filename)  # TODO: remove (for testing)

                no_ext_name = os.path.splitext(filename)[0]

                numpy_spec_path = os.path.join(npy_folder, no_ext_name + '.npy')
                print('numpy file: ', numpy_spec_path)  # TODO: remove (for testing)

                name_list.append(no_ext_name)

                labels[no_ext_name] = value

                spec = self.convert_wav_to_melspec(wav_file=full_path_wav)
                np.save(numpy_spec_path, spec)

        return name_list, labels

    def saveNpy(self, clipList, npy_folder, value):
        labels = {}
        name_list = []
        for full_path_wav in clipList:
            filename = os.path.basename(full_path_wav)
            filename = os.path.basename(full_path_wav)
            if filename.endswith(".wav"):
                # full_path_wav = os.path.join(aud_folder, filename)
                print('filename: ', filename)  # TODO: remove (for testing)

                no_ext_name = os.path.splitext(filename)[0]

                numpy_spec_path = os.path.join(npy_folder, no_ext_name + '.npy')
                print('numpy file: ', numpy_spec_path)  # TODO: remove (for testing)

                name_list.append(no_ext_name)

                labels[no_ext_name] = value

                print(full_path_wav)
                spec = self.convert_wav_to_melspec(wav_file=full_path_wav)

                np.save(numpy_spec_path, spec)

        return name_list, labels


    '''
    Method for processing unlabled data in bulk
    '''
    def process_raw(self, aud_folder, npy_folder, dict_folder):
        print("Converting audio from: ", aud_folder)
        list, raw_labels = self.save_npy(aud_folder, npy_folder, self.NO_VAL)
        partition = {}
        partition['raw'] = list
        partition_dict_path = os.path.join(dict_folder, 'partition_dict.pkl')
        print("Saving raw partition dictionary: ", partition_dict_path)
        with open(partition_dict_path, 'wb') as output_file:
            pickle.dump(partition, file=output_file)

        labels = {}
        labels.update(raw_labels)
        labels_dict_path = os.path.join(dict_folder, 'labels_dict.pkl')
        print("Saving labels dictionary: ", labels_dict_path)
        with open(labels_dict_path, 'wb') as output_file:
            pickle.dump(labels, file=output_file)

    '''
        Method for processing unlabled data in bulk
    '''
    def processList(self, clipList, npy_folder, dict_folder):
        print("Converting audio from list")
        list, raw_labels = self.saveNpy(clipList, npy_folder, self.NO_VAL)
        partition = {}
        partition['raw'] = list
        partition_dict_path = os.path.join(dict_folder, 'partition_dict.pkl')
        print("Saving raw partition dictionary: ", partition_dict_path)
        with open(partition_dict_path, 'wb') as output_file:
            pickle.dump(partition, file=output_file)

        labels = {}
        labels.update(raw_labels)
        labels_dict_path = os.path.join(dict_folder, 'labels_dict.pkl')
        print("Saving labels dictionary: ", labels_dict_path)
        with open(labels_dict_path, 'wb') as output_file:
            pickle.dump(labels, file=output_file)


    '''
    Method for processing unlabled data in bulk
    '''
    def processListReturn(self, clipList, npy_folder):
        print("Converting audio from list")
        list, raw_labels = self.saveNpy(clipList, npy_folder, self.NO_VAL)
        partition = {}
        partition['raw'] = list

        labels = {}
        labels.update(raw_labels)

        return labels, partition

    @staticmethod
    def clear(aud_folder):
        for filename in os.listdir(aud_folder):
            os.remove(os.path.join(aud_folder, filename))