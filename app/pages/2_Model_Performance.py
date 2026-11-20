from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Model Performance", layout="wide")

# result files made by notebook 05 and notebook 08
DATA = Path(__file__).parents[1] / "data"
GROUPS = ["toddler", "child", "adolescent", "adult"]

# cv_summary.csv has two header rows (metric name, then mean or std)
cv = pd.read_csv(DATA / "cv_summary.csv", header=[0, 1], index_col=[0, 1])
cross = pd.read_csv(DATA / "cross_source.csv")
chosen = pd.read_csv(DATA / "chosen_models.csv", index_col="group")

st.title("Model Performance")
st.markdown("""
This page shows how well the models did when they were tested. Six models were compared for each age group.

**How they were tested.** The data was cut into 5 parts. A model learned from 4 parts and was tested on
the part it had not seen. This was done for every part, and the whole thing was repeated 3 times, so
each model was tested 15 times. This is called *cross-validation*. The total questionnaire score was
not given to the models, only the ten answers and the personal details.
""")

with st.expander("What the numbers mean"):
    st.markdown("""
All of these go from 0 to 1. Higher is better, except for the Brier score.

* **accuracy** – share of people the model got right. Example: 95 right out of 100 = 0.95.
* **precision** – of the people the model marked as "ASD traits", how many really were. Example: it marks 10, and 8 are correct = 0.8.
* **recall** – of the people who really had "ASD traits", how many the model found. Example: 10 such people, the model finds 9 = 0.9. In screening this matters most, because a missed case gets no follow-up.
* **f1** – one number that mixes precision and recall. It is only high when both are high.
* **roc_auc** – how well the model puts people with traits above people without. 1.0 is perfect, 0.5 is the same as guessing.
* **brier** – how far the model's percentages are from the truth. **Lower is better**, 0 is perfect.
* **± value** – how much the result changed between the 15 tests. A small value means stable results.

Other words on this page:

* **SMOTE** – Synthetic Minority Over-sampling Technique. When one class has far fewer records, it makes extra, similar records for that class, for training only. Example: 100 "no" and 40 "yes" records become 100 and 100.
* **EBM** – Explainable Boosting Machine, a model whose reasoning can be read directly.
* **TabPFN** – Tabular Prior-data Fitted Network, a ready-trained model for small tables.
""")

st.subheader("Model used by this app")
st.markdown("For each age group the app uses the model that did best in the tests above.")
st.dataframe(chosen.round(3), width="stretch")
st.caption("TabPFN was compared in the study but is not deployed, because it needs PyTorch "
           "and large model weights.")

st.subheader("Cross-validation results")
group = st.radio("Age group", GROUPS, horizontal=True)
table = cv.loc[group]
# split the table into the averages and the spreads
means = table.xs("mean", axis=1, level=1)
stds = table.xs("std", axis=1, level=1)
st.markdown("Average over the 15 tests, with the spread after the ± sign.")
st.dataframe((means.round(3).astype(str) + " ± " + stds.round(3).astype(str)), width="stretch")
st.bar_chart(means[["roc_auc", "recall", "f1"]])

st.subheader("Trained on one source, tested on another")
st.markdown("""
Here a model learns from one dataset and is tested on a dataset collected by someone else. This shows
if it still works on new data. The numbers are ROC-AUC (1.0 is perfect).

Toddlers: Thabtah (ASDTests) ↔ Saudi Arabia. Adults: UCI ↔ Kaggle.
""")
# one row for each train and test pair, one column for each model
st.dataframe(cross.pivot_table(index=["train", "test"], columns="model", values="roc_auc", sort=False).round(3),
             width="stretch")

st.info("Why are so many numbers close to 1.0? In the main datasets the label was made by the questionnaire's "
        "own scoring rule (score above the cut-off). A model only has to learn to add up the answers, so "
        "very high results are expected. See **About** for what this means.")

st.subheader("Harder settings: fewer questions and noisy answers")
st.markdown("""
With all ten answers a model can simply learn the scoring rule, so the results above do not show which
model is really better. Two harder tests were added:

* **Fewer questions.** The model gets only the 4, 6 or 8 most useful questions and must still predict the
  result of the full questionnaire.
* **Noisy answers.** 5%, 10% or 20% of the answers are changed at random before testing (a 0 becomes a 1,
  or a 1 becomes a 0). This is like a parent who misreads a question.

The tables show the average over 10 tests.
""")
harder = pd.read_csv(DATA / "harder_settings.csv")
metric = st.radio("Metric", ["roc_auc", "recall"], horizontal=True, format_func=lambda m: {"roc_auc": "ROC-AUC", "recall": "Recall"}[m])
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Questions available**")
    # results for the chosen age group only
    q = harder[(harder.setting == "questions") & (harder.group == group)]
    st.dataframe(q.pivot(index="model", columns="value", values=metric).rename(columns=int), width="stretch")
with col2:
    st.markdown("**Share of answers changed**")
    n = harder[(harder.setting == "noise") & (harder.group == group)]
    st.dataframe(n.pivot(index="model", columns="value", values=metric), width="stretch")
