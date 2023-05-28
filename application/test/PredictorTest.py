import os
import unittest

from application.code.FileManager import FileManager
from application.code.Predictor import Predictor
from application.test.TestHelper import TestHelper, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH


class PredictorTest(unittest.TestCase):

    def test_fuzzy_criterion_train(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        result = Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual([[3.4], [3.5]], result)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))

    def test_fuzzy_criterion_train_empty_intersection(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0}])

        result = Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual([[], []], result)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))

    def test_fuzzy_criterion_train_empty_whole_liver_file(self):
        file_path = os.path.join(CONFIG_FOLDER_PATH, "whole_liver.csv")
        f = open(file_path, "a")
        f.close()

        paths = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                         data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0}])

        result = Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual([[], []], result)

        for p in paths:
            os.remove(p)
        os.remove(file_path)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))

    def test_fuzzy_criterion_train_empty_train_file(self):
        file_path = os.path.join(CONFIG_FOLDER_PATH, "train.csv")
        f = open(file_path, "a")
        f.close()

        paths = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                         data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 0.0}])

        result = Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual([[], []], result)

        for p in paths:
            os.remove(p)
        os.remove(file_path)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))

    def test_fuzzy_criterion_train_empty_files(self):
        file_path1 = os.path.join(CONFIG_FOLDER_PATH, "train.csv")
        f = open(file_path1, "a")
        f.close()

        file_path2 = os.path.join(CONFIG_FOLDER_PATH, "whole_liver.csv")
        f = open(file_path2, "a")
        f.close()

        result = Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                 config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual([[], []], result)

        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_sick_in_intersection_value.json'))
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'fuzzy_criterion_train_healthy_in_intersection_value.json'))

    def test_fuzzy_criterion_train_wrong_type_of_average(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.fuzzy_criterion_train(type_of_average="not_value", data_folder_path=DATA_FOLDER_PATH,
                                            config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_fuzzy_criterion_train_wrong_keys_in_train_file(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"not_nii": "a", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                            config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_fuzzy_criterion_train_wrong_keys_in_whole_liver_file(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"not_nii": "a", "value": 1.0}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.fuzzy_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                            config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_most_powerful_criterion_train(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 2.0},
                                                {"nii": "c", "value": 3.0}, {"nii": "d", "value": 4.0},
                                                {"nii": "e", "value": 5.0}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        result = Predictor.most_powerful_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                         config_folder_path=CONFIG_FOLDER_PATH)

        self.assertEqual(3.9, round(result, 1))

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)
        os.remove(os.path.join(CONFIG_FOLDER_PATH, 'most_powerful_criterion_train_value.txt'))

    def test_most_powerful_criterion_train_wrong_keys_in_whole_liver_file(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"not_nii": "a", "value": 1.0}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_most_powerful_criterion_train_wrong_keys_in_train_file(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"not_nii": "a", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value", data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_most_powerful_criterion_train_wrong_type_of_average(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="not_value", data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        for p in paths2:
            os.remove(p)
        for p in paths1:
            os.remove(p)

    def test_most_powerful_criterion_train_empty_files(self):
        file_path1 = os.path.join(CONFIG_FOLDER_PATH, "train.csv")
        f = open(file_path1, "a")
        f.close()

        file_path2 = os.path.join(CONFIG_FOLDER_PATH, "whole_liver.csv")
        f = open(file_path2, "a")
        f.close()

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        os.remove(file_path1)
        os.remove(file_path2)

    def test_most_powerful_criterion_train_empty_train_file(self):
        file_path2 = os.path.join(CONFIG_FOLDER_PATH, "train.csv")
        f = open(file_path2, "a")
        f.close()

        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        os.remove(file_path2)
        for p in paths1:
            os.remove(p)

    def test_most_powerful_criterion_whole_liver_empty_file(self):
        file_path2 = os.path.join(CONFIG_FOLDER_PATH, "train.csv")
        f = open(file_path2, "a")
        f.close()

        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    data_folder_path=DATA_FOLDER_PATH,
                                                    config_folder_path=CONFIG_FOLDER_PATH)

        os.remove(file_path2)
        for p in paths1:
            os.remove(p)

    def test_make_config(self):
        paths1 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="whole_liver",
                                          data=[{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                                {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                                {"nii": "e", "value": 3.4}])

        paths2 = TestHelper.make_csv_file(path=CONFIG_FOLDER_PATH, file="train",
                                          data=[{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                                                {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                                                {"nii": "e", "ground_truth": 1.0}])

        Predictor.make_config(data_folder_path=DATA_FOLDER_PATH, config_folder_path=CONFIG_FOLDER_PATH,
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
