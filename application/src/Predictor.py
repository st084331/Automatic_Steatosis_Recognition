import math

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from application.src.FileManager import FileManager
from application.src.FormatConverter import FormatConverter
from application.src.Init import AVERAGES


class Predictor:

    @staticmethod
    def make_config():
        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=AVERAGES)
        for type in current_types:
            Predictor.most_powerful_criterion_train(type)
            Predictor.fuzzy_criterion_train(type)

    @staticmethod
    def fuzzy_criterion_train(type_of_average):

        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

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
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

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

    @staticmethod
    def linear_regression(values_of_brightness, types_of_average, relative_types_of_average):

        full_img_brightness_data = FileManager.load_full_img_brightness_data()
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        X = []
        y = []
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

        reg = LinearRegression().fit(X, y)

        y_pred = reg.predict([values_of_brightness])

        print("y_pred", y_pred)

        return y_pred[0]

    @staticmethod
    def polynomial_regression(values_of_brightness, types_of_average, relative_types_of_average, degree):

        full_img_brightness_data = FileManager.load_full_img_brightness_data()
        whole_liver_brightness_data = FileManager.load_whole_liver_brightness_data()
        train = FileManager.load_test_data()

        X = []
        y = []
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

        poly_x = poly_model.fit_transform([values_of_brightness])
        y_pred = regression_model.predict(poly_x)

        print("y_pred", y_pred)

        return y_pred[0]