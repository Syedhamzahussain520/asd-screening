import streamlit as st

st.set_page_config(page_title="About", layout="centered")

st.title("About this tool")

st.header("Purpose")
st.markdown("""
A formal autism diagnosis needs long assessments by specialists, and waiting lists are long.
Short screening questionnaires help decide who should be referred. This tool combines such a
questionnaire with an interpretable machine learning model and shows **why** it gave its answer.
""")

st.header("Data")
st.markdown("""
The models were trained on public, anonymised screening datasets collected through the
ASDTests app by F. Thabtah:

* Toddlers – Q-CHAT-10, 1,054 records (Kaggle)
* Children – AQ-10 Child, 292 records (UCI Machine Learning Repository)
* Adolescents – AQ-10 Adolescent, 104 records (UCI)
* Adults – AQ-10 Adult, 704 records (UCI)

Two further datasets (Saudi toddlers, Kaggle adults) were used only to test whether the
models work on data from a different source.
""")

st.header("Method")
st.markdown("""
Logistic Regression, Random Forest, XGBoost, LightGBM, the Explainable Boosting Machine (EBM)
and TabPFN were compared using the same leakage-aware pipeline for each age group. Because the
full questionnaire lets a model recover the scoring rule exactly, the models were also tested with
only 4, 6 or 8 of the questions and with 5–20% of answers flipped at random; the **Model Performance**
page shows both. Explanations use SHAP values, which show how much each answer moved the estimate
up or down for this person.
""")

st.header("Limitations")
st.markdown("""
* **The labels are screening results, not diagnoses.** In these datasets a person was labelled
  "ASD traits" when their questionnaire score was above the standard cut-off. The model has
  therefore learned to reproduce the questionnaire's scoring, not to diagnose autism.
* The datasets are small and were collected through an app and online forms, so they may not
  represent every population.
* Questionnaires can miss autism, especially in girls and in people who mask their traits.
* A low result does not rule autism out. A high result does not confirm it.
""")

st.header("Privacy")
st.markdown("Answers are processed in memory to produce the result and are never stored or logged.")

st.header("References")
st.markdown("""
1. C. Allison, B. Auyeung and S. Baron-Cohen, "Toward brief 'red flags' for autism screening: the short Autism Spectrum Quotient and the short Quantitative Checklist in 1,000 cases and 3,000 controls," *J. Am. Acad. Child Adolesc. Psychiatry*, 51(2), 2012.
2. F. Thabtah, "Autism spectrum disorder screening: machine learning adaptation and DSM-5 fulfillment," *Proc. ICMHI*, 2017.
3. H. Nori et al., "InterpretML: A unified framework for machine learning interpretability," arXiv:1909.09223, 2019.
4. N. Hollmann et al., "Accurate predictions on small data with a tabular foundation model," *Nature*, 637, 2025.
5. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," *NeurIPS*, 2017.
""")
