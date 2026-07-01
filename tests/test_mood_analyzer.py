import unittest

from mood_analyzer import MoodAnalyzer


class MoodAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = MoodAnalyzer()

    def test_preprocess_removes_punctuation_and_normalizes_spacing(self) -> None:
        tokens = self.analyzer.preprocess("  I LOVE this!!!  ")
        self.assertEqual(tokens, ["i", "love", "this"])

    def test_negated_positive_is_scored_as_negative(self) -> None:
        score = self.analyzer.score_text("I am not happy today")
        self.assertLess(score, 0)

    def test_positive_emoji_and_repeated_letters_are_recognized(self) -> None:
        score = self.analyzer.score_text("soooo happy :)")
        self.assertGreater(score, 0)


if __name__ == "__main__":
    unittest.main()
