import csv
import os.path
import unittest

from application.code.FileManager import FileManager
from application.test.TestHelper import TestHelper

types = ["median", "mode", "mean", "1", "3", "median_low", "median_high", "median_grouped"]
CURRENT_PATH = os.getcwd()
PARENT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
CONFIG_PATH = os.path.join(PARENT_PATH, "test", "additional_files")
DATA_PATH = os.path.join(PARENT_PATH, "test", "additional_files")


class FileManagerTest(unittest.TestCase):

    def test_load_brightness_data(self):
        TestHelper.make_csv_file(path=os.path.join(PARENT_PATH, DATA_PATH), file="test_brightness.csv",
                                 data=[{"a": "a", "b": "b"}])
        full_img_brightness_data = FileManager.load_brightness_data(data=DATA_PATH, file="test_brightness.csv")
        self.assertEqual(full_img_brightness_data, [{"a": "a", "b": "b"}])

    def test_load_data_for_fuzzy_criterion(self):
        intersection = FileManager.load_data_for_fuzzy_criterion(config=CONFIG_PATH,
                                                                 type_of_average="test")
        self.assertEqual([[1], [1]], intersection)

    def test_load_data_for_most_powerful_criterion(self):
        value = FileManager.load_data_for_most_powerful_criterion(config=CONFIG_PATH,
                                                                  type_of_average="test")
        self.assertEqual(value, 1.0)

    def test_save_data_for_fuzzy_criterion(self):
        paths = FileManager.save_data_for_fuzzy_criterion(sick_in_intersection=[], healthy_in_intersection=[],
                                                          type_of_average="test_save",
                                                          config=CONFIG_PATH)
        self.assertTrue(os.path.exists(paths[0]))
        self.assertTrue(os.path.exists(paths[1]))

        if os.path.exists(paths[0]):
            os.remove(paths[0])

        if os.path.exists(paths[1]):
            os.remove(paths[1])

    def test_save_data_for_most_powerful_criterion(self):
        path = FileManager.save_data_for_most_powerful_criterion(border_point=0, type_of_average="test_save",
                                                                 config=CONFIG_PATH)

        self.assertTrue(os.path.exists(path))

        if os.path.exists(path):
            os.remove(path)

    def test_delete_residual_files(self):

        FileManager.delete_residual_files(substr="test_delete_residual", path=os.path.join(PARENT_PATH, config))

        for i in range(3):
            self.assertFalse(os.path.exists(os.path.join(PARENT_PATH, config, f"test_delete_residual_files_{i}.nii")))


if __name__ == '__main__':
    unittest.main()
