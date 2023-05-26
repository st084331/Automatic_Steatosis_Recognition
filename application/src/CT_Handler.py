import os
from random import randint

import dicom2nifti

from application.src.FileManager import FileManager
from application.src.Init import CPU, VERBOSE, VESSELS
from livermask import livermask


class CT_Handler:

    def __init__(self, folder, name_of_nifti):
        self.folder = folder
        self.name_of_nifti = name_of_nifti
        self.dicom_to_nifti()
        self.make_mask()

    def dicom_to_nifti(self):
        dicom2nifti.dicom_series_to_nifti(self.folder, os.path.join('.', self.name_of_nifti + ".nii"),
                                          reorient_nifti=False)

    def make_mask(self):
        livermask.func(os.path.abspath(self.name_of_nifti + ".nii"),
                                 os.path.abspath(self.name_of_nifti),
                                 CPU, VERBOSE, VESSELS)

    def full_img_brightness_info(self):
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        full_data = full_img.get_fdata()

        full_img_brightness = []

        for z in range(0, full_data.shape[0], 2):
            for y in range(0, full_data.shape[1], 2):
                for x in range(0, full_data.shape[2], 2):
                    full_img_brightness.append(full_data[z][y][x])

        return full_img_brightness

    def whole_liver_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()

        whole_liver_list_of_brightness = []
        for z in range(0, mask_data.shape[0], 2):
            for y in range(0, mask_data.shape[1], 2):
                for x in range(0, mask_data.shape[2], 2):
                    if mask_data[z][y][x] == 1:
                        whole_liver_list_of_brightness.append(full_data[z][y][x])

        return whole_liver_list_of_brightness

    def three_areas_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
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

        return three_areas_brightness

    def two_areas_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
        two_areas_brightness = []
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

        return two_areas_brightness

    def one_area_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
        diameter = int(min(mask_data.shape) / 10)
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

        return one_area_brightness

    def random_points_brightness_info(self):
        mask_img = FileManager.load_mask_image(name_of_nifti=self.name_of_nifti)
        full_img = FileManager.load_original_image(name_of_nifti=self.name_of_nifti)
        mask_data = mask_img.get_fdata()
        full_data = full_img.get_fdata()
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
        return random_points_brightness