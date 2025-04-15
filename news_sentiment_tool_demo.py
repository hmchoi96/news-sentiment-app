"""
📊 Wiserbond News Sentiment Analyzer

WHY – Why was this built?
Economic news is everywhere—but understanding what truly matters and how it's being perceived can be hard,
especially for people without a background in finance. Instead of reading through dozens of articles,
this tool helps users quickly grasp the emotional tone and key narratives surrounding major economic topics.

HOW – How does it work?
The tool collects recent news articles on selected economic topics, filters them using targeted keywords,
classifies them by sentiment (positive/negative) using NLP, and generates concise summaries for both sides.
It also visualizes the sentiment distribution to make interpretation easier.

WHAT – What does it do?
- Gathers news on selected topics: `tariff`, `trump`, `inflation`, `fed`, `unemployment`
- Filters out unrelated content using topic-specific keyword lists
- Performs AI-based sentiment analysis and summarization
- Separates and summarizes positive and negative coverage
- Visualizes the emotional tone with a simple bar chart

This tool is especially helpful for non-finance professionals, strategy teams, and policymakers
who need clear, unbiased insights on complex economic signals—without reading everything.
Created by: Hyun Myung (Jamie) Choi, Wiserbond Research

"""

import requests
from transformers import pipeline
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# ✅ API Key
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'

# ✅ Keyword Setting
TOPIC_SETTINGS = {
    "tariff": {
        "search_term": "tariff",
        "keywords": [
            "tariff", "tariffs", "duties", "customs", "import", "export", "trade",
            "sanction", "levy", "protectionism", "trade war", "tariff hike",
            "border tax", "retaliatory", "quota"
        ]
    },
    "trump": {
        "search_term": "Donald Trump",
        "keywords": [
            "trump", "donald", "republican", "president", "white house",
            "gop", "maga", "trump administration", "former president",
            "2024 election", "trump rally", "indictment", "mar-a-lago"
        ]
    },
    "inflation": {
        "search_term": "inflation",
        "keywords": ["inflation", "price index", "cpi", "ppi", "consumer price", "core inflation",
        "cost of living", "rising prices", "inflationary pressure", 
        "interest rates", "wage growth", "monetary tightening", "headline inflation", 
        "economic overheating", "sticky inflation", "disinflation"]
    },
    "fed": {
        "search_term": "fed",
        "keywords": [
        "federal reserve", "interest rate", "rate hike", "rate cut", "jerome powell",
        "fed", "fomc", "central bank", "tightening", "pause", "pivot", "monetary policy"
        ]
    },
    "unemployment": {
        "search_term": "employment",
        "keywords": [
        "unemployment", "employment", "jobless", "nonfarm payroll", "labor market", "jobs report",
        "layoffs", "job cuts", "hiring freeze", "job growth", "employment rate"
        ]
    }
}

FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

def get_news(search_term, max_pages=4, page_size=100):
    all_articles = []
    for page in range(1, max_pages + 1):
        url = (
            f'https://newsapi.org/v2/everything?q={search_term}'
            f'&from={FROM_DATE}&language=en&pageSize={page_size}&page={page}&sortBy=publishedAt'
            f'&apiKey={NEWS_API_KEY}'
        )
        response = requests.get(url)
        data = response.json()
        if 'articles' in data:
            all_articles.extend(data['articles'])
        if len(data.get("articles", [])) < page_size:
            break
    return all_articles

def contains_keywords(text, keywords):
    text = (text or "").lower()
    return sum(k in text for k in keywords) >= 1  # 최소 한 개 이상 포함

def filter_articles(articles, keywords, max_filtered=50):
    seen_sources = set()
    filtered = []
    for a in articles:
        source = a['source']['name']
        title = a['title']
        desc = a['description']
        if not title or not desc:
            continue
        combined = f"{title} {desc}"
        if contains_keywords(combined, keywords) and source not in seen_sources:
            filtered.append(a)
            seen_sources.add(source)
        if len(filtered) >= max_filtered:
            break
    return filtered

def run_sentiment_analysis(articles):
    sentiment_pipeline = pipeline("sentiment-analysis")
    results = []
    for a in articles:
        text = f"{a['title']}. {a['description'] or ''}"
        sentiment = sentiment_pipeline(text)[0]
        results.append({
            "source": a['source']['name'],
            "title": a['title'],
            "description": a['description'],
            "sentiment": sentiment['label'],
            "score": round(sentiment['score'], 2)
        })
    return results

def summarize_by_sentiment(articles, sentiment_label, keywords):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a['sentiment'] == sentiment_label and a['description'] and contains_keywords(f"{a['description']} {a['title']}", keywords)
    ]
    if not texts:
        return "No related news articles found."
    joined = "\n".join(texts)
    max_tokens = 1000
    truncated = " ".join(joined.split()[:max_tokens])
    try:
        summary = summarizer(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except:
        return "Summarization failed."

def draw_sentiment_chart(articles):
    total = len(articles)
    if total == 0:
        print("No articles to visualize.")
        return
    from collections import Counter
    counts = Counter([a['sentiment'] for a in articles])
    labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
    colors = ['#d9534f', '#f7f1f1', '#bfaeff']
    values = [counts.get(label, 0) / total * 100 for label in labels]

    plt.figure(figsize=(8, 1.2))
    plt.barh(['Sentiment'], values, color=colors, edgecolor='black', height=0.4, left=[0, values[0], values[0]+values[1]])
    for i, (v, label) in enumerate(zip(values, labels)):
        if v > 0:
            plt.text(sum(values[:i]) + v/2, 0, f"{label.title()} {int(v)}%", va='center', ha='center', fontsize=9)
    plt.axis('off')
    plt.title("Sentiment Breakdown")
    plt.show()

def run_analysis():
    while True:
        topic = input("📝 Enter a keyword (Available: tariff, trump, inflation, fed, unemployment): ").strip().lower()
        if topic not in TOPIC_SETTINGS:
            print(f"❌ '{topic}' is not available. Please try again.")
            continue

        setting = TOPIC_SETTINGS[topic]
        search_term = setting['search_term']
        filter_keywords = setting['keywords']

        raw = get_news(search_term)
        filtered = filter_articles(raw, filter_keywords)
        analyzed = run_sentiment_analysis(filtered)

        pos_summary = summarize_by_sentiment(analyzed, 'POSITIVE', filter_keywords)
        neg_summary = summarize_by_sentiment(analyzed, 'NEGATIVE', filter_keywords)

        print(f"\n📅 News Summary for the Period: {FROM_DATE} to {datetime.today().strftime('%Y-%m-%d')}")
        print(f"📊 Analyzed {len(analyzed)} articles from {len(set(a['source'] for a in analyzed))} news sources.\n")
        print("🤖 AI Summary:")
        print(f"❗ Negative News: {neg_summary}")
        print(f"✅ Positive News: {pos_summary}")

        draw_sentiment_chart(analyzed)

        again = input("\n🔁 Would you like to analyze another topic? (yes / no): ").strip().lower()
        if again in ['no', 'n']:
            print("👋 Analysis finished. Have a great day!")
            break

# execute
if __name__ == "__main__":
    run_analysis()
