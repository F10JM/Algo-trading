import pandas as pd
import alpaca_trade_api as tradeapi
from lightweight_charts import Chart
from time import sleep
from datetime import datetime, timedelta
from alpaca_trade_api.stream import Stream
import threading

# Alpaca API credentials
APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  # URL for paper trading


# Define a function to handle incoming messages for real-time data
def format_data_for_chart(bar):
    # Convert the timestamp to the required format
    # Assuming the timestamp is in nanoseconds, convert it to seconds first
    timestamp = pd.to_datetime(bar.timestamp, unit='ns')

    # Create a pandas Series with the required format
    formatted_data = pd.Series({
        'time': timestamp.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'open': bar.open,
        'high': bar.high,
        'low': bar.low,
        'close': bar.close,
        'volume': bar.volume
    })

    return formatted_data

async def handle_realtime_data(data):
    if (datetime.now()-current_time > timedelta(minutes=15)):
        chart.update(format_data_for_chart(data))
    print(f"Real-time data: {format_data_for_chart(data)}")

def start_stream():
    stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL, data_feed='iex')
    stream.subscribe_bars(handle_realtime_data, 'AAPL')
    stream.run()

def wait_until_next_minute():
    # Get the current time
    now = datetime.now()

    # Calculate the start of the next minute
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

    # Calculate the waiting time in seconds
    wait_seconds = (next_minute - now).total_seconds()

    sleep(wait_seconds)
    return(next_minute)



if __name__ == '__main__':
    current_time = wait_until_next_minute()
    api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)
    # Fetch historical data
    ticker = "AAPL"
    timeframe = "1Min"
    start_date = "2023-11-01"

    stream_thread = threading.Thread(target=start_stream)
    stream_thread.start()
    sleep(60*15)
    bars = api.get_bars(ticker, timeframe, start=start_date).df

    # Prepare data for lightweight_charts
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
    # Initialize Chart
    chart = Chart()
    chart.set(bars) 
    chart.watermark(ticker)
    chart.show(block=False)  # Non-blocking show


    

    # Simulate real-time updates
    #for index, row in bars.iloc[30:].iterrows():
    #    sleep()  # Delay to simulate real-time (1 second)
    #    chart.update(pd.Series(row))  # Update chart with new data point as Series