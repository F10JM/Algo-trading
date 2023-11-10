import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart
import alpaca_trade_api as tradeapi

APCA_API_KEY_ID = "PKM83SCG7GK5OHPJKEEM"
APCA_API_SECRET_KEY = "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

def get_bar_data(symbol, timeframe):
    start_date = "2023-11-01"
    end_date = "2023-11-09"
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

def on_timeframe_selection(chart):  # Called when the user changes the timeframe.
    new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
    if new_data.empty:
        return
    chart.set(new_data, True)


if __name__ == '__main__':
    chart = Chart(toolbox=True)
    chart.legend(True)


    chart.topbar.textbox('symbol', 'TSLA')
    chart.topbar.switcher('timeframe', ('1min', '5min', '30min'), default='5min',
                        func=on_timeframe_selection)

    df = get_bar_data('TSLA', '5min')
    chart.set(df)


    chart.show(block=True)