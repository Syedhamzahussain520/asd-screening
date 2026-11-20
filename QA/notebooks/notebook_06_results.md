# Notebook 06: Results

**Q1. What does this notebook do?**
It turns the saved fold scores from notebook 05 into tables, figures and statistical tests. It does not train the six models again.

**Q2. Section "Records per dataset": what does it show?**
The number of records, positive cases and negative cases in each cleaned dataset.
Example: adults have 691 records, 185 positive and 506 negative.

**Q3. Section 1 "Main results": what does the table show?**
The average and the spread of each measure over the 15 test folds, for every model and age group. It is saved as `main_results.csv`.

**Q4. Section 1b "PR-AUC and calibration": why was it added?**
The supervisor asked for the Brier score, calibration and PR-AUC to be reported.

**Q5. How is PR-AUC computed here?**
From the saved predictions. Each person is predicted once in each of the 3 repeats. PR-AUC is computed for each repeat and then averaged.

**Q6. What does the function `ece` do?**
It puts the predictions into 10 boxes by probability (0 to 10%, 10 to 20%, and so on). In each box it compares the average probability with the real share of positive cases.
Example: a box with an average of 80% where 70% are really positive has a gap of 0.10.

**Q7. How do I read the calibration figure?**
A model on the dashed diagonal line gives percentages that match the truth. Lines far from it are less trustworthy.

**Q8. Section 2 "Baseline": what is computed?**
The ten answers are added up and compared with the cut-off, with no model. It is right for 100% of records.

**Q9. Section 2b "Sanity checks": what are they?**
1. The labels are shuffled and Logistic Regression is trained again. The score falls to about 0.5.
2. Logistic Regression is trained on the raw files with only the ten answers. It still reaches 1.000.

**Q10. Section 3 "Spread across folds": what does it show?**
Box plots of ROC-AUC and recall over the 15 folds. A narrow box means stable results. For adolescents the boxes are wide.

**Q11. Section 4 "Are the differences real?": what tests are run?**
The Friedman test (with Kendall's W), the Nemenyi test, and the corrected resampled t-test with the Holm correction and an effect size.

**Q12. What does `corrected_ttest` do differently from a normal t-test?**
It makes the variance bigger, because the folds share training rows. A normal t-test would find too many "significant" differences.

**Q13. What does `holm` do?**
It adjusts the nine p-values of each age group, because many comparisons are made together.

**Q14. What was the result of the tests?**
Only one difference is significant after correction: EBM and TabPFN against Random Forest for toddlers (adjusted p = 0.021).

**Q15. Section 5 "Missed cases": what is counted?**
The false negatives, added up over the 15 folds. Example: Random Forest missed about 6% of positive adult cases, while EBM missed none.

**Q16. Section 6 "Cross-source results": what is added here?**
The cross-source score is put next to the score of the same model on its own data, so the drop can be seen directly. A bar chart is also made.

**Q17. Section 7 "Bias check": how does it work?**
The saved predictions of the chosen model are joined with each person's sex and ethnicity. Recall and the false-positive rate are computed for each subgroup, with the number of positive and negative cases.

**Q18. Why are small ethnic groups merged into "Other/Unknown"?**
Groups with fewer than 20 people are too small to measure a rate.

**Q19. Section 8 "Answers": what does it hold?**
The written answers to RQ1 and RQ2, with the numbers that support each point.

**Q20. Which files does this notebook save?**
`main_results.csv`, `dataset_sizes.csv`, `pr_auc_calibration.csv`, `sanity_checks.csv`, `corrected_ttests.csv`, `bias_check.csv` and several figures.
