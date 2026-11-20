# 17. Implementation: what was done in which file

**Q1. Which file downloads the data?**
`notebooks/01_download_data.ipynb`. It downloads three datasets from UCI and three from Kaggle into `data/raw/`.

**Q2. Which file proves how the label is made?**
`notebooks/02_understanding_the_data.ipynb`. It adds up the ten answers, applies the cut-off and compares the result with the label for every row.

**Q3. Which file cleans the data?**
`notebooks/03_preprocessing.ipynb`. It renames columns, removes duplicates and wrong ages, and saves the cleaned files to `data/processed/`.

**Q4. Which file makes the charts about the data?**
`notebooks/04_eda.ipynb`. Its figures are saved in `results/figures/`.

**Q5. Which file trains the models?**
`notebooks/05_model_training.ipynb`. It runs the cross-validation, the cross-source test, chooses the model for each age group and saves it.

**Q6. Which file makes the result tables and statistical tests?**
`notebooks/06_results.ipynb`. It also has the baseline, the sanity checks, PR-AUC, calibration and the fairness check.

**Q7. Which file compares SHAP, LIME and EBM?**
`notebooks/07_explainability.ipynb`.

**Q8. Which file runs the fewer-questions and noisy-answers tests?**
`notebooks/08_harder_settings.ipynb`.

**Q9. Where are the results saved?**
- `results/tables/`: CSV files such as `cv_folds.csv`, `main_results.csv`, `cross_source.csv`, `harder_settings.csv`, `explanation_agreement.csv`, `pr_auc_calibration.csv`, `corrected_ttests.csv`, `bias_check.csv`, `sanity_checks.csv`, `dataset_sizes.csv`.
- `results/figures/`: all figures as PNG files.
- `results/models/`: one saved model for each age group.

**Q10. Which files make up the web app?**
- `app/Home.py`: the first page.
- `app/pages/1_Screening.py`: the questions, the result and the explanation chart.
- `app/pages/2_Model_Performance.py`: the test results.
- `app/pages/3_About.py`: data, method, limits and privacy.
- `app/questions.py`: the wording and scoring of the questionnaires.
- `app/models/` and `app/data/`: the saved models and result tables that the app reads.

**Q11. Which function builds a model with its settings?**
`get_classifier(name)` in notebook 05. It returns the model and the settings to try.

**Q12. Which function builds the pipeline?**
`make_pipeline(name, features)` in notebook 05. It chains SMOTENC, scaling (for Logistic Regression only) and the model.

**Q13. Which function does the tuning?**
`fit(name, X, y, features)` in notebook 05. It runs the grid search with 3 inner folds and returns the best model.

**Q14. Which function runs the cross-validation?**
`nested_cv(name, df, features)` in notebook 05. It loops over the 15 folds and collects the scores and predictions.

**Q15. Which function computes the measures?**
`scores(y_true, prob)` in notebook 05: accuracy, precision, recall, F1, ROC-AUC, Brier score and the counts of right and wrong predictions.

**Q16. Which functions run the statistical tests?**
In notebook 06: `corrected_ttest(a, b)` for the corrected t-test, `holm(p)` for the Holm correction and `ece(y, prob)` for the calibration error.

**Q17. Which functions make the harder settings?**
In notebook 08: `top_questions(df, k)` picks the k most useful questions, and `flip_answers(X, p, rng)` flips answers at random.

**Q18. Which functions make the explanations?**
In notebook 07: `ebm_scores`, `shap_values` and `lime_weights`. In the app, `explain(bundle, row)` computes the SHAP values for one person.

**Q19. Which function turns an answer into a score in the app?**
`score_answer(group, item, answer)` in `app/questions.py`.
Example: for adult question 1, "Slightly agree" gives 1 point.

**Q20. How is the app connected to the notebooks?**
Notebook 05 saves the chosen models and summary tables into the `app` folder. The app only reads them. It does not train anything.
