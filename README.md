This project shows the bank failures in the United States from 2007, the onset of the Great Recession, through 2024. 
One page displays the states where each bank failed by year. The other page shows the amount of bank failures compared to the interest rate spread, specifically the ten year to one month treasury yields.
The relationship between bank failures and macroeconomic conditions is often unclear or overlooked by the general public, as data on these topics exists but is rarely presented in an intuitive, interactive, or accessible way.
We made this website with the goal of providing accessible, data-driven insights to how the banking industry and Federal Reserve policy overlap to help people better understand warning signs of financial instability or the impact of monetary policy decisions.

The audience could be students and educators studying finance, economics, or public policy; researchers interest in historical financial tends, or the curious general public.

This website provides an interactive, visual exploration of bank failures in the U.S. from 2007 to 2024, contextualized alongside interest rates.
By making complex financial data more understandable, it helps users understand historical patterns in financial crises, understand how monetary policy correlates with banking instability, and engage with data through clear, dynamic visuals instead of static reports or dense tables.

**Data Description:**
Bank Failures - 
Data obtained from Data.gov sourced from the Federal Deposit Insurance Corporation (FDIC). The dataset, "banklist.csv" contains information on bank failures including institution names, locations, dates of closure, and who acquired them.

Interest Rates Spread - 
Data from the U.S. Department of the Treasury, _Daily Treasury Par Yield Curve Rates from 1990-2024_. The dataset, "yield-curve-rates-1990-2024.csv", includes daily rates for multiple Treasury maturirties, from which the 10-Year minus 1-Month spread was calculated.

**Data Dictionary:**
Bank Failures - 
Bank Name: a string, full legal name of the failed financial institution
City: a string, city where the failed bank was headquatered
State: a string (two characters), state abbreviation where the bank was located
Cert: an integer, FDIC identifying number assigned to the bank
Acquiring Institution: a string, name of the bank or financial institution that acquired the failed bank
Closing date: date format, date of when the bank officially failed or was closed
Fund: an integer, numeric identifer associated with the resolution

Interest Rate Spread - 
Date: date format, date on which the yield rates were recorded
1-Month, 2-Month, 3-Month, 4-Month, 6-Month, 1-Year, 2-Year, 3-Year, 5-Year, 7-Year, 10-Year, 20-Year, 30-Year: U.S Treasury securities yields, expressed as annualized percentages
