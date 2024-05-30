import numpy as np
from numba import njit
import numba as nb

@njit
def frobenius_norm(a):
    norms = np.empty(a.shape[0], dtype=a.dtype)
    for i in nb.prange(a.shape[0]):
        norms[i] = np.linalg.norm(a[i,:])
    return norms

@njit(parallel = True)
def vote_optimal(population, candidates) -> np.array:
    """
    Calculate vote totals assuming everyone ranks all candidates, and rank
    based on closeness of political values.
    """
    out = np.zeros((population.shape[0], candidates.shape[0]))
    for i in range (len(population)):
        preference = population[i]

        goodness = frobenius_norm(candidates - preference)

        out[i] = np.argsort(goodness)

    return out

@njit(parallel = True)
def vote_name_recognition(population, candidates) -> np.array:
    """
    Calculate vote totals assuming everyone ranks all candidates, and rank
    based on closeness of political values.
    """
    name_recognition = np.arange(candidates.shape[0]) / 10
    out = np.zeros((population.shape[0], candidates.shape[0]))
    for i in range (len(population)):
        preference = population[i]

        goodness = name_recognition + np.log(frobenius_norm(candidates - preference))

        out[i] = np.argsort(goodness)

    print(out[:, 0:3])

    return out[:, 0:3]

if __name__ == "__main__":
    import population_preff
    pop = population_preff.uniform_pref(10000, 3)
    candidates = population_preff.uniform_pref(7, 3)

    votes = vote_optimal(pop, candidates)

    print(votes)