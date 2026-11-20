# 11. Hard questions an examiner may ask

**Q1. If a simple sum is 100% correct, why use machine learning at all?**
On the full questionnaire there is no reason, and the project says so. That is the main finding. Machine learning was used here to test the claims in earlier papers, not to replace the questionnaire.

**Q2. Then what is your contribution?**
Showing, with evidence, what the near-perfect accuracy in earlier papers means. The project gives a baseline, sanity checks, harder tests and a careful check of the explanations. It also gives advice for future studies on these datasets.

**Q3. Is this not just data leakage in your own work?**
No. The total score was removed, and all learning steps happen inside the training folds. The perfect score comes from the label itself, which is a fixed function of the ten answers. The shuffled-label check proves there is no leak in the code.

**Q4. Earlier papers removed the score column too. What is different here?**
Removing the score is not enough, because the ten answers still fix the label. This project shows that directly with the scoring-rule baseline, and then tests the models where the rule cannot be recovered exactly.

**Q5. Can your model diagnose autism?**
No. The labels are questionnaire results, not diagnoses from a clinician. The model can only predict the questionnaire result.

**Q6. Why did you choose EBM if it is not more accurate than Logistic Regression?**
They are equal on accuracy. EBM is readable and gave the best-calibrated probabilities in three of the four age groups. For adolescents Logistic Regression is used.

**Q7. Why is TabPFN in the study if you do not deploy it?**
To answer RQ1. It is a recent model made for small tables, so it is a fair test of whether a modern model helps. It matched the best models but did not beat them.

**Q8. Your cross-source test uses a synthetic dataset. Is RQ2 answered?**
Only in part, and the paper says so. The toddler test shares the same rule and the adult test is not independent. A test on independent data is listed as future work.

**Q9. Why are the Friedman and Nemenyi tests still in the work?**
They were in the approved proposal. They are kept as a description of the ranking. The conclusions rest on the corrected t-test with the Holm correction.

**Q10. Why do EBM and SHAP rank the questions differently if they are the same numbers?**
They are the same once both start from the same reference point. The importance is the average size of each value, and that depends on the reference point. The two methods use different ones. Because all ten questions are almost equally important, a small shift changes the order.

**Q11. Is LIME wrong then?**
Not wrong, but not informative here. In two age groups it gives every question almost the same weight, so its ranking is mostly noise.

**Q12. Why not use more data or deep learning?**
The public datasets are what earlier papers used, so the same data was needed to test their claims. The data is small, and deep learning does not help on small tables of yes and no answers.

**Q13. How do you know your results are not just luck?**
Repeated cross-validation gives 15 test folds for each model, results are reported with their spread, and the explanation analysis is repeated over 10 splits. Seeds are fixed so the runs can be repeated.

**Q14. Is your tool safe for parents to use?**
It is a research demonstration and says so on every page. It is not a medical device. It shows the standard questionnaire score, tells the user it is not a diagnosis, and stores nothing.

**Q15. What would you do differently next time?**
Look at how the label was made before choosing the models, and look for data with clinical diagnoses from the start.

**Q16. Why does recall matter more than accuracy here?**
In screening, missing a real case is the costly mistake, because that person gets no follow-up. Recall measures exactly that.

**Q17. What is the practical use of the reduced-questionnaire result?**
It shows the cost of a shorter questionnaire. With 8 of the 10 questions, up to one positive case in seven is missed. So shortening the questionnaire is risky.

**Q18. Why did you apply SMOTENC if the models were already perfect?**
The proposal planned for class imbalance, and it matters for the harder settings and for adolescents. It is applied inside the folds, so it cannot make the results look better than they are.

**Q19. Could the fairness difference for girls be real?**
It could, but the data cannot show it. The rate rests on 18 negative cases for girls. It is reported as a pointer for future work, not as a finding.

**Q20. What is the single most important sentence of your project?**
High accuracy on these datasets shows that a model has learned a screening rule, not that it can diagnose autism.
