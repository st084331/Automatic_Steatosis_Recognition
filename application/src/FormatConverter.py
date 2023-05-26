from datetime import datetime


class FormatConverter:

    @staticmethod
    def types_of_average_to_current_types(types_of_average):
        # print(f"Start types_of_average_to_current_types: {types_of_average} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        current_types = []
        for type_of_average in types_of_average:
            if type_of_average == "Median":
                current_type = "median"
            elif type_of_average == "Mode":
                current_type = "mode"
            elif type_of_average == "Mean":
                current_type = "mean"
            elif type_of_average == "Median low":
                current_type = "median_low"
            elif type_of_average == "Median high":
                current_type = "median_high"
            elif type_of_average == "Median grouped":
                current_type = "median_grouped"
            elif type_of_average == "First quartile":
                current_type = "1"
            elif type_of_average == "Third quartile":
                current_type = "3"
            else:
                raise Exception(f"{type_of_average} type of average is not defined")
            current_types.append(current_type)

        # print(f"End types_of_average_to_current_types: {current_types} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return current_types
