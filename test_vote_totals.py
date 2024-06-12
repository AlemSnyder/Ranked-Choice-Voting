import src.population_preff as pref
import src.vote_analysis as analyze
import src.vote_tallie as tale

import numpy as np
import pandas as pd

population_size = 1000
#candidate_size = 10

#preferences = 3 # politics dimension

N = 10000
#total = 0 # number of runs where the top candidate wins out right
# 80% of the time the first winner will stay the winner

#total_top_candidate = 0
#total_top_two = 0

avg_votes_cast = []
rc_mv = []
rc_par = []
fptp_mv = []

num_candidates_vals = []
pol_dim_vals = []
pol_duty_max_vals = []
ranked_positions_vals = []
c_0_vals = []
dc_vals = []
F_vals = []

for _ in range(N):

    num_candidates = np.random.randint(1, 15 + 1) + 2
    pol_dim = np.random.randint(1, 5 + 1)
    pol_duty_max = np.random.uniform(0, 1)
    ranked_positions = np.random.randint(2, 10 + 1)
    c_0 = np.random.uniform(0, 1)
    ranked_positions = max(ranked_positions, num_candidates)
    dc = np.random.uniform(0, .3)
    F = np.random.uniform(0, 0.1)

    num_candidates_vals.append(num_candidates)
    pol_dim_vals.append(pol_dim)
    pol_duty_max_vals.append(pol_duty_max)
    ranked_positions_vals.append(ranked_positions)
    c_0_vals.append(c_0)
    dc_vals.append(dc)
    F_vals.append(F)

    pop = pref.uniform_pref(population_size, pol_dim)
    pop_duty = np.random.uniform(0, pol_duty_max, population_size)

    candidates = np.append([np.ones(pol_dim) * 0.5], [np.ones(pol_dim) * -0.5], axis=0)

    #candidates = pref.uniform_pref(num_candidates, pol_dim)

    votes = tale.vote_cost_benefit(pop, candidates, pop_duty, 1, c_0, dc, F)

    candidate_ids = [x for x in range(2)] # there are 2 candidates originally

    first_round = analyze.get_partial_elections(votes, candidate_ids)
    first_round_ranked_candidates = [x for x in first_round.keys()]
    first_round_ranked_candidates.sort(key = lambda x : first_round[x], reverse=True)

    top_candidate = first_round_ranked_candidates[0]

    total_meaningful_votes = analyze.total_participants(votes)

    #print("Total Votes:", total_votes)
    #print("Percent of Population:", total_votes / population_size * 100)

    #print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    #print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    fptp_mv.append(total_meaningful_votes)

    # redo candidates

    candidates = np.append(candidates, pref.uniform_pref(num_candidates - 2, pol_dim), axis = 0)

    votes = tale.vote_cost_benefit(pop, candidates, pop_duty, ranked_positions, c_0, dc, F)

    voters = votes[ np.logical_not(np.isnan(votes[:, 0])), :]

    voters = votes[ votes[:, 0] == -1, :]

    did_vote = np.ones_like(votes)
    did_vote[votes == -1] = 0
    did_vote[np.isnan(votes)] = 0

    total_votes = analyze.total_participants(votes)
    if total_votes != 0:
        avg_votes_cast.append(did_vote.sum() / total_votes)
    else:
        avg_votes_cast.append(0)

    last_partial_election = {}

    ranked_choice_winner = analyze.analyze_election(votes, num_candidates, PE=last_partial_election)
    # get last partial election

    #print("Total Votes:", total_votes)
    #print("Percent of Population:", total_votes / population_size * 100)

    total_meaningful_votes = 0
    for key in last_partial_election:
        total_meaningful_votes += last_partial_election[key]

    #print("Total Votes for First and Second place Candidate:", total_meaningful_votes)
    #print("Percent of Meaningful Participation:", total_meaningful_votes / population_size * 100)

    rc_mv.append(total_meaningful_votes)
    rc_par.append(total_votes)

data = pd.DataFrame()

data["Average Votes Cast"] = avg_votes_cast
data["Traditional Meaningful Votes"] = fptp_mv
data["Ranked Choice Meaningful Votes"] = rc_mv
data["Ranked Choice Total Participants"] = rc_par
data["Number Candidates"] = num_candidates_vals
data["Politics Dimension"] = pol_dim_vals
data["Max Duty"] = pol_duty_max_vals
data["Number of Ranking Positions"] = ranked_positions_vals
data["c_0"] = c_0_vals
data["dc"] = dc_vals
data["F"] = F_vals

#data = data.drop( data[data["Traditional Meaningful Votes"] > (.9 * population_size) ].index )
#data = data.drop( data[data["Traditional Meaningful Votes"] < (.1 * population_size) ].index )

#print( (data["Traditional Meaningful Votes"] > (.9 * population_size) ) .index)

data["dif"] = data["Ranked Choice Meaningful Votes"] - data["Traditional Meaningful Votes"]

data.to_csv("data/Vote_Totals_Data.csv", index=None)

# plot candidates vs 2^dim * avg votes

# added votes


