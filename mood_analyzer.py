# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        emoji_replacements = {
            ":)": " smile ",
            ":-)": " smile ",
            ":(" : " frown ",
            ":-(": " frown ",
            ":d": " laugh ",
            "lol": " laugh ",
            "lmao": " laugh ",
            "😂": " laugh ",
            "😭": " cry ",
            "🥲": " sad ",
            "😊": " smile ",
            "🙂": " smile ",
            "😒": " annoyed ",
            "💀": " laugh ",
        }

        for original, replacement in emoji_replacements.items():
            cleaned = cleaned.replace(original, replacement)

        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
        cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)

        return [token for token in cleaned.split() if token]

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _score_tokens(self, tokens: List[str]) -> Tuple[int, List[str], List[str]]:
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negation_words = {"not", "never", "no", "hardly", "barely", "isnt", "isn't", "dont", "don't", "cant", "can't", "wont", "won't"}

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token in negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token in self.positive_words:
                    score -= 2
                    negative_hits.append(f"not {next_token}")
                elif next_token in self.negative_words:
                    score += 2
                    positive_hits.append(f"not {next_token}")
                i += 2
                continue

            if token in self.positive_words:
                score += 2 if token in {"love", "great", "amazing", "awesome", "terrific", "awsome", "happy"} else 1
                positive_hits.append(token)
            elif token in self.negative_words:
                score -= 2 if token in {"hate", "terrible", "awful", "boring", "brutal", "sad", "sick", "upset"} else 1
                negative_hits.append(token)
            elif token in {"smile", "laugh"}:
                score += 1
                positive_hits.append(token)
            elif token in {"frown", "cry", "sad", "annoyed", "tired", "stressed"}:
                score -= 1
                negative_hits.append(token)

            i += 1

        return score, positive_hits, negative_hits

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        The implementation now also handles simple negation,
        repeated letters, and a few common emoji-style cues.
        """
        tokens = self.preprocess(text)
        score, _, _ = self._score_tokens(tokens)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The simple mapping now uses a small threshold so that mildly mixed
        sentiment can be labeled as "mixed" instead of always falling back to
        "neutral".
        """
        score = self.score_text(text)

        if score >= 2:
            return "positive"
        if score <= -2:
            return "negative"
        if score == 0:
            return "neutral"
        return "mixed"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._score_tokens(tokens)

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
