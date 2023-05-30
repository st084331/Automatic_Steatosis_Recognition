import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from application.code.FileManager import FileManager
from application.code.Init import AVERAGES
from application.code.MainWindow import MainWindow
from typing import List


class Application:

    def __init__(self):
        # print("Start Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # Deleting files left after a critical program termination
        FileManager.delete_residual_files(substr=".nii")

        # Creation of configuration files for fuzzy and most powerful criteria
        FileManager.make_config(averages=AVERAGES)

        self.app = QApplication(sys.argv)

        self.window = MainWindow()

        self.window.show()

        self.app.exec()

        # print("End Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])


if __name__ == "__main__":
    # print("Creating Application object |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
    steatosis_recognizer = Application()
