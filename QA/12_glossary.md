# 12. Short forms and terms, with examples

**ASD.** Autism Spectrum Disorder. Many people simply say autism.

**AQ-10.** Autism Spectrum Quotient, short form with 10 questions. Used for children, adolescents and adults.

**Q-CHAT-10.** Quantitative Checklist for Autism in Toddlers, short form with 10 questions. A parent answers it.

**Screening.** A quick first check. Example: a ten-question form that shows who should see a specialist.

**Cut-off.** The score where the questionnaire says "a full assessment may be useful". Example: above 6 for the AQ-10.

**Label (class).** The answer the model tries to predict. Here: ASD traits, yes or no.

**Feature (input).** A column given to the model. Example: the answer to question 3, or the age.

**ML.** Machine learning. A computer program learns a pattern from examples.

**Model.** The program after it has learned. Example: a Logistic Regression that predicts yes or no.

**Training and testing.** The model learns from the training data and is checked on the test data, which it has not seen.

**Data leakage.** The model gets information it should not have. Example: giving the total score when the label is made from that score.

**Baseline.** A simple method to compare with. Here: add the answers and apply the cut-off.

**Cross-validation (CV).** Testing in turns. Example: 5 folds, each one used once as the test part.

**Fold.** One part of the data in cross-validation.

**Stratified.** Every fold keeps the same share of positive cases.

**Hyperparameter.** A setting chosen before training. Example: the number of trees.

**Grid search.** Trying every combination of the chosen settings.

**Pipeline.** A chain of steps run in order. Example: SMOTENC, then scaling, then the model.

**SMOTE.** Synthetic Minority Over-sampling Technique. It makes extra records for the smaller class. Example: 40 "yes" records become 100.

**SMOTENC.** SMOTE for Nominal and Continuous. SMOTE for data with yes or no columns. It keeps answers as 0 or 1.

**LR.** Logistic Regression. A simple model that adds up weighted inputs.

**RF.** Random Forest. Many decision trees that vote.

**XGBoost and LightGBM.** Models that build trees one after another, each fixing earlier mistakes.

**EBM.** Explainable Boosting Machine. One readable curve for each input, added together.

**TabPFN.** Tabular Prior-data Fitted Network. A ready-trained model for small tables.

**Interpretable.** A person can see how the model reaches its answer.

**Black box.** A model too complex for a person to follow.

**Accuracy.** Share of people the model gets right. Example: 95 of 100 is 0.95.

**Recall.** Share of real positive cases that the model finds. Example: 9 of 10 is 0.9.

**Precision.** Share of the model's positive calls that are correct. Example: 8 of 10 is 0.8.

**F1-score.** One number that mixes precision and recall.

**ROC-AUC.** Area under the ROC curve. 1.0 is perfect, 0.5 is guessing.

**PR-AUC.** Area under the precision-recall curve. Useful when classes are unbalanced.

**Brier score.** How far the probabilities are from the truth. 0 is best.

**Calibration.** Whether the percentages can be trusted. Example: of people given 80%, about 80% are positive.

**ECE.** Expected Calibration Error. The average gap between the predicted percentage and the truth.

**False positive.** The model says yes, but the truth is no. A false alarm.

**False negative.** The model says no, but the truth is yes. A missed case.

**FPR.** False-positive rate. Share of negative people wrongly marked positive.

**p-value.** A small value (below 0.05) means the difference is unlikely to be only luck.

**Friedman test.** Asks if several models differ at all.

**Nemenyi test.** Asks which pairs of models differ.

**Corrected resampled t-test.** A t-test made for cross-validation results.

**Holm correction.** Makes p-values bigger when many tests are run. Example: 0.01, 0.04, 0.30 become 0.03, 0.08, 0.30.

**Effect size.** How big a difference is. Cohen's d: 0.2 small, 0.5 medium, 0.8 large.

**Kendall's W.** From 0 to 1. How much the folds agree on the ranking of the models.

**Chi-square.** A measure of how strongly an answer is related to the label.

**SHAP.** SHapley Additive exPlanations. Shares one prediction out between the inputs.

**LIME.** Local Interpretable Model-agnostic Explanations. Changes one row a little, many times, to see what moves the prediction.

**Log-odds.** The model's score before it becomes a probability. 0 means 50%.

**Spearman correlation.** How similar two rankings are. 1 means the same order.

**Top-five overlap.** How many of the top five questions two methods share. Chance level is 2.5.

**Synthetic data.** Data made by a computer, not collected from real people.

**Cross-source test.** Train on data from one source, test on data from another.

**Fairness check.** Comparing mistakes between groups, such as girls and boys.

**UCI.** University of California, Irvine. Home of a free library of datasets.

**Kaggle.** A website with public datasets and competitions.

**Streamlit.** A Python library for making simple web apps.

**UK GDPR.** UK General Data Protection Regulation. The law on personal data.

**MHRA.** Medicines and Healthcare products Regulatory Agency. It regulates medical devices in the UK.

**IEEE.** Institute of Electrical and Electronics Engineers. The paper uses its two-column format.

**RQ.** Research question.
