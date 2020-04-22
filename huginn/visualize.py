##################################
# PLOT DATA

import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.express as px

def plot_data_plotly(data):
    fig = px.line(data, x=data.index, y=data.columns[0])

    fig.update_layout(
        title='Google Search Interest in '+ data.columns[0] + ' over Time',
        xaxis_title="Year",
        yaxis_title="Interest (Standardized)",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
            )
        )
    return plotly.offline.plot(fig, auto_open=False, output_type='div')

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

def plot_data_with_anomalies_plotly(data, anomalies, as_var=False):
    fig = px.line(data, x=data.index, y=data.columns[0])

    shapes = []
    for anomaly in anomalies:
        # shapes.append({  # Unbounded line at x = 4
        #         'type': 'line',
        #         # x-reference is assigned to the x-values
        #         'xref': 'x',
        #         # y-reference is assigned to the plot paper [0,1]
        #         'yref': 'paper',
        #         'x0': anomaly,
        #         'y0': 0,
        #         'x1': anomaly,
        #         'y1': 1,
        #         'line': {
        #             'color': 'rgb(55, 128, 191)',
        #             'width': 3,
        #         },
        #     }
        # )
        shapes.append({# Unbounded span at 6 <= x <= 8
                'type': 'rect',
                # x-reference is assigned to the x-values
                'xref': 'x',
                # y-reference is assigned to the plot paper [0,1]
                'yref': 'paper',
                'x0': anomaly - pd.DateOffset(15),
                'y0': 0,
                'x1': anomaly + pd.DateOffset(15),
                'y1': 1,
                'fillcolor': 'red',
                'opacity': 0.2,
                'line': {
                    'width': 0,
                }
            }
        )

    fig.update_layout(
        title='Google Search Interest in '+ data.columns[0] + ' over Time',
        xaxis_title="Year",
        yaxis_title="Interest (Standardized)",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
            ),
        shapes=shapes
        )
    return plotly.offline.plot(fig, auto_open=False, output_type='div')

def plot_data_with_anomalies(data, anomalies, as_var=False):
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
    if not as_var:
        plt.show()
        print("""
        If you are not happy with these anomalies, you can call the method \'get_anomalies\' and
        specify the function to get anomalies:
        - method = 'constant' with parameter k (set to 1 by default)
        - method = 'rolling' with parameters lookback_mean, lookback_std and k (set to 1, 10, 1 by default)
        - method = 'ewm' with parameters halflife_mean, halflife_std and k(set to 1,10,1 by default) [default method]
        """)
    return fig
