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


def logreg_train(stats, houses, x, y, learning_rate=0.01, iteration_max=100000, tolerance=1e-6):
    n_samples = len(x)
    n_features = len(x[0])
    n_houses = len(houses)

    print(f"Learning rate: {learning_rate}, max iterations: {iteration_max}, tolerance: {tolerance}")
    print(f"Input: {n_samples} samples with {n_features} features and {n_houses} houses: {houses}")

    weights = [utils.thetas_initialize(n_features) for _ in range(n_houses)]

    for house_index, house_name in enumerate(houses):
        house_binary = [1 if label == house_index else 0 for label in y]
        previous_loss = float('inf')

        for iteration in range(iteration_max):
            gradients = [0.0] * n_features
            total_loss = 0.0

            for i in range(n_samples):
                z = utils.maths_matrix_multiply(x[i], weights[house_index])
                error = utils.maths_sigmoid(z) - house_binary[i]

                for j in range(n_features):
                    gradients[j] += error * x[i][j]

                total_loss += -house_binary[i] * math.log(utils.maths_sigmoid(z) + 1e-6) - (1 - house_binary[i]) * math.log(1 - utils.maths_sigmoid(z) + 1e-6)

            for j in range(n_features):
                weights[house_index][j] -= learning_rate * (gradients[j] / n_samples)

            if abs(previous_loss - total_loss) < tolerance or iteration == iteration_max - 1:
                print(f"Model for house {house_name} trained after {iteration + 1} iterations. (last loss: {total_loss})")
                break

            previous_loss = total_loss

    for weights_value in weights:
        for i, key in enumerate(stats):
            weights_value[i] = weights_value[i] * stats[key]['std'] + stats[key]['mean']

    return weights


def main():
    if len(sys.argv) != 2:
        print("Usage: logreg_train.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse_pair(sys.argv[1])
    stats, houses, x, y = statistics_compute(data)
    thetas = logreg_train(stats, houses, x, y)
    utils.thetas_create(thetas, stats.keys())


if __name__ == "__main__":
    main()


# -- Results from MPB on 14/01/25 -- #
# Learning rate: 0.01, max iterations: 100000, tolerance: 1e-06
# Input: 1251 samples with 14 features and 4 houses: {'Hufflepuff': 0, 'Gryffindor': 1, 'Ravenclaw': 2, 'Slytherin': 3}
# Model for house Hufflepuff trained after 100000 iterations. (last loss: 68.59352007938718)
# Model for house Gryffindor trained after 100000 iterations. (last loss: 52.49510410125179)
# Model for house Ravenclaw trained after 81332 iterations. (last loss: 81.75424237817141)
# Model for house Slytherin trained after 100000 iterations. (last loss: 40.09832363412982)