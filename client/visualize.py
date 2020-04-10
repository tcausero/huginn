##################################
# PLOT DATA

import matplotlib.pyplot as plt
import pandas as pd

def plot_data(data):
    """ Plot the data (time series)
    
    :argument data: dataframe with time as index and interests (volume of google searches) as first column
    Note that the name of the first column is the name of the enity
    """
    fig, ax = plt.subplots(1, 1, figsize=(20, 5))
    ax.plot(data, label = data.columns[0])
    ax.set_xlabel('Year')
    ax.set_ylabel('Interest (Standardized)')
    ax.set_title('Google Search Interest in '+ data.columns[0] + ' over Time')
    fig.autofmt_xdate()
    plt.legend()
    plt.show()

def plot_data_with_anomalies(data, anomalies):
    """ Plot the data and add anomalies as line on the graph
    
    :argument data: dataframe (same as above)
    :argument anomalies: DatetimeIndex of dates (corresponding to anomalies) - dtype=datetime64[ns]
    """
    fig, ax = plt.subplots(1, 1, figsize=(20, 5))
    ax.plot(data, label = data.columns[0])
    ax.set_xlabel('Year')
    ax.set_ylabel('Interest (Standardized)')
    ax.set_title('Google Search Interest in '+ data.columns[0] + ' over Time')
    fig.autofmt_xdate()
    
    for anomaly in anomalies:
        ax.axvspan(anomaly - pd.DateOffset(5), 
                     anomaly + pd.DateOffset(5), 
                     color='y', alpha=0.5, lw=0)
    
    plt.legend()
    plt.show()