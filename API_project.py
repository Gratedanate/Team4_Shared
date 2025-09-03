### Team 4
### Nathan Brewer, Andrew Piercy, Brynn Vetrano, Zoe Zung

### Question/Story:

import requests
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

nvda = yf.Ticker('NVDA')

nvda_df = nvda.history(period='2y', interval = '1wk')
#print(nvda_history)

nvda_df['Rolling Average'] = nvda_df['Close'].rolling(window=5).mean()

plt.plot(nvda_df['Close'])
plt.plot(nvda_df['Rolling Average'], linestyle='--')
plt.title('NVIDIA Stock Price - Last 2 Years')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend(['NVDA Closing Price', 'NVDA 5-Week Rolling Average'])
plt.show()

### Takeaway: