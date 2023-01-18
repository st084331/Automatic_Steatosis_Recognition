import csv
import sklearn.metrics
import sklearn

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

            brightness_of_sick_patients = []
            brightness_of_healthy_patients = []
            for bd in brightness_data:
                for t in train:
                    if bd['nii'] == t['nii']:
                        if float(t['ground_truth']) == 0.0:
                            brightness_of_healthy_patients.append(float(bd[type]))
                        else:
                            brightness_of_sick_patients.append(float(bd[type]))
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
                            point = float(bd[type])
                            y_real.append(int(float(t['ground_truth'])))

                            if point >= intersection_max_point:
                                y_pred.append(0.0)
                            elif point <= intersection_min_point:
                                y_pred.append(1.0)
                            else:
                                sick_counter = 0
                                for inter in intersection:
                                    if inter[1] >= point and inter[0] == 1:
                                        sick_counter += 1
                                y_pred.append(sick_counter / len(intersection))

                log_loss = sklearn.metrics.log_loss(y_real, y_pred)
                r2 = sklearn.metrics.r2_score(y_real, y_pred)

                score_dicts.append(
                    {'place': place, 'type': type, 'train': i, 'test': j, 'log_loss': log_loss, 'r2': r2})

sorted_dicts = sorted(score_dicts, key=lambda d: d['r2'])

with open('statistical_model.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(sorted_dicts[0].keys()))
    writer.writeheader()
    for dict in sorted_dicts:
        writer.writerow(dict)
