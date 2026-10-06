import streamlit as st
import csv
from pathlib import Path

st.set_page_config(
    page_title="TrendPulse",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path.cwd()
data_file = BASE_DIR / "data" / "sample_data.csv"
trend_file = BASE_DIR / "data" / "trend_scores.csv"

# Load CSV
with open(data_file, newline="", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

# Calculate engagement
for row in data:
    row["likes"] = int(row["likes"])
    row["comments"] = int(row["comments"])
    row["shares"] = int(row["shares"])
    row["views"] = int(row["views"])

    row["engagement"] = (
        row["likes"] +
        row["comments"] +
        row["shares"]
    )

    row["trend_score"] = (
        row["engagement"] +
        row["views"] * 0.1
    )

topic_trends = {}

with open(trend_file, newline="", encoding="utf-8") as file:
    trend_data = list(csv.DictReader(file))

for row in trend_data:
    topic_trends[row["topic"]] = float(row["trend_score"])

# Dashboard
st.title("📈 TrendPulse")
st.subheader("Real-Time Social Media Trend Analyzer")

st.write(
    "Analyze social media data to discover "
    "trending topics and engagement patterns."
)

st.write("### 📊 Dataset Overview")

total_posts = len(data)
total_views = sum(row["views"] for row in data)
total_engagement = sum(row["engagement"] for row in data)

st.write(f"Total Posts: **{total_posts}**")
st.write(f"Total Views: **{total_views:,}**")
st.write(f"Total Engagement: **{total_engagement:,}**")

st.write("### 💬 Topic Engagement")

topic_engagement = {}

for row in data:
    topic = row["topic"]

    if topic not in topic_engagement:
        topic_engagement[topic] = 0

    topic_engagement[topic] += row["engagement"]

topic_engagement = dict(
    sorted(
        topic_engagement.items(),
        key=lambda item: item[1],
        reverse=True
    )
)

for topic, engagement in topic_engagement.items():
    st.write(f"**{topic}** → {engagement:,}")

st.write("### 🔥 Trending Topics")

max_score = max(topic_trends.values())

for rank, (topic, score) in enumerate(topic_trends.items(), start=1):
    percentage = (score / max_score) * 100

    st.write(f"**#{rank} {topic}**")
    st.progress(int(percentage))
    st.write(f"Trend Score: {score:.0f}")


# Sentiment Analysis
sentiment_file = BASE_DIR / "data" / "analyzed_data.csv"

with open(sentiment_file, newline="", encoding="utf-8") as file:
    analyzed_data = list(csv.DictReader(file))

sentiment_counts = {
    "Positive": 0,
    "Neutral": 0,
    "Negative": 0
}

for row in analyzed_data:
    sentiment = row["sentiment"]

    if sentiment in sentiment_counts:
        sentiment_counts[sentiment] += 1

st.write("### 😊 Sentiment Overview")

st.write(f"🟢 Positive: {sentiment_counts['Positive']}")
st.write(f"⚪ Neutral: {sentiment_counts['Neutral']}")
st.write(f"🔴 Negative: {sentiment_counts['Negative']}")

# Top Keywords
keyword_file = BASE_DIR / "data" / "keywords.csv"

with open(keyword_file, newline="", encoding="utf-8") as file:
    keywords = list(csv.DictReader(file))

st.write("### 🔑 Top Keywords")

for row in keywords:
    st.write(f"**{row['keyword']}** → {row['count']} mentions")