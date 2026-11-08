# About this project

MSc project: *Early Autism Screening Using Interpretable Machine Learning Models and a Web Based Decision Support Tool*.

## What the project is

Autism Spectrum Disorder (ASD) affects roughly 1 in 100 people worldwide. Early support helps, but a formal diagnosis needs trained specialists and several visits, and in many places there are not enough specialists, so families wait a long time. Short screening questionnaires are the usual first step: the Q-CHAT-10 for toddlers and the AQ-10 for children, adolescents and adults. Each has ten yes/no style questions and takes a few minutes. A screening result is not a diagnosis; it only says who should be referred.

Answers to these questionnaires, collected through the ASDTests app, are public for all four age groups, and many papers have trained machine learning (ML) models on them. This project builds on that work. It compares six models for the four age groups, tests them on data from a second source, compares three ways of explaining the predictions, and delivers the chosen models through a small web tool that shows a risk estimate together with the reasons for it.

## The problem

Published models on these datasets usually report accuracy close to 100%. Those numbers should be read with care, for three reasons.

1. **The label is made from the inputs.** In the ASDTests datasets the class label is simply "questionnaire score above the cut-off" (3 for Q-CHAT-10, 6 for AQ-10). Notebook 02 checks this for every row. A model that receives the ten answers can reproduce the label exactly, and a model that also receives the total score has the answer handed to it. This is a form of data leakage, the problem Kapoor and Narayanan found in nearly 300 ML papers across 17 fields.
2. **Models are hard to trust.** Many of the best-scoring models are black boxes. Post-hoc tools such as SHAP and LIME can explain them from the outside, but their explanations are estimates. Rudin argues that for high-stakes decisions it is better to use models that are interpretable by design.
3. **One source, one split.** Most studies train and test on a single dataset, often with a single train/test split, so it is unclear how the models would behave on new data from somewhere else.

## Research questions

- **RQ1.** How do the Explainable Boosting Machine (EBM) and TabPFN compare with Logistic Regression, Random Forest, XGBoost and LightGBM in the four age groups, when leakage is controlled and when the questionnaire is incomplete or noisy?
- **RQ2.** How well do the models work when trained on one data source and tested on another?
- **RQ3.** Which questions matter most for the predictions, and do SHAP, LIME and EBM agree on them?

## Previous work and the gap

| Study | Data | Models | What they found / limitation |
|---|---|---|---|
| Akter et al., 2019 | Child, adolescent, adult (AQ-10) | Several classifiers | AUC above 0.98; single source |
| Bala et al., 2022 | All four age groups | Several, SVM best | SHAP used; single source, single split |
| Farooq et al., 2023 | Child and adult | LR and SVM, federated | 98% (child) and 81% (adult) accuracy |
| Abu-Errub, 2025 | Toddler (Q-CHAT-10) | Six classifiers with chi-square selection | Perfect scores; score column not removed |
| Mumenin et al., 2025 | All four and merged | Stacked RF, Extra Trees, CatBoost + ANN | 97–99.9%; gain over simple models not significant |
| Singh et al., 2026 | Child, adolescent, adult, two sources | 17 models incl. TabPFN | TabPFN best AUC but least stable under noise; single split, no external test |
| Irram and Suaib, 2025 | Infant EEG | DT, RF, SVM | AUC 0.93; needs special equipment |
| **This project** | All four groups + two extra sources | LR, RF, XGBoost, LightGBM, EBM, TabPFN | Leakage-aware repeated CV, cross-source test, reduced and noisy questionnaires, SHAP vs LIME vs EBM, web tool |

The gap in short: EBM has rarely been used on this kind of data, TabPFN has only just been tried, almost nobody tests on a second source, and explanation methods are usually used one at a time rather than compared. Few papers say clearly that the label is a scoring rule, so their high numbers are presented as diagnostic accuracy when they are not.

## Why these six models

| Model | Reason for including it |
|---|---|
| Logistic Regression | The simplest interpretable baseline. The label is a weighted sum of answers over a threshold, which is exactly what LR represents. If anything beats it, that is worth knowing. |
| Random Forest | The most common model in the earlier ASD papers; needed for a fair comparison with them. |
| XGBoost, LightGBM | Strong gradient boosting models that usually win on tabular data; standard non-interpretable reference points. |
| Explainable Boosting Machine | Interpretable by design: a boosted generalised additive model whose per-question shape functions can be read directly. Rarely used on ASD questionnaires. |
| TabPFN | A transformer pre-trained on synthetic tables that needs no tuning and is built for small datasets like these. Recently benchmarked on ASD data but not with leakage controls or a cross-source test. |

Deep neural networks are not included. On small tables of yes/no answers they have no advantage over tree models, and they add tuning cost and lose interpretability.

## How each issue is handled

**Leakage.** The total score and any column derived from it are dropped. All preprocessing that learns from data (scaling, oversampling) runs inside the cross-validation pipeline, so it only ever sees the training fold. Hyperparameters are tuned with a nested inner cross-validation, never on the test fold. Because the label is a deterministic rule of the ten answers, near-perfect scores are still expected; they show that a model has recovered the rule, not that it diagnoses autism. The project says so plainly rather than presenting them as diagnostic accuracy.

**A meaningful comparison despite that.** With all ten answers every reasonable model can recover the rule, so the models are also compared under two harder settings: with only the 4, 6 or 8 most informative questions (chosen by chi-square on the training fold only) and with 5–20% of the answers flipped at random. These settings mimic incomplete and unreliable questionnaires and separate the models.

**Small, imbalanced data.** The datasets are small. Repeated stratified 5-fold cross-validation (3 repeats) gives 15 test folds per model instead of one split. Class imbalance is handled with SMOTE for mixed data types (SMOTENC), applied only to the training fold.

**Fair comparison between models.** The same folds, the same features and the same pipeline are used for every model. Differences are tested with the Friedman test and Nemenyi post-hoc test across folds and with the corrected resampled t-test, so small differences are not over-interpreted.

**Generalisation to other data.** Two further datasets from different sources (Saudi toddlers, a Kaggle adult dataset) are used only as test sets: train on one source, test on the other, and the reverse.

**Explainability.** Every prediction is explained three ways: SHAP, LIME and the EBM's own term contributions. Question rankings from the three methods are compared with Spearman correlation and top-5 overlap, so the project can say whether the explanations agree rather than trusting one tool.

**Fairness.** Model performance is broken down by sex and ethnicity to check whether any group is screened worse.

**Delivery.** The best interpretable model for each age group is saved and served through a web tool. The tool asks the questionnaire, shows a risk estimate with a per-question explanation, states that the result is a screening aid and not a diagnosis, and stores nothing.

**Reproducibility.** Everything runs from numbered notebooks with fixed random seeds and pinned package versions. Data download, cleaning, analysis, modelling and results are separate notebooks so each step can be checked on its own.

## Data

| Dataset | Questionnaire | Role |
|---|---|---|
| Toddlers (Thabtah, Kaggle) | Q-CHAT-10 | main |
| Children (Thabtah, UCI) | AQ-10 Child | main |
| Adolescents (Thabtah, UCI) | AQ-10 Adolescent | main |
| Adults (Thabtah, UCI) | AQ-10 Adult | main |
| Saudi toddlers (Kaggle) | Q-CHAT-10 | second source |
| Kaggle adults | AQ-10 Adult | second source |

Each record has the ten answers, age, sex, ethnicity, whether the person had jaundice at birth and whether a family member has autism.
