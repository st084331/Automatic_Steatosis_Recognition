import os.path
import unittest
from application.code.CT_Handler import CT_Handler
from application.test.TestHelper import TestHelper, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH, TEST_STUDY_PATH_FOR_CT_HANDLER, \
    TEST_STUDY_NAME_FOR_CT_HANDLER


class CT_HandlerTests(unittest.TestCase):

    def test_init(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)

    def test_init_wrong_folder_path(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        with self.assertRaises(Exception):
            CT_Handler(folder_path="not_folder_path", name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                       mask_output_folder_path=DATA_FOLDER_PATH,
                       dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                       cpu=True, vessels=False, verbose=False)

    def test_init_wrong_mask_output_folder_path(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        with self.assertRaises(Exception):
            CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                       mask_output_folder_path="not_mask_output_folder_path",
                       dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                       cpu=True, vessels=False, verbose=False)

    def test_init_wrong_dicom_to_nifti_output_folder_path(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        with self.assertRaises(Exception):
            CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                       mask_output_folder_path=DATA_FOLDER_PATH,
                       dicom_to_nifti_output_folder_path="dicom_to_nifti_output_folder_path",
                       cpu=True, vessels=False, verbose=False)

    def test_init_wrong_name_of_nifti_wo_extension(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        with self.assertRaises(Exception):
            CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension="",
                       mask_output_folder_path=DATA_FOLDER_PATH,
                       dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                       cpu=True, vessels=False, verbose=False)

    def test_get_whole_study_brightness_info(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        whole_study_brightness_data = handler.get_whole_study_brightness_info()
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)
        self.assertEqual(len(whole_study_brightness_data), (512 // 2 * 512 // 2 * 3))

    def test_get_three_areas_brightness_info(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        three_areas_brightness_data = handler.get_three_areas_brightness_info()
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)
        self.assertEqual([], three_areas_brightness_data)

    def test_get_two_areas_brightness_info(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        two_areas_brightness_data = handler.get_two_areas_brightness_info()
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)
        self.assertEqual([], two_areas_brightness_data)

    def test_get_one_area_brightness_info(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        one_area_brightness_data = handler.get_one_area_brightness_info()
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)
        self.assertEqual([], one_area_brightness_data)

    def test_get_random_points_brightness_info(self):
        folder_path = TEST_STUDY_PATH_FOR_CT_HANDLER
        name_of_nifti_wo_extension = TEST_STUDY_NAME_FOR_CT_HANDLER
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        list = handler.get_random_points_brightness_info()
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)
        self.assertEqual(100, len(list))


if __name__ == '__main__':
    unittest.main()
