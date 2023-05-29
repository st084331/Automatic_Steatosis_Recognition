import os.path
import unittest
from application.code.CT_Handler import CT_Handler
from application.test.TestHelper import TestHelper, DATA_FOLDER_PATH, CONFIG_FOLDER_PATH, TEST_STUDY_PATH, TEST_STUDY_NAME


class CT_HandlerTests(unittest.TestCase):

    def test_init(self):
        folder_path = TEST_STUDY_PATH
        name_of_nifti_wo_extension = TEST_STUDY_NAME
        handler = CT_Handler(folder_path=folder_path, name_of_nifti_wo_extension=name_of_nifti_wo_extension,
                             mask_output_folder_path=DATA_FOLDER_PATH,
                             dicom_to_nifti_output_folder_path=DATA_FOLDER_PATH,
                             cpu=True, vessels=False, verbose=False)
        self.assertTrue(os.path.exists(handler.nii_file_path))
        os.remove(handler.nii_file_path)
        self.assertTrue(os.path.exists(handler.mask_file_path))
        os.remove(handler.mask_file_path)


if __name__ == '__main__':
    unittest.main()
