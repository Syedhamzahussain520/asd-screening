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
