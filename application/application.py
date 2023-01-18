import os
import nibabel as nib
from datetime import datetime
import statistics
import dicom2nifti
import dicom2nifti.settings as settings
import livermask.livermask

vessels = False
verbose = False
cpu = True
settings.disable_validate_slice_increment()


def dicomToNifti(dicom_folder):
    folder_struct = dicom_folder.split('/')
    name_of_nifti = folder_struct[len(folder_struct) - 1]
    dicom2nifti.dicom_series_to_nifti(dicom_folder, os.path.join('.', name_of_nifti + ".nii"), reorient_nifti=False)
    return name_of_nifti


def makeMask(name_of_nifti):
    livermask.livermask.func(os.path.abspath(name_of_nifti + ".nii"),
                             os.path.abspath(name_of_nifti),
                             cpu, verbose, vessels)
    return name_of_nifti


def brightnessInfo(name_of_nifti):
    t1_img = nib.load(os.path.join(".", name_of_nifti + "-livermask2.nii"))
    t1_data = t1_img.get_fdata()
    t2_img = nib.load(os.path.join(".", name_of_nifti + ".nii"))
    t2_data = t2_img.get_fdata()

    whole_liver_list_of_brightness = []
    for z in range(0, t1_data.shape[0], 2):
        for y in range(0, t1_data.shape[1], 2):
            for x in range(0, t1_data.shape[2], 2):
                if t1_data[z][y][x] == 1:
                    whole_liver_list_of_brightness.append(t2_data[z][y][x])

    return statistics.mode(whole_liver_list_of_brightness)


def statisticalModel(mode_of_liver):
    brightness_data_wo_quantiles = []
    with open(os.path.join(".", 'data', 'whole_liver' + '.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            brightness_data_wo_quantiles.append(row)

    brightness_data_quantiles = []
    with open(os.path.join(".", 'data', 'whole_liver' + '_quantiles.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            brightness_data_quantiles.append(row)

    brightness_data = []
    for i in range(len(brightness_data_wo_quantiles)):
        brightness_data.append({**brightness_data_wo_quantiles[i], **brightness_data_quantiles[i]})

    train = []
    train_csv = os.path.join(".", "data", "new_train.csv")
    with open(train_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            train.append(row)

    brightness_of_sick_patients = []
    brightness_of_healthy_patients = []
    for bd in brightness_data:
        for t in train:
            if bd['nii'] == t['nii']:
                if float(t['ground_truth']) == 0.0:
                    brightness_of_healthy_patients.append(float(bd['mode']))
                else:
                    brightness_of_sick_patients.append(float(bd['mode']))
                break

    intersection_max_point = max(brightness_of_sick_patients)
    intersection_min_point = min(brightness_of_healthy_patients)
    intersection = []
    for b in brightness_of_healthy_patients:
        if b < intersection_max_point:
            intersection.append([0, b])
    for b in brightness_of_sick_patients:
        if b > intersection_min_point:
            intersection.append([1, b])

    prediction = 0.5

    if mode_of_liver >= intersection_max_point:
        prediction = 0.0
    elif mode_of_liver <= intersection_min_point:
        prediction = 1.0
    else:
        sick_counter = 0
        for inter in intersection:
            if inter[1] >= mode_of_liver and inter[0] == 1:
                sick_counter += 1
        prediction = sick_counter / len(intersection)

    return prediction


if __name__ == "__main__":
    print("Enter absolute path to the folder with dicom files: ")
    dicom_folder = input()
    if os.path.exists(dicom_folder):
        try:
            name_of_nifti = makeMask(dicomToNifti(dicom_folder))
            mode_of_liver = brightnessInfo(name_of_nifti)
            print("File", name_of_nifti + ".nii", "parsed successfully", "|", datetime.now().strftime("%H:%M:%S"))
            print(statisticalModel(mode_of_liver))
        except:
            print("Error")
        os.remove(name_of_nifti + ".nii")
        os.remove(name_of_nifti + "-livermask2.nii")
