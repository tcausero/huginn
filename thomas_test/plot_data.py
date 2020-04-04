import matplotlib.pyplot as plt
from anomalies import get_anomalies_v1, get_anomalies_v2, get_anomalies_v3
import pandas as pd

def plot_data(data):
    fig, ax = plt.subplots(1, 1, figsize=(20, 5))
    ax.plot(data, label = data.columns[0])
    ax.set_xlabel('Year')
    ax.set_ylabel('Interest (Standardized)')
    ax.set_title('Google Search Interest in '+ data.columns[0] + ' over Time')
    fig.autofmt_xdate()
    plt.legend()
    plt.show()

def plot_data_with_anomalies(data, anomalies):
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