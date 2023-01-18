import csv
import sklearn.metrics
import math
import sklearn
from datetime import datetime

places = ['whole_liver', 'one_area', 'two_areas', 'three_areas', 'random_points', 'random_point']
score_dicts = []
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

    for i in range(1, 31):
        for type in types:
            train = []
            train_csv = f"./splits/train_split{i}.csv"
            with open(train_csv) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    train.append(row)

            brightness = []
            y = []
            for bd in brightness_data:
                for t in train:
                    if bd['nii'] == t['nii']:
                        brightness.append(float(bd[type]))
                        y.append(int(float(t['ground_truth'])))

            max_point = max(brightness)
            min_point = min(brightness)
            border_point = (max_point + min_point) / 2

            y_pred_init = []

            for bd in brightness_data:
                for t in train:
                    if bd['nii'] == t['nii']:
                        if float(bd[type]) <= border_point:
                            y_pred_init.append(1)
                        else:
                            y_pred_init.append(0)
                        break

            score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
            leftmost_best_score = 0.0
            leftmost_point = border_point
            step = 0.1

            while leftmost_best_score <= score:

                leftmost_best_score = score
                point1 = leftmost_point - step

                y_pred1 = []

                for bd in brightness_data:
                    for t in train:
                        if bd['nii'] == t['nii']:
                            if float(bd[type]) <= point1:
                                y_pred1.append(1)
                            else:
                                y_pred1.append(0)

                score1 = math.fabs(sklearn.metrics.f1_score(y, y_pred1))

                if score1 >= score:
                    score = score1
                    leftmost_point = point1
                else:
                    break

            border_point = (max_point + min_point) / 2
            score = math.fabs(sklearn.metrics.f1_score(y, y_pred_init))
            rightmost_best_score = 0.0
            rightmost_point = border_point

            while rightmost_best_score <= score:

                rightmost_best_score = score
                point2 = rightmost_point + step

                y_pred2 = []

                for bd in brightness_data:
                    for t in train:
                        if bd['nii'] == t['nii']:
                            if float(bd[type]) <= point2:
                                y_pred2.append(1)
                            else:
                                y_pred2.append(0)

                score2 = math.fabs(sklearn.metrics.f1_score(y, y_pred2))

                if score2 >= score:
                    score = score2
                    rightmost_point = point2
                else:
                    break

            if rightmost_best_score >= leftmost_best_score:
                border_point = rightmost_point
            else:
                border_point = leftmost_point
            print(place, type, border_point, i, datetime.now().strftime("%H:%M:%S"))

            for j in range(1, 31):
                test = []
                test_csv = f"./splits/test_split{j}.csv"
                with open(test_csv) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        test.append(row)

                y_pred = []
                y_real = []

                for bd in brightness_data:
                    for t in test:
                        if bd['nii'] == t['nii']:
                            y_real.append(int(float(t['ground_truth'])))
                            if float(bd[type]) <= border_point:
                                y_pred.append(1)
                            else:
                                y_pred.append(0)

                score = math.fabs(sklearn.metrics.f1_score(y_real, y_pred))

                score_dicts.append({'place': place, 'type': type, 'train': i, 'test': j, 'f1_score': score,
                                    'border_point': border_point})

sorted_dicts = sorted(score_dicts, key=lambda d: d['score'])

with open('interval_model_f1_score.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(sorted_dicts[0].keys()))
    writer.writeheader()
    for dict in sorted_dicts:
        writer.writerow(dict)
