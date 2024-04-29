import matplotlib.pyplot as plt
import numpy as np
import typing

def weakest_candidate(election_tally):
    candidate = -1
    votes = np.inf
    for c, v in election_tally.items():
        if v < votes:
            votes = v
            candidate = c
    return candidate

def plot_results(partial_election):
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
        f'Number of Voters: {total_votes}')


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

    plt.show()

def analyze_election(votes, display = False):
    num_voters, num_candidates = votes.shape

    runoff_candidates = [x for x in range(num_candidates)]

    while len(runoff_candidates) > 1:
        partial_election = {x : 0 for x in runoff_candidates}
        for ballot in votes:
            for candidate in ballot:
                if candidate in partial_election:
                    partial_election[candidate] += 1
                    break
        if display:
            print("Instant runoff result")
            print(partial_election)
            plot_results(partial_election)
            
        lowest_candidate = weakest_candidate(partial_election)
        if display:
            print("removing lowest candidate", lowest_candidate)
        runoff_candidates.remove(lowest_candidate)

    return runoff_candidates[0]


if __name__ == "__main__":
    import vote_tallie
    import population_preff

    pop = population_preff.random_pref(1000, 21)
    candidates = population_preff.random_pref(10, 21)

    votes = vote_tallie.vote(pop, candidates)

    print(analyze_election(votes, True))
