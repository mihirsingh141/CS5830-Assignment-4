
import pandas as pd
import numpy as np
import os
import sys

import warnings
warnings.filterwarnings('ignore')

def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    df = pd.read_csv(in_path)
    df['DATE'] = pd.to_datetime(df['DATE'])

    with open('data/variable.txt','r') as f:
        file_contents = f.read()
        vars = file_contents.split()

    df['month'] = df['DATE'].dt.month
    values = []

    # Loop through the variables and calculate the mean for each
    for variable in vars:
        # Select the relevant subset of the DataFrame and drop rows with NaN values
        df_temp = df[['month','Daily'+variable]].dropna()
        # Group by 'month' and calculate the mean, then flatten to a list
        temp = df_temp.groupby(['month'])['Daily'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    # Create a new DataFrame from the mean values, with months as rows
    values_df = pd.DataFrame(values).T

    # Save the DataFrame to the output path as a CSV file
    values_df.to_csv(out_path,index=True)

if __name__ == '__main__':
    main()


