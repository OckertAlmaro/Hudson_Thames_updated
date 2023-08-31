import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import math
from datetime import datetime, timedelta

# Define a function to read tick data from a CSV file
def read_data(file_path):
    """
    Reads data from a CSV file containing timestamp, price, and volume columns.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries, each containing timestamp, price, and volume.
    """
    data = []
    # Open and read the CSV file
    with open(file_path, 'r') as file:
        # Split the CSV line into individual data fields
        for line in file:
            timestamp_str, price_str, volume_str, _, _ = line.strip().split(',')
            # Convert strings to appropriate data types
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
            price = float(price_str)
            volume = int(volume_str)
            # Store the data as a dictionary in the list
            data.append({'timestamp': timestamp, 'price': price, 'volume': volume})

    return data

# Define a function to generate tick bars
def calculate_tick_bars(data, tick_threshold):
    """
    Generates tick bars from tick data based on a specified tick threshold.

    Args:
        data (list): List of tick dictionaries.
        tick_threshold (int): Number of ticks required for a new tick bar.

    Returns:
        list: List of tick bar dictionaries.
    """
    tick_bars = []
    current_bar = None
    accumulated_ticks = 0

    for trade in data:
        if current_bar is None:
            # Start a new tick bar
            current_bar = {'timestamp': trade['timestamp'], 'open': trade['price'], 'high': trade['price'],
                           'low': trade['price'], 'close': None, 'volume': trade['volume']}
        else:
            # Update the high and low prices of the current tick bar
            current_bar['high'] = max(current_bar['high'], trade['price'])
            current_bar['low'] = min(current_bar['low'], trade['price'])
            # Accumulate volume for the current tick bar
            current_bar['volume'] += trade['volume']

        accumulated_ticks += 1

        # Check if the accumulated ticks reach the threshold
        if accumulated_ticks >= tick_threshold:
            # Set the close price and timestamp for the tick bar
            current_bar['close'] = trade['price']  # Set the close price to the current trade's price
            current_bar['timestamp'] = trade['timestamp']  # Update the timestamp
            # Add the completed tick bar to the list
            tick_bars.append(current_bar)
            # Reset variables for the next tick bar
            current_bar = None
            accumulated_ticks = 0
    # print(tick_bars)

    return tick_bars

# Define a function to generate time-based OHLC bars
def generate_ohlc_bars(data, time_threshold_seconds):
    bars = []
    current_bar = None
    time_threshold = timedelta(seconds=time_threshold_seconds)

    for tick in data:
        tick_timestamp = tick['timestamp']
        # Round the timestamp to the nearest time_threshold interval
        rounded_timestamp = tick_timestamp + timedelta(
            seconds=(math.ceil((tick_timestamp - tick_timestamp.replace(microsecond=0)).total_seconds() / time_threshold.total_seconds())) * time_threshold.total_seconds())

        if current_bar is None or rounded_timestamp - current_bar['timestamp'] >= time_threshold:
            if current_bar is not None:
                bars.append(current_bar)
            # Start a new OHLC bar with the rounded timestamp
            current_bar = {
                'timestamp': rounded_timestamp,
                'open': tick['price'],
                'high': tick['price'],
                'low': tick['price'],
                'close': tick['price'],
                'volume': tick['volume']
            }
        # Update the high, low, and close prices of the current bar
        else:
            current_bar['high'] = max(current_bar['high'], tick['price'])
            current_bar['low'] = min(current_bar['low'], tick['price'])
            current_bar['close'] = tick['price']
            current_bar['volume'] += tick['volume']

    if current_bar is not None:
        bars.append(current_bar)
    # Convert the OHLC bars into a format suitable for further processing
    start_time = data[0]['timestamp']
    end_time = data[-1]['timestamp']
    time_index = pd.date_range(start_time, end_time, freq=f"{time_threshold_seconds}S")

    # Create an empty DataFrame with the time index
    output_df = pd.DataFrame(index=time_index)

    # Iterate through the original data and populate the output_df
    for entry in bars:
        # Convert Pandas Timestamp to standard Python datetime
        rounded_timestamp = start_time + timedelta(
            seconds=(entry['timestamp'] - start_time).seconds // time_threshold_seconds * time_threshold_seconds + time_threshold_seconds)

        if rounded_timestamp not in output_df.index:
            output_df.loc[rounded_timestamp] = None

        output_df.loc[rounded_timestamp, ['open', 'high', 'low', 'close', 'volume']] = [
            entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']
        ]

    output_data = []

    for timestamp, row in output_df.iterrows():
        if not row.isnull().all():
            data_entry = {
                'timestamp': timestamp.to_pydatetime(),  # Convert Pandas Timestamp to datetime.datetime
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            }
            output_data.append(data_entry)

    return output_data

# Define a function to generate volume bars
def create_volume_bars(data, threshold):
    """
    Generates volume bars from tick data based on a specified volume threshold.

    Args:
        data (list): List of tick dictionaries.
        threshold (int): Minimum volume required for a new volume bar.

    Returns:
        list: List of volume bar dictionaries.
    """
    bars = []
    current_bar = None

    for tick in data:
        if current_bar is None:
            # Start a new volume bar
            current_bar = {
                'timestamp': tick['timestamp'],
                'open': tick['price'],
                'high': tick['price'],
                'low': tick['price'],
                'close': tick['price'],
                'volume': tick['volume']
            }
        # Update the high, low, and close prices of the current volume bar
        else:
            current_bar['high'] = max(current_bar['high'], tick['price'])
            current_bar['low'] = min(current_bar['low'], tick['price'])
            current_bar['close'] = tick['price']
            current_bar['volume'] += tick['volume']
        # Check if the accumulated volume reaches the threshold
        if current_bar['volume'] >= threshold:
            # Update the timestamp to the last tick's timestamp
            current_bar['timestamp'] = tick['timestamp']  # Update timestamp to the last tick's timestamp
            # Add the completed volume bar to the list
            bars.append(dict(current_bar))
            # Reset volume for the next volume bar
            current_bar = {
                'timestamp': tick['timestamp'],
                'open': tick['price'],
                'high': tick['price'],
                'low': tick['price'],
                'close': tick['price'],
                'volume': 0
            }

    return bars

# Main execution starts here
if __name__ == '__main__':
    # Read tick data from a CSV file
    data = read_data('googl_trade_2023_05_12.txt')
#     # print(data)
#     data = [
#             {'timestamp': datetime(2023,8,1,0,0,0), 'price': 10, 'volume': 1},
#             {'timestamp': datetime(2023,8,1,0,0,1), 'price': 11, 'volume': 5},
#             {'timestamp': datetime(2023,8,1,0,0,3), 'price': 9, 'volume': 3},
#             {'timestamp': datetime(2023,8,1,0,0,4), 'price': 10, 'volume': 2},
#             {'timestamp': datetime(2023,8,1,0,0,9), 'price': 12, 'volume': 3},]
#
    # Generate tick bars using the tick data and threshold
    tick_threshold = 3
    tick_bars = calculate_tick_bars(data, tick_threshold)
    print(tick_bars)
#
    # Generate time-based OHLC bars using the tick data and time threshold
    time_threshold_seconds = 2
    bars = generate_ohlc_bars(data, time_threshold_seconds)
    print(bars)
    # Generate volume bars using the tick data and volume threshold
    volume_threshold = 5
    volume_bars = create_volume_bars(data, volume_threshold)
    print(volume_bars)
