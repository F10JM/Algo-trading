import pandas as pd
from lightweight_charts import Chart
from alpaca_trade_api import REST
from time import sleep
import datetime

# Alpaca API credentials
APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  

# Initialize Alpaca API
api = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

# Function to fetch bar data for a symbol and timeframe
def get_bar_data(symbol, timeframe, start_date, end_date):
    bars = api.get_bars(symbol, timeframe, start=start_date, end=end_date).df.reset_index()
    bars['timestamp'] = bars['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    bars.rename(columns={
        'timestamp': 'time',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume'
    }, inplace=True)
    bars.columns = bars.columns.str.lower()
    return bars
if __name__ == '__main__':
    # Define the ticker and timeframe for historical data
    ticker = "AAPL"
    timeframe = "5Min"
    start_date = "2023-11-01"
    end_date = "2023-11-09"

    # Fetch historical data
    historical_data = get_bar_data(ticker, timeframe, start_date, end_date)

    # Create and display the chart with historical data
    chart = Chart()
    chart.set(historical_data)
    chart.watermark(ticker)
    chart.show()

    # Simulate real-time updates
    # In practice, you would fetch the latest data from a real-time API endpoint
    while True:
        # Fetch the latest data point (simulated here by taking the last point and modifying it)
        latest_data = historical_data.iloc[-1].copy()
        latest_data['time'] = (pd.to_datetime(latest_data['time']) + pd.Timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        latest_data['close'] += 0.1  # Simulate a price change
        
        # Update the chart with the new data point
        chart.update(latest_data)
        
        # Pause for 5 minutes
        sleep(5 * 60)