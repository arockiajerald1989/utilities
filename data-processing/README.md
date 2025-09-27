# Data Processing Utilities

Professional-grade Python utilities for financial data analysis and log processing.

## Features

### 📈 Stock Analysis (`multibagger_stocks.py`)
- **Comprehensive Financial Analysis**: 20+ financial metrics including EGR, ROE, PE, technical indicators
- **Technical Indicators**: SMA, RSI, MACD integration
- **Concurrent Processing**: Multi-threaded data fetching with timeout handling
- **Caching System**: Intelligent data caching to reduce API calls
- **Backtesting**: Historical performance validation
- **Visualization**: Automated chart generation and CSV export
- **Safe Scoring**: Secure calculation method without eval()

### 📊 Log Processing (`multiline_log_processor.py`)
- **Multiline JSON Support**: Handles complex log formats
- **Timestamp Filtering**: Extract data between specific time ranges
- **Robust Error Handling**: Comprehensive exception management
- **Memory Efficient**: Streaming file processing
- **UTF-8 Support**: Proper encoding handling

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

All settings are centralized in `config.py`:

```python
# Modify these values as needed
DEFAULT_SYMBOL_LIMIT = 30
BATCH_SIZE = 10
TIMEOUT_SECONDS = 180
```

## Usage

### Stock Analysis
```python
from multibagger_stocks import *

# Run full analysis
python multibagger_stocks.py
```

### Log Processing
```python
from multiline_log_processor import extract_last_dict_between_timestamps

result = extract_last_dict_between_timestamps(
    file_path="log_file.txt",
    start_timestamp="2025-01-01 11:00:00",
    end_timestamp="2025-01-01 12:00:00"
)
```

## Output Files

### Stock Analysis Generates:
- `top_20_enhanced_multibagger_stocks.csv` - Top stock rankings
- `top_20_enhanced_multibagger_stocks.png` - Visualization chart
- `stock_cache/` - Cached financial data

## Security Features

- ✅ **No eval() usage** - Safe calculation methods
- ✅ **Input validation** - Timestamp format checking
- ✅ **Error boundaries** - Comprehensive exception handling
- ✅ **Timeout protection** - Prevents hanging requests

## Technical Specifications

### Financial Metrics Analyzed:
- **Growth**: EGR (Earnings Growth Rate), SGR (Sales Growth Rate)
- **Profitability**: ROE (Return on Equity), ROIC (Return on Invested Capital)
- **Valuation**: PE (Price to Earnings), PEG (Price Earnings to Growth)
- **Technical**: SMA, RSI, MACD indicators
- **Risk**: Debt ratios, current ratios

### Performance:
- **Concurrent processing**: 10 stocks per batch
- **Timeout handling**: 180-second limits
- **Caching**: JSON-based data persistence
- **Memory efficient**: Streaming log processing

## Logging

All operations are logged with appropriate levels:
```
INFO: General operation status
WARNING: Non-critical issues (timeouts)
ERROR: Processing failures
```

## Requirements

- Python 3.8+
- Internet connection (for financial data)
- ~50MB storage (for caching)

## Professional Features

- 🔧 **Configurable**: Centralized configuration management
- 📝 **Well-documented**: Comprehensive docstrings and comments
- 🛡️ **Secure**: No dangerous eval() usage
- 🚀 **Performance**: Concurrent processing with caching
- 📊 **Production-ready**: Proper logging and error handling
- 🧪 **Testable**: Modular design for easy testing

---

*Last Updated: September 2025*