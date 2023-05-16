import math
import os
import random
import nibabel as nib
from datetime import datetime
import statistics
import csv
import dicom2nifti
import dicom2nifti.settings as settings
import sklearn
import sklearn.metrics
import torch as torch

import livermask.livermask

vessels = False
verbose = False
cpu = True
if torch.cuda.is_available():
    cpu = False
settings.disable_validate_slice_increment()


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
                                 cpu, verbose, vessels)

    def whole_liver_brightness_info(self):
        mask_img = nib.load(os.path.join(".", self.name_of_nifti + "-livermask2.nii"))
        mask_data = mask_img.get_fdata()
        full_img = nib.load(os.path.join(".", self.name_of_nifti + ".nii"))
        full_data = full_img.get_fdata()

        whole_liver_list_of_brightness = []
        for z in range(0, mask_data.shape[0], 2):
            for y in range(0, mask_data.shape[1], 2):
                for x in range(0, mask_data.shape[2], 2):
                    if mask_data[z][y][x] == 1:
                        whole_liver_list_of_brightness.append(full_data[z][y][x])

        return whole_liver_list_of_brightness

    def three_areas_brightness_info(self):
        mask_img = nib.load(os.path.join(".", self.name_of_nifti + "-livermask2.nii"))
        mask_data = mask_img.get_fdata()
        full_img = nib.load(os.path.join(".", self.name_of_nifti + ".nii"))
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

    def most_poweful_criterion(self, value_of_brightness, type_of_average):
        brightness_data = []
        with open(os.path.join(".", 'data', 'whole_liver' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data.append(row)

        train = []
        train_csv = os.path.join(".", "data", "train.csv")
        with open(train_csv) as f:
            reader = csv.DictReader(f)
            for row in reader:
                train.append(row)

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

        if float(value_of_brightness) <= border_point:
            return 1.0
        else:
            return 0.0

    def fuzzy_criterion(self, value_of_brightness, type_of_average):
        brightness_data = []
        with open(os.path.join(".", 'data', 'whole_liver' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data.append(row)

        train = []
        train_csv = os.path.join(".", "data", "train.csv")
        with open(train_csv) as f:
            reader = csv.DictReader(f)
            for row in reader:
                train.append(row)

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
        intersection = []
        for b in brightness_of_healthy_patients:
            if b < intersection_max_point:
                intersection.append([0, b])
        for b in brightness_of_sick_patients:
            if b > intersection_min_point:
                intersection.append([1, b])

        prediction = 0.5

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
    print("Enter absolute path to the folder with dicom files: ")
    folder = input()
    if os.path.exists(folder):
        # try:
        folder_struct = folder.split('/')
        name_of_nifti = folder_struct[len(folder_struct) - 1]
        handler = CT_Handler(folder, name_of_nifti)
        value_of_brightness = handler.three_areas_median_of_brightness()
        print("File parsed successfully", "|", datetime.now().strftime("%H:%M:%S"))
        predictor = Predictor()
        print(predictor.fuzzy_criterion(value_of_brightness, "median"))
        print(predictor.most_poweful_criterion(value_of_brightness, "median"))
        os.remove(name_of_nifti + ".nii")
        os.remove(name_of_nifti + "-livermask2.nii")
    # except:
    # print("The specified folder cannot be opened")
    else:
        print("Wrong path")
