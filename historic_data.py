import config, requests, json
from datetime import datetime

# minute_bars_url = config.BARS_URL + '/5Min?symbols=MSFT&limit=1000'

day_bars_url = '{}/day?symbols={}&limit=1000'.format(config.BARS_URL, "AAPL")

r = requests.get(day_bars_url, headers=config.HEADERS)

print(json.dumps(r.json(), indent=4))