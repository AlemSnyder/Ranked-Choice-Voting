import numpy as np


def uniform_pref(persons = 100, pref = 3):
    return np.random.uniform(size=(persons, pref))

def normal_pref(persons = 100, pref = 3, loc = 0.0, scale = 1.0):
    return np.random.normal(loc=loc, scale=scale, size=(persons, pref))


if __name__ == "__main__":
    print(uniform_pref(10, 2))