import csv
import os.path
import unittest
from json import JSONDecodeError

from application.code.FileManager import FileManager
from application.test.TestHelper import TestHelper, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH


class FileManagerTest(unittest.TestCase):

    def test_load_brightness_data(self):
        paths = TestHelper.make_csv_file(path=DATA_FOLDER_PATH, file="test_brightness",
                                         data=[{"a": "a", "b": "b"}])
        full_img_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                    file_name="test_brightness.csv")
        self.assertEqual(full_img_brightness_data, [{"a": "a", "b": "b"}])

        for path in paths:
            os.remove(path)

    def test_load_brightness_data_empty_file(self):
        file_path = os.path.join(DATA_FOLDER_PATH, "test_brightness.csv")
        f = open(file_path, "a")
        f.close()

        full_img_brightness_data = FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                                                    file_name="test_brightness.csv")
        self.assertEqual(full_img_brightness_data, [])

        os.remove(file_path)

    def test_load_brightness_data_wrong_file_name(self):
        paths = TestHelper.make_csv_file(path=DATA_FOLDER_PATH, file="test_brightness",
                                         data=[{"a": "a", "b": "b"}])

        with self.assertRaises(FileExistsError):
            FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                             file_name="not_test_brightness.csv")

        for path in paths:
            os.remove(path)

    def test_load_brightness_data_wrong_data_folder_path(self):
        paths = TestHelper.make_csv_file(path=DATA_FOLDER_PATH, file="test_brightness",
                                         data=[{"a": "a", "b": "b"}])

        with self.assertRaises(FileExistsError):
            FileManager.load_brightness_data(data_folder_path="bad_folder",
                                             file_name="test_brightness.csv")

        for path in paths:
            os.remove(path)

    def test_load_brightness_data_missing_file(self):
        with self.assertRaises(FileExistsError):
            FileManager.load_brightness_data(data_folder_path=DATA_FOLDER_PATH,
                                             file_name="test_brightness.csv")

    def test_load_data_for_fuzzy_criterion(self):
        paths1 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_sick_in_intersection_test_load', data=[1])
        paths2 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_healthy_in_intersection_test_load', data=[1])

        intersection = FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                                 type_of_average="test_load")
        self.assertEqual([[1], [1]], intersection)

        for path in paths1:
            os.remove(path)
        for path in paths2:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion_empty_sick_in_intersection(self):
        empty_file_path = os.path.join(CONFIG_FOLDER_PATH, "fuzzy_criterion_train_sick_in_intersection_test_load.json")
        f = open(empty_file_path, "a")
        f.close()

        paths = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                          file='fuzzy_criterion_train_healthy_in_intersection_test_load', data=[1])

        with self.assertRaises(JSONDecodeError):
            FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                      type_of_average="test_load")

        os.remove(empty_file_path)
        for path in paths:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion_empty_healthy_in_intersection(self):
        empty_file_path = os.path.join(CONFIG_FOLDER_PATH,
                                       "fuzzy_criterion_train_healthy_in_intersection_test_load.json")
        f = open(empty_file_path, "a")
        f.close()

        paths = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                          file='fuzzy_criterion_train_sick_in_intersection_test_load', data=[1])

        with self.assertRaises(JSONDecodeError):
            FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                      type_of_average="test_load")

        os.remove(empty_file_path)
        for path in paths:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion_wrong_type_of_average(self):
        paths1 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_sick_in_intersection_test_load', data=[1])
        paths2 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_healthy_in_intersection_test_load', data=[1])

        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                      type_of_average="not_test_load")

        for path in paths1:
            os.remove(path)
        for path in paths2:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion_wrong_config_folder_path(self):
        paths1 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_sick_in_intersection_test_load', data=[1])
        paths2 = TestHelper.make_json_file(path=CONFIG_FOLDER_PATH,
                                           file='fuzzy_criterion_train_healthy_in_intersection_test_load', data=[1])

        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_fuzzy_criterion(config_folder_path="bad_folder",
                                                      type_of_average="test_load")

        for path in paths1:
            os.remove(path)
        for path in paths2:
            os.remove(path)

    def test_load_data_for_fuzzy_criterion_missing_file(self):
        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_fuzzy_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                      type_of_average="test_load")

    def test_load_data_for_most_powerful_criterion(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file='most_powerful_criterion_train_test_load',
                                         data="1.0")

        value = FileManager.load_data_for_most_powerful_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                                  type_of_average="test_load")
        self.assertEqual(value, 1.0)

        for path in paths:
            os.remove(path)

    def test_load_data_for_most_powerful_criterion_wrong_type_of_average(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file='most_powerful_criterion_train_test_load',
                                         data="1.0")

        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_most_powerful_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                              type_of_average="no_test_load")

        for path in paths:
            os.remove(path)

    def test_load_data_for_most_powerful_criterion_wrong_config_folder_path(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file='most_powerful_criterion_train_test_load',
                                         data="1.0")

        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_most_powerful_criterion(config_folder_path="bad_folder",
                                                              type_of_average="test_load")

        for path in paths:
            os.remove(path)

    def test_load_data_for_most_powerful_criterion_empty_file(self):
        empty_file_path = os.path.join(CONFIG_FOLDER_PATH,
                                       "most_powerful_criterion_train_test_load.txt")
        f = open(empty_file_path, "a")
        f.close()

        with self.assertRaises(ValueError):
            FileManager.load_data_for_most_powerful_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                              type_of_average="test_load")

        os.remove(empty_file_path)

    def test_load_data_for_most_powerful_criterion_missing_file(self):
        with self.assertRaises(FileExistsError):
            FileManager.load_data_for_most_powerful_criterion(config_folder_path=CONFIG_FOLDER_PATH,
                                                              type_of_average="test_load")

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
        TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file="test_delete_residual_files", data="Delete it!",
                                 n_copy=3)

        FileManager.delete_residual_files(substr="test_delete_residual", folder_path=CONFIG_FOLDER_PATH)

        for i in range(3):
            self.assertFalse(
                os.path.exists(os.path.join(CONFIG_FOLDER_PATH, f"test_delete_residual_files_{i + 1}.txt")))

    def test_delete_residual_files_wrong_folder_path(self):
        with self.assertRaises(Exception):
            FileManager.delete_residual_files(substr="test_delete_residual", folder_path="bad_folder")

    def test_check_dcm_only_in_folder_true(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file="test_check_dcm_in_folder", data="Check it!")

        self.assertEqual(FileManager.check_dcm_only_in_folder(folder_path=CONFIG_FOLDER_PATH, substr="test"), 1)

        for path in paths:
            os.remove(path)

    def test_check_dcm_only_in_folder_false(self):
        paths = TestHelper.make_txt_file(path=CONFIG_FOLDER_PATH, file="dest_check_dcm_in_folder", data="Check it!")

        self.assertEqual(FileManager.check_dcm_only_in_folder(folder_path=CONFIG_FOLDER_PATH, substr="test"), -1)

        for path in paths:
            os.remove(path)

    def test_check_dcm_only_in_folder_empty(self):
        self.assertEqual(FileManager.check_dcm_only_in_folder(folder_path=CONFIG_FOLDER_PATH, substr="test"), 0)

    def test_check_dcm_only_in_folder_wrong_folder_path(self):
        with self.assertRaises(Exception):
            self.assertEqual(FileManager.check_dcm_only_in_folder(folder_path="bad_folder", substr="test"), 0)

    def test_make_config(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        FileManager.make_config(data_folder_path=DATA_FOLDER_PATH, config_folder_path=CONFIG_FOLDER_PATH,
                              averages=['value'])

        self.assertTrue(os.path.exists(os.path.join(CONFIG_FOLDER_PATH, 'most_powerful_criterion_train_value.txt')))
        self.assertTrue(
            os.path.exists(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json')))
        self.assertTrue(os.path.exists(
            os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json')))

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'most_powerful_criterion_train_value.txt'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))


if __name__ == '__main__':
    unittest.main()
