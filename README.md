# 📊 TrendPulse – Real-Time Social Media Trend Analyzer

TrendPulse is a data analytics dashboard designed to analyze social media trends, audience engagement, sentiment, and popular keywords through interactive visualizations. It helps users explore social media data and understand which topics are attracting attention.

🌐 **Live Demo:** [Open TrendPulse Dashboard](PASTE_YOUR_STREAMLIT_APP_URL_HERE)

📁 **GitHub Repository:** https://github.com/rohanw2004/Trendpulse-

---

## 🚀 Features

- **Social Media Data Analysis:** Explore social media topics and their engagement metrics.
- **Trend Analysis:** Analyze likes, comments, shares, and views to understand topic popularity.
- **Sentiment Analysis:** Analyze text sentiment using VADER.
- **Interactive Visualizations:** Display analytical results through interactive Plotly charts.
- **Keyword Analysis:** Identify and explore frequently occurring keywords.
- **Engagement Analysis:** Compare engagement across different topics and platforms.
- **Dark and Light Modes:** Switch between visual themes for a better dashboard experience.
- **CSV-Based Data Processing:** Load and analyze structured social media datasets.
- **Sample and YouTube Data:** Explore available datasets and their analytical results.

> **Note:** The current project analyzes available datasets. Continuous live monitoring of social media platforms is not yet enabled.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| Pandas | Data processing and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive charts and visualizations |
| VADER Sentiment | Text sentiment analysis |
| CSV | Structured data storage |

---

## 🏗️ System Architecture

```text
Social Media Datasets
         |
         v
 Data Loading
         |
         v
 Data Preprocessing
         |
         v
 Trend and Engagement Analysis
         |
         v
 Sentiment and Keyword Analysis
         |
         v
 Interactive Plotly Visualizations
         |
         v
    Streamlit Dashboard
```

---

## 📂 Project Structure

```text
Trendpulse-/
├── app.py
├── requirements.txt
├── data/
│   ├── sample_data.csv
│   ├── analyzed_data.csv
│   ├── keywords.csv
│   ├── youtube_data.csv
│   ├── youtube_analyzed_data.csv
│  


📚 Academic Subject Integration

TrendPulse is developed as a common project for two different academic subjects: Big Data Analytics (BDA) and Natural Language Processing (NLP). Both subjects contribute different functionalities and technical concepts to the same application while maintaining their individual academic objectives.

1. 📊 Big Data Analytics (BDA)

The BDA component of TrendPulse focuses on collecting, processing, analyzing, and visualizing structured social media datasets. It uses engagement metrics such as likes, comments, shares, and views to understand topic popularity and identify emerging trends. The system performs data processing, trend scoring, engagement analysis, and historical trend comparisons to generate meaningful insights. Interactive visualizations created using Plotly and presented through Streamlit help users explore analytical results and understand patterns across different social media platforms.

2. 🧠 Natural Language Processing (NLP)

The NLP component of TrendPulse focuses on understanding and analyzing the textual content of social media posts. It applies text processing techniques, sentiment analysis, and keyword extraction to identify public opinions and frequently discussed topics. Using VADER Sentiment Analysis, the system classifies text into positive, negative, and neutral sentiments. Keyword analysis helps identify commonly occurring words and important discussion topics. These techniques transform unstructured social media text into meaningful information that can help users understand audience reactions and the context behind trending topics.

🔗 Integration of BDA and NLP

Both components work together within the TrendPulse dashboard. BDA provides quantitative insights through engagement metrics and trend analysis, while NLP provides textual insights through sentiment and keyword analysis. Their combination offers a broader understanding of social media trends by connecting numerical engagement patterns with the opinions and discussions expressed in social media content.
