"""
Application enums.

Author: Alexander Shiarella
"""

from enum import IntEnum, unique


@unique
class AudioSource(IntEnum):
    SELECTED = 0   # Single audio file selected in MediaPlayerWidget.
    ALL = 1        # All audio loaded into MediaPlayerWidget.
    DIREC = 2      # All audio in designated file directory.
    NONE = -1


@unique
class AudioInputType(IntEnum):
    FULL = 0       # Process full audio file(s).
    CLIP = 1       # Process clips already extracted from audio (skip splitting).
    NONE = -1


@unique
class ScreenMode(IntEnum):
    ALL = -1       # All widgets.
    EDIT = 0
    SURVEY = 1
    EXTRACT = 2
    PROCESS = 3
    PREPARE = 4
    TRAIN = 5