# Fama-French
Fama-French Code for FIN 448 @ UAkron by John Goodell

## Operations
1. Asks user for ticker and date range
2. Pulls data for ticker from Yahoo Finance and most recent 5-Factors data
3. Merges data by date and adds additional neccessary columns
4. Performs CAPM, FF-3, FF-5, FF No HML, and FF No SMB regressions.
5. Consolidates and formats results with coefficients, significance indicators (1%***, 5%**, 10%***), standard errors, R-Square, Adjusted R-Square, and Overall Significance.
6. Prints results and outputs to file with information used to run the analysis.
