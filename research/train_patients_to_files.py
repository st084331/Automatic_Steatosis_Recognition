import csv
from glob import glob

new_train = []
train = []
csv_filename = './unifesp-fatty-liver/train.csv'
with open(csv_filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        train.append(row)

for t in train:
    id = t['Id']
    patient_studies = sorted(glob("./res_dicom2nifti" + '/' + id + '/*' + '/*'))
    for dir in patient_studies:
        new_train.append({'nii': dir, 'ground_truth': t['ground_truth']})

csv_info = ['nii', 'ground_truth']
with open('new_train.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_info)
    writer.writeheader()
    for dict in new_train:
        writer.writerow(dict)
