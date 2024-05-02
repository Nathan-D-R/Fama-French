## Improvements

### Send source data to ./Data directory
ex. ./Data/VINAX_d_12-01-2018_-_01-01-2024.csv
ex. ./Data/F-F_Research_Data_5_Factors_2x3_d.csv

### Calculate rough beta for each ticker

### Don't pull data if it would have specified date range already

### Support daily frequency
> Ask for frequency first, defaulting to monthly
> Ask for monthly, with simplified format (Monthly = MM/YYYY, Daily = MM/DD/YYYY)

### Allow list of tickers as input

### Allow command line args with flags
ex. fama-french --ticker VINAX,SP500 --from 12/01/2018 --to 01/01/2024 --frequency mo

### Add GUI frontend
