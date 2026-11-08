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

**1. Main results.** Groups the folds by age group and model, takes mean and standard deviation of every metric, formats them as "mean ± sd", orders the rows as `GROUPS × MODEL_NAMES` and saves `results/tables/main_results.csv`.

**2. Baseline: the scoring rule itself.** For each group, adds up A1–A10, applies the cut-off and compares the result with the label. No learning is involved. The markdown below explains why the rule is right every time and what that means for reading the model scores.

**2b. Sanity checks.** Two controls that show the perfect scores come from the data, not from a leak in the pipeline:

- *Shuffled labels.* A plain scaled Logistic Regression is cross-validated on the real labels and again on randomly permuted labels. If anything leaked between folds the shuffled score would stay high; it should fall to about 0.5.
- *Raw-file hold-out.* The four raw downloaded files are read again with the same `read_arff()` as notebook 02, with no cleaning at all. A random 20% hold-out is split off before anything else happens, and a Logistic Regression on the ten answers only is fitted on the rest and scored on the hold-out.

The three AUCs per group go to `results/tables/sanity_checks.csv`.

**3. Spread across folds.** For ROC-AUC and recall, a 2×2 grid of horizontal box plots (one panel per group, one box per model) showing how the 15 fold scores spread. Saved as `fig_cv_roc_auc` and `fig_cv_recall`.

**4. Are the differences real?** Three tests:

- *Friedman test* per group and metric (ROC-AUC and F1): the fold scores are pivoted to a folds × models table and `friedmanchisquare()` tests whether the six models differ overall, with folds as blocks.
- *Nemenyi post-hoc test*: `posthoc_nemenyi_friedman()` on the same table gives a p-value for every pair of models. Drawn as a 2×2 grid of heatmaps, saved as `fig_nemenyi_roc_auc`.
- *Corrected resampled t-test*: `corrected_ttest(a, b)` implements the Nadeau–Bengio correction, inflating the variance of the fold differences by `1/n + test_frac/(1 − test_frac)` because folds from repeated cross-validation share training data. It is run for EBM and TabPFN against every other model on ROC-AUC, and the table flags pairs with p < 0.05. The markdown explains why the plain Friedman p-values are a little too small.

**5. Missed cases.** Sums the confusion-matrix counts over the 15 folds per group and model and computes the share of positive cases missed (false negatives). Each record appears three times because of the three repeats.

**6. Cross-source results (RQ2).** Adds an "in-source AUC" column to the cross-source table (the cross-validated ROC-AUC of the same model on its training source) so the drop can be read directly. Then a grouped bar chart of ROC-AUC per train→test pair and model, saved as `fig_cross_source`.

**7. Bias check.** Loads the out-of-fold predictions and the chosen model per group. `rates(df)` returns the number of people, recall and false-positive rate at the 0.5 threshold. Predictions are joined back to the processed data by row index, ethnic groups with fewer than 20 people (60 prediction rows, because of the three repeats) are merged into "Other/Unknown", sex is labelled, and the rates are computed for every value of sex and ethnicity for the model chosen for that group.

**8. Answers.** Markdown only: the answers to RQ1 and RQ2 drawn from the tables above, with the numbers that support each point.
