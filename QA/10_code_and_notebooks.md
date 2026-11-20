# 10. Code and notebooks

**Q1. How is the code organised?**
- `notebooks/`: eight Jupyter notebooks, numbered 01 to 08, one for each stage.
- `app/`: the Streamlit web app.
- `data/`: raw files (downloaded by notebook 01) and cleaned files.
- `results/`: tables, figures and saved models.
- `README.md`, `ABOUT.md`, `NOTEBOOKS.md`: how to run it, the background, and a guide to each notebook.

**Q2. What does each notebook do?**
1. `01_download_data`: downloads the six datasets from UCI and Kaggle.
2. `02_understanding_the_data`: looks at the columns and checks how the label was made.
3. `03_preprocessing`: cleans the data and saves it.
4. `04_eda`: charts of class balance, age, scores, answers and correlations.
5. `05_model_training`: trains the six models with cross-validation, runs the cross-source test and saves the chosen models.
6. `06_results`: result tables, PR-AUC, calibration, the baseline, sanity checks, statistical tests and the fairness check.
7. `07_explainability`: compares SHAP, LIME and EBM.
8. `08_harder_settings`: the reduced questionnaire and noisy answers tests.

**Q3. In which order must the notebooks run?**
From 01 to 08. Each one uses files made by the earlier ones.

**Q4. What is needed to run the code?**
Python 3.11, the packages in `requirements-research.txt`, and a free Kaggle account for the token that notebook 01 needs.

**Q5. What is the difference between `requirements.txt` and `requirements-research.txt`?**
`requirements.txt` is the short list that the web app needs. Streamlit Cloud installs it. `requirements-research.txt` is the full list for the notebooks.

**Q6. How do I run the web app on my computer?**
Install the packages, then run `streamlit run app/Home.py` in the project folder.

**Q7. Which file starts the web app?**
`app/Home.py`. The other pages are in `app/pages/`.

**Q8. Where are the questions and the scoring kept?**
In `app/questions.py`. It has the wording of each questionnaire, the cut-off for each age group and the function that turns an answer into 0 or 1.

**Q9. What is saved in a model file?**
One file for each age group in `results/models/` (copied to `app/models/`). It holds the trained model, its name, the list of inputs, the chosen settings and a small sample of rows that SHAP needs.

**Q10. Why must TabPFN be imported before LightGBM and XGBoost?**
If they are imported in the other order, the notebook can crash, because the libraries use two different copies of a shared parallel-computing library.

**Q11. What does `SEED = 42` do?**
It fixes the random numbers, so the same results come out on every run.

**Q12. What does `RERUN = True` do in notebooks 05 and 08?**
When it is True, the models are trained again. When it is False, the saved results are loaded, which is much faster.

**Q13. Why is the grid of settings small?**
The datasets are small, and the search runs many times (inside every fold). A large grid would take very long and would not help much.

**Q14. What settings are tried for each model?**
- Logistic Regression: C = 0.01, 0.1, 1, 10 (a small C gives a simpler model).
- Random Forest: 200 or 500 trees; depth unlimited, 5 or 10.
- XGBoost: 100 or 300 trees; depth 3 or 5; learning rate 0.05 or 0.1.
- LightGBM: 100 or 300 trees; 7 or 15 leaves; learning rate 0.05 or 0.1.
- EBM: 0 or 10 pair terms.
- TabPFN: nothing to tune.

**Q15. What did the EBM tuning choose?**
No pair terms in every age group. So the final EBMs are purely additive: one curve for each input.

**Q16. How is the app deployed?**
On Streamlit Community Cloud, from the GitHub repository, with `app/Home.py` as the main file. A push to GitHub makes the app rebuild by itself.

**Q17. Do the notebooks have comments?**
Yes. Every notebook and every app file has short comments in easy English. Short names such as SMOTE, EBM, SHAP and LIME are written in full with an example where they are first used.
