import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream

# Set your API key and secret
APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  # URL for paper trading

# Define a function to handle incoming messages for trade updates
async def handle_trade_update(data):
    print(f"Trade update: {data}")

# Define a function to handle incoming messages for real-time data
async def handle_realtime_data(data):
    print(f"Real-time data: {data}")

# Initialize Stream
stream = Stream(APCA_API_KEY_ID,
                APCA_API_SECRET_KEY,
                base_url=APCA_API_BASE_URL,
                data_feed='iex')  # use 'sip' for paid subscription

# Subscribe to trade updates and real-time data for a specific ticker
stream.subscribe_trade_updates(handle_trade_update)
stream.subscribe_bars(handle_realtime_data, 'AAPL')

# Start streaming in an asynchronous context
stream.run()