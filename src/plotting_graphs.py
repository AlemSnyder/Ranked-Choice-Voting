import matplotlib.pyplot as plt
import numpy as np
import numba

SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

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

# plots the election
def plot_results(partial_election, save = False):
    fig, ax1 = plt.subplots(figsize=(9, 7), layout='constrained')
    fig.canvas.manager.set_window_title('Partial Election results')


    candidates = list(partial_election.keys())
    votes = np.fromiter(partial_election.values(), dtype = float )
    order = np.arange(len(candidates), dtype = int )

    candidates_vote_pairs = np.array([votes, candidates]).transpose()
    candidates_vote_pairs = candidates_vote_pairs[candidates_vote_pairs[:, 0].argsort()].transpose()

    # print(candidates_vote_pairs)

    total_votes = votes.sum()
    max_votes = votes.max()

    ax1.set_title("Results")
    ax1.set_xlabel(
        'Popular Vote\n'
        f'Number of Voters: {int(total_votes)}')


    # percentiles = [score.percentile for score in scores_by_test.values()]

    color = ["tab:blue" for x in candidates]
    color[0] = "tab:red"
    if (candidates_vote_pairs[0][-1] / total_votes > .5):
        color[-1] = "tab:green"

    rects = ax1.barh(order, candidates_vote_pairs[0] / total_votes * 100, align='center', height=0.5, color = color)
    # Partition the percentile values to be able to draw large numbers in
    # white within the bar, and small numbers in black outside the bar.
    #large_percentiles = [to_ordinal(p) if p > 40 else '' for p in percentiles]
    #small_percentiles = [to_ordinal(p) if p <= 40 else '' for p in percentiles]
    #ax1.bar_label(rects, small_percentiles,
    #              padding=5, color='black', fontweight='bold')
    #ax1.bar_label(rects, large_percentiles,
    #              padding=-32, color='white', fontweight='bold')

    ax1.set_yticks(order, np.array(candidates_vote_pairs[1], dtype = int))

    ticks = [10 * x for x in range( int (max_votes * 10 / total_votes) + 1) ]

    ax1.set_xlim([0, ticks[-1] + 10])
    ax1.set_xticks(ticks)
    ax1.xaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
    ax1.axvline(50, color='grey', alpha=0.25)  # median position

    # Set the right-hand Y-axis ticks and labels
    #ax2 = ax1.twinx()
    # Set equal limits on both yaxis so that the ticks line up
    #ax2.set_ylim(ax1.get_ylim())

    # Set the tick locations and labels
    #ax2.set_yticks( NO TICKS
    #    np.arange(len(scores_by_test)),
    #    labels=[format_score(score) for score in scores_by_test.values()])

    # ax2.set_ylabel('Test Scores')

    if not save:
        plt.show()
    else:
        plt.savefig(f"plots/tally_{ len(partial_election) }.png")
    plt.clf()

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
        plot_results(partial_election, True)

        if not pop is None and not candidates is None:

            plt.scatter(pop[:, 0], pop[:, 1], s = 4, c = top_candidates, cmap = "tab10")

            candidates_array = np.array(runoff_candidates)
            available_positions = candidates[candidates_array]

            plt.scatter(available_positions[:,0], available_positions[:,1], s = 50, c = runoff_candidates, cmap = "tab10")
            plt.gca().set_aspect('equal', adjustable='box')
            plt.savefig(f"plots/scatter_{ len(partial_election) }.png")
            plt.clf()


    return partial_election

def analyze_election(votes, num_candidates, pop = None, candidates = None, display = False):
    #num_voters, ballot_length = votes.shape

    runoff_candidates = [x for x in range(num_candidates)]

    while len(runoff_candidates) > 1:
        partial_election = get_partial_elections(votes, runoff_candidates, pop, candidates, display)
            
        lowest_candidate = weakest_candidate(partial_election)
        if display:
            print("removing lowest candidate", lowest_candidate)
        runoff_candidates.remove(lowest_candidate)

    return runoff_candidates[0]

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

    pop = population_preff.uniform_pref(1000, 21)
    candidates = population_preff.uniform_pref(num_candidates, 21)

    votes = vote_tallie.vote_optimal(pop, candidates)

    print("Winning candidate:", analyze_election(votes, num_candidates, pop = pop, candidates = candidates, display = True))
