import alpaca_trade_api as tradeapi
import pandas as pd

APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  

# Create an API object
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

# Define the ticker, timeframe, start, and end dates
ticker = "AAPL"
timeframe = "1D"  # Possible values: '1Min', '5Min', '15Min', '1H', '1D'
start_date = "2022-01-01"
end_date = "2022-12-31"

# Fetch historical data
#bars = api.get_bars(ticker, timeframe, start=start_date, end=end_date).df

# The result is already a pandas DataFrame
#print(bars.head())

# Define a function to handle incoming price updates
async def on_price_update(data):
    print(f"Received price update: {data}")

# Set up the streaming connection
stream = tradeapi.Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# Subscribe to updates for a specific ticker
stream.subscribe_bars(on_price_update, 'AAPL')

# Start the stream
stream.run()