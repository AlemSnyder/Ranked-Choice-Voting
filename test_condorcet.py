import src.population_preff as pref
import src.plotting_graphs as analyze
import src.vote_tallie as tale

import numpy as np

population_size = 1000
candidate_size = 10

preferences = 3

N = 100

totals = 0#{x : 0 for x in range(candidate_size)}
total_con_wta = 0

totals_none = 0

position = {x : 0 for x in range(candidate_size)}
top_candidate_position = {x: 0 for x in range(candidate_size)}

mean_dist_from_average_wta = 0
mean_dist_from_average_rkc = 0
mean_dist_from_average_ccp = 0
mean_dist_from_average_icp = 0

for _ in range(N):
    pop = pref.uniform(population_size, preferences)
    candidates = pref.uniform(candidate_size, preferences)

    candidate_ids = [x for x in range(candidate_size)]

    votes = tale.vote_optimal(pop, candidates)

    average_vote = pop.mean(axis=0)

    first_round = analyze.get_partial_elections(votes, candidate_ids)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    top_candidate = first_round_ranked_candidates[0]

    ranked_choice_winner = analyze.analyze_election(votes, candidate_size)

    condorcet_winner = analyze.condorcet_winner(votes)

    condorcet_proxy = sorted(candidate_ids, key = lambda x : np.linalg.norm(candidates[x] - average_vote), reverse=False)

    if ranked_choice_winner == condorcet_winner:
        totals += 1
    if top_candidate == condorcet_winner:
        total_con_wta +=1
    if condorcet_winner is None:
        totals_none +=1

    position[condorcet_proxy.index(ranked_choice_winner)] += 1
    top_candidate_position[condorcet_proxy.index(top_candidate)] +=1

    mean_dist_from_average_wta += np.linalg.norm(candidates[top_candidate] - average_vote)
    mean_dist_from_average_rkc += np.linalg.norm(candidates[ranked_choice_winner] - average_vote)
    mean_dist_from_average_ccp += np.linalg.norm(candidates[condorcet_proxy[0]] - average_vote)
    mean_dist_from_average_icp += np.linalg.norm(candidates[condorcet_proxy[-1]] - average_vote)

print("chooses best winner", totals)
print("chooses best winner wta", total_con_wta)
print("No clear", totals_none)

print("Position", position)
print("Top Candidate Position", top_candidate_position)

print("mean loss winner take all", mean_dist_from_average_wta / N)
print("mean loss ranked choice", mean_dist_from_average_rkc / N)
print("mean loss best candidate", mean_dist_from_average_ccp / N)
print("mean loss worst candidate", mean_dist_from_average_icp / N)

min = mean_dist_from_average_ccp / N
delta = mean_dist_from_average_icp / N - mean_dist_from_average_ccp / N

print("Winner take all", (mean_dist_from_average_wta / N - min) / delta * 100, "%")
print("Ranked choice", (mean_dist_from_average_rkc / N - min) / delta * 100, "%")

# chooses best winner 6
# No clear 94
# Position {0: 76, 1: 15, 2: 4, 3: 4, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
# Top Candidate Position {0: 27, 1: 32, 2: 12, 3: 9, 4: 5, 5: 9, 6: 2, 7: 2, 8: 1, 9: 1}
# mean loss winner take all 0.35443989790754826
# mean loss ranked choice 0.2713243674626499
# mean loss best candidate 0.24850763742519905
# mean loss worst candidate 0.6739238875743753
# Winner take all 24.900849566795596 %
# Ranked choice 5.363389393200172 %