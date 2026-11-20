# 2. Data

**Q1. How many datasets are used?**
Six public datasets. Four are the main datasets, one for each age group. Two more are used only for the cross-source test.

**Q2. What are the four main datasets?**
They were shared by Fadi Thabtah and collected with a mobile app called ASDTests.
- Toddlers (12 to 36 months), from Kaggle, 1,054 records.
- Children (4 to 11 years), from the UCI repository, 292 records.
- Adolescents (12 to 16 years), from the UCI repository, 104 records.
- Adults (17 years and over), from the UCI repository, 704 records.

**Q3. What are the two extra datasets?**
- Toddlers from Saudi Arabia, collected with an online form in Arabic, 506 records.
- Adults from a Kaggle competition, 800 records. This one is synthetic. It was generated from the UCI adult data.

**Q4. What does UCI mean?**
University of California, Irvine. It has a well-known free library of datasets for machine learning.

**Q5. What is in one record (one row)?**
Ten answers scored 0 or 1 (called A1 to A10), age, sex, ethnicity, jaundice at birth, family history of autism, the total score and the class label.

**Q6. What is the Q-CHAT-10?**
Quantitative Checklist for Autism in Toddlers, short form with 10 questions. A parent answers it for a toddler. Example question: "Does your child look at you when you call his or her name?"

**Q7. What is the AQ-10?**
Autism Spectrum Quotient, short form with 10 questions. There is one version for children, one for adolescents and one for adults. Example (adult): "I often notice small sounds when others do not."

**Q8. How is one answer scored?**
Each answer becomes 1 if it points towards autistic traits, and 0 if it does not. Example: for the adult question above, "agree" gives 1 point.

**Q9. How is the label made?**
The ten scores are added up. If the total is above the cut-off, the label is "ASD traits".
- Q-CHAT-10 (toddlers): a score above 3.
- AQ-10 (children, adolescents, adults): a score above 6.
Example: an adult with a score of 7 is labelled positive. An adult with a score of 6 is labelled negative.

**Q10. How do you know the label is made this way?**
The dataset description says so, and I checked it for every row. The rule matches the label in 100% of records in the four main datasets and in the Saudi data. In the Kaggle adult data it matches in 80.5% of records.

**Q11. Why is this the most important finding?**
Because it means the label is not a doctor's diagnosis. It is only the questionnaire result. A model that sees the ten answers can simply learn to add them up.

**Q12. What cleaning was done?**
1. All six files were given the same column names.
2. Exact duplicate records were removed.
3. Records with a missing age, or an age outside the range of the questionnaire, were removed.
4. Ethnicity spellings were fixed.
5. Yes and no values were changed to 1 and 0.

**Q13. How many duplicates were removed and why?**
81 for toddlers, 8 for children, 3 for adolescents and 10 for adults. If the same record is in both the training part and the test part, the results look better than they really are.

**Q14. What strange ages were found?**
One adult had a recorded age of 383. The Kaggle "adult" data had 194 records with ages from 2 to 89 that were outside the adult range or missing.

**Q15. How many records are left after cleaning?**
- Toddler: 973 (70.9% positive)
- Child: 280 (47.5% positive)
- Adolescent: 101 (59.4% positive)
- Adult: 691 (26.8% positive)
- Toddler, Saudi: 443 (69.1% positive)
- Adult, Kaggle: 606 (21.3% positive)

**Q16. Which columns are given to the models?**
The ten answers, age, sex, jaundice at birth and family history of autism. That is 14 inputs.

**Q17. Which columns are not given to the models, and why?**
- The total score: the label is made from it, so it would give the answer away.
- Ethnicity: kept only for the fairness check.
- Country, relation, "used the app before" and the age band: they do not describe the person or they never change.

**Q18. What is class imbalance, and is it a problem here?**
It means one class has many more records than the other. Here 71% of toddlers are positive but only 27% of adults. It is handled with SMOTENC during training.

**Q19. Which group is the hardest and why?**
Adolescents. There are only 101 records, so each test fold has about 20 people and the results change a lot from fold to fold.

**Q20. Is any personal data stored or collected by the project?**
No. Only public, anonymous datasets are used. The web tool does not store any answer.

**Q21. What did the exploratory data analysis (EDA) show?**
- The classes are unbalanced in different directions in different age groups.
- The two classes never overlap at the cut-off in the score chart.
- Some questions separate the classes more strongly than others.
- Age, sex, jaundice and family history are only weakly related to the label.
