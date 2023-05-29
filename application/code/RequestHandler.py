import os
import statistics
from datetime import datetime

from application.code.CT_Handler import CT_Handler
from application.code.FileManager import FileManager
from application.code.FormatConverter import FormatConverter
from application.code.Init import CONFIG_FOLDER_PATH
from application.code.Predictor import Predictor
from typing import List, Dict, Optional, Union


class RequestHandler:

    @staticmethod
    def result_request(types_of_average: List[str],
                       relative_types_of_average: List[str], method: str, folder_path: str, area: str,
                       config_folder_path: str = CONFIG_FOLDER_PATH) -> float:

        # print("Start result_request |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        folder_struct = os.path.split(folder_path)
        # print(f"folder_struct = {folder_struct}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        name_of_nifti_wo_extension: str = folder_struct[len(folder_struct) - 1]
        # print(f"name_of_nifti_wo_extension = {name_of_nifti_wo_extension}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=types_of_average)

        current_relative_types = FormatConverter.types_of_average_to_current_types(
            types_of_average=relative_types_of_average)

        values_of_brightness: List[float] = RequestHandler.brightness_values_request(area=area,
                                                                                     types_of_average=types_of_average,
                                                                                     relative_types_of_average=relative_types_of_average,
                                                                                     handler=CT_Handler(folder_path=folder_path,
                                                                                                        name_of_nifti_wo_extension=name_of_nifti_wo_extension))
        # print(f"values_of_brightness = {values_of_brightness}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        if method == "Fuzzy criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    sick_intersection, healthy_intersection = FileManager.load_data_for_fuzzy_criterion(
                        type_of_average=current_types[0])
                    result: float = Predictor.fuzzy_criterion(value_of_brightness=values_of_brightness[0],
                                                              healthy_intersection=healthy_intersection,
                                                              sick_intersection=sick_intersection)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Most powerful criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    boarder_point: float = FileManager.load_data_for_most_powerful_criterion(
                        type_of_average=current_types[0], config_folder_path=config_folder_path)
                    result: float = Predictor.most_powerful_criterion(value_of_brightness=values_of_brightness[0],
                                                                      boarder_point=boarder_point)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif "regression" in method:
            if method == "Second degree polynomial regression":
                degree = 2
            elif method == "Linear regression":
                degree = 1
            else:
                raise Exception(f"{method} method is not defined")
            if len(values_of_brightness) >= 1:
                if len(types_of_average) >= 1:
                    whole_study_brightness_data: List[
                        Dict[str, Optional[Union[str, float]]]] = FileManager.load_brightness_data(
                        "whole_study.csv")
                    whole_liver_brightness_data: List[
                        Dict[str, Optional[Union[str, float]]]] = FileManager.load_brightness_data(
                        "whole_liver.csv")
                    train_data: List[Dict[str, Optional[Union[str, float]]]] = FileManager.load_brightness_data(
                        "train.csv")
                    brightness_list, steatosis_status_list = Predictor.regression_data_maker(
                        whole_study_brightness_data=whole_study_brightness_data,
                        whole_liver_brightness_data=whole_liver_brightness_data, train_data=train_data,
                        types_of_average=current_types, relative_types_of_average=current_relative_types)
                    result: float = Predictor.polynomial_regression(values_of_brightness=values_of_brightness,
                                                                    brightness_list=brightness_list,
                                                                    steatosis_status_list=steatosis_status_list,
                                                                    degree=degree)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        else:
            raise Exception(f"{method} method is not defined")

        # print(f"End result_request with {result} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return result

    @staticmethod
    def brightness_values_request(area: str, types_of_average: List[str], relative_types_of_average: List[str],
                                  handler: CT_Handler) -> List[float]:
        # print("Start brightness_values_request |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if area == "Whole liver":
            brightness_list: List[float] = handler.get_whole_liver_brightness_info()
        elif area == "Three random areas":
            brightness_list: List[float] = handler.get_three_areas_brightness_info()
        elif area == "Two random areas":
            brightness_list: List[float] = handler.get_two_areas_brightness_info()
        elif area == "One random area":
            brightness_list: List[float] = handler.get_one_area_brightness_info()
        elif area == "100 random points":
            brightness_list: List[float] = handler.get_random_points_brightness_info()
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
            relative_brightness_list: List[float] = handler.get_whole_study_brightness_info()
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

        # print(f"End brightness_values_request with {brightness_values} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return brightness_values
