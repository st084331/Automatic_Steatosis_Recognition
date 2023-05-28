import math
from datetime import datetime

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from application.code.FileManager import FileManager
from application.code.FormatConverter import FormatConverter
from application.code.Init import AVERAGES, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH


class Predictor:

    @staticmethod
    def make_config():
        # print("Start make_config |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=AVERAGES)

        for type in current_types:
            Predictor.most_powerful_criterion_train(type_of_average=type)

            Predictor.fuzzy_criterion_train(type_of_average=type)

        # print("End make_config |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def fuzzy_criterion_train(type_of_average, data_folder_path=DATA_FOLDER_PATH,
                              config_folder_path=CONFIG_FOLDER_PATH):
        # print("Start fuzzy_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        whole_liver_brightness_data = FileManager.load_brightness_data(data_folder_path=data_folder_path,
                                                                       file_name="whole_liver.csv")

        train = FileManager.load_brightness_data(data_folder_path=data_folder_path, file_name="train.csv")

        # print("Start finding intersection", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_of_sick_patients = []
        brightness_of_healthy_patients = []
        for bd in whole_liver_brightness_data:
            for t in train:
                if 'nii' in bd.keys():
                    if 'nii' in t.keys():
                        if bd['nii'] == t['nii']:
                            if type_of_average in bd.keys():
                                content = bd[type_of_average]
                                if content.replace('.', '', 1).isdigit():
                                    value = float(content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception(f"{type_of_average} type of average does not exist")
                            if float(t['ground_truth']) == 0.0:
                                brightness_of_healthy_patients.append(value)
                            else:
                                brightness_of_sick_patients.append(value)
                            break
                    else:
                        raise Exception(f"Wrong keys in {t}")
                else:
                    raise Exception(f"Wrong keys in {bd}")

        if len(brightness_of_sick_patients) > 0:
            intersection_max_point = max(brightness_of_sick_patients)
        else:
            intersection_max_point = float('-inf')

        if len(brightness_of_healthy_patients) > 0:
            intersection_min_point = min(brightness_of_healthy_patients)
        else:
            intersection_min_point = float('inf')

        healthy_in_intersection = []
        for brightness_list in brightness_of_healthy_patients:
            if brightness_list < intersection_max_point and intersection_min_point < brightness_list:
                healthy_in_intersection.append(brightness_list)

        sick_in_intersection = []
        for brightness_list in brightness_of_sick_patients:
            if brightness_list < intersection_max_point and intersection_min_point < brightness_list:
                sick_in_intersection.append(brightness_list)

        # print("End finding intersection", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        FileManager.save_data_for_fuzzy_criterion(sick_in_intersection=sick_in_intersection,
                                                  healthy_in_intersection=healthy_in_intersection,
                                                  type_of_average=type_of_average,
                                                  config_folder_path=config_folder_path)

        return [sick_in_intersection, healthy_in_intersection]

        # print("End fuzzy_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

    @staticmethod
    def most_powerful_criterion_train(type_of_average, data_folder_path=DATA_FOLDER_PATH,
                                      config_folder_path=CONFIG_FOLDER_PATH):
        # print("Start most_powerful_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        whole_liver_brightness_data = FileManager.load_brightness_data(data_folder_path=data_folder_path,
                                                                       file_name="whole_liver.csv")

        train = FileManager.load_brightness_data(data_folder_path=data_folder_path, file_name="train.csv")

        # print("Start finding best score point", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_list = []
        y = []
        for bd in whole_liver_brightness_data:
            for t in train:
                if 'nii' in bd.keys():
                    if 'nii' in t.keys():
                        if bd['nii'] == t['nii']:
                            if type_of_average in bd.keys():
                                content = bd[type_of_average]
                                if content.replace('.', '', 1).isdigit():
                                    value = float(content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception(f"{type_of_average} type of average does not exist")

                            brightness_list.append(value)
                            y.append(int(float(t['ground_truth'])))
                    else:
                        raise Exception(f"Wrong keys in {t}")
                else:
                    raise Exception(f"Wrong keys in {bd}")

        if len(brightness_list) > 0:
            max_point = max(brightness_list)
            min_point = min(brightness_list)
            border_point = (max_point + min_point) / 2

            y_pred_init = []

            for bd in whole_liver_brightness_data:
                for t in train:
                    if 'nii' in bd.keys():
                        if 'nii' in t.keys():
                            if bd['nii'] == t['nii']:
                                if type_of_average in bd.keys():
                                    content = bd[type_of_average]
                                    if content.replace('.', '', 1).isdigit():
                                        value = float(content)
                                    else:
                                        raise ValueError
                                else:
                                    raise Exception(f"{type_of_average} type of average does not exist")
                                if value <= border_point:
                                    y_pred_init.append(1)
                                else:
                                    y_pred_init.append(0)
                                break
                        else:
                            raise Exception(f"Wrong keys in {t}")
                    else:
                        raise Exception(f"Wrong keys in {bd}")

            score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
            leftmost_best_score = score
            current_leftmost_score = score
            leftmost_point = border_point
            step = 0.1

            while current_leftmost_score >= score:
                # print(f"leftmost_best_score={leftmost_best_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                # print(f"leftmost_point={leftmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                # print(f"score={score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                score = leftmost_best_score
                current_leftmost_point = leftmost_point - step

                y_pred_leftmost_point = []

                for bd in whole_liver_brightness_data:
                    for t in train:
                        if 'nii' in bd.keys():
                            if 'nii' in t.keys():
                                if bd['nii'] == t['nii']:
                                    if type_of_average in bd.keys():
                                        content = bd[type_of_average]
                                        if content.replace('.', '', 1).isdigit():
                                            value = float(content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if value <= current_leftmost_point:
                                        y_pred_leftmost_point.append(1)
                                    else:
                                        y_pred_leftmost_point.append(0)
                                    break
                            else:
                                raise Exception(f"Wrong keys in {t}")
                        else:
                            raise Exception(f"Wrong keys in {bd}")

                # print(f"y_pred_leftmost_point={y_pred_leftmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                current_leftmost_score = math.fabs(sklearn.metrics.f1_score(y, y_pred_leftmost_point))
                # print(f"current_leftmost_score={current_leftmost_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                if current_leftmost_score >= score:
                    leftmost_best_score = current_leftmost_score
                    leftmost_point = current_leftmost_point

            border_point = (max_point + min_point) / 2
            score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
            rightmost_best_score = score
            current_rightmost_score = score
            rightmost_point = border_point

            while current_rightmost_score >= score:
                # print(f"rightmost_best_score={rightmost_best_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                # print(f"rightmost_point={rightmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                # print(f"score={score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                score = rightmost_best_score
                current_rightmost_point = rightmost_point + step

                y_pred_rightmost_point = []

                for bd in whole_liver_brightness_data:
                    for t in train:
                        if 'nii' in bd.keys():
                            if 'nii' in t.keys():
                                if bd['nii'] == t['nii']:
                                    if type_of_average in bd.keys():
                                        content = bd[type_of_average]
                                        if content.replace('.', '', 1).isdigit():
                                            value = float(content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if value <= current_rightmost_point:
                                        y_pred_rightmost_point.append(1)
                                    else:
                                        y_pred_rightmost_point.append(0)
                                    break
                            else:
                                raise Exception(f"Wrong keys in {t}")
                        else:
                            raise Exception(f"Wrong keys in {bd}")

                # print(f"y_pred_rightmost_point={y_pred_rightmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                current_rightmost_score = math.fabs(sklearn.metrics.f1_score(y, y_pred_rightmost_point))
                # print(f"current_rightmost_score={current_rightmost_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

                if current_rightmost_score >= score:
                    rightmost_best_score = current_rightmost_score
                    rightmost_point = current_rightmost_point

            # print(f"rightmost_point={rightmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            # print(f"leftmost_point={leftmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            if rightmost_best_score >= leftmost_best_score:
                border_point = rightmost_point
            else:
                border_point = leftmost_point

            # print("End finding best score point", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            FileManager.save_data_for_most_powerful_criterion(border_point=border_point,
                                                              type_of_average=type_of_average,
                                                              config_folder_path=config_folder_path)

            return border_point
            # print("End most_powerful_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        else:
            raise Exception("Brightness list is empty")

    @staticmethod
    def most_powerful_criterion(value_of_brightness, type_of_average):

        # print("Start most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        boarder_point = FileManager.load_data_for_most_powerful_criterion(
            type_of_average=type_of_average, config_folder_path=CONFIG_FOLDER_PATH)

        if float(value_of_brightness) <= boarder_point:
            # print("End most_powerful_criterion with 1.0 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            return 1.0
        else:
            # print("End most_powerful_criterion with 0.0 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            return 0.0

    @staticmethod
    def fuzzy_criterion(value_of_brightness, type_of_average):
        # print("Start fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        sick_intersection, healthy_intersection = FileManager.load_data_for_fuzzy_criterion(
            type_of_average=type_of_average, config_folder_path=CONFIG_FOLDER_PATH)

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

        # print(f"End fuzzy_criterion with {prediction} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return prediction

    @staticmethod
    def linear_regression(values_of_brightness, types_of_average, relative_types_of_average):

        # print("Start linear_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        full_img_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                    file_name="full_img.csv")

        whole_liver_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                       file_name="whole_liver.csv")

        train = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH, file_name="train.csv")

        X = []
        y = []
        # print("Start training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
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

        reg = LinearRegression()
        reg.fit(X, y)

        # print("End training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        y_pred = reg.predict([values_of_brightness])

        # print(f"End linear_regression with {y_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return y_pred[0]

    @staticmethod
    def polynomial_regression(values_of_brightness, types_of_average, relative_types_of_average, degree):

        # print("Start polynomial_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        full_img_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                    file_name="full_img.csv")

        whole_liver_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                       file_name="whole_liver.csv")

        train = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH, file_name="train.csv")

        X = []
        y = []
        # print("Start training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
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
        # print("End training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        poly_x = poly_model.fit_transform([values_of_brightness])
        y_pred = regression_model.predict(poly_x)

        # print(f"End polynomial_regression with {y_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return y_pred[0]
