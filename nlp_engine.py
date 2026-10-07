"""
NLP and Linguistic Feature Extraction Engine for Amazon Bestseller Book Titles.
Designed to run in standard Python with pure-Python sentiment lexicons, n-grams,
readability estimation, and TF-IDF calculation.
"""

import math
import re
from collections import Counter

# Standard English stopwords
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "book", "books",
    "novel", "edition", "series", "parts", "part", "vol", "volume"
}

# Pure Python Sentiment Lexicon (valenced polarity weights: -1.0 to +1.0)
SENTIMENT_LEXICON = {
    # Strong positive
    "love": 0.8, "loved": 0.8, "good": 0.5, "great": 0.7, "best": 0.8, "power": 0.6,
    "powerful": 0.8, "effective": 0.7, "miracle": 0.8, "magic": 0.6, "success": 0.8,
    "happy": 0.7, "happiness": 0.8, "freedom": 0.7, "brave": 0.7, "triumph": 0.8,
    "perseverance": 0.7, "meaning": 0.5, "clean": 0.5, "peace": 0.7, "rich": 0.6,
    "gentleman": 0.5, "win": 0.7, "friends": 0.6, "influence": 0.5, "easy": 0.5,
    "proven": 0.6, "tidying": 0.5, "resilience": 0.7, "redemption": 0.7, "genius": 0.8,
    "hope": 0.6, "smart": 0.6, "smarter": 0.7, "focused": 0.5, "super": 0.7,
    "wonderful": 0.8, "light": 0.5, "places": 0.3, "hungry": 0.1, "caterpillar": 0.1,
    "comfort": 0.6, "goodnight": 0.5, "sweet": 0.6, "cure": 0.7, "healing": 0.7,

    # Strong negative / conflict / tension (very common in thrillers & memoirs)
    "fury": -0.8, "fear": -0.8, "bad": -0.6, "blood": -0.6, "crime": -0.8, "kill": -0.8,
    "mockingbird": 0.0, "gone": -0.3, "silent": -0.2, "fault": -0.5, "stars": 0.3,
    "hurt": -0.7, "trauma": -0.8, "untold": -0.2, "disaster": -0.9, "murder": -0.9,
    "meltdown": -0.6, "wrecking": -0.6, "f*ck": -0.4, "rage": -0.8, "dangerous": -0.7,
    "lies": -0.8, "secrets": -0.3, "crisis": -0.8, "unbroken": 0.6, "hornet": -0.4,
    "thief": -0.6, "nuclear": -0.5, "death": -0.8, "dead": -0.8, "lost": -0.5,
    "dragon": 0.0, "tattoo": 0.0, "wimpy": -0.3, "hard": -0.3, "crying": -0.6,

    # Power & Emotional archetypes
    "secret": 0.4, "art": 0.4, "subtle": 0.2, "atomic": 0.4, "habits": 0.3,
    "mind": 0.3, "defy": 0.5, "odds": 0.2, "caste": -0.2, "discontents": -0.5,
    "vanished": -0.4, "vanishing": -0.4, "whisper": 0.1, "library": 0.3,
    "promised": 0.6, "land": 0.2, "fire": -0.1, "greenlights": 0.6, "deep": 0.3,
    "psychology": 0.2, "money": 0.3, "greed": -0.6, "becoming": 0.6, "educated": 0.6
}

def clean_text(text: str) -> str:
    """Removes special punctuation, preserves words and digits."""
    return re.sub(r"[^\w\s]", " ", text).strip().lower()

def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """Tokenizes text into words."""
    cleaned = clean_text(text)
    words = cleaned.split()
    if remove_stopwords:
        return [w for w in words if w not in STOPWORDS and len(w) > 1 and not w.isdigit()]
    return [w for w in words if len(w) > 0]

def count_syllables(word: str) -> int:
    """Heuristic syllable counter for readability metrics."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", word)
    word = re.sub(r"^y", "", word)
    matches = re.findall(r"[aeiouy]{1,2}", word)
    return max(1, len(matches))

def calculate_readability(title: str) -> float:
    """
    Computes an estimated Flesch Reading Ease score for book titles.
    Higher = easier to read, lower = more complex/academic.
    Formula adapted for short phrases: 206.835 - 1.015 * (words) - 84.6 * (syllables/word)
    """
    words = tokenize(title, remove_stopwords=False)
    if not words:
        return 100.0
    total_syllables = sum(count_syllables(w) for w in words)
    syllables_per_word = total_syllables / len(words)
    score = 206.835 - (1.015 * len(words)) - (84.6 * syllables_per_word)
    return round(max(0.0, min(100.0, score)), 2)

def analyze_sentiment(title: str) -> dict:
    """
    Computes polarity and subjectivity of title.
    Polarity: -1.0 (very negative) to +1.0 (very positive)
    Subjectivity: 0.0 (completely objective/matter-of-fact) to 1.0 (highly emotional/subjective)
    """
    tokens = clean_text(title).split()
    if not tokens:
        return {"polarity": 0.0, "subjectivity": 0.0, "label": "Neutral"}

    scores = []
    subjective_hits = 0
    for t in tokens:
        if t in SENTIMENT_LEXICON:
            val = SENTIMENT_LEXICON[t]
            scores.append(val)
            if abs(val) > 0.2:
                subjective_hits += 1

    if not scores:
        polarity = 0.0
        subjectivity = 0.1
    else:
        polarity = sum(scores) / len(scores)
        subjectivity = min(1.0, subjective_hits / max(1, len(tokens) * 0.5))

    polarity = round(max(-1.0, min(1.0, polarity)), 3)
    subjectivity = round(subjectivity, 3)

    if polarity > 0.15:
        label = "Positive"
    elif polarity < -0.15:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "label": label
    }

def extract_linguistic_features(title: str) -> dict:
    """
    Extracts structural and stylistic features of a book title:
    - Word count, character count, avg word length
    - Subtitle presence (indicated by colon, hyphen, or dash)
    - Punctuation count
    - Title case ratio
    - Readability index
    - Sentiment metrics
    """
    raw_words = title.strip().split()
    char_len = len(title)
    word_count = len(raw_words)
    avg_word_len = round(sum(len(w) for w in raw_words) / max(1, word_count), 2)

    has_colon = ":" in title
    has_hyphen_dash = " - " in title or "—" in title or "–" in title
    has_subtitle = has_colon or has_hyphen_dash
    has_question = "?" in title
    has_exclamation = "!" in title

    # Uppercase analysis
    caps_words = sum(1 for w in raw_words if w.isupper() and len(w) > 1)
    title_cased = sum(1 for w in raw_words if w.istitle())
    title_case_ratio = round(title_cased / max(1, word_count), 2)

    # Subtitle length vs Main title length
    if has_colon:
        parts = title.split(":", 1)
        main_len = len(parts[0].strip().split())
        sub_len = len(parts[1].strip().split())
    else:
        main_len = word_count
        sub_len = 0

    sentiment = analyze_sentiment(title)
    readability = calculate_readability(title)

    return {
        "char_count": char_len,
        "word_count": word_count,
        "avg_word_length": avg_word_len,
        "has_subtitle": has_subtitle,
        "has_colon": has_colon,
        "has_question": has_question,
        "has_exclamation": has_exclamation,
        "title_case_ratio": title_case_ratio,
        "caps_word_count": caps_words,
        "main_title_words": main_len,
        "subtitle_words": sub_len,
        "readability_score": readability,
        "sentiment_polarity": sentiment["polarity"],
        "sentiment_subjectivity": sentiment["subjectivity"],
        "sentiment_label": sentiment["label"]
    }

def extract_ngrams(tokens: list[str], n: int) -> list[str]:
    """Generates n-grams from a list of tokens."""
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def compute_corpus_tfidf(documents: list[str], top_k: int = 15) -> list[tuple[str, float]]:
    """
    Computes top TF-IDF unigram terms for a corpus of book titles.
    """
    doc_tokens = [tokenize(doc, remove_stopwords=True) for doc in documents]
    num_docs = len(documents)
    if num_docs == 0:
        return []

    # Document frequency
    df = Counter()
    for tokens in doc_tokens:
        unique_tokens = set(tokens)
        for t in unique_tokens:
            df[t] += 1

    # Term frequency total across documents
    tf = Counter()
    for tokens in doc_tokens:
        for t in tokens:
            tf[t] += 1

    tfidf_scores = {}
    for term, freq in tf.items():
        doc_f = df.get(term, 1)
        idf = math.log((num_docs + 1) / (doc_f + 1)) + 1
        tfidf_scores[term] = round(freq * idf, 3)

    return sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
