import unittest

from application.code.FormatConverter import FormatConverter
from application.test.TestHelper import TYPES


class FormatConverterTest(unittest.TestCase):

    def test_types_of_average_to_current_types(self):
        result = FormatConverter.types_of_average_to_current_types(["Median", "Mode", "Mean", "Median low", "Median high", "Median grouped", "First quartile", 'Third quartile'])
        self.assertEqual(TYPES.sort(), result.sort())

    def test_types_of_average_to_current_types_empty(self):
        result = FormatConverter.types_of_average_to_current_types([])
        self.assertEqual([], result)

    def test_types_of_average_to_current_types_wrong_type(self):
        with self.assertRaises(Exception):
            FormatConverter.types_of_average_to_current_types(["wrong_type"])





if __name__ == '__main__':
    unittest.main()
