import yfinance as yf
import requests
import pandas as pd
#Creator Sahil Lala
# Function to get Nifty index data using yfinance at 5-minute intervals
def get_nifty_index_data_5min():
    # Ticker symbol for Nifty 50
    nifty_ticker = "^NSEI"
    
    # Fetch historical data with 5-minute intervals for the past 5 days
    nifty_data = yf.download(tickers=nifty_ticker, period='5d', interval='5m')
    
    return nifty_data

# Function to scrape Nifty options data from NSE India (snapshot data)
def get_nifty_options_data(expiry_date):
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY',
        'DNT': '1',  # Do Not Track Request Header
        'Host': 'www.nseindia.com'
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    
    # Raise an error if the request failed
    response.raise_for_status()
    
    # Parse JSON data
    data = response.json()
    
    # Extract calls and puts data for the specified expiry date
    calls_data = []
    puts_data = []
    for record in data['records']['data']:
        if record['expiryDate'] == expiry_date:
            if 'CE' in record:
                calls_data.append(record['CE'])
            if 'PE' in record:
                puts_data.append(record['PE'])
    
    # Convert to DataFrame
    calls_df = pd.DataFrame(calls_data)
    puts_df = pd.DataFrame(puts_data)
    
    return calls_df, puts_df

# Fetch 5-minute interval data for the Nifty index
nifty_index_data_5min = get_nifty_index_data_5min()

# Specify the expiry date you want to fetch options data for
expiry_date = "18-Jul-2024"

# Fetch options data for the specified expiry date
calls_df, puts_df = get_nifty_options_data(expiry_date)

# Display the data
print("Nifty Index Data (5-minute intervals):")
print(nifty_index_data_5min.head())

print(f"\nNifty Options Data - Calls (Expiry: {expiry_date}):")
# print(calls_df.head())
print(calls_df)
print(f"\nNifty Options Data - Puts (Expiry: {expiry_date}):")
print(puts_df.head())
