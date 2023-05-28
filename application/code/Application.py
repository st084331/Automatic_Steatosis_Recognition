import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from application.code.FileManager import FileManager
from application.code.FormatConverter import FormatConverter
from application.code.Init import PARENT_FOLDER_PATH, AVERAGES
from application.code.MainWindow import MainWindow
from application.code.Predictor import Predictor


class Application:

    def main(self):
        # print("Start Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        FileManager.delete_residual_files(substr=".nii", folder_path=PARENT_FOLDER_PATH)

        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=AVERAGES)

        Predictor.make_config(averages=current_types)

        app = QApplication(sys.argv)

        window = MainWindow()

        window.show()

        app.exec()

        # print("End Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])


if __name__ == "__main__":
    # print("Creating Application object |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
    steatosis_recognizer = Application()

    steatosis_recognizer.main()
