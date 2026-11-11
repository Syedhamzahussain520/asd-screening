from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Model Performance", layout="wide")

DATA = Path(__file__).parents[1] / "data"
GROUPS = ["toddler", "child", "adolescent", "adult"]

cv = pd.read_csv(DATA / "cv_summary.csv", header=[0, 1], index_col=[0, 1])
cross = pd.read_csv(DATA / "cross_source.csv")
chosen = pd.read_csv(DATA / "chosen_models.csv", index_col="group")

st.title("Model Performance")
st.markdown("""
Six models were compared on each age group using **repeated stratified 5-fold cross-validation**
(3 repeats, 15 test folds), with hyperparameters tuned *inside* each training fold and SMOTE
applied to training data only. The questionnaire score was removed from the inputs.
""")

st.subheader("Model used by this app")
st.dataframe(chosen.round(3), width="stretch")
st.caption("TabPFN was compared in the study but is not deployed, because it needs PyTorch "
           "and large model weights.")

st.subheader("Cross-validation results")
group = st.radio("Age group", GROUPS, horizontal=True)
table = cv.loc[group]
means = table.xs("mean", axis=1, level=1)
stds = table.xs("std", axis=1, level=1)
st.dataframe((means.round(3).astype(str) + " ± " + stds.round(3).astype(str)), width="stretch")
st.bar_chart(means[["roc_auc", "recall", "f1"]])

st.subheader("Trained on one source, tested on another")
st.markdown("Toddlers: Thabtah (ASDTests) ↔ Saudi Arabia. Adults: UCI ↔ Kaggle.")
st.dataframe(cross.pivot_table(index=["train", "test"], columns="model", values="roc_auc", sort=False).round(3),
             width="stretch")

st.info("In the main datasets the label was produced by the questionnaire's own scoring rule, so "
        "very high scores are expected. See **About** for what this means.")

st.subheader("Harder settings: fewer questions and noisy answers")
st.markdown("""
With all ten answers the scoring rule can be recovered exactly, so the scores above say little about
how the models compare. Two harder tests: the model sees only the 4, 6 or 8 most informative
questions and must predict the full-questionnaire result, or it is tested after 5–20% of the
answers have been flipped at random. Mean over 10 folds.
""")
harder = pd.read_csv(DATA / "harder_settings.csv")
metric = st.radio("Metric", ["roc_auc", "recall"], horizontal=True, format_func=lambda m: {"roc_auc": "ROC-AUC", "recall": "Recall"}[m])
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Questions available**")
    q = harder[(harder.setting == "questions") & (harder.group == group)]
    st.dataframe(q.pivot(index="model", columns="value", values=metric).rename(columns=int), width="stretch")
with col2:
    st.markdown("**Share of answers flipped**")
    n = harder[(harder.setting == "noise") & (harder.group == group)]
    st.dataframe(n.pivot(index="model", columns="value", values=metric), width="stretch")
