# Notebook 02: Understanding the data

**Q1. What does this notebook do?**
It looks at what one row means, what each column holds, and how the class label was made. Nothing is changed here.

**Q2. Why is this notebook the most important one?**
It shows that the label is made from the questionnaire score. The rest of the project follows from this.

**Q3. Section 1 "Loading the raw files": what is ARFF?**
Attribute-Relation File Format. It is a text file used by UCI. The column names are listed at the top, and the rows below are normal comma-separated values.

**Q4. Why did you write your own `read_arff` function?**
The usual reader in `scipy` fails on these files. The small function reads the column names from the lines that start with `@attribute` and then reads the rows as CSV.

**Q5. What does `na_values="?"` mean?**
In these files a missing value is written as a question mark. This tells pandas to treat "?" as missing.

**Q6. What does the first table show?**
The number of rows and columns of each dataset.
Example: the toddler file has 1,054 rows.

**Q7. Section 2 "The screening questionnaires": what is explained?**
What the Q-CHAT-10 and the AQ-10 are, who answers them, and how each answer becomes 0 or 1.

**Q8. Section 3 "Columns": what was found about missing values?**
Missing values only appear in `age`, `ethnicity` and `relation`. Only `age` matters for the models.

**Q9. Section 4 "How the class label was made": what is checked?**
For every row the ten answers are added up and compared with the cut-off (above 3 for toddlers, above 6 for the others). The result is compared with the label in the file.

**Q10. What did the check find?**
The rule matches the label in 100% of rows in the four main datasets and in the Saudi data. In the Kaggle adult data it matches in 80.5%.

**Q11. Can you give an example of the rule?**
An adult answers so that 7 of the 10 answers score 1. The total is 7. 7 is above 6, so the label is "ASD traits". With a total of 6 the label would be "no".

**Q12. What does the cross table for adults show?**
The label against the total score. All records with a score of 6 or less are "NO", and all with 7 or more are "YES". There is no overlap.

**Q13. What does this mean for the models?**
A model that gets the ten answers can add them up itself. So near-perfect accuracy is expected, and it does not show that the model can diagnose autism.

**Q14. Why does the Kaggle adult data only match in 80.5% of rows?**
That dataset is synthetic. It was generated from the UCI data, and its labels do not follow the rule exactly.

**Q15. Section 5 "Summary": what are the key points?**
There are four main datasets and two second-source datasets, the label is the score above a cut-off, and the total score must not be given to the models.
