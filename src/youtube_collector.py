
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "youtube_data.csv"
BACKUP_FILE = DATA_DIR / "youtube_data_backup.csv"

TOPICS = [
    "Artificial Intelligence",
    "Python Programming",
    "Generative AI",
    "Machine Learning",
    "Data Science",
    "Cloud Computing",
]

VIDEOS_PER_TOPIC = 10


def load_api_key():
    """Read the API key from the local .env file."""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            "Missing .env file in the TrendPulse project folder."
        )

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if line.startswith("YOUTUBE_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")

            if key and key != "paste_your_actual_key_here":
                return key

    raise ValueError(
        "YOUTUBE_API_KEY is missing or still a placeholder in .env."
    )


def youtube_request(endpoint, params, api_key):
    """Send a request to the YouTube Data API."""
    request_params = dict(params)
    request_params["key"] = api_key

    url = (
        "https://www.googleapis.com/youtube/v3/"
        + endpoint
        + "?"
        + urllib.parse.urlencode(request_params)
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "TrendPulse/1.0"}
    )

    try:
        with urllib.request.urlopen(url=request, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))

    except Exception as exc:
        raise RuntimeError(
            f"YouTube API request failed for {endpoint}. "
            "Check internet, API key, API enablement and quota."
        ) from exc


def collect_topic(query, api_key, max_results=10):
    """Collect recent public videos for one topic."""
    search_data = youtube_request(
        "search",
        {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max(1, min(int(max_results), 50)),
            "order": "date",
        },
        api_key,
    )

    video_ids = [
        item.get("id", {}).get("videoId")
        for item in search_data.get("items", [])
        if item.get("id", {}).get("videoId")
    ]

    if not video_ids:
        print("No videos found for:", query)
        return []

    details = youtube_request(
        "videos",
        {
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
        },
        api_key,
    )

    rows = []

    for item in details.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})

        rows.append({
            "timestamp": snippet.get("publishedAt", ""),
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "platform": "YouTube",
            "topic": query,
            "text": snippet.get("title", ""),
            "video_id": item.get("id", ""),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "shares": 0,
            "views": int(stats.get("viewCount", 0)),
        })

    return rows


def save_data(rows):
    """Save the combined dataset without losing the previous CSV."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Keep the first backup of the existing dataset.
    if OUTPUT_FILE.exists() and not BACKUP_FILE.exists():
        BACKUP_FILE.write_bytes(OUTPUT_FILE.read_bytes())
        print("Previous dataset backed up to:", BACKUP_FILE)

    fieldnames = [
        "timestamp",
        "collected_at",
        "platform",
        "topic",
        "text",
        "video_id",
        "likes",
        "comments",
        "shares",
        "views",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Total videos saved:", len(rows))
    print("Dataset saved to:", OUTPUT_FILE)


def collect_all_topics():
    """Collect videos across all configured topics."""
    api_key = load_api_key()
    all_rows = []
    failed_topics = []

    for index, topic in enumerate(TOPICS, start=1):
        print(f"\n[{index}/{len(TOPICS)}] Collecting: {topic}")

        try:
            rows = collect_topic(
                topic,
                api_key,
                VIDEOS_PER_TOPIC
            )
            all_rows.extend(rows)
            print("Videos collected for this topic:", len(rows))

        except Exception as error:
            failed_topics.append(topic)
            print("Topic collection failed:", topic)
            print("Reason:", error)

    if all_rows:
        save_data(all_rows)
    else:
        print("\nNo videos were collected. Existing dataset was not changed.")
        return

    print("\nCollection summary")
    print("Topics requested:", len(TOPICS))
    print("Topics failed:", len(failed_topics))
    print("Total videos:", len(all_rows))
    print("Note: shares are 0 because the API does not expose share counts.")

    if failed_topics:
        print("Failed topics:", ", ".join(failed_topics))


if __name__ == "__main__":
    try:
        collect_all_topics()
    except Exception as error:
        print("Collector error:", error)
