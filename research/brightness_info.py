import os
from glob import glob
import nibabel as nib
import random
import csv
from datetime import datetime
import statistics

if __name__ == '__main__':
    full_nii_dicts = []
    full_nii_dicts_quantiles = []

    whole_liver_nii_dicts_quantiles = []
    whole_liver_nii_dicts = []

    random_point_dicts = []

    random_points_dicts = []
    random_points_dicts_quantiles = []

    one_area_dicts = []
    one_area_dicts_quantiles = []

    two_areas_dicts = []
    two_areas_dicts_quantiles = []

    three_areas_dicts = []
    three_areas_dicts_quantiles = []

    input_dir = './res_dicom2nifti'
    for file in (sorted(glob(input_dir + '/*' + '/*'))):
        list_of_nii = os.listdir(file)
        file_struct = file.split('/')
        for nii in list_of_nii:
            print("Patient", file_struct[2], "| Analyzing the file", nii, "|", datetime.now().strftime("%H:%M:%S"))
            t1_img = nib.load(os.path.join("./res_mask", file_struct[2], file_struct[3], nii + "-livermask2.nii"))
            t1_data = t1_img.get_fdata()
            t2_img = nib.load(os.path.join(file, nii))
            t2_data = t2_img.get_fdata()

            rand_z = random.randint(0, t1_data.shape[0] - 1)
            rand_y = random.randint(0, t1_data.shape[1] - 1)
            rand_x = random.randint(0, t1_data.shape[2] - 1)
            while t1_data[rand_z][rand_y][rand_x] != 1:
                rand_z = random.randint(0, t1_data.shape[0] - 1)
                rand_y = random.randint(0, t1_data.shape[1] - 1)
                rand_x = random.randint(0, t1_data.shape[2] - 1)
            random_point_dicts.append({'nii': os.path.join(file, nii), 'value': t2_data[rand_z][rand_y][rand_x]})

            random_points_brightness = []
            for i in range(100):
                rand_z = random.randint(0, t1_data.shape[0] - 1)
                rand_y = random.randint(0, t1_data.shape[1] - 1)
                rand_x = random.randint(0, t1_data.shape[2] - 1)
                while t1_data[rand_z][rand_y][rand_x] != 1:
                    rand_z = random.randint(0, t1_data.shape[0] - 1)
                    rand_y = random.randint(0, t1_data.shape[1] - 1)
                    rand_x = random.randint(0, t1_data.shape[2] - 1)
                random_points_brightness.append(t2_data[rand_z][rand_y][rand_x])
            random_points_quantiles = statistics.quantiles(random_points_brightness)
            random_points_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': random_points_quantiles[0], '2': random_points_quantiles[1],
                 '3': random_points_quantiles[2]})
            random_points_dicts.append(
                {'nii': os.path.join(file, nii), 'mean': statistics.mean(random_points_brightness),
                 'median': statistics.median(random_points_brightness),
                 'mode': statistics.mode(random_points_brightness)})

            one_area_brightness = []
            radius = int(min(t1_data.shape) / 10)
            rand_z = random.randint(0, t1_data.shape[0] - 1)
            rand_y = random.randint(0, t1_data.shape[1] - 1)
            rand_x = random.randint(0, t1_data.shape[2] - 1)
            while t1_data[rand_z][rand_y][rand_x] != 1:
                rand_z = random.randint(0, t1_data.shape[0] - 1)
                rand_y = random.randint(0, t1_data.shape[1] - 1)
                rand_x = random.randint(0, t1_data.shape[2] - 1)

            min_z = int(rand_z - radius / 2)
            if min_z < 0:
                min_z = 0
            max_z = int(rand_z + radius / 2)
            if max_z > t1_data.shape[0]:
                max_z = t1_data.shape[0]

            min_y = int(rand_y - radius / 2)
            if min_y < 0:
                min_y = 0
            max_y = int(rand_y + radius / 2)
            if max_y > t1_data.shape[1]:
                max_y = t1_data.shape[1]

            min_x = int(rand_x - radius / 2)
            if min_x < 0:
                min_x = 0
            max_x = int(rand_x + radius / 2)
            if max_x > t1_data.shape[2]:
                max_x = t1_data.shape[2]

            for z in range(min_z, max_z):
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        if t1_data[z][y][x] == 1:
                            one_area_brightness.append(t2_data[z][y][x])

            one_area_quantiles = statistics.quantiles(one_area_brightness)
            one_area_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': one_area_quantiles[0], '2': one_area_quantiles[1],
                 '3': one_area_quantiles[2]})
            one_area_dicts.append(
                {'nii': os.path.join(file, nii), 'mean': statistics.mean(one_area_brightness),
                 'median': statistics.median(one_area_brightness),
                 'mode': statistics.mode(one_area_brightness)})

            two_areas_brightness = []
            for i in range(2):
                rand_z = random.randint(0, t1_data.shape[0] - 1)
                rand_y = random.randint(0, t1_data.shape[1] - 1)
                rand_x = random.randint(0, t1_data.shape[2] - 1)
                while t1_data[rand_z][rand_y][rand_x] != 1:
                    rand_z = random.randint(0, t1_data.shape[0] - 1)
                    rand_y = random.randint(0, t1_data.shape[1] - 1)
                    rand_x = random.randint(0, t1_data.shape[2] - 1)

                min_z = int(rand_z - radius / 2)
                if min_z < 0:
                    min_z = 0
                max_z = int(rand_z + radius / 2)
                if max_z > t1_data.shape[0]:
                    max_z = t1_data.shape[0]

                min_y = int(rand_y - radius / 2)
                if min_y < 0:
                    min_y = 0
                max_y = int(rand_y + radius / 2)
                if max_y > t1_data.shape[1]:
                    max_y = t1_data.shape[1]

                min_x = int(rand_x - radius / 2)
                if min_x < 0:
                    min_x = 0
                max_x = int(rand_x + radius / 2)
                if max_x > t1_data.shape[2]:
                    max_x = t1_data.shape[2]

                for z in range(min_z, max_z):
                    for y in range(min_y, max_y):
                        for x in range(min_x, max_x):
                            if t1_data[z][y][x] == 1:
                                two_areas_brightness.append(t2_data[z][y][x])

            two_areas_quantiles = statistics.quantiles(two_areas_brightness)
            two_areas_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': two_areas_quantiles[0], '2': two_areas_quantiles[1],
                 '3': two_areas_quantiles[2]})
            two_areas_dicts.append(
                {'nii': os.path.join(file, nii), 'mean': statistics.mean(two_areas_brightness),
                 'median': statistics.median(two_areas_brightness),
                 'mode': statistics.mode(two_areas_brightness)})

            three_areas_brightness = []
            for i in range(3):
                rand_z = random.randint(0, t1_data.shape[0] - 1)
                rand_y = random.randint(0, t1_data.shape[1] - 1)
                rand_x = random.randint(0, t1_data.shape[2] - 1)
                while t1_data[rand_z][rand_y][rand_x] != 1:
                    rand_z = random.randint(0, t1_data.shape[0] - 1)
                    rand_y = random.randint(0, t1_data.shape[1] - 1)
                    rand_x = random.randint(0, t1_data.shape[2] - 1)

                min_z = int(rand_z - radius / 2)
                if min_z < 0:
                    min_z = 0
                max_z = int(rand_z + radius / 2)
                if max_z > t1_data.shape[0]:
                    max_z = t1_data.shape[0]

                min_y = int(rand_y - radius / 2)
                if min_y < 0:
                    min_y = 0
                max_y = int(rand_y + radius / 2)
                if max_y > t1_data.shape[1]:
                    max_y = t1_data.shape[1]

                min_x = int(rand_x - radius / 2)
                if min_x < 0:
                    min_x = 0
                max_x = int(rand_x + radius / 2)
                if max_x > t1_data.shape[2]:
                    max_x = t1_data.shape[2]

                for z in range(min_z, max_z):
                    for y in range(min_y, max_y):
                        for x in range(min_x, max_x):
                            if t1_data[z][y][x] == 1:
                                three_areas_brightness.append(t2_data[z][y][x])

            three_areas_quantiles = statistics.quantiles(three_areas_brightness)
            three_areas_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': three_areas_quantiles[0], '2': three_areas_quantiles[1],
                 '3': three_areas_quantiles[2]})
            three_areas_dicts.append(
                {'nii': os.path.join(file, nii), 'mean': statistics.mean(three_areas_brightness),
                 'median': statistics.median(three_areas_brightness),
                 'mode': statistics.mode(three_areas_brightness)})

            full_list_of_brightness = []

            whole_liver_list_of_brightness = []

            for z in range(0, t1_data.shape[0], 2):
                for y in range(0, t1_data.shape[1], 2):
                    for x in range(0, t1_data.shape[2], 2):
                        full_list_of_brightness.append(t2_data[z][y][x])
                        if t1_data[z][y][x] == 1:
                            whole_liver_list_of_brightness.append(t2_data[z][y][x])

            full_nii_dicts.append({'nii': os.path.join(file, nii), 'mean': statistics.mean(full_list_of_brightness),
                                   'median': statistics.median(full_list_of_brightness),
                                   'mode': statistics.mode(full_list_of_brightness)})
            full_quantiles = statistics.quantiles(full_list_of_brightness)
            full_nii_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': full_quantiles[0], '2': full_quantiles[1],
                 '3': full_quantiles[2]})

            whole_liver_quantiles = statistics.quantiles(whole_liver_list_of_brightness)
            whole_liver_nii_dicts_quantiles.append(
                {'nii': os.path.join(file, nii), '1': whole_liver_quantiles[0], '2': whole_liver_quantiles[1],
                 '3': whole_liver_quantiles[2]})
            whole_liver_nii_dicts.append(
                {'nii': os.path.join(file, nii), 'mean': statistics.mean(whole_liver_list_of_brightness),
                 'median': statistics.median(whole_liver_list_of_brightness),
                 'mode': statistics.mode(whole_liver_list_of_brightness)})

            print("File", nii, "parsed successfully", "|", datetime.now().strftime("%H:%M:%S"))

    niis_info = ['nii', 'mean', 'median', 'mode']
    niis_info_quantiles = ['nii', '1', '2', '3']
    print("Converting to csv")

    with open('full_brightness.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in full_nii_dicts:
            writer.writerow(dict)
    with open('full_brightness_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in full_nii_dicts_quantiles:
            writer.writerow(dict)

    with open('random_points.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in random_points_dicts:
            writer.writerow(dict)
    with open('random_points_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in random_points_dicts_quantiles:
            writer.writerow(dict)

    with open('one_area.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in one_area_dicts:
            writer.writerow(dict)
    with open('one_area_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in one_area_dicts_quantiles:
            writer.writerow(dict)

    with open('two_areas.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in two_areas_dicts:
            writer.writerow(dict)
    with open('two_areas_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in two_areas_dicts_quantiles:
            writer.writerow(dict)

    with open('three_areas.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in three_areas_dicts:
            writer.writerow(dict)
    with open('three_areas_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in three_areas_dicts_quantiles:
            writer.writerow(dict)

    with open('whole_liver_quantiles.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info_quantiles)
        writer.writeheader()
        for dict in whole_liver_nii_dicts_quantiles:
            writer.writerow(dict)
    with open('whole_liver.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=niis_info)
        writer.writeheader()
        for dict in whole_liver_nii_dicts:
            writer.writerow(dict)

    with open('random_point.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['nii', 'value'])
        writer.writeheader()
        for dict in random_point_dicts:
            writer.writerow(dict)
