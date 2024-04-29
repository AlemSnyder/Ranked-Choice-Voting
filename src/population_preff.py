import numpy as np


def random_pref(persons = 100, pref = 3):
    return np.random.uniform(size=(persons, pref))


if __name__ == "__main__":
    print(random_pref(10, 2))