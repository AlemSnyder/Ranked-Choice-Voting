import json
import pandas as pd

def analyze_to_csv(f, file_path):

    Uniform = json.load(f)

    # ["0"] - ["0"] / 1000 * 100

    data_out = pd.DataFrame()

    data = []
    for pol_dim in Uniform["Ranked_Choice"]["3"]:

        data.append(int(pol_dim))

    data_out["Politics Dim"] = data

    for key in Uniform["Ranked_Choice"]:
        data = []
        for pol_dim in Uniform["Ranked_Choice"][key]:
            rc_val = Uniform["Ranked_Choice"][key][pol_dim]["0"] # number of best winner
            fc_val = Uniform["First_Past_Post"][key][pol_dim]["0"] # number of best winner

            data.append((rc_val - fc_val) / 100)

        data_out[key] = data

    data_out.to_csv(file_path, index=None)


with open('data/Normal_3_Candidates.json', 'r', encoding='utf-8') as f:

    analyze_to_csv(f, "data/Normal.csv")

with open('data/Uniform_All_Candidates.json', 'r', encoding='utf-8') as f:

    analyze_to_csv(f, "data/Uniform.csv")

