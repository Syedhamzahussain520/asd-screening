# 3. Methods

**Q1. What is data leakage?**
Data leakage means the model gets information during training that it should not have. Then the test result looks better than it really is.
Example: a student who sees the exam answers before the exam gets full marks, but has not learned anything.

**Q2. What kinds of leakage are possible in this data?**
1. Giving the total score to the model. The label is made from it.
2. Making extra training records (oversampling) before splitting the data, so copies of test records end up in training.
3. Choosing the model settings while looking at the test data.
4. The same record appearing in both training and test data.

**Q3. How is leakage controlled in this project?**
- The total score is removed.
- Duplicate records are removed.
- SMOTENC, scaling and tuning all happen inside the training part of each fold only.
- A baseline and two sanity checks are reported.

**Q4. Is removing the total score enough?**
No. The model still gets the ten answers, and it can add them up by itself. That is why the project also uses harder tests.

**Q5. What is cross-validation?**
A way to test a model fairly. The data is cut into parts. The model learns from some parts and is tested on a part it has not seen. This is repeated so that every part is used for testing once.
Example: with 5 parts (5 folds), the model trains on 4 parts and is tested on the 5th. This is done 5 times.

**Q6. Which cross-validation is used here?**
Stratified 5-fold cross-validation, repeated 3 times. That gives 15 test folds for every model, and every model uses the same folds.

**Q7. What does "stratified" mean?**
Each fold keeps the same share of positive and negative cases as the full data.
Example: if 27% of adults are positive, every fold also has about 27% positive.

**Q8. Why repeat it three times?**
One split can be lucky or unlucky. Repeating gives a more stable average and shows how much the result changes.

**Q9. What is hyperparameter tuning?**
Hyperparameters are settings of a model that we choose before training. Tuning means trying several values and keeping the best one.
Example: for Random Forest, the number of trees can be 200 or 500. Both are tried and the better one is kept.

**Q10. What is grid search?**
Trying every combination of the chosen values.
Example: 2 values for the number of trees and 3 values for the depth give 6 combinations.

**Q11. What is nested cross-validation?**
Tuning is done with a second, inner cross-validation inside each training fold (here 3 folds). The outer test fold is never used for tuning. This keeps the test honest.

**Q12. What is SMOTE?**
Synthetic Minority Over-sampling Technique. It makes new, similar records for the smaller class, so that both classes have the same size during training.
Example: 100 "no" records and 40 "yes" records. SMOTE makes 60 new "yes" records, so both have 100.

**Q13. What is SMOTENC and why is it used instead of SMOTE?**
SMOTE for Nominal and Continuous. Normal SMOTE would make answers such as 0.4, which is not possible for a yes or no question. SMOTENC keeps those answers as 0 or 1.

**Q14. Why is SMOTENC put inside the pipeline?**
A pipeline is a chain of steps that run in order. When SMOTENC is one of the steps, it only sees the training part of a fold. No made-up record can reach the test data.

**Q15. What is scaling and which model needs it?**
Scaling puts all inputs on a similar range. Example: age goes from 12 to 36, while answers are 0 or 1. Only Logistic Regression needs scaling here.

**Q16. What are the six models?**
1. Logistic Regression (LR): a simple model that adds up weighted inputs.
2. Random Forest (RF): many decision trees that vote.
3. XGBoost: trees built one after another, each fixing the mistakes of the ones before.
4. LightGBM: a faster kind of the same idea.
5. EBM: Explainable Boosting Machine. It learns one curve for each input and adds them up. A person can read it.
6. TabPFN: Tabular Prior-data Fitted Network. A model that was trained in advance on millions of made-up tables. It needs no training and no tuning on new data.

**Q17. What is a decision tree?**
A model that asks a chain of yes or no questions.
Example: "Is A1 equal to 1? If yes, is A5 equal to 1?" and so on, until it gives an answer.

**Q18. Why were these six models chosen?**
- Logistic Regression: the simplest baseline, and it can copy a "sum above a cut-off" rule exactly.
- Random Forest: the most common model in earlier autism papers.
- XGBoost and LightGBM: usually the strongest models on tables of data.
- EBM: accurate and readable.
- TabPFN: a recent model made for small datasets.

**Q19. Why not deep learning (neural networks)?**
The datasets are small tables of yes and no answers. On such data, deep learning usually does not beat tree models, and it is harder to tune and explain.

**Q20. What does "interpretable" mean?**
A person can see how the model reaches its answer.
Example: in an EBM you can see that answering "yes" to question 5 adds a certain amount to the score.

**Q21. What is a "black box" model?**
A model whose inside working is too complex for a person to follow. Example: a forest of 500 trees.

**Q22. What is the scoring-rule baseline?**
No machine learning at all. Just add the ten answers and compare with the cut-off. It is right for 100% of records, because it is how the label was made.

**Q23. What are the two sanity checks?**
1. Shuffled labels: the labels are mixed up at random and the model is trained again. If the code is correct, the score must fall to about 0.5, which is the same as guessing.
2. Raw files: a plain Logistic Regression is trained on the raw downloaded files with no cleaning. Only the ten answers are used, not the total score. The test part is set aside before anything else.

**Q24. What question does the second sanity check answer?**
"Does a simple model still get everything right when none of my own cleaning or pipeline code is used?" The answer is yes. So the perfect scores come from the data, not from my code.

**Q25. What is the cross-source test?**
The model is trained on all of one dataset and tested on all of another dataset from a different source. It is done in both directions, for toddlers and for adults.

**Q26. What are the two harder settings?**
1. Reduced questionnaire: the model only gets the 4, 6 or 8 most useful questions and must still predict the full result.
2. Noisy answers: 5%, 10% or 20% of the test answers are flipped at random (0 becomes 1, or 1 becomes 0). This is like a person who misreads a question.

**Q27. How are the "most useful" questions chosen?**
With the chi-square test on the training fold only. Chi-square measures how strongly an answer is related to the label. A bigger value means a stronger relation.

**Q28. What is the fairness check?**
Recall and the false-positive rate are compared between sexes and between ethnic groups, to see if the model makes more mistakes for one group.

**Q29. Which software was used?**
Python 3.11, JupyterLab, pandas, NumPy, scikit-learn, imbalanced-learn, XGBoost, LightGBM, InterpretML (for EBM), TabPFN, SHAP, LIME, matplotlib, seaborn and Streamlit.

**Q30. Can the results be repeated?**
Yes. The random seed is fixed at 42 everywhere, the library versions are listed, and the notebooks run in order from 01 to 08.
