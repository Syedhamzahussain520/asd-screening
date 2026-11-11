from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st

from questions import GROUPS, question_list, score_answer

st.set_page_config(page_title="Screening", layout="centered")

MODELS = Path(__file__).parents[1] / "models"

LABELS = {"age": "Age", "male": "Sex (male)", "jaundice": "Born with jaundice",
          "family_asd": "Family member with autism"}


@st.cache_resource
def load_bundle(group):
    return joblib.load(MODELS / f"{group}.joblib")


def explain(bundle, row):
    features = bundle["features"]
    model = bundle["model"]

    def predict(data):
        return model.predict_proba(pd.DataFrame(data, columns=features))[:, 1]

    explainer = shap.Explainer(predict, bundle["background"], seed=42)
    return pd.Series(explainer(row).values[0], index=features)


st.title("Screening")

group = st.selectbox("Who is being screened?", list(GROUPS), format_func=lambda g: GROUPS[g]["label"])
info = GROUPS[group]
questions = question_list(group)

st.caption(f"Questionnaire: {info['questionnaire']}. Please answer every question.")

with st.form("screening"):
    answers = []
    for i, (text, options) in enumerate(questions, start=1):
        answers.append(st.radio(f"**{i}.** {text}", options, index=None, key=f"{group}_q{i}"))

    st.divider()
    low, high = info["age_range"]
    age = st.number_input(f"Age ({info['age_unit']})", min_value=low, max_value=high, value=low, step=1)
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    jaundice = st.radio("Born with jaundice?", ["No", "Yes"], horizontal=True)
    family = st.radio("Does an immediate family member have autism?", ["No", "Yes"], horizontal=True)

    submitted = st.form_submit_button("Get result", type="primary")

if not submitted:
    st.stop()

if None in answers:
    missing = [str(i) for i, a in enumerate(answers, start=1) if a is None]
    st.error(f"Please answer question(s) {', '.join(missing)}.")
    st.stop()

bundle = load_bundle(group)
scored = [score_answer(group, i, a) for i, a in enumerate(answers, start=1)]
row = pd.DataFrame([scored + [age, int(sex == "Male"), int(jaundice == "Yes"), int(family == "Yes")]],
                   columns=bundle["features"])

prob = bundle["model"].predict_proba(row)[0, 1]
total = sum(scored)

# result
st.header("Result")
col1, col2 = st.columns(2)
col1.metric("Estimated likelihood of ASD traits", f"{prob:.0%}")
col2.metric(f"{info['questionnaire']} score", f"{total} / 10", help=f"The standard cut-off is more than {info['cutoff']}.")

if prob >= 0.5:
    st.error("The answers show **signs of autistic traits**. It would be worth talking to a health "
             "professional about a full assessment.")
else:
    st.success("The answers do **not** show clear signs of autistic traits. If you still have "
               "concerns, please talk to a health professional – screening tools can miss things.")

# explanation
st.header("Why this result?")
contrib = explain(bundle, row)
names = {f: f"Q{f[1:]}" for f in bundle["features"] if f.startswith("A")} | LABELS
contrib = contrib.rename(index=names)
shown = contrib.reindex(contrib.abs().sort_values(ascending=False).index)[:8][::-1]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(shown.index, shown.values, color=["#d9775f" if v > 0 else "#6b9ac4" for v in shown.values])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("effect on the estimate (SHAP value)")
plt.tight_layout()
st.pyplot(fig)

up = contrib[contrib > 0.01].sort_values(ascending=False).index[:3].tolist()
down = contrib[contrib < -0.01].sort_values().index[:3].tolist()
text = []
if up:
    text.append(f"The answers that **raised** the estimate most were {', '.join(up)}.")
if down:
    text.append(f"The answers that **lowered** it most were {', '.join(down)}.")
text.append(f"In total {total} of the 10 answers pointed towards autistic traits. "
            f"Red bars push the result towards 'ASD traits', blue bars push it away.")
st.markdown(" ".join(text))

with st.expander("Your scored answers"):
    st.dataframe(pd.DataFrame({"question": [t for t, _ in questions], "your answer": answers,
                               "counts towards traits": ["yes" if s else "no" for s in scored]},
                              index=[f"Q{i}" for i in range(1, 11)]))

st.info(f"Model: {bundle['model_name']}. This result is a screening aid, **not a diagnosis**. "
        "Nothing you entered has been saved.")
