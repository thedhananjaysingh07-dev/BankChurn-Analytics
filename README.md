# 🏦 Bank Customer Churn Analytics
### Customer Segmentation & Churn Pattern Analytics in European Banking
**Unified Mentor Finance Analytics Internship | August 2026**

---

## 🚀 Live Dashboard
> **[View Live Streamlit Dashboard →](https://bankchurn-analytics-7jscndsfaappd3mgvamxzu8.streamlit.app/)**

---

## 📌 Project Overview

A full end-to-end data analytics project analysing customer churn in a European retail bank — covering all four analytics stages:

| Stage | Description |
|-------|-------------|
| **Descriptive** | EDA across 10,000 customers, 6 hypothesis tests, survival analysis |
| **Diagnostic** | K-Means clustering, 4 customer personas, SHAP explainability |
| **Predictive** | Random Forest model — AUC 0.851, Recall 64%, 4-tier risk scoring |
| **Prescriptive** | Retention ROI Simulator — live what-if scenario modelling |

---

## 🔑 Key Findings

| Finding | Value |
|---------|-------|
| Overall Churn Rate | **20.37%** vs 15% European benchmark |
| Revenue at Risk | **€185.6M** in customer balance |
| Most Extreme Segment | Germany + Age 46-60 = **67.33% churn** |
| Best ML Model | Random Forest — **AUC 0.851, Recall 64%** |
| Critical Risk Tier | **73.7%** actual churn rate confirmed |
| Top Churn Predictors | **Age** and **IsActiveMember** (SHAP) |

> **Most counterintuitive finding:** Age 46-60 churns at **51.12%** — our hypothesis predicted older customers would be more loyal. The data rejected this completely.

> **Most actionable finding:** Clusters 0 and 3 hold identical balances (~€122K) but churn at **16% vs 31%**. The sole differentiator is engagement status. Re-engaging inactive high-value customers is the single highest-ROI retention intervention available.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-3.3-green)
![Plotly](https://img.shields.io/badge/Plotly-6.8-blue?logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)

**Libraries:** pandas, numpy, matplotlib, seaborn, plotly, streamlit, scikit-learn, xgboost, imbalanced-learn, shap, lifelines, sweetviz

---

## 📊 Dashboard Features

The Streamlit dashboard has 6 interactive tabs:

- **Overview** — 5 KPI cards, geography bar chart, churn donut, insight callouts
- **Geography** — Churn by country, heatmap (Geography × Age), gender-geography analysis
- **Demographics** — Age group, gender, engagement status, product count churn rates
- **High Value Customers** — CLV segment analysis, revenue lost, persona churn rates
- **Churn Predictor** — Live Random Forest model: input customer details → instant churn probability + risk tier + retention recommendation
- **Retention ROI Simulator** — What-if modelling: adjust campaign budget and target segment → net ROI calculation

---

## 📁 Project Structure

```
BankChurn-Analytics/
├── app/
│   └── app.py                          # Streamlit dashboard (6 tabs)
├── data/
│   ├── European_Bank.csv               # Raw dataset (10,000 customers)
│   ├── European_Bank_Cleaned.csv       # Cleaned + 8 engineered features
│   ├── European_Bank_Clustered.csv     # + K-Means cluster labels
│   ├── European_Bank_Segmented.csv     # + Persona labels
│   └── Customer_Risk_Scores.csv        # ML churn probability scores
├── models/
│   └── rf_model.pkl                    # Trained Random Forest model
├── notebooks/
│   ├── 01_data_loading_and_quality.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_clustering_and_personas.ipynb
│   └── 04_baseline_models.ipynb        # ML, SHAP, risk scoring
├── reports/
│   ├── Executive_Summary_BankChurn_Analytics.pdf
│   ├── executive_summary_notes.txt
│   ├── benchmarks.txt
│   └── [26 chart PNGs — 01 to 26]
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/thedhananjaysingh07-dev/BankChurn-Analytics.git
cd BankChurn-Analytics

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit dashboard
streamlit run app/app.py
```

---

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| `01_data_loading_and_quality.ipynb` | Data ingestion, quality checks, feature engineering |
| `02_exploratory_data_analysis.ipynb` | EDA, hypothesis testing, survival analysis, 22 charts |
| `03_clustering_and_personas.ipynb` | K-Means clustering, persona profiling, segmented CSV |
| `04_baseline_models.ipynb` | 6 ML models, SMOTE, SHAP, risk scoring |

---

## 📈 Model Performance Summary

| Model | Recall | Precision | F1-Score | AUC |
|-------|--------|-----------|----------|-----|
| Logistic Regression | 0.40 | 0.39 | 0.39 | 0.698 |
| Decision Tree | 0.64 | 0.47 | 0.54 | 0.826 |
| **Random Forest** ✅ | **0.64** | **0.59** | **0.61** | **0.851** |
| XGBoost | 0.58 | 0.61 | 0.59 | 0.836 |

*Random Forest selected as production model — best balance of recall, precision and AUC.*

---

## 👤 Author

**Dhananjay Singh**
B.Com Honours — Maharaja Agrasen College, University of Delhi
Unified Mentor Finance Analytics Internship | 2026

[![GitHub](https://img.shields.io/badge/GitHub-thedhananjaysingh07--dev-black?logo=github)](https://github.com/thedhananjaysingh07-dev)

---

## 📄 License

This project was completed as part of the Unified Mentor performance-based stipend internship program. Dataset sourced from European banking records for academic analytics purposes.
