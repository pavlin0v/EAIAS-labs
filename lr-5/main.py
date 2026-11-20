import math
import csv
from typing import List

THRESHOLD = 0.995

def import_data():
    data = []

    with open('data/lr5.csv', 'r') as f:
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

def similarity_matrix(items: List[List[int]]):
    matrix = []

    for i in range(len(items)):
        matrix.append([])
        for j in range(len(items)):
            matrix[i].append(0 if i == j else cos_similarity(items[i], items[j]))

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
                print(f"{value:>{width}.3f}", end="")
        print()

def find_max(data: List[List[float]]):
    max_item = (0, 1, -1)

    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if data[i][j] > max_item[2]: max_item = (i, j, data[i][j])

    return max_item

def merge_clusters(data: List[List[float]], clusters: List[List[int]], a: int, b: int):
    for i in range(len(data)):
        data[a][i] = max(data[a][i], data[b][i])
        data[i][a] = data[a][i]
    data[a][a] = 0

    del data[b]
    for row in data:
        del row[b]

    clusters[a] = clusters[a] + clusters[b]
    del clusters[b]

def cluster_name(cluster: List[int]):
    return ", ".join(f"P{i+1}" for i in cluster)

def find_clusters(sim: List[List[float]]):
    data = [row[:] for row in sim]
    clusters = [[i] for i in range(len(sim))]

    i,j,max_sim = find_max(data)

    while max_sim >= THRESHOLD:
        print(f"Объединяем ({cluster_name(clusters[i])}) и ({cluster_name(clusters[j])}) с подобием {max_sim:.3f}")
        merge_clusters(data, clusters, i, j)

        i,j,max_sim = find_max(data)

    return clusters

def predict_rating(ratings: List[int], sim: List[List[float]], item: int, cluster: List[int]):
    numerator = 0
    denominator = 0

    for j in cluster:
        if j == item or ratings[j] == 0: continue

        numerator += ratings[j] * sim[item][j]
        denominator += abs(sim[item][j])

    if denominator == 0: return 0

    return numerator / denominator

def recommend(ratings: List[int], sim: List[List[float]], clusters: List[List[int]], name: str):
    best_item = -1
    best_rating = 0

    for cluster in clusters:
        for item in cluster:
            if ratings[item] != 0: continue

            rating = predict_rating(ratings, sim, item, cluster)
            if rating > best_rating:
                best_rating = rating
                best_item = item

    if best_item == -1:
        print(f"{name} рекомендовать нечего")
        return

    print(f"{name} рекомендовать P{best_item + 1} (прогноз {best_rating:.2f})")

def find_best_product(products: List[List[int]]):
    best_item = 0

    for item in range(len(products)):
        if mean_rating(products[item]) > mean_rating(products[best_item]):
            best_item = item

    return best_item

def main():
    products = import_data()
    users = list(map(list, zip(*products)))
    names = [f"P{i+1}" for i in range(len(products))]

    sim = similarity_matrix(products)

    print("Подобие товаров:")
    print_matrix(sim, names)
    print()

    clusters = find_clusters(sim)
    print(f"Кластеры (R = {THRESHOLD}):", "; ".join(f"({cluster_name(c)})" for c in clusters))
    print()

    best_item = find_best_product(products)

    for a in range(len(users)):
        if mean_rating(users[a]) == 0:
            print(f"U{a + 1} новый, рекомендовать P{best_item + 1}")
        else:
            recommend(users[a], sim, clusters, f"U{a + 1}")
            
if __name__ == "__main__":
    main()
