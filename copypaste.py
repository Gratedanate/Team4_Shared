import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates   #for formatting dates on x-axis

nvda = yf.Ticker('NVDA')

nvda_df = nvda.history(period='2y', interval='1wk')
#print(nvda_history)
nvda_df['Rolling Average'] = nvda_df['Close'].rolling(window=5).mean()

plt.figure(figsize=(12,6))  # optional: bigger chart

plt.plot(nvda_df.index, nvda_df['Close'], label='NVDA Closing Price')
plt.plot(nvda_df.index, nvda_df['Rolling Average'], linestyle='--', label='NVDA 5-Week Rolling Average')

plt.title('NVIDIA Stock Price - Last 2 Years')
plt.xlabel('Month')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Format x-axis labels  for better readability
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))   # tick every 3 months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # e.g. "Jan 2024"
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()