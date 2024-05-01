# Fama-French
Fama-French Code for FIN 448 @ UAkron by John Goodell

## Operations
1. Asks user for ticker and date range
2. Pulls data for ticker from Yahoo Finance and most recent 5-Factors data
3. Merges data by date and adds additional neccessary columns
4. Performs CAPM, FF-3, FF-5, FF No HML, and FF No SMB regressions.
5. Consolidates and formats results with coefficients, significance indicators (1%\*\*\*, 5%\*\*, 10%\*), standard errors, R-Square, Adjusted R-Square, and Overall Significance.
6. Prints results and outputs to file with information used to run the analysis.

## Usage
Before using, ensure you have Python, Pandas, and StatsModels.

```
Fama-French ➤ python main.py
Enter the ticker symbol: VINAX
Enter the start date (05/02/2017): 12/01/2018
Enter the end date (04/30/2024): 01/01/2024
Data downloaded and saved to yahoo_data.csv
Ken French data downloaded and saved.
                           CAPM       FF 3  ...  FF No HML  FF No SMB
Intercept             -0.124***  -0.121***  ...  -0.124***  -0.124***
Intercept (SE)          (0.029)    (0.029)  ...    (0.030)    (0.030)
Mkt-RF                   -0.002     -0.002  ...     -0.001      0.000
Mkt-RF (SE)             (0.005)    (0.006)  ...    (0.006)    (0.006)
SMB                         NaN      0.009  ...      0.013        NaN
SMB (SE)                    NaN    (0.011)  ...    (0.011)        NaN
HML                         NaN      0.002  ...        NaN     -0.003
HML (SE)                    NaN    (0.008)  ...        NaN    (0.009)
RMW                         NaN        NaN  ...      0.008      0.002
RMW (SE)                    NaN        NaN  ...    (0.012)    (0.011)
CMA                         NaN        NaN  ...      0.013      0.016
CMA (SE)                    NaN        NaN  ...    (0.011)    (0.013)
Overall Significance      0.727      0.784  ...      0.493      0.718
R-Square                  0.003      0.029  ...      0.090      0.057
Adjusted R-Square        -0.023     -0.052  ...     -0.014     -0.051

[15 rows x 5 columns]
Analysis completed.
```
