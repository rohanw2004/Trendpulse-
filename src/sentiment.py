import pandas as pd
from pathlib import Path
from nltk.sentiment import SentimentIntensityAnalyzer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "youtube_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "youtube_analyzed_data.csv"

# Load real YouTube data
data = pd.read_csv(INPUT_FILE)

# Create VADER analyzer
sia = SentimentIntensityAnalyzer()


def get_sentiment(text):
    score = sia.polarity_scores(str(text))

    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    return "Neutral"


# Analyze YouTube video titles
data["sentiment"] = data["text"].apply(get_sentiment)

# Save results separately
data.to_csv(OUTPUT_FILE, index=False)

print("\nYouTube Sentiment Analysis:")
print(data[["topic", "text", "sentiment"]])

print("\nSentiment Counts:")
print(data["sentiment"].value_counts())

print("\nSaved to:", OUTPUT_FILE)