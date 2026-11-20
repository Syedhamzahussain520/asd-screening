import streamlit as st

st.set_page_config(page_title="ASD Screening Support", layout="centered")

# first page of the app. It only shows text, there is no model here
st.title("Early Autism Screening – Decision Support")

st.markdown("""
This tool is a **research demonstration** of early screening for autism spectrum disorder (ASD).
You answer a short, well-known questionnaire with ten questions. The tool then shows:

* your **questionnaire score** and whether it is above the standard cut-off. This is the main result.
* what a **machine learning model** says about the same answers, and which answers mattered most to it.

It covers four age groups:

| Age group | Questionnaire |
|---|---|
| Toddler (12–36 months) | Q-CHAT-10 |
| Child (4–11 years) | AQ-10 Child |
| Adolescent (12–16 years) | AQ-10 Adolescent |
| Adult (18+ years) | AQ-10 Adult |
""")

st.warning(
    "**This is not a diagnosis.** Only a qualified clinician can diagnose autism. "
    "If you have concerns, please speak to your GP, health visitor or another health professional, "
    "whatever result this tool gives."
)

with st.expander("What the words mean"):
    st.markdown("""
* **ASD** – autism spectrum disorder. Many people simply say autism.
* **Screening** – a quick first check. It shows who may need a full assessment. It does not say who has autism.
* **Q-CHAT-10** – Quantitative Checklist for Autism in Toddlers. Ten questions that a parent answers.
* **AQ-10** – Autism Spectrum Quotient, short form with ten questions. There is one version for children,
  one for adolescents and one for adults.
* **Score** – every answer that points towards autistic traits counts as 1 point. Ten questions, so the
  score is between 0 and 10. Example: 7 such answers give a score of 7.
* **Cut-off** – the score where the questionnaire says "a full assessment may be useful". For toddlers
  this is a score above 3. For the other groups it is a score above 6.
* **Model** – a computer program that has learned from past screening records.
* **Explanation** – a chart that shows which of your answers moved the model's number up or down.
""")

st.subheader("How to use it")
st.markdown("""
1. Open **Screening** in the sidebar.
2. Choose the age group and answer the ten questions (a parent or carer answers for toddlers, children and adolescents).
3. Read the score first, then the model's number and the explanation.

**Model Performance** shows how well the models did in testing. **About** explains the data,
the method and the limits of this tool.
""")

st.caption("Nothing you enter is stored. The page forgets your answers as soon as you close it.")
st.caption("MSc research project (COM748) – Early Autism Screening Using Interpretable Machine Learning.")
