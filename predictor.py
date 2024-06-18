import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

training_csv = pd.read_csv("data.csv")
predicting_csv = pd.read_csv("test_data.csv")

def create_predictors(matches, training):
    matches["opp_code"] = matches["Away"].astype("category").cat.codes
    matches["hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype("int")
    matches["Date"] = pd.to_datetime(matches["Date"])
    matches["day_code"] = matches["Date"].dt.dayofweek.astype("int")

    if training:
        scores = matches["Score"].to_list()
        home_score = [(score.split("–")[0][-1]) for score in scores]
        away_score = [(score.split("–")[1][0]) for score in scores]
        W_or_L = ["W" if home_score[i] > away_score[i] else "L" for i in range(len(home_score))]
        matches["result"] = W_or_L
    return matches

training = create_predictors(training_csv, True)
predicting = create_predictors(predicting_csv, False)

rf = RandomForestClassifier(n_estimators=50,min_samples_split=10, random_state=1)

train = training[training["Date"] < '2016-07-11']

test = training[training["Date"] > '2016-07-11']


predictors = ["opp_code", "hour", "day_code"]
rf.fit(train[predictors], train["result"])

preds = rf.predict(predicting[predictors])
for row_index,result in enumerate(preds):
    print("Home: " + predicting.loc[row_index]["Home"] + " Away: " + predicting.loc[row_index]["Away"] + " Result:" + result)

