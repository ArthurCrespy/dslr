import sys
import math
import utils

def statistics_compute(data):
    stats = {}

    for key, values in data.items():
        try:
            values = [float(v) for v in values]
        except ValueError:
            continue

        if not values or key == "Index":
            continue

        stats[key] = {}

        n = len(values)
        stats[key]['Count'] = n

        mean = sum(values) / n
        stats[key]['Mean'] = mean

        variance = sum([((v - mean) ** 2) for v in values]) / n
        std_dev = math.sqrt(variance)
        stats[key]['Std'] = std_dev

        val_min = min(values)
        val_max = max(values)
        stats[key]['Min'] = val_min
        stats[key]['Max'] = val_max

        values_sorted = sorted(values)
        q1 = values_sorted[n // 4]
        q2 = values_sorted[n // 2]
        q3 = values_sorted[(3 * n) // 4]
        stats[key]['25%'] = q1
        stats[key]['50%'] = q2
        stats[key]['75%'] = q3

    return stats


def statistics_display(stats):
    width = 15
    features = [feature.ljust(10) if len(feature) < 10 else (feature[:9] + '.') for feature in list(stats.keys())]

    print("".join(["Statistic".ljust(width)] + [f.ljust(width) for f in features]))
    for stat in ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]:
        row = [stat.ljust(width)]
        for key in list(stats.keys()):
            row.append(f"{stats[key][stat]:.6f}".ljust(width))
        print("".join(row))


def main():
    if len(sys.argv) != 2:
        print("Usage: describe.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse(sys.argv[1])
    stats = statistics_compute(data)

    statistics_display(stats)


if __name__ == "__main__":
    main()