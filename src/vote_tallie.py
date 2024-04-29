import numpy as np

def vote(population, candidates) -> np.array:
    out = np.zeros((population.shape[0], candidates.shape[0]))
    for i in range (len(population)):
        preference = population[i]
        order = [x for x in range(len(candidates))]
        order.sort( key = lambda x : np.linalg.norm(preference - candidates[x]))
        out[i] = order

    return out

if __name__ == "__main__":
    import population_preff
    pop = population_preff.random_pref(20)
    candidates = population_preff.random_pref(7)

    votes = vote(pop, candidates)

    print(votes)