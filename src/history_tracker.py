
import csv
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "youtube_data.csv"
HISTORY_FILE = BASE_DIR / "data" / "trend_history.csv"


def record_snapshot():
    if not DATA_FILE.exists():
        print("YouTube data not found. Run the collector first.")
        return

    # Aggregate the current collection by topic
    topics = {}

    with DATA_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            topic = row.get("topic", "Unknown")

            try:
                likes = int(row.get("likes") or 0)
                comments = int(row.get("comments") or 0)
                shares = int(row.get("shares") or 0)
                views = int(row.get("views") or 0)
            except ValueError:
                continue

            if topic not in topics:
                topics[topic] = {
                    "video_count": 0,
                    "views": 0,
                    "engagement": 0,
                }

            topics[topic]["video_count"] += 1
            topics[topic]["views"] += views
            topics[topic]["engagement"] += (
                likes + comments + shares
            )

    if not topics:
        print("No usable topic data found.")
        return

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "snapshot_time",
        "topic",
        "video_count",
        "views",
        "engagement",
    ]

    # Prevent accidental duplicate snapshots within 5 minutes
    if HISTORY_FILE.exists():
        try:
            with HISTORY_FILE.open(
                "r", newline="", encoding="utf-8"
            ) as file:
                existing = list(csv.DictReader(file))

            if existing:
                last_time = datetime.fromisoformat(
                    existing[-1]["snapshot_time"]
                )
                elapsed = (
                    datetime.now(timezone.utc)
                    - last_time.astimezone(timezone.utc)
                ).total_seconds()

                if 0 <= elapsed < 300:
                    print(
                        "A snapshot was recorded recently. "
                        "Wait at least 5 minutes before recording again."
                    )
                    return
        except (ValueError, KeyError, OSError):
            pass

    snapshot_time = datetime.now(timezone.utc).isoformat()

    with HISTORY_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        for topic, metrics in topics.items():
            writer.writerow({
                "snapshot_time": snapshot_time,
                "topic": topic,
                "video_count": metrics["video_count"],
                "views": metrics["views"],
                "engagement": metrics["engagement"],
            })

    print("Trend history snapshot saved!")
    print("Topics recorded:", len(topics))
    print("Saved to:", HISTORY_FILE)


if __name__ == "__main__":
    record_snapshot()
