# Early Autism Screening Using Interpretable Machine Learning

Code for the MSc project *"Early Autism Screening Using Interpretable Machine Learning Models and a Web Based Decision Support Tool"*.

The project compares interpretable machine learning models for autism (ASD) screening in four age groups (toddler, child, adolescent, adult) using public questionnaire datasets, and delivers the chosen models through a web based screening tool.

See [ABOUT.md](ABOUT.md) for the background (the problem, previous work, the research gap and how each part of the study is handled) and [NOTEBOOKS.md](NOTEBOOKS.md) for a section-by-section walk-through of the code in each notebook.

The repository contains the full research pipeline (data download, understanding and preprocessing, exploratory analysis, model training, results, explainability and the harder-setting experiments) and the Streamlit web app that serves the chosen models.

## Project layout

```
asd-screening/
├── notebooks/
│   ├── 01_download_data.ipynb            download all six datasets into data/raw/
│   ├── 02_understanding_the_data.ipynb   columns, questionnaires, how the label was made
│   ├── 03_preprocessing.ipynb            cleaning and harmonising -> data/processed/
│   ├── 04_eda.ipynb                      exploratory data analysis -> results/figures/
│   ├── 05_model_training.ipynb           nested cross-validation, cross-source test, final models
│   ├── 06_results.ipynb                  result tables, statistical tests, sanity and bias checks
│   ├── 07_explainability.ipynb           SHAP vs LIME vs EBM (RQ3)
│   └── 08_harder_settings.ipynb          reduced questionnaire and noisy answers
├── data/
│   ├── raw/                              created by notebook 01 (not in the repository)
│   └── processed/                        six cleaned CSV files, one per dataset
├── results/
│   ├── figures/                          figures (PNG, sized for a two-column paper)
│   ├── tables/                           per-fold scores, predictions, result and test tables
│   └── models/                           one trained model per age group (joblib)
├── app/                                  Streamlit web app (runs on its own)
│   ├── Home.py                           start page
│   ├── pages/                            1_Screening.py, 2_Model_Performance.py, 3_About.py
│   ├── questions.py                      questionnaire wording and scoring
│   ├── models/                           trained models used by the app (written by notebook 05)
│   └── data/                             summary tables shown in the app (written by notebooks 05 and 08)
├── .streamlit/config.toml                Streamlit settings
├── requirements.txt                      web app dependencies (what Streamlit Cloud installs)
├── requirements-research.txt             full environment for the notebooks
├── README.md
├── ABOUT.md                              background, previous work and approach
└── NOTEBOOKS.md                          what each notebook does, section by section
```

## Setup on Windows

Everything below was written for Windows 10 or 11. Each command is typed into *Command Prompt* unless it says PowerShell.

### 1. Install the tools

- **Python 3.11** from https://www.python.org/downloads/ (choose a 3.11.x release, 64-bit). On the first screen of the installer tick **Add python.exe to PATH**. Other versions of Python can stay installed; the `py -3.11` command below picks the right one.
- **Git for Windows** from https://git-scm.com/download/win, with the default options. This is only needed to clone the repository; downloading it as a zip works too (see step 2).
- A web browser for Jupyter and the app.

Check the installation by opening a new Command Prompt and typing:

```bat
py -3.11 --version
git --version
```

### 2. Get the code

The repository is private, so you need to be signed in to GitHub with an account that has access. Then either

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/Syedhamzahussain520/asd-screening.git
cd asd-screening
```

(Git asks you to sign in to GitHub in a browser window the first time), or on the repository page click **Code → Download ZIP**, unzip it, and open Command Prompt inside the unzipped `asd-screening` folder. A quick way to open a Command Prompt in a folder is to type `cmd` in the address bar of File Explorer while that folder is open.

Keep the folder path short and without special characters (for example `C:\Users\<you>\Documents\asd-screening`); very long paths can make `pip` fail on Windows.

### 3. Create the Python environment

Inside the project folder:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-research.txt
```

The prompt starts with `(.venv)` when the environment is active. Installation downloads a few hundred megabytes (PyTorch, needed by TabPFN, is the largest part), so it takes a while on a slow connection.

**Every time you open a new Command Prompt** you have to activate the environment again with `.venv\Scripts\activate` before running Jupyter or the app. `deactivate` leaves it.

If you use **PowerShell** instead of Command Prompt, activate with `.venv\Scripts\Activate.ps1`. If PowerShell refuses to run the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, answer `Y`, and try again.

### 4. Kaggle token (only needed for notebook 01)

Three datasets are hosted on Kaggle, which needs an API token. The UCI datasets download without an account.

1. Log in to https://www.kaggle.com, open *Settings* → *API* and click **Create New Token**. This downloads a file called `kaggle.json`.
2. Create the folder `.kaggle` in your user folder. File Explorer does not accept folder names that start with a dot, so create it from Command Prompt:

   ```bat
   mkdir %USERPROFILE%\.kaggle
   move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\
   ```

   The file must end up at `C:\Users\<your user name>\.kaggle\kaggle.json`.

Keep this file private; it is listed in `.gitignore` so it cannot be committed by accident.

### 5. Start Jupyter

With the environment active, from the project folder:

```bat
jupyter lab
```

A browser tab opens with JupyterLab. In the file browser on the left open the `notebooks` folder and double-click a notebook. The kernel should show as **Python 3 (ipykernel)**; because Jupyter was started from the environment, that is the project environment. To run a whole notebook use the menu *Run → Run All Cells*. The notebooks use paths relative to the `notebooks` folder, so Jupyter must be started from the project folder as shown, not from somewhere else.

Close Jupyter with `Ctrl+C` in the Command Prompt window (twice if it asks for confirmation).

### 6. Common problems

| Message | Cause and fix |
|---|---|
| `'py' is not recognized` or `'pip' is not recognized` | Python was installed without *Add to PATH*. Re-run the installer, choose *Modify* and tick the PATH option, then open a new Command Prompt. |
| `'jupyter' is not recognized` or `'streamlit' is not recognized` | The environment is not active. Run `.venv\Scripts\activate` first. |
| `OSError: Could not find kaggle.json` | The token is not at `C:\Users\<you>\.kaggle\kaggle.json`. Check the folder name and that the file was not renamed to `kaggle.json.json`. |
| `401 Unauthorized` from Kaggle | The token has expired or the dataset's terms were not accepted on the Kaggle website. Create a new token, and open each Kaggle dataset page once while logged in. |
| `DLL load failed` when importing LightGBM or XGBoost | Install the *Microsoft Visual C++ Redistributable* (x64) from https://aka.ms/vs/17/release/vc_redist.x64.exe and restart. |
| `pip` fails with a *path too long* error | Move the project to a shorter path, or enable long paths in Windows (*Edit group policy* → *Computer Configuration* → *Administrative Templates* → *System* → *Filesystem* → *Enable Win32 long paths*). |
| The kernel dies while running notebook 05 or 08 | Make sure the TabPFN import is still the first import in the notebook, and that no other notebook kernel is running at the same time. Restart the kernel and run again. |

## Running the notebooks

| Notebook | What it does |
|---|---|
| `01_download_data` | Downloads the four Thabtah ASDTests datasets (UCI and Kaggle) plus two datasets from other sources into `data/raw/` |
| `02_understanding_the_data` | Looks at the columns, the Q-CHAT-10 / AQ-10 questionnaires and checks how the class label was produced |
| `03_preprocessing` | Harmonises the six files to one schema (A1–A10 answers, age, sex, jaundice, family history), cleans ages, removes duplicates and writes `data/processed/*.csv` |
| `04_eda` | Class balance, age and score distributions, answer rates per question, question correlations and chi-square tests, saved as PNG figures in `results/figures/` |
| `05_model_training` | Compares Logistic Regression, Random Forest, XGBoost, LightGBM, EBM and TabPFN with repeated stratified 5-fold cross-validation (hyperparameters tuned inside each training fold, SMOTENC on training data only), runs the cross-source test, and saves the best model per age group to `results/models/` |
| `06_results` | Builds the result tables from the saved folds, compares the models with the scoring-rule baseline, runs two sanity checks (shuffled labels, hold-out on the raw files), the Friedman and Nemenyi tests and the corrected resampled t-test, counts missed cases, summarises the cross-source test and checks recall by sex and ethnicity |
| `07_explainability` | Trains an additive EBM per age group, explains the same predictions with SHAP, LIME and the EBM's own term importances, and measures how far the three rankings of the ten questions agree |
| `08_harder_settings` | Re-compares the six models when only the 4, 6 or 8 most informative questions are available, and when 5–20% of the test answers are flipped at random |

The processed CSV files, the EDA figures, the cross-validation tables and the trained models are all included in the repository, so any notebook can be opened and read without rerunning the ones before it. Notebooks 05 and 08 are the slow ones; each has a `RERUN` flag at the top, and with `RERUN = False` it loads its saved table from `results/tables/` instead of training again.

**TabPFN.** Version 2.0.9 is pinned because it is the version described in the Nature paper and downloads its weights without a login; newer releases ask you to accept a licence first. Installing it pulls in PyTorch, which is a large download. The weights are fetched the first time the model is used. Notebooks 05 and 08 import TabPFN before XGBoost and LightGBM on purpose, because loading them the other way round can crash the kernel.

## The web app

The app has three pages. **Screening** asks the questionnaire for the chosen age group plus age, sex, jaundice and family history, gives a probability of ASD traits with the questionnaire score, and explains the result with SHAP values showing which answers moved the estimate up or down. **Model Performance** shows the cross-validation, cross-source and harder-setting results. **About** explains the data, the method and the limitations. Nothing entered is stored.

Run it locally from the project folder, with the virtual environment active:

```bat
streamlit run app/Home.py
```

The first time Streamlit runs it asks for an email address in the terminal; just press Enter. The browser then opens at `http://localhost:8501`; if it does not, open that address yourself. Stop the app with `Ctrl+C` in the Command Prompt window. The research environment above already contains everything the app needs. To run the app on its own, for example on another machine, install `app/requirements.txt` instead; it leaves out TabPFN and PyTorch, which the deployed models do not need.

To deploy on [Streamlit Community Cloud](https://share.streamlit.io): sign in with GitHub, choose **New app**, pick this repository and branch `main`, set the main file to `app/Home.py`, and under *Advanced settings* choose **Python 3.11**. Streamlit Cloud installs `requirements.txt` from the repository root, which holds only what the app needs. Package versions are pinned to the training environment so the saved models load with the same scikit-learn version. If the app is created on Python 3.14, where those versions have no pre-built packages, the file falls back to newer numpy and scikit-learn releases; the models load and give the same predictions, with a version warning in the log.

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
