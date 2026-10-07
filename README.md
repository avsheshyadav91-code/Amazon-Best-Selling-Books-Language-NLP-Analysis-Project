# Amazon Best Selling Books — Language & NLP Analysis Project

An end-to-end Python project that performs Natural Language Processing (NLP), linguistic feature engineering, and statistical exploratory data analysis (EDA) on Amazon Bestselling Books.

---

## 📌 Project Overview

This project investigates the linguistic patterns and language dynamics behind bestselling books on Amazon:
1. **Linguistic Title Anatomy**: Word counts, character lengths, subtitle syntax (`:` and `-`), title case ratios, and Flesch readability indices.
2. **Genre Contrasts**: How naming conventions differ between **Fiction** (punchy, evocative) and **Non-Fiction** (benefit-driven, descriptive).
3. **Multilingual Representation**: Performance and rating distributions across English, Spanish, French, Italian, and German editions.
4. **Sentiment & Tone Analysis**: Title emotional valence (Positive, Negative, Neutral) and its relationship with customer ratings and review volume.
5. **Statistical Correlations**: Pearson correlation coefficients between title length, sentiment, readability, pricing, and ratings.

---

## 📁 Repository Structure

```
amazon_bestsellers_nlp/
├── data/
│   └── bestsellers.csv               # Bestseller records with ratings, reviews, genre, language
├── src/
│   ├── prepare_dataset.py            # Dataset generator & catalog loader
│   ├── nlp_engine.py                 # Pure-Python NLP, sentiment, readability & n-gram extractor
│   ├── analyzer.py                   # Statistical engine (correlations, KPIs, genre breakdowns)
│   └── generate_report.py            # Produces interactive HTML dashboard & Markdown reports
├── reports/
│   ├── amazon_bestseller_language_report.html # Interactive visual dashboard with live search/filters
│   └── amazon_bestseller_language_report.md   # Detailed summary Markdown document
├── tests/
│   └── test_analysis.py              # Unit tests for the NLP and statistical functions
├── main.py                           # Single-command pipeline runner
└── README.md                         # Project documentation
```

---

## 🚀 Quick Start

### 1. Requirements
The project is built using Python's standard library (`math`, `re`, `csv`, `collections`, `defaultdict`), so it runs immediately out-of-the-box with **zero external pip dependencies required**.

### 2. Run the Full Pipeline
```bash
cd /Users/avshesh/.gemini/antigravity/scratch/amazon_bestsellers_nlp
python3 main.py
```

### 3. Run the Unit Tests
```bash
python3 -m unittest discover -s tests
```

### 4. View the Interactive Dashboard
Open `reports/amazon_bestseller_language_report.html` in your web browser:
```bash
open reports/amazon_bestseller_language_report.html
```

---

## 🔍 Key Findings & Linguistic Insights

| Metric / Dimension | Observation | Linguistic Interpretation |
| :--- | :--- | :--- |
| **Non-Fiction vs Fiction Length** | **8.67** vs **4.47** words | Non-fiction titles are nearly **2x longer**, utilizing explanatory subtitles to communicate explicit reader value. |
| **Subtitle Adoption (`:`)** | **78.8%** in Non-Fiction vs **19.9%** in Fiction | The *"Hook: Explanatory Benefit"* formula is the dominant naming convention in business, psychology, and self-help bestsellers. |
| **Multilingual Ratings** | Spanish (★ 4.83) & French (★ 4.82) vs English (★ 4.65) | Foreign language editions undergo an extreme global curation filter—only universally beloved literature gets exported into international bestseller tiers. |
| **Title Length vs Rating** | Correlation: **+0.2021** | Informative titles set clearer expectations for readers, correlating with slightly higher user ratings. |
| **Price vs Rating** | Correlation: **-0.1690** | Higher-priced books face higher scrutiny and critical expectations from buyers. |
| **Sentiment Polarity vs Rating** | Correlation: **+0.1264** | Positively framed, empowering titles achieve slightly higher review ratings. |

---

## 🛠️ Extending with Advanced NLP Libraries (Optional)

If you have `pandas`, `nltk`, `spacy`, or `scikit-learn` installed in your environment, you can extend this pipeline:
- **Topic Modeling (LDA / BERTopic)** on full book descriptions and reader reviews.
- **Transformers (Hugging Face)**: Zero-shot classification using `facebook/bart-large-mnli` to classify emotional appeal (e.g., *Inspirational*, *Thrilling*, *Educational*).
- **POS Tagging with spaCy**: Measure the exact ratio of Imperative Verbs vs Abstract Nouns in non-fiction titles.
