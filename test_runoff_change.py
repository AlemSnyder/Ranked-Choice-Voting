import src.population_preff as pref
import src.plotting_graphs as analyze
import src.vote_tallie as tale

population_size = 1000
candidate_size = 10

preferences = 3

N = 1000
#total = 0 # number of runs where the top candidate wins out right
# 80% of the time the first winner will stay the winner

#total_top_candidate = 0
#total_top_two = 0

totals = {x : 0 for x in range(candidate_size)}

for _ in range(N):
    pop = pref.random_pref(population_size, preferences)
    candidates = pref.random_pref(candidate_size, preferences)

    votes = tale.vote_optimal(pop, candidates)

    #print(votes)

    first_round = analyze.get_partial_elections(votes)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    #print(first_round)
    #print(first_round_ranked_candidates)

    top_candidate = first_round_ranked_candidates[0]

    ranked_choice_winner = analyze.analyze_election(votes, candidate_size)

    # print(top_candidate, ranked_choice_winner)

    #if top_candidate == ranked_choice_winner:
    #    total_top_candidate += 1

    #if ranked_choice_winner in (first_round_ranked_candidates[0:2]):
    #    total_top_two +=1

    totals[first_round_ranked_candidates.index(ranked_choice_winner)] += 1

#print("rate top candidate", total_top_candidate / N)
#print("rate top two candidate", total_top_two / N)

print(totals)

# rate top candidate 0.837
# rate top two candidate 0.837

# 0.824
# 0.955

# {0: 8292, 1: 1324, 2: 278, 3: 77, 4: 23, 5: 4, 6: 1, 7: 1, 8: 0, 9: 0}
# {0: 8311, 1: 1284, 2: 322, 3: 62, 4: 16, 5: 4, 6: 1, 7: 0, 8: 0, 9: 0}
# {0: 430, 1: 223, 2: 133, 3: 87, 4: 54, 5: 37, 6: 21, 7: 12, 8: 3, 9: 0}