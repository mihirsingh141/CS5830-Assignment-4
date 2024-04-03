
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
    for variable in vars:
        df_temp = df[['month','Daily'+variable]].dropna()
        temp = df_temp.groupby(['month'])['Daily'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    values_df = pd.DataFrame(values).T
    values_df.to_csv(out_path,index=True)

if __name__ == '__main__':
    main()


