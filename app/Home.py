import streamlit as st

st.set_page_config(page_title="ASD Screening Support", layout="centered")

st.title("Early Autism Screening – Decision Support")

st.markdown("""
This tool supports **early screening** for autism spectrum disorder (ASD). You answer a
short, well-known questionnaire, and a machine learning model trained on public screening data
estimates whether the answers show **signs that a full assessment may be worthwhile**.
Every result comes with an explanation of which answers mattered most.

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

st.subheader("How to use it")
st.markdown("""
1. Open **Screening** in the sidebar.
2. Choose the age group and answer the ten questions (a parent or carer answers for toddlers, children and adolescents).
3. Read the result and the explanation.

**Model Performance** shows how the models were tested, and **About** explains the data,
the method and the limitations.
""")

st.caption("Nothing you enter is stored. The page forgets your answers as soon as you close it.")
st.caption("MSc research project (COM748) – Early Autism Screening Using Interpretable Machine Learning.")
