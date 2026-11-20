import csv

def import_data():
    rules = {}

    with open('data/lr6.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["rule_name"]
            if name not in rules:
                rules[name] = {"operator": row["operator"], "conditions": []}

            rules[name]["conditions"].append((row["condition"], float(row["md"]), float(row["mnd"])))

    return rules

def min_or_max(rule):
    operator = rule["operator"]
    
    if operator == "AND":
        return min(md for _, md, _ in rule["conditions"]), min(mnd for _, _, mnd in rule["conditions"])
    elif operator == "OR":
        return max(md for _, md, _ in rule["conditions"]), max(mnd for _, _, mnd in rule["conditions"])
    else:
        raise ValueError(f"Unknown operator: {operator}")

def calculate_trust_measure(e1, e2):
    return e1 + e2 * (1 - e1)

def main():
    rules = import_data()
    assumptions = {}

    for name, rule in rules.items():
        assumptions[name] = min_or_max(rule)

    for name, (md, mnd) in assumptions.items():
        print(f"Предположение: {name}, MD: {md}, MND: {mnd}")

    md = calculate_trust_measure(assumptions["E1"][0], assumptions["E2"][0])
    mnd = calculate_trust_measure(assumptions["E1"][1], assumptions["E2"][1])

    print(f"Итоговый коэффициент уверенности (формула Шортлиффа): KU = {md - mnd}, MD = {md}, MND = {mnd}")


if __name__ == "__main__":
    main()
