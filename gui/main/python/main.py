"""
Main entry-point for the application. Initializes logging, data storage, and uncaught exception handling.

Author: Alexander Shiarella
"""

import sys
import os
import logging
import traceback

from PyQt5.QtWidgets import QApplication
import qtmodern.styles

from whoop.MainWindow import MainWindow
from whoop.widgets.DatabaseDialog import DatabaseDialog
from whoop.widgets.LogWidget import LogWidget
from whoop.AppResources import baseDirec
from whoop.AppUtils import ErrorUtils


def exceptHook(exc_type, exc_value, exc_tb):
    """Handle all uncaught exceptions by logging and displaying traceback message."""
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.error("Uncaught Exception occurred. Exiting application.\n" + tb)
    ErrorUtils.showErrorDialog(text="Uncaught exception occurred. Exiting application.", info=tb)
    QApplication.quit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)  #

    # Initialize log file to be in append mode.
    logging.basicConfig(filename='app.log',
                        filemode='a',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info('New session initialized.')

    sys.excepthook = exceptHook

    # To display process info to the user.
    logWidget = LogWidget()

    # Directory needed to store intermediate files for audio processing.
    if not os.path.exists(baseDirec):
        print("Creating base app directory: " + baseDirec)
        logWidget.logItem("Creating base app directory: " + baseDirec)
        os.mkdir(baseDirec)

    # Show database selection/creation dialog.
    dialog = DatabaseDialog(logWidget)
    if dialog.exec_():
        widget = MainWindow(dialog.getDatabasePath(), logWidget)
        widget.show()
    else:
        sys.exit()

    # Required for built version but not console.
    sys.exit(app.exec_())