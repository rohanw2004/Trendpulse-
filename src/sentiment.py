import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Load our dataset
data = pd.read_csv("data/sample_data.csv")

# Create VADER analyzer
sia = SentimentIntensityAnalyzer()

# Function to classify sentiment
def get_sentiment(text):
    score = sia.polarity_scores(text)

    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Analyze every post
data["sentiment"] = data["text"].apply(get_sentiment)

# Save analyzed data
data.to_csv("data/analyzed_data.csv", index=False)

# Show results
print("\nSentiment Analysis:")
print(data[["topic", "text", "sentiment"]])

print("\nSentiment Counts:")
print(data["sentiment"].value_counts())

print("\nAnalyzed data saved successfully!")