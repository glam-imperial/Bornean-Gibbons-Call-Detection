"""
Application resources.
TODO complete String externalization for other classes and remove unused.

Author: Alexander Shiarella
"""

import os
from pathlib import Path


baseDirec = os.path.join(Path(__file__).parent.parent.parent, "app_data")


class GlobalResources:
    datetimeFormat = "yyyy-MM-dd hh:mm:ss.zzz"


class MediaPlayerResources:
    title = "Audio Player"
    height = 500
    width = 1000
    initVolume = 75
    timeLabelWidth = 100
    playButtonText = "play" # todo change to icons
    pauseButtonText = "pause"
    stopButtonText = "stop"
    previousButtonText = "previous"
    nextButtonText = "next"
    removeButtonText = "remove"
    initTimeLabel = "0:00 (0 ms)"
    initTotalTimeLabel = "N/A"


class SurveyTableResources:
    tableName = "survey"
    title = "Survey Table"
    height = 500
    width = 1000
    buttonBoxLabelText = "Survey Tools:"
    addSurveyButtonText = "Add"
    editSurveyButtonText = "Edit"
    deleteSurveyButtonText = "Delete"
    loadAudioButtonText = "Load Audio"
    combineButtonText = "Combine"
    datetimeFormat = GlobalResources.datetimeFormat

class StampTableResources:
    height = 500
    width = 1000
    tableName = "annotation"


class AudioResources:
    allowedExt = (".mp3", ".m4a", ".aac", ".wav")


class SQLResources:
    dbType = "QSQLITE"
    createSurveyTable = '''CREATE TABLE survey(
                           survey_datetime TEXT NOT NULL,
                           recorder_id TEXT,
                           recording_datetime TEXT,
                           recording_duration TEXT,
                           file TEXT,
                           url TEXT,
                           note TEXT,
                           PRIMARY KEY(survey_datetime)
                        );'''

    createAnnotationTable = '''CREATE TABLE annotation(
                               miliseconds INT NOT NULL,
                               survey_datetime TEXT NOT NULL,
                               creation_datetime TEXT NOT NULL,
                               label TEXT,
                               note TEXT,
                               PRIMARY KEY(survey_datetime, creation_datetime)
                               FOREIGN KEY(survey_datetime) REFERENCES survey(survey_datetime)
                            );'''
