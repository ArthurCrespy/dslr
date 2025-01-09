import sys
import utils

def statistics_compute(data):
    stats = {}

    for column, values in data.items():
        try:
            values = [float(v) for v in values]
        except ValueError:
            continue

        if not values or column == "Index":
            continue

        stats[column] = {}

        n = len(values)
        stats[column]['Count'] = n

        mean = sum(values) / n
        stats[column]['Mean'] = mean

        variance = sum([((x - mean) ** 2) for x in values]) / n
        std_dev = variance ** 0.5
        stats[column]['Std'] = std_dev

        val_min = min(values)
        val_max = max(values)
        stats[column]['Min'] = val_min
        stats[column]['Max'] = val_max

        values_sorted = sorted(values)
        q1 = values_sorted[n // 4]
        q2 = values_sorted[n // 2]
        q3 = values_sorted[(3 * n) // 4]
        stats[column]['25%'] = q1
        stats[column]['50%'] = q2
        stats[column]['75%'] = q3

    return stats


def statistics_display(stats):
    width_column = 15
    features = [feature.ljust(10) if len(feature) < 10 else (feature[:9] + '.') for feature in list(stats.keys())]
    print("".join(["Statistic".ljust(width_column)] + [i.ljust(width_column) for i in features]))

    for i in ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]:
        row = [i.ljust(width_column)]
        for feature in list(stats.keys()):
            value = f"{stats[feature][i]:.6f}"
            row.append(value.ljust(width_column))
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