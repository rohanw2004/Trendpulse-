import pandas as pd
import re
from collections import Counter

# Load our dataset
data = pd.read_csv("data/sample_data.csv")

# Words we don't want to count
stop_words = {
    "the", "is", "a", "an", "and", "are", "to", "of",
    "for", "in", "on", "one", "with", "this", "that",
    "it", "as", "be", "by", "from"
}

# Combine all post text
all_text = " ".join(data["text"].astype(str))

# Convert to lowercase
all_text = all_text.lower()

# Keep only words
words = re.findall(r"\b[a-zA-Z]+\b", all_text)

# Remove common words
filtered_words = [
    word for word in words
    if word not in stop_words
]

# Count words
word_counts = Counter(filtered_words)

# Get top 10 keywords
top_keywords = word_counts.most_common(10)

print("\n🔑 Top Keywords:")

for word, count in top_keywords:
    print(word, "→", count)

  # Save keywords for the dashboard
keyword_data = pd.DataFrame(
    top_keywords,
    columns=["keyword", "count"]
)

keyword_data.to_csv(
    "data/keywords.csv",
    index=False
)

print("\nKeywords saved successfully!") 