import yfinance as yf
import random

def get_stock_std(symbol):

  # Download historical data for the past year
  data = yf.download(symbol, period="1y")

  # Check if data is downloaded successfully
  if data.empty:
    return None

  # Calculate standard deviation of closing prices (using Bessel's correction)
  std = data['Close'].std(ddof=1)
  return std

def get_stock_correlation(symbol):
  # Download historical data for the past year
  data = yf.download([symbol, "^NSEI"], period="1y")

  # Check if data is downloaded successfully
  if data.empty:
    return None

  # Calculate correlation between closing prices of the stock and NIFTY
  correlation = data['Close'].corr(method='pearson')
  return correlation[symbol]

# Example usage
stock_symbol = "RELIANCE.NS"  # Replace with your desired symbol
std = get_stock_std(stock_symbol)
correlation = get_stock_correlation(stock_symbol)

if std is not None:
  print(f"Standard deviation of {stock_symbol}: {std:.2f}")
if correlation is not None:
  print(f"Correlation of {stock_symbol} with NIFTY: {correlation:.2f}")
