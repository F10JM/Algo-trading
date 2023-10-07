from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
import config
import pandas
client = StockHistoricalDataClient(config.API_KEY,config.SECRET_KEY)
request_params = StockBarsRequest(
                        symbol_or_symbols=["TSLA"],
                        timeframe=TimeFrame(5, TimeFrame.Minute),
                        start="2023-0-01 00:00:00")
bars = client.get_stock_bars(request_params)
bars_df = bars.df
print(bars_df)