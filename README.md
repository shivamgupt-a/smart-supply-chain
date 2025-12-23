# 🚀 Smart Supply Chain Demand Forecasting with Sustainability Analytics

An intelligent end-to-end machine learning system that forecasts product demand, optimizes inventory levels, and tracks carbon emissions to help businesses reduce costs by 15-30% while minimizing environmental impact.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Business Problem](#business-problem)
- [Project Status](#-project-statusatus)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Results So Far](#results-so-far)
- [Roadmap](#roadmap)
- [Author](#author)

---

## 🎯 Overview

This project builds a comprehensive supply chain forecasting system that combines:
- **Demand Forecasting**: ARIMA, Prophet, and LSTM models for accurate sales predictions
- **Inventory Optimization**: Economic Order Quantity (EOQ) and reorder point calculations
- **Sustainability Tracking**: Carbon footprint monitoring across supply chain operations
- **Interactive Dashboard**: Real-time visualizations and recommendations via Streamlit

**Dataset**: Rossmann Store Sales (Kaggle) - 1,017,209 records from 1,115 stores (2013-2015)

---

## 💼 Business Problem

Supply chain managers face three critical challenges:

1. **Demand Uncertainty** → Stock-outs or excess inventory
2. **Inventory Inefficiency** → 20-30% higher holding costs
3. **Sustainability Pressure** → Need to track and reduce carbon emissions

**Expected Impact**:
- Reduce forecast error from 25-30% to 10-15% (MAPE)
- Cut excess inventory costs by 15-30%
- Decrease stock-out incidents by 20-25%
- Provide carbon footprint visibility for ESG reporting

---

## 📊 Project Status

### ✅ **Week 1: Exploratory Data Analysis** (COMPLETED - Dec 2024)

**What I Did:**
- Analyzed 1,017,209 sales records across 1,115 stores
- Performed comprehensive data quality checks (missing values, outliers, duplicates)
- Created time-based features (year, month, day, week, quarter)
- Discovered key business patterns and seasonality

**Key Findings:**
- 📈 **Strong Weekly Seasonality**: Sunday sales are 35% higher than Monday
- 📆 **Monthly Patterns**: December shows 28% sales spike (Christmas effect)
- 🎯 **Promotion Impact**: Promotions increase sales by 40.3%
- 👥 **Customer Correlation**: Very strong relationship with sales (r = 0.82)
- 🏪 **Store Variation**: Store Type matters significantly for performance
- 🏢 **Competition Effect**: Stores near competitors show different patterns

**Deliverables:**
- ✅ `01_EDA_Rossmann.ipynb` - Complete exploratory analysis
- ✅ `train_with_features.csv` - Processed dataset with engineered features
- ✅ `store_1_data.csv` - Single store data for baseline modeling
- ✅ `eda_insights.json` - Key metrics and statistics
- ✅ 15+ visualizations documenting patterns

**Visualizations Created:**
- Time series plots with trend analysis
- Sales distribution and box plots
- Seasonality analysis (monthly, weekly)
- Promotion impact comparison
- Store type and assortment analysis
- Competition distance effects
- Correlation heatmaps

---

### 🔄 **Week 2: Baseline Models & Preprocessing** (IN PROGRESS)

**Current Tasks:**
- [ ] Build moving average baseline models (7-day, 30-day)
- [ ] Create proper train/test splits (time-based)
- [ ] Establish MAPE benchmarks for comparison
- [ ] Additional feature engineering
- [ ] Evaluate baseline performance

**Target**: Establish baseline MAPE of 15-20% to beat with advanced models



---

## 🎯 Key Features

### 📈 Demand Forecasting
- Multiple models: Moving Average, ARIMA, Prophet, LSTM
- Handles seasonality, trends, and promotions
- Confidence intervals for predictions
- Model comparison and ensemble methods

### 📦 Inventory Optimization
- Economic Order Quantity (EOQ) calculations
- Dynamic reorder point recommendations
- Safety stock based on service levels
- Cost savings quantification

### 🌱 Sustainability Analytics
- Carbon footprint tracking per shipment
- Transport mode comparison (truck, rail, ship)
- Green route recommendations
- Emissions trend monitoring

### 📊 Interactive Dashboard
- Executive summary with KPIs
- Multi-product forecasting views
- Inventory recommendations table
- Carbon tracker with visualizations
- Model performance comparison

---

## 🛠️ Tech Stack

**Programming & Data Science**
- Python 3.9+
- Pandas, NumPy, SciPy

**Machine Learning**
- Scikit-learn (preprocessing, metrics)
- Statsmodels (ARIMA)
- Prophet (Facebook's time series library)
- TensorFlow/Keras (LSTM)

**Visualization**
- Matplotlib, Seaborn
- Plotly (interactive charts)
- Streamlit (dashboard)

**Development Tools**
- Jupyter Notebook
- Git & GitHub
- VS Code

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Jupyter Notebook
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https:/github.com/smart-supply-chain/shivamgupt002/y-chain.git
cd smart-supply-chain
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Kaggle dataset**
- Go to: https://www.kaggle.com/competitions/rossmann-store-sales/data
- Download `train.csv`, `test.csv`, `store.csv`
- Place in `data/raw/` folder

5. **Run notebooks**
```bash
jupyter notebook
# Navigate to notebooks/ and open 01_EDA_Rossmann.ipynb
```
