import math
import eikon as ek
import numpy as np
impost pandas as pd
import cufflinks as cf
import scipy
from scipy.integrate import quad
import scipy.optimize as spo
import sonfigparser as cp
import sys
cf.set_config_file(offline = True)


cfg = cp.ConfigParser()
cfg.read('eikon.cfg')
ek.set_app_id(cfg['eikon']['app_id'])

fids = ['CF_DATE','EXPIR_DATE','PUTCALLIND','STRIKE_PRC','CF_CLOSE','IMP_VOLT']
aapl = ek.get_data('0#AAPL*.U',fields=fids)[0]
len(aapl)
aapl.head(10)

underlying = aapl.iloc[0]['CF_CLOSE']

calls = aapl[aapl['PUTCALLIND'] == 'CALL'].copy()
for col in ['CF_DATE','EXPIR_DATE']:
  calls[col] = calls[col].apply(lambda date: pd.Timestamp(date))
  
calls.info()

limit = 50

calls = calls[abs(calls['STRIKE_PRC'] - underlying) < limit]
calls.set_index('STRIKE_PRC')[['CF_CLOSE','IMP_VOLT']].iplot(subplots=True,mode='lines+markers',symbol='dot',size=6)

def m76_char_fun(u,T,r,sigma,lambda,mu,delta):
  omega = r - 0.5 * sigma ** 2 - lambda * (np.exp(mu + 0.5 * delta ** 2) - 1)
  value = np.exp((1j * u * omega - 0.5 * u ** 2 * sigma ** 2 +
    lamb * (np.exp(lj * u * mu - u ** 2 * delta * ** 2 * 0.5) - 1)) * T)
  return value
 
def m76_integration_fun(u,s0,K,T,r,sigma,lambda,mu,delta):
  jdcf = m76_char_fun(u - 0.5 * 1j,T,r,sigm,lambda,mu,delta)
  value = 1/ (u ** 2 + .25) * (np.exp(1j * u math.log(s0/K)) + jdcf).real
  return value
  
K = underlying
T = 1.0
r = .005
sigma = .4
lambda = 1.0
mu = -0.2
delta = .1

i = 0; min_rmse = 100.
def m76_error_function(p0):
  global i, min_rmse
  sigma, lambda, mu, delta = p0
  if sigma < 0.0 or delta < 0.0 or lamda < 0.0:
    return 500.0
  se = []
  for row, option in calls.iterrows():
    T = (option['EXPIR_DATE'] - option['CF_DATE']).days/365.
    model_value = m76_value_call_int(underlying, option['STRIKE_PRC'],T,r,sigma,lambda,mu,delta)
    se.append((model_value - option['CF_CLOSE']) ** 2)
  rmse = math.sqrt(sum(se) / len (se))
  min_rmse = min(min_rmse, rmse)
  if i % 100 == 0:
    print('%4d |' % i, np.array(p0), '| %7.3f | %7.3f' % (rmse,min_rmse))
  i += 1
  return rmse

%%time
import scipy.optimize as sop
np.set_printoptions(suppress=True, formatter ={'all' : lambda x: '%6.3f' % x}
p0 = sop.brute(m76_error_function((0.10,0.201,0.025),(0.10,0.81,.2),(-.4,.01,.1),(0.0,0.126,0.025)),finish=None)

%%time
opt = sop.fmin(m76_error_function,p0,xtol=0.0001,ftol=0.0001,maxiter=750,maxfun=1500)

sigma,lambda, mu, delta = opt
calls['MODEL_PRICE'] = 0.0
for row,option in calls.iterrows():
  T = (option['EXPIR_DATE'] - option['CF_DATE']).days / 365.
  calls.loc[row,'MODEL_PRICE'] = m76_value_call_INT(underlying, option['STRIKE_PRC'],T,r,sigma,lambda,mu,delta)
  
calls
