
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
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    random.seed(seed)

    df = pd.read_csv(in_path)
    df['DATE'] = pd.to_datetime(df['DATE'])

    monthly_cols = [col for col in df.columns if 'monthly' in col.lower() and ~df[col].isna().all()]
    daily_cols = [col for col in df.columns if 'daily' in col.lower() and ~df[col].isna().all()]

    vars_monthly = [col.replace('Monthly','') for col in monthly_cols]
    vars_daily = [col.replace('Daily','') for col in daily_cols]


    vars = list(set(vars_daily).intersection(set(vars_monthly)))


    df['month'] = df['DATE'].dt.month

    values = []
    for variable in vars:
        df_temp = df[['month','Monthly'+variable]].dropna()
        temp = df_temp.groupby(['month'])['Monthly'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    values_df = pd.DataFrame(values).T
    values_df.to_csv(out_path,index=True)

    
    with open('data/variable.txt','w') as f:
        for variable in vars:
            f.write(variable+' ')

if __name__ == "__main__":
    main()



