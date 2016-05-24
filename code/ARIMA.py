#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
rcParams['figure.figsize'] = 15, 6

from statsmodels.tsa.stattools import adfuller

def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    #plt.show(block=False)
    #plt.show()
    
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput
def ARIMA_process(i,filename):
    print('../demo/'+filename.split('/')[-1])
    IND = [1,4,9,14,26,30,35,40,45]
    if i in IND:
        print 'RRRR!!!',i,filename
        return 
    data = pd.read_csv(filename)
    #print data.head()
    #print '\n Data Types:'
    #print data.dtypes
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
    data = pd.read_csv(filename, parse_dates='Date', index_col='Date',date_parser=dateparse)
    #print data.head()
    #print data.index
    ts = data['play'] 
    #print ts.head(1)
    #print ts['2015-04-01':'2015-04-06']
    #print ts['2015-04']
    test_stationarity(ts)
    #ts_log = np.log(ts['2015-03-01':'2015-06-30'])
    ts_log = np.log(ts)
    plt.plot(ts_log)
    #plt.show()
    plt.plot(ts)
    #plt.show()
    moving_avg = pd.rolling_mean(ts_log,7)
    plt.plot(ts_log)
    plt.plot(moving_avg, color='red')
    #plt.show()
    ts_log_moving_avg_diff = ts_log - moving_avg
    ts_log_moving_avg_diff.head(7)
    #print ts_log_moving_avg_diff
    ts_log_moving_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_moving_avg_diff)
    expwighted_avg = pd.ewma(ts_log, halflife=7)
    plt.plot(ts_log)
    plt.plot(expwighted_avg, color='red')
    #plt.show()
    ts_log_ewma_diff = ts_log - expwighted_avg
    test_stationarity(ts_log_ewma_diff)

    ts_log_diff = ts_log - ts_log.shift()
    plt.plot(ts_log_diff)
    #plt.show()
    ts_log_diff.dropna(inplace=True)
    test_stationarity(ts_log_diff)

    from statsmodels.tsa.seasonal import seasonal_decompose
    '''decomposition = seasonal_decompose(ts_log.values,freq=7)
    #decomposition = seasonal_decompose(ts_log)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal,label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    #plt.show()

    #ts_log_decompose = residual
    #ts_log_decompose.dropna(inplace=True)
    #test_stationarity(ts_log_decompose)'''

    #ACF and PACF plots:
    from statsmodels.tsa.stattools import acf, pacf
    lag_acf = acf(ts_log_diff, nlags=20)
    lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')
    #Plot ACF: 
    plt.subplot(121) 
    plt.plot(lag_acf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Autocorrelation Function')

    #Plot PACF:
    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()
    #plt.show()

    #ts_log = np.log(ts['2015-04-01':'2015-08-30'])
    #ts_log = np.log(ts['2015-03-01':'2015-08-31'])
    #print len(ts_log)
    #print ts_log
    from statsmodels.tsa.arima_model import ARIMA
    print i
    IND = [1,4,9]
    if i in IND:
        return 
        leap = 0
        OR = (1,0,0)
        OR_1 = (0,0,1)
        OR_2 = (1,0,1)
    else:
        leap = 1
        OR_1 = (2,1,0)
        OR_2 = (0,1,2)
        OR = (2,1,2)
    leap = 1
    model = ARIMA(ts_log, order=OR_1)  
    results_AR = model.fit(disp=-1)  
    #print results_AR.predict('2015-08-01','2015-10-30')

    plt.plot(ts_log_diff)
    plt.plot(results_AR.fittedvalues, color='red')
    plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_log_diff)**2))
    #plt.show()

    model = ARIMA(ts_log, order=OR_2)  
    #print ts_log[-1]
    results_MA = model.fit(disp=-1)  
    plt.plot(ts_log_diff)
    plt.plot(results_MA.fittedvalues, color='red')
    plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2))
    #plt.show()

    #model = ARIMA(ts_log, order=(2, 1, 2))  
    model = ARIMA(ts_log, order=OR)  
    #print ts_log_diff
    #print ts_log
    results_ARIMA = model.fit(disp=-1)  
    #print 'RRRR',results_ARIMA.fittedvalues
    ranyu = results_ARIMA.forecast(steps=30)[0]
    #print ranyu
    #print results_ARIMA.fittedvalues
    #raw_input()
    #plt.plot(ts_log_diff)
    #plt.plot(results_ARIMA.fittedvalues, color='red')
    #plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
    #plt.show()

    #predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_1 = pd.Series(results_ARIMA.fittedvalues, copy=True)
    #predictions_ARIMA_diff = pd.Series(ranyu, copy=True)
    #print '~~~',predictions_ARIMA_1
    #print '!!!',predictions_ARIMA_diff
    #print ranyu
    #print results_ARIMA.fittedvalues
    #predictions_ARIMA_diff = pd.Series(ranyu, copy=True)
    #print predictions_ARIMA_diff.head()
    #predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA_diff_1 = predictions_ARIMA_1.cumsum()
    #print predictions_ARIMA_diff_cumsum.head()
    print predictions_ARIMA_diff_1.head()
    #rng = pd.date_range('9/1/2015', periods=60, freq='D')
    predictions_ARIMA_log_1 = pd.Series(ts_log.ix[0], index=ts_log.index)
    #predictions_ARIMA_log = pd.Series(ranyu.ix[0], index=ranyu.index)
    #print predictions_ARIMA_log_1
    #print predictions_ARIMA_log
    #predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    predictions_ARIMA_log_1 = predictions_ARIMA_log_1.add(predictions_ARIMA_diff_1,fill_value=0)
    #print predictions_ARIMA_log_1
    #print predictions_ARIMA_log
    #print predictions_ARIMA_log.head()
    #print predictions_ARIMA_log_1.head()

    predictions_ARIMA = np.exp(ranyu)
    predictions_ARIMA_1 = np.exp(predictions_ARIMA_log_1)
    #print predictions_ARIMA
    #print predictions_ARIMA_1
    #plt.plot(ts)
    plt.plot(predictions_ARIMA)
    #plt.show()
    plt.plot(predictions_ARIMA_1)
    #plt.show()
    print '---------\n'
    with open('../demo/'+filename.split('/')[-1],'w') as f:
        for fl,i in enumerate(predictions_ARIMA):
            if fl < 9:
                f.write('2015080'+str(fl+1)+',')
            else:
                f.write('201508'+str(fl+1)+',')
            #print i
            f.write(str(i)+'\n')
    #plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
    #plt.show()

def main():
    import glob
    for i,filename in enumerate(glob.glob('../local_train/*')):
        #print i,filename
        ARIMA_process(i,'../local_train/'+filename)
if __name__ == "__main__":
    main()

