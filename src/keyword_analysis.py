
import pandas as pd
import re
from collections import Counter
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "youtube_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "youtube_keywords.csv"

# Load real YouTube data
data = pd.read_csv(INPUT_FILE)

# Words we don't want to count
stop_words = {
    "the", "is", "a", "an", "and", "are", "to", "of",
    "for", "in", "on", "one", "with", "this", "that",
    "it", "as", "be", "by", "from", "you", "your",
    "we", "our", "how", "what", "why", "when", "who",
    "video", "videos", "official", "new", "2026"
}

# Combine YouTube video titles
all_text = " ".join(data["text"].fillna("").astype(str))
all_text = all_text.lower()

# Extract words
words = re.findall(r"\b[a-zA-Z]+\b", all_text)

# Remove common words
filtered_words = [
    word for word in words
    if word not in stop_words and len(word) > 1
]

# Count keywords
word_counts = Counter(filtered_words)
top_keywords = word_counts.most_common(10)

# Display results
print("\nYouTube Top Keywords:")

for word, count in top_keywords:
    print(word, "->", count)

# Save separately from sample-data keywords
keyword_data = pd.DataFrame(
    top_keywords,
    columns=["keyword", "count"]
)

keyword_data.to_csv(OUTPUT_FILE, index=False)

print("\nKeywords saved to:", OUTPUT_FILE)
