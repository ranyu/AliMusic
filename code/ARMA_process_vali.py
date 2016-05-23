from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import datetime

def ARMA_process(i,filename,p_q,test_error):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
    data = pd.read_csv(filename,parse_dates='Date', index_col='Date',date_parser=dateparse)
    data = data.asfreq('D')
    ts = data['play']
    data.fillna(0,inplace=True)
    data['play'] = data['play'].astype(float) 
    #print (type(data['play']['2015-06-01']))
    #data.plot(figsize=(12,8));
    #plt.show()
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(data.values.squeeze(), lags=90, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(data, lags=90, ax=ax2)
    #plt.show()

    #arma_mod20 = sm.tsa.ARMA(data, (3,0)).fit()
    #print(arma_mod20.params)
    print (p_q)
    '''exception = [3,21,25,27,42]
    if i in exception:
        order = (p_q[0],0,p_q[1])
    else:
        order = (p_q[0],1,p_q[1])'''
    order = (3,0)
    arma_mod30 = sm.tsa.ARMA(data, order).fit()
    #print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    #print(arma_mod30.params)
    sm.stats.durbin_watson(arma_mod30.resid.values)
    #fig = plt.figure(figsize=(12,8))
    #ax = fig.add_subplot(111)
    #ax = arma_mod30.resid.plot(ax=ax)
    #plt.show()
    resid = arma_mod30.resid
    stats.normaltest(resid)
    #fig = plt.figure(figsize=(12,8))
    #ax = fig.add_subplot(111)
    #fig = qqplot(resid, line='q', ax=ax, fit=True)
    #fig = plt.figure(figsize=(12,8))
    #ax1 = fig.add_subplot(211)
    #fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
    #ax2 = fig.add_subplot(212)
    #fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
    r,q,p = sm.tsa.acf(resid.values.squeeze(), nlags=90,qstat=True)
    data = np.c_[range(1,91), r[1:], q, p]
    table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    print(table.set_index('lag'))
    #plt.show()

    predict_sunspots = arma_mod30.predict('2015-08-01','2015-10-30', dynamic=True)
    print(predict_sunspots)
    result = 0
    for s in xrange(1,30):
        if s < 10:
            ele = '2015-08-0'+str(s)
        else:
            ele = '2015-08-'+str(s)
        result += (ts[ele]-predict_sunspots[ele])
    print (result * result)
    test_error += result*result

    fig, ax = plt.subplots(figsize=(12, 8))
    #ax = data.ix['2015-03-02':].plot(ax=ax)
    fig = arma_mod30.plot_predict('2015-08-01','2015-08-30', dynamic=True, ax=ax, plot_insample=False)
    #plt.show()
    return predict_sunspots['2015-08-01':'2015-08-30'],test_error

if __name__ == "__main__":
    import glob
    p_q = [(3,13),(3,10),(2,11),(2,4),(3,11),(3,3),(2,9),(5,13),(3,5),(2,4),(2,8),(3,5),(4,10),(3,9),(3,9),(3,2),(2,2),(3,7),(2,7),(2,2),(3,8),(2,4),(2,11),(6,13),(4,10),(3,10),(3,3),(11,3),(2,2),(2,10),(2,2),(3,5),(2,14),(5,10),(2,2),(4,13),(3,8),(4,5),(3,8),(3,3),(4,6),(1,1),(2,9),(2,8),(4,14),(3,3),(4,12),(4,6),(2,3),(3,8)]
    test_error = 0
    for i,filename in enumerate(glob.glob('../play_number/*.csv')):
        print (i,filename)
        predict_result,test_error = ARMA_process(i,filename,p_q[i],test_error)
        name = '../vali_result/'+filename.split('/')[-1].split('.')[0] + '.csv'
        predict_result.to_csv(name)
    print (test_error)



