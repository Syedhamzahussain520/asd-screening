# Notebook guide

A walk-through of each notebook, section by section, so the code can be followed without running it. Paths inside the notebooks are relative to the `notebooks/` folder, which is why they start with `../`.

Conventions used in every notebook:

- `QUESTIONS = ["A1", ..., "A10"]` are the ten questionnaire answers.
- `GROUPS = ["toddler", "child", "adolescent", "adult"]` are the four main age groups.
- The two extra datasets are called `toddler_saudi` and `adult_kaggle`.
- `RAW`, `PROCESSED` and `FIGURES` are `pathlib.Path` objects pointing at `data/raw/`, `data/processed/` and `results/figures/`.

---

## 01_download_data.ipynb

Downloads the six datasets into `data/raw/`. No data is changed here.

**Setup cell.** Imports `requests` (HTTP download), `zipfile` and `io` (unpack a zip held in memory) and `pathlib`. Two dictionaries map a short dataset name to where it lives:

- `UCI` holds the path part of the UCI download URL for child (dataset 419), adolescent (420) and adult (426).
- `KAGGLE` holds the Kaggle `owner/dataset` slug for toddler, toddler_saudi and adult_kaggle.

**UCI datasets.** For each entry in `UCI`: create `data/raw/<name>/`, fetch `https://archive.ics.uci.edu/static/public/<path>.zip` with a 60-second timeout, raise an error if the HTTP status is not OK, and extract the zip straight from memory into the folder. Each zip contains an `.arff` data file and a Word document describing the data.

**Kaggle datasets.** `KaggleApi().authenticate()` reads the token from the `.kaggle/kaggle.json` file in the user's home folder. `dataset_download_files(ref, path=..., unzip=True)` downloads and unpacks each dataset into its own folder.

**What was downloaded.** Walks through `data/raw/` and prints every file with its size in KB. This is a quick check that nothing is missing and shows the file names used in the next notebooks. The markdown below notes that `adult_kaggle` has an unlabelled `test.csv` (from a competition), so only `train.csv` is used, and records the licences.

---

## 02_understanding_the_data.ipynb

Reads the raw files and works out what each column means and how the label was produced. Nothing is saved.

**1. Loading the raw files.** The UCI files are ARFF. `scipy.io.arff` fails on them because some values are quoted with trailing spaces, so a small `read_arff()` function is written instead:

1. read the file as text (latin-1 encoding, because of a few non-ASCII characters),
2. split it at the `@data` line into header and body,
3. take the column names from the `@attribute` lines of the header,
4. read the body with `pandas.read_csv`, using `'` as the quote character and `?` as the missing-value marker.

The `raw` dictionary then holds one DataFrame per dataset, the three UCI ones through `read_arff()` and the three Kaggle ones through `read_csv()`. A small table prints rows and columns per dataset, and `head()` is shown for the adult and toddler files to see the two different layouts.

**2. The screening questionnaires.** Markdown only. Lists the ten Q-CHAT-10 items and the ten AQ-10 items (child, adolescent and adult wording) and explains the scoring: in the files each answer is already scored as 0 or 1, and the total score is the sum.

**3. Columns.** A table of every column in the UCI layout with its meaning and whether it is used as a feature. The key decisions: the ten scored answers, age, gender, jaundice and family autism are features; ethnicity is kept only for the bias check; country, relation, `used_app_before` and `age_desc` are dropped; `result` (the total score) is dropped because the label is computed from it. The toddler files have the same information under different names.

A code cell counts missing values per column per dataset. Only `age`, `ethnicity` and `relation` have any.

**4. How the class label was made.** The dataset description says the class was assigned automatically from the score. The code checks this for every row:

- `label_col` gives the name of the label column for the two toddler files (the others use `Class/ASD`).
- `cutoff` gives the threshold per dataset: 3 for Q-CHAT-10, 6 for AQ-10.
- For each dataset, the answer columns are found with a regular expression (`A\d+` or `A\d+_Score`), the label is converted to True/False, the rule `sum of answers > cutoff` is evaluated, and the share of rows where rule and label agree is printed.

A cross-tabulation of label against score for the adult file shows the split visually: every score up to 6 is "NO", every score from 7 is "YES".

**What this means** (markdown): in the five ASDTests/Saudi datasets the match is 100%, so dropping the score column is necessary but not enough; the models learn the scoring rule, not a diagnosis; under the rule every question has equal weight. The Kaggle adult data matches the rule only about four times in five.

**5. Summary.** Bullet list of the findings carried into notebook 03.

---

## 03_preprocessing.ipynb

Cleans the six datasets and writes `data/processed/<name>.csv`. Scaling and oversampling are deliberately *not* done here; they belong inside the cross-validation pipeline so they only see training data.

**Setup.** Same imports and `read_arff()` as notebook 02, plus `FEATURES = QUESTIONS + ["age", "male", "jaundice", "family_asd"]`, the final list of model inputs.

**1. One schema for all datasets.** `RENAME` holds three mappings from original column names to the common names: one for the Thabtah toddler file, one for the Saudi toddler file and one (`"uci"`) for the three UCI files and the Kaggle adult file. `yes_no()` turns any yes/no or 1/0 column into integers 0/1.

`harmonise(name, df)` builds the cleaned frame for one dataset:

- rename the columns using the right mapping,
- take A1–A10 as integers,
- `age` as a number (`errors="coerce"` turns anything unreadable into missing),
- `male` = 1 if gender starts with "m",
- `jaundice` and `family_asd` through `yes_no()`; jaundice is left missing for the Saudi data, which has no such column,
- `ethnicity` kept as is (missing for the Saudi data),
- `score` kept **for analysis only**, never as a feature,
- `asd` = the label as 0/1.

`data` holds the harmonised frames and `rows_before` remembers the original row counts for the summary at the end.

**2. Duplicates.** `df.duplicated().sum()` counts exact copies; `drop_duplicates()` removes them. The markdown explains why: a copied record falling in both training and test fold makes results look better than they are.

**3. Age.** `AGE_RANGE` gives the valid range per questionnaire (toddler 12–36 months, child 4–11, adolescent 12–16, adult 17–100 years). `name.split("_")[0]` maps `toddler_saudi` to the toddler range and `adult_kaggle` to the adult range. Rows with a missing age or an age outside the range are dropped and the count is printed. This removes the adult aged 383 and the under-age rows in the Kaggle adult file.

**4. Ethnicity.** `clean_ethnicity()` strips spaces, replaces hyphens with spaces, title-cases the text, merges `Others` into `Other` and `Pacifica` into `Pasifika`, and fills missing values with `Unknown`. The value counts for adults are shown as a check.

**5. Model inputs.** A table of keep/drop decisions for each column with the reason, and a print of `FEATURES`. All inputs except age are 0/1, so no encoding is needed.

**6. Result and save.** A summary table with rows before, rows after and the percentage of positive labels per dataset. Then each frame is written to `data/processed/<name>.csv` without the index, and the saved file names are listed. The closing markdown notes the different class balance per group, which is why SMOTE is used later.

---

## 04_eda.ipynb

Exploratory analysis of the four cleaned main datasets. Every figure is saved as a PNG in `results/figures/`.

**Setup.** Imports matplotlib, pandas, seaborn and `chi2_contingency` from scipy. Loads the four processed CSVs into `data` and adds a `class` column with readable labels ("ASD traits" / "No ASD traits"). `CUTOFF` repeats the thresholds for the score plot.

**Figure style.** `COLUMN = 3.5` and `PAGE = 7.16` are the widths in inches of one column and the full page in a two-column paper; every figure is built at one of these widths so it can be dropped into the paper without rescaling. `COLORS` fixes one colour per class, `HANDLES` are legend entries shared by the multi-panel figures, and `sns.set_theme()` sets a serif font at 7–8 pt with 300 dpi output. `save(fig, name)` writes `results/figures/<name>.png`.

**1. Class balance.** `counts` is a table of records per class per group with the percentage positive. A bar chart of it is saved as `fig_class_balance`.

**2. Age.** A 2×2 grid, one panel per group, with a stacked histogram of age by class (`sns.histplot(..., multiple="stack")`). Toddlers are in months, the others in years. Saved as `fig_age`.

**3. Questionnaire score.** The same 2×2 layout, but the x-axis is the score (sum of A1–A10) and a dashed vertical line marks the cut-off. Saved as `fig_score_distribution`. The markdown points out that the two colours never overlap, which is the leakage finding as a picture.

**4. Answers by class.** `rates` is a 10 × 8 table: for every question, the share of people scoring 1 in each (group, class) combination, built with `groupby("asd")[QUESTIONS].mean()`. Drawn as an annotated heatmap, saved as `fig_answer_rates`. The markdown reminds that the AQ-10 wording differs between age groups, so a row is not always the same question across columns.

**5. Chi-square test.** For every group and every input (ten questions plus male, jaundice, family history), a contingency table against the label is built with `pd.crosstab()` and passed to `chi2_contingency()`. The chi-square statistics are pivoted into a features × groups table and drawn as a heatmap, saved as `fig_chi_square`. A second small table shows the p-values for the three personal details only, since nearly every question is significant anyway.

**6. Relationships between questions.** For each group, `df[QUESTIONS].corr()` gives the correlation between the ten answers (the phi coefficient for 0/1 data). Drawn as a 2×2 grid of heatmaps with one shared colour bar, saved as `fig_question_correlation`.

**7. Personal details.** A table of the share of positive screens for male vs female, jaundice vs none and family history vs none, per group.

**Summary.** Markdown with the findings (balance per group, perfect separation at the cut-off, which questions separate the classes most and least, which personal details relate to the label) and a table suggesting the size of each figure in the paper.

---

## 05_model_training.ipynb

Trains and compares the six models for every age group, runs the cross-source test and saves the final model per group. Everything that learns from data happens inside a pipeline that is fitted on the training fold only.

**Setup.** TabPFN is imported first on purpose (see the comment in the cell). Then scikit-learn (models, metrics, cross-validation, scaler), imbalanced-learn (`SMOTENC` and its `Pipeline`, which knows that oversampling must only run at fit time), InterpretML (`ExplainableBoostingClassifier`), XGBoost and LightGBM. Output folders are created. `SEED = 42` fixes every random choice. `RERUN = True` trains from scratch; `False` reads the saved tables. The six processed CSVs are loaded into `data`.

**1. Models and parameter grids.** `get_classifier(name)` returns a model object and its small grid of hyperparameters:

- Logistic Regression: regularisation strength `C`.
- Random Forest: number of trees and maximum depth.
- XGBoost and LightGBM: number of trees, depth or number of leaves, learning rate.
- EBM: whether to allow pairwise interaction terms (0 or 10).
- TabPFN: no grid; it has no hyperparameters to tune. `ignore_pretraining_limits=True` lets it run on more than 1,000 rows on CPU, which the toddler training folds exceed after oversampling.

All models use `n_jobs=1`; parallelism is applied at the grid-search level instead, which avoids clashes between the libraries.

`make_pipeline(name, features)` wraps the model in a pipeline: SMOTENC first (every feature except age is marked categorical), then a `StandardScaler` for Logistic Regression only, then the classifier. The grid keys are prefixed with `clf__` so `GridSearchCV` knows they belong to the last step.

**2. Training and scoring helpers.** `fit(name, X, y, features)` builds the pipeline and, if there is a grid, runs `GridSearchCV` with an inner stratified 3-fold split scored by ROC-AUC, returning the best pipeline and its parameters. It is only ever called with training data, so the test fold never influences tuning, scaling or oversampling. `scores(y_true, prob)` turns predicted probabilities into a row of metrics: accuracy, precision, recall, F1, ROC-AUC, Brier score and the four confusion-matrix counts, using 0.5 as the decision threshold.

**3. Nested cross-validation (RQ1).** `nested_cv(name, df, features)` makes a `RepeatedStratifiedKFold` with 5 folds and 3 repeats (15 test folds). For each fold it calls `fit()` on the training part, predicts probabilities for the test part, records the scores with the chosen parameters, and keeps the out-of-fold predictions (row index, repeat number, probability) for the fairness check in notebook 06. The loop below runs this for every group and every model, printing the mean ROC-AUC and recall as it goes, and writes `results/tables/cv_folds.csv` (one row per model per fold) and `results/tables/cv_predictions.csv` (one row per record per model per repeat). A grouped table of mean metrics is shown at the end.

**4. Cross-source test (RQ2).** `PAIRS` lists the four train/test directions: Thabtah toddlers and Saudi toddlers each way, UCI adults and Kaggle adults each way. `CROSS_FEATURES` drops jaundice, because the Saudi data does not record it. For every pair and model, `fit()` is called on the whole training dataset and the model is scored on the whole test dataset. Results go to `results/tables/cross_source.csv` and are shown as a train/test × model table of ROC-AUC.

**5. Final model for the web app.** `PREFERENCE` orders the deployable models from most to least interpretable; TabPFN is excluded because it needs PyTorch and a large weights file. Mean ROC-AUC per model is rounded to three decimals, ties are broken by recall and then by the preference order, and the top model per group is kept in `best`. Each chosen model is retrained on all data of its group with `fit()` and saved with `joblib.dump` as a bundle: group name, model name, the fitted pipeline, the feature list, the chosen parameters and a 100-row background sample used later for SHAP explanations. The bundle is written to `results/models/<group>.joblib` and copied into the app folder. The last cell writes the summary tables the app displays: mean and standard deviation of every metric per group and model, the cross-source table and the chosen models.

---

## 06_results.ipynb

Turns the per-fold scores saved by notebook 05 into the tables, figures and statistical tests for RQ1 and RQ2. Nothing is trained here except the small controls in the sanity checks.

**Setup.** Loads `cv_folds.csv` and `cross_source.csv`. `METRICS` lists the six scores reported. The figure style is the same as notebook 04. `SHORT` maps the model names to the abbreviations used in figures.

**Records per dataset.** A small table with the number of records, positive cases and negative cases in each of the six cleaned datasets, saved as `results/tables/dataset_sizes.csv`.

**1. Main results.** Groups the folds by age group and model, takes mean and standard deviation of every metric, formats them as "mean ± sd", orders the rows as `GROUPS × MODEL_NAMES` and saves `results/tables/main_results.csv`.

**1b. PR-AUC and calibration.** Uses the out-of-fold predictions from notebook 05, joined to the true labels by row number. PR-AUC (`average_precision_score`) is computed for each of the three repeats and averaged, and shown next to the chance level, which is the share of positive cases. `ece(y, prob)` computes the expected calibration error: predictions are put into ten boxes by probability and the average gap between predicted probability and the real share of positives is taken. Both go to `results/tables/pr_auc_calibration.csv`. A 2×2 calibration plot (one line per model) is saved as `fig_calibration`.

**2. Baseline: the scoring rule itself.** For each group, adds up A1–A10, applies the cut-off and compares the result with the label. No learning is involved. The markdown below explains why the rule is right every time and what that means for reading the model scores.

**2b. Sanity checks.** Two controls that show the perfect scores come from the data, not from a leak in the pipeline:

- *Shuffled labels.* A plain scaled Logistic Regression is cross-validated on the real labels and again on randomly permuted labels. If anything leaked between folds the shuffled score would stay high; it should fall to about 0.5.
- *Raw-file hold-out.* The four raw downloaded files are read again with the same `read_arff()` as notebook 02, with no cleaning at all. A random 20% hold-out is split off before anything else happens, and a Logistic Regression on the ten answers only is fitted on the rest and scored on the hold-out. The total-score column is not used, because the label is made from it. The check shows that the perfect scores do not depend on the project's own cleaning or pipeline code.

The three AUCs per group go to `results/tables/sanity_checks.csv`.

**3. Spread across folds.** For ROC-AUC and recall, a 2×2 grid of horizontal box plots (one panel per group, one box per model) showing how the 15 fold scores spread. Saved as `fig_cv_roc_auc` and `fig_cv_recall`.

**4. Are the differences real?** Three tests:

- *Friedman test* per group and metric (ROC-AUC and F1): the fold scores are pivoted to a folds × models table and `friedmanchisquare()` tests whether the six models differ overall, with folds as blocks. Kendall's W is added as the effect size.
- *Nemenyi post-hoc test*: `posthoc_nemenyi_friedman()` on the same table gives a p-value for every pair of models. Drawn as a 2×2 grid of heatmaps, saved as `fig_nemenyi_roc_auc`.
- *Corrected resampled t-test*: `corrected_ttest(a, b)` implements the Nadeau–Bengio correction, inflating the variance of the fold differences by `1/n + test_frac/(1 − test_frac)` because folds from repeated cross-validation share training data. It is run for EBM and TabPFN against every other model on ROC-AUC. `holm(p)` then adjusts the nine p-values of each age group for multiple comparisons, an effect size (Cohen's d of the fold differences) is added, and the table flags pairs with adjusted p < 0.05. Saved as `results/tables/corrected_ttests.csv`. The markdown explains that Friedman and Nemenyi assume independent blocks, which folds of one dataset are not, so those two are read as a description only.

**5. Missed cases.** Sums the confusion-matrix counts over the 15 folds per group and model and computes the share of positive cases missed (false negatives). Each record appears three times because of the three repeats.

**6. Cross-source results (RQ2).** Adds an "in-source AUC" column to the cross-source table (the cross-validated ROC-AUC of the same model on its training source) so the drop can be read directly. Then a grouped bar chart of ROC-AUC per train→test pair and model, saved as `fig_cross_source`.

**7. Bias check.** Loads the out-of-fold predictions and the chosen model per group. `rates(df)` returns the number of people, the number of positive and negative cases, recall and false-positive rate at the 0.5 threshold. Predictions are joined back to the processed data by row index, ethnic groups with fewer than 20 people (60 prediction rows, because of the three repeats) are merged into "Other/Unknown", sex is labelled, and the rates are computed for every value of sex and ethnicity for the model chosen for that group. Sex and ethnicity are two separate groupings of the same people. The table is saved as `results/tables/bias_check.csv`.

**8. Answers.** Markdown only: the answers to RQ1 and RQ2 drawn from the tables above, with the numbers that support each point.

---

## 07_explainability.ipynb

Answers RQ3: which questions drive the predictions, and do SHAP, LIME and the EBM's own importances agree? All three explain the same model, an EBM with `interactions=0` (purely additive). The three methods are measured on the same test rows and on the same scale (log-odds), and everything is repeated over 10 train/test splits.

**Setup.** Imports `shap`, `LimeTabularExplainer` from lime, the EBM, SMOTENC and `RepeatedStratifiedKFold`. `CATEGORICAL` lists the positions of every feature except age, which LIME and SMOTENC both need. `PAIRS` lists the three pairs of methods that are compared. Figure style as before.

**1. Three ways of measuring importance.**

- `log_odds(ebm)` returns a small function that gives the EBM's score before it is turned into a probability. All three methods explain this same number.
- `ebm_scores(ebm, X_test)` calls `eval_terms`, which gives the EBM's own score for every input and every test row: the model's own, exact explanation.
- `shap_values(ebm, background, X_test)` builds a permutation `shap.Explainer` around the log-odds function, with up to 100 training rows as background, and returns the SHAP values for every test row.
- `lime_weights(ebm, X_train, X_test)` fits a LIME explainer in regression mode on the training data and explains every test row one at a time, returning one weight per input and row.

**Main loop.** For each group, 5 folds repeated 2 times give 10 splits. In each split the SMOTENC + EBM pipeline is fitted on the training part, the three methods are run on the same test rows, and the mean absolute effect per input is stored for each method. The loop also runs a check: the EBM scores are moved to the same starting point as SHAP (the background average) and the largest difference from the SHAP values is recorded.

**2. Is SHAP independent of the EBM?** A table of that largest difference per group. It is zero apart from rounding error, so for this additive model SHAP gives back the EBM's own numbers. Their agreement is a consistency check, not separate evidence.

**3. Importance per method and age group.** Each method is scaled to sum to 1 in every split and averaged over the splits, saved as `results/tables/feature_importance.csv`, and drawn as a 2×2 grid of heatmaps, saved as `fig_importance_by_method`.

**4. Do the methods agree?** For every group, split and pair of methods, two numbers on the ten questions only: Spearman's ρ between the two rankings and the number of questions shared by the two top-5 sets. The table reports the mean and standard deviation over the 10 splits, saved as `results/tables/explanation_agreement.csv`. A short cell estimates the chance level: two random rankings share 2.5 of their top five on average.

**5. Top questions per age group.** A table of the five highest-ranked questions per group and method, from the averaged importances. The markdown warns that the same item number is a different question in Q-CHAT-10 and the three AQ-10 versions.

**6. SHAP summary plots.** A 2×2 grid of SHAP beeswarm plots from the first split (one per group, eight features shown), where each dot is one test person and the colour is the answer value. Saved as `fig_shap_beeswarm`.

**7. Answer to RQ3.** Markdown with the findings: all ten questions carry roughly equal importance; EBM and SHAP are the same numbers and only differ in their starting point; LIME agrees with them for adolescents but is at chance level for children and adults; the rankings change from split to split; personal details hardly matter; and why the rankings describe the sample rather than clinical importance.

---

## 08_harder_settings.ipynb

Makes the task harder in two practical ways so the models can be told apart: a reduced questionnaire and noisy answers. Six models, stratified 5-fold cross-validation repeated twice, fixed hyperparameters (the values notebook 05 chose most often).

**Setup.** Same libraries as notebook 05, TabPFN imported first. `K_VALUES = [4, 6, 8]` are the reduced questionnaire sizes and `NOISE_LEVELS = [0.05, 0.10, 0.20]` the shares of answers flipped. `RERUN` works as in notebook 05.

**Helpers.**

- `get_classifier(name)` returns each model with fixed settings; `make_pipeline(name, features)` wraps it with SMOTENC (and a scaler for Logistic Regression) exactly as in notebook 05.
- `top_questions(df, k)` ranks the ten questions by their chi-square statistic against the label, computed on the training fold only, and returns the top k.
- `flip_answers(X, p, rng)` flips each answer in A1–A10 with probability p, leaving the personal details alone.
- `evaluate(model, X, y)` returns ROC-AUC, recall, accuracy and Brier score at the 0.5 threshold.

**Running both experiments.** One loop over groups and folds. In each fold the noisy test sets are made once (one per noise level, seeded by fold number) and the reduced question sets are chosen once from the training fold. Then for every model: fit on all ten questions plus details, score on the clean test fold (`setting = "questions", value = 10`) and on each noisy copy (`setting = "noise"`); then fit again on each reduced set and score on the clean test fold (`setting = "questions", value = k`, with the chosen questions recorded). Everything goes to `results/tables/harder_settings.csv`, one row per group, fold, model and setting.

**Reduced questionnaire.** Two pivot tables, ROC-AUC and recall, with groups and models as rows and 4, 6, 8, 10 questions as columns. A third table counts which questions the chi-square step chose for k = 6 across the ten folds, to show the choice is stable.

**Noisy answers.** A pivot table of ROC-AUC per group and model with the clean result (noise 0) inserted as the first column, followed by 5%, 10% and 20%.

**Figures.** `lines(frame, xlabel, title, filename)` draws a 2×2 grid, one panel per group, with one line per model. Called twice: ROC-AUC against the number of questions (`fig_reduced_questions`) and against the noise level (`fig_noise`).

**What this shows.** Markdown with the findings for both settings and how they relate to the full-questionnaire result.
