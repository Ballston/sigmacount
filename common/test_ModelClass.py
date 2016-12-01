import pandas as pd
from pandas import DataFrame
import pandas.io.data
import numpy as np

import matplotlib.pyplot as plt

import datetime

import modeler

import statsmodels.api as sm


df = pd.read_csv("/home/teddy/Development/Data/DFAST2015/DFAST2015base.csv", index_col='Date', parse_dates=True)


st = datetime.datetime(2000, 3, 31, 0, 0)
en = datetime.datetime(2015, 12, 31, 0, 0)

ig=lambda x:np.exp(x)
g=lambda x:np.log(x)
test=modeler.ModelClass(data=df,startdate=st,enddate=en, dependent='DWCF',exogenous=['VIX','CPI'] ,transform=g,inverstransform=ig)

test.setmodel(AR=1,I=0,MA=0)

test.estimate()
a=test.fit.summary()
print(dir(test.fit))

print(dir(test.fit.fittedvalues))

#plt.acorr(test.fit.resid,maxlags = 24, linestyle = "solid", usevlines = False, marker='')
#lt.show()

#pandas.tools.plotting.autocorrelation_plot(test.fit.resid)
#plt.show()

#sm.qqplot(test.fit.resid)
#plt.savefig('test.png')
plt.plot(test.fit.fittedvalues.index,test.fit.fittedvalues.values)
plt.show()
print(dir(test.fit.fittedvalues))
#test.fit.fittedvalues.rename('VIX')
# a=pd.DataFrame()
# a['resid']=test.fit.resid
# a['%s_%s' %(test.fit.model.endog_names, 'hat')]=test.fit.fittedvalues
# a['resid'].plot(legend=True,title='Residuals')
# plt.show()
#a['VIX_hat'].plot(legend=True)


print(dir(test.fit))

#test.insample()

