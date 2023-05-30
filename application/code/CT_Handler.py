import os
from datetime import datetime
from random import randint
import nibabel as nib
import dicom2nifti
from typing import List

from application.code.Init import VERBOSE, VESSELS, PARENT_FOLDER_PATH, CPU
from livermask import livermask


class CT_Handler:

    def __init__(self, folder_path: str, name_of_nifti_wo_extension: str,
                 dicom_to_nifti_output_folder_path: str = PARENT_FOLDER_PATH,
                 mask_output_folder_path: str = PARENT_FOLDER_PATH,
                 cpu: bool = CPU,
                 verbose: bool = VERBOSE, vessels: bool = VESSELS):

        if not os.path.exists(folder_path):
            raise Exception("folder_path does not exist")
        if not os.path.exists(mask_output_folder_path):
            raise Exception("mask_output_folder_path does not exist")
        if not os.path.exists(dicom_to_nifti_output_folder_path):
            raise Exception("dicom_to_nifti_output_folder_path does not exist")
        if len(name_of_nifti_wo_extension) < 1:
            raise Exception("Impossible name of name_of_nifti_wo_extension")
        # print("Start CT_Handler __init__ |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        self.folder_path: str = folder_path
        self.name_of_nifti_wo_extension: str = name_of_nifti_wo_extension
        self.name_of_nifti: str = name_of_nifti_wo_extension + ".nii"
        self.mask_file_name: str = name_of_nifti_wo_extension + "-livermask2.nii"

        # Convert Dicom folder to NifTi file
        self.nii_file_path: str = self.dicom_to_nifti(output_folder_path=dicom_to_nifti_output_folder_path)

        # Getting a liver mask
        self.mask_file_path: str = self.make_mask(output_folder_path=mask_output_folder_path,
                                                  input_folder_path=dicom_to_nifti_output_folder_path,
                                                  cpu=cpu,
                                                  verbose=verbose,
                                                  vessels=vessels)

    def dicom_to_nifti(self, output_folder_path: str) -> str:

        # print("Start dicom_to_nifti |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        output_path: str = os.path.join(output_folder_path, self.name_of_nifti)
        dicom2nifti.dicom_series_to_nifti(self.folder_path, output_path, reorient_nifti=False)
        # print(f"dicom_to_nifti saved as {output} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return output_path

    def make_mask(self, output_folder_path: str, input_folder_path: str, cpu: bool, verbose: bool,
                  vessels: bool) -> str:

        # print("Start CT_Handler make_mask |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        output_folder_path_wo_extension: str = os.path.join(output_folder_path, self.name_of_nifti_wo_extension)
        input_path: str = os.path.join(input_folder_path, self.name_of_nifti)
        livermask.func(path=input_path, output=output_folder_path_wo_extension, cpu=cpu, verbose=verbose,
                       vessels=vessels)
        # print(f"make_mask saved as {output_folder_path_wo_extension} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return os.path.join(output_folder_path, self.mask_file_name)

    # Method for getting a list of hounsfield unit values of a NifTi file
    def get_whole_study_brightness_info(self) -> List[float]:

        whole_study = nib.load(self.nii_file_path)

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        whole_study_brightness = []
        # print("Start of collection whole_study_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # Step is 2 to speed up the collection process
        for z in range(0, whole_study_data.shape[0], 2):
            for y in range(0, whole_study_data.shape[1], 2):
                for x in range(0, whole_study_data.shape[2], 2):
                    whole_study_brightness.append(whole_study_data[z][y][x])
        # print("End of collection whole_study_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return whole_study_brightness

    # Method for getting a list of hounsfield unit values of whole liver
    def get_whole_liver_brightness_info(self) -> List[float]:

        mask_img = nib.load(self.mask_file_path)

        whole_study = nib.load(self.nii_file_path)

        mask_data: List[List[List[float]]] = mask_img.get_fdata()

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        # print("Start of collection whole_liver_list_of_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        whole_liver_list_of_brightness = []

        # Step is 2 to speed up the collection process
        for z in range(0, mask_data.shape[0], 2):
            for y in range(0, mask_data.shape[1], 2):
                for x in range(0, mask_data.shape[2], 2):
                    # If mask_data at this point is equal to 1, then this is the liver
                    if mask_data[z][y][x] == 1:
                        whole_liver_list_of_brightness.append(whole_study_data[z][y][x])
        # print("End of collection whole_liver_list_of_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return whole_liver_list_of_brightness

    # Method for getting a list of hounsfield unit values of three random areas of liver
    def get_three_areas_brightness_info(self) -> List[float]:

        mask_img = nib.load(self.mask_file_path)

        whole_study = nib.load(self.nii_file_path)

        mask_data: List[List[List[float]]] = mask_img.get_fdata()

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        diameter: int = min(mask_data.shape) // 10
        # print(f"Diameter is {diameter} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Start of collection three_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        three_areas_brightness = []

        for i in range(3):
            rand_z = randint(0, mask_data.shape[0] - 1)
            rand_y = randint(0, mask_data.shape[1] - 1)
            rand_x = randint(0, mask_data.shape[2] - 1)
            # Random again if the point is not from the liver
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = randint(0, mask_data.shape[0] - 1)
                rand_y = randint(0, mask_data.shape[1] - 1)
                rand_x = randint(0, mask_data.shape[2] - 1)

            # Build an area around the received point and control the exit beyond the array boundary
            min_z = int(rand_z - diameter / 2)
            if min_z < 0:
                min_z = 0
            max_z = int(rand_z + diameter / 2)
            if max_z > mask_data.shape[0]:
                max_z = mask_data.shape[0]

            min_y = int(rand_y - diameter / 2)
            if min_y < 0:
                min_y = 0
            max_y = int(rand_y + diameter / 2)
            if max_y > mask_data.shape[1]:
                max_y = mask_data.shape[1]

            min_x = int(rand_x - diameter / 2)
            if min_x < 0:
                min_x = 0
            max_x = int(rand_x + diameter / 2)
            if max_x > mask_data.shape[2]:
                max_x = mask_data.shape[2]

            for z in range(min_z, max_z):
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        # If mask_data at this point is equal to 1, then this is the liver
                        if mask_data[z][y][x] == 1:
                            three_areas_brightness.append(whole_study_data[z][y][x])
        # print("End of collection three_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return three_areas_brightness

    # Method for getting a list of hounsfield unit values of two random areas of liver
    def get_two_areas_brightness_info(self) -> List[float]:

        mask_img = nib.load(self.mask_file_path)

        whole_study = nib.load(self.nii_file_path)

        mask_data: List[List[List[float]]] = mask_img.get_fdata()

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        diameter: int = min(mask_data.shape) // 10
        # print(f"Diameter is {diameter} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        two_areas_brightness = []

        # print("Start of collection two_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for i in range(2):
            rand_z = randint(0, mask_data.shape[0] - 1)
            rand_y = randint(0, mask_data.shape[1] - 1)
            rand_x = randint(0, mask_data.shape[2] - 1)
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = randint(0, mask_data.shape[0] - 1)
                rand_y = randint(0, mask_data.shape[1] - 1)
                rand_x = randint(0, mask_data.shape[2] - 1)

            min_z = int(rand_z - diameter / 2)
            if min_z < 0:
                min_z = 0
            max_z = int(rand_z + diameter / 2)
            if max_z > mask_data.shape[0]:
                max_z = mask_data.shape[0]

            min_y = int(rand_y - diameter / 2)
            if min_y < 0:
                min_y = 0
            max_y = int(rand_y + diameter / 2)
            if max_y > mask_data.shape[1]:
                max_y = mask_data.shape[1]

            min_x = int(rand_x - diameter / 2)
            if min_x < 0:
                min_x = 0
            max_x = int(rand_x + diameter / 2)
            if max_x > mask_data.shape[2]:
                max_x = mask_data.shape[2]

            for z in range(min_z, max_z):
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        # If mask_data at this point is equal to 1, then this is the liver
                        if mask_data[z][y][x] == 1:
                            two_areas_brightness.append(whole_study_data[z][y][x])
        # print("End of collection two_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return two_areas_brightness

    # Method for getting a list of hounsfield unit values of one random area of liver
    def get_one_area_brightness_info(self) -> List[float]:

        mask_img = nib.load(self.mask_file_path)

        whole_study = nib.load(self.nii_file_path)

        mask_data: List[List[List[float]]] = mask_img.get_fdata()

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        diameter: int = min(mask_data.shape) // 10
        # print(f"Diameter is {diameter} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Start of collection one_area_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        one_area_brightness = []
        rand_z = randint(0, mask_data.shape[0] - 1)
        rand_y = randint(0, mask_data.shape[1] - 1)
        rand_x = randint(0, mask_data.shape[2] - 1)
        while mask_data[rand_z][rand_y][rand_x] != 1:
            rand_z = randint(0, mask_data.shape[0] - 1)
            rand_y = randint(0, mask_data.shape[1] - 1)
            rand_x = randint(0, mask_data.shape[2] - 1)

        min_z = int(rand_z - diameter / 2)
        if min_z < 0:
            min_z = 0
        max_z = int(rand_z + diameter / 2)
        if max_z > mask_data.shape[0]:
            max_z = mask_data.shape[0]

        min_y = int(rand_y - diameter / 2)
        if min_y < 0:
            min_y = 0
        max_y = int(rand_y + diameter / 2)
        if max_y > mask_data.shape[1]:
            max_y = mask_data.shape[1]

        min_x = int(rand_x - diameter / 2)
        if min_x < 0:
            min_x = 0
        max_x = int(rand_x + diameter / 2)
        if max_x > mask_data.shape[2]:
            max_x = mask_data.shape[2]

        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    # If mask_data at this point is equal to 1, then this is the liver
                    if mask_data[z][y][x] == 1:
                        one_area_brightness.append(whole_study_data[z][y][x])
        # print("End of collection one_area_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return one_area_brightness

    # Method for getting a list of hounsfield unit values of 100 random points of liver
    def get_random_points_brightness_info(self) -> List[float]:

        mask_img = nib.load(self.mask_file_path)

        whole_study = nib.load(self.nii_file_path)

        mask_data: List[List[List[float]]] = mask_img.get_fdata()

        whole_study_data: List[List[List[float]]] = whole_study.get_fdata()

        # print("Start of collection random_points_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        random_points_brightness = []

        for i in range(100):
            rand_z = randint(0, mask_data.shape[0] - 1)
            rand_y = randint(0, mask_data.shape[1] - 1)
            rand_x = randint(0, mask_data.shape[2] - 1)
            # Random again if the point is not from the liver
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = randint(0, mask_data.shape[0] - 1)
                rand_y = randint(0, mask_data.shape[1] - 1)
                rand_x = randint(0, mask_data.shape[2] - 1)
            random_points_brightness.append(whole_study_data[rand_z][rand_y][rand_x])
        # print("End of collection random_points_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return random_points_brightness
