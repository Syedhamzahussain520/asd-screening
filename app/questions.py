# The questions and how each answer is scored.
# Q-CHAT-10 = Quantitative Checklist for Autism in Toddlers (10 questions).
# AQ-10 = Autism Spectrum Quotient, short form with 10 questions (child, adolescent, adult).
# Both are from Allison, Auyeung & Baron-Cohen (2012).
# Each answer becomes 0 or 1, in the same way as in the ASDTests datasets.

# the four answers of every AQ-10 question
AQ_OPTIONS = ["Definitely agree", "Slightly agree", "Slightly disagree", "Definitely disagree"]

# answer lists used by the toddler questions
FREQUENCY = ["Many times a day", "A few times a day", "A few times a week", "Less than once a week", "Never"]
ALWAYS_NEVER = ["Always", "Usually", "Sometimes", "Rarely", "Never"]

# cutoff: a score higher than this means "ASD traits".
# agree_items: the questions where "agree" gives 1 point. For the other questions "disagree" gives 1 point.
GROUPS = {
    "toddler": {
        "label": "Toddler (12–36 months)",
        "questionnaire": "Q-CHAT-10",
        "age_unit": "months",
        "age_range": (12, 36),
        "cutoff": 3,
        "questions": [
            ("Does your child look at you when you call his/her name?", ALWAYS_NEVER),
            ("How easy is it for you to get eye contact with your child?",
             ["Very easy", "Quite easy", "Quite difficult", "Very difficult", "Impossible"]),
            ("Does your child point to indicate that s/he wants something? (e.g. a toy that is out of reach)", FREQUENCY),
            ("Does your child point to share interest with you? (e.g. pointing at an interesting sight)", FREQUENCY),
            ("Does your child pretend? (e.g. care for dolls, talk on a toy phone)", FREQUENCY),
            ("Does your child follow where you're looking?", FREQUENCY),
            ("If you or someone else in the family is visibly upset, does your child show signs of "
             "wanting to comfort them? (e.g. stroking hair, hugging them)", ALWAYS_NEVER),
            ("Would you describe your child's first words as:",
             ["Very typical", "Quite typical", "Slightly unusual", "Very unusual", "My child doesn't speak"]),
            ("Does your child use simple gestures? (e.g. wave goodbye)", FREQUENCY),
            ("Does your child stare at nothing with no apparent purpose?", FREQUENCY),
        ],
    },
    "child": {
        "label": "Child (4–11 years)",
        "questionnaire": "AQ-10 Child",
        "age_unit": "years",
        "age_range": (4, 11),
        "cutoff": 6,
        "agree_items": [1, 5, 7, 10],
        "questions": [
            "S/he often notices small sounds when others do not.",
            "S/he usually concentrates more on the whole picture, rather than the small details.",
            "In a social group, s/he can easily keep track of several different people's conversations.",
            "S/he finds it easy to go back and forth between different activities.",
            "S/he doesn't know how to keep a conversation going with his/her peers.",
            "S/he is good at social chit-chat.",
            "When s/he is read a story, s/he finds it difficult to work out the character's intentions or feelings.",
            "When s/he was in preschool, s/he used to enjoy playing games involving pretending with other children.",
            "S/he finds it easy to work out what someone is thinking or feeling just by looking at their face.",
            "S/he finds it hard to make new friends.",
        ],
    },
    "adolescent": {
        "label": "Adolescent (12–16 years)",
        "questionnaire": "AQ-10 Adolescent",
        "age_unit": "years",
        "age_range": (12, 16),
        "cutoff": 6,
        "agree_items": [1, 5, 8, 10],
        "questions": [
            "S/he notices patterns in things all the time.",
            "S/he usually concentrates more on the whole picture, rather than the small details.",
            "In a social group, s/he can easily keep track of several different people's conversations.",
            "If there is an interruption, s/he can switch back to what s/he was doing very quickly.",
            "S/he frequently finds that s/he doesn't know how to keep a conversation going.",
            "S/he is good at social chit-chat.",
            "When s/he was younger, s/he used to enjoy playing games involving pretending with other children.",
            "S/he finds it difficult to imagine what it would be like to be someone else.",
            "S/he finds social situations easy.",
            "S/he finds it hard to make new friends.",
        ],
    },
    "adult": {
        "label": "Adult (18+ years)",
        "questionnaire": "AQ-10 Adult",
        "age_unit": "years",
        "age_range": (17, 100),
        "cutoff": 6,
        "agree_items": [1, 7, 8, 10],
        "questions": [
            "I often notice small sounds when others do not.",
            "I usually concentrate more on the whole picture, rather than the small details.",
            "I find it easy to do more than one thing at once.",
            "If there is an interruption, I can switch back to what I was doing very quickly.",
            "I find it easy to 'read between the lines' when someone is talking to me.",
            "I know how to tell if someone listening to me is getting bored.",
            "When I'm reading a story I find it difficult to work out the characters' intentions.",
            "I like to collect information about categories of things (e.g. types of car, bird, train, plant).",
            "I find it easy to work out what someone is thinking or feeling just by looking at their face.",
            "I find it difficult to work out people's intentions.",
        ],
    },
}


def question_list(group):
    # gives back a list of (question text, possible answers)
    info = GROUPS[group]
    if group == "toddler":
        return info["questions"]
    return [(q, AQ_OPTIONS) for q in info["questions"]]


def score_answer(group, item, answer):
    # item is the question number (1 to 10). Gives 1 if the answer points towards autistic traits.
    # Example: adult question 1 is an "agree" question, so "Slightly agree" gives 1
    if group == "toddler":
        options = GROUPS["toddler"]["questions"][item - 1][1]
        pos = options.index(answer)
        # questions 1 to 9: the last three answers give 1 point. Question 10: the first three do
        return int(pos <= 2) if item == 10 else int(pos >= 2)

    # "Definitely agree" and "Slightly agree" both count as agree
    agree = answer in AQ_OPTIONS[:2]
    return int(agree) if item in GROUPS[group]["agree_items"] else int(not agree)
