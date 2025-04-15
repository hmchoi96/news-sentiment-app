***
📊 Wiserbond News Sentiment Analyzer

WHY – Why was this built?
Economic news is everywhere—but understanding what truly matters and how it's being perceived can be hard,
especially for people without a background in finance. Instead of reading through dozens of articles,
this tool helps users quickly grasp the emotional tone and key narratives surrounding major economic topics.

HOW – How does it work?
The tool collects recent news articles on selected economic topics, filters them using targeted keywords,
classifies them by sentiment (positive/negative/neutral) using NLP, and generates concise summaries for both sides.
It also visualizes the sentiment distribution to make interpretation easier.

WHAT – What does it do?
- Gathers news on selected topics: `tariff`, `trump`, `inflation`, `fed`, `unemployment`
- Filters out unrelated content using topic-specific keyword lists
- Performs AI-based sentiment analysis and summarization
- Separates and summarizes positive and negative coverage
- Visualizes the emotional tone with a simple bar chart

This tool is especially helpful for non-finance professionals, strategy teams, and policymakers
who need clear, unbiased insights on complex economic signals—without reading everything.



***
▶️ To run the file:

In your **Mac Terminal** or **Windows Command Prompt**, type:

    python news_sentiment_tool_final.py

(Ensure your environment has Python installed and necessary packages like `transformers`, `requests`, `matplotlib`.)

---

🔑 To quickly test the tool:

You can use this API key (personal):

    NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'

Paste it in the script where the `NEWS_API_KEY` variable is defined.

---

🌐 Topics currently available:

- tariff  
- trump  
- inflation  
- fed  
- unemployment

This keyword list is fixed to ensure filtering quality and relevance.
