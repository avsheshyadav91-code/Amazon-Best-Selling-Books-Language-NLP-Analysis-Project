"""
Unit tests for Amazon Bestseller Language & NLP Engine.
"""

import os
import sys
import unittest

SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from analyzer import AmazonBookLanguageAnalyzer, mean, pearson_corr
from nlp_engine import (
    analyze_sentiment,
    calculate_readability,
    clean_text,
    extract_linguistic_features,
    extract_ngrams,
    tokenize,
)


class TestNLPEngine(unittest.TestCase):

    def test_clean_and_tokenize(self):
        text = "Atomic Habits: An Easy & Proven Way!"
        tokens = tokenize(text, remove_stopwords=True)
        self.assertIn("atomic", tokens)
        self.assertIn("habits", tokens)
        self.assertIn("easy", tokens)
        self.assertIn("proven", tokens)
        self.assertNotIn("&", tokens)

    def test_subtitle_extraction(self):
        feat = extract_linguistic_features("Thinking, Fast and Slow: The Story of Decision")
        self.assertTrue(feat["has_subtitle"])
        self.assertTrue(feat["has_colon"])
        self.assertGreater(feat["subtitle_words"], 0)

    def test_sentiment_scoring(self):
        pos = analyze_sentiment("The Power of Positive Habits and Success")
        neg = analyze_sentiment("Bad Blood: Secrets, Lies, and Fury")
        self.assertEqual(pos["label"], "Positive")
        self.assertEqual(neg["label"], "Negative")
        self.assertGreater(pos["polarity"], 0)
        self.assertLess(neg["polarity"], 0)

    def test_readability(self):
        simple = calculate_readability("Good Cat")
        complex_title = calculate_readability("Astrophysics and Counterintuitive Anthropological Phenomenologies")
        self.assertGreater(simple, complex_title)

    def test_ngrams(self):
        tokens = ["atomic", "habits", "easy", "way"]
        bigrams = extract_ngrams(tokens, 2)
        self.assertEqual(bigrams, ["atomic habits", "habits easy", "easy way"])

    def test_pearson_correlation(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(pearson_corr(x, y), 1.0, places=2)

        y_inv = [10, 8, 6, 4, 2]
        self.assertAlmostEqual(pearson_corr(x, y_inv), -1.0, places=2)

if __name__ == "__main__":
    unittest.main()
