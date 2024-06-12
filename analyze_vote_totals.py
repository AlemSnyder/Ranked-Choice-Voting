import pandas as pd

population_size = 1000

data = pd.read_csv("data/Vote_Totals_Data.csv")

data = data.drop( data[data["Traditional Meaningful Votes"] > (.9 * population_size) ].index )
data = data.drop( data[data["Traditional Meaningful Votes"] < (.1 * population_size) ].index )

data["Candidate Fraction Ranked"] = data["Average Votes Cast"] / data["Number Candidates"]

data["Estimator"] = 2 * (3/2) ** data["Politics Dimension"] * data["Average Votes Cast"]


data.to_csv("data/Vote_Totals_out.csv", index = None)

# 1- fraction have voted * 


#data["estimator"] = 1.5 ** data["Politics Dimension"] * data["Average Votes Cast"]

data_1 = data[data["dif"] > 0]
data_2 = data[data["dif"] < 0]

data_1.to_csv("data/Votes_High_RC.csv", index=None)
data_2.to_csv("data/Votes_High_TR.csv", index=None)


