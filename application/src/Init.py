import torch
from dicom2nifti import settings

METHODS = ["Fuzzy criterion", "Most powerful criterion", "Linear regression", "Second degree polynomial regression"]
AREAS = ["Whole liver", "Three random areas", "Two random areas", "One random area", "100 random points"]
AVERAGES = ["Median", "Mode", "Mean", "Median low", "Median high", "Median grouped", "First quartile", 'Third quartile']

VESSELS = False
VERBOSE = False

if torch.cuda.is_available():
    CPU = False
else:
    CPU = True

settings.disable_validate_slice_increment()