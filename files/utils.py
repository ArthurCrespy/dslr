import os
import sys
import csv
import math
import matplotlib.pyplot

## CSV Utils ##

def csv_parse(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            data = {}
            for row in reader:
                for key, value in row.items():
                    if key not in data:
                        data[key] = []
                    if value.strip():
                        data[key].append(value.strip())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return data


def csv_parse_pair(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            data = {}
            for row in reader:
                for key, value in row.items():
                    if key not in data:
                        data[key] = []
                    if not value:
                        data[key].append(None)
                    elif value.strip():
                        data[key].append(value.strip())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return data


## Theta Utils ##

def thetas_create(thetas, features, file_path=".theta.csv"):
    try:
        with open(file_path, 'w') as f:
            f.write(",".join(features) + ',Bias' + "\n")
            for theta in thetas:
                f.write(",".join(map(str, theta)) + "\n")
    except Exception as e:
        print(f"An error occurred while creating file '{file_path}'\n\t -> {e}")
        return None, None


def thetas_initialize(n):
    return [0.0] * n

## Color Utils ##

def color_cmap(n, color_map='Set3'):
    return matplotlib.pyplot.cm.get_cmap(color_map, n)


def color_house():
    colors = {}
    houses = { 'Ravenclaw': 0, 'Hufflepuff': 8, 'Slytherin': 2, 'Gryffindor': 3 }

    for house, index in houses.items():
        colors[house] = matplotlib.pyplot.cm.tab10(houses[house])

    return colors


## Maths Utils ##

def maths_sigmoid(z):
    return 1 / (1 + math.exp(-z))


def maths_matrix_multiply(vector, weights):
    return sum(v * w for v, w in zip(vector, weights))


def maths_beta(a, b):
    log_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)

    return math.exp(log_beta)


def maths_beta_incomplete(x, a, b):
    total = 0.0
    n_steps = 10000
    step = x / n_steps

    for i in range(n_steps):
        t = i * step
        total += (t ** (a - 1)) * ((1 - t) ** (b - 1)) * step

    return total


def maths_anova_distri(F, d1, d2):
    if F <= 0:
        return 1

    x = (d1 * F) / (d1 * F + d2)

    a = d1 / 2
    b = d2 / 2

    B = maths_beta(a, b)
    I = maths_beta_incomplete(x, a, b) / B

    return 1 - I


## Stats Utils ##

def stats_mean(values):
    if not values:
        return None

    return sum(values) / len(values)


def stats_std(values):
    if not values:
        return None

    return math.sqrt(sum([((v - stats_mean(values)) ** 2) for v in values]) / len(values))


def stats_standardize(values):
    if not values:
        return None, None, None

    result = []

    mean = stats_mean(values)
    std = math.sqrt(sum([((v - mean) ** 2) for v in values]) / len(values))

    for v in values:
        result.append((v - mean) / std)

    return result


def stats_anova_interpret(F, p):
    if p < 0.05 and F >= 100:
        return f"Very high variance (F: {F:.3f})"
    elif p >= 0.5 and F < 0.5:
        return f"Very low variance (F: {F:.3f})"

    if p < 0.05:
        result = f"Very homogenous (p: {p:.3f})"
    elif p < 0.09:
        result = f"Homogenous (p: {p:.3f})"
    elif p < 0.25:
        result = f"Almost homogeneous (p: {p:.3f})"
    elif p < 0.3:
        result = f"Borderline (p: {p:.3f})"
    else:
        result = f"Uneven (p: {p:.3f})"

    if F < 0.5:
        result += f" with very low variance (F: {F:.3f})"
    elif F < 1:
        result += f" with low variance (F: {F:.3f})"
    elif F < 10:
        result += f" with acceptable variance (F: {F:.3f})"
    elif F < 100:
        result += f" with high variance (F: {F:.3f})"
    else:
        result += f" with very high variance (F: {F:.3f})"

    return result


def stats_anova(values):
    if not values:
        return None

    N = sum(len(group) for group in values.values())
    k = len(values)

    mean_global = sum(sum(group) for group in values.values()) / N

    ssbw = sum(len(group) * ((sum(group) / len(group)) - mean_global) ** 2 for group in values.values())
    sswt = sum(sum((x - (sum(group) / len(group))) ** 2 for x in group) for group in values.values())

    dfbw = k - 1
    dfwt = N - k

    msbw = ssbw / dfbw
    mswt = sswt / dfwt

    F = msbw / mswt
    p = maths_anova_distri(F, dfbw, dfwt)

    return F, p