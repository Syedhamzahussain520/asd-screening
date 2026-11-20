# 16. Discussion: what the results mean

**Q1. What is the first thing the results tell us?**
A perfect score on these datasets means the model has learned the scoring rule. The label is the questionnaire score compared with a cut-off, and a rule that only adds the ten answers is also 100% correct.

**Q2. Is a more complex model better for this task?**
No. Logistic Regression, the simplest model, is as good as EBM and TabPFN. The tree models are slightly worse.

**Q3. What do the harder settings add?**
A more useful picture. When the rule cannot be recovered exactly, no model is perfect, and all six lose accuracy at a similar rate. EBM and TabPFN show no clear advantage.

**Q4. What does the cross-source test add?**
Less than was hoped. The toddler datasets share the same rule, and the second adult dataset is synthetic. So neither result shows how the models work on new people.

**Q5. What does a model add to the score?**
On the full questionnaire, nothing. A model is only useful when the rule cannot be applied directly, for example when answers are missing. Even then it estimates the questionnaire result, not a diagnosis.

**Q6. Why is EBM used in the tool for three groups?**
It is as accurate as the others, it is readable, it made no errors in cross-validation and it gave the best-calibrated probabilities.

**Q7. What do the explanation results mean?**
All three methods agree that each question counts for about one tenth. They do not agree reliably on which questions come first, because there is no real order to find. EBM and SHAP are not independent, and LIME is close to chance in two groups.

**Q8. Do the results agree with earlier studies?**
The numbers agree: very high accuracy. The reading is different. Earlier studies present it as the ability to detect autism. This project shows it is the ability to copy a scoring rule.

**Q9. Is any earlier result wrong?**
Not wrong as a number. But a perfect score should not be presented as diagnostic ability when the label comes from the questionnaire itself.

**Q10. What is the practical meaning for researchers?**
Report a baseline, add harder tests, test on independent data, and report recall and calibration together with accuracy.

**Q11. What is the practical meaning for clinicians and families?**
The standard questionnaire score is already the best use of these ten answers. A machine learning model does not improve it.

**Q12. What surprised you most?**
That a plain Logistic Regression on raw, uncleaned files, using only ten answers, made no errors at all.

**Q13. What is the weakest part of the study?**
There are no clinical diagnoses in the data, so nothing can be said about real diagnostic accuracy. The paper is clear about this.
