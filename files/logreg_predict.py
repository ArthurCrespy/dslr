import sys
import utils

def statistics_compute(data, weights):
    stats = {}
    x = []
    y = []
    i = 0

    for key, values in data.items():
        if key == "Hogwarts House":
            continue
        if key == "Index":
            y = values
            continue
        try:
            valid = [float(v) for v in values if v is not None]
            mean = utils.stats_mean(valid)

            values = [mean if v is None else float(v) for v in values]
        except ValueError:
            continue

        stats[key] = {}

        stats[key]['mean'] = weights['mean'][i]
        stats[key]['std'] = weights['std'][i]
        stats[key]['scores'] = [0 if v == 0 else (v - stats[key]['mean']) / stats[key]['std'] for v in values]

        i += 1

    for i in range(len(stats[next(iter(stats))]['scores'])):
        row = []
        for key in stats.keys():
            if key == "Index":
                continue
            row.append(stats[key]['scores'][i])
        x.append(row)

    return stats, x, y


def logreg_predict(stats, weights, x, y):
    n_samples = len(x)
    n_features = len(x[0])
    house_names = list(weights.keys())[:-2]

    predictions = []
    for i in range(n_samples):
        probabilities = []

        for house_name in house_names:
            bias = weights[house_name][-1]
            z = utils.maths_sigmoid(sum(weights[house_name][j] * x[i][j] for j in range(n_features)) + bias)
            probabilities.append(z)

        predicted_class = probabilities.index(max(probabilities))
        predictions.append(house_names[predicted_class])

    return predictions


def main():
    if len(sys.argv) != 2:
        print("Usage: logreg_predict.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse_pair(sys.argv[1])
    weights = utils.weights_read()
    stats, x, y = statistics_compute(data, weights)
    result = logreg_predict(stats, weights, x, y)
    utils.results_create(result)


if __name__ == "__main__":
    main()
