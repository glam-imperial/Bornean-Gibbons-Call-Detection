'''
Helper class for sorting CSV by chunk number

TODO: replace with sorting method that includes datetime, location, etc.

Author: Alexander Shiarella
'''

import pandas as pd


class CsvSorter:

    def __init__(self, csv):
        self.csv = csv


    def sort(self):
        df = pd.read_csv(self.csv)
        df = df.rename(columns={df.columns[0]: 'Clip'})
        df['Chunk'] = df['Clip'].str.extract(r'(chunk_\d*)')
        df['Chunk'] = pd.to_numeric(df['Chunk'].map(lambda x: x.lstrip('_chunk')))
        df = df.sort_values(['Chunk'])
        df.to_csv(self.csv)