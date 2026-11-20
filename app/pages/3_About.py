import streamlit as st

st.set_page_config(page_title="About", layout="centered")

# this page is text only
st.title("About this tool")

st.header("Purpose")
st.markdown("""
A formal autism diagnosis needs long assessments by specialists, and waiting lists are long.
Short screening questionnaires help decide who should be referred. This tool combines such a
questionnaire with a machine learning model that can be explained, and shows **why** the model gave its answer.

This tool is a **research demonstration**. The questionnaire score is the main result. The model is shown
next to it to demonstrate how its reasoning can be made visible.
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
and TabPFN were compared in the same way for each age group. Care was taken that no information from the
test data reached the models during training (this problem is called *leakage*). With the full questionnaire
a model can simply learn the scoring rule, so the models were also tested with only 4, 6 or 8 of the questions
and with 5–20% of the answers changed at random. The **Model Performance** page shows both. The explanations
use SHAP values, which show how much each answer moved the model's number up or down for this person.
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

st.header("Privacy and responsible use")
st.markdown("""
* Your answers are only used to make the result on the screen. They are never stored or logged.
* The tool does not ask for a name or anything else that could identify a person.
* This is a student research project. It is **not a medical device** and has not been approved for clinical use.
* It must not be used to decide about a diagnosis, treatment or support. Only a qualified clinician can do that.
* The training data is public and anonymous. It was collected by other researchers.
""")

st.header("References")
st.markdown("""
1. C. Allison, B. Auyeung and S. Baron-Cohen, "Toward brief 'red flags' for autism screening: the short Autism Spectrum Quotient and the short Quantitative Checklist in 1,000 cases and 3,000 controls," *J. Am. Acad. Child Adolesc. Psychiatry*, 51(2), 2012.
2. F. Thabtah, "Autism spectrum disorder screening: machine learning adaptation and DSM-5 fulfillment," *Proc. ICMHI*, 2017.
3. H. Nori et al., "InterpretML: A unified framework for machine learning interpretability," arXiv:1909.09223, 2019.
4. N. Hollmann et al., "Accurate predictions on small data with a tabular foundation model," *Nature*, 637, 2025.
5. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," *NeurIPS*, 2017.
""")
