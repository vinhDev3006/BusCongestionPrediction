import os
import random

import numpy as np
import pandas as pd
from keras.losses import mean_squared_error
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

"""
    LOAD DATA
"""
FILE_PATH = os.path.join("dataset", "main_data.csv")
df = pd.read_csv(FILE_PATH)

"""
    CLEAN DATA
"""
col = ['trip_id', 'start_stop_id', 'arrival_time', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id',
       'direction_id', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id', 'distance_m']
df = df[col]

# df['arrival_time'] = pd.to_datetime(df['arrival_time'].dt.strftime('%H:%M:%S'))
df['arrival_time'] = pd.to_datetime(df['arrival_time'])

df = df.sort_values(by=['direction_id', 'trip_id'], ascending=[True, True])
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

# Sort the DataFrame by 'trip_id' and 'direction_id' columns
df_sorted = df.sort_values(['trip_id', 'direction_id'])

# Group the sorted DataFrame by 'trip_id' and 'direction_id'
grouped = df_sorted.groupby(['trip_id', 'direction_id'])

# Create a list to store the modified DataFrames
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

# Print the merged dataset
df = merged_dataset

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

df = df[[
    'trip_id', 'start_stop_id', 'arrival_time', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id', 'direction_id', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id', 'distance_m', 'next_lat', 'next_lon', 'congestion_level']]


df['arrival_hour'] = df['arrival_time'].dt.hour
df['arrival_minute'] = df['arrival_time'].dt.minute

df = df[['trip_id', 'start_stop_id', 'arrival_time', 'arrival_hour', 'arrival_minute', 'stop_sequence_x', 'stop_lat', 'stop_lon', 'route_id', 'direction_id', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'end_stop_id', 'distance_m', 'next_lat', 'next_lon', 'congestion_level']]


# df = df.sort_values(by=['trip_id','arrival_time'])
# df = df.sort_values(by=['trip_id','direction_id'])


df['arrival_time'] = pd.to_datetime(df['arrival_time'])
df = df.sort_values(by=['arrival_time'])

# print(df.info())
df.to_csv('new.csv', index=True)

"""
    MACHINE LEARNING
"""
# Select features and target
X = df[['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon', 'speed_kmh', 'segment_max_speed_kmh', 'runtime_sec', 'direction_id', 'distance_m']]
Y = df['congestion_level']

# Normalize feature data
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Define the sequence length
seq_length = 5  # You can adjust this based on your data

X_seq, Y_seq = [], []

# Generate sequences
for i in range(len(X) - seq_length):
    X_seq.append(X[i:i+seq_length])
    Y_seq.append(Y[i+seq_length])

X_seq = np.array(X_seq)
Y_seq = np.array(Y_seq)

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X_seq, Y_seq, test_size=0.4, random_state=42)

# Build the LSTM model
model = keras.Sequential([
    keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, X.shape[1])),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, Y_train, epochs=1000, batch_size=64)

# Evaluate the model on the test set
Y_pred = model.predict(X_test)
Y_test_1d = Y_test.reshape(-1)  # Reshape to a 1D array
Y_pred_1d = Y_pred.reshape(-1)  # Reshape to a 1D array
mse = mean_squared_error(Y_test_1d, Y_pred_1d)
print(f"Mean Squared Error: {mse}")

# Inference with the model (e.g., make predictions for future congestion levels)
# Prepare your input data accordingly and use model.predict()

# Example for making predictions
# Replace this example with your own input data
# input_data = X_test[:100]  # Adjust the slice as needed
# predicted_congestion = model.predict(input_data)
#
# print("Predicted Congestion Level:", predicted_congestion)
#
# # Plot the predicted and actual congestion levels
# plt.figure(figsize=(12, 6))
# plt.plot(Y_test[:100], label="Actual Congestion")
# plt.plot(predicted_congestion, label="Predicted Congestion")
# plt.legend()
# plt.xlabel("Time Steps")
# plt.ylabel("Congestion Level")
# plt.title("Actual vs. Predicted Congestion Levels")
# plt.show()
