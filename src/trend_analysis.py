import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "youtube_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "trend_scores.csv"


def normalize_series(series):
    series = series.replace(
        [float("inf"), -float("inf")], 0
    ).fillna(0)

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return series * 0 + 50

    return (series - minimum) / (maximum - minimum) * 100


def calculate_trend_score(data):
    data = data.copy()

    data["engagement"] = (
        data["likes"] + data["comments"] + data["shares"]
    )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"], utc=True
    )

    data = data.sort_values("timestamp")

    topic_engagement = data.groupby("topic")["engagement"].sum()
    topic_views = data.groupby("topic")["views"].sum()

    data["growth_percent"] = (
        data.groupby("topic")["engagement"]
        .pct_change(fill_method=None)
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0) * 100
    )

    topic_growth = data.groupby("topic")["growth_percent"].mean()

    engagement_normalized = normalize_series(topic_engagement)
    views_normalized = normalize_series(topic_views)
    growth_normalized = normalize_series(topic_growth)

    final_trend_score = (
        engagement_normalized * 0.40
        + views_normalized * 0.30
        + growth_normalized * 0.30
    )

    return final_trend_score.sort_values(ascending=False)


if __name__ == "__main__":
    data = pd.read_csv(INPUT_FILE)
    scores = calculate_trend_score(data)

    trend_scores = scores.rename("trend_score").reset_index()
    trend_scores.to_csv(OUTPUT_FILE, index=False)

    print("\nFinal Trend Scores:")
    print(trend_scores)
    print("\nSaved to:", OUTPUT_FILE)