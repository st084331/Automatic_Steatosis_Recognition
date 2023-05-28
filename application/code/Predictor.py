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
                if bd['nii'] == t['nii']:
                    if float(t['ground_truth']) == 0.0:
                        brightness_of_healthy_patients.append(float(bd[type_of_average]))
                    else:
                        brightness_of_sick_patients.append(float(bd[type_of_average]))
                    break

        if len(brightness_of_sick_patients) > 0:
            intersection_max_point = max(brightness_of_sick_patients)
        else:
            intersection_max_point = float('-inf')

        if len(brightness_of_healthy_patients) > 0:
            intersection_min_point = min(brightness_of_healthy_patients)
        else:
            intersection_min_point = float('inf')


        healthy_in_intersection = []
        for brightness in brightness_of_healthy_patients:
            if brightness < intersection_max_point and intersection_min_point < brightness:
                healthy_in_intersection.append(brightness)

        sick_in_intersection = []
        for brightness in brightness_of_sick_patients:
            if brightness < intersection_max_point and intersection_min_point < brightness:
                sick_in_intersection.append(brightness)

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

        # print("End finding best score point", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        FileManager.save_data_for_most_powerful_criterion(border_point=border_point, type_of_average=type_of_average,
                                                          config_folder_path=config_folder_path)

        # print("End most_powerful_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

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
