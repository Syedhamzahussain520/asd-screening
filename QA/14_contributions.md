# 14. Contributions

**Q1. What is a "contribution"?**
Something new that the project adds to what was known before.

**Q2. What are the contributions of this project?**
1. A clear demonstration, with evidence, that near-perfect accuracy on the ASDTests datasets comes from the label rule and not from diagnostic ability.
2. A fair comparison of six models, including EBM and TabPFN, in four age groups with leakage control.
3. A scoring-rule baseline and two sanity checks that other studies can reuse.
4. Harder tests (fewer questions, noisy answers) that show how the models behave when the rule cannot be recovered exactly.
5. A careful comparison of three explanation methods, repeated over many splits and compared with chance.
6. A transparent web tool that shows the questionnaire score first.
7. Practical advice for future studies on these datasets.

**Q3. Which contribution is the most important?**
The first one. It changes how results on these datasets should be read.

**Q4. What evidence supports the first contribution?**
- The rule matches the label in 100% of records in the main datasets.
- A baseline with no machine learning is 100% correct.
- A plain Logistic Regression on raw files, using only the ten answers, is also perfect.
- When the rule cannot be recovered (fewer questions, noise), accuracy falls for every model.

**Q5. Is the web tool a contribution if the model adds nothing?**
Yes, as a demonstration. It shows an honest way to present such a model: the standard score first, the model second, with clear limits.

**Q6. Who can use these findings?**
- Researchers who work with these datasets.
- Reviewers who read papers that report near-perfect accuracy.
- Students who learn how to test a model fairly.

**Q7. What is the advice for future studies?**
- Report a simple scoring-rule baseline.
- Add harder tests and a test on independent data.
- Report recall, the Brier score and calibration.
- Check explanations over many splits and against chance.

**Q8. Did the project find a better model than earlier work?**
No, and that is the point. On this data a simple, readable model is enough.
