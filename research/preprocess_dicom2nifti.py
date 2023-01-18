""" Import packages """
import os
from glob import glob
import pydicom as dcm
import dicom2nifti
import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()
input_dir = './unifesp-fatty-liver'
imaging_dir = os.path.join(input_dir, 'fatty-liver-dataset', 'd_2')

"""
First, we split all patients between Chest and Abdomen. 
We get this information by iterating through the exam directories, opening a dicom file 
and reading the Study Description Tag. 
"""
if __name__ == '__main__':
    try:
        os.mkdir(os.path.join('./res_dicom2nifti'))
    except:
        print('Dir exists')

    for file in (sorted(glob(imaging_dir + '/*' + '/*' + '/*'))):
        dicom = dcm.dcmread(os.path.join(file, os.listdir(file)[0]), stop_before_pixels=True)

        # Here we iterate through each series directory (the last subdirectory) and read the first dicom file
        # (doesn't matter which one you read). We stop before the pixel array, so the process takes less time.
        print("Dicom to NiFti:", file)
        file_struct = file.split('/')
        try:
            os.mkdir(os.path.join('./res_dicom2nifti', file_struct[4]))
        except:
            print('Patient dir exists')
        try:
            os.mkdir(os.path.join('./res_dicom2nifti', file_struct[4], file_struct[5]))
        except:
            print('Study dir exists')
        dicom2nifti.dicom_series_to_nifti(file, os.path.join('res_dicom2nifti', file_struct[4], file_struct[5],
                                                             file_struct[6] + ".nii"), reorient_nifti=False)
