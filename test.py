import yfinance as yf
import pandas as pd

# Define the stock symbol and the start date
stock_symbol = 'ZM'
start_date = '2023-01-01'

# Fetch historical data
data = yf.download(stock_symbol, start=start_date, interval='1mo')

# Calculate returns
data['Return'] = data['Adj Close'].pct_change()
output_file = 'returns1.xlsx'
data.to_excel(output_file, index=True)


# Define periods for return calculations
periods = {
    '1 Week': 5,  # 5 trading days
    '1 Month': 21,  # Approximate trading days in a month
    '3 Months': 63  # Approximate trading days in 3 months
}

# Calculate returns for each period
returns_distribution = {}
for period, days in periods.items():
    returns_distribution[period] = data['Return'].tail(days).dropna()

# Convert to DataFrame for better visualization
returns_df = pd.DataFrame(returns_distribution)
returns_df = returns_df * 100
returns_df = returns_df.applymap(lambda x: f"{x:.2f}%" if pd.notnull(x) else "NaN%")

# Display the returns distribution
#print(returns_df)
# Specify the output file name
output_file = 'returns.xlsx'

# Write the DataFrame to an Excel file
returns_df.to_excel(output_file, index=True)

print(f"Returns DataFrame saved to {output_file}")