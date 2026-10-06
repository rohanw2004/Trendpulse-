import pandas as pd
from pathlib import Path


def calculate_trend_score(data):
    # Total engagement for each topic
    topic_engagement = data.groupby("topic")["engagement"].sum()

    # Total views for each topic
    topic_views = data.groupby("topic")["views"].sum()

    # Normalize engagement
    engagement_min = topic_engagement.min()
    engagement_max = topic_engagement.max()

    engagement_normalized = (
        (topic_engagement - engagement_min)
        / (engagement_max - engagement_min)
    ) * 100

    # Normalize views
    views_min = topic_views.min()
    views_max = topic_views.max()

    views_normalized = (
        (topic_views - views_min)
        / (views_max - views_min)
    ) * 100

    # Calculate growth percentage
    growth_percent = (
        data.groupby("topic")["engagement"]
        .pct_change()
        .groupby(data["topic"])
        .mean()
        .fillna(0) * 100
    )

    # Normalize growth
    growth_min = growth_percent.min()
    growth_max = growth_percent.max()

    growth_normalized = (
        (growth_percent - growth_min)
        / (growth_max - growth_min)
    ) * 100

    # Final weighted trend score
    final_trend_score = (
        engagement_normalized * 0.40
        + views_normalized * 0.30
        + growth_normalized * 0.30
    )

    return final_trend_score.sort_values(ascending=False)

  # Save trend scores
trend_scores = final_trend_score.reset_index()
trend_scores.columns = ["topic", "trend_score"]

output_file = Path("data/trend_scores.csv")
trend_scores.to_csv(output_file, index=False)
