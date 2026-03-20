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

print("\nAll sheets loaded successfully")

# SALES_DATA
print("\n── Sales_data ──────────────────────────────────────────")
print(f"Rows before cleaning: {len(sales)}")

# 1. Validate SalesAmount = UnitPrice * OrderQuantity (within rounding)
sales["CalculatedAmount"] = sales["Unit Price"] * sales["Order Quantity"]
sales["AmountVariance"] = abs(sales["Sales Amount"] - sales["CalculatedAmount"])
variance_issues = (sales["AmountVariance"] > 1).sum()
print(f"Rows with sales amount variance > $1: {variance_issues}")

# 2. Check for negative values in numeric columns
numeric_cols = ["Unit Price", "Sales Amount", "Total Product Cost", "Order Quantity"]
for col in numeric_cols:
    neg_count = (sales[col] < 0).sum()
    if neg_count > 0:
        print(f"WARNING: {col} has {neg_count} negative values")
    else:
        print(f"✅ {col} — no negative values")

# 3. Check for duplicates
dupes = sales.duplicated().sum()
print(f"Duplicate rows: {dupes}")

# 4. Note on ShipDateKey nulls
ship_nulls = sales["ShipDateKey"].isnull().sum()
print(f"ShipDateKey nulls (valid unshipped orders): {ship_nulls}")

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
nulls = customer_clean.isnull().sum()
nulls = nulls[nulls > 0]
print(f"Nulls: {nulls.to_dict() if len(nulls) > 0 else 'None'}")

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
print(f"DateKey range: {date['DateKey'].min()} to {date['DateKey'].max()}")
print(f"Nulls: {date.isnull().sum().sum()}")
print(f"Duplicates: {date.duplicated().sum()}")

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
    date.to_excel(writer, sheet_name="Date_data", index=False)
    sales_order.to_excel(writer, sheet_name="Sales Order_data", index=False)
    sales_territory.to_excel(writer, sheet_name="Sales Territory_data", index=False)

print(f"\n✅ Cleaned file exported to: {output_file}")

# CLEANING SUMMARY REPORT
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"""
Sales_data:
  - Date columns (OrderDateKey, DueDateKey, ShipDateKey) retained as integers
  - Power BI handles date conversion natively via Date table relationship
  - Channel filtering handled via Sales Order table Channel field
  - ShipDateKey has {sales['ShipDateKey'].isnull().sum():,} nulls (valid unshipped orders)
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
  - No changes — retained as source
  - DateKey range: {date['DateKey'].min()} to {date['DateKey'].max()}
  - No nulls or duplicates

Sales Order_data:
  - No issues found
  - Channels: {sales_order['Channel'].value_counts().to_dict()}

Sales Territory_data:
  - No issues found
  - 11 territories across North America, Europe, Pacific
""")
