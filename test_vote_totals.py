import src.population_preff as pref
import src.vote_analysis as analyze
import src.vote_tallie as tale

import numpy as np

population_size = 1000
candidate_size = 10

preferences = 3

N = 1
#total = 0 # number of runs where the top candidate wins out right
# 80% of the time the first winner will stay the winner

#total_top_candidate = 0
#total_top_two = 0

totals = {x : 0 for x in range(candidate_size)}

for _ in range(N):
    pop = pref.uniform_pref(population_size, preferences)
    pop_duty = np.random.uniform(0,1, population_size)
    candidates = pref.uniform_pref(candidate_size, preferences)

    votes = tale.vote_cost_benefit(pop, candidates, pop_duty)

    candidate_ids = [x for x in range(candidate_size)]

    first_round = analyze.get_partial_elections(votes, candidate_ids)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    top_candidate = first_round_ranked_candidates[0]

    total_meaningful_votes = first_round[first_round_ranked_candidates[0]] + first_round[first_round_ranked_candidates[1]]
    total_votes = sum(first_round)

    print("Total Votes:", total_votes)
    print("Percent of Population:", total_votes / population_size * 100)

    print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    # redo candidates

    last_partial_election = {}

    ranked_choice_winner = analyze.analyze_election(votes, candidate_size, PE=last_partial_election)
    # get last partial election

    total_votes = analyze.total_participants(votes)

    print("Total Votes:", total_votes)
    print("Percent of Population:", total_votes / population_size * 100)

    total_meaningful_votes = 0
    for key in last_partial_election:
        total_meaningful_votes += last_partial_election[key]

    print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    totals[first_round_ranked_candidates.index(ranked_choice_winner)] += 1

print(totals)
