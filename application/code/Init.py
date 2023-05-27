import os
from datetime import datetime

import torch
from dicom2nifti import settings

CURRENT_PATH = os.getcwd()
PARENT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
CONFIG = "config"
DATA = "data"
# print(f"CURRENT_PATH={CURRENT_PATH} PARENT_PATH={PARENT_PATH} |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

METHODS = ["Fuzzy criterion", "Most powerful criterion", "Linear regression", "Second degree polynomial regression"]
AREAS = ["Whole liver", "Three random areas", "Two random areas", "One random area", "100 random points"]
AVERAGES = ["Median", "Mode", "Mean", "Median low", "Median high", "Median grouped", "First quartile", 'Third quartile']

VESSELS = False
VERBOSE = False

if torch.cuda.is_available():
    CPU = False
    # print("CPU mode off |", datetime.now().strftime("%H:%M:%S.%f")[:-3])
else:
    CPU = True
    # print("CPU mode on |", datetime.now().strftime("%H:%M:%S.%f")[:-3])

settings.disable_validate_slice_increment()