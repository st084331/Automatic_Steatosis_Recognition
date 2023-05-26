import csv
import json
import os
import nibabel as nib

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
        with open(os.path.join('.', 'config', 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            sick_intersection = json.load(f)

        with open(os.path.join('.', 'config', 'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            healthy_intersection = json.load(f)

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average):
        file = open(os.path.join('.', 'config', 'most_powerful_criterion_train_' + type_of_average + '.txt'), "r")
        return float(file.read())

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection, healthy_in_intersection, type_of_average):
        if not os.path.exists(os.path.join(".", "config")):
            os.mkdir(os.path.join(".", "config"))

        with open(os.path.join('.', 'config', 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                  'w') as f:
            json.dump(sick_in_intersection, f)

        with open(os.path.join('.', 'config', 'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'w') as f:
            json.dump(healthy_in_intersection, f)

    @staticmethod
    def save_data_for_most_powerful_criterion(border_point, type_of_average):
        if not os.path.exists(os.path.join(".", "config")):
            os.mkdir(os.path.join(".", "config"))

        with open(os.path.join('.', 'config', 'most_powerful_criterion_train_' + type_of_average + '.txt'), 'w') as f:
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