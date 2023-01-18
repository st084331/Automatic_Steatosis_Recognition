import csv
import math
import itertools
import scipy.stats
import numpy as np
import scipy.signal
from numpy.linalg import inv

train = []
train_csv = './new_train.csv'
with open(train_csv) as f:
    reader = csv.DictReader(f)
    for row in reader:
        train.append(row)

hypos_dicts = []


def correlations_coefs(x, y):
    R_xx = []
    c_base = []
    for i in range(len(x)):
        c_base.append(scipy.stats.spearmanr(x[i], y)[0])
        row = []
        for j in range(len(x)):
            row.append(scipy.stats.spearmanr(x[i], x[j])[0])
        R_xx.append(row)
    c = np.array(c_base)
    c_T = c.transpose()
    R_2 = np.matmul(c_T, np.matmul(inv(R_xx), c))
    spearman = math.sqrt(R_2)
    return spearman


full_data_wo_quantiles = []
with open('full_brightness.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        full_data_wo_quantiles.append(row)

full_data_quantiles = []
with open('full_brightness_quantiles.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        full_data_quantiles.append(row)

full_data = []
for i in range(len(full_data_wo_quantiles)):
    full_data.append({**full_data_wo_quantiles[i], **full_data_quantiles[i]})

random_point = []
csv_filename = 'random_point.csv'
with open('random_point.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        random_point.append(row)

types = ['mean', 'median', 'mode', '1', '3']
all_relative_type_combinations = list()
for n in range(len(types) + 1):
    all_relative_type_combinations += list(itertools.combinations(types, n))

all_type_combinations = list()
for n in range(1, len(types) + 1):
    all_type_combinations += list(itertools.combinations(types, n))

for current_relative_types in all_relative_type_combinations:

    current_relative_types_for_dict = []
    for q in range(5):
        if len(current_relative_types) > q:
            current_relative_types_for_dict.append(current_relative_types[q])
        else:
            current_relative_types_for_dict.append('')
    current_types = ['value']
    X = []
    for h in range(len(current_relative_types) + len(current_types)):
        X.append([])
    y = []
    for t in train:
        for i in range(len(random_point)):
            if t['nii'] == random_point[i]['nii'] and t['nii'] == full_data[i]['nii']:
                for k in range(len(current_relative_types)):
                    X[k].append(float(full_data[i][current_relative_types[k]]))
                for k in range(len(current_relative_types), len(X)):
                    X[k].append(float(random_point[i]['value']))
                y.append(float(t['ground_truth']))
                break

    try:
        hypos_dicts.append({'place': 'random_point', 'relative_type_1': current_relative_types_for_dict[0],
                            'relative_type_2': current_relative_types_for_dict[1],
                            'relative_type_3': current_relative_types_for_dict[2],
                            'relative_type_4': current_relative_types_for_dict[3],
                            'relative_type_5': current_relative_types_for_dict[4], 'type_1': 'value', 'type_2': '',
                            'type_3': '',
                            'type_4': '', 'type_5': '', 'spearman': correlations_coefs(X, y)})
    except:
        hypos_dicts.append({'place': 'random_point', 'relative_type_1': current_relative_types_for_dict[0],
                            'relative_type_2': current_relative_types_for_dict[1],
                            'relative_type_3': current_relative_types_for_dict[2],
                            'relative_type_4': current_relative_types_for_dict[3],
                            'relative_type_5': current_relative_types_for_dict[4], 'type_1': 'value', 'type_2': '',
                            'type_3': '',
                            'type_4': '', 'type_5': '', 'spearman': -2.0})

    places = ['whole_liver', 'one_area', 'two_areas', 'three_areas', 'random_points']

    for place in places:

        brightness_data_wo_quantiles = []
        with open(place + '.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_wo_quantiles.append(row)

        brightness_data_quantiles = []
        with open(place + '_quantiles.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                brightness_data_quantiles.append(row)

        brightness_data = []
        for i in range(len(brightness_data_wo_quantiles)):
            brightness_data.append({**brightness_data_wo_quantiles[i], **brightness_data_quantiles[i]})

        for current_types in all_type_combinations:

            current_types_for_dict = []
            for q in range(5):
                if len(current_types) > q:
                    current_types_for_dict.append(current_types[q])
                else:
                    current_types_for_dict.append('')
            X = []
            for h in range(len(current_relative_types) + len(current_types)):
                X.append([])
            y = []
            for t in train:
                for i in range(len(brightness_data)):
                    if t['nii'] == brightness_data[i]['nii'] and t['nii'] == \
                            full_data[i][
                                'nii']:
                        for k in range(len(current_relative_types)):
                            X[k].append(float(full_data[i][current_relative_types[k]]))
                        for k in range(len(current_relative_types), len(X)):
                            X[k].append(float(brightness_data[i][current_types[
                                k - len(current_relative_types)]]))
                        y.append(float(t['ground_truth']))
                        break

            try:
                hypos_dicts.append(
                    {'place': place, 'relative_type_1': current_relative_types_for_dict[0],
                     'relative_type_2': current_relative_types_for_dict[1],
                     'relative_type_3': current_relative_types_for_dict[2],
                     'relative_type_4': current_relative_types_for_dict[3],
                     'relative_type_5': current_relative_types_for_dict[4], 'type_1': current_types_for_dict[0],
                     'type_2': current_types_for_dict[1],
                     'type_3': current_types_for_dict[2],
                     'type_4': current_types_for_dict[3], 'type_5': current_types_for_dict[4],
                     'spearman': correlations_coefs(X, y)})
            except:
                hypos_dicts.append(
                    {'place': place, 'relative_type_1': current_relative_types_for_dict[0],
                     'relative_type_2': current_relative_types_for_dict[1],
                     'relative_type_3': current_relative_types_for_dict[2],
                     'relative_type_4': current_relative_types_for_dict[3],
                     'relative_type_5': current_relative_types_for_dict[4], 'type_1': current_types_for_dict[0],
                     'type_2': current_types_for_dict[1],
                     'type_3': current_types_for_dict[2],
                     'type_4': current_types_for_dict[3], 'type_5': current_types_for_dict[4],
                     'spearman': -2.0})

hypos_dicts = sorted(hypos_dicts, key=lambda d: d['spearman'])
with open('correlations.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(hypos_dicts[0].keys()))
    writer.writeheader()
    for dict in hypos_dicts:
        writer.writerow(dict)
