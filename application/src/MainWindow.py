import os
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMainWindow
from application.src.CT_Handler import CT_Handler
from application.src.CheckableComboBox import CheckableComboBox
from application.src.FileManager import FileManager
from application.src.Init import AVERAGES, AREAS, METHODS
from application.src.RequestHandler import RequestHandler


class MainWindow(QMainWindow):

    def __init__(self):
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

    def handle_method_combobox(self):
        method = self.method_combobox.currentText()

        layout = QVBoxLayout()
        if method == "All":
            layout.addWidget(self.help_label)
            layout.addWidget(self.input)
            layout.addWidget(self.method_label)
            layout.addWidget(self.method_combobox)
            layout.addWidget(self.button)
            layout.addWidget(self.result_label)
        elif "regression" in method:
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

    def handle_analyse_button(self):
        folder = str(self.input.text())
        method = self.method_combobox.currentText()
        area = self.area_combobox.currentText()
        if "regression" in method:
            types_of_average = self.averages_combobox.currentData()
            relative_types_of_average = self.relative_averages_combobox.currentData()
        else:
            types_of_average = [self.average_combobox.currentText()]
            relative_types_of_average = []
        if len(types_of_average) >= 1:
            if os.path.exists(folder):

                if FileManager.check_dcm_in_folder(folder=folder, substr=".dcm"):
                    folder_struct = os.path.split(folder)
                    name_of_nifti = folder_struct[len(folder_struct) - 1]

                    values_of_brightness = RequestHandler.brightness_values_request(area=area,
                                                                                    types_of_average=types_of_average,
                                                                                    relative_types_of_average=relative_types_of_average,
                                                                                    handler=CT_Handler(folder,
                                                                                                       name_of_nifti))

                    result = f"The probability of having steatosis is {RequestHandler.result_request(values_of_brightness=values_of_brightness, types_of_average=types_of_average, relative_types_of_average=relative_types_of_average, method=method) * 100}%"

                    FileManager.remove_additional_files(name_of_nifti=name_of_nifti)
                else:
                    result = "This is not Dicom folder"

            else:
                result = "Wrong path"
        else:
            result = "You must select at least 1 type of average"

        self.result_label.setText(result)
