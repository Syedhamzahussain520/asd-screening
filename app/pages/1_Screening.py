from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st

from questions import GROUPS, question_list, score_answer

st.set_page_config(page_title="Screening", layout="centered")

# folder with the saved models, one file for each age group
MODELS = Path(__file__).parents[1] / "models"

# names shown in the chart for the personal details
LABELS = {"age": "Age", "male": "Sex (male)", "jaundice": "Born with jaundice",
          "family_asd": "Family member with autism"}


# cache_resource: the model file is loaded once and then kept in memory
@st.cache_resource
def load_bundle(group):
    return joblib.load(MODELS / f"{group}.joblib")


# SHAP = SHapley Additive exPlanations. It tells how much each answer moved the model's number.
# Example: the model says 80%, the average is 50%, and Q1 gets +10% of that difference
def explain(bundle, row):
    features = bundle["features"]
    model = bundle["model"]

    def predict(data):
        return model.predict_proba(pd.DataFrame(data, columns=features))[:, 1]

    # background = a few rows of training data that SHAP compares this person with
    explainer = shap.Explainer(predict, bundle["background"], seed=42)
    return pd.Series(explainer(row).values[0], index=features)


st.title("Screening")

group = st.selectbox("Who is being screened?", list(GROUPS), format_func=lambda g: GROUPS[g]["label"])
# questionnaire name, age range and cut-off for the chosen group
info = GROUPS[group]
questions = question_list(group)

st.caption(f"Questionnaire: {info['questionnaire']}. Please answer every question. "
           "There are no right or wrong answers. Pick the answer that fits best.")

# a form, so the page only runs the model after the button is pressed
with st.form("screening"):
    answers = []
    for i, (text, options) in enumerate(questions, start=1):
        # index=None: no answer is chosen at the start
        answers.append(st.radio(f"**{i}.** {text}", options, index=None, key=f"{group}_q{i}"))

    st.divider()
    st.caption("A few personal details. The model was trained with them, so it needs them too. "
               "They do not change the questionnaire score.")
    low, high = info["age_range"]
    age = st.number_input(f"Age ({info['age_unit']})", min_value=low, max_value=high, value=low, step=1)
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    jaundice = st.radio("Born with jaundice?", ["No", "Yes"], horizontal=True,
                        help="Jaundice is yellow skin in the first days after birth. It is common in newborn babies.")
    family = st.radio("Does an immediate family member have autism?", ["No", "Yes"], horizontal=True)

    submitted = st.form_submit_button("Get result", type="primary")

# nothing below runs until the button is pressed
if not submitted:
    st.stop()

# every question must be answered
if None in answers:
    missing = [str(i) for i, a in enumerate(answers, start=1) if a is None]
    st.error(f"Please answer question(s) {', '.join(missing)}.")
    st.stop()

bundle = load_bundle(group)
# change each answer into 1 (points towards traits) or 0
scored = [score_answer(group, i, a) for i, a in enumerate(answers, start=1)]
# one row with the same columns, in the same order, as the training data
row = pd.DataFrame([scored + [age, int(sex == "Male"), int(jaundice == "Yes"), int(family == "Yes")]],
                   columns=bundle["features"])

# the model gives two numbers (no, yes). We take the second one
prob = bundle["model"].predict_proba(row)[0, 1]
total = sum(scored)
# the standard rule: a score higher than the cut-off
above = total > info["cutoff"]

# the questionnaire score is the main result
st.header("Result")
col1, col2 = st.columns(2)
col1.metric(f"{info['questionnaire']} score", f"{total} / 10")
col2.metric("Cut-off", f"above {info['cutoff']}")
st.caption("The score is the number of answers that point towards autistic traits. "
           f"Each such answer is 1 point. A score above {info['cutoff']} means a full assessment may be useful.")

if above:
    st.error(f"The score is **{total}**, which is above the cut-off of {info['cutoff']}. The answers show "
             "**signs of autistic traits**. It would be worth talking to a health professional about a full assessment.")
else:
    st.success(f"The score is **{total}**, which is not above the cut-off of {info['cutoff']}. The answers do "
               "**not** show clear signs of autistic traits. If you still have concerns, please talk to a "
               "health professional. Screening tools can miss things.")

# the model comes second
st.subheader("What the model says")
st.metric("Model output", f"{prob:.0%}")
st.markdown(
    f"The model ({bundle['model_name']}) has learned from past screening records. Its number shows how sure "
    "the model is that these answers belong to the group *above the cut-off*. Close to 100% means "
    "\"very sure it is above\", close to 0% means \"very sure it is not\".\n\n"
    "**It is not the chance that the person has autism.** With all ten answers the model normally "
    "agrees with the score. It is shown here to demonstrate how such a model can explain itself."
)
# 50% or more counts as "above" for the model
if (prob >= 0.5) != above:
    st.warning("Here the model and the score do not agree. The score is the standard result, so please go by the score.")

# explanation
st.header("Why did the model give this number?")
st.markdown("Each bar in the chart is one of your answers. A **red** bar pushed the model's number **up**. "
            "A **blue** bar pushed it **down**. A longer bar means a bigger push. "
            "Only the eight answers with the biggest effect are shown.")
contrib = explain(bundle, row)
# A1..A10 are shown as Q1..Q10
names = {f: f"Q{f[1:]}" for f in bundle["features"] if f.startswith("A")} | LABELS
contrib = contrib.rename(index=names)
# the eight biggest effects, the biggest at the top of the chart
shown = contrib.reindex(contrib.abs().sort_values(ascending=False).index)[:8][::-1]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(shown.index, shown.values, color=["#d9775f" if v > 0 else "#6b9ac4" for v in shown.values])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("push on the model's number (SHAP value)")
plt.tight_layout()
st.pyplot(fig)

# up to three answers that raised the number and three that lowered it. Very small effects are left out
up = contrib[contrib > 0.01].sort_values(ascending=False).index[:3].tolist()
down = contrib[contrib < -0.01].sort_values().index[:3].tolist()
text = []
if up:
    text.append(f"The answers that **raised** the model's number most were {', '.join(up)}.")
if down:
    text.append(f"The answers that **lowered** it most were {', '.join(down)}.")
st.markdown(" ".join(text))
st.caption("Q1 to Q10 are the ten questions above. The bar lengths are SHAP values. SHAP (SHapley Additive "
           "exPlanations) is a method that shares out the model's number between the answers.")

with st.expander("Your scored answers"):
    st.markdown("\"Counts towards traits\" says if the answer gives 1 point. The score is the number of \"yes\" rows.")
    st.dataframe(pd.DataFrame({"question": [t for t, _ in questions], "your answer": answers,
                               "counts towards traits": ["yes" if s else "no" for s in scored]},
                              index=[f"Q{i}" for i in range(1, 11)]))

st.info("This tool is a research demonstration and a screening aid, **not a diagnosis**. "
        "Nothing you entered has been saved.")
