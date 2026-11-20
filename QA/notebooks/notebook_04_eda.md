# Notebook 04: Exploratory data analysis (EDA)

**Q1. What is EDA?**
Exploratory data analysis. Looking at the data with tables and charts before building models, to understand it.

**Q2. What does this notebook do?**
It makes seven kinds of charts and tables for the four main datasets after cleaning. The figures are saved in `results/figures/`.

**Q3. Section "Figure style": why set a style?**
So every figure has the same colours, font and size, and fits the width of a column in the IEEE paper (3.5 inches).

**Q4. Section 1 "Class balance": what does it show?**
How many records are in each class. Toddlers are 71% positive, children about 48%, adolescents 59% and adults only 27%.

**Q5. Why does class balance matter?**
A model can look accurate just by guessing the bigger class. That is why SMOTENC is used and why recall and PR-AUC are reported.

**Q6. Section 2 "Age": what does it show?**
The age of the people in each class. Age does not separate the two classes in a clear way.

**Q7. Section 3 "Questionnaire score": what does it show?**
A bar chart of the total score, coloured by class, with a dashed line at the cut-off. The two colours never overlap.

**Q8. What does that chart prove?**
That the label is exactly "score above the cut-off". It is the same finding as in notebook 02, shown as a picture.

**Q9. Section 4 "Answers by class": what does it show?**
For each question, the share of people who scored 1, split by class.
Example: for adults, questions 6 and 9 are scored 1 much more often by the positive class than by the negative class.

**Q10. Section 5 "Chi-square test": what is it and what does it show?**
Chi-square measures how strongly an answer is related to the label. A bigger number means a stronger relation. The chart shows this number for every input and age group.

**Q11. What did the chi-square test show about personal details?**
Sex, jaundice and family history are only weakly related to the label.

**Q12. Where is the chi-square ranking used again?**
In notebook 08, to choose the 4, 6 or 8 most useful questions.

**Q13. Section 6 "Relationships between questions": what does it show?**
The correlation between the ten answers. Correlation says how much two answers go together. For 0 and 1 data it is called the phi coefficient.

**Q14. Section 7 "Personal details": what does it show?**
The percent with ASD traits in each category.
Example: the percent among males and among females.

**Q15. What are the main points of the summary?**
The classes are unbalanced in different directions, the score separates the classes perfectly, the questions differ in strength, and the personal details matter little.
