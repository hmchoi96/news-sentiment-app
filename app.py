import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# ------------------------------
# App Config
# ------------------------------
st.set_page_config(
    page_title="Wiserbond News Sentiment Report",
    layout="centered"
)

# ------------------------------
# Header
# ------------------------------
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

# ------------------------------
# Executive Summary
# ------------------------------
st.markdown("### 🔍 Executive Summary")
st.markdown("""
This report provides an AI-powered sentiment analysis of recent news articles related to the selected topic.
Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective.
""")

# ------------------------------
# Sentiment Chart
# ------------------------------
st.markdown("### 📈 Sentiment Breakdown")
sentiment_counts = st.session_state.get("sentiment_counts", {"Positive": 10, "Neutral": 5, "Negative": 12})

fig, ax = plt.subplots()
ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=["#2ca02c", "#1f77b4", "#d62728"])
ax.set_title("Sentiment Distribution")
ax.set_ylabel("Number of Articles")
st.pyplot(fig)

# ------------------------------
# News Highlights Section
# ------------------------------
st.markdown("### 📰 Key News Highlights")

positive_news = st.session_state.get("positive_news", [])
negative_news = st.session_state.get("negative_news", [])

with st.expander("✅ Positive Coverage"):
    if positive_news:
        for item in positive_news:
            st.markdown(f"- **[{item['source']}]** {item['title']} _“{item['summary']}”_")
    else:
        st.markdown("_No positive news items found._")

with st.expander("⚠️ Negative Coverage"):
    if negative_news:
        for item in negative_news:
            st.markdown(f"- **[{item['source']}]** {item['title']} _“{item['summary']}”_")
    else:
        st.markdown("_No negative news items found._")

# ------------------------------
# Expert Interpretation
# ------------------------------
st.markdown("### 💡 Wiserbond Interpretation")

expert_summary = st.session_state.get("expert_summary", "")

if expert_summary:
    st.info(expert_summary)
else:
    st.info("_No expert interpretation generated yet._")

# ------------------------------
# Footer
# ------------------------------
st.markdown("""---""")
st.markdown("""
<small>Wiserbond Research · wiserbond.ca · info@wiserbond.ca  
This report was generated using the Wiserbond AI Sentiment Engine v1.0</small>
""", unsafe_allow_html=True)
