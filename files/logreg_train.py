import sys
import math
import utils

def statistics_compute(data):
    stats = {}
    remove = set()
    x = []

    for key, values in data.items():
        for i, v in enumerate(values):
            if v is None:
                remove.add(i)

    for key in data.keys():
        data[key] = [v for i, v in enumerate(data[key]) if i not in remove]

    for key, values in data.items():
        try:
            values = [float(v) for v in values]
        except ValueError:
            continue

        if not values or key == "Index":
            continue

        stats[key] = {}

        stats[key]['mean'] = utils.stats_mean(values)
        stats[key]['std'] = utils.stats_std(values)
        stats[key]['scores'] = utils.stats_standardize(values)

    for i in range(len(data['Hogwarts House'])):
        row = []
        for key in stats.keys():
            row.append(stats[key]["scores"][i])
        x.append(row)
    x = [row + [1] for row in x]

    houses = {house: h for h, house in enumerate(list(set(data['Hogwarts House'])))}
    y = [houses[label] for label in data['Hogwarts House']]

    return stats, houses, x, y


def logreg_train(stats, houses, x, y, learning_rate=0.001, iteration_max=1000, tolerance=1e-8):
    n_samples = len(x)
    n_features = len(x[0])
    n_houses = len(houses)

    print(f"Learning rate: {learning_rate}, max iterations: {iteration_max}, tolerance: {tolerance}")
    print(f"Input: {n_samples} samples for each {n_features - 1} features and {n_houses} different houses \n")

    weights = [utils.weights_initialize(n_features) for _ in range(n_houses)]

    for house_index, house_name in enumerate(houses):
        house_binary = [1 if label == house_index else 0 for label in y]
        log_loss_prev = float('inf')

        for iteration in range(iteration_max):
            log_loss = 0

            for i in range(n_samples):
                z = utils.maths_sigmoid(sum(weights[house_index][j] * x[i][j] for j in range(n_features)))
                log_loss += house_binary[i] * math.log(z) + (1 - house_binary[i]) * math.log(1 - z)
                log_loss = -log_loss / n_samples

            for i in range(n_features):
                gradient = 0
                for j in range(n_samples):
                    z = utils.maths_sigmoid(sum(weights[house_index][k] * x[j][k] for k in range(n_features)))
                    gradient += (z - house_binary[j]) * x[j][i]

                weights[house_index][i] -= learning_rate * (gradient / n_samples)

            if abs(log_loss_prev - log_loss) < tolerance or iteration == iteration_max - 1:
                print(f"Model for house {house_name} trained after {iteration + 1} iterations. (log loss: {log_loss})")
                break

            log_loss_prev = log_loss

    return weights


def main():
    if len(sys.argv) != 2:
        print("Usage: logreg_train.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse_pair(sys.argv[1])
    stats, houses, x, y = statistics_compute(data)
    weights = logreg_train(stats, houses, x, y)
    utils.weights_create(stats, houses, weights)


if __name__ == "__main__":
    main()