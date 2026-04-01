# Notebooks

This directory contains Jupyter notebooks documenting the analytical and machine learning work for the AdventureWorks Sales Analytics project. Each notebook is structured for two audiences executives and hiring managers can read the summary sections at the top, technical reviewers can work through the full methodology.

---

## Contents

### 1. `sales_forecasting.ipynb`
**Time Series Forecasting Using Facebook Prophet**

12 month revenue forecasts across channels and product categories using Facebook Prophet. Includes exploratory analysis, model selection rationale, metric-specific tuning, cross-validation accuracy assessment, and business recommendations.

**Metrics forecasted:**
- Total Revenue
- Reseller Revenue
- Internet Revenue
- Revenue by Product Category (Bikes, Components, Accessories, Clothing)

**Key findings:**
- Total Revenue MAPE: 31.4%  best performing metric with a clean trend and consistent seasonality
- Reseller Revenue MAPE: 68.7%  high monthly volatility from large individual orders makes this channel harder to predict
- Internet Revenue MAE improved from $880K to $487K after metric-specific tuning  MAPE is misleading here due to a June 2020 data anomaly ($49K actual vs typical $500K–$1.9M range)
- COVID-19 overlap in the final training year creates forecast uncertainty  the Internet channel acceleration may be partially pandemic-driven rather than a permanent structural shift

**Tools:** Prophet, pandas, matplotlib, scikit-learn

**Output:** `outputs/sales_forecasts.csv`  loaded into Power BI to add forecast lines to trend visuals

---

### 2. `reseller_segmentation.ipynb`
**K-Means Clustering - Reseller Segmentation**

Data-driven reseller segmentation using K-Means clustering across six features  revenue, order frequency, profit margin, average order value, product category breadth, and recency. Replaces intuitive tier groupings with statistically derived segments that the sales team can act on.

**Features used:**
- Total Revenue
- Total Orders
- Profit Margin %
- Average Order Value
- Unique Product Categories purchased
- Recency (days since last order)

**Key findings:**
- Silhouette analysis selected K=2 as optimal  the reseller base naturally separates into two tiers rather than the four or five segments sometimes assumed in B2B sales contexts
- Star Resellers (n=154)  avg revenue $383K, avg 261 orders
- Growth Partners (n=481)  avg revenue $45K, avg 43 orders
- Margins are uniformly thin (~1%) across both segments  reinforcing the structural margin issue identified in the dashboard analysis. The primary differentiator between segments is scale not profitability

**Tools:** scikit-learn (KMeans, StandardScaler, PCA, silhouette_score), pandas, matplotlib

**Output:** `outputs/reseller_segments.csv`  loaded into Power BI to colour the Reseller Analytics scatter chart by segment

---

### 3. `customer_segmentation.ipynb`
**K-Means Clustering  Customer RFM Segmentation** *(In Progress)*

RFM (Recency, Frequency, Monetary) based customer segmentation using K-Means clustering. Replaces the manual High/Mid/Low Value customer tiers on the Customer Analytics dashboard page with data-driven segments that reflect actual purchasing behaviour patterns.

**Features planned:**
- Recency  days since last purchase
- Frequency  total order count
- Monetary  total revenue
- Average Order Value

**Expected segments:**
- Champions  high spend, high frequency, recent purchase
- Loyal Customers  high frequency, moderate spend
- At Risk  previously frequent, declining recency
- Lost Customers  low recency, low frequency

**Tools:** scikit-learn, pandas, matplotlib

**Output:** `outputs/customer_segments.csv`  loaded into Power BI Customer Analytics page

---

## Design Decisions

**Why Prophet over ARIMA for forecasting?**
Prophet handles yearly seasonality automatically without manual parameter identification. With only 36 monthly observations ARIMA's manual tuning burden was disproportionate. Prophet also produces interpretable confidence intervals that are easy to communicate to non-technical stakeholders.

**Why K-Means for segmentation?**
K-Means is the industry standard for customer and reseller segmentation  well understood, computationally efficient, and produces segments that are straightforward to explain to a sales or marketing team. The silhouette score provides an objective measure for selecting the number of clusters rather than relying on intuition.

**Why StandardScaler before clustering?**
K-Means is distance-based  without scaling, Total Revenue dominates purely because of its large magnitude ($1–$877K range) compared to Unique Categories (1–4 range). Scaling puts all features on equal footing so the algorithm segments on commercial behaviour rather than just revenue size.

**Why both MAPE and MAE are reported**
MAPE divides by the actual value  in months where actual revenue is near zero (such as the June 2020 Internet Revenue anomaly at $49K) even a small absolute error produces an enormous percentage error. Reporting MAE alongside MAPE gives a more complete and honest picture of forecast accuracy.

---

## Running the Notebooks

**Prerequisites**
```bash
pip install prophet scikit-learn pandas matplotlib nbformat openpyxl yellowbrick
```

**Data required**
Place `AdventureWorks_Sales_Cleaned.xlsx` in the project root before running. The cleaned file is produced by `scripts/adventureworks_cleaning.py`.

**Output directory**
All charts and CSV exports are written to `outputs/` which is created automatically on first run.

**Recommended run order**
```
1. scripts/adventureworks_cleaning.py   # produces cleaned Excel file
2. notebooks/sales_forecasting.ipynb   # produces sales_forecasts.csv
3. notebooks/reseller_segmentation.ipynb  # produces reseller_segments.csv
4. notebooks/customer_segmentation.ipynb  # produces customer_segments.csv
```

---

## Outputs Summary

| File | Source Notebook | Power BI Use |
|---|---|---|
| `sales_forecasts.csv` | sales_forecasting.ipynb | Forecast lines on trend visuals |
| `reseller_segments.csv` | reseller_segmentation.ipynb | Scatter chart colouring on Reseller Analytics page |
| `customer_segments.csv` | customer_segmentation.ipynb | Donut chart and slicer on Customer Analytics page |
| `exploratory_analysis.png` | sales_forecasting.ipynb | GitHub README |
| `forecast_*.png` | sales_forecasting.ipynb | GitHub README |
| `reseller_*.png` | reseller_segmentation.ipynb | GitHub README |

---

## Limitations

- **Training data volume**  36 monthly observations for forecasting and 635 resellers for segmentation. Both models would benefit significantly from additional years of data. Forecast accuracy metrics should be treated as directional indicators.
- **COVID-19 overlap**  the final year of training data overlaps the pandemic period. Internet channel trends in particular may reflect temporary behavioural shifts rather than permanent structural changes.
- **Static segmentation**  K-Means segments are computed on the full historical period. A production implementation would retrain periodically as new transaction data arrives to keep segments current.
- **Profit forecasting excluded**  total profit was excluded from the forecasting notebook due to extreme MAPE scores caused by near-zero actual values in certain months. A separate profit model using margin percentage as the target variable would be more tractable.
