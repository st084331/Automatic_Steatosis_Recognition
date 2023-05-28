import os
import unittest

from application.code.Predictor import Predictor
from application.test.TestHelper import TestHelper, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH


class PredictorTest(unittest.TestCase):

    def test_fuzzy_criterion_train(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]
        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=whole_liver_brightness_data,
                                                 train_data=train_data)

        self.assertEqual([[4.0, 3.4], [3.0, 3.5]], result)

    def test_fuzzy_criterion_train_empty_intersection(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=whole_liver_brightness_data,
                                                 train_data=train_data)

        self.assertEqual([[], []], result)

    def test_fuzzy_criterion_train_empty_sick_intersection(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0}]

        train_data = [{"nii": "a", "ground_truth": 0.0}, {"nii": "b", "ground_truth": 0.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=whole_liver_brightness_data,
                                                 train_data=train_data)

        self.assertEqual([[], [1.0, 3.0]], result)

    def test_fuzzy_criterion_train_empty_healthy_intersection(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 1.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=whole_liver_brightness_data,
                                                 train_data=train_data)

        self.assertEqual([[1.0, 3.0], []], result)

    def test_fuzzy_criterion_train_empty_whole_liver_data(self):
        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=[],
                                                 train_data=train_data)

        self.assertEqual([[], []], result)

    def test_fuzzy_criterion_train_empty_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 0.0}]

        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=whole_liver_brightness_data,
                                                 train_data=[])

        self.assertEqual([[], []], result)

    def test_fuzzy_criterion_train_empty_lists(self):
        result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                 whole_liver_brightness_data=[],
                                                 train_data=[])

        self.assertEqual([[], []], result)

    def test_fuzzy_criterion_train_wrong_type_of_average(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            result = Predictor.fuzzy_criterion_train(type_of_average="not_value",
                                                     whole_liver_brightness_data=whole_liver_brightness_data,
                                                     train_data=train_data)

    def test_fuzzy_criterion_train_wrong_keys_in_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"not_nii": "a", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                     whole_liver_brightness_data=whole_liver_brightness_data,
                                                     train_data=train_data)

    def test_fuzzy_criterion_train_wrong_keys_in_whole_liver_file(self):
        whole_liver_brightness_data = [{"not_nii": "a", "value": 1.0}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            result = Predictor.fuzzy_criterion_train(type_of_average="value",
                                                     whole_liver_brightness_data=whole_liver_brightness_data,
                                                     train_data=train_data)

    def test_fuzzy_criterion_train_train_wrong_type_of_ground_truth(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"nii": "a", "ground_truth": "a"}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.fuzzy_criterion_train(type_of_average="value",
                                            whole_liver_brightness_data=whole_liver_brightness_data,
                                            train_data=train_data)

    def test_fuzzy_criterion_train_wrong_nii_key_in_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"not_nii": "a", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.fuzzy_criterion_train(type_of_average="value",
                                            whole_liver_brightness_data=whole_liver_brightness_data,
                                            train_data=train_data)

    def test_most_powerful_criterion_train(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 2.0},
                                       {"nii": "c", "value": 3.0}, {"nii": "d", "value": 4.0},
                                       {"nii": "e", "value": 5.0}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        result = Predictor.most_powerful_criterion_train(type_of_average="value",
                                                         whole_liver_brightness_data=whole_liver_brightness_data,
                                                         train_data=train_data)

        self.assertEqual(3.9, round(result, 1))

    def test_most_powerful_criterion_train_wrong_keys_in_whole_liver_file(self):
        whole_liver_brightness_data = [{"not_nii": "a", "value": 1.0}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=train_data)

    def test_most_powerful_criterion_train_wrong_nii_key_in_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"not_nii": "a", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=train_data)

    def test_most_powerful_criterion_train_wrong_ground_truth_key_in_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"nii": "a", "not_ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=train_data)

    def test_most_powerful_criterion_train_wrong_type_of_average(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="not_value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=train_data)

    def test_most_powerful_criterion_train_wrong_type_of_ground_truth(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        train_data = [{"nii": "a", "ground_truth": "a"}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=train_data)

    def test_most_powerful_criterion_train_empty_lists(self):
        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=[],
                                                    train_data=[])

    def test_most_powerful_criterion_train_empty_train_list(self):
        whole_liver_brightness_data = [{"nii": "a", "value": 1.0}, {"nii": "b", "value": 3.0},
                                       {"nii": "c", "value": 4.0}, {"nii": "d", "value": 3.5},
                                       {"nii": "e", "value": 3.4}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=whole_liver_brightness_data,
                                                    train_data=[])

    def test_most_powerful_criterion_whole_liver_empty_list(self):
        train_data = [{"nii": "a", "ground_truth": 1.0}, {"nii": "b", "ground_truth": 0.0},
                      {"nii": "c", "ground_truth": 1.0}, {"nii": "d", "ground_truth": 0.0},
                      {"nii": "e", "ground_truth": 1.0}]

        with self.assertRaises(Exception):
            Predictor.most_powerful_criterion_train(type_of_average="value",
                                                    whole_liver_brightness_data=[],
                                                    train_data=train_data)

    def test_most_powerful_criterion_true(self):
        result = Predictor.most_powerful_criterion(value_of_brightness=1.0, boarder_point=2.0)
        self.assertEqual(1.0, result)

    def test_most_powerful_criterion_false(self):
        result = Predictor.most_powerful_criterion(value_of_brightness=3.0, boarder_point=2.0)
        self.assertEqual(0.0, result)

    def test_most_powerful_criterion_wrong_value_of_brightness(self):
        with self.assertRaises(ValueError):
            Predictor.most_powerful_criterion(value_of_brightness="a", boarder_point=2.0)

    def test_most_powerful_criterion_wrong_boarder_point(self):
        with self.assertRaises(ValueError):
            Predictor.most_powerful_criterion(value_of_brightness=1.0, boarder_point="b")

    def test_fuzzy_criterion(self):
        self.assertEqual(0.25, Predictor.fuzzy_criterion(value_of_brightness=3.6, sick_intersection=[4.0, 3.4],
                                                         healthy_intersection=[3.0, 3.5]))


if __name__ == '__main__':
    unittest.main()
