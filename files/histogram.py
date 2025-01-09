import sys
import math
import utils
import matplotlib.pyplot as plt

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
        stats[column]['scores'] = {}
        stats[column]['stats'] = {}

        for house in set(data['Hogwarts House']):
            stats[column]['scores'][house] = {}
            stats[column]['stats'][house] = {}
            stats[column]['scores'][house] = [v for v, h in zip(values, data['Hogwarts House']) if h == house]
            stats[column]['stats'][house]['mean'] = utils.stats_mean(stats[column]['scores'][house])

    for column, values in stats.items():
        if stats[column]['stats']['variation'] < result:
            result = stats[column]['stats']['variation']
            course = column

    print(f"The course with the most homogeneous score distribution between all four houses is {course} with a variation of {result:.2f}%")

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