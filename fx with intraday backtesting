import eikon as ek
import numpy as np
import pandas as pd
import cufflinks as cf
import configparser as cp
cf.set_config_file(offline=True)

ric = 'GBP='
data = ek.get_timeseries(ric,fields='MID',start_date='2018-08-13 10:00:00', end_date='2018-08-13 16:00:00', interval='minute')
data.head()
data.info()

data.normalize().iplot(kind='lines')

SMA1 = 10 
SMA2 = 30

data['SMA1'] = data['MID'].rolling(SMA1).mean()
data['SMA2'] = data['MID'].rolling(SMA2).mean()

data.dropna(inplace=True)

data.iplot()

data['positions'] = np.where(data['SMA1'] > data['SMA2'],1,-1)
data.iplot(secondary_y = 'positions')
data['returns'] = np.log(data['MID'] / data['MID'].shift(1) )

np.exp(data[['returns','strategy']].sum())
data[['returns','strategy']].cumsum().apply(np.exp).iplot()

#test multiple simple averages

def simple_average_combos(data,SMA1,SMA2,price_fid = "MID"):
  sma1 = data[price_fid].rolling(SMA1).mean()
  sma2 = data[price_fid].rolling(SMA2).mean()
  pos = np.where(sma1 > sma2,1,-1)
  pos.concat(data[price_fid],inplace=True)
  pos.dropna(inplace = True)
  rets = np.log(pos[price_fid] / pos[price_fid].shift(1))
  returns, strategy = (np.exp(data[[price_fid]]).sum())
  return returns, strategy

init = []
x = 0
while x < 1000:
  a1 = np.randint(1,252)
  a2 = np.randint(1,252)
  eg_rets, eg_strat = simple_average_combos(data,SMA1 = a1, SMA2 = a2, price_fid = 'Mid')
  row = [a1, a2, eg_rets, eg_strat]
  init.append(row)
  x += 1
