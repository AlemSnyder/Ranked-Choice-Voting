import numpy as np
import numba

if __name__ == "__main__":
    import plotting_graphs
else:
    from . import plotting_graphs

def weakest_candidate(election_tally):
    candidate = -1
    votes = np.inf
    for c, v in election_tally.items():
        if v < votes:
            votes = v
            candidate = c
    return candidate

def strongest_candidate(election_tally):
    candidate = -1
    votes = -np.inf
    for c, v in election_tally.items():
        if v > votes:
            votes = v
            candidate = c
    return candidate

def get_partial_elections(votes, runoff_candidates, pop = None, candidates = None, display = False):

    partial_election = {x : 0 for x in runoff_candidates} # crate dictionary
    top_candidates = [] # who each voter is voting for if -1 then None
    for ballot in votes:
        casts_vote = False
        for candidate in ballot:
            if candidate in partial_election:
                partial_election[candidate] += 1
                top_candidates.append(candidate)
                casts_vote = True
                break
        if not casts_vote:
            top_candidates.append(-1)

    if display:

        print("Instant runoff result")
        print(partial_election)
        plotting_graphs.plot_results(partial_election, True)

        if not pop is None and not candidates is None:
            plotting_graphs.plot_2D_political_position(pop, runoff_candidates, partial_election, candidates, top_candidates, True)


    return partial_election

def analyze_election(votes, num_candidates, pop = None, candidates = None, display = False, PE = None):
    #num_voters, ballot_length = votes.shape

    runoff_candidates = [x for x in range(num_candidates)]

    partial_election = {}
    while len(runoff_candidates) > 1:
        partial_election = get_partial_elections(votes, runoff_candidates, pop, candidates, display)
            
        lowest_candidate = weakest_candidate(partial_election)
        if display:
            print("removing lowest candidate", lowest_candidate)
        runoff_candidates.remove(lowest_candidate)

    if not PE is None:
        for key in partial_election:
            PE[key] = partial_election[key]

    return runoff_candidates[0]

def total_participants(votes: np.ndarray) -> int:

    first_choice = votes[:, 0]
    first_choice = first_choice[np.logical_not(np.isnan(first_choice))]

    return first_choice.size[0]

# Condorcet winner does not work if every candidate is not ranked
# every candidate must be ranked
# need this information
def condorcet_winner(votes):
    num_voters, num_candidates = votes.shape
    x = 0
    y = 1
    while x != y:
        partial_election = get_partial_elections(votes, [x, y])
        out = strongest_candidate(partial_election)
        if out == x:
            y += 1
            y = y % num_candidates
        else:
            if x < y:
                return None
            else:
                x = y
                y = x + 1
    return x

if __name__ == "__main__":
    import vote_tallie
    import population_preff

    num_candidates = 10
    politics_dim = 2

    pop = population_preff.uniform_pref(1000, politics_dim)
    candidates = population_preff.uniform_pref(num_candidates, politics_dim)

    votes = vote_tallie.vote_name_recognition(pop, candidates)

    print("Winning candidate:", analyze_election(votes, num_candidates, pop = pop, candidates = candidates, display = True))
