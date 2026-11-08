# About this project

MSc project: *Early Autism Screening Using Interpretable Machine Learning Models and a Web Based Decision Support Tool*.

## What the project is

Autism Spectrum Disorder (ASD) affects roughly 1 in 100 people worldwide [1]. Early support helps, but a formal diagnosis needs trained specialists and several visits, and in many places there are not enough specialists, so families wait a long time [2]. Short screening questionnaires are the usual first step: the Q-CHAT-10 for toddlers and the AQ-10 for children, adolescents and adults. Each has ten yes/no style questions and takes a few minutes. A screening result is not a diagnosis; it only says who should be referred.

Answers to these questionnaires, collected through the ASDTests app, are public for all four age groups [3]–[6], and many papers have trained machine learning (ML) models on them. This project builds on that work. It compares six models for the four age groups, tests them on data from a second source, compares three ways of explaining the predictions, and delivers the chosen models through a small web tool that shows a risk estimate together with the reasons for it.

## The problem

Published models on these datasets usually report accuracy close to 100%. Those numbers should be read with care, for three reasons.

1. **The label is made from the inputs.** In the ASDTests datasets the class label is simply "questionnaire score above the cut-off" (3 for Q-CHAT-10, 6 for AQ-10). Notebook 02 checks this for every row. A model that receives the ten answers can reproduce the label exactly, and a model that also receives the total score has the answer handed to it. This is a form of data leakage, the problem Kapoor and Narayanan found in nearly 300 ML papers across 17 fields [7].
2. **Models are hard to trust.** Many of the best-scoring models are black boxes. Post-hoc tools such as SHAP and LIME can explain them from the outside, but their explanations are estimates. Rudin argues that for high-stakes decisions it is better to use models that are interpretable by design [8].
3. **One source, one split.** Most studies train and test on a single dataset, often with a single train/test split, so it is unclear how the models would behave on new data from somewhere else.

## Research questions

- **RQ1.** How do the Explainable Boosting Machine (EBM) and TabPFN compare with Logistic Regression, Random Forest, XGBoost and LightGBM in the four age groups, when leakage is controlled and when the questionnaire is incomplete or noisy?
- **RQ2.** How well do the models work when trained on one data source and tested on another?
- **RQ3.** Which questions matter most for the predictions, and do SHAP, LIME and EBM agree on them?

## Previous work and the gap

| Study | Data | Models | What they found / limitation |
|---|---|---|---|
| Akter et al., 2019 [9] | Child, adolescent, adult (AQ-10) | Several classifiers | AUC above 0.98; single source |
| Bala et al., 2022 [10] | All four age groups | Several, SVM best | SHAP used; single source, single split |
| Farooq et al., 2023 [11] | Child and adult | LR and SVM, federated | 98% (child) and 81% (adult) accuracy |
| Abu-Errub, 2025 [12] | Toddler (Q-CHAT-10) | Six classifiers with chi-square selection | Perfect scores; score column not removed |
| Mumenin et al., 2025 [2] | All four and merged | Stacked RF, Extra Trees, CatBoost + ANN | 97–99.9%; gain over simple models not significant |
| Singh et al., 2026 [13] | Child, adolescent, adult, two sources | 17 models incl. TabPFN | TabPFN best AUC but least stable under noise; single split, no external test |
| Irram and Suaib, 2025 [14] | Infant EEG | DT, RF, SVM | AUC 0.93; needs special equipment |
| **This project** | All four groups + two extra sources | LR, RF, XGBoost, LightGBM, EBM, TabPFN | Leakage-aware repeated CV, cross-source test, reduced and noisy questionnaires, SHAP vs LIME vs EBM, web tool |

The gap in short: EBM has rarely been used on this kind of data, TabPFN has only just been tried, almost nobody tests on a second source, and explanation methods are usually used one at a time rather than compared. Few papers say clearly that the label is a scoring rule, so their high numbers are presented as diagnostic accuracy when they are not.

## Why these six models

| Model | Reason for including it |
|---|---|
| Logistic Regression | The simplest interpretable baseline. The label is a weighted sum of answers over a threshold, which is exactly what LR represents. If anything beats it, that is worth knowing. |
| Random Forest | The most common model in the earlier ASD papers; needed for a fair comparison with them. |
| XGBoost, LightGBM | Strong gradient boosting models that usually win on tabular data [15], [16]; standard non-interpretable reference points. |
| Explainable Boosting Machine | Interpretable by design: a boosted generalised additive model whose per-question shape functions can be read directly [17]. Rarely used on ASD questionnaires. |
| TabPFN | A transformer pre-trained on synthetic tables that needs no tuning and is built for small datasets like these [18]. Recently benchmarked on ASD data [13] but not with leakage controls or a cross-source test. |

Deep neural networks are not included. On small tables of yes/no answers they have no advantage over tree models [15], [16], and they add tuning cost and lose interpretability.

## How each issue is handled

**Leakage.** The total score and any column derived from it are dropped. All preprocessing that learns from data (scaling, oversampling) runs inside the cross-validation pipeline, so it only ever sees the training fold. Hyperparameters are tuned with a nested inner cross-validation, never on the test fold. Because the label is a deterministic rule of the ten answers, near-perfect scores are still expected; they show that a model has recovered the rule, not that it diagnoses autism. The project says so plainly rather than presenting them as diagnostic accuracy.

**A meaningful comparison despite that.** With all ten answers every reasonable model can recover the rule, so the models are also compared under two harder settings: with only the 4, 6 or 8 most informative questions (chosen by chi-square on the training fold only) and with 5–20% of the answers flipped at random. These settings mimic incomplete and unreliable questionnaires and separate the models.

**Small, imbalanced data.** Datasets range from about 100 to 1,000 rows. Repeated stratified 5-fold cross-validation (3 repeats) gives 15 test folds per model instead of one split. Class imbalance is handled with SMOTE for mixed data types (SMOTENC) [19], applied only to the training fold.

**Fair comparison between models.** The same folds, the same features and the same pipeline are used for every model. Differences are tested with the Friedman test and Nemenyi post-hoc test across folds [20] and with the corrected resampled t-test [21], so small differences are not over-interpreted.

**Generalisation to other data.** Two further datasets from different sources (Saudi toddlers, a Kaggle adult dataset) are used only as test sets: train on one source, test on the other, and the reverse.

**Explainability.** Every prediction is explained three ways: SHAP, LIME and the EBM's own term contributions. Question rankings from the three methods are compared with Spearman correlation and top-5 overlap, so the project can say whether the explanations agree rather than trusting one tool.

**Fairness.** Model performance is broken down by sex and ethnicity to check whether any group is screened worse.

**Delivery.** The best interpretable model for each age group is saved and served through a web tool. The tool asks the questionnaire, shows a risk estimate with a per-question explanation, states that the result is a screening aid and not a diagnosis, and stores nothing.

**Reproducibility.** Everything runs from numbered notebooks with fixed random seeds and pinned package versions. Data download, cleaning, analysis, modelling and results are separate notebooks so each step can be checked on its own.

## Data

| Dataset | Questionnaire | Rows | Role |
|---|---|---|---|
| Toddlers [3] | Q-CHAT-10 | 1,054 | main |
| Children [4] | AQ-10 Child | 292 | main |
| Adolescents [5] | AQ-10 Adolescent | 104 | main |
| Adults [6] | AQ-10 Adult | 704 | main |
| Saudi toddlers [22] | Q-CHAT-10 | 506 | second source |
| Kaggle adults [23] | AQ-10 Adult | 800 | second source |

Row counts are before cleaning. Each record has the ten answers, age, sex, ethnicity, whether the person had jaundice at birth and whether a family member has autism.

## References

1. J. Zeidan et al., "Global prevalence of autism: A systematic review update," *Autism Research*, 15(5), 2022.
2. N. Mumenin et al., "Early diagnosis of autism across developmental stages through scalable and interpretable ensemble model," *Frontiers in Artificial Intelligence*, 8, 2025.
3. F. Thabtah, "Autism screening data for toddlers," Kaggle, 2018.
4. F. Thabtah, "Autistic spectrum disorder screening data for children," UCI Machine Learning Repository, 2017.
5. F. Thabtah, "Autistic spectrum disorder screening data for adolescent," UCI Machine Learning Repository, 2017.
6. F. Thabtah, "Autism screening adult," UCI Machine Learning Repository, 2017.
7. S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, 4(9), 2023.
8. C. Rudin, "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead," *Nature Machine Intelligence*, 1(5), 2019.
9. T. Akter et al., "Machine learning-based models for early stage detection of autism spectrum disorders," *IEEE Access*, 7, 2019.
10. M. Bala et al., "Efficient machine learning models for early stage detection of autism spectrum disorder," *Algorithms*, 15(5), 2022.
11. M. S. Farooq et al., "Detection of autism spectrum disorder (ASD) in children and adults using machine learning," *Scientific Reports*, 13, 2023.
12. A. Abu-Errub, "Improving early autism detection with chi-square feature selection, machine learning, and explainable AI," *Engineering, Technology & Applied Science Research*, 15(5), 2025.
13. S. Singh et al., "ASD-Bench: A four-axis comprehensive benchmark of AI models for autism spectrum disorder," arXiv:2605.11091, 2026.
14. S. Irram and M. Suaib, "An early detection of autism spectrum disorder using machine learning," *Computers in Biology and Medicine*, 198, 2025.
15. L. Grinsztajn, E. Oyallon and G. Varoquaux, "Why do tree-based models still outperform deep learning on typical tabular data?" *NeurIPS Datasets and Benchmarks*, 2022.
16. R. Shwartz-Ziv and A. Armon, "Tabular data: Deep learning is not all you need," *Information Fusion*, 81, 2022.
17. H. Nori et al., "InterpretML: A unified framework for machine learning interpretability," arXiv:1909.09223, 2019.
18. N. Hollmann et al., "Accurate predictions on small data with a tabular foundation model," *Nature*, 637, 2025.
19. N. V. Chawla et al., "SMOTE: Synthetic minority over-sampling technique," *JAIR*, 16, 2002.
20. J. Demšar, "Statistical comparisons of classifiers over multiple data sets," *JMLR*, 7, 2006.
21. C. Nadeau and Y. Bengio, "Inference for the generalization error," *Machine Learning*, 52(3), 2003.
22. "ASD screening data for toddlers in Saudi Arabia," Kaggle, 2022.
23. S. Shinde, "Autism prediction dataset," Kaggle, 2022.
