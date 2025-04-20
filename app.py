
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
# 다국어 텍스트 설정
# ------------------------------
LANG_TEXT = {
    "English": {
        "header": "📊 Wiserbond News Sentiment Report",
        "executive_summary": "## 🔍 Executive Summary\n\nThis report provides an AI-powered sentiment analysis of recent news articles related to the selected topic. Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective.",
        "sentiment_chart": "## 📈 Sentiment Breakdown",
        "positive_title": "### ✅ Positive Coverage",
        "negative_title": "### ⚠️ Negative Coverage",
        "expert_insight": "## 💡 Wiserbond Interpretation",
        "footer": "<small>Wiserbond Research · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    },
    "한국어": {
        "header": "📊 와이저본드 뉴스 감정 분석 리포트",
        "executive_summary": "## 🔍 핵심 요약\n\n이 보고서는 AI 기반의 감정 분석을 통해 최근 뉴스의 흐름과 내러티브를 정리했습니다.",
        "sentiment_chart": "## 📈 감정 분포 차트",
        "positive_title": "### ✅ 긍정 뉴스 요약",
        "negative_title": "### ⚠️ 부정 뉴스 요약",
        "expert_insight": "## 💡 Wiserbond 해석",
        "footer": "<small>Wiserbond 리서치 · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    },
    "Español": {
        "header": "📊 Informe de Sentimiento de Noticias de Wiserbond",
        "executive_summary": "## 🔍 Resumen Ejecutivo\n\nEste informe proporciona un análisis de sentimiento impulsado por IA sobre las noticias recientes relacionadas con el tema seleccionado.",
        "sentiment_chart": "## 📈 Distribución de Sentimiento",
        "positive_title": "### ✅ Cobertura Positiva",
        "negative_title": "### ⚠️ Cobertura Negativa",
        "expert_insight": "## 💡 Interpretación de Wiserbond",
        "footer": "<small>Investigación Wiserbond · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    }
}

# ------------------------------
# 산업별 키워드
# ------------------------------
INDUSTRY_KEYWORDS = {
    "Supply Chain": ["logistics", "freight", "shipping", "port", "customs", "supply chain", "export", "import"],
    "Consulting": ["client", "recommendation", "strategy", "project", "transformation", "management"],
    "Retail": ["sales", "store", "consumer", "pricing", "discount", "e-commerce"],
    "Finance": ["bank", "interest rate", "investment", "credit", "bond", "liquidity"],
    "Manufacturing": ["factory", "production", "plant", "assembly", "automation", "capacity"]
}

# ------------------------------
# 분석 실행 함수
# ------------------------------
def analyze_topic(topic, industry):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    keywords = setting["keywords"]

    if industry != "All":
        keywords += INDUSTRY_KEYWORDS.get(industry, [])

    raw = get_news(search_term)
    filtered = filter_articles(raw, keywords)
    analyzed = run_sentiment_analysis(filtered)

    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    pos_news = [a for a in analyzed if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed if a["sentiment"] == "NEGATIVE"]

    expert_summary = (
        "✅ **Positive Insight**\n\n"
        + summarize_by_sentiment(analyzed, "POSITIVE", keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    st.session_state["topic"] = topic
    st.session_state["industry"] = industry
    st.session_state["sentiment_counts"] = sentiment_counts
    st.session_state["positive_news"] = pos_news
    st.session_state["negative_news"] = neg_news
    st.session_state["expert_summary"] = expert_summary

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
        st.markdown(f"**Summary:** {news['description']}")
        st.write("---")

    if hidden:
        with st.expander(f"View more {label.lower()} news"):
            for news in hidden:
                st.markdown(f"**Source:** {news['source']}")
                st.markdown(f"**Title:** {news['title']}")
                st.markdown(f"**Summary:** {news['description']}")
                st.write("---")

# ------------------------------
# UI 구성
# ------------------------------
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# Sidebar
st.sidebar.title("🔍 Select Topic")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
industry_choice = st.sidebar.selectbox("🏭 Select Industry (Optional)", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("🌐 Language / 언어 선택", ["English", "한국어", "Español"])

st.session_state["language"] = language_choice
texts = LANG_TEXT[language_choice]

if st.sidebar.button("Run Analysis"):
    analyze_topic(topic_choice, industry_choice)

# Header
st.markdown(f"# {texts['header']}")
st.markdown(
    f"**Date:** {datetime.today().strftime('%B %d, %Y')} | **Topic:** {st.session_state.get('topic', 'Not selected')} | **Industry:** {st.session_state.get('industry', 'All')}"
)

if "topic" in st.session_state:
    sentiment_counts = st.session_state["sentiment_counts"]
    positive_news = st.session_state["positive_news"]
    negative_news = st.session_state["negative_news"]
    expert_summary = st.session_state["expert_summary"]

    st.markdown(texts["executive_summary"])
    st.markdown(texts["sentiment_chart"])

    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#2ca02c", "#7f7f7f", "#d62728"])
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Articles")
    st.pyplot(fig)

    st.markdown("## 📰 Key News Highlights")
    st.markdown(texts["positive_title"])
    display_news_section("Positive", positive_news)

    st.markdown(texts["negative_title"])
    display_news_section("Negative", negative_news)

    st.markdown(texts["expert_insight"])
    st.markdown(f"<div style='white-space: pre-wrap'>{expert_summary}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(texts["footer"], unsafe_allow_html=True)
