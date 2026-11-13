import math
import csv
from typing import List

def import_data():
    data = []

    with open('data/lr1.csv', 'r') as f:
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

def find_max_similarity(data: List[List[int]], item_type: str):
    num_a = 0
    num_b = 1
    max_sim = -1

    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            sim = cos_similarity(data[i], data[j])
            if sim > max_sim:
                max_sim = sim
                num_a = i
                num_b = j

    print(f"Максимальное подобие: {max_sim:.5f} между {num_a + 1} и {num_b + 1} {item_type}")

def main():
    products = import_data()
    users = list(map(list, zip(*products)))

    find_max_similarity(products, "продуктом")
    find_max_similarity(users, "пользователем")

if __name__ == "__main__":
    main()
