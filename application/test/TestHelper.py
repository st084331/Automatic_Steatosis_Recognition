import csv
import os


class TestHelper:
    @staticmethod
    def make_csv_file(path, file, data, n_copy=1):
        if not os.path.exists(path):
            os.mkdir(path)
        paths = []
        for i in range(n_copy):
            if n_copy > 1:
                file_path = os.path.join(path, f"{file}_{i+1}")
            else:
                file_path = os.path.join(path, f"{file}")
            with open(file_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                writer.writeheader()
                for dict in data:
                    writer.writerow(dict)
            paths.append(file_path)
        return paths

    @staticmethod
    def make_txt_file(path, file, data, n_copy=1):
        if not os.path.exists(path):
            os.mkdir(path)
        paths = []
        for i in range(n_copy):
            if n_copy > 1:
                file_path = os.path.join(path, f"{file}_{i + 1}")
            else:
                file_path = os.path.join(path, f"{file}")
            f = open(file_path, "a")
            f.write(data)
            f.close()
            paths.append(file_path)
        return paths