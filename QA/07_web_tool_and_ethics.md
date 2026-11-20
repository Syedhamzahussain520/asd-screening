# 7. Web tool and ethics

**Q1. What is the web tool?**
A small web app made with Streamlit. A user picks an age group, answers the ten questions and gets a result with an explanation.

**Q2. What is Streamlit?**
A Python library for making simple web apps without writing web code. Streamlit Community Cloud can host such an app for free.

**Q3. What pages does it have?**
- Home: what the tool is and what the words mean.
- Screening: the questions and the result.
- Model Performance: how the models did in testing.
- About: the data, the method, the limits and privacy.

**Q4. What does the result page show?**
1. The questionnaire score and the cut-off. This is the main result.
2. The model output, shown second, with a note that it is not the chance that the person has autism.
3. A bar chart of the answers that pushed the model output up or down.
4. A statement that the result is not a diagnosis.

**Q5. Why is the score shown first and not the model?**
Because the results show that on the full questionnaire a model adds nothing to the score. The label is the score. The supervisor pointed out that showing "likelihood of ASD traits: 100%" was misleading.

**Q6. Then what does the model add?**
On the full questionnaire, nothing. It is in the tool to demonstrate how an interpretable model can explain a result. A model could only be useful when the rule cannot be applied directly, for example when some answers are missing.

**Q7. Is the tool a decision support tool or a demonstration?**
It is a research demonstration. It is not a clinical tool and not a medical device.

**Q8. What happens if the model and the score do not agree?**
The tool shows a warning and tells the user to go by the score, because the score is the standard result.

**Q9. Does the tool store my answers?**
No. Answers are only used to make the result on the screen. Nothing is saved or logged, and no name is asked.

**Q10. What is UK GDPR and why does it matter?**
The UK General Data Protection Regulation is the law on personal data. Health information is "special category data" and needs strong protection. The tool avoids the problem by not storing anything and not asking for anything that identifies a person.

**Q11. Why is data about children a special concern?**
Three of the four age groups are children and young people, and a parent answers for them. Children cannot agree to the use of their data in the same way as adults, so extra care is needed.

**Q12. What is "software as a medical device"?**
Software that is meant to help diagnose or screen for a health condition can count as a medical device. In the UK such software is regulated by the MHRA (Medicines and Healthcare products Regulatory Agency).

**Q13. Is this tool a medical device?**
No. It is a research demonstration, it is not meant for clinical use and it has not been assessed as a medical device. Before any real use it would need a clinical evaluation and the correct approval.

**Q14. What disclaimers does the tool show?**
That the result is not a diagnosis, that only a qualified clinician can diagnose autism, that a low score does not rule autism out, and that anyone with concerns should speak to a health professional.

**Q15. What harm could a screening tool do?**
- A false negative can give false comfort and delay a referral.
- A false positive can cause worry.
This is why the tool is clear about its limits.

**Q16. Why is TabPFN not in the web tool?**
It needs PyTorch and a large file of model weights, which does not fit a free hosting service.

**Q17. Has the tool been tested with real users?**
No. Testing with clinicians and families is listed as future work.

**Q18. Was ethical approval needed for the data?**
The project uses only public, anonymous datasets and collects no new data from people.
