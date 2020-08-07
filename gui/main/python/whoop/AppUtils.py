"""
Application utilities.

Author: Alexander Shiarella
"""

from PyQt5.QtWidgets import QMessageBox


def hhmmss(ms):
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d (%d ms)" % (h, m, s, ms)) if h else ("%d:%02d (%d ms)" % (m, s, ms))


class ErrorUtils:

    def showErrorDialog(icon=QMessageBox.Critical,
                        text="",
                        info="",
                        title="Error",
                        buttons=QMessageBox.Ok,
                        parent=None):
        message = QMessageBox(parent)
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle(title)
        message.setText(text)
        message.setInformativeText(info)
        message.setStandardButtons(buttons)
        message.exec_()