"""
    LOAD DATA and CLEAN DATA
"""
import os
import random
import pandas as pd


# -- Load file --
FILE_PATH = os.path.join("dataset", "main_data.csv")
df = pd.read_csv(FILE_PATH)


# -- Choose features --
# col = ['trip_id', 'start_stop_id', 'arrival_time', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id',
#        'direction_id', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id', 'distance_m']
# df = df[col]


# -- Convert 'arrival-time' object to datetime64[ns] --
# df['arrival_time'] = pd.to_datetime(df['arrival_time'].dt.strftime('%H:%M:%S'))
df['arrival_time'] = pd.to_datetime(df['arrival_time'])


# -- Sort by 'direction_id' and 'trip_id' to categorize by bus trip and by its direction (left or right) --
df = df.sort_values(by=['direction_id', 'trip_id'], ascending=[True, True])


# -- Create 'decisive_speed' attributes to determine the 'congestion_level' --
df['decisive_speed'] = df.apply(lambda row, weight=random.uniform(0.8, 0.9): (
        row['speed_kmh'] * weight + row['segment_max_speed_kmh'] * (1 - weight)), axis=1)
conditions = [
    (df['decisive_speed'] > 40),
    (df['decisive_speed'] > 30),
    (df['decisive_speed'] > 20),
    (df['decisive_speed'] > 15)
]
congestion_levels = [0, 1, 2, 3]
df['congestion_level'] = pd.np.select(conditions, congestion_levels, default=4)
df = df.drop(['decisive_speed'], axis=1)
df = df.drop_duplicates(
    subset=['trip_id', 'start_stop_id', 'arrival_time', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id',
            'direction_id', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id'])

# -- Group the DataFrame by 'trip_id' and 'direction_id' for slicing and processing on each sub-dataset --
df_sorted = df.sort_values(['trip_id', 'direction_id'])
grouped = df_sorted.groupby(['trip_id', 'direction_id'])


# -- Create new columns called 'next_lat' and 'next_lon' --
subdatasets = []

for key, subdataset in grouped:
    # Sort the subdataset by 'arrival_time' to ensure the correct order
    subdataset = subdataset.sort_values('arrival_time')

    # Use .shift() to get the next latitude and longitude values
    subdataset['next_lat'] = subdataset['stop_lat'].shift(-1)
    subdataset['next_lon'] = subdataset['stop_lon'].shift(-1)

    # Replace 'NaN' in the last row of 'next_lat' and 'next_lon' with the current values
    subdataset['next_lat'].fillna(subdataset['stop_lat'].iloc[-1], inplace=True)
    subdataset['next_lon'].fillna(subdataset['stop_lon'].iloc[-1], inplace=True)

    # Append the modified subdataset to the list
    subdatasets.append(subdataset)

# Concatenate the modified subdatasets into one dataset
merged_dataset = pd.concat(subdatasets, ignore_index=True)

# Reset the index of the merged dataset
merged_dataset.reset_index(drop=True, inplace=True)

# Update the DataFrame
df = merged_dataset



# -- Update 'arrival_time' the previous time with the 'runtime-sec' --
grouped = df.groupby(['trip_id', 'direction_id'])

sub_datasets = {group_name: group_df for group_name, group_df in grouped}
dataset = []
# Access the sub-datasets as needed
for key, sub_dataset in sub_datasets.items():
    # print(f"Sub-dataset for {key}:")
    # Reset the index of the sub-dataset
    sub_dataset = sub_dataset.reset_index(drop=True)

    calculated_arrival_times = []

    for idx in range(len(sub_dataset)):
        if idx < 1:
            # For the first two rows, use the original 'arrival_time' values
            calculated_arrival_times.append(sub_dataset['arrival_time'].iloc[idx])
        else:
            # For subsequent rows, calculate the 'arrival_time' based on the two previous rows
            previous_arrival_time = calculated_arrival_times[idx - 1]
            previous_runtime = sub_dataset['runtime_sec'].iloc[idx - 1]
            new_arrival_time = previous_arrival_time + pd.to_timedelta(previous_runtime, unit='s')
            calculated_arrival_times.append(new_arrival_time)

    # Replace the original 'arrival_time' column with the calculated values
    sub_dataset['arrival_time'] = calculated_arrival_times
    dataset.append(sub_dataset)
# Concatenate all sub-datasets into one dataset
merged_dataset = pd.concat(dataset, ignore_index=True)

# Reset the index of the merged dataset
merged_dataset.reset_index(drop=True, inplace=True)

df = merged_dataset

# -- Create 'arrival_hour' and 'arrival_minute' --
df = df[[
    'trip_id', 'start_stop_id', 'arrival_time', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id', 'direction_id',
    'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id', 'distance_m', 'next_lat', 'next_lon',
    'congestion_level']]

df['arrival_hour'] = df['arrival_time'].dt.hour
df['arrival_minute'] = df['arrival_time'].dt.minute

df = df[['trip_id', 'start_stop_id', 'arrival_time', 'arrival_hour', 'arrival_minute', 'stop_sequence_x', 'stop_lat',
         'stop_lon', 'route_id', 'direction_id', 'runtime_sec', 'end_stop_id', 'next_lat', 'next_lon', 'congestion_level']]

df = df.sort_values(by=['trip_id','arrival_time'])
df = df.sort_values(by=['trip_id','direction_id'])

# df = df.sort_values(by=['arrival_time'])

# print(df.info())
df.to_csv(os.path.join("dataset", "pre_processed_data.csv"), index=False)
print(df.info())