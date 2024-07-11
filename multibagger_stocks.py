import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import os
import json

# Directory to cache stock data
CACHE_DIR = 'stock_cache'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Function to fetch and process financial data for a given stock symbol
def fetch_stock_data(symbol):
    cache_file = os.path.join(CACHE_DIR, f'{symbol}.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        data = {
            "Symbol": symbol,
            "EGR": info.get('earningsGrowth', np.nan),
            "ROE": info.get('returnOnEquity', np.nan),
            "PE": info.get('trailingPE', np.nan),
            "DE": info.get('debtToEquity', np.nan),
            "PEG": info.get('pegRatio', np.nan),
            "EV_EBITDA": info.get('enterpriseToEbitda', np.nan),
            "FCF_Yield": info.get('freeCashflow', np.nan) / info.get('marketCap', np.nan) if info.get('marketCap', np.nan) else np.nan,
            "ROIC": info.get('returnOnCapitalEmployed', np.nan),
            "DY": info.get('dividendYield', np.nan),
            "PB": info.get('priceToBook', np.nan),
            "OM": info.get('operatingMargins', np.nan),
            "CR": info.get('currentRatio', np.nan),
            "DER": info.get('debtToEquity', np.nan),  # Already included as DE
            "SGR": info.get('revenueGrowth', np.nan),  # Sales Growth
            "PGR": info.get('grossProfits', np.nan) / info.get('revenue', np.nan) if info.get('revenue', np.nan) else np.nan,
            "Close": ticker.history(period='1d')['Close'].iloc[0] if not ticker.history(period='1d').empty else np.nan
        }

        with open(cache_file, 'w') as f:
            json.dump(data, f)

        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to get a list of NASDAQ stock symbols
def get_nasdaq_symbols(limit=100):
    nasdaq_symbols = ['ADBE', 'AMD', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ARM', 'ASML', 'TEAM', 'ADSK', 'AVGO', 'CDNS', 'CDW', 'CSCO', 'CTSH', 'CRWD', 'DDOG', 'FTNT', 'GFS', 'INTC', 'INTU', 'KLAC', 'LRCX', 'MRVL', 'MCHP', 'MU', 'MSFT', 'MDB', 'NVDA', 'NXPI']
    return nasdaq_symbols[:limit]

# Function to process stocks in batches
def process_stocks_in_batches(symbols, batch_size=10, timeout=180):
    all_results = []
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_symbol = {executor.submit(fetch_stock_data, symbol): symbol for symbol in batch}
            for future in as_completed(future_to_symbol, timeout=timeout):
                symbol = future_to_symbol[future]
                try:
                    result = future.result(timeout=timeout)
                    if result:
                        all_results.append(result)
                except TimeoutError:
                    print(f"Fetching data for {symbol} timed out.")
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
    return all_results

# Function to fetch technical indicators for a given stock symbol
def fetch_technical_indicators(symbol):
    try:
        df = yf.download(symbol, period='1y')
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        df['RSI'] = 100 - (100 / (1 + df['Close'].diff().rolling(window=14).apply(lambda x: np.sum(x[x > 0]) / np.sum(-x[x < 0]))))
        df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        indicators = {
            "SMA_50": df['SMA_50'].iloc[-1],
            "SMA_200": df['SMA_200'].iloc[-1],
            "RSI": df['RSI'].iloc[-1],
            "MACD": df['MACD'].iloc[-1],
            "Signal": df['Signal'].iloc[-1]
        }
        return indicators
    except Exception as e:
        print(f"Error fetching technical indicators for {symbol}: {e}")
        return None

# Fetching the list of NASDAQ stock symbols (limit to 100 for now)
nasdaq_symbols = get_nasdaq_symbols(30)

# Logging the fetched symbols
print(f"Fetched NASDAQ symbols: {nasdaq_symbols}")

# Process stocks in batches
results = process_stocks_in_batches(nasdaq_symbols, batch_size=10, timeout=180)

# Converting results to DataFrame
df = pd.DataFrame(results).set_index('Symbol')

# Fetch technical indicators for each stock and merge with financial data
tech_indicators = []
for symbol in df.index:
    tech_data = fetch_technical_indicators(symbol)
    if tech_data:
        tech_data['Symbol'] = symbol
        tech_indicators.append(tech_data)

tech_df = pd.DataFrame(tech_indicators).set_index('Symbol')

# Merge the financial data and technical indicators
df = df.merge(tech_df, left_index=True, right_index=True, how='left')

# Logging the fetched data
print("Fetched stock data with technical indicators:")
print(df.head())

# List of essential metrics to check for presence
essential_metrics = ['EGR', 'ROE', 'PE', 'DE', 'PEG', 'EV_EBITDA', 'FCF_Yield', 'ROIC', 'DY', 'PB', 'OM', 'CR', 'DER', 'SGR', 'PGR', 'Close', 'SMA_50', 'SMA_200', 'RSI', 'MACD', 'Signal']

# Check which essential metrics are present
present_metrics = [metric for metric in essential_metrics if metric in df.columns]

# Cleaning data (removing rows where all present essential columns are NaN)
df = df.dropna(subset=present_metrics, how='all')

# Substitute NaN values with appropriate defaults
df.fillna({
    'ROIC': 0.01,
    'DY': 0,
    'PB': df['PB'].median() if 'PB' in df.columns else 1,  # Substitute NaN PB with median PB or 1 if not present
    'OM': df['OM'].median() if 'OM' in df.columns else 0.1,  # Substitute NaN OM with median OM or 0.1 if not present
    'CR': df['CR'].median() if 'CR' in df.columns else 1,  # Substitute NaN CR with median CR or 1 if not present
    'DER': df['DER'].median() if 'DER' in df.columns else 1,  # Substitute NaN DER with median DER or 1 if not present
    'SGR': df['SGR'].median() if 'SGR' in df.columns else 0.1,  # Substitute NaN SGR with median SGR or 0.1 if not present
    'PGR': df['PGR'].median() if 'PGR' in df.columns else 0.1,  # Substitute NaN PGR with median PGR or 0.1 if not present
    'SMA_50': df['SMA_50'].median() if 'SMA_50' in df.columns else df['Close'].median(),
    'SMA_200': df['SMA_200'].median() if 'SMA_200' in df.columns else df['Close'].median(),
    'RSI': df['RSI'].median() if 'RSI' in df.columns else 50,
    'MACD': df['MACD'].median() if 'MACD' in df.columns else 0,
    'Signal': df['Signal'].median() if 'Signal' in df.columns else 0
}, inplace=True)

# Normalize values to ensure they're within a reasonable range
if 'EGR' in df.columns:
    df['EGR'] = df['EGR'] / 100
if 'ROE' in df.columns:
    df['ROE'] = df['ROE'] / 100
if 'PE' in df.columns:
    df['PE'] = 1 / df['PE']
if 'DE' in df.columns:
    df['DE'] = 1 / df['DE']
if 'PEG' in df.columns:
    df['PEG'] = 1 / df['PEG']
if 'FCF_Yield' in df.columns:
    df['FCF_Yield'] = df['FCF_Yield'] / 100
if 'DY' in df.columns:
    df['DY'] = df['DY'] / 100
if 'PB' in df.columns:
    df['PB'] = 1 / df['PB']
if 'OM' in df.columns:
    df['OM'] = df['OM'] / 100
if 'CR' in df.columns:
    df['CR'] = df['CR'] / 100
if 'DER' in df.columns:
    df['DER'] = 1 / df['DER']
if 'SMA_50' in df.columns:
    df['SMA_50'] = df['SMA_50'] / df['Close']
if 'SMA_200' in df.columns:
    df['SMA_200'] = df['SMA_200'] / df['Close']
if 'RSI' in df.columns:
    df['RSI'] = df['RSI'] / 100
if 'MACD' in df.columns:
    df['MACD'] = df['MACD'] / df['Close']
if 'Signal' in df.columns:
    df['Signal'] = df['Signal'] / df['Close']

# Logging the cleaned and normalized data
print("Cleaned and normalized stock data:")
print(df.head())

# Checking if the DataFrame is empty after cleaning
if df.empty:
    print("No valid stock data available after cleaning.")
else:
    # Calculating Enhanced Multibagger Potential Score
    score_components = [
        '((df["EGR"] + df["ROE"] + df["PE"] + df["DE"] + df["PEG"] + df["EV_EBITDA"] + df["FCF_Yield"] + df["ROIC"])'
    ]
    if 'SGR' in df.columns and not df['SGR'].isna().all():
        score_components[0] += ' + df["SGR"]'
    if 'PGR' in df.columns and not df['PGR'].isna().all():
        score_components[0] += ' + df["PGR"]'
    score_components[0] += ')'
    if 'DY' in df.columns:
        score_components.append('(1 + df["DY"])')
    if 'PB' in df.columns:
        score_components.append('df["PB"]')
    if 'OM' in df.columns:
        score_components.append('df["OM"]')
    if 'CR' in df.columns:
        score_components.append('df["CR"]')
    if 'DER' in df.columns:
        score_components.append('df["DER"]')
    if 'SMA_50' in df.columns:
        score_components.append('df["SMA_50"]')
    if 'SMA_200' in df.columns:
        score_components.append('df["SMA_200"]')
    if 'RSI' in df.columns:
        score_components.append('df["RSI"]')
    if 'MACD' in df.columns:
        score_components.append('df["MACD"]')
    if 'Signal' in df.columns:
        score_components.append('df["Signal"]')

    score_formula = ' * '.join(score_components)
    df['Enhanced_Score'] = eval(score_formula)

    # Scaling Enhanced_Score to avoid extremely small values
    df['Enhanced_Score'] = df['Enhanced_Score'] * 1e12  # Scale up by 1 trillion for better readability

    # Sorting stocks by the Enhanced Multibagger Potential Score in descending order
    df_sorted = df.sort_values(by='Enhanced_Score', ascending=False)

    # Display the top 20 stocks
    top_20_stocks = df_sorted.head(20)
    print(top_20_stocks)

    # Save the result to a CSV file for further analysis if needed
    top_20_stocks.to_csv('top_20_enhanced_multibagger_stocks.csv', index=True)

    # Plotting the top 20 stocks
    plt.figure(figsize=(14, 8))
    plt.bar(top_20_stocks.index, top_20_stocks['Enhanced_Score'], color='skyblue')
    plt.xlabel('Stock Symbol')
    plt.ylabel('Enhanced Multibagger Potential Score')
    plt.title('Top 20 NASDAQ Stocks by Enhanced Multibagger Potential Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_20_enhanced_multibagger_stocks.png')
    plt.show()

    # Placeholder for qualitative analysis (manual steps required)
    def qualitative_analysis(stock):
        try:
            # Example: Print basic company info (customize as needed)
            ticker = yf.Ticker(stock)
            info = ticker.info
            print(f"Qualitative analysis for {stock}:")
            print(f"Company: {info.get('longName')}")
            print(f"Industry: {info.get('industry')}")
            print(f"Description: {info.get('longBusinessSummary')}\n")
        except Exception as e:
            print(f"Error fetching qualitative analysis for {stock}: {e}")

    # Example of how to incorporate qualitative analysis
    for stock in top_20_stocks.index:
        qualitative_analysis(stock)

    # Backtesting
    historical_data = {}
    for symbol in top_20_stocks.index:
        historical_data[symbol] = yf.download(symbol, start='2020-01-01', end='2023-01-01')['Close']

    historical_df = pd.DataFrame(historical_data)
    historical_df.ffill(inplace=True)
    historical_df.bfill(inplace=True)

    initial_investment = 100000
    investment_per_stock = initial_investment / len(top_20_stocks)

    portfolio = (historical_df / historical_df.iloc[0]) * investment_per_stock
    portfolio['Total'] = portfolio.sum(axis=1)

    final_investment_value = portfolio['Total'].iloc[-1]
    print(f"Final investment value after backtesting: ${final_investment_value:.2f}")

    # Printing the value of investment in each stock
    investment_values = portfolio.iloc[-1][:-1]  # Exclude the 'Total' column
    for symbol, value in investment_values.items():
        print(f"Final value of investment in {symbol}: ${value:.2f}")
