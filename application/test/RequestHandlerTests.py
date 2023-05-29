import unittest
from application.code.RequestHandler import RequestHandler


class RequestHandlerTest(unittest.TestCase):
    def test_brightness_values_request(self):
        RequestHandler.brightness_values_request()


if __name__ == '__main__':
    unittest.main()
