import csv
import json
import os
from datetime import datetime


class FileManager:

    @staticmethod
    def load_brightness_data(data_folder_path, file_name):
        # print("Start load_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_path = os.path.join(data_folder_path, file_name)

        if os.path.exists(brightness_path):

            brightness_data = []
            with open(brightness_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    brightness_data.append(row)

            # print(f"{brightness_data} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            # print("End load_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            return brightness_data
        else:
            raise FileExistsError

    @staticmethod
    def load_data_for_fuzzy_criterion(type_of_average, config_folder_path):

        # print("Start load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(
                os.path.join(config_folder_path,
                             'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json'),
                'rb') as f:
            sick_intersection = json.load(f)

        with open(os.path.join(config_folder_path,
                               'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json'),
                  'rb') as f:
            healthy_intersection = json.load(f)

        # print("End load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average, config_folder_path):

        # print("Start load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(os.path.join(config_folder_path, 'most_powerful_criterion_train_' + type_of_average + '.txt'),
                  "r") as f:
            value = float(f.read())

        # print("End load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return value

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection, healthy_in_intersection, type_of_average, config_folder_path):

        # print("Start save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        sick_in_intersection_path = os.path.join(config_folder_path,
                                                 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json')
        healthy_in_intersection_path = os.path.join(config_folder_path,
                                                    'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json')

        if not os.path.exists(config_folder_path):
            os.mkdir(config_folder_path)
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        with open(sick_in_intersection_path, 'w') as f:
            json.dump(sick_in_intersection, f)

        with open(healthy_in_intersection_path, 'w') as f:
            json.dump(healthy_in_intersection, f)

        # print("End save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return [sick_in_intersection_path, healthy_in_intersection_path]

    @staticmethod
    def save_data_for_most_powerful_criterion(border_point, type_of_average, config_folder_path):

        # print("Start save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if not os.path.exists(config_folder_path):
            os.mkdir(config_folder_path)
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        border_point_path = os.path.join(config_folder_path,
                                         'most_powerful_criterion_train_' + type_of_average + '.txt')

        with open(border_point_path, 'w') as f:
            f.write(str(border_point))

        # print("End save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return border_point_path

    @staticmethod
    def delete_residual_files(substr, folder_path):
        # print("Start delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        folder = os.listdir(folder_path)
        # print(f"files = {files} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for file in folder:
            if substr in file:
                os.remove(os.path.join(folder_path, file))
                # print(f"{file} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("End delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def check_dcm_in_folder(folder_path, substr):
        # print("Start check_dcm_in_folder |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        files_in_folder = os.listdir(folder_path)
        for file in files_in_folder:
            if substr in file:
                # print("End check_dcm_in_folder with True |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                return True

        # print("End check_dcm_in_folder with False |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return False
