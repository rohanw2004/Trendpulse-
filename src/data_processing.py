import pandas as pd
from pathlib import Path

# Project folder
BASE_DIR = Path.cwd()

# Load sample data
data_file = BASE_DIR / "data" / "sample_data.csv"
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
    .pct_change()
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

engagement_min = topic_engagement.min()
engagement_max = topic_engagement.max()

engagement_normalized = (
    (topic_engagement - engagement_min)
    / (engagement_max - engagement_min)
) * 100

print("\nNormalized Engagement:")
print(engagement_normalized)

# Normalize views to 0-100
topic_views = data.groupby("topic")["views"].sum()

views_min = topic_views.min()
views_max = topic_views.max()

views_normalized = (
    (topic_views - views_min)
    / (views_max - views_min)
) * 100

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
growth_min = topic_growth.min()
growth_max = topic_growth.max()

growth_normalized = (
    (topic_growth - growth_min)
    / (growth_max - growth_min)
) * 100

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