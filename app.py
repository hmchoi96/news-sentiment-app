import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from news_sentiment_tool_demo import (
    get_news, filter_articles, run_sentiment_analysis,
    summarize_by_sentiment, TOPIC_SETTINGS
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
        for a in analyzed if a["sentiment"] == "POSITIVE"
    ]
    neg_news = [
        {"source": a["source"], "title": a["title"], "summary": a["description"]}
        for a in analyzed if a["sentiment"] == "NEGATIVE"
    ]

    # 전문가 요약 포맷 개선 (줄바꿈 포함)
    expert_summary = (
        "✅ **Positive Insight**\n\n" + summarize_by_sentiment(analyzed, "POSITIVE", keywords) +
        "\n\n❗ **Negative Insight**\n\n" + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    st.session_state["topic"] = topic
    st.session_state["sentiment_counts"] = sentiment_counts
    st.session_state["positive_news"] = pos_news
    st.session_state["negative_news"] = neg_news
    st.session_state["expert_summary"] = expert_summary

# ------------------------------
# Streamlit UI 구성
# ------------------------------
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="centered")

# Sidebar
st.sidebar.title("🔍 Select Topic")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
if st.sidebar.button("Run Analysis"):
    analyze_topic(topic_choice)

# Header
st.markdown(
    f"""
    <div style="text-align: left; padding-top: 30px;">
        <h1 style="font-size: 36px; color: #051F5B; margin-bottom: 5px;">📊 {st.session_state.get("topic", "Tariff")} – News Sentiment Report</h1>
        <p style="font-size: 18px; color: #444;">Wiserbond AI Sentiment Summary | {datetime.today().strftime('%B %d, %Y')}</p>
        <hr style="margin-top: 10px; border: none; border-top: 1px solid #051F5B;">
    </div>
    """,
    unsafe_allow_html=True
)

# Executive Summary
st.markdown("### 🔍 Executive Summary")
st.markdown("""
            This report provides an AI-powered sentiment analysis of recent news articles related to the selected topic.
            Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective.
        """)

# Sentiment Chart
st.markdown("### 📈 Sentiment Breakdown")
sentiment_counts = st.session_state.get("sentiment_counts", {"Positive": 0, "Neutral": 0, "Negative": 0})
fig, ax = plt.subplots()
ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=["#2ca02c", "#1f77b4", "#d62728"])
ax.set_title("Sentiment Distribution")
ax.set_ylabel("Number of Articles")
st.pyplot(fig)

# News Highlights
st.markdown("### 📰 Key News Highlights")
positive_news = st.session_state.get("positive_news", [])
negative_news = st.session_state.get("negative_news", [])

with st.expander("✅ Positive Coverage"):
    if positive_news:
        for item in positive_news:
            st.markdown(f"- **[{item['source']}]** {item['title']}  \n_“{item['summary']}”_")
    else:
        st.markdown("_No positive news items found._")

with st.expander("⚠️ Negative Coverage"):
    if negative_news:
        for item in negative_news:
            st.markdown(f"- **[{item['source']}]** {item['title']}  \n_“{item['summary']}”_")
    else:
        st.markdown("_No negative news items found._")

# Expert Summary
st.markdown("### 💡 Wiserbond Interpretation")
expert_summary = st.session_state.get("expert_summary", "")
if expert_summary:
    st.markdown(f"<div style='white-space: pre-wrap'>{expert_summary}</div>", unsafe_allow_html=True)
else:
    st.info("_No expert interpretation generated yet._")

# Footer
st.markdown("""---""")
st.markdown("""
            <small>Wiserbond Research · wiserbond.ca · info@wiserbond.ca  
            This report was generated using the Wiserbond AI Sentiment Engine v1.0</small>
            """, unsafe_allow_html=True
            )
