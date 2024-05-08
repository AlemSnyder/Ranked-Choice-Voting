import src.population_preff as pref
import src.plotting_graphs as analyze
import src.vote_tallie as tale

population_size = 1000
candidate_size = 10

preferences = 21

N = 10

totals = 0#{x : 0 for x in range(candidate_size)}

totals_none = 0

for _ in range(N):
    pop = pref.random_pref(population_size, preferences)
    candidates = pref.random_pref(candidate_size, preferences)

    votes = tale.vote_optimal(pop, candidates)

    average_vote = pop.mean(axis=0)

    first_round = analyze.get_partial_elections(votes)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    top_candidate = first_round_ranked_candidates[0]

    ranked_choice_winner = analyze.analyze_election(votes)

    condorcet_winner = analyze.condorcet_winner(votes)

    #totals[first_round_ranked_candidates.index(ranked_choice_winner)] += 1

    if ranked_choice_winner == condorcet_winner:
        totals += 1
    if condorcet_winner is None:
        totals_none +=1

print("chooses best winner", totals)
print("No clear", totals_none)
