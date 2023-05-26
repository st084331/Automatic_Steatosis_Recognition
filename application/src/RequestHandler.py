import statistics
from datetime import datetime

from application.src.FormatConverter import FormatConverter
from application.src.Predictor import Predictor


class RequestHandler:

    @staticmethod
    def result_request(values_of_brightness, types_of_average, relative_types_of_average, method):
        # print("Start result_request |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print(f"Call FormatConverter.types_of_average_to_current_types(types_of_average={types_of_average}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        current_types = FormatConverter.types_of_average_to_current_types(types_of_average=types_of_average)

        # print(f"Call FormatConverter.types_of_average_to_current_types(types_of_average={relative_types_of_average}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        relative_current_types = FormatConverter.types_of_average_to_current_types(
            types_of_average=relative_types_of_average)

        if method == "Fuzzy criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    # print(f"End and Call Predictor.fuzzy_criterion(value_of_brightness={values_of_brightness[0]}, type_of_average={current_types[0]}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                    return Predictor.fuzzy_criterion(value_of_brightness=values_of_brightness[0],
                                                     type_of_average=current_types[0])
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Most powerful criterion":
            if len(values_of_brightness) == 1:
                if len(types_of_average) == 1:
                    # print(f"End and Call Predictor.most_powerful_criterion(value_of_brightness={values_of_brightness[0]}, type_of_average={current_types[0]}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                    return Predictor.most_powerful_criterion(value_of_brightness=values_of_brightness[0],
                                                             type_of_average=current_types[0])
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Linear regression":
            if len(values_of_brightness) >= 1:
                if len(types_of_average) >= 1:
                    # print(f"End and Call Predictor.linear_regression(values_of_brightness={values_of_brightness}, types_of_average={current_types}, relative_types_of_average={relative_current_types}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                    return Predictor.linear_regression(values_of_brightness=values_of_brightness,
                                                       types_of_average=current_types,
                                                       relative_types_of_average=relative_current_types)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        elif method == "Second degree polynomial regression":
            if len(values_of_brightness) >= 1:
                if len(types_of_average) >= 1:
                    # print(f"End and Call Predictor.polynomial_regression(values_of_brightness={values_of_brightness}, types_of_average={current_types}, relative_types_of_average={relative_current_types}) |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
                    return Predictor.polynomial_regression(values_of_brightness=values_of_brightness,
                                                           types_of_average=current_types,
                                                           relative_types_of_average=relative_current_types, degree=2)
                else:
                    raise Exception("Incorrect number of types of average")
            else:
                raise Exception("Incorrect number of brightness values")

        else:
            raise Exception(f"{method} method is not defined")

    @staticmethod
    def brightness_values_request(area, types_of_average, relative_types_of_average, handler):
        # print("Start brightness_values_request |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        if area == "Whole liver":
            brightness_list = handler.whole_liver_brightness_info()
        elif area == "Three random areas":
            brightness_list = handler.three_areas_brightness_info()
        elif area == "Two random areas":
            brightness_list = handler.two_areas_brightness_info()
        elif area == "One random area":
            brightness_list = handler.one_area_brightness_info()
        elif area == "100 random points":
            brightness_list = handler.random_points_brightness_info()
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
            relative_brightness_list = handler.full_img_brightness_info()
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
