# 6. Explaining the model

**Q1. What does "explaining a model" mean?**
Showing which inputs made the model give its answer.
Example: "The model output is high mainly because of the answers to questions 1, 2 and 8."

**Q2. What is SHAP?**
SHapley Additive exPlanations. It shares out one prediction between the inputs. Each input gets a plus or minus value, and together they add up to the prediction.
Example: the model says 0.80, the average is 0.50, and question 1 gets +0.10 of that difference.

**Q3. What is LIME?**
Local Interpretable Model-agnostic Explanations. It takes one person's row, changes it a little many times, and watches how the prediction moves. Then it fits a very simple model to those changes.

**Q4. What is the EBM's own explanation?**
The EBM has one curve for each input. The value of the curve is the input's contribution. Nothing extra is needed. It is exact, because it is the model itself.

**Q5. What does "additive model" mean?**
The prediction is a sum of separate parts, one for each input.
Example: score = part for A1 + part for A2 + ... + part for age.

**Q6. What are log-odds?**
The model's score before it is turned into a probability. 0 means 50%. Above 0 means more than 50%. Below 0 means less than 50%. All three methods are compared on this same scale.

**Q7. What was wrong with the first version of this analysis?**
The three methods were not compared like for like. The EBM importance was measured on training rows, SHAP on test rows and on a different scale, and LIME on its own scale. Only one train and test split was used. The supervisor asked for this to be checked.

**Q8. How was it fixed?**
- All three methods now explain the same test records.
- All three use the same scale (log-odds).
- The comparison is repeated over 10 splits and the average is reported.
- The chance level (2.5 for top-five overlap) is reported next to the results.

**Q9. Is SHAP independent of the EBM?**
No. For an additive model, SHAP gives back the model's own values once both start from the same reference point. I checked this: the largest difference was smaller than 0.000001. So when EBM and SHAP agree, it is only a consistency check. It is not new evidence.

**Q10. What is a "reference point" here?**
The average that the values are measured from. The EBM measures from the average of its training data (after SMOTENC). SHAP measures from the average of the background rows (original records).

**Q11. Then why do EBM and SHAP rank the questions differently for toddlers and adults?**
The only difference between them is the reference point. Toddlers and adults are the two unbalanced groups, so SMOTENC changes the training data most there. This is a likely reason, but it was not tested on its own. Because all ten questions have almost the same importance, a small shift is enough to change the order.

**Q12. Does LIME agree with the other two?**
Partly. For adolescents it agrees well (correlation about 0.9, overlap 4.2 of 5). For toddlers it agrees partly. For children and adults the top-five overlap is only 2.6 to 2.9, which is close to the chance level of 2.5.

**Q13. What are the agreement numbers?**
Mean Spearman correlation, with mean top-five overlap in brackets:
- Toddler: EBM and SHAP 0.65 (3.9), EBM and LIME 0.60 (3.2), SHAP and LIME 0.62 (3.6)
- Child: 0.96 (4.8), 0.22 (2.8), 0.28 (2.8)
- Adolescent: 0.98 (4.9), 0.90 (4.2), 0.88 (4.2)
- Adult: 0.67 (3.7), 0.27 (2.9), 0.23 (2.6)

**Q14. Which question is the most important?**
None can be named. For toddlers, children and adults each question gets between 0.08 and 0.11 of the total importance. That is close to 0.10, which is what an equal-weight rule gives. The rankings also change from split to split.

**Q15. Why is every question about equally important?**
Because the label is a simple sum where every question counts as 1 point. The model has learned this rule.

**Q16. Do the personal details matter?**
Almost not at all. Age, sex, jaundice and family history get close to zero importance, because the label depends only on the ten answers.

**Q17. Do these rankings tell us which question matters most for autism?**
No. They only describe the model and this sample. They should not be read as a clinical finding.

**Q18. So what are the explanations good for?**
They show why one person got their result from the model. In the web tool this is shown as a bar chart.
