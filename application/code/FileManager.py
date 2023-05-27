import csv
import json
import os
from datetime import datetime

import nibabel as nib

from application.code.Init import PARENT_PATH


class FileManager:

    @staticmethod
    def load_full_img_brightness_data():
        # print("Start load_full_img_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        full_img_brightness_data = []
        with open(os.path.join(PARENT_PATH, 'data', 'full_brightness' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_img_brightness_data.append(row)

        # print(f"{full_img_brightness_data} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("End load_full_img_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return full_img_brightness_data

    @staticmethod
    def load_whole_liver_brightness_data():
        # print("Start load_whole_liver_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        brightness_data_wo_quantiles = []
        with open(os.path.join(PARENT_PATH, 'data', 'whole_liver' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_wo_quantiles.append(row)

        brightness_data_quantiles = []
        with open(os.path.join(PARENT_PATH, 'data', 'whole_liver_quantiles' + '.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_quantiles.append(row)

        whole_liver_brightness_data = []
        for i in range(len(brightness_data_wo_quantiles)):
            whole_liver_brightness_data.append({**brightness_data_wo_quantiles[i], **brightness_data_quantiles[i]})

        # print(f"{whole_liver_brightness_data} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        # print("End load_whole_liver_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return whole_liver_brightness_data

    @staticmethod
    def load_test_data():

        train = []

        # print("Start load_test_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        train_csv = os.path.join(PARENT_PATH, "data", "train.csv")
        with open(train_csv) as f:
            reader = csv.DictReader(f)
            for row in reader:
                train.append(row)

        # print(f"{train} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        # print("End load_test_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return train

    @staticmethod
    def load_mask_image(name_of_nifti):

        # print(f"Start load_mask_image |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        path = os.path.join(PARENT_PATH, name_of_nifti + "-livermask2.nii")

        # print(f"End and Call nib.load({path}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return nib.load(path)

    @staticmethod
    def load_original_image(name_of_nifti):

        # print(f"Start load_original_image |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        path = os.path.join(PARENT_PATH, name_of_nifti + ".nii")

        # print(f"End and Call nib.load({path}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return nib.load(path)

    @staticmethod
    def load_data_for_fuzzy_criterion(type_of_average):

        # print("Start load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(
                os.path.join(PARENT_PATH, 'config',
                             'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                'rb') as f:
            sick_intersection = json.load(f)

        with open(os.path.join(PARENT_PATH, 'config',
                               'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            healthy_intersection = json.load(f)

        # print("End load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average):

        # print("Start load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        file = open(os.path.join(PARENT_PATH, 'config', 'most_powerful_criterion_train_' + type_of_average + '.txt'),
                    "r")
        value = float(file.read())

        # print("End load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return value

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection, healthy_in_intersection, type_of_average):

        # print("Start save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if not os.path.exists(os.path.join(PARENT_PATH, "config")):
            os.mkdir(os.path.join(PARENT_PATH, "config"))
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(
                os.path.join(PARENT_PATH, 'config',
                             'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                'w') as f:
            json.dump(sick_in_intersection, f)

        with open(os.path.join(PARENT_PATH, 'config',
                               'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'w') as f:
            json.dump(healthy_in_intersection, f)

        # print("End save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def save_data_for_most_powerful_criterion(border_point, type_of_average):

        # print("Start save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if not os.path.exists(os.path.join(PARENT_PATH, "config")):
            os.mkdir(os.path.join(PARENT_PATH, "config"))
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(os.path.join(PARENT_PATH, 'config', 'most_powerful_criterion_train_' + type_of_average + '.txt'),
                  'w') as f:
            f.write(str(border_point))

        # print("End save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def remove_additional_files(name_of_nifti):

        # print("Start remove_additional_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        filename_of_nifti = name_of_nifti + ".nii"
        os.remove(os.path.join(PARENT_PATH, filename_of_nifti))
        # print(f"{filename_of_nifti} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        filename_of_nifti_livermask = name_of_nifti + "-livermask2.nii"
        os.remove(os.path.join(PARENT_PATH, filename_of_nifti_livermask))
        # print(f"{filename_of_nifti_livermask} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("End remove_additional_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def delete_residual_files(substr):
        # print("Start delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        files = os.listdir(PARENT_PATH)
        # print(f"files = {files} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for file in files:
            if substr in file:
                os.remove(os.path.join(PARENT_PATH, file))
                # print(f"{file} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("End delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def check_dcm_in_folder(folder, substr):
        # print("Start check_dcm_in_folder |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        files_in_folder = os.listdir(folder)
        for file in files_in_folder:
            if substr in file:
                # print("End check_dcm_in_folder with True |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                return True

        # print("End check_dcm_in_folder with False |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return False
