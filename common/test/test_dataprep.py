#!/usr/bin/env python
import sys

import pandas as pd
from pandas import DataFrame
import pandas.io.data

sys.path.append('/home/teddy/Development/Python/common/')

import dataprep


df = pd.read_csv("/home/teddy/Development/Data/DFAST2015/DFAST2015base.csv", index_col='Date', parse_dates=True)

print df['DWCF']

print df['Dates']
#dataprep.transforms.function1(5)

