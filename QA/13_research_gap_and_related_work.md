# 13. Related work and research gap

**Q1. What did earlier studies do?**
Most of them trained machine learning models on the same public ASDTests datasets and reported very high accuracy.

**Q2. Can you give examples of earlier studies?**
- Akter et al. (2019): several models on the four datasets, AUC above 0.98.
- Bala et al. (2022): all four age groups, Support Vector Machine best, used SHAP.
- Erkan and Thanh (2019): 100% accuracy with Random Forest on three datasets.
- Hossain et al. (2021): 100% accuracy with a multilayer perceptron on all four.
- Farooq et al. (2023): federated learning, 98% for children and 81% for adults.
- Abu-Errub (2025): chi-square feature selection, perfect scores on toddler data.
- Mumenin et al. (2025): a stacked model, 97% to 99.9%, but not significantly better than simple models.
- Singh et al. (2026): 17 models including TabPFN, one train and test split.

**Q3. What do these studies agree on?**
That many kinds of models reach very high accuracy on this data.

**Q4. What is a "research gap"?**
Something that earlier work has not done or not answered. A project should fill a gap.
Example: many papers report 100% accuracy, but none of them explains what that 100% means. That is a gap.

**Q5. What are the weak points of the earlier studies?**
1. The label: it comes from the questionnaire score, not from a clinician. Two studies (Bala, Hossain) removed the total score from the inputs, but the ten answers still fix the label.
2. Leakage: other leakage risks are seldom discussed. One study made extra records before splitting the data.
3. Testing: none of the studies in the table reports a test on data from a different source, and several use a single split.
4. Explanations: usually one tool (SHAP) is used and it is not checked against a second tool.

**Q6. So what exactly is the gap?**
The gap is not a lack of accurate models. It is a lack of evidence about what the reported accuracy means.

**Q7. How does this project fill the gap?**
- It reports a scoring-rule baseline and sanity checks.
- It controls leakage in every step.
- It adds harder settings and a cross-source test.
- It checks three explanation methods against the level expected by chance.

**Q8. What does Table I in the paper show?**
For each earlier study: the data used, how the models were validated, what leakage control was reported, and whether an external test was done. The last row shows this study for comparison.

**Q9. What does "external test" (external validation) mean?**
Testing a model on data that comes from a different place than the training data.
Example: train on UK data, test on data collected in another country.

**Q10. What is a "single split" and why is it weak?**
The data is cut once, for example 80% for training and 20% for testing. The result depends on which records happen to land in the test part. Cross-validation repeats this many times and is more reliable.

**Q11. Why is leakage a known problem in machine learning research?**
Kapoor and Narayanan (2023) found leakage problems in 294 papers across 17 fields. So it is a common mistake, not a rare one.

**Q12. Why were questionnaire data chosen and not brain scans or eye tracking?**
Questionnaires are cheap and can be filled in at home. Other methods need special equipment and trained staff.

**Q13. How were the facts in Table I checked?**
Each paper was read where the full text was available. One paper (Erkan and Thanh) is behind a paywall, so its row says "Full text not available".
