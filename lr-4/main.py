import math
import csv
from typing import List

def import_data():
    data = []

    with open('data/lr4.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([int(x) for x in row])

    return data

def cos_similarity(a: List[int], b: List[int]):
    if len(a) != len(b): return 0

    ab_sum = 0
    a_sum = 0
    b_sum = 0

    for i in range(len(a)):
        if a[i] == 0 or b[i] == 0: continue

        ab_sum += a[i]*b[i]
        a_sum += a[i]**2
        b_sum += b[i]**2

    denominator = math.sqrt(a_sum) * math.sqrt(b_sum)
    if denominator == 0: return 0

    return ab_sum / denominator

def mean_rating(ratings: List[int]):
    rated = [x for x in ratings if x != 0]
    if len(rated) == 0: return 0

    return sum(rated) / len(rated)

def similarity_matrix(users: List[List[int]]):
    matrix = []

    for i in range(len(users)):
        matrix.append([])
        for j in range(len(users)):
            matrix[i].append(0 if i == j else cos_similarity(users[i], users[j]))

    return matrix

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

def find_most_similar(sim: List[List[float]], a: int):
    num = -1
    max_sim = -1

    for u in range(len(sim)):
        if u == a: continue

        if sim[a][u] > max_sim:
            max_sim = sim[a][u]
            num = u

    return num

def predict_rating(users: List[List[int]], sim: List[List[float]], a: int, neighbours: List[int], item: int):
    numerator = 0
    denominator = 0

    for u in neighbours:
        if users[u][item] == 0: continue

        numerator += (users[u][item] - mean_rating(users[u])) * sim[a][u]
        denominator += abs(sim[a][u])

    if denominator == 0: return 0

    return mean_rating(users[a]) + numerator / denominator

def recommend(users: List[List[int]], sim: List[List[float]], names: List[str], a: int):
    neighbours = [find_most_similar(sim, a)]
    best_item = -1
    best_rating = 0

    for item in range(len(users[a])):
        if users[a][item] != 0: continue

        rating = predict_rating(users, sim, a, neighbours, item)
        if rating > best_rating:
            best_rating = rating
            best_item = item

    if best_item == -1:
        print(f"{names[a]} рекомендовать нечего")
        return

    print(f"{names[a]} рекомендовать P{best_item + 1} (прогноз {best_rating:.2f}, похожий {names[neighbours[0]]})")

def find_best_product(products: List[List[int]]):
    best_item = 0

    for item in range(len(products)):
        if mean_rating(products[item]) > mean_rating(products[best_item]):
            best_item = item

    return best_item

def main():
    products = import_data()
    all_users = list(map(list, zip(*products)))
    all_names = [f"U{i+1}" for i in range(len(all_users))]

    excluded = int(input("Номер пользователя для исключения: ")) - 1

    users = []
    names = []
    for i in range(len(all_users)):
        if i == excluded: continue

        users.append(all_users[i])
        names.append(all_names[i])

    sim = similarity_matrix(users)

    print()
    print(f"Подобие пользователей (исключён U{excluded + 1}):")
    print_matrix(sim, names)
    print()

    best_item = find_best_product(products)

    for a in range(len(users)):
        if mean_rating(users[a]) == 0:
            print(f"{names[a]} новый, рекомендовать P{best_item + 1}")
        else:
            recommend(users, sim, names, a)

    print()
    print(f"Новому пользователю рекомендовать P{best_item + 1} (средний рейтинг {mean_rating(products[best_item]):.2f})")

if __name__ == "__main__":
    main()
