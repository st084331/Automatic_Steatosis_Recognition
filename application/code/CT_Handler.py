import os
from datetime import datetime
from random import randint
import nibabel as nib
import dicom2nifti

from application.code.Init import VERBOSE, VESSELS, PARENT_FOLDER_PATH, CPU
from livermask import livermask


class CT_Handler:

    def __init__(self, folder, name_of_nifti_wo_extension, dicom_to_nifti_output_folder=PARENT_FOLDER_PATH,
                 mask_output_folder=PARENT_FOLDER_PATH, mask_input_folder=PARENT_FOLDER_PATH, cpu=CPU,
                 verbose=VERBOSE, vessels=VESSELS):

        # print("Start CT_Handler __init__ |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        self.folder = folder
        self.name_of_nifti_wo_extension = name_of_nifti_wo_extension
        self.name_of_nifti = name_of_nifti_wo_extension + ".nii"
        self.mask_file_name = name_of_nifti_wo_extension + "-livermask2.nii"

        self.nii_file_path = self.dicom_to_nifti(output_folder=dicom_to_nifti_output_folder)

        self.mask_file_path = self.make_mask(output_folder=mask_output_folder, input_folder=mask_input_folder, cpu=cpu,
                                             verbose=verbose,
                                             vessels=vessels)

    def dicom_to_nifti(self, output_folder):

        # print("Start dicom_to_nifti |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        output_path = os.path.join(output_folder, self.name_of_nifti)
        dicom2nifti.dicom_series_to_nifti(self.folder, output_path, reorient_nifti=False)
        # print(f"dicom_to_nifti saved as {output} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return output_path

    def make_mask(self, output_folder, input_folder, cpu, verbose, vessels):

        # print("Start CT_Handler make_mask |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        output_folder_wo_extension = os.path.join(output_folder, self.name_of_nifti_wo_extension)
        input = os.path.join(input_folder, self.name_of_nifti)
        livermask.func(path=input, output=output_folder_wo_extension, cpu=cpu, verbose=verbose, vessels=vessels)
        # print(f"make_mask saved as {output} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return os.path.join(output_folder, self.mask_file_name)

    def get_full_img_brightness_info(self):

        full_img = nib.load(self.nii_file_path)

        full_data = full_img.get_fdata()

        full_img_brightness = []

        # print("Start of collection full_img_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        for z in range(0, full_data.shape[0], 2):
            for y in range(0, full_data.shape[1], 2):
                for x in range(0, full_data.shape[2], 2):
                    full_img_brightness.append(full_data[z][y][x])
        # print("End of collection full_img_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return full_img_brightness

    def get_whole_liver_brightness_info(self):

        mask_img = nib.load(self.mask_file_path)

        full_img = nib.load(self.nii_file_path)

        mask_data = mask_img.get_fdata()

        full_data = full_img.get_fdata()

        # print("Start of collection whole_liver_list_of_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        whole_liver_list_of_brightness = []

        for z in range(0, mask_data.shape[0], 2):
            for y in range(0, mask_data.shape[1], 2):
                for x in range(0, mask_data.shape[2], 2):
                    if mask_data[z][y][x] == 1:
                        whole_liver_list_of_brightness.append(full_data[z][y][x])
        # print("End of collection whole_liver_list_of_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return whole_liver_list_of_brightness

    def get_three_areas_brightness_info(self):

        mask_img = nib.load(self.mask_file_path)

        full_img = nib.load(self.nii_file_path)

        mask_data = mask_img.get_fdata()

        full_data = full_img.get_fdata()

        diameter = int(min(mask_data.shape) / 10)
        # print(f"Diameter is {diameter} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        # print("Start of collection three_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        three_areas_brightness = []

        for i in range(3):
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
                        if mask_data[z][y][x] == 1:
                            three_areas_brightness.append(full_data[z][y][x])
        # print("End of collection three_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return three_areas_brightness

    def get_two_areas_brightness_info(self):

        mask_img = nib.load(self.mask_file_path)

        full_img = nib.load(self.nii_file_path)

        mask_data = mask_img.get_fdata()

        full_data = full_img.get_fdata()

        diameter = int(min(mask_data.shape) / 10)
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
                        if mask_data[z][y][x] == 1:
                            two_areas_brightness.append(full_data[z][y][x])
        # print("End of collection two_areas_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return two_areas_brightness

    def get_one_area_brightness_info(self):

        mask_img = nib.load(self.mask_file_path)

        full_img = nib.load(self.nii_file_path)

        mask_data = mask_img.get_fdata()

        full_data = full_img.get_fdata()

        diameter = int(min(mask_data.shape) / 10)
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
                    if mask_data[z][y][x] == 1:
                        one_area_brightness.append(full_data[z][y][x])
        # print("End of collection one_area_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

        return one_area_brightness

    def get_random_points_brightness_info(self):

        mask_img = nib.load(self.mask_file_path)

        full_img = nib.load(self.nii_file_path)

        mask_data = mask_img.get_fdata()

        full_data = full_img.get_fdata()

        # print("Start of collection random_points_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        random_points_brightness = []

        for i in range(100):
            rand_z = randint(0, mask_data.shape[0] - 1)
            rand_y = randint(0, mask_data.shape[1] - 1)
            rand_x = randint(0, mask_data.shape[2] - 1)
            while mask_data[rand_z][rand_y][rand_x] != 1:
                rand_z = randint(0, mask_data.shape[0] - 1)
                rand_y = randint(0, mask_data.shape[1] - 1)
                rand_x = randint(0, mask_data.shape[2] - 1)
            random_points_brightness.append(full_data[rand_z][rand_y][rand_x])
        # print("End of collection random_points_brightness |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
        return random_points_brightness
