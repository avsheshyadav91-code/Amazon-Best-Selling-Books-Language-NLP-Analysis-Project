#!/usr/bin/env python3
"""
Amazon Bestselling Books: Language & NLP Project
Main Entry Point
"""
import os
import sys
# Ensure src is in sys.path
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from analyzer import AmazonBookLanguageAnalyzer
from generate_report import generate_html_dashboard, generate_markdown_summary
from prepare_dataset import DATASET_PATH, generate_dataset

def run_pipeline():
    print("=" * 70)
    print("   AMAZON BESTSELLING BOOKS - LANGUAGE & NLP ANALYSIS PIPELINE")
    print("=" * 70)
    # 1. Dataset Generation / Check
    if not os.path.exists(DATASET_PATH):
        print("\n[Step 1/3] Generating dataset...")
        generate_dataset()
    else:
        print(f"\n[Step 1/3] Dataset verified: {DATASET_PATH}")
    # 2. Linguistic & Statistical Analysis
    print("\n[Step 2/3] Extracting linguistic features & running NLP analysis...")
    analyzer = AmazonBookLanguageAnalyzer(DATASET_PATH)
    results = analyzer.run_full_analysis()
    kpis = results["kpis"]
    langs = results["languages"]
    genres = results["genres"]
    corr = results["correlations"]
    print("\n" + "-" * 70)
    print("📊 KEY METRICS SUMMARY:")
    print(f"  • Total Records Analyzed:     {kpis['total_records']}")
    print(f"  • Unique Titles:              {kpis['unique_titles']} across {kpis['unique_authors']} authors")
    print(f"  • Overall Average Rating:     ★ {kpis['avg_rating']} (Median: {kpis['median_rating']})")
    print(f"  • Average Title Word Count:   {kpis['avg_word_count']} words")
    print(f"  • Titles with Subtitles:      {kpis['subtitle_percentage']}%")
    print(f"  • Avg Flesch Readability:     {kpis['avg_readability']} / 100")
    print(f"  • Average Review Volume:      {kpis['avg_reviews']:,.0f}")
    print("\n🌍 MULTILINGUAL DISTRIBUTION:")
    for lang, d in langs.items():
        print(f"  • {lang:<10}: {d['count']:>3} books ({d['share_pct']:>5}%) | Avg Rating: ★ {d['avg_rating']} | Avg Words: {d['avg_word_count']}")


if __name__ == "__main__":
    run_pipeline()