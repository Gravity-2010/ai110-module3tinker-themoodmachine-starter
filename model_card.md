# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  

I used both model, I made changes to rule based model but inly ran the ML model, for comparision.

**Intended purpose:**  
What is this model trying to do?  
Both the models are trying to classify short text messages as moods like positive, negative, neutral, or mixed.

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).

The rule-based mood analyzer looks at the words in a sentence and compares them to lists of positive and negative words. It also handles a few simple cases like negation, repeated letters, and emojis, and gives those clues a score. Then it uses that score to decide whether the mood is positive, negative, neutral, or mixed.

The ML model works by turning each text into a simple bag-of-words representation, where it counts which words appear in the message. It then trains a logistic regression classifier on those word counts using the labeled examples from the dataset. After training, it can predict a mood label for new text by looking at which words in it match patterns it learned from the training data.



## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.

The dataset contains a few short example posts in SAMPLE_POSTS. I also added a few new posts to make the dataset more varied and to test how the models handle different kinds of language.
I added a new sentence to sample post and a subsequent label for it to the list of labels.

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

I labeled each post based on the mood it seemed to express most clearly, such as positive, negative, neutral, or mixed. Some posts were harder to label because they contained both positive and negative feelings, sarcasm, or casual slang.



**Important characteristics of your dataset:**  
- The dataset includes slang and emojis.
- Some posts contain sarcasm or irony.
- Several posts express mixed feelings rather than only one clear emotion.
- Many messages are short and somewhat ambiguous.


**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

The dataset is small, so the models may not generalize well to new examples. Some posts are also ambiguous, which can make labeling subjective and may lead to inconsistent predictions. Imbalance in the dataset can also create bias, say I have more sentences with mixed emotions, then the model will be biased towards mixed emotions and predict it more often.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
The rule-based model gives points to words that suggest positive or negative mood. Positive words increase the score, while negative words decrease it. I also added simple rules for negation, such as “not happy,” and for emojis or emotional cues like smile, laugh, cry, and sad. The final score is mapped to a label: positive, negative, neutral, or mixed.


**Strengths of this approach:**  
Where does it behave predictably or reasonably well?
This approach is simple, easy to understand, and works well for short texts that contain clear emotional words.

**Weaknesses of this approach:**  
Where does it fail?  
It can struggle with sarcasm, mixed feelings, and phrases that depend on context. It also may fail when the text uses slang, unusual wording, or subtle emotional cues.

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
The ML model uses a bag-of-words representation created with CountVectorizer, which turns each text into counts of the words it contains.

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.
The model was trained on the posts in SAMPLE_POSTS and their labels in TRUE_LABELS.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?
The model learns patterns from the labeled examples and uses them to predict labels for new text. Its performance depends heavily on the quality and variety of the training examples.

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

A strength is that it can learn patterns automatically from data. A weakness is that it may overfit the small dataset and may rely on words that appear by chance rather than true emotional meaning.

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

I evaluated the models by testing them on the labeled posts in dataset.py and comparing their predicted labels to the true labels.

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

I am tired but happy got a mixed label, which was accurate.

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

I am happy. I am Sad. Mostly all the sentences got a mixed label, which makes me think that the model is biased towards mixed labels.

## 6. Limitations

The dataset is small, so the models may not generalize well to new or more complex posts. The models may struggle with sarcasm, subtle emotions, and short messages that are ambiguous. They also depend heavily on the words and labels provided in the dataset.

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  

Mood detection can be inaccurate, and that can lead to incorrect conclusions about a person’s emotional state. It is important to be careful when using this kind of system in real applications, especially for personal messages or mental health-related situations. Privacy is also a concern because analyzing people’s text can be sensitive.
## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

More labeled data could improve both models. The ML model could use TF-IDF instead of simple CountVectorizer, and the rule-based model could be improved with better handling of sarcasm, slang, and context. A separate test set and more diverse examples would also make the evaluation more reliable.