import sys
import csv
import matplotlib.pyplot

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

            for column, row in data.items():
                if len(row) != len(data['Index']):
                    print(f"Error: Missing value in column {column}")
                    sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return data


def color_cmap(n, color_map='Set3'):
    return matplotlib.pyplot.cm.get_cmap(color_map, n)


def color_house():
    colors = {}
    houses = { 'Ravenclaw': 0, 'Hufflepuff': 8, 'Slytherin': 2, 'Gryffindor': 3 }

    for house, index in houses.items():
        colors[house] = matplotlib.pyplot.cm.tab10(houses[house])

    return colors


def maths_sum(values):
    if not values:
        return None

    result = 0
    for i in range(len(values)):
        result += float(values[i])

    return result


def maths_mean(values):
    if not values:
        return None

    return maths_sum(values) / len(values)


def maths_max(values):
    if not values:
        return None

    result = float(values[0])
    for i in range(len(values)):
        if float(values[i]) > result:
            result = float(values[i])

    return result


def maths_min(values):
    if not values:
        return None

    result = float(values[0])
    for i in range(len(values)):
        if float(values[i]) < result:
            result = float(values[i])

    return result

def maths_abs(value):
    return value if value >= 0 else -value


def maths_sqrt(value):
    return value ** 0.5