import csv
import json
import os
from typing import List, Dict, Optional, Union
from datetime import datetime

from application.code.Init import DATA_FOLDER_PATH, CONFIG_FOLDER_PATH, PARENT_FOLDER_PATH
from application.code.Predictor import Predictor


class FileManager:

    @staticmethod
    def load_brightness_data(file_name: str, data_folder_path: str = DATA_FOLDER_PATH) -> List[Dict[str, Optional[Union[str, float]]]]:

        # print("Start load_brightness_data |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_path: str = os.path.join(data_folder_path, file_name)

        if os.path.exists(brightness_path):

            brightness_data: list = []
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
    def load_data_for_fuzzy_criterion(type_of_average: str, config_folder_path: str = CONFIG_FOLDER_PATH) -> List[
        List[float]]:
        # print("Start load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        fuzzy_criterion_train_sick_in_intersection_path: str = os.path.join(config_folder_path,
                                                                            'fuzzy_criterion_train_sick_in_intersection_'
                                                                            + type_of_average + '.json')
        if os.path.exists(fuzzy_criterion_train_sick_in_intersection_path):

            with open(fuzzy_criterion_train_sick_in_intersection_path, 'rb') as f:
                sick_intersection: List[float] = json.load(f)
        else:
            raise FileExistsError

        fuzzy_criterion_train_healthy_in_intersection_path: str = os.path.join(config_folder_path,
                                                                               'fuzzy_criterion_train_healthy_in_intersection_'
                                                                               + type_of_average + '.json')
        if os.path.exists(fuzzy_criterion_train_healthy_in_intersection_path):
            with open(fuzzy_criterion_train_healthy_in_intersection_path, 'rb') as f:
                healthy_intersection: List[float] = json.load(f)
        else:
            raise FileExistsError

        # print("End load_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return [sick_intersection, healthy_intersection]

    @staticmethod
    def load_data_for_most_powerful_criterion(type_of_average: str,
                                              config_folder_path: str = CONFIG_FOLDER_PATH) -> float:
        # print("Start load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        most_powerful_criterion_train_path: str = os.path.join(config_folder_path,
                                                               'most_powerful_criterion_train_' + type_of_average + '.txt')
        if os.path.exists(most_powerful_criterion_train_path):
            with open(most_powerful_criterion_train_path, "r") as f:
                content: str = f.read()
                # Float check
                if content.replace('.', '', 1).isdigit():
                    value: float = float(content)
                else:
                    raise ValueError
            return value
        else:
            raise FileExistsError

        # print("End load_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def save_data_for_fuzzy_criterion(sick_in_intersection: List[float], healthy_in_intersection: List[float],
                                      type_of_average: str,
                                      config_folder_path: str = CONFIG_FOLDER_PATH) -> List[str]:
        # print("Start save_data_for_fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        sick_in_intersection_path: str = os.path.join(config_folder_path,
                                                      'fuzzy_criterion_train_sick_in_intersection_' + type_of_average + '.json')
        healthy_in_intersection_path: str = os.path.join(config_folder_path,
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
    def save_data_for_most_powerful_criterion(border_point: float, type_of_average: str,
                                              config_folder_path: str = CONFIG_FOLDER_PATH) -> str:
        # print("Start save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if not os.path.exists(config_folder_path):
            os.mkdir(config_folder_path)
            # print("config dir created |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if not os.path.exists(config_folder_path):
            raise Exception("Unable to create config folder")

        border_point_path: str = os.path.join(config_folder_path,
                                              'most_powerful_criterion_train_' + type_of_average + '.txt')

        with open(border_point_path, 'w') as f:
            f.write(str(border_point))

        # print("End save_data_for_most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return border_point_path

    @staticmethod
    def delete_residual_files(substr: str, folder_path: str = PARENT_FOLDER_PATH):
        # print("Start delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if os.path.exists(folder_path):
            folder: List[str] = os.listdir(folder_path)
            # print(f"files = {files} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            for file in folder:
                if substr in file:
                    residual_file_path: str = os.path.join(folder_path, file)
                    if os.path.exists(residual_file_path):
                        os.remove(residual_file_path)
                    else:
                        raise FileExistsError
                    # print(f"{file} removed |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        else:
            raise Exception("Folder does not exist")

        # print("End delete_residual_files |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    # Checking if there are only Dicom files in the folder
    def check_dcm_only_in_folder(folder_path: str, substr: str) -> int:
        # print("Start check_dcm_in_folder |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if os.path.exists(folder_path):
            files_in_folder: List[str] = os.listdir(folder_path)
            if len(files_in_folder) > 0:
                for file in files_in_folder:
                    if substr not in file:
                        # print("End check_dcm_in_folder with True |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                        # There is at least 1 non-Dicom file
                        return -1

                # print("End check_dcm_in_folder with False |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                # There are only Dicom files
                return 1
            else:
                # Folder is empty
                return 0
        else:
            raise Exception("Folder does not exist")

    @staticmethod
    def make_config(averages: List[str], data_folder_path: str = DATA_FOLDER_PATH,
                    config_folder_path: str = CONFIG_FOLDER_PATH):
        # print("Start make_config |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # Data upload

        whole_liver_brightness_data: List[Dict[str, Optional[Union[str, float]]]] = FileManager.load_brightness_data(
            data_folder_path=data_folder_path,
            file_name="whole_liver.csv")

        train_data: List[Dict[str, Optional[Union[str, float]]]] = FileManager.load_brightness_data(data_folder_path=data_folder_path,
                                                                              file_name="train.csv")

        for type in averages:
            border_point: float = Predictor.most_powerful_criterion_train(type_of_average=type, train_data=train_data,
                                                                          whole_liver_brightness_data=whole_liver_brightness_data)

            FileManager.save_data_for_most_powerful_criterion(border_point=border_point,
                                                              type_of_average=type,
                                                              config_folder_path=config_folder_path)

            intersection: List[List[float]] = Predictor.fuzzy_criterion_train(type_of_average=type,
                                                                              train_data=train_data,
                                                                              whole_liver_brightness_data=whole_liver_brightness_data)

            FileManager.save_data_for_fuzzy_criterion(sick_in_intersection=intersection[0],
                                                      healthy_in_intersection=intersection[1],
                                                      type_of_average=type,
                                                      config_folder_path=config_folder_path)

        # print("End make_config |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
