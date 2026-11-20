# 1. Project overview

**Q1. What is the title of the project?**
Early Autism Screening Using Interpretable Machine Learning Models and a Web-Based Decision Support Tool.

**Q2. What is the project about, in one or two sentences?**
Many papers say that machine learning can find autism with almost 100% accuracy from a short questionnaire. This project checks what that accuracy really means, compares six models in a fair way, and builds a small web tool.

**Q3. What is autism (ASD)?**
ASD means Autism Spectrum Disorder. It is a lifelong condition that affects how a person communicates, interacts with others and behaves. About 1 in 100 people have it.

**Q4. What is the real-world problem?**
A full autism diagnosis needs trained specialists and several visits, and waiting lists are long. So a quick first check, called screening, is used to decide who should see a specialist.

**Q5. What is screening? Is it the same as diagnosis?**
No. Screening is a quick first check. It only says "this person may need a full assessment". A diagnosis is made by a qualified clinician after a full assessment.

**Q6. What is the research problem?**
In the public datasets, the label (ASD traits: yes or no) is made from the same ten answers that the model gets as input. So a model can get almost 100% just by learning to add up the answers. Earlier papers present this as if the model can detect autism.

**Q7. What is the aim of the project?**
To find out what near-perfect accuracy on these datasets really means, and whether two models, EBM and TabPFN, add anything over simpler models.

**Q8. What are the objectives?**
1. Compare six models in four age groups with data leakage under control.
2. Test the models in harder settings: fewer questions and noisy answers.
3. Test the models on data from a second source.
4. Compare three explanation methods: SHAP, LIME and EBM.
5. Build a small web tool as a transparent demonstration.

**Q9. What are the three research questions?**
- RQ1: How well do EBM and TabPFN perform compared with the four other models in the four age groups, when data leakage is controlled and when the questionnaire is incomplete or noisy?
- RQ2: How well do the models work when they are trained on one data source and tested on a second source for the same age group?
- RQ3: Which screening questions matter most for the predictions, and do SHAP, LIME and EBM agree on them?

**Q10. What is the short answer to each research question?**
- RQ1: Logistic Regression, EBM and TabPFN get perfect scores on the full questionnaire, because the label is a sum of the answers. In harder settings all six models lose accuracy at a similar rate. EBM and TabPFN are as good as Logistic Regression but not better. EBM gives the most trustworthy probabilities.
- RQ2: Answered only in part. Toddler models transfer almost perfectly, but both toddler datasets use the same rule. The second adult dataset is synthetic, so it is not an independent test.
- RQ3: Every question gets about the same importance. SHAP repeats the EBM values. LIME agrees on the top five questions only in some age groups.

**Q11. What is the main message of the project?**
Very high accuracy on these public datasets shows that a model has learned a screening rule. It does not show that the model can diagnose autism.

**Q12. What is new in this project compared with earlier work?**
- A baseline that only applies the scoring rule, with no machine learning.
- Sanity checks that prove the perfect scores come from the data and not from a mistake.
- Leakage control in every step.
- Harder tests: fewer questions, noisy answers and a second data source.
- Three explanation methods compared with each other and with the level expected by chance.

**Q13. What are the parts of the project?**
- Eight Jupyter notebooks (the code and experiments).
- A Streamlit web app.
- An IEEE format paper of 8 pages, plus supporting material.
- A presentation with speaker notes.

**Q14. Where is the code?**
On GitHub: https://github.com/Syedhamzahussain520/asd-screening

**Q15. Which module is this for?**
COM748 Master's Project, School of Computing, Ulster University.
