import math
import os
import random
import sys
import nibabel as nib
from datetime import datetime
import statistics
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox
import csv
import dicom2nifti
import dicom2nifti.settings as settings
import sklearn
import sklearn.metrics
import json
import torch as torch
import livermask.livermask

METHODS = ["Fuzzy criterion", "Most powerful criterion"]
AREAS = ["Whole liver", "Three random areas"]
AVERAGES = ["Median", "Mode", "Mean"]

VESSELS = False
VERBOSE = False
CPU = True
if torch.cuda.is_available():
    CPU = False
settings.disable_validate_slice_increment()


class Application:

    def main(self):
        FileManager.delete_residual_files(substr=".nii")
        for type in AVERAGES:
            Predictor.most_powerful_criterion_train(type.lower())
            Predictor.fuzzy_criterion_train(type.lower())
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()


class FileManager:

    @staticmethod
    def load_brightness_data():
        brightness_data = []
        with open(os.path.join(".", 'data', 'whole_liver' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data.append(row)
        return brightness_data

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
    def result_request(value_of_brightness, type_of_average, method):
        if method == "Fuzzy criterion":
            return Predictor.fuzzy_criterion(value_of_brightness, type_of_average)
        elif method == "Most powerful criterion":
            return Predictor.most_powerful_criterion(value_of_brightness, type_of_average)
        return 0.0

    @staticmethod
    def brightness_value_request(area, type_of_average, handler):
        if area == "Whole liver":
            if type_of_average == "Median":
                return handler.whole_liver_median_of_brightness()
            elif type_of_average == "Mode":
                return handler.whole_liver_mode_of_brightness()
            elif type_of_average == "Mean":
                return handler.whole_liver_mean_of_brightness()
        elif area == "Three random areas":
            if type_of_average == "Median":
                return handler.three_areas_median_of_brightness()
            elif type_of_average == "Mode":
                return handler.three_areas_mode_of_brightness()
            elif type_of_average == "Mean":
                return handler.three_areas_mean_of_brightness()
        return 0.0


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steatosis Recognizer")

        self.result_label = QLabel()

        self.methods_combobox = QComboBox()
        self.methods_combobox.addItems(METHODS)

        self.averages_combobox = QComboBox()
        self.averages_combobox.addItems(AVERAGES)

        self.areas_combobox = QComboBox()
        self.areas_combobox.addItems(AREAS)

        self.help_label = QLabel("Enter the full path to the research folder")

        self.input = QLineEdit()

        self.button = QPushButton("Analyse")
        self.button.clicked.connect(self.handle_button)

        layout = QVBoxLayout()
        layout.addWidget(self.help_label)
        layout.addWidget(self.input)
        layout.addWidget(self.methods_combobox)
        layout.addWidget(self.averages_combobox)
        layout.addWidget(self.areas_combobox)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def handle_button(self):
        folder = str(self.input.text())
        method = self.methods_combobox.currentText()
        type_of_average = self.averages_combobox.currentText().lower()
        area = self.areas_combobox.currentText()
        if os.path.exists(folder):
            try:

                if FileManager.check_dcm_in_folder(folder=folder, substr=".dcm"):
                    folder_struct = os.path.split(folder)
                    name_of_nifti = folder_struct[len(folder_struct) - 1]

                    value_of_brightness = RequestHandler.brightness_value_request(area=area,
                                                                                  type_of_average=type_of_average,
                                                                                  handler=CT_Handler(folder,
                                                                                                     name_of_nifti))

                    result = f"The probability of having steatosis is {RequestHandler.result_request(value_of_brightness=value_of_brightness, type_of_average=type_of_average, method=method) * 100}%"

                    FileManager.remove_additional_files(name_of_nifti=name_of_nifti)
                else:
                    result = "This is not Dicom folder"

            except:
                result = "The specified folder cannot be opened"
        else:
            result = "Wrong path"

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

    def whole_liver_mode_of_brightness(self):
        whole_liver_list_of_brightness = self.whole_liver_brightness_info()
        return statistics.mode(whole_liver_list_of_brightness)

    def whole_liver_mean_of_brightness(self):
        whole_liver_list_of_brightness = self.whole_liver_brightness_info()
        return statistics.mean(whole_liver_list_of_brightness)

    def whole_liver_median_of_brightness(self):
        whole_liver_list_of_brightness = self.whole_liver_brightness_info()
        return statistics.median(whole_liver_list_of_brightness)

    def three_areas_mode_of_brightness(self):
        three_areas_brightness = self.three_areas_brightness_info()
        return statistics.mode(three_areas_brightness)

    def three_areas_mean_of_brightness(self):
        three_areas_brightness = self.three_areas_brightness_info()
        return statistics.mean(three_areas_brightness)

    def three_areas_median_of_brightness(self):
        three_areas_brightness = self.three_areas_brightness_info()
        return statistics.median(three_areas_brightness)


class Predictor:

    @staticmethod
    def fuzzy_criterion_train(type_of_average):
        brightness_data = FileManager.load_brightness_data()
        train = FileManager.load_test_data()

        brightness_of_sick_patients = []
        brightness_of_healthy_patients = []
        for bd in brightness_data:
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
        brightness_data = FileManager.load_brightness_data()
        train = FileManager.load_test_data()

        brightness = []
        y = []
        for bd in brightness_data:
            for t in train:
                if bd['nii'] == t['nii']:
                    brightness.append(float(bd[type_of_average]))
                    y.append(int(float(t['ground_truth'])))

        max_point = max(brightness)
        min_point = min(brightness)
        border_point = (max_point + min_point) / 2

        y_pred_init = []

        for bd in brightness_data:
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

            for bd in brightness_data:
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

            for bd in brightness_data:
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


if __name__ == "__main__":
    steatosis_recognizer = Application()
    steatosis_recognizer.main()
