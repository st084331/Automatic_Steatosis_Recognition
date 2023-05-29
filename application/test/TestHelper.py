import csv
import json
import os

TYPES = ["median", "mode", "mean", "1", "3", "median_low", "median_high", "median_grouped"]

CURRENT_FOLDER_PATH = os.getcwd()
PARENT_FOLDER_PATH = os.path.abspath(os.path.join(CURRENT_FOLDER_PATH, os.pardir))

CONFIG_FOLDER_PATH = os.path.join(PARENT_FOLDER_PATH, "test", "additional_files")
DATA_FOLDER_PATH = os.path.join(PARENT_FOLDER_PATH, "test", "additional_files")

TEST_STUDY_NAME_FOR_CT_HANDLER = "1.2.826.0.1.3680043.8.498.13402560764035164755255899587734776159"
TEST_STUDY_PATH_FOR_CT_HANDLER = os.path.join(DATA_FOLDER_PATH, TEST_STUDY_NAME_FOR_CT_HANDLER)

TEST_STUDY_NAME_FOR_REQUEST_HANDLER = "1.2.826.0.1.3680043.8.498.62936922154322974298059413866663358841"
TEST_STUDY_PATH_FOR_REQUEST_HANDLER = os.path.join(DATA_FOLDER_PATH, TEST_STUDY_NAME_FOR_REQUEST_HANDLER)


class TestHelper:

    @staticmethod
    def combs(a: list):
        if len(a) == 0:
            return [[]]
        cs = []
        for c in TestHelper.combs(a[1:]):
            cs += [c, c + [a[0]]]
        return cs

    @staticmethod
    def make_csv_file(path, file, data, n_copy=1):
        if not os.path.exists(path):
            os.mkdir(path)
        paths = []
        for i in range(n_copy):
            if n_copy > 1:
                file_path = os.path.join(path, f"{file}_{i + 1}.csv")
            else:
                file_path = os.path.join(path, f"{file}.csv")
            with open(file_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                for dict in data:
                    writer.writerow(dict)
            paths.append(file_path)
        return paths

    @staticmethod
    def make_txt_file(path, file, data, n_copy=1):
        if not os.path.exists(path):
            os.mkdir(path)
        paths = []
        for i in range(n_copy):
            if n_copy > 1:
                file_path = os.path.join(path, f"{file}_{i + 1}.txt")
            else:
                file_path = os.path.join(path, f"{file}.txt")
            with open(file_path, "a") as f:
                f.write(data)
                f.close()
            paths.append(file_path)
        return paths

    @staticmethod
    def make_json_file(path, file, data, n_copy=1):
        if not os.path.exists(path):
            os.mkdir(path)
        paths = []
        for i in range(n_copy):
            if n_copy > 1:
                file_path = os.path.join(path, f"{file}_{i + 1}.json")
            else:
                file_path = os.path.join(path, f"{file}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f)
            paths.append(file_path)
        return paths
