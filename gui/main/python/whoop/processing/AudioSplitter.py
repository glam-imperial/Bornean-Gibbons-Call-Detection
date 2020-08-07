'''
Author: Alexander Shiarella
'''

from pydub import AudioSegment
import os
import pandas as pd
from ..widgets.ExtractorWidget import Type as ExtractionType
import sys


class AudioSplitter:

    def __init__(self, clip_len=5000, shift_len=2500, alpha=2000, beta=0, gamma=4000, delta=6000):
        self.clip_len = clip_len
        self.shift_len = shift_len
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta


    def gen_audio_seg(self, input_file):
        extension = os.path.splitext(input_file)[1]
        if extension not in ('.mp3', '.wav', '.aac', '.m4a'): # TODO m4a
            print("Unsupported file " + input_file)
            exit(1)
        else:
            extension = extension[1:]
            audio_seg = AudioSegment.from_file(input_file, extension)
            return audio_seg


    def split(self, input_file, output_folder, aud_start=0, aud_end=None):
        audio_seg = self.gen_audio_seg(input_file)
        os.chdir(output_folder)
        if aud_end is None:
            aud_end = len(audio_seg)
        clip_start = aud_start
        clip_end = clip_start + self.clip_len
        while clip_end <= aud_end:
            clip = audio_seg[clip_start : clip_end]
            new_filename = os.path.basename(input_file)[: -4] + "_chunk_" + str(clip_start) + ".wav"
            print("Saving: ", new_filename)
            clip.export(new_filename, format='wav')
            clip_start += self.shift_len
            clip_end += self.shift_len


    def returnSplit(self, input_file, output_folder, statusSignal=None, aud_start=0, aud_end=None):
        fileList = []
        audio_seg = self.gen_audio_seg(input_file)
        os.chdir(output_folder)
        if aud_end is None:
            aud_end = len(audio_seg)

        print("____SPLIT LEN TEST____")
        print(aud_start)
        print(aud_end)
        clip_start = aud_start
        clip_end = clip_start + self.clip_len
        while clip_end <= aud_end:
            clip = audio_seg[clip_start: clip_end]
            new_filename = os.path.basename(input_file)[: -4] + "_chunk_" + str(clip_start) + ".wav"
            print("Saving: ", new_filename)
            if statusSignal != None:
                statusSignal.emit("Saving: " + new_filename)
            fullPath = os.path.join(output_folder, new_filename)
            fileList.append(fullPath)
            clip.export(new_filename, format='wav')
            clip_start += self.shift_len
            clip_end += self.shift_len
        return fileList


    def extract(self, data, type, input_file, output_folder, aud_start=0, aud_end=None):
        audio_seg = self.gen_audio_seg(input_file)
        os.chdir(output_folder)

        if aud_end is None:
            aud_end = len(audio_seg)
            print(aud_end)
        # clip_start = aud_start
        # clip_end = clip_start + self.clip_len

        # create series from column in CSV with audio filename
        filename = os.path.basename(input_file)
        # series = pd.Series(data[filename].values)
        print(data)
        series = pd.Series(data)
        series.sort_values() # todo maybe remove and use order by in SQL
        print(series)

        # for every possible clip (based on window shift) save positive clip if its postive examination window contains timestamp
        # start = 0
        # end = start + self.clip_len
        start = aud_start
        end = start + self.clip_len
        while end <= aud_end:

            clip = audio_seg[start:end]

            # define positive examination window
            pos_bottom_cutoff = start + self.alpha # 2000
            pos_top_cutoff = end - self.beta #0
            print(start)
            print(self.alpha)
            print(end)
            print(self.beta)
            print(pos_bottom_cutoff)
            print(pos_top_cutoff)

            # define negative examination window
            neg_bottom_cutoff = start - self.gamma # 4000
            neg_top_cutoff = end + self.delta # 6000

            if type == ExtractionType.POS or type == ExtractionType.BOTH:
                # save clip (as wav) if timestamp present in examination window
                temp_ser = series.between(pos_bottom_cutoff, pos_top_cutoff)
                for key, value in temp_ser.iteritems():
                    if value is True:
                        new_filename = filename[: -4] + "_chunk_" + str(start) + ".wav"
                        print("Saving: ", new_filename)
                        clip.export(new_filename, format='wav')
                        break

            if type == ExtractionType.NEG or type == ExtractionType.BOTH:
                # save clip (as wav) if timestamp not present in examination window
                temp_ser = series.between(neg_bottom_cutoff, neg_top_cutoff)
                if all(value is False for key, value in temp_ser.iteritems()):
                    new_filename = filename[: -4] + "_negchunk_" + str(start) + ".wav"
                    print("Saving: ", new_filename)
                    clip.export(new_filename, format='wav')

            start += self.shift_len
            end += self.shift_len


    @staticmethod
    def clear(output_folder):
        for filename in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, filename))


if __name__ == '__main__':
    if len(sys.argv) is 5:
        splitter = AudioSplitter(sys.argv[1], sys.argv[2])
        splitter.split(sys.argv[3], sys.argv[4])