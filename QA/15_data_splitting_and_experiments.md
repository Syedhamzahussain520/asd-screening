# 15. How the data was split and how the experiments were run

**Q1. Why do we split data at all?**
To test a model on records it has not seen. Otherwise we only measure how well it remembers.
Example: a student should be tested with new questions, not with the ones used in class.

**Q2. How was the data split in the main experiment?**
Each age group was split with stratified 5-fold cross-validation, repeated 3 times.
Example for adults (691 records): each fold has about 138 records. The model trains on about 553 and is tested on about 138. This is done 15 times.

**Q3. Was there one fixed train set and test set?**
No. Every record is used for testing three times (once in each repeat) and for training the rest of the time.

**Q4. How was the data split for tuning?**
Inside each training fold there is a second split into 3 folds. The settings are chosen there. The outer test fold is never used for this.

**Q5. How was the data split for the cross-source test?**
No split. The model is trained on all of one dataset and tested on all of the other.
Example: train on all 973 Thabtah toddlers, test on all 443 Saudi toddlers. Then the other way round.

**Q6. How was the data split for the harder settings?**
5 folds repeated 2 times, which gives 10 test folds. The settings are fixed (no tuning) to save time.

**Q7. How was the data split for the explanation analysis?**
5 folds repeated 2 times, which gives 10 splits. In each one the EBM is trained on 80% and explained on the other 20%.

**Q8. How was the data split for the raw-file sanity check?**
The rows are mixed at random. The first 20% is set aside as the test part before anything else is done. The model trains on the other 80%.

**Q9. Is each age group mixed with the others?**
No. Each age group is modelled on its own, because the questionnaires are different.

**Q10. What are the steps of one experiment run, in order?**
1. Take the cleaned data of one age group.
2. Split it into folds.
3. For each fold: balance the training part with SMOTENC, tune the settings inside the training part, train the model.
4. Predict the test part and compute the measures.
5. Average the measures over the 15 folds.

**Q11. Which experiments were run in total?**
1. Main comparison: 6 models, 4 age groups, 15 folds.
2. Scoring-rule baseline.
3. Two sanity checks.
4. Cross-source test: 4 train and test pairs, 6 models.
5. Reduced questionnaire: 4, 6 and 8 questions.
6. Noisy answers: 5%, 10% and 20%.
7. Explanation agreement: 3 methods, 10 splits.
8. Fairness check by sex and ethnicity.

**Q12. Why does every model use the same folds?**
So the comparison is fair. Each model is tested on exactly the same people.

**Q13. Where does SMOTENC run in this process?**
Only on the training part of each fold. The test part always holds real records only.

**Q14. How do you make sure no test information reaches training?**
All steps that learn from data (SMOTENC, scaling, tuning, choosing the top questions) are done inside the training part. Duplicate records were removed before any split.

**Q15. In the noise test, is noise added to the training data?**
No. The models train on clean data. Noise is added to the test answers only.
