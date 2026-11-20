# 5. Results

**Q1. What happened on the full questionnaire?**
Logistic Regression, EBM and TabPFN reached a ROC-AUC of 1.000 for toddlers, children and adults. EBM made no errors at all in these three groups (2,919, 840 and 2,073 test cases).

**Q2. How did the tree models do?**
Random Forest, XGBoost and LightGBM were a little behind, with ROC-AUC between 0.964 and 0.999. They missed about 1% to 7% of the positive cases.

**Q3. Why are the tree models worse?**
The label is a sum of ten answers. A tree asks about one answer at a time, so it can only come close to a sum. Logistic Regression and EBM add things up, so they can copy the rule exactly.

**Q4. What about adolescents?**
They are the hardest group for every model. ROC-AUC is between 0.964 and 0.990. There are only 101 records.

**Q5. Why did three models get a perfect score?**
Because the label is the questionnaire score compared with a cut-off. The scoring-rule baseline, with no machine learning, is also 100% correct. The models have learned the rule.

**Q6. Does a perfect score mean the model can detect autism?**
No. No clinical diagnosis is used anywhere in the data. The model has only learned the scoring rule of the questionnaire.

**Q7. What did the sanity checks show?**
- With shuffled labels, ROC-AUC fell to between 0.47 and 0.52. That is chance level, so nothing leaks.
- On the raw files, with only the ten answers, a plain Logistic Regression still reached 1.000 with no errors.
So the perfect scores come from the data and not from the code.

**Q8. What did the Brier score and calibration show?**
For toddlers, children and adults, EBM has the best-calibrated probabilities (ECE 0.000), then TabPFN (0.004 to 0.023). Logistic Regression ranks people just as well, but its percentages are less exact (ECE 0.025 to 0.096). For adolescents every model is less well calibrated (0.038 to 0.123).

**Q9. What did PR-AUC show?**
It is between 0.96 and 1.00 for every model in every group. That is far above chance (0.27 for adults, 0.71 for toddlers). So the high results are not caused by unbalanced classes.

**Q10. Are the differences between models real?**
After the Holm correction, EBM and TabPFN are significantly better than Random Forest for toddlers only (adjusted p = 0.021, a difference of 0.005 in ROC-AUC). No other difference is significant. Neither model is better than Logistic Regression.

**Q11. What did the cross-source test show for toddlers?**
The models transfer almost perfectly in both directions (ROC-AUC 0.986 to 1.000). This is expected, because both toddler datasets use the same Q-CHAT-10 rule. It is not strong proof that the models work on new data.

**Q12. What did the cross-source test show for adults?**
Trained on the UCI data and tested on the Kaggle data, ROC-AUC fell to between 0.871 and 0.903. The Kaggle labels follow the rule in only 80.5% of records. In the other direction Logistic Regression was best (0.998), then EBM (0.984).

**Q13. Why must the adult cross-source result be read with care?**
The Kaggle adult data is synthetic and was generated from the UCI data. So it is not an independent source. The test shows what happens when the label rule changes. It does not show how the models work on new people.

**Q14. What happened with fewer questions?**
- 4 questions: ROC-AUC 0.84 to 0.96
- 6 questions: 0.91 to 0.98
- 8 questions: 0.92 to 0.99
Recall falls faster. With 8 questions it is 0.86 to 0.97, so up to one positive case in seven is missed.

**Q15. What happened with noisy answers?**
Flipping 5% of the answers costs about 0.02 in ROC-AUC. Flipping 20% costs about 0.10 to 0.17. All models lose accuracy at about the same rate.

**Q16. Was any model weaker with noise?**
One case: EBM for toddlers at 20% noise got 0.869, while the others were about 0.90. EBM uses sharp steps for each answer, and these react strongly to a flipped answer.

**Q17. What did the fairness check show?**
For toddlers, children and adults the chosen model makes no errors in any subgroup, so no bias can be measured. For adolescents the false-positive rate is higher for girls (0.24) than boys (0.10), and higher for White European participants (0.33) than the rest (0.11).

**Q18. Can we trust the fairness numbers?**
Only as a pointer. They rest on 10 to 31 negative cases in each subgroup, which is very few. Sex and ethnicity are also two separate ways of splitting the same 101 people, so the counts must not be added.

**Q19. Which model is used in the web tool for each age group?**
EBM for toddlers, children and adults. Logistic Regression for adolescents. TabPFN is not used in the tool, because it is too large for a free hosting service.

**Q20. How were these models chosen?**
By the highest average ROC-AUC. If two are equal, the higher recall wins. If they are still equal, the more readable model wins.

**Q21. Which model is the best overall?**
There is no clear winner on accuracy. EBM, TabPFN and Logistic Regression are equal. EBM is preferred because it is readable and gives the best-calibrated probabilities.

**Q22. What should future studies on these datasets do?**
- Report the simple scoring-rule baseline next to any model.
- Add harder tests: fewer questions, noisy answers, and data from an independent source.
- Report recall, the Brier score and calibration, not only accuracy.
- Check explanation rankings over many splits and against the chance level.
