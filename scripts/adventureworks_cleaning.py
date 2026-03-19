import pandas as pd
import numpy as np

print("AdventureWorks Data Cleaning Script")

# Load all sheets
file_path = "AdventureWorks_Sales.xlsx"

sales_order = pd.read_excel(file_path, sheet_name="Sales Order_data")
sales_territory = pd.read_excel(file_path, sheet_name="Sales Territory_data")
sales = pd.read_excel(file_path, sheet_name="Sales_data")
reseller = pd.read_excel(file_path, sheet_name="Reseller_data")
date = pd.read_excel(file_path, sheet_name="Date_data")
product = pd.read_excel(file_path, sheet_name="Product_data")
customer = pd.read_excel(file_path, sheet_name="Customer_data")

print("\n All sheets loaded successfully")

# SALES_DATA
print("\n── Sales_data ──────────────────────────────────────────")
print(f"Rows before cleaning: {len(sales)}")

# 1. Convert OrderDateKey to proper date
sales["OrderDate"] = pd.to_datetime(
    sales["OrderDateKey"].astype(str), format="%Y%m%d"
).dt.date

# 2. Convert DueDateKey to proper date
sales["DueDate"] = pd.to_datetime(
    sales["DueDateKey"].astype(str), format="%Y%m%d"
).dt.date

# 3. Convert ShipDateKey — has 2,113 nulls so handle missing values
sales["ShipDate"] = pd.to_datetime(
    sales["ShipDateKey"].dropna().astype(int).astype(str), format="%Y%m%d"
).reindex(sales.index).dt.date

print(f"ShipDate nulls (unshipped orders): {sales['ShipDate'].isnull().sum()}")

# 4. Flag channel split — CustomerKey=-1 means Reseller, ResellerKey=-1 means Internet
# Keep all rows but add a clean channel flag for filtering in Power BI
sales["IsSale_Reseller"] = sales["ResellerKey"] != -1
sales["IsSale_Internet"] = sales["CustomerKey"] != -1

print(f"Reseller transactions: {sales['IsSale_Reseller'].sum()}")
print(f"Internet transactions: {sales['IsSale_Internet'].sum()}")

# 5. Validate SalesAmount = UnitPrice * OrderQuantity (within rounding)
sales["CalculatedAmount"] = sales["Unit Price"] * sales["Order Quantity"]
sales["AmountVariance"] = abs(sales["Sales Amount"] - sales["CalculatedAmount"])
variance_issues = (sales["AmountVariance"] > 1).sum()
print(f"Rows with sales amount variance > $1: {variance_issues}")

# 6. Check for negative values in numeric columns
numeric_cols = ["Unit Price", "Sales Amount", "Total Product Cost", "Order Quantity"]
for col in numeric_cols:
    neg_count = (sales[col] < 0).sum()
    if neg_count > 0:
        print(f"WARNING: {col} has {neg_count} negative values")
    else:
        print(f" {col} — no negative values")

# 7. Check for duplicates
dupes = sales.duplicated().sum()
print(f"Duplicate rows: {dupes}")

print(f"Rows after cleaning: {len(sales)}")

# CUSTOMER_DATA
print("\n── Customer_data ───────────────────────────────────────")
print(f"Rows before cleaning: {len(customer)}")

# 1. Remove -1 surrogate key (Not Applicable placeholder)
not_applicable_customers = customer[customer["CustomerKey"] == -1]
print(f"Not Applicable customer rows removed: {len(not_applicable_customers)}")
customer_clean = customer[customer["CustomerKey"] != -1].copy()

# 2. Check for duplicates
dupes = customer_clean.duplicated().sum()
print(f"Duplicate rows: {dupes}")

# 3. Check for nulls
print(f"Nulls:\n{customer_clean.isnull().sum()[customer_clean.isnull().sum() > 0]}")

print(f"Rows after cleaning: {len(customer_clean)}")

# RESELLER_DATA
print("\n── Reseller_data ───────────────────────────────────────")
print(f"Rows before cleaning: {len(reseller)}")

# 1. Remove -1 surrogate key (Not Applicable placeholder)
not_applicable_resellers = reseller[reseller["ResellerKey"] == -1]
print(f"Not Applicable reseller rows removed: {len(not_applicable_resellers)}")
reseller_clean = reseller[reseller["ResellerKey"] != -1].copy()

# 2. Check for duplicates
dupes = reseller_clean.duplicated().sum()
print(f"Duplicate rows: {dupes}")

print(f"Rows after cleaning: {len(reseller_clean)}")

# PRODUCT_DATA
print("\n── Product_data ────────────────────────────────────────")
print(f"Rows before cleaning: {len(product)}")

# 1. Color has 56 nulls — fill with Unknown for reporting
print(f"Color nulls before: {product['Color'].isnull().sum()}")
product_clean = product.copy()
product_clean["Color"] = product_clean["Color"].fillna("Unknown")
print(f"Color nulls after: {product_clean['Color'].isnull().sum()}")

# 2. Check for duplicates
dupes = product_clean.duplicated().sum()
print(f"Duplicate rows: {dupes}")

# 3. Check for negative prices
neg_price = (product_clean["List Price"] < 0).sum()
neg_cost = (product_clean["Standard Cost"] < 0).sum()
print(f"Negative List Price rows: {neg_price}")
print(f"Negative Standard Cost rows: {neg_cost}")

print(f"Rows after cleaning: {len(product_clean)}")

# DATE_DATA
print("\n── Date_data ───────────────────────────────────────────")
print(f"Rows: {len(date)}")

# 1. Strip time component from Date column
date_clean = date.copy()
date_clean["Date"] = pd.to_datetime(date_clean["Date"]).dt.date
print(f"Date range: {date_clean['Date'].min()} to {date_clean['Date'].max()}")
print(f"Nulls: {date_clean.isnull().sum().sum()}")
print(f"Duplicates: {date_clean.duplicated().sum()}")

# SALES_ORDER_DATA
print("\n── Sales Order_data ────────────────────────────────────")
print(f"Rows: {len(sales_order)}")
print(f"Channels: {sales_order['Channel'].value_counts().to_dict()}")
print(f"Nulls: {sales_order.isnull().sum().sum()}")
print(f"Duplicates: {sales_order.duplicated().sum()}")

# SALES_TERRITORY_DATA
print("\n── Sales Territory_data ────────────────────────────────")
print(f"Rows: {len(sales_territory)}")
print(f"Nulls: {sales_territory.isnull().sum().sum()}")
print(f"Duplicates: {sales_territory.duplicated().sum()}")
print(f"Regions:\n{sales_territory[['Region', 'Country', 'Group']]}")

# EXPORT CLEANED SHEETS BACK TO EXCEL
print("\n── Exporting cleaned data ──────────────────────────────")

output_file = "AdventureWorks_Sales_Cleaned.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    sales.to_excel(writer, sheet_name="Sales_data", index=False)
    customer_clean.to_excel(writer, sheet_name="Customer_data", index=False)
    reseller_clean.to_excel(writer, sheet_name="Reseller_data", index=False)
    product_clean.to_excel(writer, sheet_name="Product_data", index=False)
    date_clean.to_excel(writer, sheet_name="Date_data", index=False)
    sales_order.to_excel(writer, sheet_name="Sales Order_data", index=False)
    sales_territory.to_excel(writer, sheet_name="Sales Territory_data", index=False)

print(f"\n Cleaned file exported to: {output_file}")

# CLEANING SUMMARY REPORT
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"""
Sales_data:
  - Converted OrderDateKey, DueDateKey, ShipDateKey to proper dates
  - Flagged {sales['IsSale_Reseller'].sum():,} Reseller transactions
  - Flagged {sales['IsSale_Internet'].sum():,} Internet transactions
  - ShipDate has {sales['ShipDate'].isnull().sum():,} nulls (valid unshipped orders)
  - No duplicates found
  - No negative values in key numeric columns

Customer_data:
  - Removed 1 Not Applicable surrogate key row (-1)
  - {len(customer_clean):,} valid customers retained
  - No duplicates found

Reseller_data:
  - Removed 1 Not Applicable surrogate key row (-1)
  - {len(reseller_clean):,} valid resellers retained
  - No duplicates found

Product_data:
  - Filled 56 null Color values with 'Unknown'
  - No duplicates found
  - No negative prices found

Date_data:
  - Stripped time component from Date column
  - Date range: {date_clean['Date'].min()} to {date_clean['Date'].max()}
  - No nulls or duplicates

Sales Order_data:
  - No issues found
  - Channels: {sales_order['Channel'].value_counts().to_dict()}

Sales Territory_data:
  - No issues found
  - 11 territories across North America, Europe, Pacific
""")
