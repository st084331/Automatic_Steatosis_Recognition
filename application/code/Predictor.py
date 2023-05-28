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
                                bd_content = str(bd[type_of_average])
                                if str(bd_content).replace('.', '', 1).isdigit():
                                    bd_value = float(bd_content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception(f"{type_of_average} type of average does not exist")

                            if 'ground_truth' in t.keys():
                                t_content = t['ground_truth']
                                if str(t_content).replace('.', '', 1).isdigit():
                                    t_value = float(t_content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception("No ground_truth key in train element")

                            if t_value == 0.0:
                                brightness_of_healthy_patients.append(bd_value)
                            else:
                                brightness_of_sick_patients.append(bd_value)
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
                                bd_content = str(bd[type_of_average])
                                if str(bd_content).replace('.', '', 1).isdigit():
                                    bd_value = float(bd_content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception(f"{type_of_average} type of average does not exist")

                            brightness_list.append(bd_value)
                            if 'ground_truth' in t.keys():
                                t_content = t['ground_truth']
                                if str(t_content).replace('.', '', 1).isdigit():
                                    t_value = float(t_content)
                                else:
                                    raise ValueError
                            else:
                                raise Exception("No ground_truth key in train element")
                            steatosis_status_list.append(t_value)
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
                                    bd_content = str(bd[type_of_average])
                                    if str(bd_content).replace('.', '', 1).isdigit():
                                        bd_value = float(bd_content)
                                    else:
                                        raise ValueError
                                else:
                                    raise Exception(f"{type_of_average} type of average does not exist")
                                if bd_value <= border_point:
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
                                        bd_content = str(bd[type_of_average])
                                        if str(bd_content).replace('.', '', 1).isdigit():
                                            bd_value = float(bd_content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if bd_value <= current_leftmost_point:
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
                                        bd_content = str(bd[type_of_average])
                                        if str(bd_content).replace('.', '', 1).isdigit():
                                            bd_value = float(bd_content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type_of_average} type of average does not exist")
                                    if bd_value <= current_rightmost_point:
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
        if not str(value_of_brightness).replace(".", "", 1).isdigit():
            raise ValueError

        if len(sick_intersection) == 0 and len(healthy_intersection) == 0:
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
            prediction = float(sick_counter / (len(sick_intersection) + len(healthy_intersection)))

        # print(f"End fuzzy_criterion with {prediction} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return prediction

    @staticmethod
    def regression_data_maker(whole_study_brightness_data, whole_liver_brightness_data, train_data, types_of_average,
                              relative_types_of_average):
        brightness_list = []
        steatosis_status_list = []
        # print("Start training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if len(relative_types_of_average) > 0:
            for t in train_data:
                for wl in whole_liver_brightness_data:
                    for ws in whole_study_brightness_data:
                        if 'nii' in wl.keys():
                            if 'nii' in ws.keys():
                                if 'nii' in t.keys():
                                    if t['nii'] == wl['nii'] and t['nii'] == ws['nii']:
                                        row = []
                                        for type in types_of_average:
                                            if type in wl.keys():
                                                wl_content = str(wl[type])
                                                if str(wl_content).replace('.', '', 1).isdigit():
                                                    wl_value = float(wl_content)
                                                else:
                                                    raise ValueError
                                            else:
                                                raise Exception(f"{type} type of average does not exist")
                                            row.append(wl_value)
                                        for type in relative_types_of_average:
                                            if type in ws.keys():
                                                ws_content = str(ws[type])
                                                if str(ws_content).replace('.', '', 1).isdigit():
                                                    ws_value = float(ws_content)
                                                else:
                                                    raise ValueError
                                            else:
                                                raise Exception(f"{type} type of average does not exist")
                                            row.append(ws_value)
                                        brightness_list.append(row)
                                        if 'ground_truth' in t.keys():
                                            t_content = t['ground_truth']
                                            if str(t_content).replace('.', '', 1).isdigit():
                                                t_value = float(t_content)
                                            else:
                                                raise ValueError
                                        else:
                                            raise Exception("No ground_truth key in train element")
                                        steatosis_status_list.append(t_value)
                                        break
                                else:
                                    raise Exception(f"Wrong keys in {t}")
                            else:
                                raise Exception(f"Wrong keys in {ws}")
                        else:
                            raise Exception(f"Wrong keys in {wl}")
        else:
            for t in train_data:
                for wl in whole_liver_brightness_data:
                    if 'nii' in wl.keys():
                        if 'nii' in t.keys():
                            if t['nii'] == wl['nii']:
                                row = []
                                for type in types_of_average:
                                    if type in wl.keys():
                                        wl_content = str(wl[type])
                                        if str(wl_content).replace('.', '', 1).isdigit():
                                            wl_value = float(wl_content)
                                        else:
                                            raise ValueError
                                    else:
                                        raise Exception(f"{type} type of average does not exist")
                                    row.append(wl_value)
                                brightness_list.append(row)
                                if 'ground_truth' in t.keys():
                                    t_content = t['ground_truth']
                                    if str(t_content).replace('.', '', 1).isdigit():
                                        t_value = float(t_content)
                                    else:
                                        raise ValueError
                                else:
                                    raise Exception("No ground_truth key in train element")
                                steatosis_status_list.append(t_value)
                                break
                        else:
                            raise Exception(f"Wrong keys in {t}")
                    else:
                        raise Exception(f"Wrong keys in {wl}")

        return [brightness_list, steatosis_status_list]

    @staticmethod
    def linear_regression(values_of_brightness, whole_study_brightness_data, whole_liver_brightness_data, train_data,
                          types_of_average, relative_types_of_average):

        # print("Start linear_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_list, steatosis_status_list = Predictor.regression_data_maker(whole_study_brightness_data,
                                                                                 whole_liver_brightness_data,
                                                                                 train_data, types_of_average,
                                                                                 relative_types_of_average)
        if len(brightness_list) == 0 or len(steatosis_status_list) == 0:
            raise Exception("Impossible to predict")

        # print("Start training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        reg = LinearRegression()
        reg.fit(brightness_list, steatosis_status_list)

        # print("End training linear regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        result_pred = reg.predict([values_of_brightness])

        # print(f"End linear_regression with {result_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return result_pred[0]

    @staticmethod
    def polynomial_regression(whole_study_brightness_data, whole_liver_brightness_data, train_data,
                              values_of_brightness, types_of_average, relative_types_of_average, degree):

        # print("Start polynomial_regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        brightness_list, steatosis_status_list = Predictor.regression_data_maker(whole_study_brightness_data,
                                                                                 whole_liver_brightness_data,
                                                                                 train_data, types_of_average,
                                                                                 relative_types_of_average)
        if len(brightness_list) == 0 or len(steatosis_status_list) == 0:
            raise Exception("Impossible to predict")
        # print("Start training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        poly_model = PolynomialFeatures(degree=degree)
        poly_x_values = poly_model.fit_transform(brightness_list)
        poly_model.fit(poly_x_values, steatosis_status_list)
        regression_model = LinearRegression()
        regression_model.fit(poly_x_values, steatosis_status_list)
        # print("End training polynomial regression |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        poly_x = poly_model.fit_transform([values_of_brightness])
        result_pred = regression_model.predict(poly_x)

        # print(f"End polynomial_regression with {result_pred[0]} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return result_pred[0]
