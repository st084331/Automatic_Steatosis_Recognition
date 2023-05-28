import math
from datetime import datetime

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class Predictor:

    @staticmethod
    def fuzzy_criterion_train(type_of_average, whole_liver_brightness_data, train_data):
        # print("Start fuzzy_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Start finding intersection", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_of_sick_patients = []
        brightness_of_healthy_patients = []
        for bd in whole_liver_brightness_data:
            for t in train_data:
                if 'nii' in bd.keys():
                    if 'nii' in t.keys():
                        if bd['nii'] == t['nii']:
                            if type_of_average in bd.keys():
                                content = str(bd[type_of_average])
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
        if intersection_max_point != float('-inf'):
            for brightness_list in brightness_of_healthy_patients:
                if intersection_max_point >= brightness_list >= intersection_min_point:
                    healthy_in_intersection.append(brightness_list)
        else:
            for brightness_list in brightness_of_healthy_patients:
                if brightness_list >= intersection_min_point:
                    healthy_in_intersection.append(brightness_list)

        sick_in_intersection = []
        if intersection_min_point != float('inf'):
            for brightness_list in brightness_of_sick_patients:
                if intersection_max_point >= brightness_list >= intersection_min_point:
                    sick_in_intersection.append(brightness_list)
        else:
            for brightness_list in brightness_of_sick_patients:
                if intersection_max_point >= brightness_list:
                    sick_in_intersection.append(brightness_list)

        # print("End finding intersection", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return [sick_in_intersection, healthy_in_intersection]

    @staticmethod
    def most_powerful_criterion_train(type_of_average, whole_liver_brightness_data, train_data):
        # print("Start most_powerful_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Start finding best score point", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_list = []
        steatosis_status_list = []
        for bd in whole_liver_brightness_data:
            for t in train_data:
                if 'nii' in bd.keys():
                    if 'nii' in t.keys():
                        if bd['nii'] == t['nii']:
                            if type_of_average in bd.keys():
                                content = str(bd[type_of_average])
                                if content.replace('.', '', 1).isdigit():
                                    value = float(content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception(f"{type_of_average} type of average does not exist")

                            brightness_list.append(value)
                            steatosis_status_list.append(int(float(t['ground_truth'])))
                    else:
                        raise Exception(f"Wrong keys in {t}")
                else:
                    raise Exception(f"Wrong keys in {bd}")

        if len(brightness_list) > 0:
            max_point = max(brightness_list)
            min_point = min(brightness_list)
            border_point = (max_point + min_point) / 2

            pred_steatosis_status_list_init = []

            for bd in whole_liver_brightness_data:
                for t in train_data:
                    if 'nii' in bd.keys():
                        if 'nii' in t.keys():
                            if bd['nii'] == t['nii']:
                                if type_of_average in bd.keys():
                                    content = str(bd[type_of_average])
                                    if content.replace('.', '', 1).isdigit():
                                        value = float(content)
                                    else:
                                        raise ValueError
                                else:
                                    raise Exception(f"{type_of_average} type of average does not exist")
                                if value <= border_point:
                                    pred_steatosis_status_list_init.append(1)
                                else:
                                    pred_steatosis_status_list_init.append(0)
                                break
                        else:
                            raise Exception(f"Wrong keys in {t}")
                    else:
                        raise Exception(f"Wrong keys in {bd}")

            score = math.fabs(sklearn.metrics.f1_score(steatosis_status_list, pred_steatosis_status_list_init))
            leftmost_best_score = score
            leftmost_point = border_point
            current_leftmost_score = score
            current_leftmost_point = border_point
            step = 0.1

            while current_leftmost_score >= score:
                leftmost_best_score = current_leftmost_score
                leftmost_point = current_leftmost_point

                score = current_leftmost_score
                current_leftmost_point = leftmost_point - step

                pred_steatosis_status_list_leftmost = []

                for bd in whole_liver_brightness_data:
                    for t in train_data:
                        if 'nii' in bd.keys():
                            if 'nii' in t.keys():
                                if bd['nii'] == t['nii']:
                                    if type_of_average in bd.keys():
                                        content = str(bd[type_of_average])
                                        if content.replace('.', '', 1).isdigit():
                                            value = float(content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if value <= current_leftmost_point:
                                        pred_steatosis_status_list_leftmost.append(1)
                                    else:
                                        pred_steatosis_status_list_leftmost.append(0)
                                    break
                            else:
                                raise Exception(f"Wrong keys in {t}")
                        else:
                            raise Exception(f"Wrong keys in {bd}")

                # print(f"pred_steatosis_status_list_leftmost={pred_steatosis_status_list_leftmost}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                current_leftmost_score = math.fabs(
                    sklearn.metrics.f1_score(steatosis_status_list, pred_steatosis_status_list_leftmost))
                # print(f"current_leftmost_score={current_leftmost_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            border_point = (max_point + min_point) / 2
            score = math.fabs(sklearn.metrics.f1_score(steatosis_status_list, pred_steatosis_status_list_init))
            rightmost_best_score = score
            rightmost_point = border_point
            current_rightmost_score = score
            current_rightmost_point = border_point

            while current_rightmost_score >= score:
                rightmost_best_score = current_rightmost_score
                rightmost_point = current_rightmost_point

                score = current_rightmost_score
                current_rightmost_point = rightmost_point + step

                pred_steatosis_status_list_rightmost = []

                for bd in whole_liver_brightness_data:
                    for t in train_data:
                        if 'nii' in bd.keys():
                            if 'nii' in t.keys():
                                if bd['nii'] == t['nii']:
                                    if type_of_average in bd.keys():
                                        content = str(bd[type_of_average])
                                        if content.replace('.', '', 1).isdigit():
                                            value = float(content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if value <= current_rightmost_point:
                                        pred_steatosis_status_list_rightmost.append(1)
                                    else:
                                        pred_steatosis_status_list_rightmost.append(0)
                                    break
                            else:
                                raise Exception(f"Wrong keys in {t}")
                        else:
                            raise Exception(f"Wrong keys in {bd}")

                # print(f"pred_steatosis_status_list_rightmost={pred_steatosis_status_list_rightmost}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                current_rightmost_score = math.fabs(
                    sklearn.metrics.f1_score(steatosis_status_list, pred_steatosis_status_list_rightmost))
                # print(f"current_rightmost_score={current_rightmost_score}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            # print(f"rightmost_point={rightmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            # print(f"leftmost_point={leftmost_point}", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            if rightmost_best_score >= leftmost_best_score:
                border_point = rightmost_point
            else:
                border_point = leftmost_point

            # print("End finding best score point", datetime.now().strftime("%H:%M:%S.%f")[:-3])

            return border_point
            # print("End most_powerful_criterion_train |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        else:
            raise Exception("Brightness list is empty")

    @staticmethod
    def most_powerful_criterion(value_of_brightness, boarder_point):

        # print("Start most_powerful_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if str(value_of_brightness).replace(".", "", 1).isdigit() or str(boarder_point).replace(".", "", 1).isdigit():
            if float(value_of_brightness) <= float(boarder_point):
                # print("End most_powerful_criterion with 1.0 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                return 1.0
            else:
                # print("End most_powerful_criterion with 0.0 |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                return 0.0
        else:
            raise ValueError

    @staticmethod
    def fuzzy_criterion(value_of_brightness, sick_intersection, healthy_intersection):
        # print("Start fuzzy_criterion |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for elem in healthy_intersection:
            if not str(elem).replace(".", "", 1).isdigit():
                raise ValueError
        for elem in sick_intersection:
            if not str(elem).replace(".", "", 1).isdigit():
                raise ValueError

        if len(sick_intersection) > 0 and len(healthy_intersection) > 0:
            raise Exception("Impossible to predict")

        if len(sick_intersection) > 0:
            intersection_max_point = max(sick_intersection)
        else:
            intersection_max_point = float("-inf")

        if len(healthy_intersection) > 0:
            intersection_min_point = min(healthy_intersection)
        else:
            intersection_min_point = float("inf")

        if value_of_brightness > intersection_max_point:
            prediction = 0.0
        elif value_of_brightness < intersection_min_point:
            prediction = 1.0
        else:
            sick_counter = 0
            for sick in sick_intersection:
                if sick >= value_of_brightness:
                    sick_counter += 1
            prediction = float(sick_counter / len(sick_intersection))

        # print(f"End fuzzy_criterion with {prediction} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return prediction

    @staticmethod
    def linear_regression(whole_study_brightness_data, whole_liver_brightness_data, train_data, values_of_brightness,
                          types_of_average, relative_types_of_average):

        # print("Start linear_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        brightness_list = []
        steatosis_status_list = []
        # print("Start training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for t in train_data:
            for i in range(len(whole_liver_brightness_data)):
                if t['nii'] == whole_liver_brightness_data[i]['nii'] and t['nii'] == \
                        whole_study_brightness_data[i]['nii']:
                    row = []
                    for k in range(len(types_of_average)):
                        row.append(float(whole_liver_brightness_data[i][types_of_average[k]]))
                    for k in range(len(relative_types_of_average)):
                        row.append(float(whole_study_brightness_data[i][relative_types_of_average[k]]))
                    brightness_list.append(row)
                    steatosis_status_list.append(float(t['ground_truth']))
                    break

        reg = LinearRegression()
        reg.fit(brightness_list, steatosis_status_list)

        # print("End training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        y_pred = reg.predict([values_of_brightness])

        # print(f"End linear_regression with {y_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return y_pred[0]

    @staticmethod
    def polynomial_regression(whole_study_brightness_data, whole_liver_brightness_data, train_data,
                              values_of_brightness, types_of_average, relative_types_of_average, degree):

        # print("Start polynomial_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        brightness_list = []
        steatosis_status_list = []
        # print("Start training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for t in train_data:
            for i in range(len(whole_liver_brightness_data)):
                if t['nii'] == whole_liver_brightness_data[i]['nii'] and t['nii'] == \
                        whole_study_brightness_data[i]['nii']:
                    row = []
                    for k in range(len(types_of_average)):
                        row.append(float(whole_liver_brightness_data[i][types_of_average[k]]))
                    for k in range(len(relative_types_of_average)):
                        row.append(float(whole_study_brightness_data[i][relative_types_of_average[k]]))
                    brightness_list.append(row)
                    steatosis_status_list.append(float(t['ground_truth']))
                    break

        poly_model = PolynomialFeatures(degree=degree)
        poly_x_values = poly_model.fit_transform(brightness_list)
        poly_model.fit(poly_x_values, steatosis_status_list)
        regression_model = LinearRegression()
        regression_model.fit(poly_x_values, steatosis_status_list)
        # print("End training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        poly_x = poly_model.fit_transform([values_of_brightness])
        y_pred = regression_model.predict(poly_x)

        # print(f"End polynomial_regression with {y_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return y_pred[0]
