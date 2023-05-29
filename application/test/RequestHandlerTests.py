import os
import unittest

from application.code.CT_Handler import CT_Handler
from application.code.FileManager import FileManager
from application.code.Init import AREAS, AVERAGES, METHODS
from application.code.RequestHandler import RequestHandler
from application.test.TestHelper import TEST_STUDY_PATH_FOR_REQUEST_HANDLER, CONFIG_FOLDER_PATH, TestHelper


class RequestHandlerTest(unittest.TestCase):

    def test_brightness_values_request(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        folder_struct = os.path.split(folder_path)
        name_of_nifti_wo_extension = folder_struct[-1]
        dicom_to_nifti_output_folder_path = CONFIG_FOLDER_PATH
        mask_output_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        handler = CT_Handler(folder_path=folder_path,
                             name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             dicom_to_nifti_output_folder_path=dicom_to_nifti_output_folder_path,
                             mask_output_folder_path=mask_output_folder_path)
        relative_types_of_average = AVERAGES
        types_of_average = AVERAGES
        for area in AREAS:
            result = RequestHandler.brightness_values_request(area=area,
                                                              relative_types_of_average=relative_types_of_average,
                                                              types_of_average=types_of_average, handler=handler)
            self.assertEqual(len(relative_types_of_average) + len(types_of_average), len(result))
            for elem in result:
                self.assertTrue(elem != 0)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_brightness_values_request_wrong_area(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        folder_struct = os.path.split(folder_path)
        name_of_nifti_wo_extension = folder_struct[-1]
        dicom_to_nifti_output_folder_path = CONFIG_FOLDER_PATH
        mask_output_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH

        handler = CT_Handler(folder_path=folder_path,
                             name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             dicom_to_nifti_output_folder_path=dicom_to_nifti_output_folder_path,
                             mask_output_folder_path=mask_output_folder_path)
        relative_types_of_average = AVERAGES
        types_of_average = AVERAGES
        with self.assertRaises(Exception):
            RequestHandler.brightness_values_request(area="not_area",
                                                     relative_types_of_average=relative_types_of_average,
                                                     types_of_average=types_of_average, handler=handler)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_brightness_values_request_wrong_types_of_average(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        folder_struct = os.path.split(folder_path)
        name_of_nifti_wo_extension = folder_struct[-1]
        dicom_to_nifti_output_folder_path = CONFIG_FOLDER_PATH
        mask_output_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH

        handler = CT_Handler(folder_path=folder_path,
                             name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             dicom_to_nifti_output_folder_path=dicom_to_nifti_output_folder_path,
                             mask_output_folder_path=mask_output_folder_path)
        relative_types_of_average = AVERAGES

        with self.assertRaises(Exception):
            RequestHandler.brightness_values_request(area="100 random points",
                                                     relative_types_of_average=relative_types_of_average,
                                                     types_of_average=["not_type_of_average"], handler=handler)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_brightness_values_request_wrong_relative_types_of_average(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        folder_struct = os.path.split(folder_path)
        name_of_nifti_wo_extension = folder_struct[-1]
        dicom_to_nifti_output_folder_path = CONFIG_FOLDER_PATH
        mask_output_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH

        handler = CT_Handler(folder_path=folder_path,
                             name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             dicom_to_nifti_output_folder_path=dicom_to_nifti_output_folder_path,
                             mask_output_folder_path=mask_output_folder_path)
        types_of_average = AVERAGES
        with self.assertRaises(Exception):
            RequestHandler.brightness_values_request(area="100 random points",
                                                     relative_types_of_average=["not_relative_types_of_average"],
                                                     types_of_average=types_of_average, handler=handler)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_folder_path(self):
        folder_path = "NOT_TEST_STUDY_PATH_FOR_REQUEST_HANDLER"
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = AVERAGES
        relative_types_of_average = []
        method = METHODS[0]
        area = AREAS[-1]
        with self.assertRaises(Exception):
            RequestHandler.result_request(types_of_average=types_of_average,
                                          relative_types_of_average=relative_types_of_average,
                                          method=method,
                                          folder_path=folder_path,
                                          config_folder_path=config_folder_path,
                                          area=area,
                                          parent_folder_path=parent_folder_path)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_config_folder_path(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = "NOT_CONFIG_FOLDER_PATH"
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = AVERAGES
        relative_types_of_average = []
        method = METHODS[0]
        area = AREAS[-1]
        with self.assertRaises(Exception):
            RequestHandler.result_request(types_of_average=types_of_average,
                                          relative_types_of_average=relative_types_of_average,
                                          method=method,
                                          folder_path=folder_path,
                                          config_folder_path=config_folder_path,
                                          area=area,
                                          parent_folder_path=parent_folder_path)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_parent_folder_path(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = "NOT_PARENT_FOLDER_PATH"
        types_of_average = AVERAGES
        relative_types_of_average = []
        method = METHODS[0]
        area = AREAS[-1]
        with self.assertRaises(Exception):
            RequestHandler.result_request(types_of_average=types_of_average,
                                          relative_types_of_average=relative_types_of_average,
                                          method=method,
                                          folder_path=folder_path,
                                          config_folder_path=config_folder_path,
                                          area=area,
                                          parent_folder_path=parent_folder_path)
        parent_folder_path = CONFIG_FOLDER_PATH
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_types_of_average_len(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = []
        relative_types_of_average = [AVERAGES[0]]
        area = AREAS[-1]
        for method in METHODS:
            with self.assertRaises(Exception):
                RequestHandler.result_request(types_of_average=types_of_average,
                                              relative_types_of_average=relative_types_of_average,
                                              method=method,
                                              folder_path=folder_path,
                                              config_folder_path=config_folder_path,
                                              area=area,
                                              parent_folder_path=parent_folder_path)
            FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_values_of_brightness_len(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = []
        relative_types_of_average = []
        area = AREAS[-1]
        for method in METHODS:
            with self.assertRaises(Exception):
                RequestHandler.result_request(types_of_average=types_of_average,
                                              relative_types_of_average=relative_types_of_average,
                                              method=method,
                                              folder_path=folder_path,
                                              config_folder_path=config_folder_path,
                                              area=area,
                                              parent_folder_path=parent_folder_path)
            FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_method(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = AVERAGES[0]
        relative_types_of_average = []
        area = AREAS[-1]
        method = "Not Method"
        with self.assertRaises(Exception):
            RequestHandler.result_request(types_of_average=types_of_average,
                                          relative_types_of_average=relative_types_of_average,
                                          method=method,
                                          folder_path=folder_path,
                                          config_folder_path=config_folder_path,
                                          area=area,
                                          parent_folder_path=parent_folder_path)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)

    def test_result_request_wrong_regression_method(self):
        folder_path = TEST_STUDY_PATH_FOR_REQUEST_HANDLER
        config_folder_path = CONFIG_FOLDER_PATH
        parent_folder_path = CONFIG_FOLDER_PATH
        types_of_average = AVERAGES[0]
        relative_types_of_average = []
        area = AREAS[-1]
        method = "Not regression Method"
        with self.assertRaises(Exception):
            RequestHandler.result_request(types_of_average=types_of_average,
                                          relative_types_of_average=relative_types_of_average,
                                          method=method,
                                          folder_path=folder_path,
                                          config_folder_path=config_folder_path,
                                          area=area,
                                          parent_folder_path=parent_folder_path)
        FileManager.delete_residual_files(substr=".nii", folder_path=parent_folder_path)


if __name__ == '__main__':
    FileManager.delete_residual_files(substr=".nii", folder_path=CONFIG_FOLDER_PATH)
    unittest.main()
