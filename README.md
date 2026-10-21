# 📊 TrendPulse – Real-Time Social Media Trend Analyzer

**A Big Data Analytics Project**

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
