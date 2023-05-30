import os
from datetime import datetime
from typing import List

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMainWindow
from application.code.CheckableComboBox import CheckableComboBox
from application.code.FileManager import FileManager
from application.code.Init import AVERAGES, AREAS, METHODS
from application.code.RequestHandler import RequestHandler


class MainWindow(QMainWindow):

    def __init__(self):

        # print("Start MainWindow __init__ |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        super().__init__()

        self.setWindowTitle("Steatosis Recognizer")

        # Here will be the result
        self.result_label = QLabel()

        # Here you can select the types of average value
        self.averages_label = QLabel("Select the types of average of liver (not 0)")
        self.averages_combobox = CheckableComboBox()
        self.averages_combobox.addItems(AVERAGES)

        # Here you can select the relative types of average value
        self.relative_averages_label = QLabel("Select the types of average of whole study")
        self.relative_averages_combobox = CheckableComboBox()
        self.relative_averages_combobox.addItems(AVERAGES)

        # Here you can select method
        self.method_label = QLabel("Select method")
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(METHODS)
        self.method_combobox.currentIndexChanged.connect(self.handle_method_combobox)

        # Here you can select the type of average value
        self.average_label = QLabel("Select type of average")
        self.average_combobox = QComboBox()
        self.average_combobox.addItems(AVERAGES)

        # Here you can select the area
        self.area_label = QLabel("Select area")
        self.area_combobox = QComboBox()
        self.area_combobox.addItems(AREAS)

        self.help_label = QLabel("Enter the full path to the research folder")

        # Here you can enter absolute path to folder
        self.input = QLineEdit()

        self.button = QPushButton("Analyse")
        # This is button to star process
        self.button.clicked.connect(self.handle_analyse_button)

        layout = QVBoxLayout()
        layout.addWidget(self.help_label)
        layout.addWidget(self.input)
        layout.addWidget(self.method_label)
        layout.addWidget(self.method_combobox)
        layout.addWidget(self.average_label)
        layout.addWidget(self.average_combobox)
        layout.addWidget(self.area_label)
        layout.addWidget(self.area_combobox)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # print("End MainWindow __init__ |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    def handle_method_combobox(self):
        # print("Start handle_method_combobox |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        method = self.method_combobox.currentText()
        # print(f"Switching to method {method} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        layout = QVBoxLayout()
        # If regression is chosen as the method, then the following widgets are needed
        if "regression" in method:
            self.area_label = QLabel("Select area")
            self.area_combobox = QComboBox()
            self.area_combobox.addItems(AREAS)

            self.averages_label = QLabel("Select the types of average of liver (not 0)")
            self.averages_combobox = CheckableComboBox()
            self.averages_combobox.addItems(AVERAGES)

            self.relative_averages_label = QLabel("Select the types of average of whole study")
            self.relative_averages_combobox = CheckableComboBox()
            self.relative_averages_combobox.addItems(AVERAGES)

            layout.addWidget(self.help_label)
            layout.addWidget(self.input)
            layout.addWidget(self.method_label)
            layout.addWidget(self.method_combobox)
            layout.addWidget(self.area_label)
            layout.addWidget(self.area_combobox)
            layout.addWidget(self.averages_label)
            layout.addWidget(self.averages_combobox)
            layout.addWidget(self.relative_averages_label)
            layout.addWidget(self.relative_averages_combobox)
            layout.addWidget(self.button)
            layout.addWidget(self.result_label)

        # If criterion is chosen as the method, then the following widgets are needed
        else:
            self.average_label = QLabel("Select type of average")
            self.average_combobox = QComboBox()
            self.average_combobox.addItems(AVERAGES)

            self.area_label = QLabel("Select area")
            self.area_combobox = QComboBox()
            self.area_combobox.addItems(AREAS)

            layout.addWidget(self.help_label)
            layout.addWidget(self.input)
            layout.addWidget(self.method_label)
            layout.addWidget(self.method_combobox)
            layout.addWidget(self.average_label)
            layout.addWidget(self.average_combobox)
            layout.addWidget(self.area_label)
            layout.addWidget(self.area_combobox)
            layout.addWidget(self.button)
            layout.addWidget(self.result_label)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # print("End handle_method_combobox |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    def handle_analyse_button(self):
        # print(f"Start handle_analyse_button |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        folder_path: str = str(self.input.text())
        method: str = self.method_combobox.currentText()
        area: str = self.area_combobox.currentText()

        # print(f"folder_path = {folder_path}; method = {method}; area = {area}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if "regression" in method:
            types_of_average: List[str] = self.averages_combobox.currentData()
            relative_types_of_average: List[str] = self.relative_averages_combobox.currentData()
        else:
            types_of_average: List[str] = [self.average_combobox.currentText()]
            relative_types_of_average = []

        # print(f"types_of_average = {types_of_average}; relative_types_of_average = {relative_types_of_average}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if len(types_of_average) >= 1:
            # print("len of types_of_average >= 1 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            if os.path.exists(folder_path):
                # print(f"{folder} exists |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                substr: str = ".dcm"
                if FileManager.check_dcm_only_in_folder(folder_path=folder_path, substr=substr) == 1:
                    # print(f"FileManager.check_dcm_in_folder(folder={folder}, substr={substr}) is True", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                    result = f"The probability of having steatosis is {round(RequestHandler.result_request(area=area, types_of_average=types_of_average, relative_types_of_average=relative_types_of_average, method=method, folder_path=folder_path), 2) * 100}%"

                    FileManager.delete_residual_files(".nii")
                elif FileManager.check_dcm_only_in_folder(folder_path=folder_path, substr=substr) == -1:
                    result = "The folder contains not only dicom files"
                else:
                    result = "This folder is empty"

            else:
                result = "Wrong path"

        else:
            result = "You must select at least 1 type of average"

        self.result_label.setText(result)
        # print(f"End handle_analyse_button with result: {result} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
