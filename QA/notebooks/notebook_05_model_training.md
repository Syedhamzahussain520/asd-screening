# Notebook 05: Model training

**Q1. What does this notebook do?**
It trains and tests the six models for each age group, runs the cross-source test, chooses the model for the web tool and saves it.

**Q2. Why is TabPFN imported first?**
If LightGBM or XGBoost is imported before it, the notebook can crash. So the import order matters.

**Q3. What do `SEED = 42` and `RERUN = True` mean?**
`SEED` fixes the random numbers so results can be repeated. `RERUN = True` trains everything again. With `False` the saved results are loaded instead.

**Q4. Section 1 "Models and parameter grids": what does `get_classifier` return?**
The model and the settings to try for it.
Example: for Logistic Regression it returns the model and `C = 0.01, 0.1, 1, 10`.

**Q5. What does the setting C mean in Logistic Regression?**
It controls how simple the model is. A small C gives a simpler model.

**Q6. Why `n_jobs=1` in every model?**
The grid search already uses all CPU cores. If each model also tried to use all cores, they would get in each other's way.

**Q7. What does `interactions` mean for the EBM?**
`interactions=0` means the EBM looks at one input at a time. `interactions=10` also allows ten pairs of inputs. The tuning chose 0 in every age group.

**Q8. What does `make_pipeline` do?**
It chains the steps: SMOTENC first, then scaling (for Logistic Regression only), then the model.

**Q9. Why does SMOTENC need the list `categorical`?**
It must know which columns are yes or no columns, so it keeps them as 0 or 1. Every input except age is such a column.

**Q10. Section 2 "Training and scoring helpers": what does `fit` do?**
It tunes one model on the data it is given. It tries every setting with 3 inner folds and keeps the one with the highest ROC-AUC.

**Q11. Why is the best setting chosen by ROC-AUC and not by accuracy?**
Accuracy can look good just by guessing the bigger class. ROC-AUC does not have this problem.

**Q12. What does `scores` do?**
It turns the predicted probabilities into measures. A probability of 0.5 or more counts as positive. It returns accuracy, precision, recall, F1, ROC-AUC, the Brier score and the counts of right and wrong predictions.

**Q13. Section 3 "Nested cross-validation": what does `nested_cv` do?**
It splits the data into 5 folds, 3 times. For each of the 15 folds it tunes and trains on the training part and tests on the test part. It also keeps the predictions for the fairness check.

**Q14. Can you walk through one fold with an example?**
Take adults (691 records). About 553 are for training and 138 for testing. SMOTENC balances the 553. The grid search picks the best setting using 3 folds inside the 553. The model then predicts the 138, and the measures are computed.

**Q15. What is saved from this section?**
`cv_folds.csv` (one row for each model and fold) and `cv_predictions.csv` (one prediction for each person in each repeat).

**Q16. Section 4 "Cross-source test": what happens?**
Each model is trained on all of one dataset and tested on all of another. There are four pairs: Thabtah toddlers to Saudi toddlers and back, UCI adults to Kaggle adults and back.

**Q17. Why is `jaundice` left out in the cross-source test?**
The Saudi file has no jaundice column. Both datasets must have the same inputs.

**Q18. Section 5 "Final model for the web app": how is the model chosen?**
By the highest average ROC-AUC, then recall, then a preference order that puts the most readable models first (EBM, then Logistic Regression). TabPFN is not offered to the app.

**Q19. Which models were chosen?**
EBM for toddlers, children and adults. Logistic Regression for adolescents.

**Q20. What is done with the chosen model?**
It is trained once more on all the data of its age group and saved as a file, together with 100 rows of background data that SHAP needs.

**Q21. Why train again on all data?**
Cross-validation is for testing. Once the model is chosen, using all the data gives the best final model.

**Q22. Why does the full run take long?**
Mostly because of EBM and TabPFN, and because the tuning runs inside every one of the 15 folds.
