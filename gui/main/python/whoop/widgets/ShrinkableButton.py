import re

from PyQt5.QtWidgets import QPushButton

class ShrinkableButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)
        # self.text = text
        width = self.fontMetrics().boundingRect(re.sub('&(?=(?:&&)*[^&])', '', text)).width() + 10
        self.setMinimumWidth(width)