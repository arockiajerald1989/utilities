"""
Configuration settings for data processing utilities
"""

# Stock Analysis Configuration
NASDAQ_SYMBOLS = [
    'ADBE', 'AMD', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ARM', 'ASML', 'TEAM',
    'ADSK', 'AVGO', 'CDNS', 'CDW', 'CSCO', 'CTSH', 'CRWD', 'DDOG', 'FTNT',
    'GFS', 'INTC', 'INTU', 'KLAC', 'LRCX', 'MRVL', 'MCHP', 'MU', 'MSFT',
    'MDB', 'NVDA', 'NXPI'
]

# Processing Configuration
DEFAULT_SYMBOL_LIMIT = 30
BATCH_SIZE = 10
TIMEOUT_SECONDS = 180
MAX_WORKERS = 10

# Cache Configuration
CACHE_DIR = 'stock_cache'

# Output Configuration
OUTPUT_CSV = 'top_20_enhanced_multibagger_stocks.csv'
OUTPUT_CHART = 'top_20_enhanced_multibagger_stocks.png'
TOP_STOCKS_COUNT = 20

# Financial Metrics Configuration
ESSENTIAL_METRICS = [
    'EGR', 'ROE', 'PE', 'DE', 'PEG', 'EV_EBITDA', 'FCF_Yield', 'ROIC',
    'DY', 'PB', 'OM', 'CR', 'DER', 'SGR', 'PGR', 'Close', 'SMA_50',
    'SMA_200', 'RSI', 'MACD', 'Signal'
]

# Default Values for Missing Data
DEFAULT_VALUES = {
    'ROIC': 0.01,
    'DY': 0,
    'PB': 1,
    'OM': 0.1,
    'CR': 1,
    'DER': 1,
    'SGR': 0.1,
    'PGR': 0.1,
    'RSI': 50,
    'MACD': 0,
    'Signal': 0
}

# Normalization Factors
PERCENTAGE_METRICS = ['EGR', 'ROE', 'FCF_Yield', 'DY', 'OM', 'CR']
INVERSE_METRICS = ['PE', 'DE', 'PEG', 'PB', 'DER']

# Backtesting Configuration
BACKTEST_START_DATE = '2020-01-01'
BACKTEST_END_DATE = '2023-01-01'
INITIAL_INVESTMENT = 100000

# Technical Indicators Configuration
SMA_SHORT_PERIOD = 50
SMA_LONG_PERIOD = 200
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Score Scaling Factor
SCORE_SCALE_FACTOR = 1e12