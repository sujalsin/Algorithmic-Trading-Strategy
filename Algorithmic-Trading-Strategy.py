import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np


# Define Moving Average Strategy
def moving_average_strategy(data, short_window, long_window):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # Create short simple moving average over the short window
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

    # Create long simple moving average over the long window
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                > signals['long_mavg'][short_window:], 1.0, 0.0)
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    return signals


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Download AAPL data
    data = yf.download('AAPL', start='2020-01-01', end='2023-12-31')

    # Create a moving average DataFrame
    ma_df = moving_average_strategy(data, 50, 200)

    # Plotting
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Price in $')
    data['Close'].plot(ax=ax1, color='r', lw=2.)
    ma_df[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the buy signals
    ax1.plot(ma_df.loc[ma_df.positions == 1.0].index,
             ma_df.short_mavg[ma_df.positions == 1.0],
             '^', markersize=10, color='m')

    # Plot the sell signals
    ax1.plot(ma_df.loc[ma_df.positions == -1.0].index,
             ma_df.short_mavg[ma_df.positions == -1.0],
             'v', markersize=10, color='k')

    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
