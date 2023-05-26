
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from application.src.FileManager import FileManager
from application.src.MainWindow import MainWindow
from application.src.Predictor import Predictor


class Application:

    def main(self):
        print("Start Application().main() |", datetime.now().strftime("%H:%M:%S"))
        FileManager.delete_residual_files(substr=".nii")
        Predictor.make_config()
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()

if __name__ == "__main__":
    steatosis_recognizer = Application()
    steatosis_recognizer.main()
