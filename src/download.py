import requests
from bs4 import BeautifulSoup
import os
import random
import pandas as pd
import numpy as np
import yaml

import warnings
warnings.filterwarnings('ignore')



def main():
    # Load parameters from the params.yaml file
    params = yaml.safe_load(open("params.yaml"))["download"]

    # Format the year and number of locations based on the parameters
    year = str(params['year'])+'/'
    n_loc = str(params['n_loc'])+'.csv'

    # Base URL for the NOAA Climatological Data
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/'
    

    main_url = os.path.join(url,year,n_loc)
    response = requests.get(main_url)

    local_filename = 'weather.csv'

    os.makedirs('data',exist_ok=True)

    # Write the response content to a CSV file under the 'data' directory
    open(os.path.join('data',local_filename),'wb').write(response.content)
    
if __name__ == "__main__":
    main()

