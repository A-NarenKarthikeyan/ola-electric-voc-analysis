# ⚡ OLA Electric — Voice of Customer Crisis Analysis

> *Diagnosing a market share collapse through 7,119 customer reviews, NLP sentiment analysis, and multi-label complaint classification.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit)
![VADER](https://img.shields.io/badge/NLP-VADER_Sentiment-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## 📌 Business Context

OLA Electric, once holding **38.83% of India's EV two-wheeler market**, saw its share collapse to **17.35% by July 2025** — a decline of over 55% in 12 months. While internal reports cited operational challenges, the customer experience breakdown was playing out publicly across thousands of Play Store reviews, complaint forums, and social media posts.

This project uses real scraped customer data to answer one business question:

> **"What specific, quantifiable complaint categories are driving OLA Electric's rating decline — and which should be prioritized for intervention first?"**

---

## 🔍 Project Overview

An end-to-end data analytics project covering:

- **Data collection** via Google Play Store scraping (`google-play-scraper`)
- **NLP sentiment analysis** using VADER (validated at 82.2% agreement with star ratings)
- **Multi-label complaint classification** with 99.2% manual validation accuracy
- **Statistical testing** — Kruskal-Wallis, Mann-Whitney U, Spearman correlation
- **Interactive dashboard** built with Streamlit and Plotly in OLA's brand colors

---

## 🔬 Methodology Pipeline

```
Google Play Store
        ↓
Data Collection — 7,119 reviews (May 2022 – Jun 2026)
        ↓
Data Cleaning — 22 engineered features, 100% row retention
        ↓
VADER Sentiment Analysis — compound score per review
        ↓
Multi-label Keyword Classifier — 10 complaint categories
        ↓
Manual Validation — 248 reviews, 99.2% agreement rate
        ↓
EDA + Statistical Testing — 4 hypothesis tests
        ↓
Insight Synthesis — 9 conclusions, 5 recommendations
        ↓
Streamlit Dashboard — 6 pages, OLA brand theme
```

**Key methodological decisions:**

| Decision | Rationale |
|---|---|
| VADER over BERT | Lexicon-based, explainable, no training data required. Upgrade not warranted by validation evidence. |
| Rule-based over LDA | Quantifying known operational failures, not discovering unknown topics. 99.2% accuracy confirmed. |
| Multi-label classification | Real complaints span multiple categories. Single-label would discard analytical signal. |
| Star rating as primary health metric | More reliable than VADER for absolute negative sentiment due to factual complaint language patterns in Indian English reviews. |

---

## 📊 Key Findings

### Finding 1 — Software is the Most Widespread Failure
**50.5%** of all reviews mention app or software issues — nearly **5× the next highest category**. The app is the connective tissue through which every other failure is experienced.

### Finding 2 — Customer Care is the Most Severe Failure
Customer Care complaints produce a **93.9% one-star rate** — the highest of any category. When customers contact OLA's support and receive no resolution, the relationship ends permanently.

### Finding 3 — Service Center and Spare Parts Are Structurally Linked
These two failures co-occur in **336 reviews**. Spare Parts has the most negative average VADER sentiment (−0.385) despite the lowest volume — when parts are unavailable, the experience is catastrophic.

### Finding 4 — Zero Developer Engagement Across Four Years
OLA Electric has maintained a **0% developer response rate** across 7,119 reviews spanning 4 years. Industry benchmark: 40–60% on negative reviews.

### Finding 5 — Sentiment Differs Significantly Across Categories
Kruskal-Wallis confirms sentiment scores differ significantly across complaint categories (**H=274.3, p<0.001**). Not all failures feel equally damaging. Volume alone should not drive prioritization.

---

## 📈 Statistical Validation

| Test | Result | Finding |
|---|---|---|
| Kruskal-Wallis | H=274.3, p<0.001 | Sentiment differs significantly across complaint categories |
| Mann-Whitney U | p=3.74e-50 | Post-crisis sentiment significantly higher than pre-crisis |
| Spearman (complaint count vs sentiment) | r=−0.341, p<0.001 | More complaint categories = more negative language |
| Spearman (word count vs sentiment) | r=−0.369, p<0.001 | Longer reviews are almost always more negative |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| `google-play-scraper` | Data collection |
| Pandas, NumPy | Data cleaning & engineering |
| VADER (`vaderSentiment`) | Sentiment analysis |
| Scikit-learn | Topic modeling validation |
| Scipy | Statistical hypothesis testing |
| Matplotlib, Seaborn | EDA visualizations |
| Plotly | Interactive dashboard charts |
| Streamlit | Dashboard framework & deployment |

---

## 📁 Project Structure

```
ola_electric_voc_analysis/
│
├── data/
│   ├── raw/
│   │   └── ola_reviews_raw.csv           # 7,119 scraped reviews
│   ├── cleaned/
│   │   ├── ola_reviews_cleaned.csv       # 22 engineered features
│   │   └── ola_monthly_trends.csv        # Monthly aggregation
│   └── classified/
│       └── ola_reviews_classified.csv    # Multi-label classified
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_sentiment_analysis.ipynb
│   ├── 04_complaint_classification.ipynb
│   └── 05_eda_and_statistics.ipynb
│
├── dashboard/
│   └── app.py                            # Streamlit dashboard
│
├── outputs/
│   ├── charts/                           # Saved visualizations
│   ├── findings_summary.md              # Full findings report
│   ├── observations.md                  # OHC insight register
│   └── interview_verbal_summary.txt     # Interview prep
│
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/coderfox-cap/ola-electric-voc-analysis.git
cd ola-electric-voc-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
cd dashboard
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`

### 4. Re-run the analysis (optional)
Run notebooks in order from `notebooks/01` through `notebooks/05`.
Note: Notebook 01 will re-scrape fresh data from Google Play Store.

---

## 📋 Requirements

```
google-play-scraper==1.2.7
pandas==2.1.0
numpy==1.24.0
matplotlib==3.7.0
seaborn==0.12.0
nltk==3.8.1
vaderSentiment==3.3.2
textblob==0.17.1
scikit-learn==1.3.0
streamlit==1.28.0
wordcloud==1.9.2
plotly==5.17.0
openpyxl==3.1.2
scipy==1.11.0
```

---

## 💡 Business Recommendations

| Priority | Recommendation | Category | Expected Impact |
|---|---|---|---|
| 🔴 Critical | Rebuild customer care with 24h SLA and visible ticket tracking | Customer Care | Addresses 93.9% one-star rate |
| 🔴 Critical | Fix app connectivity, login, and display failures via OTA update | Software / App | Removes complaint from ~25% of reviews |
| 🟠 High | Treat service center + spare parts as one system | Operations | Addresses second-lowest avg rating (1.28★) |
| 🟡 Medium | Activate Play Store as customer recovery channel | Engagement | First response in 4 years — visible accountability |
| 🟡 Medium | Implement review-based early warning system | Data Infrastructure | Surfaces high-damage complaints before escalation |

---

## 👤 Author

**Naren Karthikeyan A**
Integrated MTech — Computer Science (Data Science)
VIT Vellore | Expected 2028

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/narenkarthikeyana/)
[![GitHub](https://img.shields.io/badge/GitHub-Naren-Karthikeyan-black?style=flat-square&logo=github)](https://github.com/A-NarenKarthikeyan)

---

> *"We are not trying to discover random topics. We are trying to identify and quantify operational root causes behind customer dissatisfaction."*
> — Project Design Principle, Phase 4

---

**Data source:** Google Play Store (public reviews, scraped for academic/portfolio purposes)
**Analysis period:** May 2022 – June 2026
**Total reviews:** 7,119
