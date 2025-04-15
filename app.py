import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS,
)

# ------------------------------
# 분석 실행 함수
# ------------------------------
def analyze_topic(topic):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    keywords = setting["keywords"]
    raw = get_news(search_term)
    filtered = filter_articles(raw, keywords)
    analyzed = run_sentiment_analysis(filtered)

    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    pos_news = [
        {"source": a["source"], "title": a["title"], "summary": a["description"]}
        for a in analyzed
        if a["sentiment"] == "POSITIVE"
    ]
    neg_news = [
        {"source": a["source"], "title": a["title"], "summary": a["description"]}
        for a in analyzed
        if a["sentiment"] == "NEGATIVE"
    ]

    # 전문가 요약 포맷 개선 (줄바꿈 포함)
    expert_summary = (
        "✅ **Positive Insight**\n\n"
        + summarize_by_sentiment(analyzed, "POSITIVE", keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    st.session_state["topic"] = topic
    st.session_state["sentiment_counts"] = sentiment_counts
    st.session_state["positive_news"] = pos_news
    st.session_state["negative_news"] = neg_news
    st.session_state["expert_summary"] = expert_summary


# ------------------------------
# Streamlit UI 구성
# ------------------------------
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# Sidebar
st.sidebar.title("🔍 Select Topic")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))

if st.sidebar.button("Run Analysis"):
    analyze_topic(topic_choice)


# Header
st.markdown(
    f"""
# Wiserbond AI Sentiment Summary | {datetime.today().strftime('%B %d, %Y')}
"""
)

# Layout 구성
if "topic" in st.session_state:
    topic = st.session_state["topic"]
    sentiment_counts = st.session_state["sentiment_counts"]
    positive_news = st.session_state["positive_news"]
    negative_news = st.session_state["negative_news"]
    expert_summary = st.session_state["expert_summary"]

    # Executive Summary
    st.markdown("## 🔍 Executive Summary")
    st.markdown(
        "This report provides an AI-powered sentiment analysis of recent news articles related to the selected topic. "
        "Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective."
    )

    # 감정 분석 결과
    st.markdown("## 📈 Sentiment Breakdown")
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'gray', 'red'])
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    st.pyplot(fig)

    # Key News Highlights
    st.markdown("## 📰 Key News Highlights")

    # Positive News
    st.markdown("### ✅ Positive Coverage")
    if positive_news:
        for news in positive_news:
            st.markdown(f"**Source:** {news['source']}")
            st.markdown(f"**Title:** {news['title']}")
            st.markdown(f"**Summary:** {news['summary']}")
            st.write("---")  # 구분선
    else:
        st.markdown("No positive news found.")

    # Negative News
    st.markdown("### ⚠️ Negative Coverage")
    if negative_news:
        for news in negative_news:
            st.markdown(f"**Source:** {news['source']}")
            st.markdown(f"**Title:** {news['title']}")
            st.markdown(f"**Summary:** {news['summary']}")
            st.write("---")  # 구분선
    else:
        st.markdown("No negative news found.")

    # Wiserbond Interpretation
    st.markdown("## 💡 Wiserbond Interpretation")
    st.markdown(expert_summary)
