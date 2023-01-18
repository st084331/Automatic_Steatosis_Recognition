import csv
import sklearn.metrics
from sklearn.linear_model import LinearRegression
from datetime import datetime
import sklearn
import itertools
from sklearn.preprocessing import PolynomialFeatures

places = ['random_point', 'whole_liver', 'one_area', 'two_areas', 'three_areas', 'random_points']

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

relative_types = ['mean', 'median', 'mode', '1', '3']
all_relative_type_combinations = list()
for n in range(len(relative_types) + 1):
    all_relative_type_combinations += list(itertools.combinations(relative_types, n))

score_dicts = []
for degree in range(2, 4):
    for place in places:

        if place != 'random_point':
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
            types = ['mean', 'median', 'mode', '1', '3']

        else:
            brightness_data = []
            with open(place + '.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    brightness_data.append(row)
            types = ['value']

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
            print(current_relative_types_for_dict)

            for current_types in all_type_combinations:

                current_types_for_dict = []
                for q in range(5):
                    if len(current_types) > q:
                        current_types_for_dict.append(current_types[q])
                    else:
                        current_types_for_dict.append('')
                print(place, current_types_for_dict, datetime.now().strftime("%H:%M:%S"))

                for k in range(1, 31):
                    train = []
                    train_csv = f"./splits/train_split{k}.csv"
                    with open(train_csv) as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            train.append(row)
                    X = []
                    y = []
                    for t in train:
                        for i in range(len(brightness_data)):
                            if t['nii'] == brightness_data[i]['nii'] and t['nii'] == \
                                    full_data[i]['nii']:
                                row = []
                                for k in range(len(current_relative_types)):
                                    row.append(float(full_data[i][current_relative_types[k]]))
                                for k in range(len(current_types)):
                                    row.append(float(brightness_data[i][current_types[k]]))
                                X.append(row)
                                y.append(float(t['ground_truth']))
                                break

                    poly_model = PolynomialFeatures(degree=degree)
                    poly_x_values = poly_model.fit_transform(X)
                    poly_model.fit(poly_x_values, y)
                    regression_model = LinearRegression()
                    regression_model.fit(poly_x_values, y)

                    for j in range(1, 31):
                        test = []
                        test_csv = f"./splits/test_split{j}.csv"
                        with open(test_csv) as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                test.append(row)

                        x = []
                        y = []
                        for t in test:
                            for i in range(len(brightness_data)):
                                if t['nii'] == brightness_data[i]['nii'] and t['nii'] == \
                                        full_data[i]['nii']:
                                    row = []
                                    for k in range(len(current_relative_types)):
                                        row.append(float(full_data[i][current_relative_types[k]]))
                                    for k in range(len(current_types)):
                                        row.append(float(brightness_data[i][current_types[k]]))
                                    x.append(row)
                                    y.append(float(t['ground_truth']))
                                    break

                        poly_x = poly_model.fit_transform(x)
                        y_pred = regression_model.predict(poly_x)

                        log_loss_score = sklearn.metrics.log_loss(y, y_pred)
                        r2_score = sklearn.metrics.r2_score(y, y_pred)

                        score_dicts.append({'place': place, 'relative_type_1': current_relative_types_for_dict[0],
                                            'relative_type_2': current_relative_types_for_dict[1],
                                            'relative_type_3': current_relative_types_for_dict[2],
                                            'relative_type_4': current_relative_types_for_dict[3],
                                            'relative_type_5': current_relative_types_for_dict[4],
                                            'type_1': current_types_for_dict[0],
                                            'type_2': current_types_for_dict[1],
                                            'type_3': current_types_for_dict[2],
                                            'type_4': current_types_for_dict[3], 'type_5': current_types_for_dict[4],
                                            'train': k, 'test': j, 'log_loss': log_loss_score, 'r2': r2_score})

    sorted_score = sorted(score_dicts, key=lambda d: d['r2'])

    with open(f"polynomial_regression_model_{degree}.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(sorted_score[0].keys()))
        writer.writeheader()
        for dict in sorted_score:
            writer.writerow(dict)
