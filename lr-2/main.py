import csv
from typing import List

THRESHOLD = 0.85

def import_data():
    data = []

    with open('data/lr2.csv', 'r') as f:
        data = [[float(x) if x.strip() else 0.0 for x in row] for row in csv.reader(f)]

    return data

def print_matrix(matrix: List[List[float]], names: List[str]):
    width = max(8, max(len(name) for name in names) + 2)

    print(" " * width, end="")
    for name in names:
        print(f"{name:>{width}}", end="")
    print()

    for i, row in enumerate(matrix):
        print(f"{names[i]:>{width}}", end="")
        for j, value in enumerate(row):
            if j < i:
                print(" " * width, end="")
            else:
                print(f"{value:>{width}.2f}", end="")
        print()

def find_max(data: List[List[float]]):
    max_item = (0, 1, -1)

    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if data[i][j] > max_item[2]: max_item = (i, j, data[i][j])

    return max_item

def merge_clusters(data: List[List[float]], names: List[str], a: int, b: int):
    for i in range(len(data)):
        data[a][i] = max(data[a][i], data[b][i])
        data[i][a] = data[a][i]
    data[a][a] = 0

    del data[b]
    for row in data:
        del row[b]

    names[a] = f"{names[a]}, {names[b]}"
    del names[b]


def main():
    data = import_data()
    names = [f"U{i+1}" for i in range(len(data))]

    print_matrix(data, names)

    i,j,max_sim = find_max(data)

    while max_sim >= THRESHOLD:
        print(f"Объединяем ({names[i]}) и ({names[j]}) с подобием {max_sim:.2f}")

        merge_clusters(data, names, i, j)

        print()
        print_matrix(data, names)

        i,j,max_sim = find_max(data)

    if len(data) > 1:
        print(f"Максимальное подобие ({names[i]}) и ({names[j]}): {max_sim:.2f} < R = {THRESHOLD}")


if __name__ == "__main__":
    main()
