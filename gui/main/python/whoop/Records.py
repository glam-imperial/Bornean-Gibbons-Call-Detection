"""
Container/conversion classes for entries in SQL tables.

Author: Alexander Shiarella
"""


from PyQt5.QtCore import QDateTime

from .AppResources import GlobalResources as R

class StampRecord:

    def __init__(self, miliseconds, surveyDatetime, label="", note="", creationDatetime=None):
        self.miliseconds = miliseconds
        self.surveyDatetime = surveyDatetime
        if creationDatetime is None:
            self.creationDatetime = QDateTime.currentDateTime().toString(R.datetimeFormat)
        else:
            self.creationDatetime = creationDatetime
        self.label = label
        self.note = note
        print(self.creationDatetime)


    def getQSQLRecord(self, record):
        record.setValue('miliseconds', self.miliseconds)
        record.setValue('survey_datetime', self.surveyDatetime)
        record.setValue('creation_datetime', self.creationDatetime)
        record.setValue('label', self.label)
        record.setValue('note', self.note)
        return record


class SurveyRecord:

    def __init__(self,
                 surveyDatetime,
                 recorderID,
                 recordingDatetime,
                 recordingDuration,
                 audioFilePath,
                 audioURL,
                 note):
        self.surveyDatetime = surveyDatetime
        self.recorderID = recorderID
        self.recordingDatetime = recordingDatetime
        self.recordingDuration = recordingDuration
        self.audioFilePath = audioFilePath
        self.audioURL = audioURL
        self.note = note


    def getQSQLRecord(self, record):
        record.setValue('survey_datetime', self.surveyDatetime.toString(R.datetimeFormat))
        record.setValue('recorder_id', self.recorderID)
        record.setValue('recording_datetime', self.recordingDatetime.toString(R.datetimeFormat))
        record.setValue('recording_duration', self.recordingDuration)
        record.setValue('file', self.audioFilePath)
        record.setValue('url', self.audioURL)
        record.setValue('note', self.note)
        return record


    def editData(self, model, index):
        index1 = index.sibling(index.row(), 1)
        index2 = index.sibling(index.row(), 2)
        index3 = index.sibling(index.row(), 3)
        index4 = index.sibling(index.row(), 4)
        index5 = index.sibling(index.row(), 5)
        index6 = index.sibling(index.row(), 6)
        model.setData(index1, self.recorderID)
        model.setData(index2, self.recordingDatetime.toString(R.datetimeFormat))
        model.setData(index3, self.recordingDuration)
        model.setData(index4, self.audioFilePath)
        model.setData(index5, self.audioURL)
        model.setData(index6, self.note)
        model.submitAll()


    def printRecord(self):
        print(self.surveyDatetime.toString(R.datetimeFormat))
        print(self.recorderID)
        print(self.recordingDatetime.toString(R.datetimeFormat))
        print(self.recordingDuration)
        print(self.audioFilePath)
        print(self.audioURL)
        print(self.note)