import src.population_preff as pref
import src.vote_analysis as analyze
import src.vote_tallie as tale

import numpy as np
import pandas as pd

population_size = 1000
#candidate_size = 10

#preferences = 3 # politics dimension

N = 1000
#total = 0 # number of runs where the top candidate wins out right
# 80% of the time the first winner will stay the winner

#total_top_candidate = 0
#total_top_two = 0

avg_votes_cast = []
rc_mv = []
fptp_mv = []

num_candidates_vals = []
pol_dim_vals = []
pol_duty_max_vals = []
ranked_positions_vals = []
c_0_vals = []
dc_vals = []
F_vals = []

for _ in range(N):

    num_candidates = np.random.randint(2, 22 + 1)
    pol_dim = np.random.randint(1, 20)
    pol_duty_max = np.random.uniform(0, 2)
    ranked_positions = np.random.randint(2, 10 + 1)
    ranked_positions = max(ranked_positions, num_candidates)
    c_0 = np.random.uniform(0, 1)
    dc = np.random.uniform(0, .3)
    F = np.random.uniform(0, 0.05)

    num_candidates_vals.append(num_candidates)
    pol_dim_vals.append(pol_dim)
    pol_duty_max_vals.append(pol_duty_max)
    ranked_positions_vals.append(ranked_positions)
    c_0_vals.append(c_0)
    dc_vals.append(dc)
    F_vals.append(F)

    pop = pref.uniform_pref(population_size, pol_dim)
    pop_duty = np.random.uniform(0, pol_duty_max, population_size)
    candidates = pref.uniform_pref(num_candidates, pol_dim)

    votes = tale.vote_cost_benefit(pop, candidates, pop_duty, ranked_positions, c_0, dc, F)

    voters = votes[ np.logical_not(np.isnan(votes[:, 0])), :]

    did_vote = voters * 0 + 1
    did_vote[np.isnan(did_vote)] = 0

    avg_votes_cast.append(did_vote.sum() / population_size)

    candidate_ids = [x for x in range(num_candidates)]

    first_round = analyze.get_partial_elections(votes, candidate_ids)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    top_candidate = first_round_ranked_candidates[0]

    total_meaningful_votes = first_round[first_round_ranked_candidates[0]] + first_round[first_round_ranked_candidates[1]]
    total_votes = 0
    for key in first_round:
        total_votes += first_round[key]

    #print("Total Votes:", total_votes)
    #print("Percent of Population:", total_votes / population_size * 100)

    #print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    #print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    fptp_mv.append(total_meaningful_votes)

    # redo candidates

    last_partial_election = {}

    ranked_choice_winner = analyze.analyze_election(votes, num_candidates, PE=last_partial_election)
    # get last partial election

    total_votes = analyze.total_participants(votes)

    #print("Total Votes:", total_votes)
    #print("Percent of Population:", total_votes / population_size * 100)

    total_meaningful_votes = 0
    for key in last_partial_election:
        total_meaningful_votes += last_partial_election[key]

    #print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    #print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    rc_mv.append(total_meaningful_votes)

data = pd.DataFrame()

data["Average Votes Cast"] = avg_votes_cast
data["Ranked Choice Meaningful Votes"] = rc_mv
data["Traditional Meaningful Votes"] = fptp_mv
data["Number Candidates"] = num_candidates_vals
data["Politics Dimension"] = pol_dim_vals
data["Max Duty"] = pol_duty_max_vals
data["Number of Ranking Positions"] = ranked_positions_vals
data["c_0"] = c_0_vals
data["dc"] = dc_vals
data["F"] = F_vals

data.to_csv("data/Vote_Totals_Data.csv", index=None)
