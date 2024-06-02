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
def vote_optimal(population, candidates, ranked_positions = -1) -> np.array:
    """
    Calculate vote totals assuming everyone ranks ranked_positions (defaults to all), and rank
    based on closeness of political values.
    """
    out = np.zeros((population.shape[0], candidates.shape[0]))
    for i in range (len(population)):
        preference = population[i]

        goodness = frobenius_norm(candidates - preference)

        out[i] = np.argsort(goodness)

    return out[:, 0:ranked_positions]

@njit(parallel = True)
def vote_name_recognition(population, candidates, ranked_positions = -1) -> np.array:
    """
    Calculate vote totals assuming everyone ranks ranked_positions (defaults to all), and rank
    based on the logarithm of the closeness of political values. and a name recognition term.
    """
    name_recognition = np.arange(candidates.shape[0]) / 10
    out = np.zeros((population.shape[0], candidates.shape[0]), dtype=np.int8) # change to higher value if 
    # more than 120 candidates are needed
    for i in range (len(population)):
        preference = population[i]

        goodness = name_recognition + np.log(frobenius_norm(candidates - preference))

        out[i] = np.argsort(goodness)

    # print(out[:, 0:3])

    return out[:, 0:ranked_positions]

# cost to voting for candidates
# initial cost to vote for first candidate
# then linear cost for each additional voter

# the willingness to vote
# V = D + F / r 
# D is a duty term, F is a candidate importance term
# r is the distance in political position.

# the cost of voting is
# C = c_0 for the first candidate
# and dc for each additional candidate
# an initial cost and a small cost for each additional candidate.

# for FPTP
# voters cast ballot if V > c_0 where v is minimized over all candidates
# votes for r best candidate

# count voting participation

# for RC vote if C < V over all candidates
# vote for second candidate if second closest F/r > dc
# vote for nth candidate if F/r > n * dc

#@njit(parallel = True)
def vote_cost_benefit(population, candidates, pop_duty, ranked_positions = -1, c_0 = .5, dc = .1, F = 0.02) -> np.array:

    out = np.zeros( ( population.shape[0], candidates.shape[0] ) )
    for i in range(len(population)):
        preference = population[i]
        r = frobenius_norm(candidates - preference)
        candidates_preference_order = np.argsort(r)

        votes = np.full(candidates.shape[0], np.nan)

        for c in range(len(candidates_preference_order)):
            if c == 0 and pop_duty[i] + F / r[c] > c_0:
                votes[c] = candidates_preference_order[c]
                continue
            elif c != 0 and pop_duty[i] + F / r[c] > c * dc:
                votes[c] = candidates_preference_order[c]
                continue
            else:
                break
        
        out[i] = votes

    if ranked_positions != -1:
        return out[:, 0:ranked_positions]
    else:
        return out


if __name__ == "__main__":
    import population_preff

    N = 100

    pop = population_preff.uniform_pref(N, 3)
    candidates = population_preff.uniform_pref(7, 3)
    pop_duty = np.random.uniform(0, 1, N)

    #votes = vote_optimal(pop, candidates)

    #print(votes)

    votes = vote_cost_benefit(pop, candidates, pop_duty, c_0 = 0.3)

    print(votes)