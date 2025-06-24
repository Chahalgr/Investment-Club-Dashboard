import pandas as pd

# Load the Excel file
input_file = '250310 Corporate-Positions-2025-03-10-214631.xlsx'
output_file = 'cleaned_corporate_positions.csv'

# Read the Excel file and select the first sheet
excel_file = pd.ExcelFile(input_file)
df_raw = pd.read_excel(excel_file, sheet_name=0)

# Use the second row as column headers
df_raw.columns = df_raw.iloc[1]
df_cleaned = df_raw.iloc[2:].reset_index(drop=True)

# Drop empty rows
df_cleaned.dropna(how='all', inplace=True)

# Optional: Convert numeric columns (if needed)
numeric_cols = ['Qty', 'Price', 'Price Chng $', 'Price Chng %',
                'Mkt Val', 'Day Chng $', 'Day Chng %',
                'Cost Basis', 'Gain $', 'Gain %', '% of Acct']
for col in numeric_cols:
    if col in df_cleaned.columns:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

# Save to CSV
df_cleaned.to_csv(output_file, index=False)

print(f"Cleaned data saved to: {output_file}")
