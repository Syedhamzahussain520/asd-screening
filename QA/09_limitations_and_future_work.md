# 9. Limitations and future work

**Q1. What is the biggest limitation?**
The labels are screening results, not clinical diagnoses. So the results measure how well a model follows a questionnaire rule. They do not measure how well it detects autism.

**Q2. What is the limitation of the adolescent data?**
Only 101 records. The results change a lot between folds, and the fairness numbers rest on very few cases.

**Q3. Do the datasets represent everyone?**
No. The data come from people who chose to use a mobile app. They may not represent the wider population.

**Q4. What is the limitation of the cross-source test?**
A second dataset was only available for toddlers and adults. The toddler one uses the same label rule. The adult one is synthetic. So neither is a fully independent test.

**Q5. What is the limitation of the harder settings?**
They were simulated. Real people may skip or misread questions in a different way from random flipping.

**Q6. What is the limitation of the statistical tests?**
Folds of one dataset are not independent. The corrected t-test allows for this, but the Friedman and Nemenyi tests do not, so they are only a description.

**Q7. What is the limitation of the explanation analysis?**
The rankings are not stable and LIME is close to chance in two groups. The reason for the EBM and SHAP ranking difference is likely the reference point, but this was not tested on its own.

**Q8. What is the limitation of the web tool?**
It is a demonstration. It has not been tested with clinicians or families and it is not a medical device.

**Q9. What is the most important future work?**
To repeat the study on data with diagnoses confirmed by clinicians. Then the models are tested against real outcomes and not against a questionnaire score.

**Q10. What other future work is suggested?**
- Larger and more varied samples, especially for adolescents.
- A fuller fairness study by sex, ethnicity and age.
- Testing shortened questionnaires with real users.
- Testing the web tool with clinicians and families.
- A test on a truly independent data source.

**Q11. What were the main challenges?**
- Understanding why every model scored 100%, and proving it was the data and not a mistake.
- Finding a real second data source. One Kaggle dataset turned out to be a copy of the main data.
- Getting TabPFN, LightGBM and XGBoost to run together.
- Keeping every step free of leakage.

**Q12. What were the main lessons?**
- Always ask how the label was made before trusting an accuracy number.
- Report a simple baseline next to any model.
- Sanity checks are cheap and make a surprising result defensible.
- Harder tests tell more than a perfect score on an easy test.
- Explanations must be checked over many splits and against chance.
