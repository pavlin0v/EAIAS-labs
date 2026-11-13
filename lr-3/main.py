import csv
from typing import List

def import_data():
    data = []

    with open('data/lr3.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([int(x) if x.strip() else 0 for x in row])

    return data

def print_array(name: str, values: List[int]):
    print(f"{name:>10}", end="")
    for value in values:
        print(f"{value:>4}", end="")
    print()

def print_matrix(data: List[List[int]]):
    print("Матрица A:")
    for row in data:
        for value in row:
            if value == 0:
                print(" " * 4, end="")
            else:
                print(f"{value:>4}", end="")
        print()
    print()

def print_coordinate(data: List[List[int]]):
    values = []
    rows = []
    cols = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 0: continue

            values.append(data[i][j])
            rows.append(i)
            cols.append(j)

    print("Координатный:")
    print_array("Value", values)
    print_array("Row", rows)
    print_array("Col", cols)
    print()

def print_csr(data: List[List[int]]):
    values = []
    cols = []
    row_index = [0]

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 0: continue

            values.append(data[i][j])
            cols.append(j)
        row_index.append(len(values))

    print("По строкам:")
    print_array("Value", values)
    print_array("Col", cols)
    print_array("RowIndex", row_index)
    print()

def print_ellpack(data: List[List[int]]):
    values = []
    cols = []

    for i in range(len(data)):
        values.append([])
        cols.append([])
        for j in range(len(data[i])):
            if data[i][j] == 0: continue

            values[i].append(data[i][j])
            cols[i].append(j)

    width = max(len(row) for row in values)
    for i in range(len(data)):
        values[i] += [0] * (width - len(values[i]))
        cols[i] += [0] * (width - len(cols[i]))

    print("ELLPACK:")
    print(f"{'Value':>{4 * width}}    {'Column':>{4 * width}}")
    for i in range(len(data)):
        for value in values[i]:
            print(f"{value:>4}", end="")
        print(" " * 4, end="")
        for col in cols[i]:
            print(f"{col:>4}", end="")
        print()

def main():
    data = import_data()

    print_matrix(data)
    print_coordinate(data)
    print_csr(data)
    print_ellpack(data)

if __name__ == "__main__":
    main()
