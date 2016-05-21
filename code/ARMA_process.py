from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

def ARMA_process(filename):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
    data = pd.read_csv(filename,parse_dates='Date', index_col='Date',date_parser=dateparse)
    #print (data)
    data = data.asfreq('D')
    data.fillna(0,inplace=True)
    data['play'] = data['play'].astype(float) 
    #print (type(data['play']['2015-06-01']))
    data.plot(figsize=(12,8));
    #plt.show()
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(data.values.squeeze(), lags=40, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(data, lags=40, ax=ax2)
    #plt.show()

    arma_mod20 = sm.tsa.ARMA(data, (3,0)).fit()
    #print(arma_mod20.params)
    arma_mod30 = sm.tsa.ARMA(data, (3,0)).fit()
    #print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    #print(arma_mod30.params)
    sm.stats.durbin_watson(arma_mod30.resid.values)
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax = arma_mod30.resid.plot(ax=ax)
    #plt.show()
    resid = arma_mod30.resid
    stats.normaltest(resid)
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    fig = qqplot(resid, line='q', ax=ax, fit=True)
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
    r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
    data = np.c_[range(1,41), r[1:], q, p]
    table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    #print(table.set_index('lag'))
    #plt.show()

    predict_sunspots = arma_mod30.predict('2015-08-01', '2015-08-31', dynamic=True)
    #print(predict_sunspots)

    fig, ax = plt.subplots(figsize=(12, 8))
    #ax = data.ix['2015-03-02':].plot(ax=ax)
    fig = arma_mod30.plot_predict('2015-08-01', '2015-08-31', dynamic=True, ax=ax, plot_insample=False)
    #plt.show()
    return predict_sunspots

if __name__ == "__main__":
    import glob
    for i,filename in enumerate(glob.glob('../local_train/train_*')):
        print (i,filename)
        predict_result = ARMA_process(filename)
        name = '../vali_result/'+filename.split('/')[-1].split('.')[0] + '_result.csv'
        predict_result.to_csv(name)

