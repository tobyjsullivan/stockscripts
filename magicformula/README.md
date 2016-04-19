### How to use

1. Go to the [Google Finance Stock Screener](https://www.google.com/finance#stockscreener)
2. Set these criteria
  * Market cap >= 50M
  * P/E Ratio >= 5 and <= 20
  * Return on assets (TTM) (%) >= 20 and <= 150
3. Remove the other, unused criteria fields
4. You'll want to run the tool for each of the two major exchanges, NYSE and Nasdaq
5. Copy all records outputted into a Google Sheet (in Google Drive). Include the results of each exchange in the same spreadsheet. Sanity check: You should usually get fewer than 100 records for each exchange.
6. Download the sheet as a CSV.
7. Replace input.csv in this project with your exported csv. The one here is just a sample but does demonstrate the format you should expect.
8. Run the script!

### Interpretting the results

You'll get an output which is a list of companies. The value immediately to the right of the ticker symbol is the overall score. This value is computed from the PE Ratio and ROA values and is used to compare stocks directly to each other. 

* Choose the top stocks in the rankings and invest in those for a year (WARNING: this is NOT investment advice. This is simply how _I_ use the tool). 
* Rinse and repeat.

For further details, read The Little Book that Still Beats the Market by Joel Greenblatt.
