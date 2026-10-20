
import csv
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import base64
from pathlib import Path
import mimetypes

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="TrendPulse | Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

theme_mode = st.sidebar.radio(
    "🎨 Appearance",
    ["Dark Mode", "Light Mode"],
    key="theme_mode",
)

st.sidebar.caption("SOCIAL MEDIA INTELLIGENCE")
st.sidebar.divider()

source = st.sidebar.radio(
    "Choose data source",
    ["Real YouTube Data", "Sample Data"],
)

if theme_mode == "Light Mode":
    page_bg = "#f3f6fc"
    text_color = "#172033"
    muted_color = "#53627a"
    sidebar_bg = "#e7edf7"
    card_bg = "#ffffff"
    border_color = "#d5deed"
else:
    page_bg = "#0b1020"
    text_color = "#edf2ff"
    muted_color = "#b6c2df"
    sidebar_bg = "#0c1222"
    card_bg = "#151f35"
    border_color = "#2a3856"


# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: transparent;
    color: #edf2ff;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
[data-testid="stSidebar"] {
    background: #0c1222;
    color: #edf2ff;
    border-right: 1px solid #26314b;
}
h1, h2, h3 {
    color: #f3f6ff !important;
}
p, label, [data-testid="stCaptionContainer"] {
    color: #b6c2df;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #192440, #151d33);
    border: 1px solid #2a3858;
    padding: 18px;
    border-radius: 15px;
}
div[data-testid="stMetricLabel"] {
    color: #a9b8d8;
}
div[data-testid="stMetricValue"] {
    color: #e9efff;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6366f1, #22d3ee);
}
div[data-testid="stTabs"] button {
    color: #cbd5e1;
}
hr {
    border-color: #293550;
}
.tp-hero {
    padding: 26px;
    border-radius: 20px;
    border: 1px solid #34466c;
    background: linear-gradient(115deg, #1c2b50, #24204b 65%, #142d42);
    margin-bottom: 22px;
}
.tp-label {
    color: #8ea5ff;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
}
.tp-subtitle {
    color: #bdc9e5;
    font-size: 1rem;
}
.tp-card {
    padding: 16px;
    background: #151f35;
    border: 1px solid #2a3856;
    border-radius: 13px;
    margin-bottom: 12px;
}

.tp-muted {
    color: #9caed0;
    font-size: 0.85rem;
}

/* Wider chart area */

div[data-testid="stPlotlyChart"] {
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    border: 1px solid #2a3856;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.45);
    padding: 4px;
    box-sizing: border-box;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: #53658b #151f35;
}

div[data-testid="stPlotlyChart"] .js-plotly-plot {
    min-width: 850px;
    max-width: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- THEME OVERRIDE ----------------
if theme_mode == "Light Mode":
    st.markdown("""
    <style>
    /* Main page */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        color: #172033 !important;
    }

    /* Main text */
    .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp p, .stApp label,
    .stApp li, .stApp strong,
    [data-testid="stCaptionContainer"] {
        color: #24324a !important;
    }


/* Sidebar background — Light Mode */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarHeader"],
[data-testid="stSidebarNav"],
[data-testid="stSidebar"] section {
    background: #e7edf7 !important;
    background-color: #e7edf7 !important;
    color: #172033 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #24324a !important;
}

    /* Metric cards and their values */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        background-image: none !important;
        border: 1px solid #d5deed !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #24324a !important;
    }

    /* Hero and content cards */
    .tp-hero {
        background: linear-gradient(
            115deg, #dce8ff, #e9e3ff, #dff5fa
        ) !important;
        border-color: #cbd5e1 !important;
    }

    .tp-hero .tp-label {
        color: #4f46e5 !important;
    }

    .tp-hero h1 {
        color: #172033 !important;
    }

    .tp-hero .tp-subtitle {
        color: #53627a !important;
    }

    .tp-card {
        background: rgba(255,255,255,0.92) !important;
        border-color: #d5deed !important;
    }

    .tp-card .tp-muted {
        color: #53627a !important;
    }

    /* Progress bars */
    [data-testid="stProgress"] > div {
        background: #dce4f2 !important;
    }

    [data-testid="stProgress"] [role="progressbar"] {
        background: #6366f1 !important;
    }

    /* Tabs and buttons */
    .stTabs button,
    .stButton button {
        color: #24324a !important;
    }

    /* Chart outer containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.85) !important;
        border-color: #d5deed !important;
        scrollbar-color: #a8b5ca #edf2f9 !important;
    }

    hr {
        border-color: #d5deed !important;
    }


/* Sidebar navigation: Light Mode */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarHeader"],
[data-testid="stSidebarNav"] {
    background: #e7edf7 !important;
    background-color: #e7edf7 !important;
}

/* All sidebar text and labels */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] small {
    color: #24324a !important;
}

/* Sidebar radio buttons and their labels */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #24324a !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] button {
    color: #24324a !important;
    border-color: #cbd5e1 !important;
}

/* Sidebar input controls */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    color: #24324a !important;
    background-color: #ffffff !important;
}

/* Light Mode: inner navigation area */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] > div,
[data-testid="stSidebarNav"] ul,
[data-testid="stSidebarNav"] li,
[data-testid="stSidebarNavLink"],
[data-testid="stSidebarNavLink"] > div {
    background: #e7edf7 !important;
    background-color: #e7edf7 !important;
}

/* Navigation link text */
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span {
    color: #24324a !important;
}


    /* Top Streamlit toolbar — Light Mode */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        background: #e7edf7 !important;
        background-color: #e7edf7 !important;
    }


/* Keep toolbar controls dark and visible */
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] button svg,
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] button svg {
    color: #24324a !important;
    fill: #24324a !important;
}

/* Sidebar collapse / expand button */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebar"] button[kind="header"] svg {
    color: #24324a !important;
    fill: #24324a !important;
    opacity: 1 !important;
}


    /* Refresh dashboard button */
    [data-testid="stSidebar"] .stButton button {
        background-color: #ffffff !important;
        color: #24324a !important;
        border: 1px solid #cbd5e1 !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        return []

    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def fmt(value):
    return f"{value:,.0f}"

@st.dialog("Expanded chart", width="large")
def show_expanded_chart(chart_type):
    if chart_type == "engagement":
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )
    elif chart_type == "sentiment":
        st.plotly_chart(
            donut_fig,
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )
    elif chart_type == "keywords":
        st.plotly_chart(
            keyword_fig,
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )


# ---------------- BACKGROUND IMAGE ----------------
import base64
import mimetypes

BASE_DIR = Path(__file__).resolve().parent

if theme_mode == "Light Mode":
    bg_path = BASE_DIR / "background_light.jpg"
    overlay = "rgba(243, 246, 252, 0.48)"
    overlay_end = "rgba(243, 246, 252, 0.62)"
else:
    bg_path = BASE_DIR / "background.jpg"
    overlay = "rgba(10, 18, 38, 0.55)"
    overlay_end = "rgba(10, 18, 38, 0.72)"

if bg_path.is_file():
    mime_type = mimetypes.guess_type(str(bg_path))[0] or "image/jpeg"
    image_data = base64.b64encode(
        bg_path.read_bytes()
    ).decode("utf-8")

    background_css = f"""
    <style>
    .stApp {{
        background: transparent !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(
            {overlay}, {overlay_end}
        ), url("data:{mime_type};base64,{image_data}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stMain"] {{
        background: transparent !important;
    }}
    </style>
    """

    st.markdown(background_css, unsafe_allow_html=True)
else:
    st.error(f"Background image not found: {bg_path}")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 📈 TrendPulse")

if source == "Real YouTube Data":
    data_file = "youtube_data.csv"
    sentiment_file = "youtube_analyzed_data.csv"
    keyword_file = "youtube_keywords.csv"
else:
    data_file = "sample_data.csv"
    sentiment_file = "analyzed_data.csv"
    keyword_file = "keywords.csv"

if st.sidebar.button("↻ Refresh dashboard", use_container_width=True):
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("### About")
st.sidebar.caption(
    "TrendPulse analyzes video engagement, title sentiment, "
    "keywords and calculated topic trend scores."
)
st.sidebar.caption("BDA Semester Project")


# ---------------- LOAD DATA ----------------
data = load_csv(data_file)
sentiment_data = load_csv(sentiment_file)
keywords = load_csv(keyword_file)
trend_rows = load_csv("trend_scores.csv")

if source == "Real YouTube Data":
    trend_map = {
        row.get("topic", "Unknown"): number(row.get("trend_score"))
        for row in trend_rows
    }
else:
    trend_map = {}

for row in data:
    for col in ("likes", "comments", "shares", "views"):
        row[col] = number(row.get(col))

    row["engagement"] = (
        row["likes"] + row["comments"] + row["shares"]
    )

if source == "Sample Data":
    for row in data:
        topic = row.get("topic", "Unknown")
        trend_map[topic] = trend_map.get(topic, 0) + (
            row["engagement"] + row["views"] * 0.1
        )

trend_map = dict(
    sorted(trend_map.items(), key=lambda item: item[1], reverse=True)
)

if not data:
    st.error(f"No data found in data/{data_file}.")
    st.stop()


# ---------------- HERO ----------------
st.markdown("""
<div class="tp-hero">
    <div class="tp-label">Social intelligence platform</div>
    <h1 style="margin:8px 0 6px 0;">TrendPulse</h1>
    <div class="tp-subtitle">
        Discover emerging topics through engagement, sentiment,
        keywords and data-driven trend scoring.
    </div>
</div>
""", unsafe_allow_html=True)

if source == "Real YouTube Data":
    st.info(
        "Showing a collected snapshot of public YouTube videos. "
        "Automatic continuous monitoring is not enabled yet."
    )


# ---------------- OVERVIEW ----------------
total_videos = len(data)
total_views = sum(row["views"] for row in data)
total_engagement = sum(row["engagement"] for row in data)
unique_topics = len(set(row.get("topic", "Unknown") for row in data))

st.subheader("📊 Overview")

m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
m1.metric("Videos analyzed", fmt(total_videos))
m2.metric("Total views", fmt(total_views))

m3.metric("Total engagement", fmt(total_engagement))
m4.metric("Topics covered", fmt(unique_topics))

st.divider()


# ---------------- TOPIC ENGAGEMENT ----------------
st.subheader("💬 Topic Engagement")
st.caption("Likes + comments + shares, grouped by topic.")

engagement_by_topic = {}

for row in data:
    topic = row.get("topic", "Unknown")
    engagement_by_topic[topic] = (
        engagement_by_topic.get(topic, 0) + row["engagement"]
    )

engagement_by_topic = dict(
    sorted(
        engagement_by_topic.items(),
        key=lambda item: item[1],
        reverse=True,
    )
)

max_engagement = max(engagement_by_topic.values(), default=0)

for topic, value in engagement_by_topic.items():
    st.markdown(
        f"**{topic}**"
        f"<div style='text-align:right; color:#b6c2df;'>"
        f"{fmt(value)} interactions</div>",
        unsafe_allow_html=True,
    )
    st.progress(
        int(value / max_engagement * 100) if max_engagement else 0
    )

# Interactive engagement chart
st.markdown("### 📊 Engagement Comparison")
st.caption("Compare likes, comments and shares across topics.")

chart_rows = []

for row in data:
    chart_rows.append({
        "Topic": row.get("topic", "Unknown"),
        "Likes": row["likes"],
        "Comments": row["comments"],
        "Shares": row["shares"],
    })

topic_metrics = {}

for row in chart_rows:
    topic = row["Topic"]

    if topic not in topic_metrics:
        topic_metrics[topic] = {
            "Likes": 0,
            "Comments": 0,
            "Shares": 0,
        }

    for metric in ("Likes", "Comments", "Shares"):
        topic_metrics[topic][metric] += row[metric]

plot_rows = []

for topic, metrics in topic_metrics.items():
    for metric, value in metrics.items():
        plot_rows.append({
            "Topic": topic,
            "Metric": metric,
            "Count": value,
        })



if topic_metrics:
    fig = go.Figure()
    topics = list(topic_metrics.keys())

    for metric, color in [
        ("Likes", "#818cf8"),
        ("Comments", "#22d3ee"),
        ("Shares", "#f472b6"),
    ]:
        fig.add_trace(go.Bar(
            name=metric,
            x=topics,
            y=[topic_metrics[t][metric] for t in topics],
            marker_color=color,
        ))

    grid_color = (
        "#d5deed" if theme_mode == "Light Mode" else "#293550"
    )

    fig.update_layout(
        barmode="group",
        title="Engagement by Topic",
        width=1000,
        height=460,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=text_color,
        xaxis_title="Topic",
        yaxis_title="Total interactions",
        margin=dict(l=15, r=25, t=70, b=110),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        tickangle=-25,
        gridcolor=grid_color,
        color=text_color,
    )

    fig.update_yaxes(
        gridcolor=grid_color,
        color=text_color,
    )

    st.plotly_chart(
        fig,
        use_container_width=False,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": False,
        },
    )

    if st.button("⛶ Expand engagement chart", key="expand_engagement"):
        show_expanded_chart("engagement")

st.divider()

# ---------------- TREND RANKING ----------------

st.subheader("🔥 Trending Topics")
st.caption("Scores use the current model's normalized engagement, views and growth.")

if trend_map:
    for rank, (topic, score) in enumerate(trend_map.items(), start=1):
        icon = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "📈"

        left, middle, right = st.columns([0.7, 3, 1])

        left.markdown(f"### {icon}")
        middle.markdown(f"**{rank}. {topic}**")
        right.markdown(
            f"<div style='text-align:right'><b>{score:.2f}</b></div>",
            unsafe_allow_html=True,
        )

        st.progress(
            int(score / max(trend_map.values()) * 100)
            if max(trend_map.values()) > 0 else 0
        )
else:
    st.warning("Trend scores are not available yet.")

st.divider()


# ---------------- SENTIMENT ----------------
st.subheader("😊 Video Title Sentiment")
st.caption("VADER classifies the collected text titles, not audience opinions.")

sentiment_counts = {
    "Positive": 0,
    "Neutral": 0,
    "Negative": 0,
}

sentiment_by_topic = {}

for row in sentiment_data:
    label = row.get("sentiment", "").strip().title()
    topic = row.get("topic", "Unknown")

    if label in sentiment_counts:
        sentiment_counts[label] += 1
        sentiment_by_topic.setdefault(topic, {
            "Positive": 0, "Neutral": 0, "Negative": 0
        })
        sentiment_by_topic[topic][label] += 1

sentiment_total = sum(sentiment_counts.values())

# Interactive sentiment donut chart
if sentiment_total:
    donut_fig = go.Figure(data=[go.Pie(
        labels=list(sentiment_counts.keys()),
        values=list(sentiment_counts.values()),
        hole=0.62,
        marker=dict(colors=["#34d399", "#94a3b8", "#fb7185"]),
        textinfo="percent+label",
        hovertemplate="%{label}: %{value} titles (%{percent})<extra></extra>",
    )])

    donut_fig.update_layout(
        title="Video Title Sentiment Distribution",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=text_color,
        width=850,
        height=480,
        margin=dict(l=10, r=10, t=55, b=10),
        showlegend=True,
    )


    st.plotly_chart(
        donut_fig,
        use_container_width=False,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": False,
        },
    )


    if st.button("⛶ Expand sentiment chart", key="expand_sentiment"):
        show_expanded_chart("sentiment")

if sentiment_total:
    a, b, c = st.columns(3)

    for col, label, emoji in [
        (a, "Positive", "🟢"),
        (b, "Neutral", "⚪"),
        (c, "Negative", "🔴"),
    ]:
        count = sentiment_counts[label]
        pct = count / sentiment_total * 100
        col.metric(f"{emoji} {label}", fmt(count), f"{pct:.1f}%")
        col.progress(int(pct))

    with st.expander("Sentiment by topic"):
        for topic, counts in sentiment_by_topic.items():
            st.markdown(f"**{topic}**")
            st.caption(
                f"Positive: {counts['Positive']} · "
                f"Neutral: {counts['Neutral']} · "
                f"Negative: {counts['Negative']}"
            )
else:
    st.warning(
        f"No sentiment data found in {sentiment_file}. "
        "Run the sentiment analysis module."
    )

st.divider()


# ---------------- KEYWORDS ----------------
st.subheader("🔑 Top Keywords")
st.caption("Most frequently occurring words in the collected titles.")

if keywords:
    keyword_rows = sorted(
        keywords,
        key=lambda row: number(row.get("count")),
        reverse=True,
    )
    max_count = max((number(row.get("count")) for row in keyword_rows), default=0)


    # Interactive top keywords chart
    chart_keywords = keyword_rows[:10]

    keyword_fig = go.Figure(data=[go.Bar(
        x=[number(row.get("count")) for row in chart_keywords],
        y=[row.get("keyword", "") for row in chart_keywords],
        orientation="h",
        marker_color="#818cf8",
        text=[fmt(number(row.get("count"))) for row in chart_keywords],
        textposition="auto",
        hovertemplate="%{y}: %{x} mentions<extra></extra>",
    )])

    keyword_fig.update_layout(
        title="Top 10 Keywords",
        width=850,
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5e7eb",
        xaxis_title="Mentions",
        yaxis_title="Keyword",
        margin=dict(l=20, r=25, t=65, b=50),
    )

    keyword_fig.update_xaxes(gridcolor="#293550")
    keyword_fig.update_yaxes(
        gridcolor="#293550",
        autorange="reversed",
    )

    st.plotly_chart(
        keyword_fig,
        use_container_width=False,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": False,
        },
    )

    if st.button("⛶ Expand keyword chart", key="expand_keywords"):
        show_expanded_chart("keywords")

    left, right = st.columns(2)

    for index, row in enumerate(keyword_rows):
        target = left if index % 2 == 0 else right
        word = row.get("keyword", "")
        count = number(row.get("count"))

        with target:
            st.markdown(
                f"<div class='tp-card'><b>#{index + 1} &nbsp; {word}</b>"
                f"<div class='tp-muted'>{fmt(count)} mentions</div></div>",
                unsafe_allow_html=True,
            )
            st.progress(
                int(count / max_count * 100) if max_count else 0
            )
else:
    st.info("No keyword results available. Run keyword_analysis.py first.")


# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "TrendPulse · Big Data Analytics · "
    "Built with Python, Streamlit, Pandas, NLTK and YouTube Data API v3."
)


# ---------------- TREND GROWTH ----------------
st.divider()
st.subheader("📈 Trend Growth")
st.caption(
    "Compares the latest two recorded snapshots. "
    "Changes reflect collected video samples, not all of YouTube."
)

if source == "Real YouTube Data":
    growth_rows = load_csv("trend_growth.csv")

    if growth_rows:
        growth_rows = sorted(
            growth_rows,
            key=lambda row: number(
                row.get("engagement_change_percent")
            ) if row.get("engagement_change_percent") not in ("", None)
            else float("-inf"),
            reverse=True,
        )

        for row in growth_rows:
            topic = row.get("topic", "Unknown")
            views_change = row.get("views_change_percent", "")
            engagement_change = row.get(
                "engagement_change_percent", ""
            )

            left, middle, right = st.columns([2, 1, 1])

            left.markdown(f"**{topic}**")

            if views_change not in ("", None):
                left.caption(f"Views change: {views_change}%")
            else:
                left.caption("Views change: not calculable")

            if engagement_change not in ("", None):
                try:
                    change = float(engagement_change)
                    right.metric(
                        "Engagement change",
                        f"{change:+.2f}%",
                    )
                except ValueError:
                    right.metric("Engagement change", "N/A")
            else:
                right.metric("Engagement change", "N/A")

            try:
                view_value = float(views_change)
                middle.metric("Views change", f"{view_value:+.2f}%")
            except (ValueError, TypeError):
                middle.metric("Views change", "N/A")

            st.divider()

        st.info(
            "Large percentage changes can occur when the earlier "
            "snapshot had very low views or engagement. Compare the "
            "underlying totals before interpreting a topic as trending."
        )
    else:
        st.info(
            "No growth results yet. Record at least two snapshots "
            "and run src/trend_growth.py."
        )
else:
    st.info(
        "Trend Growth is available with Real YouTube Data. "
        "Switch data source in the sidebar to view it."
    )
