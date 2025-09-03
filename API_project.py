### Team 4
### Nathan Brewer, Andrew Piercy, Brynn Vetrano, Zoe Zung

### Question/Story: 
### We chose Nvidia because of its relevance in the Artificial Intelligence world. 
### As a leading producer of GPUs (which are critical for training and deploying AI models), Nvidia has positioned itself at the forefront of the “AI wave”. 
### The past two years were selected as the time frame because this marks the beginning and rapid acceleration of the AI boom. 
### During this period, Nvidia was (and still is) uniquely positioned to benefit from the surge in demand for AI infrastructure. 

### Data Choices: 
### We are showing the price of the Nvidia stock over the past two years, along with a five-week rolling average of the price of the stock. 
### This rapid upward trend shows how Nvidia has capitalized on the rise of AI and corresponding increased demand for GPUs.

### AI Assistance: 
### Our graph displays the price of the Nvidia stock over the past two years, along with a five-week rolling average of the price of the stock. 
### This rapid upward trend shows how Nvidia has capitalized on the rise of AI and corresponding increased demand for GPUs.

## Import libraries needed for the project
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

nvda = yf.Ticker('NVDA') ## Import NVIDIA stock data

nvda_df = nvda.history(period='2y', interval = '1wk') ## create NVIDIA Dataframe of weekly stock prices over last two years

nvda_df['Rolling Average'] = nvda_df['Close'].rolling(window=5).mean() ## Creates a column in DataFrame for 5-week rolling average

plt.figure(figsize=(12,6))  ## Sets the figure size for the plot

plt.plot(nvda_df.index, nvda_df['Close'], color = 'blue') ## Plots the Closing Price of NVIDIA Stock in the color blue
plt.plot(nvda_df.index, nvda_df['Rolling Average'], linestyle='--', color = 'orange') ## Plots the 5-Week Rolling Average in the color orange

plt.title('NVIDIA Stock Price/Rolling Average - Last 2 Years') ## Adds a title to the plot
plt.xlabel('Date') ## Labels the x-axis as "Date"
plt.ylabel('Price (USD)') ## Labels the y-axis as "Price (USD)"
plt.legend(['NVDA Closing Price', 'NVDA 5-Week Rolling Average']) ## Creates and adds a legend to the plot
plt.figtext(0.01, 0.01, "Source: Yahoo Finance", ha="left", fontsize=8, style="italic")  # Adds a note signifying the source material

ax = plt.gca() #Stores the axes object, allows for editing of x-axis, y-axis, etc.
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3)) ## Sets major ticks on x-axis to be every 3 months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) ## Formats the x-axis ticks to show month and year
plt.xticks(rotation=45) ## Rotates the x-axis ticks 45 degrees for better readability

plt.tight_layout() # Adjusts the plot to ensure that all elements fit with no overlap
plt.show() # Displays the plot

### Takeaway: 
### The graph displays significant growth in NVIDIA's stock price over the past 2 years, with noticeable acceleration in February 2024 and May 2025, and a large dip in April 2025 due to the President’s tariff announcement that caused a macro market sell-off. 
### Additionally, the five-week rolling average smoothes out volatility, making it clear that despite any short-term dips, NVIDIA's stock price continues to rise consistently and uphold a sustained momentum in the market.

