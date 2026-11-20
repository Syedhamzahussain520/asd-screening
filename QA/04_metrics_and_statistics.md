# 4. Measures and statistics

**Q1. What are true positives, false positives, true negatives and false negatives?**
- True positive (TP): the person has ASD traits and the model says yes.
- False negative (FN): the person has ASD traits but the model says no. This is a missed case.
- False positive (FP): the person has no ASD traits but the model says yes. This is a false alarm.
- True negative (TN): the person has no ASD traits and the model says no.

**Q2. What is accuracy?**
The share of all people that the model gets right.
Example: 95 right out of 100 is an accuracy of 0.95.

**Q3. Why is accuracy alone not enough?**
With unbalanced classes it can mislead. Example: only 27% of adults are positive. A model that always says "no" is 73% accurate but finds nobody.

**Q4. What is recall?**
Of the people who really have ASD traits, how many the model finds.
Example: 10 real cases, the model finds 9, so recall is 0.9.

**Q5. Why is recall the most important measure for screening?**
A missed case gets no follow-up. A false alarm only leads to one more check.

**Q6. What is precision?**
Of the people the model marks as positive, how many really are positive.
Example: the model marks 10 people, and 8 are correct, so precision is 0.8.

**Q7. What is the F1-score?**
One number that mixes precision and recall. It is high only when both are high.

**Q8. What is ROC-AUC?**
Area under the ROC curve. It shows how well a model puts positive people above negative people. 1.0 is perfect. 0.5 is the same as guessing.
Example: pick one positive and one negative person at random. ROC-AUC is the chance that the model gives the positive person the higher number.

**Q9. What is PR-AUC and why was it added?**
Area under the precision-recall curve. It looks only at the positive class, so it is a better guide when the classes are unbalanced. A model that guesses gets a PR-AUC equal to the share of positive cases.
Example: for adults, guessing gives about 0.27. The models got 0.99 to 1.00.

**Q10. What is the Brier score?**
It measures how far the model's probabilities are from the truth. Lower is better and 0 is perfect.
Example: the model says 0.9 for a person who is positive (1). The error is 0.1, and its square, 0.01, is counted.

**Q11. What is calibration?**
Whether the model's percentages can be trusted.
Example: if the model says 80% for a group of people, about 80% of them should really be positive.

**Q12. What is ECE?**
Expected Calibration Error. The average gap between what the model says and what is true. 0 is perfect.
Example: the model says 80% but only 70% are positive. The gap for those people is 0.10.

**Q13. What does "mean plus or minus standard deviation" tell us?**
The mean is the average over the 15 test folds. The standard deviation shows how much the result changes between folds. A small value means stable results.

**Q14. What is a p-value?**
A number between 0 and 1. A small p-value (below 0.05) means the difference is unlikely to be only luck.

**Q15. What is the Friedman test?**
A test that asks: do the six models perform differently at all? It ranks the models in every fold and checks if the ranks differ.

**Q16. What is the Nemenyi test?**
A follow-up test that asks: which pairs of models differ?

**Q17. Why are Friedman and Nemenyi only a "description" here?**
These tests assume that the blocks are independent, usually separate datasets. Here the blocks are 15 folds of the same dataset, and the folds share training records. So the p-values come out too small. The supervisor pointed this out.

**Q18. What is the corrected resampled t-test?**
A t-test made for cross-validation results. It makes the variance bigger to allow for the fact that folds share training data. It was proposed by Nadeau and Bengio. The conclusions of this project are based on it.

**Q19. What is the Holm correction?**
When many tests are run, some look significant only by luck. The Holm correction makes the p-values bigger to allow for that.
Example: three p-values 0.01, 0.04 and 0.30 become 0.03, 0.08 and 0.30.

**Q20. Why was Holm needed?**
Nine comparisons are made in each age group (EBM against five models and TabPFN against four more). The supervisor asked for a correction for multiple comparisons.

**Q21. What is an effect size?**
A number that says how big a difference is, not only whether it exists.
- Cohen's d: about 0.2 is small, 0.5 is medium, 0.8 is large.
- Kendall's W: from 0 to 1. It says how much the folds agree on the ranking of the models.

**Q22. What is Spearman's rank correlation?**
A number from -1 to 1 that says how similar two rankings are. 1 means the same order. 0 means no relation.
Example: two methods both rank question 5 first and question 9 last. Their correlation will be high.

**Q23. What is top-five overlap?**
How many of the five most important questions two methods share. The highest is 5.

**Q24. What is the chance level for top-five overlap?**
2.5. Two random rankings of ten questions share 2.5 of their top five on average. So an overlap near 2.5 means no real agreement.

**Q25. What is the false-positive rate?**
Of the people who are really negative, how many the model wrongly marks as positive.
Example: 20 negative people, 5 wrongly marked, so the rate is 0.25.
