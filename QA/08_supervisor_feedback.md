# 8. Supervisor feedback and how each point was handled

The supervisor gave ten points on the paper. This file lists each one, what it means in easy words, and what was done.

**Q1. Point 1: "The web tool contradicts your own finding." What does this mean and what was done?**
Meaning: the paper says the scoring rule is 100% correct, but the tool showed a model number called "likelihood of ASD traits". That looked like a medical probability, which it is not.
Done: the tool now shows the questionnaire score first. The model number is renamed "Model output" and has a note that it is not the chance of autism. The paper calls the tool a transparent demonstration. A note on ethics and regulation was added to the supporting material.

**Q2. Point 2: "Reported versus defined metrics." What does this mean and what was done?**
Meaning: the paper gave formulas for accuracy, precision, F1 and the Brier score, but the results only showed ROC-AUC and recall.
Done: the unused formulas were removed. The Brier score and calibration (ECE) are now reported in a table, and PR-AUC is reported in the text. The full numbers are in the supporting material.

**Q3. Point 3: "Explanation agreement." What does this mean and what was done?**
Meaning: for an additive EBM, SHAP should give the same values as the model itself. So agreement between them is not independent evidence, and the low correlations needed explaining.
Done: notebook 07 was rewritten and run again. All three methods now use the same test records and the same scale, over 10 splits, with the chance level reported. The paper now says that SHAP repeats the EBM values and only LIME is a separate view.

**Q4. Point 4: "Cross-source claim for adults." What does this mean and what was done?**
Meaning: the paper said the Kaggle adult data was synthetic in one place and "appears to be" synthetic in another. Also the abstract said four datasets when six were used.
Done: the paper now says "six public datasets". The Kaggle adult data is called synthetic and "not an independent source" everywhere. The toddler result is called "expected". RQ2 is described as answered only in part.

**Q5. Point 5: "Existing Work is now thin." What does this mean and what was done?**
Meaning: the literature review was mostly a list of studies, with no critical summary and no research gap.
Done: a "Critical Summary and Research Gap" section was added. Table I now has columns for validation, leakage control and external test, and includes the two studies that reported 100% accuracy. The paragraph that describes the structure of the paper was put back.

**Q6. Point 6: "Citations." What does this mean and what was done?**
Meaning: some methods were used without citing where they come from.
Done: references were added for LIME, the original SHAP paper, the origin of EBM, XGBoost, LightGBM, Random Forest, the AQ-10 and Q-CHAT-10 paper and the Holm method. The sentence about specialist shortage now cites a clinical review in the BMJ.

**Q7. Point 7: "Table VI mixes two groupings." What does this mean and what was done?**
Meaning: the fairness table listed sex and ethnicity rows together, so the counts looked as if they could be added.
Done: the table now has two sub-headings, "By sex" and "By ethnicity", with the number of positive and negative cases. The text says the rates are only indicative.

**Q8. Point 8: "Sanity check 2 is unclear." What does this mean and what was done?**
Meaning: if the raw file included the total-score column, a perfect result would be trivial.
Done: the text now says that only the ten answer columns are used and the total score is left out. It also says what question the check answers.

**Q9. Point 9: "Friedman and Nemenyi assume independent blocks." What does this mean and what was done?**
Meaning: these tests are made for separate datasets. Here they were run on overlapping folds of one dataset, so their p-values are too small.
Done: they are now described as a description only. Conclusions use the corrected t-test with the Holm correction, and effect sizes are reported. A table with the number of records in each dataset after cleaning was added.

**Q10. Point 10: "Voice and references." What does this mean and what was done?**
Meaning: the handbook asks for the third person, not "we". Two references had errors.
Done: the whole paper is in the third person. The broken "&amp;amp;" was fixed. The reference with the typo in its title belonged to a dataset that was not used, so it was removed with its sentence.

**Q11. Did the main results change because of the feedback?**
The model comparison did not change. No model was trained again. What changed is the explanation analysis (RQ3) and how carefully the cross-source result (RQ2) is described.

**Q12. Which notebooks were changed?**
Notebook 06 (new sections: PR-AUC, calibration, Holm correction, effect sizes, subgroup counts, dataset sizes) and notebook 07 (rewritten). Both were run again. All notebooks also got comments in easy English.

**Q13. What had to be moved out of the paper to stay within 8 pages?**
The cross-source bar chart, the noise figure, the importance figure, the sanity-check table and the full statistical tables. Most of these are now in the supporting material.

**Q14. Is anything from the feedback still open?**
- The title. The supervisor asked for "Decision Support Tool" to be aligned with the demonstration framing. The title was kept. This needs the supervisor's view.
- One row of Table I (Erkan and Thanh) says "Full text not available", because the paper is behind a paywall.
