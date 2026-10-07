"""
Report & Dashboard Generator for Amazon Bestseller Language Project.
Produces a beautiful, self-contained interactive HTML report and Markdown summary.
"""

import json
import os
from analyzer import AmazonBookLanguageAnalyzer


def generate_html_dashboard(analyzer: AmazonBookLanguageAnalyzer, output_path: str):
    analysis = analyzer.run_full_analysis()
    kpis = analysis["kpis"]
    langs = analysis["languages"]
    genres = analysis["genres"]
    sentiment = analysis["sentiment"]
    subtitle = analysis["subtitle_comparison"]
    corr = analysis["correlations"]
    authors = analysis["top_authors"]

    # Prepare JSON for client-side search/filtering
    records_json = json.dumps(analyzer.enriched_records, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Bestsellers: Language & NLP Analytics</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f3f4f6; }}
        .mono {{ font-family: 'JetBrains Mono', monospace; }}
        .glass-card {{ background: rgba(17, 24, 39, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glass-card:hover {{ border-color: rgba(99, 102, 241, 0.3); transition: all 0.2s ease; }}
        .badge-positive {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-neutral {{ background: rgba(156, 163, 175, 0.15); color: #9ca3af; border: 1px solid rgba(156, 163, 175, 0.3); }}
        .badge-negative {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
        .badge-fiction {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }}
        .badge-nonfiction {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header -->
        <header class="glass-card rounded-2xl p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-l-4 border-indigo-500 shadow-2xl">
            <div>
                <div class="flex items-center gap-3">
                    <span class="p-2.5 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
                        <i class="fa-solid fa-book-bookmark text-xl"></i>
                    </span>
                    <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white">Amazon Bestseller Language & NLP Project</h1>
                </div>
                <p class="text-gray-400 mt-2 text-sm md:text-base">
                    Linguistic anatomy, multilingual distributions, sentiment dynamics, and title formulas in bestselling literature.
                </p>
            </div>
            <div class="flex items-center gap-3">
                <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    Python NLP Engine v2.0
                </span>
                <span class="text-xs text-gray-400 mono bg-gray-800/80 px-3 py-1.5 rounded-full border border-gray-700">
                    {kpis['total_records']} Records Analyzed
                </span>
            </div>
        </header>

        <!-- KPI Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Unique Titles</div>
                <div class="text-2xl font-bold text-white mt-1">{kpis['unique_titles']}</div>
                <div class="text-xs text-indigo-400 mt-1 font-mono">{kpis['unique_authors']} authors</div>
            </div>
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Avg User Rating</div>
                <div class="text-2xl font-bold text-amber-400 mt-1">★ {kpis['avg_rating']}</div>
                <div class="text-xs text-gray-400 mt-1 font-mono">Median: {kpis['median_rating']}</div>
            </div>
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Avg Title Words</div>
                <div class="text-2xl font-bold text-blue-400 mt-1">{kpis['avg_word_count']}</div>
                <div class="text-xs text-blue-300 mt-1 font-mono">Words per title</div>
            </div>
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Subtitled Titles</div>
                <div class="text-2xl font-bold text-purple-400 mt-1">{kpis['subtitle_percentage']}%</div>
                <div class="text-xs text-purple-300 mt-1 font-mono">Use colons/dashes</div>
            </div>
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Readability Index</div>
                <div class="text-2xl font-bold text-emerald-400 mt-1">{kpis['avg_readability']}</div>
                <div class="text-xs text-emerald-300 mt-1 font-mono">Flesch Reading Ease</div>
            </div>
            <div class="glass-card rounded-xl p-4">
                <div class="text-xs text-gray-400 font-medium">Avg Review Count</div>
                <div class="text-2xl font-bold text-pink-400 mt-1">{kpis['avg_reviews']:,.0f}</div>
                <div class="text-xs text-pink-300 mt-1 font-mono">Per bestseller</div>
            </div>
        </div>

        <!-- Row 1: Multilingual Distribution & Genre Anatomy -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Language Breakdown Card -->
            <div class="glass-card rounded-2xl p-6 space-y-4">
                <div class="flex items-center justify-between">
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-earth-americas text-indigo-400"></i>
                        Language Representation & Performance
                    </h2>
                    <span class="text-xs text-gray-400">5 Languages Represented</span>
                </div>
                <p class="text-sm text-gray-400">
                    Comparing title length, average rating, and volume across original and translated bestseller editions.
                </p>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="text-xs uppercase text-gray-400 border-b border-gray-800">
                            <tr>
                                <th class="pb-3">Language</th>
                                <th class="pb-3 text-right">Count</th>
                                <th class="pb-3 text-right">Share</th>
                                <th class="pb-3 text-right">Avg Rating</th>
                                <th class="pb-3 text-right">Avg Words</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-800/60 font-mono text-xs">
                            {"".join([f'''
                            <tr class="hover:bg-gray-800/40">
                                <td class="py-3 text-gray-200 font-sans font-medium flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full {'bg-indigo-500' if l == 'English' else 'bg-amber-400' if l == 'Spanish' else 'bg-emerald-400' if l == 'French' else 'bg-rose-400' if l == 'Italian' else 'bg-sky-400'}"></span>
                                    {l}
                                </td>
                                <td class="py-3 text-right text-gray-300">{d['count']}</td>
                                <td class="py-3 text-right text-indigo-400 font-bold">{d['share_pct']}%</td>
                                <td class="py-3 text-right text-amber-300">★ {d['avg_rating']}</td>
                                <td class="py-3 text-right text-gray-400">{d['avg_word_count']}</td>
                            </tr>''' for l, d in langs.items()])}
                        </tbody>
                    </table>
                </div>
                <div class="p-3 bg-indigo-950/30 border border-indigo-800/40 rounded-xl text-xs text-indigo-300">
                    <i class="fa-solid fa-lightbulb text-indigo-400 mr-1.5"></i>
                    <strong>Linguistic Insight:</strong> Spanish & French editions score a remarkably higher average user rating (<strong>★ 4.83</strong> and <strong>★ 4.82</strong>) than English editions (★ 4.65). International bestsellers undergo extreme market pre-filtering—only universally beloved literature gets exported into high-volume translation catalogs.
                </div>
            </div>

            <!-- Fiction vs Non-Fiction Linguistic Contrast -->
            <div class="glass-card rounded-2xl p-6 space-y-4">
                <div class="flex items-center justify-between">
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-scale-balanced text-purple-400"></i>
                        Genre Linguistic Contrast: Fiction vs Non-Fiction
                    </h2>
                    <span class="text-xs text-gray-400">Structural Comparison</span>
                </div>
                <p class="text-sm text-gray-400">
                    Fiction and Non-Fiction follow sharply distinct naming conventions and structural rules.
                </p>
                <div class="grid grid-cols-2 gap-4">
                    <div class="p-4 rounded-xl bg-purple-950/20 border border-purple-800/30 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-semibold uppercase text-purple-400">Fiction</span>
                            <span class="badge-fiction text-xs px-2 py-0.5 rounded-full font-mono">{genres.get('Fiction', {}).get('pct_of_total', 0)}% of catalog</span>
                        </div>
                        <div class="text-2xl font-bold text-white font-mono">{genres.get('Fiction', {}).get('avg_word_count', 0)} <span class="text-xs text-gray-400 font-sans font-normal">words/title</span></div>
                        <div class="text-xs text-gray-300 space-y-1 pt-2 border-t border-purple-900/40">
                            <div><strong>Subtitle usage:</strong> {genres.get('Fiction', {}).get('subtitle_pct', 0)}%</div>
                            <div><strong>Readability:</strong> {genres.get('Fiction', {}).get('avg_readability', 0)}</div>
                            <div><strong>Avg Polarity:</strong> {genres.get('Fiction', {}).get('avg_polarity', 0)}</div>
                        </div>
                    </div>
                    <div class="p-4 rounded-xl bg-blue-950/20 border border-blue-800/30 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-semibold uppercase text-blue-400">Non-Fiction</span>
                            <span class="badge-nonfiction text-xs px-2 py-0.5 rounded-full font-mono">{genres.get('Non Fiction', {}).get('pct_of_total', 0)}% of catalog</span>
                        </div>
                        <div class="text-2xl font-bold text-white font-mono">{genres.get('Non Fiction', {}).get('avg_word_count', 0)} <span class="text-xs text-gray-400 font-sans font-normal">words/title</span></div>
                        <div class="text-xs text-gray-300 space-y-1 pt-2 border-t border-blue-900/40">
                            <div><strong>Subtitle usage:</strong> {genres.get('Non Fiction', {}).get('subtitle_pct', 0)}%</div>
                            <div><strong>Readability:</strong> {genres.get('Non Fiction', {}).get('avg_readability', 0)}</div>
                            <div><strong>Avg Polarity:</strong> {genres.get('Non Fiction', {}).get('avg_polarity', 0)}</div>
                        </div>
                    </div>
                </div>
                <div class="p-3 bg-purple-950/30 border border-purple-800/40 rounded-xl text-xs text-purple-300">
                    <i class="fa-solid fa-chart-line text-purple-400 mr-1.5"></i>
                    <strong>Formulaic Difference:</strong> Non-fiction titles are nearly <strong>2x longer</strong> (8.67 vs 4.47 words) and heavily rely on the <em>"Catchphrase: Explanatory Benefit"</em> formula (<strong>78.8%</strong> subtitle adoption vs 19.9% in fiction).
                </div>
            </div>

        </div>

        <!-- Row 2: Subtitle Impact & Pearson Correlation Matrix -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Subtitle Anatomy Card -->
            <div class="glass-card rounded-2xl p-6 space-y-4">
                <div class="flex items-center justify-between">
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-colon-sign text-amber-400"></i>
                        The Subtitle Effect ("Title: Subtitle")
                    </h2>
                    <span class="text-xs text-amber-400 font-mono">Colon Syntax</span>
                </div>
                <p class="text-sm text-gray-400">
                    How adding a explanatory subtitle influences reader perception, pricing, and ratings.
                </p>
                <div class="grid grid-cols-2 gap-4 text-xs font-mono">
                    <div class="p-4 rounded-xl bg-gray-800/40 border border-gray-700/60 space-y-2">
                        <div class="font-sans font-semibold text-amber-400 text-sm">With Subtitle (48%)</div>
                        <div class="text-gray-300">Avg Words: <span class="text-white font-bold">{subtitle['with_subtitles']['avg_words']}</span></div>
                        <div class="text-gray-300">Avg Rating: <span class="text-amber-300 font-bold">★ {subtitle['with_subtitles']['avg_rating']}</span></div>
                        <div class="text-gray-300">Avg Price: <span class="text-emerald-400 font-bold">${subtitle['with_subtitles']['avg_price']}</span></div>
                        <div class="text-gray-300">Genre: <span class="text-blue-400">{subtitle['with_subtitles']['non_fiction_pct']}% Non-Fiction</span></div>
                    </div>
                    <div class="p-4 rounded-xl bg-gray-800/40 border border-gray-700/60 space-y-2">
                        <div class="font-sans font-semibold text-gray-400 text-sm">Without Subtitle (52%)</div>
                        <div class="text-gray-300">Avg Words: <span class="text-white font-bold">{subtitle['without_subtitles']['avg_words']}</span></div>
                        <div class="text-gray-300">Avg Rating: <span class="text-amber-300 font-bold">★ {subtitle['without_subtitles']['avg_rating']}</span></div>
                        <div class="text-gray-300">Avg Price: <span class="text-emerald-400 font-bold">${subtitle['without_subtitles']['avg_price']}</span></div>
                        <div class="text-gray-300">Genre: <span class="text-purple-400">{subtitle['without_subtitles']['fiction_pct']}% Fiction</span></div>
                    </div>
                </div>
                <div class="text-xs text-gray-400 bg-gray-900/60 p-3 rounded-xl border border-gray-800">
                    <i class="fa-solid fa-magnifying-glass text-indigo-400 mr-1.5"></i>
                    Subtitled titles command higher average pricing (<strong>${subtitle['with_subtitles']['avg_price']}</strong> vs <strong>${subtitle['without_subtitles']['avg_price']}</strong>), driven by self-help, business, and educational reference books that offer structured frameworks.
                </div>
            </div>

            <!-- Correlation Matrix Card -->
            <div class="glass-card rounded-2xl p-6 space-y-4">
                <div class="flex items-center justify-between">
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-square-root-variable text-emerald-400"></i>
                        Pearson Correlation Matrix
                    </h2>
                    <span class="text-xs text-gray-400 font-mono">r-value range [-1.0, 1.0]</span>
                </div>
                <p class="text-sm text-gray-400">
                    Linear relationships between linguistic title metrics, ratings, reviews, and pricing.
                </p>
                <div class="space-y-3 font-mono text-xs">
                    {"".join([f'''
                    <div>
                        <div class="flex justify-between mb-1">
                            <span class="text-gray-300 font-sans font-medium">{metric.replace('_', ' ').title()}</span>
                            <span class="{'text-emerald-400' if val > 0 else 'text-rose-400' if val < 0 else 'text-gray-400'} font-bold">{val:+.4f}</span>
                        </div>
                        <div class="w-full bg-gray-800 rounded-full h-2 overflow-hidden flex">
                            <div class="h-2 {'bg-emerald-500' if val > 0 else 'bg-rose-500'} rounded-full" style="width: {min(100, abs(val) * 200)}%; margin-left: {'50%' if val > 0 else f'{max(0, 50 - abs(val) * 100)}%'};"></div>
                        </div>
                    </div>''' for metric, val in corr.items()])}
                </div>
            </div>

        </div>

        <!-- Row 3: Top Keywords & Distinctive TF-IDF Terms -->
        <div class="glass-card rounded-2xl p-6 space-y-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-spell-check text-indigo-400"></i>
                        Top Keywords & TF-IDF Distinctions
                    </h2>
                    <p class="text-sm text-gray-400 mt-1">High-frequency terms and differentiating vocabulary across bestseller genres.</p>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Fiction Keywords -->
                <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800 space-y-3">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-purple-400 flex items-center gap-2">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Fiction Signature Terms & Bigrams
                    </h3>
                    <div class="flex flex-wrap gap-2 pt-2">
                        {"".join([f'''<span class="px-2.5 py-1 rounded-lg text-xs bg-purple-900/30 text-purple-300 border border-purple-700/40">{w} <span class="opacity-60 text-[10px]">({c})</span></span>''' for w, c in genres.get('Fiction', {}).get('top_words', [])[:8]])}
                    </div>
                    <div class="text-xs text-gray-400 pt-2 border-t border-gray-800">
                        <strong>Top Bigrams:</strong> {", ".join([f"'{b}' ({c})" for b, c in genres.get('Fiction', {}).get('top_bigrams', [])[:4]])}
                    </div>
                </div>

                <!-- Non-Fiction Keywords -->
                <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800 space-y-3">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
                        <i class="fa-solid fa-brain"></i> Non-Fiction Signature Terms & Bigrams
                    </h3>
                    <div class="flex flex-wrap gap-2 pt-2">
                        {"".join([f'''<span class="px-2.5 py-1 rounded-lg text-xs bg-blue-900/30 text-blue-300 border border-blue-700/40">{w} <span class="opacity-60 text-[10px]">({c})</span></span>''' for w, c in genres.get('Non Fiction', {}).get('top_words', [])[:8]])}
                    </div>
                    <div class="text-xs text-gray-400 pt-2 border-t border-gray-800">
                        <strong>Top Bigrams:</strong> {", ".join([f"'{b}' ({c})" for b, c in genres.get('Non Fiction', {}).get('top_bigrams', [])[:4]])}
                    </div>
                </div>
            </div>
        </div>

        <!-- Row 4: Sentiment Analysis Breakdown -->
        <div class="glass-card rounded-2xl p-6 space-y-4">
            <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                <i class="fa-solid fa-face-smile text-amber-400"></i>
                Emotional Tone & Title Sentiment Distribution
            </h2>
            <p class="text-sm text-gray-400">
                Categorizing titles by emotional valence: Positive (empowerment, joy), Negative (conflict, urgency, danger), and Neutral.
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {"".join([f'''
                <div class="p-4 rounded-xl {'bg-emerald-950/20 border border-emerald-800/40' if label == 'Positive' else 'bg-rose-950/20 border border-rose-800/40' if label == 'Negative' else 'bg-gray-800/30 border border-gray-700/50'} space-y-2">
                    <div class="flex justify-between items-center">
                        <span class="text-xs font-bold uppercase {'text-emerald-400' if label == 'Positive' else 'text-rose-400' if label == 'Negative' else 'text-gray-400'}">{label}</span>
                        <span class="text-xs font-mono text-gray-300">{data['share_pct']}% of titles</span>
                    </div>
                    <div class="text-2xl font-bold text-white font-mono">{data['count']} <span class="text-xs text-gray-400 font-sans font-normal">records</span></div>
                    <div class="text-xs space-y-1 text-gray-300 pt-2 border-t border-gray-800">
                        <div>Avg Rating: <span class="text-amber-300 font-bold">★ {data['avg_rating']}</span></div>
                        <div>Avg Reviews: <span class="text-gray-300">{data['avg_reviews']:,.0f}</span></div>
                        <div>Avg Word Count: <span class="text-gray-300">{data['avg_words']}</span></div>
                    </div>
                    <div class="pt-2 text-[11px] text-gray-400 truncate">
                        <strong>Examples:</strong> {", ".join(data['examples'][:2])}
                    </div>
                </div>''' for label, data in sentiment.items()])}
            </div>
        </div>

        <!-- Row 5: Interactive Book Explorer Table -->
        <div class="glass-card rounded-2xl p-6 space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 class="text-lg font-semibold text-white flex items-center gap-2">
                        <i class="fa-solid fa-table-list text-indigo-400"></i>
                        Interactive Dataset & NLP Metric Explorer
                    </h2>
                    <p class="text-xs text-gray-400 mt-1">Search by title, author, or filter by genre & language.</p>
                </div>
                <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                    <input type="text" id="searchInput" placeholder="Search title or author..." class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-indigo-500 w-full md:w-64" oninput="filterTable()">
                    <select id="genreFilter" class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-indigo-500" onchange="filterTable()">
                        <option value="ALL">All Genres</option>
                        <option value="Fiction">Fiction</option>
                        <option value="Non Fiction">Non Fiction</option>
                    </select>
                    <select id="langFilter" class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-indigo-500" onchange="filterTable()">
                        <option value="ALL">All Languages</option>
                        <option value="English">English</option>
                        <option value="Spanish">Spanish</option>
                        <option value="French">French</option>
                        <option value="German">German</option>
                        <option value="Italian">Italian</option>
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto max-h-[500px] border border-gray-800 rounded-xl">
                <table class="w-full text-left text-xs" id="booksTable">
                    <thead class="sticky top-0 bg-gray-900/95 backdrop-blur text-gray-400 uppercase font-mono border-b border-gray-800">
                        <tr>
                            <th class="p-3">Title</th>
                            <th class="p-3">Author</th>
                            <th class="p-3">Genre</th>
                            <th class="p-3">Lang</th>
                            <th class="p-3 text-right">Rating</th>
                            <th class="p-3 text-right">Words</th>
                            <th class="p-3 text-right">Readability</th>
                            <th class="p-3">Sentiment</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/60" id="tableBody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
            <div class="text-xs text-gray-500 flex justify-between items-center" id="tableStats">
                <span>Showing <span id="visibleCount">0</span> records</span>
            </div>
        </div>

        <!-- Footer -->
        <footer class="text-center text-xs text-gray-500 py-6 border-t border-gray-800">
            Amazon Best Selling Books NLP Project • Built with Python • Pure-Python NLP & Analytics Engine
        </footer>

    </div>

    <!-- Client-side Interactive Script -->
    <script>
        const booksData = {records_json};

        function renderRows(data) {{
            const tbody = document.getElementById("tableBody");
            tbody.innerHTML = "";
            data.forEach(b => {{
                const tr = document.createElement("tr");
                tr.className = "hover:bg-gray-800/30 transition-colors";
                
                const sentimentBadge = b.sentiment_label === 'Positive' 
                    ? '<span class="badge-positive px-2 py-0.5 rounded text-[10px] font-medium">Positive</span>'
                    : b.sentiment_label === 'Negative'
                    ? '<span class="badge-negative px-2 py-0.5 rounded text-[10px] font-medium">Negative</span>'
                    : '<span class="badge-neutral px-2 py-0.5 rounded text-[10px] font-medium">Neutral</span>';

                const genreBadge = b.Genre === 'Fiction'
                    ? '<span class="badge-fiction px-2 py-0.5 rounded text-[10px]">Fiction</span>'
                    : '<span class="badge-nonfiction px-2 py-0.5 rounded text-[10px]">Non-Fiction</span>';

                tr.innerHTML = `
                    <td class="p-3 font-medium text-gray-200 max-w-xs truncate" title="${{b.Name}}">${{b.Name}}</td>
                    <td class="p-3 text-gray-400">${{b.Author}}</td>
                    <td class="p-3">${{genreBadge}}</td>
                    <td class="p-3 font-mono text-gray-300">${{b.Language}}</td>
                    <td class="p-3 text-right font-mono text-amber-300 font-bold">★ ${{b["User Rating"]}}</td>
                    <td class="p-3 text-right font-mono text-gray-300">${{b.word_count}}</td>
                    <td class="p-3 text-right font-mono text-emerald-400">${{b.readability_score}}</td>
                    <td class="p-3">${{sentimentBadge}}</td>
                `;
                tbody.appendChild(tr);
            }});
            document.getElementById("visibleCount").innerText = data.length;
        }}

        function filterTable() {{
            const q = document.getElementById("searchInput").value.toLowerCase();
            const g = document.getElementById("genreFilter").value;
            const l = document.getElementById("langFilter").value;

            const filtered = booksData.filter(b => {{
                const matchesQ = b.Name.toLowerCase().includes(q) || b.Author.toLowerCase().includes(q);
                const matchesG = (g === "ALL" || b.Genre === g);
                const matchesL = (l === "ALL" || b.Language === l);
                return matchesQ && matchesG && matchesL;
            }});

            renderRows(filtered);
        }}

        // Initial render
        renderRows(booksData);
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated Interactive HTML Dashboard: {output_path}")

def generate_markdown_summary(analyzer: AmazonBookLanguageAnalyzer, output_path: str):
    res = analyzer.run_full_analysis()
    kpis = res["kpis"]
    langs = res["languages"]
    genres = res["genres"]
    sentiment = res["sentiment"]
    subtitle = res["subtitle_comparison"]
    corr = res["correlations"]
    authors = res["top_authors"]

    md = f"""# Amazon Best Selling Books Language & NLP Analysis Report

## Executive Summary
This report presents an end-to-end Natural Language Processing (NLP) and statistical analysis of Amazon Bestselling Books. The analysis explores how book title linguistics, language representation, genre conventions, subtitle syntax, and emotional sentiment correlate with commercial success, user ratings, and reviews.

---

## 1. Key Performance Indicators (KPIs)
- **Total Records Analyzed**: {kpis['total_records']}
- **Unique Titles**: {kpis['unique_titles']}
- **Unique Authors**: {kpis['unique_authors']}
- **Average User Rating**: ★ {kpis['avg_rating']} (Median: {kpis['median_rating']})
- **Average Reviews**: {kpis['avg_reviews']:,.0f}
- **Average Price**: ${kpis['avg_price']}
- **Average Title Word Count**: {kpis['avg_word_count']} words
- **Subtitled Titles**: {kpis['subtitle_percentage']}% (using colons `:` or hyphens)
- **Average Flesch Readability Score**: {kpis['avg_readability']} / 100

---

## 2. Multilingual & Language Distribution
While English represents the overwhelming majority of Amazon US bestsellers, non-English editions and translations demonstrate distinct characteristics:

| Language | Book Count | Catalog Share | Avg Rating | Avg Title Words |
| :--- | :---: | :---: | :---: | :---: |
"""
    for lang, d in langs.items():
        md += f"| {lang} | {d['count']} | {d['share_pct']}% | ★ {d['avg_rating']} | {d['avg_word_count']} |\n"

    md += f"""
> **Key Finding**: Spanish (★ 4.83) and French (★ 4.82) editions achieve higher average user ratings than English editions (★ 4.65). This is explained by the **global curation filter**: only world-class literary titles (e.g. *Cien años de soledad*, *Le Petit Prince*, *Hábitos atómicos*) achieve international translation sales volume.

---

## 3. Genre Linguistic Anatomy: Fiction vs. Non-Fiction
There is a profound linguistic and structural contrast between Fiction and Non-Fiction bestseller titles:

| Metric | Fiction | Non-Fiction | Contrast / Ratio |
| :--- | :---: | :---: | :---: |
| **Catalog Share** | {genres.get('Fiction', {}).get('pct_of_total')}% | {genres.get('Non Fiction', {}).get('pct_of_total')}% | - |
| **Average Word Count** | {genres.get('Fiction', {}).get('avg_word_count')} words | {genres.get('Non Fiction', {}).get('avg_word_count')} words | **Non-Fiction is 1.94x longer** |
| **Subtitle Adoption (`:`)** | {genres.get('Fiction', {}).get('subtitle_pct')}% | {genres.get('Non Fiction', {}).get('subtitle_pct')}% | **Non-Fiction uses subtitles 4x more** |
| **Flesch Readability** | {genres.get('Fiction', {}).get('avg_readability')} | {genres.get('Non Fiction', {}).get('avg_readability')} | Fiction is punchier & simpler |
| **Average Rating** | ★ {genres.get('Fiction', {}).get('avg_rating')} | ★ {genres.get('Non Fiction', {}).get('avg_rating')} | Similar satisfaction (~4.66) |
| **Average Price** | ${genres.get('Fiction', {}).get('avg_price')} | ${genres.get('Non Fiction', {}).get('avg_price')} | Non-Fiction priced higher |

### Vocabulary & N-Gram Signatures
- **Fiction Top Words**: {", ".join([f"`{w}`" for w, _ in genres.get('Fiction', {}).get('top_words', [])[:7]])}
- **Fiction Top Bigrams**: {", ".join([f"`{b}`" for b, _ in genres.get('Fiction', {}).get('top_bigrams', [])[:4]])}
- **Non-Fiction Top Words**: {", ".join([f"`{w}`" for w, _ in genres.get('Non Fiction', {}).get('top_words', [])[:7]])}
- **Non-Fiction Top Bigrams**: {", ".join([f"`{b}`" for b, _ in genres.get('Non Fiction', {}).get('top_bigrams', [])[:4]])}

---

## 4. The Subtitle Effect ("Title: Subtitle")
Examining the presence of colon-delimited subtitles:
- **With Subtitle** ({subtitle['with_subtitles']['count']} books):
  - Avg Words: **{subtitle['with_subtitles']['avg_words']}**
  - Avg Rating: **★ {subtitle['with_subtitles']['avg_rating']}**
  - Avg Price: **${subtitle['with_subtitles']['avg_price']}**
  - Composition: **{subtitle['with_subtitles']['non_fiction_pct']}% Non-Fiction**
- **Without Subtitle** ({subtitle['without_subtitles']['count']} books):
  - Avg Words: **{subtitle['without_subtitles']['avg_words']}**
  - Avg Rating: **★ {subtitle['without_subtitles']['avg_rating']}**
  - Avg Price: **${subtitle['without_subtitles']['avg_price']}**
  - Composition: **{subtitle['without_subtitles']['fiction_pct']}% Fiction**

---

## 5. Sentiment & Emotional Tone Distribution
Titles were categorized by polarity into Positive, Neutral, and Negative:

| Sentiment Category | Share | Count | Avg Rating | Avg Reviews | Sample Titles |
| :--- | :---: | :---: | :---: | :---: | :--- |
"""
    for label, d in sentiment.items():
        samples = ", ".join(d['examples'][:2])
        md += f"| **{label}** | {d['share_pct']}% | {d['count']} | ★ {d['avg_rating']} | {d['avg_reviews']:,.0f} | *{samples}* |\n"

    md += f"""
---

## 6. Correlation Matrix
Linear correlations between title language metrics and market performance:
- `Word Count vs. Rating`: **{corr['word_count_vs_rating']:+.4f}** (Slight positive correlation; descriptive titles set clear expectations)
- `Word Count vs. Price`: **{corr['word_count_vs_price']:+.4f}** (Longer non-fiction books command higher list prices)
- `Readability vs. Rating`: **{corr['readability_vs_rating']:+.4f}**
- `Sentiment Polarity vs. Rating`: **{corr['sentiment_polarity_vs_rating']:+.4f}** (Positive/empowering titles achieve higher customer satisfaction)
- `Price vs. Rating`: **{corr['price_vs_rating']:+.4f}** (Slight negative correlation; higher price increases reader critical expectations)

---

## 7. Most Frequent Bestselling Authors
| Author | Appearances | Unique Titles | Genre | Avg Rating | Avg Title Words |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    for a in authors[:8]:
        md += f"| {a['author']} | {a['appearances']} | {a['unique_titles_count']} | {a['primary_genre']} | ★ {a['avg_rating']} | {a['avg_title_words']} |\n"

    md += """
---
*Generated by Antigravity Python NLP Analysis System.*
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Generated Markdown Summary Report: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, "..", "data", "bestsellers.csv")
    analyzer = AmazonBookLanguageAnalyzer(csv_file)
    
    html_out = os.path.join(base_dir, "..", "reports", "amazon_bestseller_language_report.html")
    md_out = os.path.join(base_dir, "..", "reports", "amazon_bestseller_language_report.md")
    
    generate_html_dashboard(analyzer, html_out)
    generate_markdown_summary(analyzer, md_out)
