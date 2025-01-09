import sys
import utils
import itertools
import matplotlib.pyplot as plt

def statistics_compute(data):
    stats = {}

    remove = set()
    for column, values in data.items():
        for i, v in enumerate(values):
            if v is None:
                remove.add(i)

    for column in data.keys():
        data[column] = [v for i, v in enumerate(data[column]) if i not in remove]

    for column, values in data.items():
        try:
            values = [float(v) for v in values]
        except ValueError:
            continue

        if not values or column == "Index":
            continue

        stats[column] = {}

        for house in set(data['Hogwarts House']):
            stats[column][house] = [v for v, h in zip(values, data['Hogwarts House']) if h == house]

    return stats


def statistics_display(stats):
    plt_combinations = list(itertools.combinations(stats.keys(), 2))
    plt_size = len(plt_combinations)

    fig, axs = plt.subplots(int(utils.maths_sqrt(plt_size) + 1) , int(utils.maths_sqrt(plt_size) + 1), figsize=(50, 50))
    axs = axs.flatten()

    color = utils.color_house()

    for i, (x, y) in enumerate(plt_combinations):
        ax = axs[i]

        for j, house in enumerate(stats[x].keys()):
            ax.scatter(stats[x][house], stats[y][house], color=color[house], alpha=0.7)
            ax.set_title(f"Scatter plot of scores in {x} vs {y}")
            ax.set_xlabel(f"Scores in {x}")
            ax.set_ylabel(f"Scores in {y}")
            ax.grid(axis='x', linestyle='-', alpha=0.3)
            ax.grid(axis='y', linestyle='-', alpha=0.3)

    for ax in axs[plt_size:]:
        ax.remove()

    fig.legend(list(color.keys()) , title="Hogwarts Houses", bbox_to_anchor=(0.995, 0.030))

    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: histogram.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse_pair(sys.argv[1])
    stats = statistics_compute(data)

    statistics_display(stats)


if __name__ == "__main__":
    main()