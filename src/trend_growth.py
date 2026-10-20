
import csv
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE_DIR / "data" / "trend_history.csv"
OUTPUT_FILE = BASE_DIR / "data" / "trend_growth.csv"


def read_history():
    history = defaultdict(list)

    if not HISTORY_FILE.exists():
        print("Trend history not found. Record snapshots first.")
        return history

    with HISTORY_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                history[row["topic"]].append({
                    "snapshot_time": row["snapshot_time"],
                    "views": int(row["views"]),
                    "engagement": int(row["engagement"]),
                    "video_count": int(row["video_count"]),
                })
            except (ValueError, KeyError):
                continue

    for topic in history:
        history[topic].sort(
            key=lambda item: item["snapshot_time"]
        )

    return history


def percentage_change(old, new):
    if old == 0:
        return 0.0 if new == 0 else None

    return round(((new - old) / old) * 100, 2)


def calculate_growth():
    history = read_history()

    if not history:
        return

    fields = [
        "topic",
        "previous_snapshot",
        "latest_snapshot",
        "previous_views",
        "latest_views",
        "views_change_percent",
        "previous_engagement",
        "latest_engagement",
        "engagement_change_percent",
        "previous_video_count",
        "latest_video_count",
    ]

    results = []

    for topic, snapshots in history.items():
        if len(snapshots) < 2:
            print(f"Skipping {topic}: need two snapshots.")
            continue

        previous = snapshots[-2]
        latest = snapshots[-1]

        results.append({
            "topic": topic,
            "previous_snapshot": previous["snapshot_time"],
            "latest_snapshot": latest["snapshot_time"],
            "previous_views": previous["views"],
            "latest_views": latest["views"],
            "views_change_percent": percentage_change(
                previous["views"], latest["views"]
            ),
            "previous_engagement": previous["engagement"],
            "latest_engagement": latest["engagement"],
            "engagement_change_percent": percentage_change(
                previous["engagement"], latest["engagement"]
            ),
            "previous_video_count": previous["video_count"],
            "latest_video_count": latest["video_count"],
        })

    if not results:
        print("No topics have two snapshots yet.")
        return

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("Trend growth analysis saved!")
    print("Topics compared:", len(results))
    print("Saved to:", OUTPUT_FILE)

    print("\nTopic growth summary:")
    for row in sorted(
        results,
        key=lambda item: (
            item["engagement_change_percent"]
            if item["engagement_change_percent"] is not None
            else float("-inf")
        ),
        reverse=True,
    ):
        print(
            f'{row["topic"]}: '
            f'Views change = {row["views_change_percent"]}%, '
            f'Engagement change = {row["engagement_change_percent"]}%'
        )


if __name__ == "__main__":
    calculate_growth()
