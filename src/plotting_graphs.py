import matplotlib.pyplot as plt
import numpy as np
import typing

def weakest_candidate(election_tally):
    candidate = -1
    votes = np.inf
    for c, v in election_tally.items():
        if v < votes:
            votes = v
            candidate = c
    return candidate

def analyze_election(votes, display = False):
    num_voters, num_candidates = votes.shape

    runoff_candidates = [x for x in range(num_candidates)]

    while len(runoff_candidates) > 1:
        partial_election = {x : 0 for x in runoff_candidates}
        for ballot in votes:
            for candidate in ballot:
                if candidate in partial_election:
                    partial_election[candidate] += 1
                    break
        if display:
            print("Instant runoff result")
            print(partial_election)
            
        lowest_candidate = weakest_candidate(partial_election)
        if display:
            print("removing lowest candidate", lowest_candidate)
        runoff_candidates.remove(lowest_candidate)

    return runoff_candidates[0]


if __name__ == "__main__":
    import vote_tallie
    import population_preff

    pop = population_preff.random_pref(1000, 21)
    candidates = population_preff.random_pref(10, 21)

    votes = vote_tallie.vote(pop, candidates)

    print(analyze_election(votes, True))
