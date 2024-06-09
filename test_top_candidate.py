import src.population_preff as pref
import src.vote_analysis as analyze
import src.vote_tallie as tale

import json
import numpy as np

# data to be written to file
json_data = {}
json_data["Ranked_Choice"] = {}
json_data["First_Past_Post"] = {}

population_size = 1000


N = 100


for candidate_size in range(3, 11):

    json_data["Ranked_Choice"][candidate_size] = {}
    json_data["First_Past_Post"][candidate_size] = {}

    for preferences in range(1, 22):

        # position of winning RC in ranking of candidates
        # closest candidates to the mean position get ranked higher
        position = {x : 0 for x in range(candidate_size)}
        # same, but for FPTP
        top_candidate_position = {x: 0 for x in range(candidate_size)}


        for _ in range(N):
            pop = pref.uniform_pref(population_size, preferences)
            candidates = pref.uniform_pref(candidate_size, preferences)

            candidate_ids = [x for x in range(candidate_size)]

            votes = tale.vote_optimal(pop, candidates)

            electorate_average = pop.mean(axis=0)

            first_round = analyze.get_partial_elections_fast(votes, candidate_ids)
            first_round_ranked_candidates = [x for x in first_round.keys()]
            first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

            top_candidate = first_round_ranked_candidates[0]

            ranked_choice_winner = analyze.analyze_election(votes, candidate_size)

            condorcet_winner = analyze.condorcet_winner(votes)

            condorcet_proxy = sorted(candidate_ids, key = lambda x : np.linalg.norm(candidates[x] - electorate_average), reverse=False)

            position[condorcet_proxy.index(ranked_choice_winner)] += 1
            top_candidate_position[condorcet_proxy.index(top_candidate)] +=1

            json_data["Ranked_Choice"][candidate_size][preferences] = position
            json_data["First_Past_Post"][candidate_size][preferences] = top_candidate_position

    with open('data/Uniform_All_Candidates.json', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


json_data = {}
json_data["Ranked_Choice"] = {}
json_data["First_Past_Post"] = {}

for candidate_size in range(3, 11):

    json_data["Ranked_Choice"][candidate_size] = {}
    json_data["First_Past_Post"][candidate_size] = {}

    for preferences in range(1, 22):

        # position of winning RC in ranking of candidates
        # closest candidates to the mean position get ranked higher
        position = {x : 0 for x in range(candidate_size)}
        # same, but for FPTP
        top_candidate_position = {x: 0 for x in range(candidate_size)}


        for _ in range(N):
            # normal distribution
            pop = pref.normal_pref(population_size, preferences)
            candidates = pref.normal_pref(candidate_size, preferences)

            candidate_ids = [x for x in range(candidate_size)]

            votes = tale.vote_optimal(pop, candidates, 3) # now only rank three candidates

            electorate_average = pop.mean(axis=0)

            first_round = analyze.get_partial_elections_fast(votes, candidate_ids)
            first_round_ranked_candidates = [x for x in first_round.keys()]
            first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

            top_candidate = first_round_ranked_candidates[0]

            ranked_choice_winner = analyze.analyze_election(votes, candidate_size)

            condorcet_winner = analyze.condorcet_winner(votes)

            condorcet_proxy = sorted(candidate_ids, key = lambda x : np.linalg.norm(candidates[x] - electorate_average), reverse=False)

            position[condorcet_proxy.index(ranked_choice_winner)] += 1
            top_candidate_position[condorcet_proxy.index(top_candidate)] +=1

            json_data["Ranked_Choice"][candidate_size][preferences] = position
            json_data["First_Past_Post"][candidate_size][preferences] = top_candidate_position

    with open('data/Normal_3_Candidates.json', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

