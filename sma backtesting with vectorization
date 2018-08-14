import eikon as ek
import numpy as np
import pandas as pd
import cufflinks as cf
import configparser as cp
cf.set_config_file(offline=True)

cfg = cp.ConfigParser()
cfg.read('eikon.cfg')
ek.set_app_id(cfg['eikon']['app_id'])

ric = 'AAPL.O'
data = ek.get_timeseries(ric,fields = 'CLOSE',start_date='2015-01-01',end_date='2018-08-15')
data.normalize().iplot(kind='lines')

SMA1 = 42 # days
SMA2 = 252 # days

data['SMA1'] = data['CLOSE'].rolling(SMA1).mean()
data['SMA2'] = data['CLOSE'].rolling(SMA2).mean()

data.iplot()
data.dropna(inplace = True) #dropping na to account for SMA periods with not enough data to smooth.

data['position'] = np.where(data['SMA1'] > data['SMA2'],1,-1)
data.iplot(secondary_y='position')

data['returns'] = np.log(data['CLOSE'] / data['CLOSE'].shift(1))
data.dropna(inplace=True)
data['returns'].iplot(kind='histogram',subplots=True)

data['strategy'] = data['positions'].shift(1) * data['returns']

np.exp(data[['returns','strategy']].sum())
data[['returns','strategy']].cumsum().apply(np.exp).iplot()

