import requests
from datetime import datetime, timedelta
import zipfile
import os
import pandas as pd
import statsmodels.api as sm

def generate_yahoo_finance_link(ticker, start_date, end_date, interval):
    start_timestamp = int(datetime.strptime(start_date, "%m/%d/%Y").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%m/%d/%Y").timestamp())
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_timestamp}&period2={end_timestamp}&interval={interval}&events=history&includeAdjustedClose=true"
    return url

def download_yahoo_finance_data(url, filename):
    headers = {'User-Agent': 'Mozilla/5.0'}
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Data downloaded and saved to {filename}")
        else:
            print("Failed to download data")

def download_ken_french_data(interval):
    urls = {
        "1d": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",
        "1mo": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"
    }
    if interval in urls:
        response = requests.get(urls[interval])
        if response.status_code == 200:
            with open("french_data.zip", "wb") as f:
                f.write(response.content)
            with zipfile.ZipFile("french_data.zip", "r") as zip_ref:
                zip_ref.extractall()
            os.remove("french_data.zip")
            print("Ken French data downloaded and saved.")
        else:
            print("Failed to download Ken French data.")
    else:
        print("Invalid interval.")

def merge_and_prepare_data():
    yahoo_data = pd.read_csv("yahoo_data.csv")
    yahoo_data = yahoo_data[['Date', 'Adj Close']]
    ff_data = pd.read_csv("F-F_Research_Data_5_Factors_2x3.csv", skiprows=3)
    ff_data = ff_data[ff_data['Unnamed: 0'].str.match(r'^\d{6}$', na=False)]
    ff_data['Date'] = pd.to_datetime(ff_data['Unnamed: 0'], format='%Y%m')
    ff_data.drop(columns=['Unnamed: 0'], inplace=True)
    yahoo_data['Date'] = pd.to_datetime(yahoo_data['Date'])
    merged_data = pd.merge(yahoo_data, ff_data, on='Date')
    merged_data['RF'] = pd.to_numeric(merged_data['RF'], errors='coerce')
    merged_data['Return'] = merged_data['Adj Close'].pct_change()
    merged_data = merged_data[merged_data['Return'].notnull()]
    merged_data['Excess Return'] = merged_data['Return'] - merged_data['RF']
    return merged_data

def run_regression_analysis(data):
    data = data.apply(pd.to_numeric, errors='coerce')
    dependent_var = data['Excess Return']
    independent_vars = {
        'CAPM': data[['Mkt-RF']],
        'FF 3': data[['Mkt-RF', 'SMB', 'HML']],
        'FF 5': data[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']],
        'FF No HML': data[['Mkt-RF', 'SMB', 'RMW', 'CMA']],
        'FF No SMB': data[['Mkt-RF', 'HML', 'RMW', 'CMA']]
    }
    results_dict = {}
    for model_name, vars in independent_vars.items():
        X = sm.add_constant(vars)
        model = sm.OLS(dependent_var, X)
        results = model.fit()
        results_dict[model_name] = results
    return results_dict

def display_and_save_results(results_dict):
    # Specified index order to maintain consistency
    index_order = [
        'Intercept', 'Intercept (SE)',
        'Mkt-RF', 'Mkt-RF (SE)',
        'SMB', 'SMB (SE)',
        'HML', 'HML (SE)',
        'RMW', 'RMW (SE)',
        'CMA', 'CMA (SE)',
        'Overall Significance',
        'R-Square',
        'Adjusted R-Square'
    ]

    # Initialize the dataframe with specified index order
    summary_table = pd.DataFrame(index=index_order, columns=results_dict.keys())

    # Populate the table
    for model_name, results in results_dict.items():
        for i, coeff_name in enumerate(results.model.exog_names):
            formatted_name = 'Intercept' if coeff_name == 'const' else coeff_name
            significance = ('*' * int(results.pvalues[i] < 0.10) +
                            '*' * int(results.pvalues[i] < 0.05) +
                            '*' * int(results.pvalues[i] < 0.01))
            summary_table.at[formatted_name, model_name] = f"{results.params[i]:.3f}{significance}"
            summary_table.at[f"{formatted_name} (SE)", model_name] = f"({results.bse[i]:.3f})"

        # Adding model statistics with significance indicator for overall significance
        f_pvalue = results.f_pvalue
        overall_significance = f"{f_pvalue:.3f}"  # Rounded to three decimal places
        overall_significance += ('***' if f_pvalue < 0.01 else '**' if f_pvalue < 0.05 else '*' if f_pvalue < 0.10 else '')
        summary_table.at['Overall Significance', model_name] = overall_significance
        summary_table.at['R-Square', model_name] = f"{results.rsquared:.3f}"
        summary_table.at['Adjusted R-Square', model_name] = f"{results.rsquared_adj:.3f}"
    
    return summary_table

def main():
    # Setup dates and interval for data retrieval
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=365*7)).strftime("%m/%d/%Y")
    ticker = input("Enter the ticker symbol: ")
    start_date = input(f"Enter the start date ({start_date}): ") or start_date
    end_date = input(f"Enter the end date ({end_date}): ") or end_date
    #interval = input("Enter 'd' for daily data (default monthly): ")
    interval = "1d" #if interval.lower() == 'd' else "1mo"

    # Download data from Yahoo Finance
    yahoo_finance_link = generate_yahoo_finance_link(ticker, start_date, end_date, interval)
    download_yahoo_finance_data(yahoo_finance_link, "yahoo_data.csv")

    # Download data from Ken French
    download_ken_french_data(interval)

    # Merge and prepare data
    data = merge_and_prepare_data()

    # Perform regression analysis
    results_dict = run_regression_analysis(data)

    # Display and save regression results
    summary_table = display_and_save_results(results_dict)
    
    summary_table.to_excel(f"{ticker}_{start_date.replace('/', '-')}_to_{end_date.replace('/', '-')}.xlsx")
    print(summary_table)
    
    print("Analysis completed.")

if __name__ == "__main__":
    main()

