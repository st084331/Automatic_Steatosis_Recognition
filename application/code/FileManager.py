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
        fuzzy_criterion_train_sick_in_intersection_path = os.path.join(config_folder_path,
                                                                       'fuzzy_criterion_train_sick_in_intersection_'
                                                                       + type_of_average + '.json')
        if os.path.exists(fuzzy_criterion_train_sick_in_intersection_path):

            with open(fuzzy_criterion_train_sick_in_intersection_path, 'rb') as f:
                sick_intersection = json.load(f)
        else:
            raise FileExistsError

        fuzzy_criterion_train_healthy_in_intersection_path = os.path.join(config_folder_path,
                                                                          'fuzzy_criterion_train_healthy_in_intersection_'
                                                                          + type_of_average + '.json')
        if os.path.exists(fuzzy_criterion_train_healthy_in_intersection_path):
            with open(fuzzy_criterion_train_healthy_in_intersection_path, 'rb') as f:
                healthy_intersection = json.load(f)
        else:
            raise FileExistsError

        # print("End load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average, config_folder_path):

        # print("Start load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        most_powerful_criterion_train_path = os.path.join(config_folder_path,
                                                          'most_powerful_criterion_train_' + type_of_average + '.txt')
        if os.path.exists(most_powerful_criterion_train_path):
            with open(most_powerful_criterion_train_path, "r") as f:
                content = f.read()
                if content.replace('.', '', 1).isdigit():
                    value = float(content)
                else:
                    raise ValueError
            return value
        else:
            raise FileExistsError

        # print("End load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection, healthy_in_intersection, type_of_average,
                                      config_folder_path):

        # print("Start save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        sick_in_intersection_path = os.path.join(config_folder_path,
                                                 'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json')
        healthy_in_intersection_path = os.path.join(config_folder_path,
                                                    'fuzzy_criterion_train_healthy_in_intersection_' + type_of_average + '.json')

        if not os.path.exists(config_folder_path):
            os.mkdir(config_folder_path)
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if not os.path.exists(config_folder_path):
            raise Exception("Unable to create config folder")

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
        if not os.path.exists(config_folder_path):
            raise Exception("Unable to create config folder")

        border_point_path = os.path.join(config_folder_path,
                                         'most_powerful_criterion_train_' + type_of_average + '.txt')

        with open(border_point_path, 'w') as f:
            f.write(str(border_point))

        # print("End save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return border_point_path

    @staticmethod
    def delete_residual_files(substr, folder_path):
        # print("Start delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if os.path.exists(folder_path):
            folder = os.listdir(folder_path)
            # print(f"files = {files} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            for file in folder:
                if substr in file:
                    residual_file_path = os.path.join(folder_path, file)
                    if os.path.exists(residual_file_path):
                        os.remove(residual_file_path)
                    else:
                        raise FileExistsError
                    # print(f"{file} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        else:
            raise Exception("Folder does not exist")

        # print("End delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def check_dcm_only_in_folder(folder_path, substr):
        # print("Start check_dcm_in_folder |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if os.path.exists(folder_path):
            files_in_folder = os.listdir(folder_path)
            if len(files_in_folder) > 0:
                for file in files_in_folder:
                    if substr not in file:
                        # print("End check_dcm_in_folder with True |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                        return -1

                # print("End check_dcm_in_folder with False |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                return 1
            else:
                return 0
        else:
            raise Exception("Folder does not exist")
