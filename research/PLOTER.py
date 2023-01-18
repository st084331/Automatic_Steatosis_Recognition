import csv
import math
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import dataframe_image as dfi

names = ['linear_regression_model', 'polynomial_regression_model_2', 'polynomial_regression_model_3']

for name in names:
    model = []
    csv_file = f"./{name}.csv"
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            model.append(row)

    places = ['whole_liver', 'three_areas', 'two_areas', 'one_area', 'random_points', 'random_point']
    types = ['mean', 'median', 'mode', '1', '3']
    places_and_number_var = []
    places_and_number_var_as_str = []
    for place in places:
        for i in range(1, 11):
            if place != 'random_point':
                places_and_number_var.append([place, i])
                places_and_number_var_as_str.append(f"{place}:{i}")
            else:
                if i <= 6:
                    places_and_number_var.append([place, i])
                    places_and_number_var_as_str.append(f"{place}:{i}")

    draw_dict = []

    sums_r2 = [0] * len(places_and_number_var)
    sums_log_loss = [0] * len(places_and_number_var)
    counter = [0] * len(places_and_number_var)
    for lrm in model:
        if float(lrm['r2']) >= 0 and float(lrm['r2']) <= 1:
            current_counter = 0
            for k in range(1, 6):
                if lrm[f"type_{k}"] != '':
                    current_counter += 1
                if lrm[f"relative_type_{k}"] != '':
                    current_counter += 1
            ind = places_and_number_var.index([lrm['place'], current_counter])
            sums_r2[ind] += math.fabs(float(lrm['r2']))
            sums_log_loss[ind] += float(lrm['log_loss'])
            counter[ind] += 1

    for i in range(len(sums_r2)):
        sums_r2[i] = sums_r2[i] / counter[i]
        sums_log_loss[i] = sums_log_loss[i] / counter[i]
        draw_dict.append({'place_and_number_of_var': places_and_number_var_as_str[i], 'mean_r2': sums_r2[i], 'mean_log_loss': sums_log_loss[i]})

    df = pd.DataFrame(draw_dict[:len(draw_dict)//2])
    cm = sns.light_palette("green", as_cmap=True)
    dfi.export(df.style.background_gradient(cmap=cm).set_precision(2), f"{name}_score_by_place_and_number_of_var_1.png")
    df = pd.DataFrame(draw_dict[len(draw_dict)//2:])
    cm = sns.light_palette("green", as_cmap=True)
    dfi.export(df.style.background_gradient(cmap=cm).set_precision(2), f"{name}_score_by_place_and_number_of_var_2.png")

"""
statistical_model = []
csv_file = './statistical_model.csv'
with open(csv_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        statistical_model.append(row)


places = ['whole_liver', 'one_area', 'two_areas', 'three_areas', 'random_points']
types = ['mean', 'median', 'mode', '1', '3']

statistical_model_dict = []

for place in places:
    for t in types:
        min_val = 100000000.0
        max_val = 0.0
        for im in statistical_model:
            if im['place'] == place and im['type'] == t:
                if float(im['log_loss']) < min_val:
                    min_val = float(im['log_loss'])
                if float(im['r2']) > max_val:
                    max_val = float(im['r2'])
        statistical_model_dict.append({'place': place, 'type': t, 'min_log_loss': min_val, 'max_r2_score': max_val})

df = pd.DataFrame(statistical_model_dict)
cm = sns.light_palette("green", as_cmap=True)
dfi.export(df.style.background_gradient(cmap=cm).set_precision(2), "statistical_model.png")
"""
