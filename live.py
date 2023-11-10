from alpaca_trade_api.stream import Stream
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart
import alpaca_trade_api as tradeapi

# Set your API key and secret
APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  # URL for paper trading
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)


# Define a function to handle incoming messages for real-time data
async def handle_realtime_data(data):
    chart.update_from_tick(data)
    print(f"Real-time data: {data}")

# Initialize Stream

if __name__ == '__main__':
    # Define the ticker, timeframe, start, and end dates
    ticker = "AAPL"
    timeframe = "1Min"  # Possible values: '1Min', '5Min', '15Min', '1H', '1D'
    start_date = "2023-11-01"
    end_date = "2023-11-09"

    # Fetch historical data
    bars = api.get_bars(ticker, timeframe, start=start_date, end=end_date).df

    bars.reset_index(inplace=True)
    bars['timestamp'] = pd.to_datetime(bars['timestamp'], unit='s').dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    bars.rename(columns={
        'timestamp': 'time',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume'
    }, inplace=True)
    bars.columns = bars.columns.str.lower()

    chart = Chart()
    chart.set(bars)
    chart.watermark(ticker)
    stream = Stream(APCA_API_KEY_ID,
                APCA_API_SECRET_KEY,
                base_url=APCA_API_BASE_URL,
                data_feed='iex')  # use 'sip' for paid subscription

    stream.subscribe_bars(handle_realtime_data, 'AAPL')

    # Start streaming in an asynchronous context
    stream.run()
    chart.show(block=True)

    