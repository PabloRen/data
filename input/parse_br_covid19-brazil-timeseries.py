#!/usr/bin/env python

from datetime import datetime
from pandas import DataFrame
from covid_io import read_argv
from utils import dataframe_output


# Read data from GitHub repo
confirmed, deaths = read_argv()
for df in (confirmed, deaths):
    df.rename(columns={'Unnamed: 1': 'RegionCode'}, inplace=True)
    df.set_index('RegionCode', inplace=True)

# Transform the data from non-tabulated format to record format
records = []
for region_code in confirmed.index.unique():
    for col in confirmed.columns[1:]:
        date = col + '/' + str(datetime.now().year)
        date = datetime.strptime(date, '%d/%m/%Y').date().isoformat()
        records.append({
            'Date': date,
            'RegionCode': region_code,
            'Confirmed': confirmed.loc[region_code, col],
            'Deaths': deaths.loc[region_code, col]})
df = DataFrame.from_records(records)

# Output the results
dataframe_output(df, 'BR')
