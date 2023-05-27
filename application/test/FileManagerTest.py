import csv
import os.path
import unittest

from application.code.FileManager import FileManager
from application.test.TestHelper import TestHelper

types = ["median", "mode", "mean", "1", "3", "median_low", "median_high", "median_grouped"]
CURRENT_FOLDER_PATH = os.getcwd()
PARENT_FOLDER_PATH = os.path.abspath(os.path.join(CURRENT_FOLDER_PATH, os.pardir))
CONFIG_FOLDER_PATH = os.path.join(PARENT_FOLDER_PATH, "test", "additional_files")
DATA_FOLDER_PATH = os.path.join(PARENT_FOLDER_PATH, "test", "additional_files")


class FileManagerTest(unittest.TestCase):

    def test_load_brightness_data(self):
        paths = TestHelper.make_csv_file(path=DATA_FOLDER_PATH, file="test_brightness",
                                 data=[{"a": "a", "b": "b"}])
        full_img_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                    file_name="test_brightness.csv")
        self.assertEqual(full_img_brightness_data, [{"a": "a", "b": "b"}])

        for path in paths:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion(self):
        paths1 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH, file='fuzzy_criterion_train_sick_in_intersection_test_load', data=[1])
        paths2 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH, file='fuzzy_criterion_train_healthy_in_intersection_test_load', data=[1])

        intersection = FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                                 type_of_average="test_load")
        self.assertEqual([[1], [1]], intersection)

        for path in paths1:
            os.remove(path)
        for path in paths2:
            os.remove(path)

    def test_load_data_for_most_powerful_criterion(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file='most_powerful_criterion_train_test_load', data="1.0")

        value = FileManager.load_data_for_most_powerful_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                                  type_of_average="test_load")
        self.assertEqual(value, 1.0)

        for path in paths:
            os.remove(path)

    def test_save_data_for_fuzzy_criterion(self):
        paths = FileManager.save_data_for_fuzzy_criterion(sick_in_intersection=[], healthy_in_intersection=[],
                                                          type_of_average="test_save",
                                                          config_folder_path=CONFIG_FOLDER_PATH)
        for path in paths:
            self.assertTrue(os.path.exists(path))
            os.remove(path)


    def test_save_data_for_most_powerful_criterion(self):
        path = FileManager.save_data_for_most_powerful_criterion(border_point=0, type_of_average="test_save",
                                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_delete_residual_files(self):
        TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file="test_delete_residual_files", data="Delete it!")

        FileManager.delete_residual_files(substr="test_delete_residual", folder_path=CONFIG_FOLDER_PATH)

        for i in range(3):
            self.assertFalse(os.path.exists(os.path.join(CONFIG_FOLDER_PATH, f"test_delete_residual_files_{i+1}.txt")))


if __name__ == '__main__':
    unittest.main()
