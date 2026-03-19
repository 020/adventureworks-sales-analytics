# AdventureWorks Sales Data Cleaning

## Overview
This script performs data quality assessment and cleaning across all seven sheets of the AdventureWorks Sales dataset in preparation for loading into Power BI for sales performance analysis.

The dataset covers sales transactions from 1 July 2017 to 30 June 2021 across two channels — Reseller and Internet — spanning North America, Europe, and the Pacific region.

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
| Date columns stored as integers | OrderDateKey, DueDateKey, ShipDateKey stored as `YYYYMMDD` format | Converted to proper date columns |
| ShipDate nulls | 2,113 null values in ShipDateKey | Retained — represent valid unshipped orders |
| Channel mixing | CustomerKey = -1 for Reseller sales, ResellerKey = -1 for Internet sales | Added IsSale_Reseller and IsSale_Internet flag columns for filtering |
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
| Datetime instead of date | Date column included time component 00:00:00 AM | Stripped time component — critical for DAX time intelligence measures in Power BI |
| Nulls | None found | No action required |
| Duplicates | None found | No action required |

### Sales Order_data and Sales Territory_data
No issues found. Both sheets were clean with no nulls, duplicates, or invalid values.

---

## Key Design Decisions

**Why keep -1 surrogate keys in Sales_data instead of removing them?**  
The -1 rows in Sales_data represent real transactions — they just don't have a linked customer or reseller depending on the channel. Removing them would understate total revenue. Instead, flag columns were added so Power BI can filter them contextually depending on the analysis being performed.

**Why fill null Color with Unknown instead of dropping rows?**  
Dropping 56 product rows would remove valid sales transactions linked to those products. Filling with Unknown preserves the data and displays cleanly in Power BI visuals without creating blank or error states.

**Why strip the time component from dates?**  
Power BI DAX time intelligence functions such as SAMEPERIODLASTYEAR and DATEADD require clean date values. Date columns stored as datetime caused comparison failures in measures, particularly for New Customers and Customer Retention Rate calculations.

**Why add IsSale_Reseller and IsSale_Internet flags?**  
AdventureWorks mixes Reseller and Internet transactions in a single Sales table. The flags allow Power BI visuals to filter to the correct channel without complex DAX. For example the geographic map uses Reseller geography while the customer analysis uses Internet customer geography — these are two completely different location contexts.

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

---
