# Notebook 08: Harder settings

**Q1. What does this notebook do?**
It tests the six models in two harder situations: with fewer questions and with noisy answers.

**Q2. Why are harder settings needed?**
With all ten answers every good model can learn the scoring rule, so they all look perfect and cannot be compared. In a harder setting the rule cannot be recovered exactly.

**Q3. What are `K_VALUES` and `NOISE_LEVELS`?**
`K_VALUES = [4, 6, 8]` is how many questions are kept. `NOISE_LEVELS = [0.05, 0.10, 0.20]` is the share of answers that are flipped.

**Q4. Why are the model settings fixed here, with no tuning?**
To keep the run time reasonable. Many more models are trained in this notebook than in notebook 05.

**Q5. What does `top_questions` do?**
It computes the chi-square value of each question against the label, using the training data only, and returns the k questions with the highest values.

**Q6. Why "training data only"?**
If the test data helped to choose the questions, that would be leakage.

**Q7. What does `flip_answers` do?**
It changes each answer with chance p.
Example: with p = 0.10 about one answer in ten is flipped, so a 0 becomes 1 or a 1 becomes 0.

**Q8. Is noise added to the training data?**
No. The models are trained on clean data. Noise is added to the test answers only. This is like a model in real use that meets careless answers.

**Q9. How is the data split in this notebook?**
5 folds repeated 2 times, so 10 test folds.

**Q10. What happens inside one fold?**
1. Train each model on all ten questions and test it on the clean test part.
2. Test the same model on the three noisy copies of the test part.
3. Train a new model on the 4, 6 and 8 chosen questions and test it.

**Q11. With fewer questions, what does the model have to predict?**
The label of the full questionnaire. So it must guess the full result from only part of the answers.

**Q12. What were the results with fewer questions?**
ROC-AUC is 0.84 to 0.96 with 4 questions, 0.91 to 0.98 with 6, and 0.92 to 0.99 with 8. Recall falls faster than ROC-AUC.

**Q13. What were the results with noise?**
5% noise costs about 0.02 in ROC-AUC. 20% noise costs about 0.10 to 0.17. All models fall at about the same rate.

**Q14. Which models did best?**
Logistic Regression, EBM and TabPFN stay very close to each other. LightGBM is usually the lowest.

**Q15. What do the two figures show?**
One line for each model. In the first, ROC-AUC against the number of questions. In the second, ROC-AUC against the share of flipped answers.

**Q16. What is the practical meaning?**
A shorter questionnaire or careless answers reduce the quality of screening, and a more complex model does not protect against this.

**Q17. Which file does this notebook save?**
`results/tables/harder_settings.csv`, plus the figures `fig_reduced_questions.png` and `fig_noise.png`.
