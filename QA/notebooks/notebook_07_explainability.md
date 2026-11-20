# Notebook 07: Explainability

**Q1. What does this notebook do?**
It answers RQ3. It explains the same EBM in three ways (its own values, SHAP and LIME) and measures how well the three agree.

**Q2. Why was this notebook rewritten?**
The first version compared values that were measured on different rows and different scales, and used only one split. The supervisor asked for this to be checked.

**Q3. What does `log_odds` do?**
It returns the model's score before it is turned into a probability. All three methods explain this same number, so they can be compared fairly.

**Q4. Section 1: what does `ebm_scores` return?**
The EBM's own score for each input, for every test row. It is exact, because it comes from the model itself.

**Q5. What does `shap_values` return?**
The SHAP value of each input for every test row. It needs "background" rows to compare with. Here 100 training rows are used.

**Q6. What does `lime_weights` return?**
One weight for each input and each test row. LIME explains one row at a time, so the notebook loops over the test rows.

**Q7. Why `mode="regression"` for LIME?**
Because the log-odds is a number, not a class. This puts LIME on the same scale as the other two.

**Q8. What does the main loop do?**
For each age group and each of 10 splits: train an EBM on the training part, run the three methods on the same test rows, and store the average size of each input's effect.

**Q9. How is "importance" measured?**
As the average size (ignoring plus or minus) of an input's effect over the test rows.
Example: if question 1 moves the score by 2, 3 and 1 for three people, its importance is 2.

**Q10. Section 2 "Is SHAP independent of the EBM?": what is checked?**
The EBM scores are moved to the same starting point as SHAP, and the two are compared. The largest difference is practically zero. So SHAP gives back the EBM's own numbers.

**Q11. Section 3 "Importance per method": what does the figure show?**
For each age group, the importance of each input under each method, scaled so each method adds up to 1. Each question gets about 0.10.

**Q12. Section 4 "Do the methods agree?": what is measured?**
For every pair of methods: the Spearman correlation of the question rankings and the number of shared questions in the top five. The table gives the average and spread over the 10 splits.

**Q13. Why are only the ten questions ranked, and not the personal details?**
The personal details are near zero under every method. Including them would make the agreement look better than it is.

**Q14. What does the chance-level cell do?**
It makes 20,000 pairs of random rankings and counts how many of their top five they share. The answer is about 2.5.

**Q15. Section 5 "Top questions": what does it show?**
The five highest-ranked questions for each age group and method.

**Q16. Why must question numbers not be compared across age groups?**
The questionnaires are different. Question 9 for adults is not the same question as question 9 for children.

**Q17. Section 6 "SHAP summary plots": how do I read them?**
Each dot is one person. Red dots are answers scored 1. Dots on the right push the prediction towards "ASD traits".

**Q18. Section 7 "Answer to RQ3": what is the answer?**
All questions matter about equally. EBM and SHAP are the same numbers. LIME agrees much less and is close to chance for children and adults. The rankings are not stable.
