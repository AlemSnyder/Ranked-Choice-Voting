import src.population_preff as pref
import src.plotting_graphs as analyze
import src.vote_tallie as tale

population_size = 1000
candidate_size = 10

preferences = 21

N = 1000
#total = 0 # number of runs where the top candidate wins out right
# 80% of the time the first winner will stay the winner

total_top_candidate = 0
total_top_two = 0

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

    ranked_choice_winner = analyze.analyze_election(votes)

    # print(top_candidate, ranked_choice_winner)

    if top_candidate == ranked_choice_winner:
        total_top_candidate += 1

    if ranked_choice_winner in (first_round_ranked_candidates[0:2]):
        total_top_two +=1

print("rate top candidate", total_top_candidate / N)
print("rate top two candidate", total_top_two / N)

# rate top candidate 0.837
# rate top two candidate 0.837

# 0.824
# 0.955