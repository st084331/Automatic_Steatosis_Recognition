import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from application.src.FileManager import FileManager
from application.src.MainWindow import MainWindow
from application.src.Predictor import Predictor


class Application:

    def main(self):
        # print("Start Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Call FileManager.delete_residual_files(substr=\".nii\") |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        FileManager.delete_residual_files(substr=".nii")

        # print("Call Predictor.make_config() |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        Predictor.make_config()

        # print("Call init of QApplication(sys.argv) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        app = QApplication(sys.argv)

        # print("Call init of MainWindow |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        window = MainWindow()

        # print("Call window.show() |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        window.show()

        # print("Call app.exec() |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        app.exec()

        # print("End Application main()", datetime.now().strftime("%H:%M:%S.%f")[:-3])


if __name__ == "__main__":
    # print("Creating Application object |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
    steatosis_recognizer = Application()

    # print("Call steatosis_recognizer.main() |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
    steatosis_recognizer.main()
