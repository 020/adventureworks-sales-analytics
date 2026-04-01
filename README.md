# AdventureWorks Sales Analytics & Predictive Intelligence

A end-to-end data analytics project demonstrating the full pipeline from raw data through cleaning, analysis, and interactive dashboard development with predictive analytics and machine learning..

Built using **Python**, **SQL**, and **Power BI** across a real-world style multi-channel sales dataset covering $US 109M in transactions across 4 fiscal years.

---

## Project Status
| Phase | Status |
|---|---|
| Data Cleaning & Preparation | ✅ Complete |
| Exploratory Data Analysis | ✅ Complete |
| Power BI Dashboard | ✅ Complete |
| Machine Learning & Predictive Analytics | 🔜 In Progress |

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Cleaning](#data-cleaning)
- [Power BI Dashboard](#power-bi-dashboard)
- [Key Insights](#key-insights)
- [Roadmap - Predictive Analytics](#roadmap)
- [How to Run](#how-to-run)
- [Author](#author)

---

## Project Overview

This project simulates the kind of end-to-end analytics engagement a business would commission from a data consultant. The goal was to take raw multi-sheet sales data, assess and clean it properly, model it correctly, and deliver an interactive executive dashboard that answers real business questions.

**Business questions answered:**
- How is overall revenue and profit trending year over year?
- Which products and categories drive the most revenue and margin?
- Where are the highest performing sales territories geographically?
- What does the customer base look like and how is it growing?
- How does the Reseller channel compare to the Internet channel?

---

## Dataset

**Source:** Microsoft AdventureWorks Sample Dataset  
**License:** Microsoft Sample Data - provided for learning and demonstration purposes  
**Period:** 1 July 2017 to 30 June 2021 (4 fiscal years)  
**Total Transactions:** 121,253  
**Channels:** Reseller (60,855 transactions) and Internet (60,398 transactions)  
**Territories:** 11 across North America, Europe, and Pacific

| Sheet | Rows | Description |
|---|---|---|
| Sales_data | 121,253 | Core transaction table |
| Customer_data | 18,485 | Internet sales customers |
| Reseller_data | 702 | Reseller business details |
| Product_data | 397 | Product catalogue |
| Date_data | 1,461 | Date dimension table |
| Sales Order_data | 121,253 | Order channel information |
| Sales Territory_data | 11 | Territory and region details |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Data cleaning and preparation |
| pandas | Data manipulation and transformation |
| openpyxl | Excel file reading and writing |
| Power BI Desktop | Dashboard development and data modelling |
| DAX | Measures and calculated columns in Power BI |
| GitHub | Version control and portfolio hosting |

**Coming soon:**
| Tool | Purpose |
|---|---|
| scikit-learn | Machine learning models |
| Prophet / ARIMA | Time series forecasting |
| XGBoost | Customer churn prediction |
| Jupyter Notebooks | ML analysis and documentation |
| matplotlib / seaborn | Exploratory data visualisation |

---

## Project Structure

```
adventureworks-sales-analytics/
│
├── data/
│   ├── AdventureWorks_Sales.xlsx              # Original raw data
│   └── AdventureWorks_Sales_Cleaned.xlsx      # Cleaned output ready for Power BI
│
├── scripts/
│   └── adventureworks_cleaning.py             # Data cleaning script
│
├── notebooks/                                 # Coming soon
│   ├── sales_forecasting.ipynb
│   ├── churn_prediction.ipynb
│   └── customer_segmentation.ipynb
│
├── models/                                    # Coming soon
│   ├── sales_forecast_model.pkl
│   ├── churn_model.pkl
│   └── segmentation_model.pkl
│
├── dashboard/
│   └── AdventureWorks_Dashboard.pbix          # Power BI dashboard file
│
└── README.md
```

---

## Data Cleaning

Full cleaning documentation is available in [`scripts/README.md`](scripts/README.md).

**Summary of issues found and resolved:**

| Sheet | Issue | Resolution |
|---|---|---|
| Sales_data | Date columns stored as integers (YYYYMMDD) | Converted to proper date columns |
| Sales_data | 2,113 null ShipDates | Retained - valid unshipped orders |
| Sales_data | Channel mixing via -1 surrogate keys | Added IsSale_Reseller and IsSale_Internet flags |
| Sales_data | 3,247 rows with minor sales amount variance | Documented - likely rounding or discount related |
| Customer_data | 1 Not Applicable row (CustomerKey = -1) | Removed |
| Reseller_data | 1 Not Applicable row (ResellerKey = -1) | Removed |
| Product_data | 56 null Color values | Filled with "Unknown" |
| Date_data | Datetime instead of date format | Stripped time component |

**Key design decision - why -1 rows were kept in Sales_data:**

The -1 surrogate keys in the Sales table represent real revenue-generating transactions that simply don't have a linked customer or reseller depending on the channel. Removing them would understate total revenue. Instead, channel flag columns were added so Power BI can filter contextually depending on the analysis being performed.

---

## Power BI Dashboard

The dashboard is structured across four pages, each telling a distinct part of the business story:

### Page 1 - Executive Summary
High level KPIs and trends for leadership. Shows total revenue, profit, orders, margin, and average order value with year over year comparisons. Includes revenue trend over time and a channel split between Reseller and Internet sales.

### Page 2 - Sales by Product
Drill-down analysis by product category, subcategory, and individual product. Includes a profitability scatter plot identifying star products, volume drivers, and hidden gems based on revenue versus margin positioning.

### Page 3 - Sales by Region
Geographic analysis using Azure Maps showing reseller sales territory performance. Covers 11 territories across the United States, Canada, United Kingdom, France, Germany, and Australia.

### Page 4 - Customer Analysis
Customer base analysis including total customers, new customers, average revenue per customer, and customer value segmentation. Splits internet sales customers by geography using customer address data.

### Page 5 - Detail View
Full transaction level drill-through table accessible via navigation buttons from any page. Filterable by channel, territory, and date.

**Dashboard features:**
- Navigation buttons on every page for intuitive browsing
- Year and month slicers consistent across all pages
- Conditional formatting highlighting negative profit in red
- Drill-through from summary pages to transaction detail
- Azure Maps for geographic visualisation
- Tooltips showing full KPI context on hover

---

## Key Insights

> Note: Insights are based on the AdventureWorks sample dataset and are illustrative of the analytical approach rather than real business findings.

- Reseller and Internet channels contribute roughly equal transaction volumes (50.1% vs 49.9%) but differ significantly in average order value
- The Pacific region including Australia shows strong revenue relative to its territory count suggesting an opportunity for further expansion
- Product Color nulls were concentrated in the Components category indicating a cataloguing gap rather than a data entry issue
- 2,113 unshipped orders represent a fulfilment tracking opportunity worth investigating in a real business context

---

## Roadmap - Predictive Analytics <a name="roadmap"></a>

The next phase of this project will add machine learning models to move from descriptive to predictive analytics:

**Sales Forecasting**
- Predict monthly revenue for the next 12 months
- Compare ARIMA, Prophet, and scikit-learn regression approaches
- Integrate forecast output into Power BI as a forward-looking trend line

**Customer Churn Prediction**
- Build a binary classification model identifying customers at risk of not returning
- Features: purchase frequency, recency, average order value, territory
- Model: XGBoost with SHAP values for explainability

**Customer Segmentation**
- Replace manual High/Mid/Low Value segments with K-Means clustering
- Let the data define natural customer groupings
- Visualise clusters in Power BI for business interpretation

**Product Demand Forecasting**
- Predict which product categories will grow or decline next quarter
- Support inventory planning and marketing allocation decisions

---

## How to Run

**Data Cleaning Script**
```bash
# Clone the repository
git clone https://github.com/yourusername/adventureworks-sales-analytics.git

# Install dependencies
pip install pandas openpyxl

# Run the cleaning script
python scripts/adventureworks_cleaning.py
```

The script expects `AdventureWorks_Sales.xlsx` in the `data/` folder and outputs `AdventureWorks_Sales_Cleaned.xlsx` to the same folder.

**Power BI Dashboard**
1. Download and install [Power BI Desktop](https://powerbi.microsoft.com/desktop)
2. Open `dashboard/AdventureWorks_Dashboard.pbix`
3. Update the data source path to point to your local `AdventureWorks_Sales_Cleaned.xlsx`
4. Refresh the data

---

## Author

**[Viet Duong]**  
Senior Data Analyst | Python • SQL • Power BI • Machine Learning  
📍 Perth, Western Australia (Available remotely worldwide)

[LinkedIn](#) • [Portfolio Website](#) • [GitHub](https://github.com/020)

---
