import csv
import sklearn.metrics
from sklearn.linear_model import LinearRegression
from datetime import datetime
import sklearn
import itertools
from sklearn.preprocessing import PolynomialFeatures

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

submission = []
with open('unifesp-fatty-liver/sample_submission.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        submission.append(row)

brightness_data_wo_quantiles = []
with open('whole_liver.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        brightness_data_wo_quantiles.append(row)

brightness_data_quantiles = []
with open('whole_liver_quantiles.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        brightness_data_quantiles.append(row)

brightness_data = []
for i in range(len(brightness_data_wo_quantiles)):
    brightness_data.append({**brightness_data_wo_quantiles[i], **brightness_data_quantiles[i]})
types = ['mean', 'median', 'mode', '1', '3']
current_relative_types = types
current_types = types

train = []
train_csv = f"./splits/train_split4.csv"
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

poly_model = PolynomialFeatures(degree=2)
poly_x_values = poly_model.fit_transform(X)
poly_model.fit(poly_x_values, y)
regression_model = LinearRegression()
regression_model.fit(poly_x_values, y)

real_submission = []
for t in submission:
    for i in range(len(brightness_data)):

        if t['Id'] == brightness_data[i]['nii'].split('/')[2]:
            x = []
            for k in range(len(current_relative_types)):
                x.append(float(full_data[i][current_relative_types[k]]))
            for k in range(len(current_types)):
                x.append(float(brightness_data[i][current_types[k]]))
            poly_x = poly_model.fit_transform([x])
            y_pred = regression_model.predict(poly_x)
            real_submission.append({'Id': t['Id'], 'Prediction': y_pred[0]})
            break

with open(f"submission.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(real_submission[0].keys()))
    writer.writeheader()
    for dict in real_submission:
        writer.writerow(dict)
