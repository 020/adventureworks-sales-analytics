# AdventureWorks Sales Data Cleaning

## Overview
This script performs data quality assessment and cleaning across all seven sheets of the AdventureWorks Sales dataset in preparation for loading into Power BI for sales performance analysis.

The dataset covers sales transactions from 1 July 2017 to 30 June 2021 across two channels (Reseller and Internet) spanning North America, Europe, and the Pacific region.

---

## Dataset
**Source:** Microsoft AdventureWorks Sample Dataset  
**File:** `AdventureWorks_Sales.xlsx`  
**License:** Microsoft Sample Data — provided for learning and demonstration purposes  
**Sheets:** 7 (Sales, Customer, Reseller, Product, Date, Sales Order, Sales Territory)  
**Total transactions:** 121,253

---

## Data Quality Issues Found

### Sales_data
| Issue | Finding | Decision |
|---|---|---|
| Date columns stored as integers | OrderDateKey, DueDateKey, ShipDateKey stored as `YYYYMMDD` format | Retained as integers — Power BI handles date conversion natively via Date table relationship |
| ShipDateKey nulls | 2,113 null values in ShipDateKey | Retained — represent valid unshipped orders |
| Channel identification | CustomerKey = -1 for Reseller sales, ResellerKey = -1 for Internet sales | No flags added — channel filtering handled via Sales Order table Channel field |
| Sales amount variance | 3,247 rows where SalesAmount differs slightly from UnitPrice × OrderQuantity | Noted as a data quirk — likely due to discounts or rounding |
| Negative values | None found across Unit Price, Sales Amount, Total Product Cost, Order Quantity | No action required |
| Duplicates | None found | No action required |

### Customer_data
| Issue | Finding | Decision |
|---|---|---|
| Surrogate key placeholder | CustomerKey = -1 representing Not Applicable | Removed — 1 row, 18,484 valid customers retained |
| Nulls | None found | No action required |
| Duplicates | None found | No action required |

### Reseller_data
| Issue | Finding | Decision |
|---|---|---|
| Surrogate key placeholder | ResellerKey = -1 representing Not Applicable | Removed — 1 row, 701 valid resellers retained |
| Nulls | None found | No action required |
| Duplicates | None found | No action required |

### Product_data
| Issue | Finding | Decision |
|---|---|---|
| Null Color values | 56 products with no color assigned | Filled with "Unknown" to maintain row count and display cleanly in visuals |
| Negative prices | None found | No action required |
| Duplicates | None found | No action required |

### Date_data
| Issue | Finding | Decision |
|---|---|---|
| No issues found | DateKey range 20170701 to 20210630, no nulls or duplicates | Retained as source — no changes made |

### Sales Order_data and Sales Territory_data
No issues found. Both sheets were clean with no nulls, duplicates, or invalid values.

---

## Key Design Decisions

**Why retain date columns as integers in Sales_data?**  
OrderDateKey, DueDateKey, and ShipDateKey are stored as integers in the YYYYMMDD format. Power BI handles date conversion natively through the relationship between Sales_data and Date_data via the DateKey column. Converting dates in Python would duplicate work that Power BI already does and adds unnecessary complexity to the pipeline.

**Why not add channel flag columns to Sales_data?**  
The Sales Order table already contains a Channel field with Reseller and Internet values. Using the existing source column is cleaner than adding derived flag columns — it avoids redundancy, reduces the chance of inconsistency, and keeps the Sales_data table focused on transaction data only.

**Why keep -1 surrogate keys in Sales_data?**  
The -1 rows in Sales_data represent real revenue-generating transactions that simply don't have a linked customer or reseller depending on the channel. Removing them would understate total revenue. Channel filtering is handled downstream via the Sales Order table Channel field.

**Why remove -1 surrogate keys from Customer_data and Reseller_data?**  
Unlike Sales_data, the -1 rows in these tables serve no analytical purpose — they are placeholder rows with no real customer or reseller information. Leaving them in causes Not Applicable to appear in customer and reseller visuals in Power BI which is misleading and unprofessional in a dashboard context.

**Why fill null Color with Unknown instead of dropping rows?**  
Dropping 56 product rows would remove valid sales transactions linked to those products. Filling with Unknown preserves the data and displays cleanly in Power BI visuals without creating blank or error states.

---

## Output
**File:** `AdventureWorks_Sales_Cleaned.xlsx`  
All seven sheets are exported to a single cleaned Excel file ready for direct import into Power BI.

---

## Tools Used
- Python 3.12
- pandas
- openpyxl
- AI assisted development used in line with modern data engineering practices

