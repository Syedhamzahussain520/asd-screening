# Early Autism Screening Using Interpretable Machine Learning

Code for the MSc project *"Early Autism Screening Using Interpretable Machine Learning Models and a Web Based Decision Support Tool"*.

The project compares interpretable machine learning models for autism (ASD) screening in four age groups (toddler, child, adolescent, adult) using public questionnaire datasets, and will deliver the chosen models through a web based screening tool.

See [ABOUT.md](ABOUT.md) for the background (the problem, previous work, the research gap and how each part of the study is handled) and [NOTEBOOKS.md](NOTEBOOKS.md) for a section-by-section walk-through of the code in each notebook.

This repository is being built up stage by stage. At the moment it contains the data stage (downloading the datasets, understanding what they contain and preparing them for modelling), the exploratory data analysis, the model training and the results for RQ1 and RQ2.

## Project layout

```
asd-screening/
├── notebooks/
│   ├── 01_download_data.ipynb            download all six datasets into data/raw/
│   ├── 02_understanding_the_data.ipynb   columns, questionnaires, how the label was made
│   ├── 03_preprocessing.ipynb            cleaning and harmonising -> data/processed/
│   ├── 04_eda.ipynb                      exploratory data analysis -> results/figures/
│   ├── 05_model_training.ipynb           nested cross-validation, cross-source test, final models
│   └── 06_results.ipynb                  result tables, statistical tests, sanity and bias checks
├── data/
│   ├── raw/                              created by notebook 01 (not in the repository)
│   └── processed/                        six cleaned CSV files, one per dataset
├── results/
│   ├── figures/                          figures (PNG, sized for a two-column paper)
│   ├── tables/                           per-fold scores, predictions, result and test tables
│   └── models/                           one trained model per age group (joblib)
├── app/
│   └── data/                             summary tables for the web app (written by notebook 05)
├── requirements.txt
├── README.md
├── ABOUT.md                              background, previous work and approach
└── NOTEBOOKS.md                          what each notebook does, section by section
```

## Setup on Windows

1. Install **Python 3.11** from https://www.python.org/downloads/ and tick *Add python.exe to PATH* during installation.

2. Open *Command Prompt* (or PowerShell) in the project folder and create a virtual environment:

   ```bat
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

   In PowerShell use `.venv\Scripts\Activate.ps1` instead of `activate`. If PowerShell refuses to run the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

3. **Kaggle token.** Three of the datasets are hosted on Kaggle, which needs an API token:
   - Log in to Kaggle, open *Settings* → *API* and click **Create New Token**. This downloads `kaggle.json`.
   - Create the folder `C:\Users\<your user name>\.kaggle` and move `kaggle.json` into it.

   The UCI datasets download without an account.

4. Start Jupyter and run the notebooks in order:

   ```bat
   jupyter lab
   ```

## Running the notebooks

| Notebook | What it does |
|---|---|
| `01_download_data` | Downloads the four Thabtah ASDTests datasets (UCI and Kaggle) plus two datasets from other sources into `data/raw/` |
| `02_understanding_the_data` | Looks at the columns, the Q-CHAT-10 / AQ-10 questionnaires and checks how the class label was produced |
| `03_preprocessing` | Harmonises the six files to one schema (A1–A10 answers, age, sex, jaundice, family history), cleans ages, removes duplicates and writes `data/processed/*.csv` |
| `04_eda` | Class balance, age and score distributions, answer rates per question, question correlations and chi-square tests, saved as PNG figures in `results/figures/` |
| `05_model_training` | Compares Logistic Regression, Random Forest, XGBoost, LightGBM, EBM and TabPFN with repeated stratified 5-fold cross-validation (hyperparameters tuned inside each training fold, SMOTENC on training data only), runs the cross-source test, and saves the best model per age group to `results/models/` |
| `06_results` | Builds the result tables from the saved folds, compares the models with the scoring-rule baseline, runs two sanity checks (shuffled labels, hold-out on the raw files), the Friedman and Nemenyi tests and the corrected resampled t-test, counts missed cases, summarises the cross-source test and checks recall by sex and ethnicity |

The processed CSV files, the EDA figures, the cross-validation tables and the trained models are all included in the repository, so any notebook can be opened and read without rerunning the ones before it. Notebook 05 is the slow one; it has a `RERUN` flag at the top, and with `RERUN = False` it loads the saved tables from `results/tables/` instead of training again.

**TabPFN.** Version 2.0.9 is pinned because it is the version described in the Nature paper and downloads its weights without a login; newer releases ask you to accept a licence first. Installing it pulls in PyTorch, which is a large download. The weights are fetched the first time the model is used. Notebook 05 imports TabPFN before XGBoost and LightGBM on purpose, because loading them the other way round can crash the kernel.

## Note on the data

In the five ASDTests/Saudi datasets the class label is exactly "questionnaire score above the cut-off" (notebook 02 checks this for every row). This matters for the modelling stage: the score column must be dropped, and even then a model can reproduce the label by adding up the ten answers. The Kaggle adult dataset does not follow the rule exactly (about 80 % agreement).

## Data sources

| Dataset | Source |
|---|---|
| Toddlers (Q-CHAT-10) | https://www.kaggle.com/datasets/fabdelja/autism-screening-for-toddlers |
| Children (AQ-10) | https://archive.ics.uci.edu/dataset/419 |
| Adolescents (AQ-10) | https://archive.ics.uci.edu/dataset/420 |
| Adults (AQ-10) | https://archive.ics.uci.edu/dataset/426 |
| Saudi toddlers (Q-CHAT-10) | https://www.kaggle.com/datasets/asdpredictioninsaudi/asd-screening-data-for-toddlers-in-saudi-arabia |
| Kaggle adults (AQ-10) | https://www.kaggle.com/datasets/shivamshinde123/autismprediction |

The UCI datasets are released under CC BY 4.0. The Kaggle pages do not state a licence, so those datasets are used for research only and credited to their authors.
