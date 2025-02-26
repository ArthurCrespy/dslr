import sys
import math
import utils
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt

def matplotlib_configure():
    mpl.use('TkAgg')
    plt.rcParams['figure.dpi'] = 20


def statistics_compute(data):
    stats = {}

    remove = set()
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
        stats[key]['scores'] = {}

        for house in set(data['Hogwarts House']):
            stats[key]['scores'][house] = [v for v, h in zip(values, data['Hogwarts House']) if h == house]

    return stats


def statistics_display(stats):
    plt_combinations = list(itertools.combinations(list(stats.keys()), 2))
    plt_size = len(plt_combinations)

    fig, axs = plt.subplots(int(math.sqrt(plt_size) + 1) , int(math.sqrt(plt_size) + 1), figsize=(50, 50))
    axs = axs.flatten()

    color = utils.color_house()

    for i, (x, y) in enumerate(plt_combinations):
        ax = axs[i]

        for j, house in enumerate(stats[x]['scores'].keys()):
            ax.scatter(stats[x]['scores'][house], stats[y]['scores'][house], color=color[house], alpha=0.7)
            ax.set_title(f"Scatter plot of scores in {x} vs {y}")
            ax.set_xlabel(f"Scores in {x}")
            ax.set_ylabel(f"Scores in {y}")
            ax.grid(axis='x', linestyle='-', alpha=0.3)
            ax.grid(axis='y', linestyle='-', alpha=0.3)

    for ax in axs[plt_size:]:
        ax.remove()

    fig.legend(list(color.keys()) , title="Hogwarts Houses", bbox_to_anchor=(0.693, 0.035))

    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: histogram.py <dataset.csv>")
        sys.exit(1)

    try:
        matplotlib_configure()
        data = utils.csv_parse_pair(sys.argv[1])
        stats = statistics_compute(data)
        statistics_display(stats)
    except Exception as e:
        print(f"An error occurred while running the program \n\t -> {e.__class__.__name__}: {e}")


if __name__ == "__main__":
    main()