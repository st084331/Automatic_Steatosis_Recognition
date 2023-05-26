import math
import os
import random
import sys
import nibabel as nib
import statistics

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, \
    QStyledItemDelegate, qApp
import csv
import dicom2nifti
import dicom2nifti.settings as settings
import sklearn
import sklearn.metrics
import json
import torch as torch
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import livermask.livermask

METHODS = ["Fuzzy criterion", "Most powerful criterion", "Linear regression", "Second degree polynomial regression"]
AREAS = ["Whole liver", "Three random areas", "Two random areas", "One random area", "100 random points"]
AVERAGES = ["Median", "Mode", "Mean", "Median low", "Median high", "Median grouped", "First quartile", 'Third quartile']

VESSELS = False
VERBOSE = False
CPU = True
if torch.cuda.is_available():
    CPU = False
settings.disable_validate_slice_increment()


class CheckableComboBox(QComboBox):
    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res


class Application:

    def main(self):
        FileManager.delete_residual_files(substr=".nii")
        Predictor.make_config()
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()


class FormatConverter:

    @staticmethod
    def types_of_average_to_current_types(types_of_average):
        current_types = []
        for type_of_average in types_of_average:
            if type_of_average == "Median":
                current_type = "median"
            elif type_of_average == "Mode":
                current_type = "mode"
            elif type_of_average == "Mean":
                current_type = "mean"
            elif type_of_average == "Median low":
                current_type = "median_low"
            elif type_of_average == "Median high":
                current_type = "median_high"
            elif type_of_average == "Median grouped":
                current_type = "median_grouped"
            elif type_of_average == "First quartile":
                current_type = "1"
            elif type_of_average == "Third quartile":
                current_type = "3"
            else:
                raise Exception(f"{type_of_average} type of average is not defined")
            current_types.append(current_type)

        print(f"types_of_average_to_current_types: from {types_of_average} to {current_types}")
        return current_types


class FileManager:

    @staticmethod
    def load_full_img_brightness_data():
        full_img_brightness_data = []
        with open(os.path.join(".", 'data', 'full_brightness' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_img_brightness_data.append(row)
        return full_img_brightness_data

    @staticmethod
    def load_whole_liver_brightness_data():
        brightness_data_wo_quantiles = []
        with open(os.path.join(".", 'data', 'whole_liver' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_wo_quantiles.append(row)

        brightness_data_quantiles = []
        with open(os.path.join(".", 'data', 'whole_liver_quantiles' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_quantiles.append(row)

        whole_liver_brightness_data = []
        for i in range(len(brightness_data_wo_quantiles)):
            whole_liver_brightness_data.append({**brightness_data_wo_quantiles[i], **brightness_data_quantiles[i]})

        return whole_liver_brightness_data

    @staticmethod
    def load_test_data():
        train = []
        train_csv = os.path.join(".", "data", "train.csv")
        with open(train_csv) as f:
            reader = csv.DictReader(f)
            for row in reader:
                train.append(row)
        return train

    @staticmethod
    def load_mask_image(name_of_nifti):
        return nib.load(os.path.join(".", name_of_nifti + "-livermask2.nii"))

    @staticmethod
    def load_original_image(name_of_nifti):
        return nib.load(os.path.join(".", name_of_nifti + ".nii"))

    @staticmethod
    def load_data_for_fuzzy_criterion(type_of_average):
        with open(os.path.join('config', 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            sick_intersection = json.load(f)

        with open(os.path.join('config', 'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            healthy_intersection = json.load(f)

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average):
        file = open(os.path.join('config', 'most_powerful_criterion_train_' + type_of_average + '.txt'), "r")
        return float(file.read())

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection, healthy_in_intersection, type_of_average):
        if not os.path.exists("config"):
            os.mkdir("config")

        with open(os.path.join('config', 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                  'w') as f:
            json.dump(sick_in_intersection, f)

        with open(os.path.join('config', 'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'w') as f:
            json.dump(healthy_in_intersection, f)

    @staticmethod
    def save_data_for_most_powerful_criterion(border_point, type_of_average):
        if not os.path.exists("config"):
            os.mkdir("config")

        with open(os.path.join('config', 'most_powerful_criterion_train_' + type_of_average + '.txt'), 'w') as f:
            f.write(str(border_point))

    @staticmethod
    def remove_additional_files(name_of_nifti):
        os.remove(name_of_nifti + ".nii")
        os.remove(name_of_nifti + "-livermask2.nii")

    @staticmethod
    def delete_residual_files(substr):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for file in files:
            if substr in file:
                os.remove(file)

    @staticmethod
    def check_dcm_in_folder(folder, substr):
        files_in_folder = os.listdir(folder)
        for file in files_in_folder:
            if substr in file:
                return True
        return False


class RequestHandler:

    @staticmethod
    def result_request(values_of_brightness, types_of_average, relative_types_of_average, method):

        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=types_of_average)
        relative_current_types = FormatConverter.types_of_average_to_current_types(
            types_of_average=relative_types_of_average)
        if method == "Fuzzy criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    return Predictor.fuzzy_criterion(value_of_brightness=values_of_brightness[0],
                                                     type_of_average=current_types[0])
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Most powerful criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    return Predictor.most_powerful_criterion(value_of_brightness=values_of_brightness[0],
                                                             type_of_average=current_types[0])
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Linear regression":
            if len(values_of_brightness) >= 1:
                if len(types_of_average) >= 1:
                    return Predictor.linear_regression(values_of_brightness=values_of_brightness,
                                                       types_of_average=current_types,
                                                       relative_types_of_average=relative_current_types)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Second degree polynomial regression":
            if len(values_of_brightness) >= 1:
                if len(types_of_average) >= 1:
                    return Predictor.polynomial_regression(values_of_brightness=values_of_brightness,
                                                           types_of_average=current_types,
                                                           relative_types_of_average=relative_current_types, degree=2)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        else:
            raise Exception(f"{method} method is not defined")

    @staticmethod
    def brightness_values_request(area, types_of_average, relative_types_of_average, handler):

        if area == "Whole liver":
            brightness_list = handler.whole_liver_brightness_info()
        elif area == "Three random areas":
            brightness_list = handler.three_areas_brightness_info()
        elif area == "Two random areas":
            brightness_list = handler.two_areas_brightness_info()
        elif area == "One random area":
            brightness_list = handler.one_area_brightness_info()
        elif area == "100 random points":
            brightness_list = handler.random_points_brightness_info()
        else:
            raise Exception(f"{area} area is not defined")

        brightness_values = []
        for type_of_average in types_of_average:
            if type_of_average == "Median":
                brightness_values.append(statistics.median(brightness_list))
            elif type_of_average == "Median grouped":
                brightness_values.append(statistics.median_grouped(brightness_list))
            elif type_of_average == "Median low":
                brightness_values.append(statistics.median_low(brightness_list))
            elif type_of_average == "Median high":
                brightness_values.append(statistics.median_high(brightness_list))
            elif type_of_average == "First quartile":
                brightness_values.append(statistics.quantiles(brightness_list)[0])
            elif type_of_average == "Third quartile":
                brightness_values.append(statistics.quantiles(brightness_list)[2])
            elif type_of_average == "Mode":
                brightness_values.append(statistics.mode(brightness_list))
            elif type_of_average == "Mean":
                brightness_values.append(statistics.mean(brightness_list))
            else:
                raise Exception(f"{type_of_average} type of average is not defined")

        if len(relative_types_of_average) > 0:
            relative_brightness_list = handler.full_img_brightness_info()
            for type_of_average in relative_types_of_average:
                if type_of_average == "Median":
                    brightness_values.append(statistics.median(relative_brightness_list))
                elif type_of_average == "Median grouped":
                    brightness_values.append(statistics.median_grouped(relative_brightness_list))
                elif type_of_average == "Median low":
                    brightness_values.append(statistics.median_low(relative_brightness_list))
                elif type_of_average == "Median high":
                    brightness_values.append(statistics.median_high(relative_brightness_list))
                elif type_of_average == "First quartile":
                    brightness_values.append(statistics.quantiles(relative_brightness_list)[0])
                elif type_of_average == "Third quartile":
                    brightness_values.append(statistics.quantiles(relative_brightness_list)[2])
                elif type_of_average == "Mode":
                    brightness_values.append(statistics.mode(relative_brightness_list))
                elif type_of_average == "Mean":
                    brightness_values.append(statistics.mean(relative_brightness_list))
                else:
                    raise Exception(f"{type_of_average} type of average is not defined")

        return brightness_values


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


class CT_Handler:

    def __init__(self, folder, name_of_nifti):
        self.folder = folder
        self.name_of_nifti = name_of_nifti
        self.dicom_to_nifti()
        self.make_mask()

    def dicom_to_nifti(self):
        dicom2nifti.dicom_series_to_nifti(self.folder, os.path.join('.', self.name_of_nifti + ".nii"),
                                          reorient_nifti=False)

    def make_mask(self):
        livermask.livermask.func(os.path.abspath(self.name_of_nifti + ".nii"),
                                 os.path.abspath(self.name_of_nifti),
                                 CPU, VERBOSE, VESSELS)

    def full_img_brightness_info(self):
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        full_data = full_img.get_fdata()

        full_img_brightness = []

        for z in range(0, full_data.shape[0], 2):
            for y in range(0, full_data.shape[1], 2):
                for x in range(0, full_data.shape[2], 2):
                    full_img_brightness.append(full_data[z][y][x])

        return full_img_brightness

    def whole_liver_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()

        whole_liver_list_of_brightness = []
        for z in range(0, mask_data.shape[0], 2):
            for y in range(0, mask_data.shape[1], 2):
                for x in range(0, mask_data.shape[2], 2):
                    if mask_data[z][y][x] == 1:
                        whole_liver_list_of_brightness.append(full_data[z][y][x])

        return whole_liver_list_of_brightness

    def three_areas_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
        three_areas_brightness = []
        for i in range(3):
            rand_z = random.randint(0, mask_data.shape[0] - 1)
            rand_y = random.randint(0, mask_data.shape[1] - 1)
            rand_x = random.randint(0, mask_data.shape[2] - 1)
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = random.randint(0, mask_data.shape[0] - 1)
                rand_y = random.randint(0, mask_data.shape[1] - 1)
                rand_x = random.randint(0, mask_data.shape[2] - 1)

            min_z = int(rand_z - diameter / 2)
            if min_z < 0:
                min_z = 0
            max_z = int(rand_z + diameter / 2)
            if max_z > mask_data.shape[0]:
                max_z = mask_data.shape[0]

            min_y = int(rand_y - diameter / 2)
            if min_y < 0:
                min_y = 0
            max_y = int(rand_y + diameter / 2)
            if max_y > mask_data.shape[1]:
                max_y = mask_data.shape[1]

            min_x = int(rand_x - diameter / 2)
            if min_x < 0:
                min_x = 0
            max_x = int(rand_x + diameter / 2)
            if max_x > mask_data.shape[2]:
                max_x = mask_data.shape[2]

            for z in range(min_z, max_z):
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        if mask_data[z][y][x] == 1:
                            three_areas_brightness.append(full_data[z][y][x])

        return three_areas_brightness

    def two_areas_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
        two_areas_brightness = []
        for i in range(2):
            rand_z = random.randint(0, mask_data.shape[0] - 1)
            rand_y = random.randint(0, mask_data.shape[1] - 1)
            rand_x = random.randint(0, mask_data.shape[2] - 1)
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = random.randint(0, mask_data.shape[0] - 1)
                rand_y = random.randint(0, mask_data.shape[1] - 1)
                rand_x = random.randint(0, mask_data.shape[2] - 1)

            min_z = int(rand_z - diameter / 2)
            if min_z < 0:
                min_z = 0
            max_z = int(rand_z + diameter / 2)
            if max_z > mask_data.shape[0]:
                max_z = mask_data.shape[0]

            min_y = int(rand_y - diameter / 2)
            if min_y < 0:
                min_y = 0
            max_y = int(rand_y + diameter / 2)
            if max_y > mask_data.shape[1]:
                max_y = mask_data.shape[1]

            min_x = int(rand_x - diameter / 2)
            if min_x < 0:
                min_x = 0
            max_x = int(rand_x + diameter / 2)
            if max_x > mask_data.shape[2]:
                max_x = mask_data.shape[2]

            for z in range(min_z, max_z):
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        if mask_data[z][y][x] == 1:
                            two_areas_brightness.append(full_data[z][y][x])

        return two_areas_brightness

    def one_area_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
        one_area_brightness = []
        rand_z = random.randint(0, mask_data.shape[0] - 1)
        rand_y = random.randint(0, mask_data.shape[1] - 1)
        rand_x = random.randint(0, mask_data.shape[2] - 1)
        while mask_data[rand_z][rand_y][rand_x] != 1:
            rand_z = random.randint(0, mask_data.shape[0] - 1)
            rand_y = random.randint(0, mask_data.shape[1] - 1)
            rand_x = random.randint(0, mask_data.shape[2] - 1)

        min_z = int(rand_z - diameter / 2)
        if min_z < 0:
            min_z = 0
        max_z = int(rand_z + diameter / 2)
        if max_z > mask_data.shape[0]:
            max_z = mask_data.shape[0]

        min_y = int(rand_y - diameter / 2)
        if min_y < 0:
            min_y = 0
        max_y = int(rand_y + diameter / 2)
        if max_y > mask_data.shape[1]:
            max_y = mask_data.shape[1]

        min_x = int(rand_x - diameter / 2)
        if min_x < 0:
            min_x = 0
        max_x = int(rand_x + diameter / 2)
        if max_x > mask_data.shape[2]:
            max_x = mask_data.shape[2]

        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    if mask_data[z][y][x] == 1:
                        one_area_brightness.append(full_data[z][y][x])

        return one_area_brightness

    def random_points_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        random_points_brightness = []
        for i in range(100):
            rand_z = random.randint(0, mask_data.shape[0] - 1)
            rand_y = random.randint(0, mask_data.shape[1] - 1)
            rand_x = random.randint(0, mask_data.shape[2] - 1)
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = random.randint(0, mask_data.shape[0] - 1)
                rand_y = random.randint(0, mask_data.shape[1] - 1)
                rand_x = random.randint(0, mask_data.shape[2] - 1)
            random_points_brightness.append(full_data[rand_z][rand_y][rand_x])
        return random_points_brightness


class Predictor:

    @staticmethod
    def make_config():
        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=AVERAGES)
        for type in current_types:
            Predictor.most_powerful_criterion_train(type)
            Predictor.fuzzy_criterion_train(type)

    @staticmethod
    def fuzzy_criterion_train(type_of_average):

        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        brightness_of_sick_patients = []
        brightness_of_healthy_patients = []
        for bd in whole_liver_brightness_data:
            for t in train:
                if bd['nii'] == t['nii']:
                    if float(t['ground_truth']) == 0.0:
                        brightness_of_healthy_patients.append(float(bd[type_of_average]))
                    else:
                        brightness_of_sick_patients.append(float(bd[type_of_average]))
                    break

        intersection_max_point = max(brightness_of_sick_patients)
        intersection_min_point = min(brightness_of_healthy_patients)

        healthy_in_intersection = []
        for brightness in brightness_of_healthy_patients:
            if brightness < intersection_max_point:
                healthy_in_intersection.append(brightness)

        sick_in_intersection = []
        for brightness in brightness_of_sick_patients:
            if brightness > intersection_min_point:
                sick_in_intersection.append(brightness)

        FileManager.save_data_for_fuzzy_criterion(sick_in_intersection=sick_in_intersection,
                                                  healthy_in_intersection=healthy_in_intersection,
                                                  type_of_average=type_of_average)

    @staticmethod
    def most_powerful_criterion_train(type_of_average):
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        brightness = []
        y = []
        for bd in whole_liver_brightness_data:
            for t in train:
                if bd['nii'] == t['nii']:
                    brightness.append(float(bd[type_of_average]))
                    y.append(int(float(t['ground_truth'])))

        max_point = max(brightness)
        min_point = min(brightness)
        border_point = (max_point + min_point) / 2

        y_pred_init = []

        for bd in whole_liver_brightness_data:
            for t in train:
                if bd['nii'] == t['nii']:
                    if float(bd[type_of_average]) <= border_point:
                        y_pred_init.append(1)
                    else:
                        y_pred_init.append(0)
                    break

        score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
        leftmost_best_score = 0.0
        leftmost_point = border_point
        step = 0.1

        while leftmost_best_score <= score:

            leftmost_best_score = score
            point1 = leftmost_point - step

            y_pred1 = []

            for bd in whole_liver_brightness_data:
                for t in train:
                    if bd['nii'] == t['nii']:
                        if float(bd[type_of_average]) <= point1:
                            y_pred1.append(1)
                        else:
                            y_pred1.append(0)

            score1 = math.fabs(sklearn.metrics.f1_score(y, y_pred1))

            if score1 >= score:
                score = score1
                leftmost_point = point1
            else:
                break

        border_point = (max_point + min_point) / 2
        score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
        rightmost_best_score = 0.0
        rightmost_point = border_point

        while rightmost_best_score <= score:

            rightmost_best_score = score
            point2 = rightmost_point + step

            y_pred2 = []

            for bd in whole_liver_brightness_data:
                for t in train:
                    if bd['nii'] == t['nii']:
                        if float(bd[type_of_average]) <= point2:
                            y_pred2.append(1)
                        else:
                            y_pred2.append(0)

            score2 = math.fabs(sklearn.metrics.f1_score(y, y_pred2))

            if score2 >= score:
                score = score2
                rightmost_point = point2
            else:
                break

        if rightmost_best_score >= leftmost_best_score:
            border_point = rightmost_point
        else:
            border_point = leftmost_point

        FileManager.save_data_for_most_powerful_criterion(border_point=border_point, type_of_average=type_of_average)

    @staticmethod
    def most_powerful_criterion(value_of_brightness, type_of_average):

        if float(value_of_brightness) <= FileManager.load_data_for_most_powerful_criterion(
                type_of_average=type_of_average):
            return 1.0
        else:
            return 0.0

    @staticmethod
    def fuzzy_criterion(value_of_brightness, type_of_average):

        sick_intersection, healthy_intersection = FileManager.load_data_for_fuzzy_criterion(type_of_average)

        intersection = []
        for elem in sick_intersection:
            intersection.append([1, float(elem)])
        for elem in healthy_intersection:
            intersection.append([0, float(elem)])

        intersection_max_point = max(sick_intersection)
        intersection_min_point = min(healthy_intersection)

        if value_of_brightness >= intersection_max_point:
            prediction = 0.0
        elif value_of_brightness <= intersection_min_point:
            prediction = 1.0
        else:
            sick_counter = 0
            for inter in intersection:
                if inter[1] >= value_of_brightness and inter[0] == 1:
                    sick_counter += 1
            prediction = sick_counter / len(intersection)

        return prediction

    @staticmethod
    def linear_regression(values_of_brightness, types_of_average, relative_types_of_average):

        full_img_brightness_data = FileManager.load_full_img_brightness_data()
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        X = []
        y = []
        for t in train:
            for i in range(len(whole_liver_brightness_data)):
                if t['nii'] == whole_liver_brightness_data[i]['nii'] and t['nii'] == \
                        full_img_brightness_data[i]['nii']:
                    row = []
                    for k in range(len(types_of_average)):
                        row.append(float(whole_liver_brightness_data[i][types_of_average[k]]))
                    for k in range(len(relative_types_of_average)):
                        row.append(float(full_img_brightness_data[i][relative_types_of_average[k]]))
                    X.append(row)
                    y.append(float(t['ground_truth']))
                    break

        reg = LinearRegression().fit(X, y)

        y_pred = reg.predict([values_of_brightness])

        print("y_pred", y_pred)

        return y_pred[0]

    @staticmethod
    def polynomial_regression(values_of_brightness, types_of_average, relative_types_of_average, degree):

        full_img_brightness_data = FileManager.load_full_img_brightness_data()
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        X = []
        y = []
        for t in train:
            for i in range(len(whole_liver_brightness_data)):
                if t['nii'] == whole_liver_brightness_data[i]['nii'] and t['nii'] == \
                        full_img_brightness_data[i]['nii']:
                    row = []
                    for k in range(len(types_of_average)):
                        row.append(float(whole_liver_brightness_data[i][types_of_average[k]]))
                    for k in range(len(relative_types_of_average)):
                        row.append(float(full_img_brightness_data[i][relative_types_of_average[k]]))
                    X.append(row)
                    y.append(float(t['ground_truth']))
                    break

        poly_model = PolynomialFeatures(degree=degree)
        poly_x_values = poly_model.fit_transform(X)
        poly_model.fit(poly_x_values, y)
        regression_model = LinearRegression()
        regression_model.fit(poly_x_values, y)

        poly_x = poly_model.fit_transform([values_of_brightness])
        y_pred = regression_model.predict(poly_x)

        print("y_pred", y_pred)

        return y_pred[0]


if __name__ == "__main__":
    steatosis_recognizer = Application()
    steatosis_recognizer.main()
