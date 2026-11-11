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

All abbreviations and methods named in this table are defined in the [Glossary](#glossary) at the end of this file.

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

## Methodology, step by step

The work is split into numbered notebooks. Each step reads what the previous one saved, so any step can be checked on its own.

### Step 1. Downloading the data (notebook 01)

- The four main datasets are fetched directly: children, adolescents and adults from the UCI Machine Learning Repository as zip files, toddlers from Kaggle through the Kaggle API.
- Two second-source datasets, Saudi toddlers and the Kaggle adult dataset, are fetched the same way. They are used only to test the models on data from somewhere else.
- Every file is stored under `data/raw/<dataset>/` together with the description document written by the dataset authors. These documents were used to understand the columns in the next step.
- The Kaggle adult data comes from a competition and has a test file without labels, so only its training file is used.

### Step 2. Understanding the data (notebook 02)

- The UCI files are in ARFF format. The standard reader fails on them because of quoted values with trailing spaces, so the part after the `@data` line is read as plain CSV, with `?` treated as missing.
- The two questionnaires are written out item by item (Q-CHAT-10 for toddlers, AQ-10 for the other groups) with their scoring: for Q-CHAT-10, items A1–A9 score 1 for the two "less typical" answers and A10 for the two "more typical" ones; for AQ-10 the scoring direction differs per item. In the files the answers are already scored as 0/1.
- Every column is listed with a decision on whether it can be a model input. The score column is the sum of the ten answers; country, relation, whether the app was used before and the age band are not about the person or are constant; ethnicity is kept aside for the bias check only.
- Missing values are counted. They occur only in age, ethnicity and relation, so only age matters for modelling.
- The class label is checked against the scoring rule for every row of every dataset. In the five ASDTests and Saudi datasets the label equals "score above the cut-off" without a single exception. The Kaggle adult data agrees with the rule in about four rows out of five, so it is the only dataset where the label is not a pure function of the answers.
- Conclusion recorded for the later steps: the score column must be dropped, near-perfect accuracy is expected even then, and the label is a screening result rather than a diagnosis.

### Step 3. Preprocessing (notebook 03)

What was cleaned, and why:

- **One schema for all six files.** The toddler files use their own column names and the others follow the UCI layout, with some names misspelt in the original (`jundice`, `austim`, `contry_of_res`). Everything is renamed to A1–A10, `age`, `male`, `jaundice`, `family_asd`, `ethnicity`, `score`, `asd`. Yes/no fields become 0/1 and gender becomes `male` (1 = male). The Saudi data has no jaundice or ethnicity columns, so those are left empty.
- **Exact duplicates removed.** After dropping the ID column some records are exact copies. With a few hundred rows, a copied record landing in both a training and a test fold inflates the results, so duplicates are dropped.
- **Age.** A few ages are missing, the adult file contains an age of 383, and the Kaggle adult file, though labelled "18 and more", contains ages from 2 to 89. Each dataset is restricted to the age range of its questionnaire: 12–36 months for toddlers, 4–11 years for children, 12–16 for adolescents, 17 and over for adults. Rows outside the range or with no age are dropped.
- **Ethnicity tidied.** Spellings are made consistent (`White-European` and `White European`, `others` and `Others`), and missing values become `Unknown`. Ethnicity is never a model input; it is kept only to check later whether the models make more mistakes for some groups.
- **Model inputs fixed.** The ten answers plus age, sex, jaundice and family history are the features. The score column is dropped because the label is computed from it. Country, relation, app use and age band are dropped. All inputs except age are already 0/1, so no one-hot encoding is needed.
- **Nothing that learns from the data is done here.** Scaling and oversampling are left to the model pipeline, so they are fitted on training folds only.
- Six cleaned CSV files are saved to `data/processed/`, one per dataset, with a before/after row count and the class balance of each.

### Step 4. Exploratory data analysis (notebook 04)

All figures are made at the width of a two-column paper (3.5 in for one column) and saved as PNG in `results/figures/`.

- **Class balance** per age group. The groups are imbalanced in different directions: most toddlers screened positive, most adults did not, children are close to even. The adolescent set is the smallest, so its results will vary the most. This is why oversampling is applied inside the training folds later.
- **Age distribution** by class for each group, to see whether age separates the classes. It does not in any obvious way.
- **Questionnaire score** by class, with the app's cut-off drawn in. The two classes never overlap: everything above the line is "ASD traits". This is the leakage finding of step 2 shown as a picture.
- **Answer rates**: the share of people scoring 1 on each question, by group and class. Some questions separate the classes strongly (for adults A6 and A9), others are scored 1 by both classes (A1 and A8 in adults, A10 in toddlers). These differences are what the explanation methods pick up later.
- **Chi-square test** of every input against the label. With these sample sizes nearly every question is highly significant, so the chi-square statistic is used to rank questions rather than the p-value. The same test, run on the training fold only, is used later to choose the reduced question sets.
- **Correlation between questions** (phi coefficient for 0/1 data) for each group, to see whether answers cluster.
- **Personal details**: share of positive screens by sex, jaundice and family history. In adults, family history and jaundice go with a positive screen; in toddlers boys screen positive a little more often; for children and adolescents there is no clear link.

### Step 5. Model training (notebook 05)

- **Six models, one pipeline.** Logistic Regression, Random Forest, XGBoost, LightGBM, EBM and TabPFN are each wrapped in the same pipeline: SMOTENC oversampling, a scaler for Logistic Regression only, then the classifier. The pipeline is fitted on the training fold only, so neither the synthetic rows nor the scaling ever see test data. The score column is not among the inputs.
- **Repeated stratified cross-validation.** Each age group is split into 5 stratified folds, and the whole split is repeated 3 times with different shuffles, giving 15 test folds per model. Every model is scored on exactly the same folds.
- **Nested tuning.** Inside each training fold a further 3-fold grid search picks the hyperparameters by ROC-AUC. The grids are small on purpose: regularisation strength for Logistic Regression, number and depth of trees for the tree models, whether EBM may use pairwise terms. TabPFN has nothing to tune and uses its defaults.
- **What is recorded.** Accuracy, precision, recall, F1, ROC-AUC, the Brier score and the confusion-matrix counts per fold, plus the out-of-fold predicted probability of every record, which the fairness check uses later.
- **Cross-source test.** Each model is trained on the whole of one source and tested on the whole of the other, in both directions, for the two pairs where a second source exists (Thabtah and Saudi toddlers, UCI and Kaggle adults). Jaundice is left out because the Saudi data does not record it.
- **Choosing the deployed model.** Per age group, the model with the highest mean ROC-AUC is chosen, with recall and then interpretability breaking ties. TabPFN is excluded from deployment because it needs PyTorch and a large weights file. The chosen model is retrained on all data of its group and saved together with a small background sample for the explanations.

### Step 6. Results (notebook 06)

- **Result tables.** Mean and standard deviation of accuracy, precision, recall, F1, ROC-AUC and Brier score over the 15 folds for every model and group.
- **Baseline.** The scoring rule itself (add up the answers, apply the cut-off) is evaluated with no learning. It is right every time because it is the label, which sets the frame for reading the model scores: they measure how well a model recovers a known rule from a few hundred examples.
- **Sanity checks.** Two controls confirm that the perfect scores come from the data and not from a leak. Shuffling the labels drops a Logistic Regression to chance level, and a hold-out split made on the raw downloaded files before any cleaning gives the same result as the cleaned pipeline.
- **Statistical tests.** The Friedman test asks whether the six models differ at all within a group, the Nemenyi test which pairs differ, and the corrected resampled t-test compares EBM and TabPFN with every other model while allowing for the overlap between repeated folds.
- **Missed cases.** False negatives are counted per model and group, because a missed case is the costliest error in screening.
- **Cross-source results.** The cross-source scores are set beside the in-source cross-validated score of the same model, so the drop when the source changes can be read directly.
- **Bias check.** Recall and false-positive rate of the chosen model per group are compared between sexes and across ethnic groups, using the out-of-fold predictions so no record is scored by a model that saw it in training.

### Step 7. Explainability (notebook 07)

- **One model, three explanations.** A purely additive EBM is trained on 80% of each age group and its predictions on the other 20% are explained three ways: the EBM's own term importances (exact, read from the model), SHAP values (permutation form, model-agnostic) and LIME weights averaged over the test set.
- **Comparing the methods.** Each method's importances are scaled to sum to one and compared per group. Agreement is measured on the ten questions only, with Spearman rank correlation and the overlap of the two top-5 sets. The personal details are excluded from the agreement measure because every method ranks them near zero.
- **Reading the result.** Because the true rule weights all ten answers equally, the rankings describe where in this sample the answers vary near the cut-off, not which question is clinically most important. They are presented as support for explaining an individual prediction, not as a finding about autism.

### Step 8. Harder settings (notebook 08)

- **Why.** With all ten answers the scoring rule can be recovered exactly, so the full-questionnaire scores say little about how the models compare. Two settings with a practical meaning make the task harder.
- **Reduced questionnaire.** In each training fold the 4, 6 or 8 questions with the largest chi-square statistic against the label are chosen (on the training fold only), the model is trained on those plus the personal details, and it must predict the full-questionnaire outcome on the test fold. This asks how much a shorter screen loses.
- **Noisy answers.** Models trained on clean data are tested after 5%, 10% or 20% of the test answers have been flipped at random, as would happen with careless or inconsistent answering.
- **Set-up.** Six models, stratified 5-fold cross-validation repeated twice, fixed hyperparameters taken from the tuning in step 5, SMOTENC inside the pipeline as before. ROC-AUC, recall, accuracy and Brier score are recorded per fold.

### Step 9. Web tool (app/)

- **What it does.** A Streamlit app with three pages. The screening page asks the ten questions of the right questionnaire for the chosen age group, plus age, sex, jaundice at birth and family history, scores the answers exactly as the datasets do, and shows the model's probability of ASD traits next to the questionnaire score.
- **Explanation with every result.** SHAP values are computed for the single submitted record against the background sample saved with the model, and shown as a bar chart of the eight answers that moved the estimate most, with a sentence naming the answers that raised and lowered it.
- **Which model.** The model chosen in step 5 for each age group, loaded from the saved bundle. TabPFN is not deployed.
- **Safeguards.** The result is labelled a screening aid and not a diagnosis on every page, the user is pointed to a health professional whatever the result, and nothing entered is stored or logged.
- **Transparency.** The performance page shows the same cross-validation, cross-source and harder-setting results as the notebooks, so a user can see how the models were tested.

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

## Glossary

Terms and abbreviations used above, each with a short meaning and an example from this project.

### Conditions and questionnaires

| Term | Meaning | Example here |
|---|---|---|
| ASD | Autism Spectrum Disorder. A lifelong developmental condition affecting communication, social interaction and behaviour. | The label in every dataset is "ASD traits: yes/no". |
| Screening vs diagnosis | Screening is a quick test to decide who should be referred for a full assessment. Diagnosis is the full assessment by a specialist. | The questionnaires and this tool only screen; they never diagnose. |
| Q-CHAT-10 | Quantitative Checklist for Autism in Toddlers, 10-item version. A parent answers ten questions about a child aged 18–36 months. Score above 3 = positive screen. | Used for the toddler and Saudi toddler datasets. |
| AQ-10 | Autism Spectrum Quotient, 10-item version. Ten questions with child, adolescent and adult wordings. Score above 6 = positive screen. | Used for the child, adolescent, adult and Kaggle adult datasets. |
| Cut-off | The score above which a screen counts as positive. | 3 for Q-CHAT-10, 6 for AQ-10. |
| EEG | Electroencephalography, recording the brain's electrical activity through the scalp. | One earlier study screened infants with EEG instead of a questionnaire. |

### Data and evaluation

| Term | Meaning | Example here |
|---|---|---|
| ML | Machine learning: a program that learns a rule from examples instead of being given the rule. | A model learns from past questionnaires which answer patterns go with a positive screen. |
| Feature / input | One piece of information the model is given for each person. | The ten answers, age, sex, jaundice at birth, family history. |
| Label / class | The answer the model is trying to predict. | ASD traits = 1 or 0. |
| Data leakage | Information about the label reaching the model in a way that would not exist in real use, which inflates the measured performance. | Giving the model the total score, from which the label is computed, is leakage. So is fitting SMOTE or a scaler on the whole dataset before splitting it. |
| Leakage-aware | Designed so that leakage cannot happen. | Score column dropped; scaling, oversampling and tuning all done inside the training fold only. |
| Train/test split | Dividing the data into a part the model learns from and a part it is scored on. | 80% of the rows for training, 20% for testing. |
| Cross-validation (CV) | Splitting the data into *k* folds, training on *k*−1 and testing on the remaining one, *k* times, so every row is tested once. | 5-fold CV gives five test scores instead of one. |
| Stratified | Each fold keeps the same proportion of positive and negative labels as the whole dataset. | A 27%-positive adult dataset gives folds that are each about 27% positive. |
| Repeated CV | Running the whole cross-validation several times with a different random shuffle, to reduce the luck of one particular split. | 5 folds × 3 repeats = 15 test scores per model. |
| Nested CV | A second, inner cross-validation run inside each training fold to choose hyperparameters, so the outer test fold is never used for tuning. | Inner 3-fold CV picks the tree depth; the outer fold then scores that choice. |
| Hyperparameter | A setting of a model chosen before training rather than learned from the data. | Number of trees in a Random Forest, learning rate in XGBoost. |
| Class imbalance | One label is much more common than the other, which can make a model ignore the rare one. | Adults are mostly negative, toddlers mostly positive. |
| SMOTE / SMOTENC | Synthetic Minority Over-sampling Technique: creates new synthetic rows of the rare class by interpolating between existing ones. SMOTENC is the version that handles a mix of numeric and categorical columns. | Applied only to the training fold, so the test fold stays real data. |
| Scaling | Rescaling numeric inputs to a common range so no single input dominates. | Age in months (12–36) is scaled before Logistic Regression; the 0/1 answers do not need it. |
| Cross-source test | Training on data from one source and testing on data collected elsewhere, to see whether the model works outside the data it was built on. | Train on Thabtah toddlers, test on Saudi toddlers, and the other way round. |
| Reduced questionnaire | The model sees only some of the ten questions and must still predict the full-questionnaire result. Mimics an incomplete form. | Only the 4, 6 or 8 most informative questions, chosen on the training fold. |
| Noisy answers | A share of the answers is flipped at random before the model sees them. Mimics unreliable responses. | 5%, 10% or 20% of answers flipped. |
| Chi-square test | A statistical test of whether two categorical variables are related. A larger statistic means a stronger relation. | Used to rank each question by how strongly it relates to the label, and to pick the reduced question sets. |
| Phi coefficient | Correlation between two 0/1 variables, from −1 to +1. | Used to see whether answers to different questions tend to agree. |

### Performance measures

| Term | Meaning | Example here |
|---|---|---|
| Accuracy | Share of all predictions that are correct. Misleading when classes are imbalanced. | Predicting "negative" for every adult would already be about 73% accurate. |
| Recall (sensitivity) | Share of true positives the model finds. The most important measure for screening, because a missed case is costly. | Of 100 people with a positive screen, how many does the model flag. |
| Precision | Share of the model's positive predictions that are correct. | Of 100 people the model flags, how many really screened positive. |
| F1 | Harmonic mean of precision and recall; one number that balances the two. | Reported alongside recall. |
| ROC-AUC | Area under the Receiver Operating Characteristic curve: the probability that a random positive gets a higher risk score than a random negative. 0.5 = guessing, 1.0 = perfect ranking. | The main measure for comparing models. |
| Brier score | Mean squared difference between the predicted probability and the true label (0 or 1). Lower is better; measures how well calibrated the probabilities are. | A model saying 0.9 for a positive case scores (1−0.9)² = 0.01 on that row. |
| Friedman test | A statistical test of whether several models differ in performance across many folds or datasets. | Tells whether the six models differ at all. |
| Nemenyi test | A follow-up to the Friedman test that says *which* pairs of models differ. | Tells whether, say, EBM and LightGBM differ. |
| Corrected resampled t-test | A t-test for comparing two models over repeated CV folds, corrected for the fact that folds overlap and are not independent. | Used for pairwise comparisons such as EBM vs Logistic Regression. |
| Fairness check | Measuring performance separately for subgroups to see whether any group is served worse. | Recall for males vs females, and per ethnicity. |
| Sanity check | A deliberately simple experiment whose outcome is known, run to confirm the pipeline is not broken. | Shuffling the labels should drop ROC-AUC to about 0.5; if it does not, something is leaking. |

### Models

| Term | Meaning | Example here |
|---|---|---|
| Logistic Regression (LR) | A linear model: each input gets a weight, the weighted sum is turned into a probability. Fully interpretable. | Ten roughly equal weights and a threshold reproduce the questionnaire rule. |
| Decision tree (DT) | A flow chart of yes/no questions on the inputs ending in a prediction. | "Is A6 = 1? If yes, is A9 = 1? ..." |
| Random Forest (RF) | Many decision trees trained on random subsets of rows and inputs; their votes are averaged. | The most common model in earlier ASD papers. |
| Gradient boosting | Trees built one after another, each correcting the errors of the previous ones. | XGBoost and LightGBM are two fast implementations; EBM is also a form of it. |
| XGBoost, LightGBM | Two widely used gradient boosting libraries, usually among the strongest models on tabular data. | Non-interpretable reference points. |
| EBM | Explainable Boosting Machine: a generalised additive model trained by boosting. Each input gets its own curve showing how it changes the prediction, and the prediction is the sum of those curves. Interpretable by design. | One can read off exactly how much "A6 = 1" adds to an adult's risk. |
| TabPFN | Tabular Prior-data Fitted Network: a transformer pre-trained on millions of synthetic tables. It makes predictions on a new small table in one pass, without training or tuning. | Compared but not deployed in the web tool, as it needs PyTorch and large weights. |
| SVM | Support Vector Machine: finds the boundary that separates the classes with the widest margin. | Reported as best in several earlier papers; not used here because it is not interpretable and the boosting models cover the same ground. |
| ANN | Artificial neural network, layers of weighted sums with non-linear activations. | One earlier paper stacked tree models under a small ANN. |
| Extra Trees, CatBoost | Variants of random forest and gradient boosting used in one earlier paper. | Included in the previous-work table only. |
| Federated learning | Training one model across several organisations without moving their data. | Used in one earlier paper on child and adult data. |

### Explanations

| Term | Meaning | Example here |
|---|---|---|
| Interpretable model | A model whose reasoning can be read directly from its parameters. | LR and EBM. |
| Black box | A model whose reasoning cannot be read directly. | Random Forest, XGBoost, LightGBM, TabPFN. |
| Post-hoc explanation | An explanation produced after training by a separate tool that probes the model from the outside. | SHAP and LIME. |
| SHAP | SHapley Additive exPlanations. Gives each input a share of a single prediction, based on game theory, so that the shares add up to the difference from the average prediction. | "A6 = 1 pushed this adult's risk up by 0.21, age pushed it down by 0.02." |
| LIME | Local Interpretable Model-agnostic Explanations. Fits a small linear model around one prediction by slightly changing the inputs, and reports that linear model's weights. | Same case, explained by a locally fitted straight line. |
| EBM term contributions | The EBM's own explanation: the value of each input's curve for this person, read directly from the model. | No approximation needed; this is what the model actually added up. |
| Global vs local explanation | Global: which inputs matter most across the whole dataset. Local: why this one prediction was made. | Global ranking of A1–A10 per group; local explanation shown in the web tool. |
| Spearman correlation | Correlation between two rankings, from −1 to +1. | Used to compare the question rankings from SHAP, LIME and EBM. |
| Top-5 overlap | How many of the five highest-ranked items two methods have in common. | SHAP and EBM agreeing on 4 of their top-5 questions. |
