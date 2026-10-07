"""
Statistical and Linguistic Analysis Engine for Amazon Bestsellers.
Calculates correlations, genre contrasts, language breakdowns, and n-gram rankings.
"""

import csv
import math
import os
from collections import Counter, defaultdict

from nlp_engine import (
    compute_corpus_tfidf,
    extract_linguistic_features,
    extract_ngrams,
    tokenize,
)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def std_dev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def median(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    n = len(sorted_v)
    mid = n // 2
    if n % 2 == 1:
        return sorted_v[mid]
    return (sorted_v[mid - 1] + sorted_v[mid]) / 2.0

def pearson_corr(x: list[float], y: list[float]) -> float:
    """Calculates Pearson correlation coefficient between two numeric lists."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    mx, my = mean(x), mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den_x = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    den_y = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if den_x == 0 or den_y == 0:
        return 0.0
    return round(num / (den_x * den_y), 4)

class AmazonBookLanguageAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.raw_records = []
        self.enriched_records = []
        self.load_and_enrich()

    def load_and_enrich(self):
        with open(self.csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rec = {
                    "Name": row["Name"],
                    "Author": row["Author"],
                    "User Rating": float(row["User Rating"]),
                    "Reviews": int(row["Reviews"]),
                    "Price": float(row["Price"]),
                    "Year": int(row["Year"]),
                    "Genre": row["Genre"],
                    "Language": row["Language"]
                }
                # Enrich with NLP features
                nlp_feats = extract_linguistic_features(rec["Name"])
                rec.update(nlp_feats)
                self.enriched_records.append(rec)
        self.raw_records = self.enriched_records

    def get_summary_kpis(self) -> dict:
        total = len(self.enriched_records)
        unique_titles = len(set(r["Name"] for r in self.enriched_records))
        unique_authors = len(set(r["Author"] for r in self.enriched_records))
        ratings = [r["User Rating"] for r in self.enriched_records]
        reviews = [r["Reviews"] for r in self.enriched_records]
        prices = [r["Price"] for r in self.enriched_records]
        word_counts = [r["word_count"] for r in self.enriched_records]
        readability = [r["readability_score"] for r in self.enriched_records]
        subtitles_count = sum(1 for r in self.enriched_records if r["has_subtitle"])

        return {
            "total_records": total,
            "unique_titles": unique_titles,
            "unique_authors": unique_authors,
            "avg_rating": round(mean(ratings), 2),
            "median_rating": round(median(ratings), 2),
            "avg_reviews": round(mean(reviews), 1),
            "median_reviews": round(median(reviews), 1),
            "avg_price": round(mean(prices), 2),
            "avg_word_count": round(mean(word_counts), 2),
            "avg_readability": round(mean(readability), 2),
            "subtitle_percentage": round((subtitles_count / total) * 100, 1)
        }

    def analyze_languages(self) -> dict:
        """Language distribution and metrics per language."""
        lang_groups = defaultdict(list)
        for r in self.enriched_records:
            lang_groups[r["Language"]].append(r)

        result = {}
        total = len(self.enriched_records)
        for lang, items in sorted(lang_groups.items(), key=lambda x: len(x[1]), reverse=True):
            ratings = [i["User Rating"] for i in items]
            reviews = [i["Reviews"] for i in items]
            prices = [i["Price"] for i in items]
            words = [i["word_count"] for i in items]

            result[lang] = {
                "count": len(items),
                "share_pct": round((len(items) / total) * 100, 2),
                "avg_rating": round(mean(ratings), 2),
                "avg_reviews": round(mean(reviews), 1),
                "avg_price": round(mean(prices), 2),
                "avg_word_count": round(mean(words), 2),
                "unique_titles": len(set(i["Name"] for i in items))
            }
        return result

    def analyze_genre_linguistics(self) -> dict:
        """Detailed linguistic and market comparison between Fiction and Non-Fiction."""
        genres = defaultdict(list)
        for r in self.enriched_records:
            genres[r["Genre"]].append(r)

        breakdown = {}
        for genre, items in genres.items():
            words = [i["word_count"] for i in items]
            chars = [i["char_count"] for i in items]
            ratings = [i["User Rating"] for i in items]
            reviews = [i["Reviews"] for i in items]
            prices = [i["Price"] for i in items]
            readability = [i["readability_score"] for i in items]
            polarities = [i["sentiment_polarity"] for i in items]
            has_sub = sum(1 for i in items if i["has_subtitle"])

            # Vocabulary and n-grams
            unique_titles = list(set(i["Name"] for i in items))
            all_tokens = []
            bigrams = []
            for t in unique_titles:
                toks = tokenize(t, remove_stopwords=True)
                all_tokens.extend(toks)
                bigrams.extend(extract_ngrams(toks, 2))

            top_words = Counter(all_tokens).most_common(10)
            top_bigrams = Counter(bigrams).most_common(8)
            tfidf = compute_corpus_tfidf(unique_titles, top_k=8)

            breakdown[genre] = {
                "count": len(items),
                "pct_of_total": round((len(items) / len(self.enriched_records)) * 100, 1),
                "avg_word_count": round(mean(words), 2),
                "avg_char_count": round(mean(chars), 2),
                "avg_readability": round(mean(readability), 2),
                "subtitle_pct": round((has_sub / len(items)) * 100, 1),
                "avg_rating": round(mean(ratings), 2),
                "avg_reviews": round(mean(reviews), 1),
                "avg_price": round(mean(prices), 2),
                "avg_polarity": round(mean(polarities), 3),
                "top_words": top_words,
                "top_bigrams": top_bigrams,
                "top_tfidf": tfidf
            }
        return breakdown

    def analyze_sentiment_impact(self) -> dict:
        """Evaluates whether title sentiment correlates with rating, reviews, or genre."""
        buckets = defaultdict(list)
        for r in self.enriched_records:
            buckets[r["sentiment_label"]].append(r)

        result = {}
        total = len(self.enriched_records)
        for label, items in buckets.items():
            ratings = [i["User Rating"] for i in items]
            reviews = [i["Reviews"] for i in items]
            prices = [i["Price"] for i in items]
            words = [i["word_count"] for i in items]

            result[label] = {
                "count": len(items),
                "share_pct": round((len(items) / total) * 100, 1),
                "avg_rating": round(mean(ratings), 2),
                "avg_reviews": round(mean(reviews), 1),
                "avg_price": round(mean(prices), 2),
                "avg_words": round(mean(words), 2),
                "examples": list(set(i["Name"] for i in items))[:3]
            }
        return result

    def analyze_subtitle_impact(self) -> dict:
        """Quantifies the difference between titles with subtitles (colons) vs single titles."""
        with_sub = [r for r in self.enriched_records if r["has_subtitle"]]
        no_sub = [r for r in self.enriched_records if not r["has_subtitle"]]

        def stats_group(items):
            return {
                "count": len(items),
                "avg_rating": round(mean([i["User Rating"] for i in items]), 2),
                "avg_reviews": round(mean([i["Reviews"] for i in items]), 1),
                "avg_price": round(mean([i["Price"] for i in items]), 2),
                "avg_words": round(mean([i["word_count"] for i in items]), 2),
                "avg_readability": round(mean([i["readability_score"] for i in items]), 2),
                "fiction_pct": round(sum(1 for i in items if i["Genre"] == "Fiction") / len(items) * 100, 1),
                "non_fiction_pct": round(sum(1 for i in items if i["Genre"] == "Non Fiction") / len(items) * 100, 1),
            }

        return {
            "with_subtitles": stats_group(with_sub),
            "without_subtitles": stats_group(no_sub)
        }

    def compute_correlations(self) -> dict:
        """Computes Pearson correlations between linguistic and market metrics."""
        words = [float(r["word_count"]) for r in self.enriched_records]
        chars = [float(r["char_count"]) for r in self.enriched_records]
        readability = [float(r["readability_score"]) for r in self.enriched_records]
        polarity = [float(r["sentiment_polarity"]) for r in self.enriched_records]
        ratings = [float(r["User Rating"]) for r in self.enriched_records]
        reviews = [float(r["Reviews"]) for r in self.enriched_records]
        prices = [float(r["Price"]) for r in self.enriched_records]

        return {
            "word_count_vs_rating": pearson_corr(words, ratings),
            "word_count_vs_reviews": pearson_corr(words, reviews),
            "word_count_vs_price": pearson_corr(words, prices),
            "readability_vs_rating": pearson_corr(readability, ratings),
            "readability_vs_reviews": pearson_corr(readability, reviews),
            "sentiment_polarity_vs_rating": pearson_corr(polarity, ratings),
            "sentiment_polarity_vs_reviews": pearson_corr(polarity, reviews),
            "price_vs_rating": pearson_corr(prices, ratings)
        }

    def analyze_top_authors_and_phrasing(self, top_n: int = 10) -> list[dict]:
        """Finds top recurring authors and their linguistic fingerprint."""
        author_books = defaultdict(list)
        for r in self.enriched_records:
            author_books[r["Author"]].append(r)

        ranked = []
        for author, items in sorted(author_books.items(), key=lambda x: len(x[1]), reverse=True)[:top_n]:
            unique_titles = list(set(i["Name"] for i in items))
            words = [i["word_count"] for i in items]
            ratings = [i["User Rating"] for i in items]
            genres = list(set(i["Genre"] for i in items))
            ranked.append({
                "author": author,
                "appearances": len(items),
                "unique_titles_count": len(unique_titles),
                "primary_genre": genres[0] if len(genres) == 1 else "Both",
                "avg_rating": round(mean(ratings), 2),
                "avg_title_words": round(mean(words), 2),
                "sample_title": unique_titles[0]
            })
        return ranked

    def run_full_analysis(self) -> dict:
        return {
            "kpis": self.get_summary_kpis(),
            "languages": self.analyze_languages(),
            "genres": self.analyze_genre_linguistics(),
            "sentiment": self.analyze_sentiment_impact(),
            "subtitle_comparison": self.analyze_subtitle_impact(),
            "correlations": self.compute_correlations(),
            "top_authors": self.analyze_top_authors_and_phrasing()
        }

if __name__ == "__main__":
    csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "bestsellers.csv")
    analyzer = AmazonBookLanguageAnalyzer(csv_file)
    results = analyzer.run_full_analysis()
    print("=== AMAZON BESTSELLER LANGUAGE ANALYSIS KPI SUMMARY ===")
    for k, v in results["kpis"].items():
        print(f"  {k}: {v}")

    print("\n=== LANGUAGE DISTRIBUTION ===")
    for lang, metrics in results["languages"].items():
        print(f"  {lang}: {metrics['count']} books ({metrics['share_pct']}%) | Avg Rating: {metrics['avg_rating']} | Avg Words: {metrics['avg_word_count']}")

    print("\n=== GENRE LINGUISTIC COMPARISON ===")
    for g, metrics in results["genres"].items():
        print(f"  {g}: Avg Words: {metrics['avg_word_count']} | Subtitle %: {metrics['subtitle_pct']}% | Avg Rating: {metrics['avg_rating']}")

    print("\n=== CORRELATIONS ===")
    for pair, val in results["correlations"].items():
        print(f"  {pair}: {val}")
