import os
from datetime import datetime

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMainWindow
from application.code.CT_Handler import CT_Handler
from application.code.CheckableComboBox import CheckableComboBox
from application.code.FileManager import FileManager
from application.code.Init import AVERAGES, AREAS, METHODS, PARENT_FOLDER_PATH
from application.code.RequestHandler import RequestHandler


class MainWindow(QMainWindow):

    def __init__(self):

        # print("Start MainWindow __init__ |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        super().__init__()

        self.setWindowTitle("Steatosis Recognizer")

        self.result_label = QLabel()

        self.averages_label = QLabel("Select the types of average of liver (not 0)")
        self.averages_combobox = CheckableComboBox()
        self.averages_combobox.addItems(AVERAGES)

        self.relative_averages_label = QLabel("Select the types of average of whole study")
        self.relative_averages_combobox = CheckableComboBox()
        self.relative_averages_combobox.addItems(AVERAGES)

        self.method_label = QLabel("Select method")
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(METHODS)
        self.method_combobox.currentIndexChanged.connect(self.handle_method_combobox)

        self.average_label = QLabel("Select type of average")
        self.average_combobox = QComboBox()
        self.average_combobox.addItems(AVERAGES)

        self.area_label = QLabel("Select area")
        self.area_combobox = QComboBox()
        self.area_combobox.addItems(AREAS)

        self.help_label = QLabel("Enter the full path to the research folder")

        self.input = QLineEdit()

        self.button = QPushButton("Analyse")
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

        folder = str(self.input.text())
        method = self.method_combobox.currentText()
        area = self.area_combobox.currentText()

        # print(f"folder = {folder}; method = {method}; area = {area}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if "regression" in method:
            types_of_average = self.averages_combobox.currentData()
            relative_types_of_average = self.relative_averages_combobox.currentData()
        else:
            types_of_average = [self.average_combobox.currentText()]
            relative_types_of_average = []

        # print(f"types_of_average = {types_of_average}; relative_types_of_average = {relative_types_of_average}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if len(types_of_average) >= 1:
            # print("len of types_of_average >= 1 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            if os.path.exists(folder):
                # print(f"{folder} exists |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                substr = ".dcm"
                if FileManager.check_dcm_only_in_folder(folder_path=folder, substr=substr) == 1:
                    # print(f"FileManager.check_dcm_in_folder(folder={folder}, substr={substr}) is True", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                    folder_struct = os.path.split(folder)
                    # print(f"folder_struct = {folder_struct}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                    name_of_nifti_wo_extension = folder_struct[len(folder_struct) - 1]
                    # print(f"name_of_nifti_wo_extension = {name_of_nifti_wo_extension}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                    values_of_brightness = RequestHandler.brightness_values_request(area=area,
                                                                                    types_of_average=types_of_average,
                                                                                    relative_types_of_average=relative_types_of_average,
                                                                                    handler=CT_Handler(folder=folder,
                                                                                                       name_of_nifti_wo_extension=name_of_nifti_wo_extension))
                    # print(f"values_of_brightness = {values_of_brightness}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                    result = f"The probability of having steatosis is {RequestHandler.result_request(values_of_brightness=values_of_brightness, types_of_average=types_of_average, relative_types_of_average=relative_types_of_average, method=method) * 100}%"

                    FileManager.delete_residual_files(".nii", folder_path=PARENT_FOLDER_PATH)
                elif FileManager.check_dcm_only_in_folder(folder_path=folder, substr=substr) == -1:
                    result = "The folder contains not only dicom files"
                else:
                    result = "This folder is empty"

            else:
                result = "Wrong path"

        else:
            result = "You must select at least 1 type of average"

        self.result_label.setText(result)
        # print(f"End handle_analyse_button with result: {result} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
