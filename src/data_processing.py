import pandas as pd
from pathlib import Path

def normalize_series(series):
    series = series.replace(
        [float("inf"), -float("inf")], 0
    ).fillna(0)

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return series * 0 + 50

    return (series - minimum) / (maximum - minimum) * 100

# Project folder
BASE_DIR = Path.cwd()

# Load real YouTube data
data_file = BASE_DIR / "data" / "youtube_data.csv"
data = pd.read_csv(data_file)

data["timestamp"] = pd.to_datetime(data["timestamp"])

print(data)

print("\nTotal posts:", len(data))
print("Columns:", list(data.columns))

data["engagement"] = data["likes"] + data["comments"] + data["shares"]

# Sort posts by topic and timestamp
data = data.sort_values(["topic", "timestamp"])

# Calculate engagement growth for each topic
data["engagement_growth"] = (
    data.groupby("topic")["engagement"]
    .diff()
    .fillna(0)
)

data["growth_percent"] = (
    data.groupby("topic")["engagement"]
    .pct_change(fill_method=None)
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0) * 100
)

print("\nEngagement:")
print(data[["topic", "engagement"]])

topic_engagement = data.groupby("topic")["engagement"].sum()

print("\nTopic Engagement:")
print(topic_engagement)

# Calculate trend score
data["trend_score"] = (
    data["engagement"]
    + (data["views"] * 0.1)
)

# Calculate total trend score for each topic
topic_trends = (
    data.groupby("topic")["trend_score"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTrending Topics:")
print(topic_trends)

# Normalize engagement to 0-100
topic_engagement = data.groupby("topic")["engagement"].sum()
engagement_normalized = normalize_series(topic_engagement)

print("\nNormalized Engagement:")
print(engagement_normalized)

# Normalize views to 0-100
topic_views = data.groupby("topic")["views"].sum()
views_normalized = normalize_series(topic_views)

print("\nNormalized Views:")
print(views_normalized)

# Calculate average growth for each topic
topic_growth = (
    data.groupby("topic")["growth_percent"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTopic Growth Percentage:")
print(topic_growth)

# Normalize growth percentage to 0-100
growth_normalized = normalize_series(topic_growth)

print("\nNormalized Growth:")
print(growth_normalized)

# Calculate final trend score
final_trend_score = (
    engagement_normalized * 0.40
    + views_normalized * 0.30
    + growth_normalized * 0.30
)

final_trend_score = final_trend_score.sort_values(
    ascending=False
)

print("\nFinal Trend Score:")
print(final_trend_score)