import sys
import math
import utils
import matplotlib.pyplot as plt

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

        stats[key]['stats'] = {}
        stats[key]['scores'] = {}

        for house in set(data['Hogwarts House']):
            stats[key]['scores'][house] = [v for v, h in zip(values, data['Hogwarts House']) if h == house]

            stats[key]['stats'][house] = {}
            stats[key]['stats'][house]['mean'] = utils.stats_mean(stats[key]['scores'][house])

        stats[key]['stats']['F'], stats[key]['stats']['p'] = utils.stats_anova(stats[key]['scores'])

    return stats


def statistics_display(stats):
    plt_combinations = list(stats.items())
    plt_size = len(plt_combinations)

    fig, axs = plt.subplots(int(math.sqrt(plt_size) + 1) , int(math.sqrt(plt_size) + 1), figsize=(25, 25))
    axs = axs.flatten()

    color = utils.color_house()

    for i, (x, y) in enumerate(plt_combinations):
        ax = axs[i]

        for j, house in enumerate(stats[x]['scores'].keys()):
            ax.hist(stats[x]['scores'][house], bins=50, color=color[house], alpha=0.7)
            ax.set_title(f"Histogram of scores by Hogwarts house for {x}")
            ax.set_xlabel("Score")
            ax.set_ylabel("Number of students")
            ax.text(0.03, 0.95, utils.stats_anova_interpret(stats[x]['stats']['F'], stats[x]['stats']['p']), fontsize=10, bbox=dict(facecolor='white', edgecolor='black'), transform=ax.transAxes)
            ax.grid(axis='x', linestyle='-', alpha=0.3)
            ax.grid(axis='y', linestyle='-', alpha=0.3)

    for ax in axs[plt_size:]:
        ax.remove()

    fig.legend(list(color.keys()) , title="Hogwarts Houses", bbox_to_anchor=(0.285, 0.07))

    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: histogram.py <dataset.csv>")
        sys.exit(1)

    data = utils.csv_parse(sys.argv[1])
    stats = statistics_compute(data)

    statistics_display(stats)


if __name__ == "__main__":
    main()