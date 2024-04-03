
import pandas as pd
import numpy as np
import random
import yaml
import sys

import warnings
warnings.filterwarnings('ignore')

def main():
    params = yaml.safe_load(open("params.yaml"))["prepare"]

    seed = params['seed']

    # Input and output file paths from command line arguments
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    random.seed(seed)

    df = pd.read_csv(in_path)

    # Convert the DATE column to datetime objects
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Find all monthly columns with data (not entirely NaN) and extract their names
    monthly_cols = [col for col in df.columns if 'monthly' in col.lower() and ~df[col].isna().all()]

    # Do the same for daily columns
    daily_cols = [col for col in df.columns if 'daily' in col.lower() and ~df[col].isna().all()]


    # Remove the 'Monthly' prefix from the monthly columns
    vars_monthly = [col.replace('Monthly','') for col in monthly_cols]
    # Remove the 'Daily' prefix from the daily columns
    vars_daily = [col.replace('Daily','') for col in daily_cols]

    # Find the intersection of variables present in both daily and monthly data
    vars = list(set(vars_daily).intersection(set(vars_monthly)))

    # Extract the month from the DATE column for grouping
    df['month'] = df['DATE'].dt.month

    # Calculate the monthly mean for each variable and add to the values list
    values = []
    for variable in vars:
        df_temp = df[['month','Monthly'+variable]].dropna()
        temp = df_temp.groupby(['month'])['Monthly'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    values_df = pd.DataFrame(values).T
    values_df.to_csv(out_path,index=True)

    # Write the variables processed to a text file
    with open('data/variable.txt','w') as f:
        for variable in vars:
            f.write(variable+' ')

if __name__ == "__main__":
    main()



