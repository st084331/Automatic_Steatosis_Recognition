import os
from glob import glob

import livermask.livermask

input_dir = './res_dicom2nifti'
vessels = False
verbose = False
cpu = True

if __name__ == '__main__':
    try:
        os.mkdir(os.path.join('./res_mask'))
    except:
        print('Dir exists')

    for file in (sorted(glob(input_dir + '/*' + '/*'))):
        list_of_nii = os.listdir(file)

        # Here we iterate through each series directory (the last subdirectory) and read the first dicom file
        # (doesn't matter which one you read). We stop before the pixel array, so the process takes less time.
        file_struct = file.split('/')
        try:
            os.mkdir(os.path.join('./res_mask', file_struct[2]))
        except:
            print('Patient dir exists')
        try:
            os.mkdir(os.path.join('./res_mask', file_struct[2], file_struct[3]))
        except:
            print('Study dir exists')

        for nii in list_of_nii:
            livermask.livermask.func(os.path.abspath(os.path.join(file, nii)),
                                     os.path.abspath(os.path.join('./res_mask', file_struct[2], file_struct[3], nii)),
                                     cpu, verbose, vessels)
