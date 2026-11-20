# Notebook 03: Preprocessing (cleaning the data)

**Q1. What does this notebook do?**
It cleans the six datasets and saves them in `data/processed/`.

**Q2. What is preprocessing?**
Getting the data ready before a model can use it.
Example: changing "yes" and "no" into 1 and 0.

**Q3. Section 1 "One schema for all datasets": what is a schema?**
The list of column names and their meaning. The six files use different names, so they are all renamed to the same ones.
Example: `Age_Mons` in the toddler file and `Age` in the Saudi file both become `age`. The misspelt `jundice` becomes `jaundice`, and `austim` becomes `family_asd`.

**Q4. What does the function `yes_no` do?**
It changes "yes" or "1" into 1, and everything else into 0.

**Q5. What does the function `harmonise` do?**
It builds one clean table for a dataset: the ten answers A1 to A10, age, male (1 or 0), jaundice, family_asd, ethnicity, score and the label `asd`.

**Q6. Why is the `score` column kept if the models must not use it?**
It is kept only for analysis, for example for the score chart in notebook 04. It is never given to a model.

**Q7. Section 2 "Duplicates": what was done?**
Rows that are exact copies of another row were removed: 81 for toddlers, 8 for children, 3 for adolescents and 10 for adults.

**Q8. Why remove duplicates?**
If the same record lands in both the training part and the test part, the model has already seen the test record. Results would look too good.

**Q9. Section 3 "Age": what was done?**
Rows with a missing age, or an age outside the range of the questionnaire, were removed.
Example: the allowed range for adults is 17 to 100 years. One adult had an age of 383, which is clearly a mistake.

**Q10. What are the allowed age ranges?**
Toddlers 12 to 36 months, children 4 to 11 years, adolescents 12 to 16 years, adults 17 to 100 years.

**Q11. Section 4 "Ethnicity": what was done?**
The spellings were fixed so one group is not counted as two.
Example: "Others" and "others" both become "Other". Missing values become "Unknown".

**Q12. Is ethnicity given to the models?**
No. It is only used later for the fairness check.

**Q13. Section 5 "Model inputs": which columns are the inputs?**
A1 to A10, age, male, jaundice and family_asd. That is 14 columns.

**Q14. Section 6 "Result and save": what is saved?**
Six CSV files, one for each dataset. A summary table shows the rows before and after cleaning and the percent with ASD traits.
Example: toddlers go from 1,054 to 973 rows, with 70.9% positive.

**Q15. Why is there no scaling or SMOTE in this notebook?**
Those steps learn from the data. They must only see training data, so they are done later, inside the model pipeline.
