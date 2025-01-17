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


def logreg_train(stats, houses, x, y, algo, learning_rate=0.001, iteration_max=1000, tolerance=1e-6):
    n_samples = len(x)
    n_features = len(x[0])
    n_houses = len(houses)

    print(f"Training parameters - algo: {algo}, learning rate: {learning_rate}, max iterations: {iteration_max}, tolerance: {tolerance}")
    print(f"Input dataset       - samples: {n_samples}, features: {n_features - 1}, houses: {n_houses}\n")

    weights = [utils.weights_initialize(n_features) for _ in range(n_houses)]

    for house_index, house_name in enumerate(houses):
        house_binary = [1 if label == house_index else 0 for label in y]
        log_loss_prev = float('inf')

        for iteration in range(iteration_max):
            log_loss = 0

            if algo == "stochastic":
                indices = list(range(n_samples))
                for i in indices:
                    z = utils.maths_sigmoid(sum(weights[house_index][j] * x[i][j] for j in range(n_features)))
                    log_loss += house_binary[i] * math.log(z) + (1 - house_binary[i]) * math.log(1 - z)

                    for j in range(n_features):
                        gradient = (z - house_binary[i]) * x[i][j]
                        weights[house_index][j] -= learning_rate * gradient

                log_loss = -log_loss / n_samples

            elif algo == "batch":
                batch_size = 32

                for batch_start in range(0, n_samples, batch_size):
                    batch_end = min(batch_start + batch_size, n_samples)
                    batch_x = x[batch_start:batch_end]
                    batch_y = house_binary[batch_start:batch_end]
                    batch_log_loss = 0
                    gradients = [0] * n_features


                    for i in range(len(batch_x)):
                        z = utils.maths_sigmoid(sum(weights[house_index][j] * batch_x[i][j] for j in range(n_features)))
                        batch_log_loss += batch_y[i] * math.log(z) + (1 - batch_y[i]) * math.log(1 - z)

                        for j in range(n_features):
                            gradients[j] += (z - batch_y[i]) * batch_x[i][j]

                    for j in range(n_features):
                        weights[house_index][j] -= learning_rate * (gradients[j] / len(batch_x))

                    batch_log_loss = -batch_log_loss / len(batch_x)
                    log_loss += batch_log_loss

            else:
                for i in range(n_samples):
                    z = utils.maths_sigmoid(sum(weights[house_index][j] * x[i][j] for j in range(n_features)))
                    log_loss += house_binary[i] * math.log(z) + (1 - house_binary[i]) * math.log(1 - z)

                for i in range(n_features):
                    gradient = 0
                    for j in range(n_samples):
                        z = utils.maths_sigmoid(sum(weights[house_index][k] * x[j][k] for k in range(n_features)))
                        gradient += (z - house_binary[j]) * x[j][i]

                    weights[house_index][i] -= learning_rate * (gradient / n_samples)

                log_loss = -log_loss / n_samples


            if abs(log_loss_prev - log_loss) < tolerance or iteration == iteration_max - 1:
                print(f"Model for house {house_name} trained after {iteration + 1} iterations. (log loss: {log_loss})")
                break

            log_loss_prev = log_loss

    return weights


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: logreg_train.py <dataset.csv> [algorithm]")
        sys.exit(1)

    dataset = sys.argv[1]
    algo = "normal"

    if len(sys.argv) == 3:
        algo = sys.argv[2]
        if algo == "-n":
            algo = "normal"
        elif algo == "-s":
            algo = "stochastic"
        elif algo == "-b":
            algo = "batch"
        else:
            print("Invalid algorithm. Use -n (normal), -s (stochastic), or -b (batch).")
            sys.exit(1)

    data = utils.csv_parse_pair(dataset)
    stats, houses, x, y = statistics_compute(data)
    weights = logreg_train(stats, houses, x, y, algo)
    utils.weights_create(stats, houses, weights)


if __name__ == "__main__":
    main()