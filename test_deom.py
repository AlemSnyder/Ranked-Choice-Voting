import src.population_preff as pref
import src.plotting_graphs as analyze
import src.vote_tallie as tale

import numpy as np
import matplotlib.pyplot as plt

population_size = 1000
candidate_size = 10

preferences = 2

totals = {x : 0 for x in range(candidate_size)}

pop = pref.uniform_pref(population_size, preferences)
candidates = pref.uniform_pref(candidate_size, preferences)

votes = tale.vote_name_recognition(pop, candidates)

first_round = analyze.get_partial_elections(votes, candidate_size)
first_round_ranked_candidates = [x for x in first_round.keys()]
first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

top_candidate = first_round_ranked_candidates[0]

ranked_choice_winner = analyze.analyze_election_2(votes, candidate_size, pop, candidates, True)

totals[first_round_ranked_candidates.index(ranked_choice_winner)] += 1


plt.scatter(pop[:, 0], pop[:, 1], s = 4, c = votes[:,0], cmap = "tab10")

plt.scatter(candidates[:, 0], candidates[:, 1], s = 50, c = [x for x in range(candidate_size)], cmap = "tab10")

plt.show()


