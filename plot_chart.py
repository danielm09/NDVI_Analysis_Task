import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_ndvi_series(df):
    """
    Plot the NDVI time series.

    Args:
        df (pd.DataFrame) : dataframe with mean ndvi values for each date.

    """

    ax = df.plot(marker=".", figsize=(10, 6))

    ax.set_title("NDVI Trend at target locations (average value per buffer)")
    ax.set_ylabel("NDVI")

    ax.legend(title="Location")

    # Format x-axis to include year-month-day
    ax.set_xticks(df.index)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    plt.show() 
    