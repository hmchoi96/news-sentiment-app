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
        {
            "source": a["source"],
            "title": a["title"],
            "summary": a["description"],
            "score": a.get("score", 0),
        }
        for a in analyzed
        if a["sentiment"] == "POSITIVE"
    ]
    neg_news = [
        {
            "source": a["source"],
            "title": a["title"],
            "summary": a["description"],
            "score": a.get("score", 0),
        }
        for a in analyzed
        if a["sentiment"] == "NEGATIVE"
    ]

    # 전문가 요약 줄바꿈 포함
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
# 뉴스 요약 표시 함수 (Top 3 + 확장)
# ------------------------------
def display_news_section(label, news_list, max_visible=3):
    if not news_list:
        st.markdown(f"_No {label.lower()} news found._")
        return

    sorted_news = sorted(news_list, key=lambda x: x.get("score", 0), reverse=True)
    visible = sorted_news[:max_visible]
    hidden = sorted_news[max_visible:]

    for news in visible:
        st.markdown(f"**Source:** {news['source']}")
        st.markdown(f"**Title:** {news['title']}")
        st.markdown(f"**Summary:** {news['summary']}")
        st.write("---")

    if hidden:
        with st.expander(f"View more {label.lower()} news"):
            for news in hidden:
                st.markdown(f"**Source:** {news['source']}")
                st.markdown(f"**Title:** {news['title']}")
                st.markdown(f"**Summary:** {news['summary']}")
                st.write("---")

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
st.markdown(f"# 📊 Wiserbond News Sentiment Report")
st.markdown(
    f"**Date:** {datetime.today().strftime('%B %d, %Y')} | **Topic:** {st.session_state.get('topic', 'Not selected')}"
)

# 본문
if "topic" in st.session_state:
    topic = st.session_state["topic"]
    sentiment_counts = st.session_state["sentiment_counts"]
    positive_news = st.session_state["positive_news"]
    negative_news = st.session_state["negative_news"]
    expert_summary = st.session_state["expert_summary"]

    st.markdown("## 🔍 Executive Summary")
    st.markdown(
        "This report provides an AI-powered sentiment analysis of recent news articles related to the selected topic. "
        "Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective."
    )

    # 감성 분석 차트
    st.markdown("## 📈 Sentiment Breakdown")
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#2ca02c", "#7f7f7f", "#d62728"])
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Articles")
    st.pyplot(fig)

    # 뉴스 요약
    st.markdown("## 📰 Key News Highlights")

    st.markdown("### ✅ Positive Coverage")
    display_news_section("Positive", positive_news)

    st.markdown("### ⚠️ Negative Coverage")
    display_news_section("Negative", negative_news)

    # 전문가 해석
    st.markdown("## 💡 Wiserbond Interpretation")
    st.markdown(f"<div style='white-space: pre-wrap'>{expert_summary}</div>", unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown(
    """
<small>Wiserbond Research · wiserbond.ca · info@wiserbond.ca  
This report was generated using the Wiserbond AI Sentiment Engine v1.0</small>
""",
    unsafe_allow_html=True,
)
