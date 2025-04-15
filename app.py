import streamlit as st
from news_sentiment_tool_demo import (
    TOPIC_SETTINGS,
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment
)
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

# Page setup
st.set_page_config(page_title="Wiserbond News Sentiment Analyzer", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")
st.markdown("Get a quick emotional and narrative breakdown of recent economic news.")

# Visualization function
def draw_sentiment_chart(articles):
    total = len(articles)
    if total == 0:
        st.warning("No articles to visualize.")
        return

    counts = Counter([a['sentiment'] for a in articles])
    labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
    colors = ['#d9534f', '#f7f1f1', '#bfaeff']
    values = [counts.get(label, 0) / total * 100 for label in labels]

    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.barh(['Sentiment'], values, color=colors, edgecolor='black', height=0.4,
            left=[0, values[0], values[0]+values[1]])
    for i, (v, label) in enumerate(zip(values, labels)):
        if v > 0:
            ax.text(sum(values[:i]) + v/2, 0, f"{label.title()} {int(v)}%", 
                    va='center', ha='center', fontsize=9)
    ax.axis('off')
    ax.set_title("Sentiment Breakdown")
    st.pyplot(fig)

# Topic selection
topic = st.selectbox("🔍 Select a topic to analyze", list(TOPIC_SETTINGS.keys()))

# Run analysis
if st.button("Run Analysis"):
    with st.spinner("Collecting and analyzing news..."):
        setting = TOPIC_SETTINGS[topic]
        raw = get_news(setting['search_term'])
        filtered = filter_articles(raw, setting['keywords'])
        analyzed = run_sentiment_analysis(filtered)

        # Display results
        st.subheader("🤖 AI Summary")
        pos_summary = summarize_by_sentiment(analyzed, 'POSITIVE', setting['keywords'])
        neg_summary = summarize_by_sentiment(analyzed, 'NEGATIVE', setting['keywords'])

        st.markdown(f"**✅ Positive Coverage:** {pos_summary}")
        st.markdown(f"**❗ Negative Coverage:** {neg_summary}")

        # Show sentiment distribution
        st.subheader("📊 Sentiment Distribution")
        draw_sentiment_chart(analyzed)
