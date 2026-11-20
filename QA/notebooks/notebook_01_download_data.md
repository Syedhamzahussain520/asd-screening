# Notebook 01: Downloading the datasets

**Q1. What does this notebook do?**
It downloads the six datasets and puts each one in its own folder under `data/raw/`.

**Q2. Why is there a notebook only for downloading?**
So that anyone can get exactly the same files and repeat the work. The raw files are not stored on GitHub.

**Q3. Section "Kaggle access": what is it for?**
Three datasets are on Kaggle, and Kaggle needs a personal key (a token) to download. The section explains how to get the file `kaggle.json`.
Example: on Kaggle, open Settings, then API, then "Create New Token".

**Q4. What are the two lists `UCI` and `KAGGLE` in the first code cell?**
They say which dataset goes into which folder.
Example: `"child"` is linked to the UCI page number 419, and `"toddler"` to the Kaggle dataset `fabdelja/autism-screening-for-toddlers`.

**Q5. Section "UCI datasets": how are they downloaded?**
With the `requests` library. Each dataset comes as a zip file. The notebook opens the zip in memory and saves the files inside it.

**Q6. What is in a UCI zip file?**
An `.arff` file with the data and a Word document that describes the data.

**Q7. What does `timeout=60` mean?**
The download stops waiting after 60 seconds, so the notebook does not hang forever if the website is down.

**Q8. What does `r.raise_for_status()` do?**
It stops the notebook with an error if the download failed. Without it a broken file could be saved without anyone noticing.

**Q9. Section "Kaggle datasets": how are they downloaded?**
With the official Kaggle library. `api.authenticate()` reads the key, and `dataset_download_files(..., unzip=True)` downloads and unpacks each dataset.

**Q10. Section "What was downloaded": why list the files?**
To check that nothing is missing. It prints every file with its size.

**Q11. Why is only `train.csv` used from the Kaggle adult data?**
That dataset came from a competition. Its `test.csv` has no labels, so it cannot be used to check a model.

**Q12. What should I say if asked about the licence of the data?**
The UCI datasets are released under CC BY 4.0. The Kaggle pages do not state a licence, so those datasets are used for research only and their authors are credited.

**Q13. What can go wrong when running this notebook?**
The most common problem is a missing or wrongly placed `kaggle.json` file. The README explains where to put it.
