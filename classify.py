import matplotlib.pyplot as plt

def extract(file):
    with open(file) as f:
        return [float(v) for v in f.readlines()]

def classifier(values : list):
    c = {
        0.00175 : 0,
        0.00180 : 0,
        0.00185 : 0,
        0.00190 : 0,
        0.00195 : 0
    }

    for v in values:
        if 0.00175 <= v < 0.00180:
            c[0.00175] += 1
        elif 0.00180 <= v < 0.00185:
            c[0.00180] += 1
        elif 0.00185 <= v < 0.00190:
            c[0.00185] += 1
        elif 0.00190 <= v < 0.00195:
            c[0.00190] += 1
        elif 0.00195 <= v < 0.00200:
            c[0.00195] += 1

    return list(c.keys()), list(c.values())

if __name__ == '__main__':
    values = extract('fichier.txt')
    x, y = classifier(values)
    plt.plot(x, y)
    plt.show()