import csv
from sklearn.model_selection import train_test_split

train = []
train_csv = './new_train.csv'
with open(train_csv) as f:
    reader = csv.DictReader(f)
    for row in reader:
        train.append(row)

zeros_counter = 0
non_zeros_counter = 0

y = []
X = []
for t in train:
    value = int(float(t['ground_truth']))
    y.append(value)
    X.append(t['nii'])
    if value == 0:
        zeros_counter += 1
    else:
        non_zeros_counter += 1
print('Percentage of patients in the train dataset', non_zeros_counter / (non_zeros_counter + zeros_counter) * 100)

for i in range(30):
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3)
    train_dicts = []
    for j in range(len(X_train)):
        train_dicts.append({'nii': X_train[j], 'ground_truth': y_train[j]})

    test_dicts = []
    for j in range(len(X_test)):
        test_dicts.append({'nii': X_test[j], 'ground_truth': y_test[j]})

    with open(f"./splits/train_split{i + 1}.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['nii', 'ground_truth'])
        writer.writeheader()
        for dict in train_dicts:
            writer.writerow(dict)

    with open(f"./splits/test_split{i + 1}.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['nii', 'ground_truth'])
        writer.writeheader()
        for dict in test_dicts:
            writer.writerow(dict)
